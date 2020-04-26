from utils.arp_spoofer.arp_spoofer import Spoofer
import inquirer


def main():
    try:
        questions = [
            # validate=validate_ip
        inquirer.Text("target_ip", message="Enter the target/client IP address"),
        inquirer.Text("gateway_ip", message="Enter the gateway/access point IP address"),
        ]
        spoofer = Spoofer()
        answers = inquirer.prompt(questions)
        target_ip = answers["target_ip"]
        gateway_ip = answers["gateway_ip"]
        spoofer.run(target_ip, gateway_ip)
    except TypeError:
        pass
    # TODO add inquirer event-handler

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[x] Program terminated by user. Resetting ARP tables...")
        spoofer.restore_defaults(target_ip, gateway_ip)
        spoofer.restore_defaults(gateway_ip, target_ip)

    # TODO need to set up inuquirer event-handling for keyboard interrupt

# description="Conduct an ARP Spoof to establish self as MITM between target client and gateway."