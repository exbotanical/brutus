#!/usr/bin/env bash
#desc           :reset IP tables
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source shutil.bash
#environment    :5.0.17(1)-release
#===============================================================================
BIN_NAME=iptables

main () {
  $BIN_NAME -F
  $BIN_NAME -X
  $BIN_NAME -t nat -F
  $BIN_NAME -t nat -X
  $BIN_NAME -t mangle -F
  $BIN_NAME -t mangle -X
  $BIN_NAME -P INPUT ACCEPT
  $BIN_NAME -P FORWARD ACCEPT
  $BIN_NAME -P OUTPUT ACCEPT
  echo "[+] IP Tables have been reset to default configurations"
}

main
