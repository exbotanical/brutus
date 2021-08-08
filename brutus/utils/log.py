"""
This module contains logging utilities
"""


class Logger:
    """Simple stdout logger"""

    @staticmethod
    def success(msg: str) -> None:
        """Print a formatted success message

        Args:
            msg (str): message to print
        """
        print('[+]', msg)

    @staticmethod
    def fail(msg: str) -> None:
        """Print a formatted failure message

        Args:
            msg (str): message to print
        """
        print('[-]', msg)

    @staticmethod
    def info(msg: str) -> None:
        """Print a formatted info message

        Args:
            msg (str): message to print
        """
        print('[*]', msg)

    @staticmethod
    def warn(msg: str) -> None:
        """Print a formatted warning message

        Args:
            msg (str): message to print
        """
        print('[!]', msg)
