#!/usr/bin/env bash
#desc           :clear any firewall rules that might interfere with port fwd
#                this script is a preliminary utility unto serving a MITM captive portal AP
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source shutil.bash
#environment    :5.0.17(1)-release
#===============================================================================

main () {
  echo 1 > /proc/sys/net/ipv4/ip_forward
  iptables --flush
  iptables --table nat --flush
  iptables --delete-chain
  iptables --table nat --delete-chain
  iptables -P FORWARD_ACCEPT
}

main
