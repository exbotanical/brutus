#!/usr/bin/env bash
#desc           :downgrade SSL connections on target
#                this script is a preliminary utility unto serving a MITM captive portal AP
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source downgrade_ssl.bash
#environment    :5.0.17(1)-release
#===============================================================================
BIN_NAME=iptables
# TODO
main () {
  # $BIN_NAME --flush
  # $BIN_NAME --delete-chain
  # $BIN_NAME --table nat --delete-chain

  # $BIN_NAME -t nat -A PREROUTING -p TCP --destination-port 80 -j REDIRECT --to-port 10000
  # $BIN_NAME -I OUTPUT -j NFQUEUE --queue-num 0
  # $BIN_NAME -I INPUT -j NFQUEUE --queue-num 0
  echo TEST
}

main
