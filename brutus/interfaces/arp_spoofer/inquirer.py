"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.arp_spoofer.ArpSpoofer import ArpSpoofer
from brutus.utils.logger import LOGGER
from brutus.utils.networking import ipaddr_valid

from ..utils.inquirer_utils import destructure, validate

questions = [
    # TODO validate
    inquirer.Text(
        name='target_ip',
        message='Enter the target IP address',
        validate=validate(ipaddr_valid),
    ),
    inquirer.Text(
        name='gateway_ip',
        message='Enter the gateway/access point IP address',
        validate=validate(ipaddr_valid),
    ),
]


def spoofer_routine(n_packets: int) -> None:
    """Callback passed to spoofer

    Args:
        n_packets (int): running total number of packets sent
    """
    LOGGER.info(f'Successful transaction; {n_packets} packets sent')


def run() -> None:
    """Run the Inquirer interface"""
    answers = inquirer.prompt(questions)
    target_ip, gateway_ip = destructure(answers, 'target_ip', 'gateway_ip')

    try:
        spoofer = ArpSpoofer(target_ip=target_ip, gateway_ip=gateway_ip)
        spoofer.spoof(callback=spoofer_routine)

    except KeyboardInterrupt:
        LOGGER.warn('user cancelled the process')
        spoofer.cleanup()

    except Exception:  # pylint: disable=W0703
        LOGGER.error('a program error occurred')


if __name__ == '__main__':
    run()
