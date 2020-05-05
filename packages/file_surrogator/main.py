#!/usr/bin/env python3
import subprocess

import inquirer

from packages.file_surrogator.file_surrogation import Surrogator

def main():
    try:
        questions = [
            inquirer.Text("redirect_url", message="Enter the full URL path for file redirect"),
            inquirer.Text("target_extension", message="Enter a file extension to target for surrogation (e.g. `--type .exe`)")
            ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        redirect_url = answers["redirect_url"]
        target_extension = answers["target_extension"]
        Surrogator(redirect_url, target_extension)
        
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] File Surrogator terminated by user. Flushing IP Tables...\n")
        subprocess.call(["iptables --flush"], shell=True)

if __name__ == "__main__":
    main()

# description="Intercepts a given type of file download by surrogating said file with that provided by the user."