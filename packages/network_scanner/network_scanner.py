#!/usr/bin/env python3

# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.1.0

"""
*Presumes controller is on same network as target.
This scanner discovers all clients on a given network by way of 
a custom algorithm that follows as such:
i) generate ARP request directed to broadcast MAC asking for IP,
ii) send packet and receive response
iii) parse response
iv) stdout result(s)
"""

import scapy.all as scapy
import argparse
import ipaddress

class Network_Scanner:
    def __init__(self, ip_range_input):
        """
        Validates input ip_range_input upon instantiation.
        """
        self.ip_range_input = ip_range_input
        clients = self.scan(self.ip_range_input)
        res_obj = self.parse_results(clients)
        self.format_output(res_obj)
        
    def scan(self, ip_address):
        """
        Accepts as input an IP range and generates a broadcast object comprised of an 
        ARP request and ethernet frame. Sends the packet with a custom ether and elicits 
        all known IPs and associated MAC addresses, returned as a list.
        """
        # generate packet
        arp_request = scapy.ARP(pdst=ip_address)
        # generate ethernet frame for dest MAC address
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        # render broadcast obj
        arp_request_broadcast = broadcast/arp_request
        # send packet w/custom ether (srp vs sr)
        acknowledged_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return acknowledged_list

        # unacknowledged_list = scapy.srp(arp_request_broadcast, timeout=1)[1]

    def parse_results(self, acknowledged_list):
        """
        Accepts as input a list of ARP request acknowledgements, which are indexed into a
        dict with keys "IP" and "MAC". The dict is appended to the clients_list, which
        is returned. 
        """
        clients_list = []
        for transaction in acknowledged_list:
            client_dict = { "ip": transaction[1].psrc, "mac": transaction[1].hwsrc }
            clients_list.append(client_dict)
        return clients_list

    def format_output(self, clients_list):
        """
        Loops over given clients list and outputs a formatted table mapping IPs to MACs.
        """
        print("\nIP\t\t|\tMAC Address\n-----------------------------------------")
        for client in clients_list:
            ip=client["ip"]
            mac=client["mac"]
            print(f"{ip}\t\t{mac}")
        print("\n")


