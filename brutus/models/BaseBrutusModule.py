"""This module implements a base class for all Brutus modules
"""
import socket


class BrutusModuleRequirements:  # pylint: disable=R0902
    """Describes Brutus module metadata"""

    __slots__ = (
        'module_path',
        'requires_mitm_state',
        'same_network_as_target',
        'multiprocessing',
        'strip_ssl',
        'needs_port_fwd',
    )

    def __init__(
        self,
        module_path: str,
        requires_mitm_state: bool = False,
        same_network_as_target: bool = False,
        multiprocessing: bool = False,
        strip_ssl: bool = False,
        needs_port_fwd: bool = False,
    ) -> None:
        self.module_path = module_path
        self.requires_mitm_state = requires_mitm_state
        self.same_network_as_target = same_network_as_target
        self.multiprocessing = multiprocessing
        self.strip_ssl = strip_ssl
        self.needs_port_fwd = needs_port_fwd


class BaseBrutusModule:  # pylint: disable=R0902
    """The BaseBrutusModule base class carries metadata common to all modules

    NOTE: Some of these items have not been wired up quite yet;
    take it as a challenge and open a PR!
    """

    def __init__(
        self,
        module_path: str,
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
        self.needs_downgraded_ssl = strip_ssl

        # do we need port forwarding to be enabled?
        self.needs_port_fwd = needs_port_fwd

        # exact dot-delimited submodule path of the child class
        self.module_path = module_path

        # STATE

        # has ssl been downgraded?
        self.ssl_downgraded = False

        # has port forwarding been enabled?
        self.port_fwd_enabled = False

    @staticmethod
    def get_interfaces() -> list:
        """Retrieve a list of present network interface names

        Returns:
            list: interface names
        """
        return [i[1] for i in socket.if_nameindex()]
