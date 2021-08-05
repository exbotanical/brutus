#!/usr/bin/env bash
#desc           :Bash utilities
#author         :Matthew Zito (goldmund)
#created        :8/2021
#version        :1.0.0
#usage          :source shutil.bash
#environment    :5.0.17(1)-release
#===============================================================================

# exit codes
E_FILENOTFOUND=2
E_XCD=86
E_NOTROOT=87

# constants
ROOT_UID=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
DEFAULT='\033[0m'

red () {
  printf "${RED}$@${DEFAULT}"
}

green () {
  printf "${GREEN}$@${DEFAULT}"
}

yellow () {
  printf "${YELLOW}$@${DEFAULT}"
}

# current time
now () {
  printf '%(%I:%M %p)T\n'
}

# print the error message and exit with the given return code
panic () {
  local exit_status="$1"

  shift # pop exit status; we don't want to print it

  red "[-] ERROR ($(now)): $*\n" >&2
  exit $exit_status
}

# print a success message
success () {
  local msg="$1"

  green "[+] $msg\n"
}

# panic if current directory not target
chk_dir () {
  local target_dir="$1"

  if [[ $(pwd) != $target_dir ]]; then
    panic $E_XCD "Unable to 'cd' into $target_dir"
  fi
}

# change directory and panic if failed
chdir_and_chk () {
  local target_dir="$1"

  cd "$target_dir "
  chk_dir "$target_dir"
}

# panic if the user is not root
chk_root () {
  if [[ ! $UID -eq $ROOT_UID ]]; then
    panic $E_NOTROOT "Must execute as root"
  fi
}

# panic if the target file does not exist
chk_file () {
  local target_file="$1"

  if [[ ! -e $target_file ]];then
    panic $E_FILENOTFOUND "Hosts file not found"
  fi
}

# invoke a callback if the return code is truthy
chk_ret () {
  local callback="$1"

  shift

  local args="$@"

  (( !$? )) && $callback $args
}

# prompt the user for a y/n response
yes? () {
  local prompt="$1"

  read -p "[!] $prompt (y/n): " answer
  case "$answer" in
  y )
    echo 1
    ;;
  n)
    echo 0
    ;;
  *)
    yes?
    ;;
  esac
}

# invoke a function upon each member in an array
# for_each forea_fn ${arr[*]}
for_each () {
  local fn="$1"

  shift

  local -a arr=($@)

  for item in "${arr[@]}"; do
    echo $($fn $item)
  done
}

# map an array 
# map map_fn ${arr[*]}
map () {
  local -a res=()

  local fn="$1"

  shift

  local -a arr=($@)

  for (( i=0; i < ${#arr[@]}; i++ )); do
    res[$i]=$($fn ${arr[i]})
  done

  echo "${res[@]}"
}

# filter an array 
# filter filter_fn ${arr[*]}
filter () {
  local -a res=()

  local fn="$1"

  shift

  local -a arr=("$@")

  for (( i=0; i < ${#arr[@]}; i++ )); do
    $fn ${arr[i]} && res[$i]=${arr[i]}
  done

  echo "${res[@]}"
}

# map an array via a pipe
# echo $(echo "${arr[*]}" | map_stream map_fn)
map_stream () {
  local fn="$1"
  local arg

  while read -r arg; do
    $fn $arg
  done
}

# filter an array via a pipe
# echo $(echo "${arr[*]}" | filter_stream filter_fn)
filter_stream () {
  local fn="$1"
  local arg

  while read -r arg; do
    $fn $arg && echo $arg
  done
}

# stop here if being sourced
return 2>/dev/null
