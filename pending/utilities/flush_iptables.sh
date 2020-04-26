#!/bin/bash
# clear any firewall rules that might interfere with port fwd
# this script is a preliminary utility unto serving a MITM captive portal AP
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD_ACCEPT