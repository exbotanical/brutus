#!/usr/bin/env python

import requests
import re
import urlparse
from bs4 import BeautifulSoup

HREF_REGEX = '(?:href=")(.*?)"'
XSS_SIMULACRUM = "<sCript>alert('test')</scriPt>"
SQLI_SIMULACRA = ["'", "' or 1=1;--", "1\' or \'1\' = \'1\''", "' or 1=1--","' or 1=1#","' or 1=1/*","') or '1'='1--", "') or ('1'='1--"]

class Scanner:
    def __init__(self, url, ignore_list):
        self.session = requests.Session()
        self.target_url = url
        self.harvested_links = []
        self.ignore_list = ignore_list

    def link_extraction(self, url):
        """
        Parses a given URL and returns all href links.
        """
        response = self.session.get(url)
        return re.findall(HREF_REGEX, response.content)
    
    def form_extraction(self, url):
        """
        Parses a given URL and returns all forms.
        """
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content,features="html.parser")
        return parsed_html.findAll("form")
    
    def form_submission(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")

        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if (input_type == "text"):
                input_value = value
            
            post_data[input_name] = input_value
        # requests lib doesn't have a JS adapter and Selenium is too slow, so skip JS for now...
        if (action is not None and "javascript" not in action):
            if (method == "post"):
                return self.session.post(post_url, data=post_data)
            return self.session.get(post_url, params=post_data)

    def crawl(self, url=None):
        """
        Primary method initiates a full recursive scan of the provided base URL
        and renders sitemap (optionally inside of a session).
        """
        if (url == None):
            url = self.target_url
        href_links = self.link_extraction(url)
        for link in href_links: 
            link = urlparse.urljoin(url, link)
            if ("#" in link): # rm anchors
                link = link.split("#")[0]
            if (self.target_url in link and link not in self.harvested_links and link not in self.ignore_list):
                self.harvested_links.append(link)
                print("[+] New URL Found --> {i}").format(i=link)
                self.crawl(link) # recursively crawl everything
    
    def initiate_scan(self):
        """
        Pulls sitemap and evaluates each discovered node for 
        vulnerabilities, as defined in the below class methods.
        """
        for link in self.harvested_links:
            forms = self.form_extraction(link)
            for form in forms:
                print("[+] Beginning POST evaluation for {i}").format(i=link)
                is_vuln_to_xss = self.eval_xss_form(form, link)
                if (is_vuln_to_xss):
                    print("\n[*] XSS Vulnerability found at {i}, in the following form: ").format(i=link)
                    print(form + "\n")
            if ("=" in link): # fix for more comprehensive targeting
                print("[+] Beginning GET evaluation for {i}").format(i=link)
                is_vuln_to_xss = self.eval_xss_link(link)
                if (is_vuln_to_xss):
                    print("\n[*] XSS Vulnerability found in URL params at {i}\n").format(i=link)
                for simulacrum in SQLI_SIMULACRA:
                    is_vuln_to_sqli = self.eval_tautological_sqli_link(link, simulacrum)
                    if (is_vuln_to_sqli and "view=image" not in link):
                        print("\n[*] Tautological SQLi Vulnerability found in URL params at {i}\n").format(i=link)

    def eval_xss_link(self, url):
        """
        Evaluates XSS vulnerability via URL parameters. 
        Accepts as input target URL; returns bool.
        """
        url = url.replace("=", "=" + XSS_SIMULACRUM)
        response = self.session.get(url)
        return XSS_SIMULACRUM in response.content

    def eval_xss_form(self, form, url):
        """
        Evaluates XSS vulnerability via form submission.
        Accepts as inputs target form and cooresponding URL; returns bool.
        """
        response = self.form_submission(form, XSS_SIMULACRUM, url)
        if (response is not None):
            return XSS_SIMULACRUM in response.content
        else:
            return False
    
    def eval_tautological_sqli_link(self, url, simulacrum):
        url = url.replace(url.rsplit('=', 1)[-1], simulacrum)
        try:
            response = self.session.get(url, timeout=5)
            return "syntax" in response.content or "error" in response.content
        except (requests.exceptions.ConnectionError):
            return False
        except (requests.exceptions.InvalidURL):
            return False
        except (requests.exceptions.Timeout):
            return False