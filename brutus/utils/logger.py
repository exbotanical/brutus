"""
This module contains a global app logger
"""

import logging
import sys
import typing
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from typing import Any


class BrutusLogger(Logger):
    """Core Brutus logger.
       Typically, we use multiple loggers per module,
       but we've no need for that here

    Inherits:
        Logger

    TODO: allow setting logger level from config
    """

    def __init__(
        self,
        log_file: typing.Union[str, PathLike] = None,  # type: ignore
        log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        name: str = 'brutus',
        level: Any = logging.DEBUG,
    ) -> None:
        self.formatter = logging.Formatter(log_format)
        self.log_file = log_file

        Logger.__init__(self, name=name, level=level)

        self.addHandler(self.stream_stdout())

        if log_file is not None:
            self.addHandler(self.write_to_file())

        # given we use a single, root logger
        # we've no need to propagate errors
        self.propagate = False

    def stream_stdout(self) -> logging.StreamHandler:
        """Set stream to stdout

        Returns:
            logging.StreamHandler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)

        return console_handler

    def write_to_file(self) -> TimedRotatingFileHandler:
        """Set stream to file

        Returns:
            TimedRotatingFileHandler
        """
        file_handler = TimedRotatingFileHandler(
            self.log_file, when='midnight'  # type: ignore
        )

        file_handler.setFormatter(self.formatter)

        return file_handler


LOGGER = BrutusLogger(name='brutus')
