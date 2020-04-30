#!/usr/bin/env python3
# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.3.0
import os
import subprocess
import argparse
import re
import random
import configparser
import inquirer
from inquirer import errors

def get_current_mac(answers=None, interface=None):
    """
    Calls ifconfig, runs a regex to find the specified device's (interface)
    current MAC address, and returns it as a string. 
    """
    FNULL = open(os.devnull, 'w')
    try:
        ifconfig_res = subprocess.check_output(["ifconfig", interface], stderr=FNULL)
        # decode what is a bytes-like object
        decoded_res = ifconfig_res.decode("utf-8")
        current_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", decoded_res)
        # does the device even have a MAC address?
        if (current_mac_res != None):
            return current_mac_res.group(0)
    except:
        raise errors.ValidationError('', reason=f"[-] Unable to read MAC address of device {interface}.")

def change_mac_address(interface, new_mac):
    """
    Uses ifconfig to reassign a given device's MAC address.
    """
    print(f"[+] Changing MAC address for interface {interface} to {new_mac}.")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def validate_new_mac_persistence(interface, new_mac):
    """
    Validates a given device's current MAC against the new MAC
    specified by the user (new_mac) to ensure new MAC persists
    and is valid.
    """
    current_mac = get_current_mac(None, interface)
    if (current_mac == new_mac):
        print(f"[+] Successfully updated device {interface} MAC address to {new_mac}.")
    else:
        print(f"[-] Failed to update/persist to specified MAC address {new_mac} for device {interface}")

def validate_new_mac_format(answers=None, new_mac=None):
    """
    A basic check to validate the user-input for new MAC address 
    by ensuring it follows the proper colon-delimited format.
    """
    valid_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", new_mac)
    return True if valid_mac_res != None else False

def generate_bytes(num=6):
    return [random.randrange(256) for _ in range(num)]

def generate_mac(oui=False, multicast=False, uaa=None):
    """
    Generates a MAC address either:
    (a) entirely (defaults unicast, LAA),
    (b) with a specified vendor prefix (OUI),
    (c) with multicast and/or UAA IEEE specifications
    """
    delimiter = ":"
    # begin Philipp Klaus' code, which I've augmented 
    # https://gist.github.com/pklaus/9638536#file-randmac-py-L10-L22
    byte_mac = generate_bytes()
    if (oui and type(oui) == str):
        try:
            # convert to bytes
            byte_oui = [int(chunk, 16) for chunk in oui.split(delimiter)]
            byte_mac = byte_oui + generate_bytes(num=6 - len(byte_oui))
        except ValueError as stderr:
            print(f"[-] OUI format is invalid. See: {stderr}")
    else:
        if (multicast):
            byte_mac[0] |= 1 # set bit 0
        else: # unicast
            byte_mac[0] &= ~1 # clear bit 0
        if (uaa):
            byte_mac[0] &= ~(1 << 1) # clear bit 1
        else: # laa
            byte_mac[0] |= 1 << 1 # set bit 1
    # end Philipp Klaus' code
    random_mac = delimiter.join(map(lambda x: "%02x" % x, byte_mac))
    return random_mac
