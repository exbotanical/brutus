class BaseException(Exception):
    """Brutus base exception class, with more readable error message formatting

    Args:
        message (str): the error message
    """
    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'\n\n{self.message}'
