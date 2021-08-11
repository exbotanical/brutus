"""Main thread UI options config
"""
import inquirer  # type: ignore

from brutus.models.BaseBrutusModule import BrutusModuleRequirements


def confirm(message: str) -> bool:
    """Prompt the user for confirmation

    Args:
        message (str)

    Returns:
        bool
    """
    answers = inquirer.prompt([inquirer.Confirm(name='confirmed', message=message)])

    return answers['confirmed']


modules = {
    'arp_spoofer': BrutusModuleRequirements(
        multiprocessing=True,
        requires_mitm_state=False,
        strip_ssl=True,
        needs_port_fwd=True,
        module_path='brutus.interfaces.arp_spoofer.inquirer',
    ),
    'lan_scanner': BrutusModuleRequirements(
        multiprocessing=True,
        requires_mitm_state=False,
        same_network_as_target=True,
        module_path='brutus.interfaces.lan_scanner.inquirer',
    ),
    'mac_address': BrutusModuleRequirements(
        module_path='brutus.interfaces.mac_address.inquirer'
    ),
    'packet_sniffer': BrutusModuleRequirements(
        multiprocessing=True,
        requires_mitm_state=True,
        strip_ssl=True,
        module_path='brutus.interfaces.packet_sniffer.inquirer',
    ),
    'port_scanner': BrutusModuleRequirements(
        multiprocessing=True, module_path='brutus.interfaces.port_scanner.inquirer'
    ),
    'subdomain_scanner': BrutusModuleRequirements(
        multiprocessing=True, module_path='brutus.interfaces.subdomain_scanner.inquirer'
    ),
    'web_crawler': BrutusModuleRequirements(
        multiprocessing=True, module_path='brutus.interfaces.web_crawler.inquirer'
    ),
}

top_level_choices = [
    ('Core Modules', 'tools'),
    ('Utilities', 'utils'),
    ('Payload Compilers', 'payloads'),
    ('Exit', 'exit'),
]

tool_choices = [
    ('ARP Spoofer', 'arp_spoofer'),
    ('LAN Scanner', 'lan_scanner'),
    ('Packet Sniffer', 'packet_sniffer'),
    ('Port Scanner', 'port_scanner'),
    ('Subdomain Scanner', 'subdomain_scanner'),
    ('Web Crawler', 'web_crawler'),
    ('Back', 'back'),
]

util_choices = [
    ('MAC Address Manager', 'mac_address'),
    ('Enable Monitor Mode', 'monitor_mode'),
    ('Enable Port Forwarding', 'port_fwd'),
    ('Downgrade HTTPs', 'downgrade_https'),
    ('Back', 'back'),
]

payload_choices = [('Remote-Report Keylogger', 'keylogger'), ('Back', 'back')]

questions = [
    inquirer.List(
        name='selected_option',
        message='Select an option',
        choices=top_level_choices,
        carousel=True,
    ),
    inquirer.List(
        name='selected_tool',
        message='Select a Tool',
        choices=tool_choices,
        ignore=lambda a: a['selected_option'] != 'tools',
        carousel=True,
    ),
    inquirer.List(
        name='selected_util',
        message='Select a Utility',
        choices=util_choices,
        ignore=lambda a: a['selected_option'] != 'utils',
        carousel=True,
    ),
    inquirer.List(
        name='selected_payload',
        message='Select a Payload to Compile',
        choices=payload_choices,
        ignore=lambda a: a['selected_option'] != 'payloads',
        carousel=True,
    ),
]
