"""This module contains socket utilities
"""
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
