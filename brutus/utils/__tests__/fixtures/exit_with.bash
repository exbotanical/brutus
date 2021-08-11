#!/usr/bin/env bash

return_with () {
  local ret_code="$1"

  return "$ret_code"
}

return_with "$*"
