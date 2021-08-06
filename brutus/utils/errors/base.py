class BaseException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'\n\n{self.message}'
