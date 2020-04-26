#!/usr/bin/env python3
# Author: Matthew Zito (goldmund) 
# Contact: https://www.github.com/MatthewZito
# Version: 0.3.0
from utils.mac_changer.mac_changer import *
import inquirer

def main():
    def manual_mode(answers):
        return answers["generation_status"] == "manual"

    def ignore_oui_proc(answers):
        return answers["oui_status"] == "no" or manual_mode(answers)

    def auto_mode(answers):
        return answers["generation_status"] == "auto"

    def oui_mode(answers):
        return answers["oui_status"] == "yes"
        
    def validate_options(answers, current):
        if ("default" in current) and (len(current) > 1):
            return False
        return True
    try:
        questions = [
            inquirer.Text("interface", message="Enter the name of a wireless interface for cloaking ", validate=get_current_mac),
            inquirer.List("generation_status", "Automatic generation, or manual?", choices=['auto', 'manual']),
            inquirer.Text("provided_mac", message="Enter new MAC address", validate=validate_new_mac_format, ignore=auto_mode),
            inquirer.List("oui_status", "Enforce a specific OUI?", choices=["yes", "no"], ignore=manual_mode),
            inquirer.Text("provided_oui", message="Enter OUI (e.g. 00:60:2f for Cisco)", ignore=ignore_oui_proc),
            inquirer.Checkbox(
                "options", 
                message="Select additional parameters you wish to apply ", 
                choices=[("UAA", "uaa"), ("Multicast", "multi"), ("Default (LAA/Unicast)", "default")],
                default=["default"],
                validate=validate_options, 
                ignore=oui_mode
                ),
            inquirer.Confirm("confirmation", message="Update MAC address?")
        ]

        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

        interface = answers["interface"]
        generation_status = answers["generation_status"]
        provided_mac = answers["provided_mac"]
        oui_status = answers["oui_status"]
        provided_oui = answers["provided_oui"]
        options = answers["options"]

        if ("uaa" in options):
            provided_uaa = True
        provided_uaa = False

        if ("multi" in options):
            provided_multi = True
        provided_multi = False
        if (generation_status == "auto"):
            new_mac = generate_mac(oui=provided_oui, uaa=provided_uaa, multicast=provided_multi)
            print(new_mac)
        elif (generation_status == "manual"):
            new_mac = provided_mac
        else:
            print("[-] An exception has been raised.")
        if (new_mac != None):
            print(f"[+] Current MAC for device {interface}: {str(get_current_mac(None, interface))}\n")
            # change_mac_address(interface, new_mac)
            # validate_new_mac_persistence(interface, new_mac)
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Program terminated by user.\n")

if __name__ == "__main__":
    main()


# inquirer.Editor('hi',message="", default=None)