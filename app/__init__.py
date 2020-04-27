import inquirer
import threading
import os
import subprocess
import platform
from inquirer import events
from utils.mac_changer import main as mac_changer
from utils.network_scanner import main as network_scan
from utils.arp_spoofer import main as arp_spoofer
from inquirer import render

def exit_status(answers):
   return (answers["primary_thread"] == "exit")


primary_choices = [("Utilities", "utils"), "Payloads", "Leviathan C&C",("Exit","exit")]
util_choices = [("MAC Changer (Cloak)", "cloak"), ("Network Scanner","network_scan"), ("ARP Spoofer", "arp_spoofer")]


questions = [
   inquirer.List("primary_thread", "Select an option", choices=primary_choices),
   inquirer.List("utils", "Select a Utility", choices=util_choices, ignore=exit_status)
]

try:
   while True:
      answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
      if (answers and answers["primary_thread"] == "exit"):
         break
      if (answers and answers["utils"] == "cloak"):
         mac_changer.main()
      if (answers and answers["utils"] == "network_scan"):
         network_scan.main()
      if (answers and answers["utils"] == "arp_spoofer"):
         # imperfect solution for production, but launch in new terminal as root user
         if (platform == "linux" or platform == "linux2"):
            os.system("gnome-terminal -e 2>/dev/null 'bash -c \"python3 -m utils.arp_spoofer.main; exec bash\"'")
         if (platform == "darwin"):
            pass
         print(answers)
         
except KeyboardInterrupt:
   print("[-] Done.")

   # TODO add inquirer event-handling
   

"""
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError


style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})
"""



   
