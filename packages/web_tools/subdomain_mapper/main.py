import inquirer
from inquirer import errors
from packages.web_tools.subdomain_mapper.subdomain_mapper import Scanner

def ignore_wordlist(answers):
    return answers["user_provided_wordlist"] != "yes"

def main():
    try:
        questions = [
            inquirer.Text("target_url", message="Enter the target login URL", validate=lambda _, x: x != ''),
            inquirer.List("user_provided_wordlist", message="Select an option", choices=[("Use Brutus' wordlist", "no"), ("Use a path-specified wordlist", "yes")]),
            inquirer.Path("wordlist", message="Enter the absolute path to desired wordlist", ignore=ignore_wordlist, validate=lambda _, x: x != '', path_type=inquirer.Path.FILE, exists=True),
            inquirer.Text("interval", message="Enter request interval in seconds", default="1", validate=lambda _, x: x != '')
            ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        wordlist = answers["wordlist"] if answers["wordlist"] else "/Users/narcissus/Applications/Brutus/config/subdomains.txt"
        print(f"[+] Building subdomain map for {answers['target_url']}.")
        Scanner(answers["target_url"], wordlist, answers["interval"])
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Subdomain mapping process terminated by user.\n")
    except:
        raise errors.ValidationError('', reason=f"[-] An error has occurred; most likely malformed input.")

if __name__ == "__main__":
    main()