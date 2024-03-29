"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.packet_sniffer.PacketSniffer import PacketSniffer
from brutus.utils.logger import LOGGER

questions = [
    inquirer.List(
        name='interface',
        message='Select a wireless interface to sniff on',
        choices=PacketSniffer.get_interfaces(),
    )
]


def routine_callback(match: tuple) -> None:
    """Packet sniffer callback

    Args:
        match (tuple): A packet that matches our filter; consists
        of URL of packet recipient and match content
    """
    LOGGER.info(f'match found in transport to {match[0]}')
    LOGGER.info(match[1])


def run() -> None:
    """Run the Inquirer interface"""
    answers = inquirer.prompt(questions)
    interface = answers['interface']

    try:
        scanner = PacketSniffer(interface=interface, callback=routine_callback)
        scanner.start_sniff()

    except KeyboardInterrupt:
        LOGGER.warn('user cancelled the process')

    except Exception:  # pylint: disable=W0703
        LOGGER.error('a program error occurred')


if __name__ == '__main__':
    run()
