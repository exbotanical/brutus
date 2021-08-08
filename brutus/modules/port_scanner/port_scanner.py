"""This module implements a port scan routine, run over a non-blocking
task queue in which units of work are delegated to daemon threads

"""
import socket
from threading import Lock

from brutus.tasking.ThreadedTaskQueue import ThreadedTaskQueue
from brutus.utils.log import Logger
from brutus.utils.socket import hostname_resolves

# prevent weird output race conditions
lock = Lock()


class PortScanner(ThreadedTaskQueue):
    """Initiate a port scan on `host` from `start_port` to `end_port`.
    Ports will be placed in a queue, then delegated to threads in a concurrent manner

    Args:
        host (str)
        start_port (int): start of range
        end_port (int): end of range; inclusive
        n_threads (int): number of threads, at maximum, to spawn
    """

    def __init__(
        self, host: str, start_port: int, end_port: int, n_threads: int
    ) -> None:
        # the ThreadedTaskQueue will push these onto the queue
        ports = [
            port for port in range(start_port, end_port)  # pylint: disable=R1721
        ]  # TODO use a lazy / async iterator or generator

        super().__init__(
            callback=self.port_scan_routine, arg=host, tasks=ports, n_threads=n_threads
        )

    def port_scan_routine(self, port: int, host: str) -> None:  # pylint: disable=R0201
        """The port scan routine, to be invoked by a daemon thread

        Args:
            port (int)
            host (str)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((host, port)) == 0:
                with lock:
                    Logger.warn(f'{host}:{port} is open')

        except socket.gaierror:
            # Logger.fail(f'hostname \'{host}\' is invalid')
            pass

        except socket.error:
            pass

        finally:
            sock.close()

    @staticmethod
    def validate_host(host: str) -> bool:
        """Perform a validation check to ensure the hostname resolves

        Returns:
            bool
        """
        return hostname_resolves(host)

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
