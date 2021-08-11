"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.arp_spoofer.ArpSpoofer import ArpSpoofer
from brutus.utils.logger import LOGGER

from ..utils.inquirer_utils import destructure

questions = [
    # TODO validate
    inquirer.Text(name='target_ip', message='Enter the target IP address'),
    inquirer.Text(
        name='gateway_ip', message='Enter the gateway/access point IP address'
    ),
]


def spoofer_routine(n_packets: int) -> None:
    """Callback passed to spoofer

    Args:
        n_packets (int): running total number of packets sent
    """
    LOGGER.info(f'Successful transaction; {n_packets} packets sent')


def run() -> None:
    """Run the Inquirer interface

    TODO: add logging decorator
    """
    answers = inquirer.prompt(questions)
    target_ip, gateway_ip = destructure(answers, 'target_ip', 'gateway_ip')

    spoofer = ArpSpoofer(target_ip=target_ip, gateway_ip=gateway_ip)

    try:
        spoofer.spoof(callback=spoofer_routine)
    except KeyboardInterrupt:
        spoofer.cleanup()
