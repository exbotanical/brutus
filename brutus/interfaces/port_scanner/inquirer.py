"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.port_scanner.PortScanner import PortScanner
from brutus.utils.logger import LOGGER

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
    inquirer.Text(
        name='hostname', message='Enter the hostname (do not include protocol)'
    ),
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
        validate=lambda _, n_threads: isinstance(int(n_threads), int),
    ),
]


def run() -> None:
    """Run the Inquirer interface

    TODO: add logging decorator
    """
    hostname, start_port, end_port, n_threads = destructure(
        inquirer.prompt(questions), 'hostname', 'start_port', 'end_port', 'n_threads'
    )

    scanner = PortScanner(
        hostname=hostname,
        start_port=int(start_port),
        end_port=int(end_port),
        n_threads=int(n_threads),
    )

    if not scanner.validate_hostname(hostname=hostname):
        LOGGER.error(f'hostname {hostname} cannot be resolved')
        return

    try:
        scanner.run()

        LOGGER.info(f'Scan of {hostname}, ports {start_port} - {end_port} complete')

    except KeyboardInterrupt:
        LOGGER.warn('user cancelled the process')

    except Exception:  # pylint: disable=W0703
        LOGGER.error('a program error occurred')


if __name__ == '__main__':
    run()
