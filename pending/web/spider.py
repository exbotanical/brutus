#!/usr/bin/env python

import requests 
import re
import urlparse

base_url = "https://google.com"
HREF_REGEX = '(?:href=")(.*?)"'
harvested_links = []

def link_extraction(url):
    response = requests.get(url)
    return re.findall(HREF_REGEX, response.content)

def crawl(base_url):
    href_links = link_extraction(base_url)
    for link in href_links:
        link = urlparse.urljoin(base_url, link)
        if ("#" in link): # rm anchors
            link = link.split("#")[0]
        if (base_url in link and link not in harvested_links):
            harvested_links.append(link)
            print("[+] New URL Found --> {i}").format(i=link)
            crawl(link) # recursively crawl everything
            
crawl(base_url)