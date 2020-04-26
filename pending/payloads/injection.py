#!/usr/bin/env python
import requests

def injection(url):
    """
    Pulls file from given URL.
    """
    file_name = url.split("/")[-1]
    get_response = requests.get(url)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)