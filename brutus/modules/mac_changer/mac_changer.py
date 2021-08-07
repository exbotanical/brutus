"""
This module comprises an API for changing network devices' MAC addresses
"""
import fcntl
import re
import socket
import struct
import subprocess

from brutus.utils.generators import generate_n_ints

# colon-delimited MAC address
MACADDR_REGEX = '[0-9a-f]{2}(:)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$'


def get_interfaces() -> list:
    """Retrieve a list of present network interface names

    Returns:
        list: tuples of interface names, indices
    """
    return socket.if_nameindex()


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


def change_mac_address(interface: str, new_macaddr: str) -> None:
    """Uses ifconfig to reassign a given device's MAC address

    Args:
        interface (str): the network interface name
        new_macaddr (str): colon-delimited octet MAC address
            to assign to the interface
    """
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_macaddr])
    subprocess.call(['ifconfig', interface, 'up'])


def validate_macaddr_persistence(interface, new_macaddr) -> bool:
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
    current_addr = get_current_macaddr(interface)

    return current_addr == new_macaddr


def validate_macaddr_format(new_macaddr: str) -> bool:
    """Basic validation of the MAC address format as a
    series of colon-delimited octet values

    Args:
        new_macaddr (str): colon-delimited octet MAC address
            to validate on the interface

    Returns:
        bool: valid format?
    """
    valid_mac_res = re.search(MACADDR_REGEX, new_macaddr)
    return valid_mac_res is not None


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
        multicast (bool, optional): should the address be multicast? Defaults to False.
        uaa (bool, optional): should the address be UAA? Defaults to False.

    Returns:
        str: generated MAC address
    """

    delimiter = ':'

    if oui is not None and re.search(r'\w\w:\w\w:\w\w', oui) is not None:
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


def get_vendor_prefixes():
    """Pending implementation"""
