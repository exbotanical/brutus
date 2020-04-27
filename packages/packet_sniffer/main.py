from packages.packet_sniffer.packet_sniff import Sniffer
import inquirer

def main():
    try:
        questions = [inquirer.Text("interface", message="Enter the name of wireless interface to sniff on")]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        interface = answers["interface"]
        Sniffer(interface)
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Packet Sniffer terminated by user.\n")

if __name__ == "__main__":
    main()

# description="Sniff HTTP packets on a given wireless interface.""
