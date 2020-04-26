#~/usr/bin/env python

import scanner

base_url = ""
login_url = base_url
ignore_list = []
username = "" 
password = ""
data_dict = {
    "user": username, 
    "password": password,
    "submit": "Sign in"
    }

try:
    vuln_scanner = scanner.Scanner(base_url,ignore_list)
    a = vuln_scanner.session.post(login_url,data=data_dict)
    print(a.content)
    vuln_scanner.crawl()
    vuln_scanner.initiate_scan()
except KeyboardInterrupt:
    print("\n\n[x] Program terminated by user.")

# fun links
# http://iberianodonataucm.myspecies.info/
# http://testing-ground.scraping.pro/login
# https://scrapethissite.com/
# http://hmrc.hackxor.net