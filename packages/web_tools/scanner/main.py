#!/usr/bin/env python3
import inquirer
from inquirer import errors
from packages.web_tools.scanner.scanner import Scanner

def ignore_credentials(answers):
   return (answers["login_url"] == answers["base_url"])

def main():
    try:
        questions = [
            inquirer.Text("base_url", message="Enter the target URL", validate=lambda _, x: x != ''),
            inquirer.Text("login_url", message="To initialize scanner in a session, enter target login URL (else, accept default)", default="{base_url}"),
            inquirer.Text("username", message="Enter a valid username", ignore=ignore_credentials, validate=lambda _, x: x != ''),
            inquirer.Text("password", message="Enter a valid password", ignore=ignore_credentials, validate=lambda _, x: x != ''),
            ]

        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

        ignore_list = []
        if (answers["username"]):
            vuln_scanner = Scanner(answers["base_url"], ignore_list, answers["login_url"], answers["username"], answers["password"])
        else:
            vuln_scanner = Scanner(answers["base_url"], ignore_list)
        
    except TypeError:
        pass
    except KeyboardInterrupt:
        print("\n[x] Web Scanner terminated by user.\n")
    except:
        raise errors.ValidationError('', reason=f"[-] An error has occurred; most likely malformed input.")

if __name__ == "__main__":
    main()


# fun links
# http://iberianodonataucm.myspecies.info/
# http://testing-ground.scraping.pro/login
# https://scrapethissite.com/
# http://hmrc.hackxor.net