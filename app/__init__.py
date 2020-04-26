import inquirer
import threading
from utils.mac_changer import main as mac_changer
from utils.network_scanner import main as network_scan
from utils.arp_spoofer import main as arp_spoofer

def exit_status(answers):
   return (answers["primary_thread"] == "exit")

primary_choices = [("Utilities", "utils"), "Payloads", "Leviathan C&C",("Exit","exit")]
util_choices = [("MAC Changer (Cloak)", "cloak"), ("Network Scanner","network_scan"), ("ARP Spoofer", "arp_spoofer")]


questions = [
   inquirer.List("primary_thread", "Select an option", choices=primary_choices),
   inquirer.List("utils", "Select a Utility", choices=util_choices, ignore=exit_status)
]


while True:
   answers = inquirer.prompt(questions)
   if (answers and answers["primary_thread"] == "exit"):
      break
   if (answers and answers["utils"] == "cloak"):
      mac_changer.main()
   if (answers and answers["utils"] == "network_scan"):
      network_scan.main()
   if (answers and answers["utils"] == "arp_spoofer"):
      arp_spoofer.main()

   print(answers)

   # TODO add inquirer event-handling
   



   
