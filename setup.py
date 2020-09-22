#!/usr/bin/env python3
# used setuppy-generator , 
# trimmed to fit requirements.txt import for saster easier mani't..  https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py 
import os
from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(...
	name='brutus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
	install_requires=required,
    ],
    scripts=[
        'scripts\flush_iptables_fwd.sh',
        'scripts\oui_refresh.sh',
        'scripts\reset_iptables_all.sh',
        'scripts\__init__.py',
    ],
    packages=[
        'app',
        'config',
        'packages',
        'scripts',
        'utils',
        'packages.arp_spoofer',
        'packages.dns_spoofer',
        'packages.file_surrogator',
        'packages.javascript_injector',
        'packages.mac_changer',
        'packages.network_scanner',
        'packages.packet_sniffer',
        'packages.payloads',
        'packages.web_tools',
        'packages.web_tools.link_harvester',
        'packages.web_tools.scanner',
        'packages.web_tools.subdomain_mapper',
    ],
    py_modules=[
        '__init__',
    ],
)
