TODO

- Make setup script that installs requirements.txt, sslstrip, and chmod all shell scripts.
add downgrade https module


INSTALL

sslstrip
iptables
pip3 install -U git+https://github.com/kti/python-netfilterqueue
pip3 install inquirer
pip3 install 

ERRORS:
sslstrip raises exceptions on POSTs 
This is actually quite easy to fix.
These are just warnings and they can be ignored for a cleaner output of SSLstrip.

Open up the ServerConnection.py file from SSLStrip and look for this function call :  HTTPClient.handleResponsePart(self, data)  and this one: HTTPClient.handleResponseEnd(self)

Just add a try/except around these calls like so:

try:
    HTTPClient.handleResponsePart(self, data)
except:
    pass

TODO
add write to file option on scanners
fix wordlist path
make http/https path resolution auto in spider/link harvester
elucidate requirements in inquirer prompts
color output
error handling
variables
