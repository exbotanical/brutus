"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.subdomain_scanner.SubdomainScanner import SubdomainScanner
from brutus.utils.logger import LOGGER

from ..utils.inquirer_utils import destructure

questions = [
    inquirer.Text(name='domain', message='Enter the domain to scan'),
    inquirer.Path(
        name='wordlist_path',
        message='Enter the wordlist file path (absolute)',
        exists=True,
        path_type=inquirer.Path.FILE,
    ),
    inquirer.Text(
        name='protocol',
        message='Enter the file protocol (e.g. https)',
        default='https',
        validate=lambda _, protocol: isinstance(protocol, str),
    ),
    inquirer.Text(
        name='timeout',
        message='Enter the request timeout (seconds)',
        default='5',
        validate=lambda _, timeout: isinstance(int(timeout), int),
    ),
    inquirer.Text(
        name='n_threads',
        message='Enter the number of threads to utilize',
        default='200',
        validate=lambda _, n_threads: isinstance(int(n_threads), int),
    ),
]


def run() -> None:
    """Run the Inquirer interface"""
    domain, wordlist_path, protocol, timeout, n_threads = destructure(
        inquirer.prompt(questions),
        'domain',
        'wordlist_path',
        'protocol',
        'timeout',
        'n_threads',
    )

    scanner = SubdomainScanner(
        domain=domain,
        wordlist_path=wordlist_path,
        protocol=protocol,
        timeout=int(timeout),
        n_threads=int(n_threads),
    )

    if not scanner.validate_hostname(hostname=domain):
        LOGGER.error(f'hostname {domain} cannot be resolved')
        return

    scanner.run()

    LOGGER.info(f'Scan of {domain} complete')
