"""
This module contains base and extended exception classes
"""


class BaseBrutusException(Exception):
    """Brutus base exception class, with more readable error message formatting

    Args:
        message (str): the error message
    """

    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return f"\n\n{self.message}"


class ScriptFailed(BaseBrutusException):
    """An exception for failed subprocess script invocations

    Args:
        returncode (int, optional): the 'failed' script's return code
        message (str, optional): the error message
        stderr (bytes, optional): the 'failed' script's stderr output, if any

    Inherits:
        BaseBrutusException
    """

    def __init__(
        self,
        returncode: int = 1,
        message: str = 'The script returned a non-zero exit code',
        stderr: bytes = None,
    ) -> None:
        self.returncode = returncode
        self.stderr = stderr
        self.message = message

        super().__init__(
            f'{self.message}\nStderr -> {str(self.stderr)}\nCode -> {self.returncode}'
        )
