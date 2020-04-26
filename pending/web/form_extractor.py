#!/usr/bin/env python

import requests 
from bs4 import BeautifulSoup
import urlparse

base_url = "http://iberianodonataucm.myspecies.info/"

def request(url):
    try:
        return requests.get(url, timeout=1)
    except (requests.exceptions.ConnectionError):
        pass


response = request(base_url)
parsed_html = BeautifulSoup(response.content,features="html.parser")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(base_url, action)
    method = form.get("method")

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if (input_type == "text"):
            input_value = "test"
        
        post_data[input_name] = input_value
    res = requests.post(post_url, data=post_data)
    print(res.content)
