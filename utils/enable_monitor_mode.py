import subprocess
import inquirer
from inquirer import errors

def enable_monitor_mode():
        """
        Configures wireless interface in monitor mode.
        """
        try:
            questions = [inquirer.Text("interface", message="Enter the name of a wireless interface to configure", validate=lambda _, x: x != '')]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            interface = answers["interface"]
            print(f"[+] Enabling monitor mode for device {interface}.")
            subprocess.call(["ifconfig", interface, "down"])
            subprocess.call(["iwconfig", interface, "mode", "monitor"])
            subprocess.call(["ifconfig", interface, "up"])
        except TypeError:
            pass
        except KeyboardInterrupt:
            print("\n[x] Utility terminated by user.\n")
        else:
            raise errors.ValidationError('', reason=f"[-] Unable to read MAC address of device {interface}.")