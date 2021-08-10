"""
This module exposes a headless API for subdomain scanning
"""
from typing import Generator

import requests

from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.tasking.ThreadedTaskQueue import ThreadedTaskQueue
from brutus.utils.fs import FileChunk, split_file  # pylint: disable=W0611
from brutus.utils.log import Logger
from brutus.utils.socket import hostname_resolves


class SubdomainScanner(BaseBrutusModule, ThreadedTaskQueue):
    """Implements a scanner that tests each word in a wordlist against a given domain.

    Inherits:
        BaseBrutusModule, ThreadedTaskQueue
    """

    def __init__(
        self,
        domain: str,
        wordlist_path: str,
        protocol: str = 'https',
        timeout: int = 5,
        n_threads: int = 50,
    ) -> None:
        self.timeout = timeout
        self.f_path = wordlist_path
        self.protocol = protocol

        # read about MRO in Python to see more ways to do this
        # otherwise, we go with the simplest because this app is supposed
        # to be educational
        BaseBrutusModule.__init__(
            self, requires_mitm_state=False, same_network_as_target=False
        )

        ThreadedTaskQueue.__init__(
            self,
            callback=self.subdomain_scan_routine,
            arg=domain,
            # read the entire wordlist into memory,
            # split it into chunks; these will be our tasks
            tasks=self.chunk_wordlist(),
            n_threads=n_threads,
        )

    def chunk_wordlist(self) -> Generator:
        """Break the wordlist into several chunked descriptors

        Returns:
            Generator: A list of file descriptors containing cursors to
            a specific chunk of memory
        """
        readers = split_file(self.f_path, 10)
        return readers

    def subdomain_scan_routine(self, reader: 'FileChunk', hostname: str) -> None:
        """Subdomain scanning routine. This is the unit of work passed on to threads.
        Each separate routine will receive its own reader (fd) to open and process.
        A reader will be a chunk of lines from the wordlist.

        Args:
            reader (FileChunk): A file descriptor object
            hostname (str): The target hostname, will be injected down
            as the routine arg
        """
        with reader.open() as fd:
            for line in fd:
                subdomain = line.strip()

                try:
                    exists: requests.models.Response = requests.get(
                        f'{self.protocol}://{subdomain}.{hostname}',
                        timeout=self.timeout,
                    )
                    if exists:
                        # TODO write to db
                        Logger.warn(f'subdomain found: {subdomain}.{hostname}')
                # TODO we want some sort of fail-fast behavior
                # either use joinable threads or an event here to break *all* threads
                # if we know the request will fail every time
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.InvalidURL:
                    pass
                except requests.exceptions.Timeout:
                    pass

    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        """Perform a validation check to ensure the hostname resolves

        Returns:
            bool
        """
        return hostname_resolves(hostname)
