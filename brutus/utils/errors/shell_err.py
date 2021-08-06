from .base import BaseException

default_err = 'The script returned a non-zero exit code'

class ScriptFailed(BaseException):
    """An exception for failed subprocess script invocations

    Args:
        returncode (int, optional): the 'failed' script's return code
        message (str, optional): the error message
        stderr (str, optional): the 'failed' script's stderr output, if any

    Inherits:
        BaseException
    """
    def __init__(self, returncode: int = 1, message: str = default_err, stderr: str = None) -> None:
        self.returncode = returncode
        self.stderr = stderr
        self.message = message

        super().__init__(f'{self.message}\nStderr -> {self.stderr}\nCode -> {self.returncode}')
