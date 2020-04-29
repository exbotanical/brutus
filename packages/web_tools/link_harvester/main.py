import inquirer
from inquirer import errors
from packages.web_tools.link_harvester.harvester import Harvester

def main():
    try:
        questions = [inquirer.Text("target_url", message="Enter full URL for link harvesting", validate=lambda _, x: x != '')]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        target_url = answers["target_url"] 
        print(f"[+] Initiating Harvester at {target_url}")
        Harvester(target_url)
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Harvesting process terminated by user.\n")
    except:
        raise errors.ValidationError('', reason=f"[-] An error has occurred; most likely malformed input.")

if __name__ == "__main__":
    main()