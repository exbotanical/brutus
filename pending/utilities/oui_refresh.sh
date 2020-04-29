#!/bin/bash

# Author: Matthew Zito (goldmund)
# Contact: https://www.github.com/MatthewZito
# Version: 0.1.0

OUI=$(ip addr list|grep -w 'link'|awk '{print $2}'|grep -P '^(?!00:00:00)'| grep -P '^(?!fe80)' | tr -d ':' | head -c 6)

curl -sS "http://standards-oui.ieee.org/oui.txt" | grep -i "$OUI" | cut -d')' -f2 | tr -d '\t'

# Automates the process and works across all Linux distros
# given no dependencies on specialized packages. Parses
# output of ip cmd, isolates MAC vendor prefix into variable
# which is finally passed to grep via an online DB of vendor prefixes.

# Possible to adapt this script to execute remotely via ssh.

# Following note from SO:
# I've seen other suggestions to identify vendor details using dmidecode for OS 
# fingerprinting, but experienced inconsistent results with that tool when testing. 