"""
This module exposes a ReporterFactory API for the purposes of instantiating
Reporters, where a Reporter is simply an object that sends data to some service.
"""
from enum import Enum
from smtplib import SMTP, SMTPException
from typing import Any, Callable


class ReportMethod(Enum):
    """Denotes a Report Method type"""

    EMAIL = (1,)
    FILE = 2


class ReporterFactory:
    """Factory for creating Reporters"""

    def __init__(self, reporter_type: ReportMethod) -> None:
        if reporter_type == ReportMethod.EMAIL:
            self.routine = email_reporter

    def create_reporter(self) -> Callable:
        """Create a Reporter caller

        Returns:
            Callable: A method, that when called, invokes the Reporter routine
        """

        def run(**kwargs: Any):
            # TODO let's look into overloads and determine if they'd be sensible here
            return self.routine(**kwargs)

        return run


def email_reporter(
    host: str, port: int, email: str, password: str, message: str
) -> None:
    """Factory template for an email Reporter. Sends reports via email

    Args:
        host (str): SMTP service host
        port (int): SMTP service port
        email (str): email address
        password (str): email password (yes, plaintext)
        message (str): data to enclose in email
    """
    try:
        server = SMTP(host=host, port=port)

        server.starttls()

        server.login(email, password)
        server.sendmail(email, email, message)
    except SMTPException:
        pass  # TODO logging

    finally:
        server.quit()
