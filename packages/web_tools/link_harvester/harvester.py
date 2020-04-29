#!/usr/bin/env python3
import requests 
import re
import inquirer
from urllib.parse import urljoin

HREF_REGEX = '(?:href=")(.*?)"'

class Harvester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.harvested_links = []
        self.crawl(self.target_url)
        print("[+] All links have been harvested.")

    def link_extraction(self, url):
        response = requests.get(url)
        return re.findall(HREF_REGEX, str(response.content))

    def crawl(self, url):
        href_links = self.link_extraction(url)
        for link in href_links:
            link = urljoin(url, link)
            if ("#" in link): # rm anchors
                link = link.split("#")[0]
            if (url in link and link not in self.harvested_links):
                self.harvested_links.append(link)
                print(f"[+] New URL Found --> {link}")
                self.crawl(link) # recursively crawl everything
                
