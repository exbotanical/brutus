#!/usr/bin/env python3
import threading
import os
import subprocess
import platform

import inquirer
from inquirer import errors

from packages.mac_changer import main as mac_changer
from packages.network_scanner import main as network_scan
from utils.enable_monitor_mode import enable_monitor_mode

operating_sys = platform.system().lower()
dir_path = os.path.dirname(os.path.dirname(__file__))

def spawn_disparate_shell_linux(pkg):
   """
   Initialize given package as its own process, in a discrete shell.
   Enforces Linux-contingent validation.
   """
   if (operating_sys == "linux" or operating_sys == "linux2"):
      os.system(f"gnome-terminal -e 2>/dev/null 'bash -c \"python3 -m {pkg}; exec bash\"'")
   else:
      print("[-] Your operating system does not support this package.\n")

def spawn_disparate_shell_unix(pkg):
   """
   Initialize given package as its own process, in a discrete shell.
   Enforces UNIX-contingent validation.
   """
   # imperfect solution for production, but launch in new terminal as root user
   if (operating_sys == "linux" or operating_sys == "linux2"):
      os.system(f"gnome-terminal -e 2>/dev/null 'bash -c \"python3 -m {pkg}; exec bash\"'")
   if (operating_sys == "darwin"):
      os.system(f"""osascript -e 'tell app "Terminal"
      do script "cd {dir_path}; python3 -m {pkg}"
      end tell' """)
   else:
      print("[-] Your operating system does not support this package.\n")

def exit_status(answers):
   """
   Simulates sigkill on primary thread loop to exit app (somewhat) quietly.
   """
   return (answers["selected_option"] == "exit")

def ignore_payloads(answers):
   return (answers["selected_option"] != "payloads")

def ignore_web(answers):
   return (answers["selected_option"] != "web")

def ignore_utils(answers):
   return (answers["selected_option"] != "utils")

def ignore_tools(answers):
   return (answers["selected_option"] != "tools")

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
      ("Payload Compilers","payloads"), 
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
      ("Subdomain Mapper", "subdomain"),
      ("Link Harvester", "harvest"),
      ("Back","back")
      ]
   util_choices = [
      ("Enable Monitor Mode","mon"),
      ("Back","back")
      ]
   payload_choices = [
      ("Remote-Report Keylogger", "keylogger"),
      ("Remote File Downloader","injctn"),
      ("Credentials Harvester","lazagne"),
      ("Windows Credentials Harvester","winharvest"),
      ("Back","back")
      ]

   questions = [
      inquirer.List("selected_option", message="Select an option", choices=primary_choices, carousel=True),
      inquirer.List("selected_tool", message="Select a Tool", choices=tool_choices, ignore=ignore_tools, validate=flag_processes, carousel=True),
      inquirer.List("selected_util", message="Select a Utility", choices=util_choices, ignore=ignore_utils, validate=flag_processes, carousel=True),
      inquirer.List("selected_web", message="Select a Tool", choices=web_choices, ignore=ignore_web, validate=flag_processes, carousel=True),
      inquirer.List("selected_payload", message="Select a Payload to Compile", choices=payload_choices, ignore=ignore_payloads, validate=flag_processes, carousel=True)
   ]

   while True:
      answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
      # Primary Menu
      if (answers and answers["selected_option"] == "exit"):
         break
      # Tools Menu
      if (answers and answers["selected_option"] == "tools"):
         if (answers and answers["selected_tool"] == "back"):
            continue
         if (answers and answers["selected_tool"] == "cloak"):
            mac_changer.main()
         if (answers and answers["selected_tool"] == "network_scan"):
            network_scan.main()
         if (answers and answers["selected_tool"] == "arp_spoofer"):
            spawn_disparate_shell_linux("packages.arp_spoofer.main")
         if (answers and answers["selected_tool"] == "dns_spoofer"):
            spawn_disparate_shell_linux("packages.dns_spoofer.main")
         if (answers and answers["selected_tool"] == "packet_sniffer"):
            spawn_disparate_shell_unix("packages.packet_sniffer.main")
         if (answers and answers["selected_tool"] == "javascript_injector"):
            spawn_disparate_shell_linux("packages.javascript_injector.main")
         if (answers and answers["selected_tool"] == "file_injector"):
            spawn_disparate_shell_linux("packages.file_surrogator.main")
      # Web Menu
      if (answers and answers["selected_option"] == "web"):
         if (answers and answers["selected_web"] == "back"):
            continue
         if (answers and answers["selected_web"] == "vulnweb"):
            spawn_disparate_shell_unix("packages.web_tools.scanner.main")
         if (answers and answers["selected_web"] == "subdomain"):
            spawn_disparate_shell_unix("packages.web_tools.subdomain_mapper.main")
         if (answers and answers["selected_web"] == "harvest"):
            spawn_disparate_shell_unix("packages.web_tools.link_harvester.main")
      # Utils Menu
      if (answers and answers["selected_option"] == "utils"): 
         if (answers and answers["selected_util"] == "back"):
            continue
         if (answers and answers["selected_util"] == "mon"):
            enable_monitor_mode()
      # Payloads Menu
      if (answers and answers["selected_option"] == "payloads"):
         if (answers and answers["selected_payload"] == "back"):
            continue
         if (answers and answers["selected_payload"] == "lazagne"):
            spawn_disparate_shell_unix("packages.payloads.compile_harvest_creds")
         if (answers and answers["selected_payload"] == "keylogger"):
            spawn_disparate_shell_unix("packages.payloads.compile_keylogger")
         if (answers and answers["selected_payload"] == "injctn"):
            spawn_disparate_shell_unix("packages.payloads.compile_injection")
         if (answers and answers["selected_payload"] == "winharvest"):
            spawn_disparate_shell_unix("packages.payloads.compile_windows_harvest")
            
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



   
