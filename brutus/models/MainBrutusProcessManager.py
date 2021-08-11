"""Implements a process manager for the program main thread
"""
from typing import Callable

from brutus.models.BaseBrutusModule import BrutusModuleRequirements
from brutus.tasking.ProcessPool import ProcessPool
from brutus.utils.logger import LOGGER
from brutus.utils.shell import attempt_script, spawn_new_shell


class MainBrutusProcessManager(ProcessPool):
    """Primary process pool for the main Brutus thread

    Inherits:
        ProcessPool
    """

    def __init__(self, confirm_fn: Callable, max_workers: int = 4):
        super().__init__(max_workers=max_workers)

        # confirmation function; expects a string and returns a bool
        self.confirm_fn = confirm_fn
        self.ssl_downgraded = False
        self.port_fwd_enabled = False

    def pretask_routine(self, reqs: BrutusModuleRequirements) -> None:
        """Routine to be invoked *prior* to the usage of some option
        e.g. we need port forwarding to perform an ARP spoof.

        Args:
            reqs (BrutusModuleRequirements)
        """
        if reqs.requires_mitm_state:
            LOGGER.debug(
                'you\'ll need to be in a MITM (man in the middle) state to successfully run this exploit'  # pylint: disable=C0301 # noqa:E501
            )

        if reqs.same_network_as_target:
            LOGGER.debug(
                'you\'ll need to be on the same network as the target to successfully run this exploit'  # pylint: disable=C0301 # noqa:E501
            )

        if reqs.strip_ssl and not self.ssl_downgraded:
            if self.confirm_fn(
                'you\'ll need to downgrade HTTPs to successfully run this exploit; shall we do so now?'  # pylint: disable=C0301 # noqa:E501
            ):
                if not self.downgrade_ssl():
                    LOGGER.warn('you\'ve not downgraded HTTPs - be advised')

        if reqs.needs_port_fwd and not self.port_fwd_enabled:
            if self.confirm_fn(
                'you\'ll need to enable port forwarding to successfully run this exploit; shall we do so now?'  # pylint: disable=C0301 # noqa:E501
            ):
                if not self.enable_portfwd():
                    LOGGER.warn('you\'ve not enabled port forwarding - be advised')

    def run_module(self, reqs: BrutusModuleRequirements) -> bool:
        """Run modules with the `multiprocessing` flag set.
        Dispatches these modules in a multi-processing pool to be invoked
        as a discrete process in a new shell.

        Args:
            reqs (BrutusModuleRequirements)

        Returns:
            bool
        """
        if reqs.multiprocessing:
            self.submit(spawn_new_shell, reqs.module_path)
            LOGGER.info(f'currently running {self.get_pool_usage()} processes')

            return True

        return False

    def downgrade_ssl(self) -> bool:
        """Downgrade SSL connections

        Returns:
            bool
        """
        if attempt_script('downgrade_ssl.bash'):
            # note that this sort of state management only works
            # because we know for a fact that the modules that depend on these
            # and will not run this main routine themselves
            self.ssl_downgraded = True

            LOGGER.info('successfully downgraded HTTPs')

            return True

        return False

    def enable_portfwd(self) -> bool:
        """Enable port forwarding on the host machine

        Returns:
            bool
        """
        if attempt_script('port_forward.bash'):
            self.port_fwd_enabled = True

            LOGGER.info('successfully enabled port forwarding')

            return True

        return False

    def enable_monitor_mode(self, interface: str) -> bool:
        """Enable monitor mode on the given device / interface

        Args:
            interface (str)

        Returns:
            bool
        """
        if attempt_script('monitor_mode.bash'):  # TODO
            LOGGER.info(
                f'successfully enabled monitoring mode on interface {interface}'
            )

            return True

        return False
