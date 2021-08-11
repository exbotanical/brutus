"""Exposes an API for multi-processing / parallel task management
"""
from concurrent.futures import Future, ProcessPoolExecutor
from typing import Any

from brutus.utils.logger import LOGGER


class ProcessPool(ProcessPoolExecutor):
    """Implements a process / context manager pool

    Inherits:
        ProcessPoolExecutor
    """

    def __init__(self, max_workers: int = 4):
        super().__init__(max_workers=max_workers)

        self.running_workers = 0

    def done_routine(self, _: Future) -> None:
        """Default callback invoked when future resolves

        Args:
            _ (Future): [description]
        """
        LOGGER.info('Brutus.ProcessPool: task running')
        self.running_workers -= 1

    def submit(self, *args: Any, **kwargs: Any) -> Future:
        """Submit a new task to be invoked in a new process

        Returns:
            Future
        """
        future = super().submit(*args, **kwargs)

        self.running_workers += 1

        future.add_done_callback(self.done_routine)

        return future

    def get_pool_usage(self) -> int:
        """Retrieve the number of currently running pool processes

        Returns:
            int
        """
        return self.running_workers
