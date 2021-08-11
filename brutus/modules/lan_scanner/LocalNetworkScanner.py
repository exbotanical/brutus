"""This module exposes a LAN scanner API and reconnaissance utility

"""
import scapy.all as scapy  # type: ignore

from brutus.models.BaseBrutusModule import BaseBrutusModule


class LocalNetworkScanner(BaseBrutusModule):
    """Implements a Local Area Network scanner. Generates ARP requests and
    multicasts them to identify all IP addresses on a given network.

    Inherits:
        BaseBrutusModule
    """

    def __init__(self, ip_range: str) -> None:
        self.ip_range = ip_range

        super().__init__(
            requires_mitm_state=False,
            same_network_as_target=True,
            module_path='brutus.interfaces.lan_scanner.inquirer',
        )

    def run(self) -> list:
        """Run the ARP scan

        Returns:
            list: discovered IPs and their respective MAC addresses
        """
        # generate packet
        arp_request = scapy.ARP(pdst=self.ip_range)

        # generate ethernet frame for destination MAC address
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

        # render broadcast obj
        arp_request_broadcast = broadcast / arp_request

        # send packet w/custom ether (srp vs sr)
        acknowledged_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[
            0
        ]

        clients_list = []

        for transaction in acknowledged_list:
            clients_list.append(
                {'ip': transaction[1].psrc, 'mac': transaction[1].hwsrc}
            )

        return clients_list
