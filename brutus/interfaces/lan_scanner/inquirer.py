"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.lan_scanner.LocalNetworkScanner import LocalNetworkScanner
from brutus.utils.logger import LOGGER

questions = [
    inquirer.Text(
        name='ip_range',
        message='Enter the IP range to scan (e.g. 10.0.0.1/24)'
        # TODO validate
    )
]


def run() -> None:
    """Run the Inquirer interface"""
    answers = inquirer.prompt(questions)
    ip_range = answers['ip_range']

    scanner = LocalNetworkScanner(ip_range=ip_range)

    try:
        discoveries = scanner.run()

        if len(discoveries):
            LOGGER.info(
                '\nIP\t\t|\tMAC Address\n-----------------------------------------'
            )

            for discovery in discoveries:
                ip = discovery['ip']
                mac = discovery['mac']
                LOGGER.warning(f'{ip}\t\t{mac}')

        LOGGER.info(f'Scan of {ip_range} complete')

    except KeyboardInterrupt:
        LOGGER.warn('user cancelled the process')

    except Exception:  # pylint: disable=W0703
        LOGGER.error('a program error occurred')


if __name__ == '__main__':
    run()
