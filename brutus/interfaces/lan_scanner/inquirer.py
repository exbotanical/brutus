"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.lan_scanner.LocalNetworkScanner import LocalNetworkScanner
from brutus.utils.logger import LOGGER

questions = [
    inquirer.Text(
        name='ip_range', message='Enter the IP range to scan (e.g. 10.0.0.1/24)'
    )
]


def run() -> None:
    """Run the Inquirer interface

    TODO: add logging decorator
    """
    answers = inquirer.prompt(questions)
    ip_range = answers['ip_range']

    scanner = LocalNetworkScanner(ip_range=ip_range)

    discoveries = scanner.run()

    if len(discoveries):
        LOGGER.info('\nIP\t\t|\tMAC Address\n-----------------------------------------')

        for discovery in discoveries:
            ip = discovery['ip']
            mac = discovery['mac']
            LOGGER.warning(f'{ip}\t\t{mac}')

    LOGGER.info(f'Scan of {ip_range} complete')
