"""The ThreadedTaskQueue implements a concurrent task queue
by way of multi-threaded task execution

It invokes a provided callback via `n_threads` daemon threads.
A daemon thread runs without blocking the main thread from exiting.
When the main thread exits, all daemon threads will exit.

Units of work are iterated over, each passed as an argument to the callback.
These units are first placed into a queue, where they are enqueued / pushed and
retrieved in a thread-safe manner
"""
from queue import Queue
from threading import Thread
from typing import Any, Callable, Generator, Union


class ThreadedTaskQueue:
    """Implements a thread-safe queue and daemon thread-runner
    Each daemon thread enters into an infinite loop, invoking the provided callback
    until the task queue is empty
    """

    def __init__(
        self,
        callback: Callable,
        n_threads: int,
        tasks: Union[list, Generator],
        arg: Any,
    ) -> None:

        # thread routine
        self.callback = callback

        # argument passed to `callback`, after
        # make this an object if more than 1 argument is needed
        self.args = arg

        # units of work; this must be an iterable object
        # place in the task_queue and passed to `callback` concurrently
        self.tasks = tasks

        # maintains task, each of which is enqueued pending a thread
        # implements mutex locking
        self.task_queue = Queue()  # type: ignore

        # number of threads to execute; you'll probably want to tune this
        # until it meets your needs
        self.n_threads = n_threads

    def __thread_routine(self):
        """Private method. The thread routine, while executing it invokes `callback`"""

        while True:
            # retrieve a unit of work
            task = (
                self.task_queue.get()
            )  # we do not need to lock here; this is thread-safe by design
            # invoke callback with work unit
            self.callback(task, self.args)

            self.task_queue.task_done()

    def run(self):
        """Run the ThreadedTaskQueue; all thread routines will commence on daemon threads
        (non-blocking and may run until the main thread exits)
        """
        for _ in range(self.n_threads):
            thread = Thread(target=self.__thread_routine)

            # we want this thread to be non-blocking
            # and able to run until the main thread finishes executing, if necessary
            thread.daemon = True

            thread.start()

        for task in self.tasks:
            self.task_queue.put(task)

        self.task_queue.join()
