"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.port_scanner.port_scanner import PortScanner
from brutus.utils.log import Logger

from ..utils.inquirer_utils import destructure


def cast_and_validate_portrange(answers: dict, end_port: int) -> bool:
    """Inquirer helper. Wrapper for port range validation

    Args:
        answers (dict)
        end_port (int)

    Returns:
        bool
    """
    start_port = answers['start_port']

    return PortScanner.validate_portrange(int(start_port), int(end_port))


questions = [
    inquirer.Text(name='host', message='Enter the hostname (do not include protocol)'),
    inquirer.Text(
        name='start_port',
        message='We\'ll need a range of ports to scan. Enter the starting port',
        validate=lambda _, start_port: isinstance(int(start_port), int),
    ),
    inquirer.Text(
        name='end_port',
        message='Enter the end port',
        validate=cast_and_validate_portrange,
    ),
    inquirer.Text(
        name='n_threads',
        message='Enter the number of threads to utilize',
        default='200',
    ),
]


def run() -> None:
    """Run the Inquirer interface

    TODO: add logging decorator
    """
    host, start_port, end_port, n_threads = destructure(
        inquirer.prompt(questions), 'host', 'start_port', 'end_port', 'n_threads'
    )

    scanner = PortScanner(
        host=host,
        start_port=int(start_port),
        end_port=int(end_port),
        n_threads=int(n_threads),
    )

    if not scanner.validate_host(host=host):
        Logger.fail(f'Hostname {host} cannot be resolved')
        return

    scanner.run()

    Logger.success(f'Scan of {host}, ports {start_port} - {end_port} complete')
