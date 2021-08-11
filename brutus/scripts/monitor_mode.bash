#!/usr/bin/env bash
#desc           :enable monitor mode on network device $1
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source monitor_mode.bash
#environment    :5.0.17(1)-release
#===============================================================================
# TODO

main () {
  # ifconfig $1 down
  # iwconfig $1 mode monitor
  # ifconfig $1 up

  echo $1
  echo HI
}

main
