#!/usr/bin/env bash
# Hard stop 8: geography claims outside where ACG self-performs.
# See _geography.py, including why the previous version validated nothing.
source "$(dirname "$0")/_lib.sh"
[ -s "$CFG/geography-counties.txt" ] || { say "CONFIG  geography: county list missing"; exit 3; }
python3 "$ROOT/scripts/_geography.py" "$ROOT"
