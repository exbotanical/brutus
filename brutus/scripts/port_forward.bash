#!/usr/bin/env bash
#desc           :clear any firewall rules that might interfere with port fwd
#                this script is a preliminary utility unto serving a MITM captive portal AP
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source port_forward.bash
#environment    :5.0.17(1)-release
#===============================================================================
BIN_NAME=iptables
# TODO

main () {
  # echo 1 > /proc/sys/net/ipv4/ip_forward
  # $BIN_NAME --flush
  # $BIN_NAME --table nat --flush
  # $BIN_NAME --delete-chain
  # $BIN_NAME --table nat --delete-chain
  # $BIN_NAME -P FORWARD_ACCEPT

  echo TEST
}

main
