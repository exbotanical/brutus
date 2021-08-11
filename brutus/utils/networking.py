"""This module contains networking utilities
"""
import ipaddress
import socket


def hostname_resolves(hostname: str) -> bool:
    """Return a boolean indicating whether the given hostname can be resolved

    Args:
        hostname (str)

    Returns:
        bool
    """
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False


def ipaddr_valid(ipaddr: str) -> bool:
    """Validate an IP address' validity

    Args:
        ipaddr (str)

    Returns:
        bool
    """
    # min length 1.1.1.1
    if len(ipaddr) < 7:
        return False

    try:
        ipaddress.ip_address(ipaddr)
        return True
    except ValueError:
        return False
