NOTE: This project is currently in development. As such, I'm not even bothering with markdown at the moment. Hence, you'll notice the following is a rather ugly doc. See my other repositories for examples of my documentation.

CONTRIBUTING:
Brutus is an open-source project; anyone can contribute. Please keep in mind the goal of Brutus is not to create a tool which performs better than those popular with the OWASP, et al communities, but to programatically define operations manually. As such, I appreciate contributions with this in mind.

Second, please note that this project first began as several, disparate Python 2 scripts. Aggregating them into am object-oriented framework, handling cross-platform interoperability, and updating to Python 3 has neither been easy nor linear. It's a hectic road, and any contributions to the effect of correcting errors which have been made in this process is helpful.


TODO
- Supplant subprocess calls with OS library for better cross-platform interoperability
- Make setup script that installs requirements.txt, sslstrip, and chmod all shell scripts.
- add downgrade https module
- add write to file option on scanners
- fix wordlist path resolution
- elucidate requirements in inquirer prompts
- color output
- error handling
- add test suite

CHANGELOG
- 29 April: Scanner (web), add new method to eval db-contingent resolutions of tautological, SQLi-injected URLs.

Odd Dependencies I need to account for and for which I should probably add automated install:
- sslstrip
- iptables
- pip3 install -U git+https://github.com/kti/python-netfilterqueue


KNOWN ERRORS:

sslstrip raises exceptions on POSTs 
This is actually quite easy to fix.
These are just warnings and they can be ignored for a cleaner output of SSLstrip.

Open up the ServerConnection.py file from SSLStrip and look for this function call :  HTTPClient.handleResponsePart(self, data)  and this one: HTTPClient.handleResponseEnd(self)

Just add a try/except around these calls like so:
```
try:
    HTTPClient.handleResponsePart(self, data)
except:
    pass
```
