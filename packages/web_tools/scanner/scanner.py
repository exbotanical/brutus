#!/usr/bin/env python3
import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

HREF_REGEX = '(?:href=")(.*?)"'
XSS_SIMULACRUM = "<sCript>alert('test')</scriPt>"
SQLI_SIMULACRA = ["'", "' or 1=1;--", "1\' or \'1\' = \'1\''", "' or 1=1--","' or 1=1#","' or 1=1/*","') or '1'='1--", "') or ('1'='1--"]

class Scanner:
    def __init__(self, url, ignore_list, login_url=None, username=None, password=None):
        self.session = requests.Session()
        self.target_url = url
        self.harvested_links = []
        self.ignore_list = ignore_list
        self.login_url = login_url
        self.username = username
        self.password = password
        if (self.username != None):
            session = self.session.post(self.login_url, 
            data={"username": self.username,"password": self.password,"submit": "Sign in"})
            print(f"[+] Session initialized for: {self.target_url}")
        else:
            print("[+] Sessionless scanner initialized.")
        print(f"[+] Beginning crawl at: {self.target_url}")
        self.crawl()
        self.initiate_scan()

    def link_extraction(self, url):
        """
        Parses a given URL and returns all href links.
        """
        
        response = self.session.get(url)
        return re.findall(HREF_REGEX, str(response.content))

    def form_extraction(self, url):
        """
        Parses a given URL and returns all forms.
        """
        response = self.session.get(url)
        parsed_html = BeautifulSoup(str(response.content),features="html.parser")
        return parsed_html.findAll("form")
    
    def form_submission(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
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
            link = urljoin(url, link)
            if ("#" in link): # rm anchors
                link = link.split("#")[0]
            if (self.target_url in link and link not in self.harvested_links and link not in self.ignore_list):
                self.harvested_links.append(link)
                print(f"[+] New URL Found --> {link}")
                self.crawl(link) # recursively crawl everything
    
    def initiate_scan(self):
        """
        Pulls sitemap and evaluates each discovered node for 
        vulnerabilities, as defined in the below class methods.
        """
        for link in self.harvested_links:
            forms = self.form_extraction(link)
            for form in forms:
                print(f"[+] Beginning POST evaluation for {link}")
                is_vuln_to_xss = self.eval_xss_form(form, link)
                if (is_vuln_to_xss):
                    print(f"\n[*] XSS Vulnerability found at {link}, in the following form: ")
                    print(form + "\n")
            if ("=" in link): # fix for more comprehensive targeting
                print(f"[+] Beginning GET evaluation for {link}")
                is_vuln_to_xss = self.eval_xss_link(link)
                if (is_vuln_to_xss):
                    print(f"[*] XSS Vulnerability found in URL params at {link}\n")
                for simulacrum in SQLI_SIMULACRA:
                    is_vuln_to_sqli = self.eval_tautological_sqli_link(link, simulacrum)
                    if (is_vuln_to_sqli and "view=image" not in link):
                        print(f"[*] Tautological SQLi Vulnerability found in URL params at {link}\n")
        print(f"[+] Eval of {self.target_url} complete.\n")

    def eval_xss_link(self, url):
        """
        Evaluates XSS vulnerability via URL parameters. 
        Accepts as input target URL; returns bool.
        """
        url = url.replace("=", "=" + XSS_SIMULACRUM)
        response = self.session.get(url)
        return XSS_SIMULACRUM in str(response.content)

    def eval_xss_form(self, form, url):
        """
        Evaluates XSS vulnerability via form submission.
        Accepts as inputs target form and cooresponding URL; returns bool.
        """
        response = self.form_submission(form, XSS_SIMULACRUM, url)
        if (response is not None):
            return XSS_SIMULACRUM in str(response.content)
        else:
            return False
    
    def eval_tautological_sqli_link(self, url, simulacrum):
        url = url.replace(url.rsplit('=', 1)[-1], simulacrum)
        try:
            response = self.session.get(url, timeout=5)
            return "syntax" in str(response.content) or "error" in str(response.content)
        except (requests.exceptions.ConnectionError):
            return False
        except (requests.exceptions.InvalidURL):
            return False
        except (requests.exceptions.Timeout):
            return False