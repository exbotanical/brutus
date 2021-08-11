"""Exposes an API for a Coroutine-synchronized Queue
"""
from asyncio import Queue
from asyncio.tasks import create_task, gather
from typing import Callable, Generator, Union


class AsyncQueue:
    """Implements an asynchronous queue that acts in accordance
    to the Producer-Consumer model.

    Maintains a synchronized queue in which producers queue tasks;
    consumers meanwhile execute the enqueued work
    """

    def __init__(self) -> None:
        self.queue = Queue()  # type: ignore

    async def producer_routine(self, tasks: Union[list, Generator]) -> None:
        """The producer routine. Iterates either a list or generator of tasks,
        placing each into the shared queue.

        Assumes the iteration may or may not incur processing time

        Args:
            tasks (Union[list, Generator]): A list of units of work AKA tasks, which
            will be passed to the consumer callback at some later point
        """
        for task in tasks:
            await self.queue.put(task)

    async def consumer_routine(self, callback: Callable) -> None:
        """Implements a worker that invokes the provided callback
        with an enqueued item as its argument

        Args:
            callback (Callable): The actual computation
        """
        while True:
            task = await self.queue.get()
            callback(task)

            self.queue.task_done()

    async def main_routine(
        self, task_groups: Union[list, Generator], callback: Callable, n_workers: int
    ):
        """Creates producers for all lists of task groups. Instantiates
        for each task group in the list a consumer coroutine,
        which then iterates each task group's tasks

        Args:
            task_groups (Union[list, Generator]): A list or generator of lists
                or generators where the latter are the task groups
            callback (Callable): A callback to be invoked at some later point.
            Accepts 1 task unit as its argument
            n_workers (int): Maximum number of consumers to create
        """
        producers = [
            create_task(self.producer_routine(task_group)) for task_group in task_groups
        ]

        consumers = [
            create_task(self.consumer_routine(callback)) for _ in range(n_workers)
        ]

        await gather(*producers)

        # implicitly awaits consumers, as well
        await self.queue.join()

        for consumer in consumers:
            consumer.cancel()
