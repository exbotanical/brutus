#!/usr/bin/env python3
import requests 

class Scanner:
    def __init__(self, target_url, wordlist, interval):
        self.target_url = target_url
        self.wordlist = wordlist
        self.interval = int(interval)
        self.discover_subdomain(self.wordlist, self.target_url)
        
    def request(self, url):
        try:
            return requests.get(f"https://{url}", timeout=self.interval)
        except (requests.exceptions.ConnectionError):
            pass
        except (requests.exceptions.InvalidURL):
            pass
        except (requests.exceptions.Timeout):
            pass

    def discover_subdomain(self, wordlist, url):
        with open(wordlist, "r") as wordlist_stream:
            for line in wordlist_stream:
                subdomain = line.strip()
                ephemeral_url = f"{subdomain}.{url}"
                response = self.request(ephemeral_url)
                if (response):
                    print(f"[+] Discovered subdomain --> {ephemeral_url}")