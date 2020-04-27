import subprocess
import inquirer
from packages.dns_spoofer.dns_spoof import Spoofer

def main():
    try:
        questions = [
            # validate=validate_ip
        inquirer.Text("target_url", message="Enter the the target url"),
        inquirer.Text("redirect_ip", message="Enter the IP to which target will resolve")
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        target_url = answers["target_url"]
        redirect_ip = answers["redirect_ip"]
        Spoofer(target_url,redirect_ip)
    except TypeError:
        pass
    except KeyboardInterrupt:
        try:
            print("\n[x] DNS Spoofer terminated by user. Resetting ARP tables...\n")
            subprocess.call(["iptables --flush"], shell=True) # IMPT - clean up
        except:
            print("[-] Unable to reset ARP tables. You'll need to do this manually, it seems...")
    
if __name__ == "__main__":
    main()

# description="Conduct a DNS Spoof to redirect a given target url."
 
        