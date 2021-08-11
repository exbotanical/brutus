"""Exposes an API for a cancellable POSIX thread
"""
from threading import Event, Thread
from typing import Callable


class CancellableThread(Thread):
    """Implements an evented, cancellable thread

    Inherits:
        Thread
    """

    def __init__(self, callback: Callable, daemon: bool = False) -> None:
        super().__init__()
        self.callback = callback
        self.daemon = daemon
        self.cancel = Event()

    def join_thread(self, timeout: int = None) -> None:
        """Join the underlying thread

        Args:
            timeout (int, optional): Time to live (TTL) for thread until killed.
            Defaults to None.
        """
        self.cancel.set()
        super().join(timeout)

    def is_cancelled(self) -> bool:
        """Has the underlying thread been signaled to cancel?

        Returns:
            bool
        """
        return self.cancel.is_set()

    def run(self) -> None:
        self.callback()
