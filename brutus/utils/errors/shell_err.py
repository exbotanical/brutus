from .base import BaseException

default_err = 'The script returned a non-zero exit code'

class ScriptFailed(BaseException):
    def __init__(self, returncode: int = 1, message: str = default_err, stderr: str = None) -> None:
        self.returncode = returncode
        self.stderr = stderr
        self.message = message

        super().__init__(f'{self.message}: Stderr -> {self.stderr} Ret -> {self.returncode}')
