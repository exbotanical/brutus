#!/usr/bin/env python3
import subprocess

import inquirer

from packages.javascript_injector.code_injector import Injector

def main():
    try:
        questions = [
            inquirer.Text("payload", message="Enter the full Javascript payload"),
            ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        payload = answers["payload"]
        Injector(payload)
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Javascript Injector terminated by user. Flushing IP Tables...\n")
        subprocess.call(["iptables --flush"], shell=True)

if __name__ == "__main__":
    main()

# description="Automates code injection in HTTPS responses."
