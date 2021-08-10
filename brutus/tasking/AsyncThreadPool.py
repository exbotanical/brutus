# from concurrent.futures import ThreadPoolExecutor, as_completed
# from typing import Any, Callable, Generator, Union


# class AsyncThreadPool:
#     """Implements a thread pool in which each threads runs
#     its routine  asynchronously
#     """
#     def __init__(
#         self,
#         callback: Callable,
#         tasks: Union[list, Generator],
#         arg: Any,
#         max_threads: int = 10,
#     ) -> None:
#         # thread routine
#         self.callback = callback

#         # argument passed to `callback`, after task
#         # make this an object if more than 1 argument is needed
#         self.args = arg

#         # units of work; this must be an iterable object
#         self.tasks = tasks

#         # the inner thread pool executor
#         self.thread_pool = ThreadPoolExecutor(max_workers=max_threads)

#     def run_task(self, thread_routine: Callable, tasks: list, **kwargs: Any):
#         futures = [
#             self.thread_pool.submit(thread_routine, task, **kwargs) for task in tasks
#         ]

#         # wait(futures, return_when=ALL_COMPLETED)

#         results = []
#         for future in as_completed(futures):
#             try:
#                 yield future.result()
#             except Exception:
#                 pass  # TODO logger

#         return results
