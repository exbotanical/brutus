"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.modules.mac_address.MacAddressManager import MacAddressManager
from brutus.utils.logger import LOGGER

from ..utils.inquirer_utils import destructure, validate

questions = [
    inquirer.List(
        name='interface',
        message='Select a wireless interface',
        choices=MacAddressManager.get_interfaces(),
    ),
    inquirer.List(
        name='generation_mode',
        message='Provide your own MAC address (manual), or generate one (auto)?',
        choices=['auto', 'manual'],
    ),
    inquirer.Text(
        name='provided_mac',
        message='Enter the new MAC address',
        validate=validate(MacAddressManager.validate_macaddr_format),
        ignore=lambda a: a['generation_mode'] == 'auto',
    ),
    inquirer.List(
        name='use_oui',
        message='Use a specific vendor prefix (OUI)?',
        choices=['no', 'yes'],
        ignore=lambda a: a['generation_mode'] == 'manual',
    ),
    inquirer.Text(
        name='provided_oui',
        message='Enter OUI (e.g. 00:60:2f for Cisco)',
        ignore=lambda a: a['use_oui'] == 'no' or a['generation_mode'] == 'manual',
        validate=validate(MacAddressManager.validate_oui_format),
    ),
    inquirer.List(
        name='transmission',
        message='''Should the MAC address be unicast or multicast
        (hint: you probably want unicast)?''',
        choices=[('Unicast', 'uni'), ('Multicast', 'multi')],
        ignore=lambda a: a['use_oui'] == 'yes',
    ),
    inquirer.List(
        name='group',
        message='Should the MAC address be UAA or LAA?',
        choices=[('LAA', 'laa'), ('UAA', 'uaa')],
        ignore=lambda a: a['use_oui'] == 'yes',
    ),
    inquirer.Confirm(name='confirmation', message='Update MAC address?'),
]


def run() -> None:
    """Run the Inquirer interface"""
    answers = inquirer.prompt(questions)

    if not answers['confirmation'] is None:
        interface, oui, mac, transmission, group = destructure(
            answers,
            'interface',
            'provided_oui',
            'provided_mac',
            'transmission',
            'group',
        )

        if mac is None:
            new_mac = MacAddressManager.generate_macaddr(
                oui=oui, multicast=transmission == 'multi', uaa=group == 'uaa'
            )
        else:
            new_mac = mac

    try:
        MacAddressManager.change_macaddr(interface, new_mac)

        if MacAddressManager.validate_macaddr_persistence(interface, new_mac):
            LOGGER.info(f'updated MAC address for interface {interface} to {new_mac}')
        else:
            LOGGER.error(f'failed to update MAC address for interface {interface} ')

    except KeyboardInterrupt:
        LOGGER.warn('user cancelled the process')

    except Exception:  # pylint: disable=W0703
        LOGGER.error('a program error occurred')


if __name__ == '__main__':
    run()
