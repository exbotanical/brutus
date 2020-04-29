#!/usr/bin/env python3

import requests 

base_url = "google.com"
wordlist = "subdomains.txt"
timeout = 1

def request(url):
    try:
        return requests.get("http://" + url, timeout=timeout)
    except (requests.exceptions.ConnectionError):
        pass
    except (requests.exceptions.InvalidURL):
        pass
    except (requests.exceptions.Timeout):
        pass
    
with open(wordlist, "r") as wordlist_stream:
    for line in wordlist_stream:
        subdomain = line.strip()
        ephemeral_url = f"{subdomain}.{base_url}"
        response = request(ephemeral_url)
        if (response):
            print(f"[+] Discovered subdomain --> {ephemeral_url}")