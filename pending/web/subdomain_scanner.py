#!/usr/bin/env python

import requests 

base_url = "google.com"
wordlist = "subdomains.txt"

def request(url):
    try:
        return requests.get("http://" + url, timeout=1)
    except (requests.exceptions.ConnectionError):
        pass
    except (requests.exceptions.InvalidURL):
        pass
    except (requests.exceptions.Timeout):
        pass
    

with open(wordlist, "r") as wordlist_stream:
    for line in wordlist_stream:
        subdomain = line.strip()
        ephemeral_url = "{a}.{b}".format(a=subdomain,b=base_url)
        response = request(ephemeral_url)
        if (response):
            print("[+] Discovered subdomain --> {i}").format(i=ephemeral_url)