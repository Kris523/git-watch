#!/bin/bash

cli_help() {
  echo "
${0##*/}
Utility for monitoring time
Usage: ${0##*/} [command]
Commands:
  check
  results {year} {month} {day}
  *         Help
"
  exit 1
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

case "$1" in
  check|c)
    python3 ${DIR}/check.py
    ;;
  results|r)
    python3 ${DIR}/results.py $2 $3 $4
    ;;
  *)
    cli_help
    ;;
esac