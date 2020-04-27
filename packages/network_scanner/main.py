from __future__ import absolute_import
import inquirer
from inquirer import errors
import ipaddress
from packages.network_scanner.network_scanner import *

def validate_ip(answers, current):
    """
    Accepts as input a valid ipv4 or ipv6 IP address with optional subnet range.
    Validates given IP and range, raises an exception if IP/range is invalid.
    """
    ip_arr = current.split("/")
    if (len(ip_arr) == 2):
        ip_range = ip_arr[1]
        # validate ip_range
    ip_address = ip_arr[0]
    try:
        ip = (u"{ip}").format(ip=ip_address)
        ipaddress.ip_address(ip)
        return True
    except:
        raise errors.ValidationError('', reason=f"[-] Invalid IP address format.")

def main():
    try:
        questions = [
            inquirer.Text("ip_range_input", message="Enter IP address and/or range to scan (e.g. 10.0.0.1/24)", validate=validate_ip)
        ]
        answers = inquirer.prompt(questions)
        ip_range_input = answers["ip_range_input"]
        scanner = Network_Scanner(ip_range_input)
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Network Scanner terminated by user.\n")
    
if __name__ == "__main__":
    main()

# "Scan a given network range for all connected clients' IP and MAC addresses."