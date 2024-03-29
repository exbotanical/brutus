"""This module implements a port scan routine, run over a non-blocking
task queue in which units of work are delegated to daemon threads

"""
import socket
from threading import Lock

from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.tasking.ThreadedTaskQueue import ThreadedTaskQueue
from brutus.utils.logger import LOGGER
from brutus.utils.networking import hostname_resolves

# prevent weird output race conditions
lock = Lock()


class PortScanner(BaseBrutusModule, ThreadedTaskQueue):
    """Initiate a port scan on `hostname` from `start_port` to `end_port`.
    Ports will be placed in a queue, then delegated to threads in a concurrent manner

    Args:
        hostname (str)
        start_port (int): Start of range
        end_port (int): End of range; inclusive
        n_threads (int): Number of threads, at maximum, to spawn

    Inherits:
        BaseBrutusModule, ThreadedTaskQueue
    """

    def __init__(
        self, hostname: str, start_port: int, end_port: int, n_threads: int
    ) -> None:
        # the ThreadedTaskQueue will push these onto the queue
        ports = [
            port for port in range(start_port, end_port)  # pylint: disable=R1721
        ]  # TODO use a lazy / async iterator or generator

        BaseBrutusModule.__init__(
            self,
            requires_mitm_state=False,
            same_network_as_target=False,
            module_path='brutus.interfaces.port_scanner.inquirer',
        )

        ThreadedTaskQueue.__init__(
            self,
            callback=self.port_scan_routine,
            arg=hostname,
            tasks=ports,
            n_threads=n_threads,
        )

    def port_scan_routine(self, port: int, hostname: str) -> None:
        """The port scan routine, to be invoked by a daemon thread

        Args:
            port (int)
            hostname (str)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((hostname, port)) == 0:
                with lock:
                    LOGGER.warning(f'{hostname}:{port} is open')

        except socket.error:
            pass

        finally:
            sock.close()

    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        """Perform a validation check to ensure the hostname resolves

        Returns:
            bool
        """
        return hostname_resolves(hostname)

    @staticmethod
    def validate_portrange(start_port: int, end_port: int) -> bool:
        """Validate the provided port range by ensuring `start_port` is less than `end_port`

        Args:
            start_port (int)
            end_port (int)

        Returns:
            bool
        """
        return start_port < end_port
