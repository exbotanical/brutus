"""This module implements a base class for all Brutus modules
"""
import socket


class BaseBrutusModule:
    """The BaseBrutusModule base class carries metadata common to all modules"""

    def __init__(
        self,
        requires_mitm_state: bool = False,
        same_network_as_target: bool = False,
        multiprocessing: bool = False,
        strip_ssl: bool = False,
        needs_port_fwd: bool = False,
    ) -> None:

        # does the module require the user to be in a MITM state?
        self.requires_mitm_state = requires_mitm_state

        # does the module require the user to be on the same network as the target?
        self.requires_same_network_as_target = same_network_as_target

        # do we need to run this module in a parallel process?
        self.needs_own_process = multiprocessing

        # does the module require downgrading SSL connections?
        self.downgrade_https = strip_ssl

        # do we need port forwarding to be enabled?
        self.needs_port_fwd = needs_port_fwd

    @staticmethod
    def get_interfaces() -> list:
        """Retrieve a list of present network interface names

        Returns:
            list: interface names
        """
        return [i[1] for i in socket.if_nameindex()]
