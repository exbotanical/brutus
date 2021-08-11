# The Brutus Exploitation Framework

An educational exploitation framework shipped on a modular and highly extensible multi-tasking and multi-processing architecture.

## Table of Contents

- [Introduction](#intro)
- [Demos](#demo)
- [Installation](#install)
- [Usage](#usage)
- [Features](#features)
- [Documentation](#docs)
  - [MAC Address Management](#macchanger)
  - [ARP Network Scanner](#networkscanner)
  - [ARP Spoofing](#arpspoof)
  - [Multi-tasking Packet Sniffer](#packetsniff)
  - [Multi-tasking Port Scanner](#portscan)
  - [Evented Web Crawler](#webcrawl)
  - [Subdomain Scanner](#subdomain)

## <a name="intro"></a> Brutus: an Introduction

Looking for version 1? See the branches in this repository.

Brutus is an educational exploitation framework written in Python. It automates pre and post-connection network-based exploits, as well as web-based reconnaissance. As a light-weight framework, Brutus aims to minimize reliance on third-party dependencies. Optimized for Kali Linux, Brutus is also compatible with macOS and most Linux distributions, featuring a fully interactive command-line interface and versatile plugin system.

Brutus features a highly-extensible, modular architecture. The included exploits (plugins layer) consists of several decoupled modules that run on a 'tasking layer' comprised of thread pools and thread-safe, async queues (whichever is most appropriate for the given module). The main thread runs atop a multi-processing pool that manages app context and dispatches new processes so tasks can run in the background, in separate shells, etc.

The UI layer is also decoupled and extensible. By default, Brutus ships with a menu-based command-line interface UI but there's no reason you can't add adapters for a GUI, an argument parser, or even an HTTP API or remote procedure call.

Last, Brutus has a utility layer with common faculties for file-system operations, shell (terminal emulator) management, persistence methods, and system metadata.

If you're just interested in some Python hacking, feel free to pull the scripts directly - each module can be invoked standalone.

## <a name="demo"></a> Demos

Web Scanning and Payload Compilation Demo: [watch mp4](https://streamable.com/scybvn)
![demo](https://github.com/MatthewZito/Brutus/blob/dev/assets/brutus_demo1.gif)


## <a name="install"></a> Installation

You will probably want the following dependencies:

- sslstrip
- pipenv

Brutus is optimized for Kali Linux. There's lots of information online about how to run Kali Linux in a VM.

To install:

```bash
pipenv install
```

## <a name="usage"></a> Usage

### <a name="features"></a> Brutus: Features and Included Modules

Brutus includes several modules which can be generalized as belonging to three macro-categories: *network-based*, *web-based*, and *payloads*. The latter category is a library of compilers and accompanying payloads - payloads can be compiled via Brutus' interactive command-line menu; compiled payloads can subsequently be loaded into many of Brutus' applicable network-based modules.

The base layer of Brutus utilizes POSIX threads for concurrent multi-tasking. Some modules - i.e. essentially anything heavily I/O bound - instead utilize Python's async I/O libraries and run on an abstraction atop Python's default event loop.

**Included Utilities/Scripts**

- IP Table Management
- Downgrade HTTPS to HTTP
- Enable Monitor Mode
- Enable Port Forwarding
- Keylogger

### <a name="docs"></a> Documentation

#### <a name="macchanger"></a>  48-bit MAC Address Changer ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/mac_changer/mac_changer.py))

NOTE: This tool is for 48-bit MACs, with a %02x default byte format.

MAC (Media Access Control) is a permanent, physical, and unique address assigned to network interfaces by device manufacturers. This means even your wireless card, for instance, has its own unique MAC address.

The MAC address, analogous to an IP on the internet, is utilized within a network in order to facilitate the proper delivery of resources and data (i.e. packets). An interaction will generally consist of a source MAC and a destination MAC. MAC addresses can identify you, be filtered, or otherwise access-restricted.

Important to note is these unique addresses are not ephemeral; they are persistent and will remain associated with a device were a user to install it in another machine. But the two don't have to be inextricably intertwined...

This module will accept as user-input any given wireless device and any valid MAC address to which the user wishes to reassign said device. The program is simple such that I need not explain it much further: it utilizes the subprocess module to automate the sequence of the necessary shell commands to bring the wireless interface down, reassign the MAC, and reinitialize it.

If you are actively changing your MAC address, it might be prudent to have some sort of validation structure or higher order method to ensure that 1) the wireless device exists, 2) the wireless device accommodates a MAC address, 3) the user-input MAC address is of a valid format, and 4) the wireless device's MAC address has successfully been updated. This tool automates these functions.

By selecting the 'generate' option in lieu of a specific MAC address, the program will generate a valid MAC address per IEEE specifications. I'm excited to have implemented extended functionality for generating not only wholly random (and valid) MAC addresses, but MAC addresses which either begin with a specific vendor prefix (OUI), or are generated with multicast and/or UAA options. These options trigger byte-code logic in the generator method, which are augmented per IEEE specifications. Learn more about MAC addresses [here](https://en.wikipedia.org/wiki/Organizationally_unique_identifier#Bit-reversed_representation).


#### <a name="networkscanner"></a> ARP-Based Network Scanner ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/network_scanner/network_scanner.py))

The network scanner is another very useful tool, and a formidable one when used in conjunction with the aforementioned MAC changer. This scanner utilizes ARP request functionality by accepting as user input a valid ipv4 or ipv6 IP address and accompanying - albeit optional - subnet range.

The program then takes the given IP and/or range, then validates them per IEEE
specifications (again, this validation is run against ipv4 and ipv6 standards). Finally, a broadcast object is instantiated with the given IP and a generated ethernet frame; this object returns to us a list of all connected devices within the given network and accompanying range, mapping their IPs to respective MAC addresses.

The program outputs a table with these associations, which then might be used as input for the MAC changer should circumstances necessitate it.

#### <a name="arpspoof"></a>  Automated ARP Spoofing ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/arp_spoofer/arp_spoof.py))

The ARP Spoof module enables us to redirect the flow of packets in a given network by simultaneously manipulating the ARP tables of a given target client and its network's gateway. This module auto-enables port forwarding during this process, and dynamically constructs and sends ARP packets.

When the module is terminated by the user, the targets' ARP tables are reset, so as not to leave the controller in a precarious situation (plus, it's the nice thing to do).

Because this process places the controller in the middle of the packet-flow between the client and AP, the controller therefore has access to all dataflow (dealing with potential encryption of said data is a task for another script). From here, the myriad options for packet-flow orchestration become readily apparent: surrogation of code by way of automation and regular expressions, forced redirects, remote access, et al. Fortunately, Brutus can automate this, too.

#### <a name="packetsniff"></a>  HTTP Packet Sniffer ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/packet_sniffer/packet_sniff.py))

The packet sniffer is an excellent module to employ after running the ARP Spoofer; it creates a dataflow of all intercepted HTTP packets' data which includes either URLs, or possible user credentials.

The script is extensible and can accommodate a variety of protocols by instantiating the listener object with one of many available filters. Note that Brutus automatically downgrades HTTPS, so unless HSTS is involved, the dataflow should be viable for reconnaissance.


__Disclaimer: This software and all contents therein were created for research use only. I neither condone nor hold, in any capacity, responsibility for the actions of those who might intend to use this software in a manner malicious or otherwise illegal.__
