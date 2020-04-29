#!/usr/bin/env python3

import inquirer
import threading
import os
import subprocess
import platform
from inquirer import errors
from packages.mac_changer import main as mac_changer
from packages.network_scanner import main as network_scan
from packages.arp_spoofer import main as arp_spoofer
from packages.packet_sniffer import main as packet_sniffer
from packages.web_tools.scanner import main as vulnerability_scanner
from utils.enable_monitor_mode import enable_monitor_mode
try:
   from packages.dns_spoofer import main as dns_spoofer
   from packages.javascript_injector import main as javascript_injector
   from packages.file_surrogator import main as file_surrogator
except ImportError:
   pass

operating_sys = platform.system().lower()
dir_path = os.path.dirname(os.path.dirname(__file__))

def spawn_disparate_shell_linux(pkg):
   """
   Initialize given package as its own process, in a discrete shell.
   Enforces Linux-contingent validation.
   """
   if (operating_sys == "linux" or operating_sys == "linux2"):
      os.system(f"gnome-terminal -e 2>/dev/null 'bash -c \"python3 -m packages.{pkg}.main; exec bash\"'")
   else:
      print("[-] Your operating system does not support this package.\n")

def spawn_disparate_shell_unix(pkg):
   """
   Initialize given package as its own process, in a discrete shell.
   Enforces UNIX-contingent validation.
   """
   # imperfect solution for production, but launch in new terminal as root user
   if (operating_sys == "linux" or operating_sys == "linux2"):
      os.system(f"gnome-terminal -e 2>/dev/null 'bash -c \"python3 -m packages.{pkg}.main; exec bash\"'")
   if (operating_sys == "darwin"):
      os.system(f"""osascript -e 'tell app "Terminal"
      do script "cd {dir_path}; python3 -m packages.{pkg}.main"
      end tell' """)
   else:
      print("[-] Your operating system does not support this package.\n")

def exit_status(answers):
   """
   Simulates sigkill on primary thread loop to exit app (somewhat) quietly.
   """
   return (answers["primary_thread"] == "exit")

def ignore_web(answers):
   return (answers["primary_thread"] != "web")

def ignore_utils(answers):
   return (answers["primary_thread"] != "utils")

def ignore_tools(answers):
   return (answers["primary_thread"] != "tools")

def flag_processes(answers, current):
   """
   Flag certain processes to prompt the user for confirmation before proceeding.
   """
   if ("spoofer" in current or "sniffer" in current or "injector" in current):
      response = inquirer.prompt([inquirer.Confirm('mitm', message="You must be established as MITM to run this module. Proceed?")])
      if (response["mitm"] == True):
         return True
      else:
         return False
   else:
      return True 

def main():
   primary_choices = [
      ("Network Tools", "tools"),
      ("Web Tools", "web"),
      ("Utils", "utils"), 
      "Payloads", 
      "Leviathan C&C",
      ("Exit","exit")]
   tool_choices = [
      ("MAC Changer (Cloak)", "cloak"), 
      ("Network Scanner","network_scan"),
      ("ARP Spoofer", "arp_spoofer"),
      ("DNS Spoofer", "dns_spoofer"),
      ("Packet Sniffer", "packet_sniffer"),
      ("Javascript Injector", "javascript_injector"),
      ("File Surrogator", "file_injector"),
      ("Back","back")
      ]
   web_choices = [
      ("Website Vulnerability Scanner","vulnweb"),
      ("Back","back")
      ]
   util_choices = [
      ("Enable Monitor Mode","mon"),
      ("Back","back")
      ]

   questions = [
      inquirer.List("primary_thread", "Select an option", choices=primary_choices, carousel=True),
      inquirer.List("selected_tool", "Select a Tool", choices=tool_choices, ignore=ignore_tools, validate=flag_processes, carousel=True),
      inquirer.List("selected_util", "Select a Utility", choices=util_choices, ignore=ignore_utils, validate=flag_processes, carousel=True),
      inquirer.List("selected_web", "Select a Tool", choices=web_choices, ignore=ignore_web, validate=flag_processes, carousel=True)
   ]

   while True:
      answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
      # Primary Menu
      if (answers and answers["primary_thread"] == "exit"):
         break
      # Tools Menu
      if (answers and answers["primary_thread"] == "tools"):
         if (answers and answers["selected_tool"] == "back"):
            continue
         if (answers and answers["selected_tool"] == "cloak"):
            mac_changer.main()
         if (answers and answers["selected_tool"] == "network_scan"):
            network_scan.main()
         if (answers and answers["selected_tool"] == "arp_spoofer"):
            spawn_disparate_shell_linux("arp_spoofer")
         if (answers and answers["selected_tool"] == "dns_spoofer"):
            spawn_disparate_shell_linux("dns_spoofer")
         if (answers and answers["selected_tool"] == "packet_sniffer"):
            spawn_disparate_shell_unix("packet_sniffer")
         if (answers and answers["selected_tool"] == "javascript_injector"):
            spawn_disparate_shell_linux("javascript_injector")
         if (answers and answers["selected_tool"] == "file_injector"):
            spawn_disparate_shell_linux("file_surrogator")
      # Web Menu
      if (answers and answers["primary_thread"] == "web"):
         if (answers and answers["selected_web"] == "back"):
            continue
         if (answers and answers["selected_web"] == "vulnweb"):
            vulnerability_scanner.main()
      # Utils Menu
      if (answers and answers["primary_thread"] == "utils"): 
         if (answers and answers["selected_util"] == "back"):
            continue
         if (answers and answers["selected_util"] == "mon"):
            enable_monitor_mode()

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      print("[-] Done.")
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



   
