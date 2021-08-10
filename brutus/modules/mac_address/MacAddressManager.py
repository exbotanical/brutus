"""
This module comprises an API for changing network devices' MAC addresses
"""
import fcntl
import re
import socket
import struct
import subprocess

from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.utils.generators import generate_n_ints

# colon-delimited MAC address
MACADDR_REGEX = '^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
OUI_REGEX = '^([0-9A-Fa-f]{2}:){2}([0-9A-Fa-f]{2})$'


class MacAddressManager(BaseBrutusModule):
    """Couples functionality for MAC Address management along with associated
    metadata for Brutus module categorization

    Inherits:
        BaseBrutusModule
    """

    def __init__(self):
        super().__init__(self, requires_mitm_state=False, same_network_as_target=False)

    @staticmethod
    def get_current_macaddr(interface: str) -> str:
        """Get the MAC address for the given network interface
        r
            Args:
                interface (str): the network interface name

            Returns:
                str: colon-delimited octet MAC address
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # it's a system call, but we'd rather deal with this than fork a new process
        datum = fcntl.ioctl(
            sock.fileno(), 0x8927, struct.pack('256s', bytes(interface, 'utf-8')[:15])
        )

        return ':'.join('%02x' % b for b in datum[18:24])

    @staticmethod
    def change_macaddr(interface: str, new_macaddr: str) -> None:
        """Uses ifconfig to reassign a given device's MAC address

        Args:
            interface (str): the network interface name
            new_macaddr (str): colon-delimited octet MAC address
                to assign to the interface
        """
        subprocess.call(['ifconfig', interface, 'down'])
        subprocess.call(['ifconfig', interface, 'hw', 'ether', new_macaddr])
        subprocess.call(['ifconfig', interface, 'up'])

    @staticmethod
    def validate_macaddr_persistence(interface: str, new_macaddr: str) -> bool:
        """
        Validates whether the provided MAC address
        persisted on the interface

        Args:
            interface (str): the network interface name
            new_macaddr (str): colon-delimited octet MAC address
                to validate on the interface

        Returns:
            bool: persistence status
        """
        current_addr = MacAddressManager.get_current_macaddr(interface)

        return current_addr == new_macaddr

    @staticmethod
    def validate_macaddr_format(new_macaddr: str) -> bool:
        """Basic validation of the MAC address format as a
        series of colon-delimited octet values

        Args:
            new_macaddr (str): colon-delimited octet MAC address
                to validate on the interface

        Returns:
            bool: valid format?
        """

        is_valid = re.search(MACADDR_REGEX, new_macaddr)
        return is_valid is not None

    @staticmethod
    def validate_oui_format(oui: str) -> bool:
        """Basic validation of the OUI format as a
        series of colon-delimited octet values

        Args:
            oui (str): colon-delimited octet OUI
                to validate

        Returns:
            bool: valid format?

        TODO:
            validate uaa/laa/(multi|uni)cast bit(s)
        """
        is_valid = re.search(OUI_REGEX, oui)
        return is_valid is not None

    @staticmethod
    def generate_macaddr(
        oui: str = None, multicast: bool = False, uaa: bool = False
    ) -> str:
        """Generates a MAC address either:
        (a) entirely (defaults unicast, LAA),
        (b) with a specified vendor prefix (OUI),
        (c) with multicast and/or UAA IEEE specifications

        OUI: Or vendor prefix. The first three octets, identifies the organization
            e.g. Cisco that issued the identifier
        LAA: Or U/L bit. Assigns second LSB of the first octet to 1,
            indicating the device address is locally administered.
        Unicast: First octet, or I/G bit, is set to zero.
            The device may be ignored, unless in promiscuous mode.
        Multicast: The LSB of the first octet is set to 1.

        Args:
            oui (str, optional): the vendor prefix to use. Defaults to None.
            multicast (bool, optional): should the address be multicast?
                Defaults to False.
            uaa (bool, optional): should the address be UAA? Defaults to False.

        Returns:
            str: generated MAC address
        """

        delimiter = ':'

        if isinstance(oui, str) and MacAddressManager.validate_oui_format(oui):
            # convert OUI to bytes
            byte_oui = [int(chunk, 16) for chunk in oui.split(delimiter)]

            rand_ints = byte_oui + generate_n_ints(num=6 - len(byte_oui))

        else:
            # we'll use these as a base
            rand_ints = generate_n_ints()

            if multicast:
                # set LSB of first octet to 1
                rand_ints[0] |= 1
            # unicast
            else:
                # complement I/G bit to 0
                rand_ints[0] &= ~1
            if uaa:
                # shift bit 1
                rand_ints[0] &= ~(1 << 1)
            # LAA
            else:
                rand_ints[0] |= 1 << 1

        random_mac = delimiter.join(map(lambda x: '%02x' % x, rand_ints))

        return random_mac

    @staticmethod
    def get_vendor_prefixes():
        """Pending implementation"""
