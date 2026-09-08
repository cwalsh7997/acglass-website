#!/usr/bin/env bash
# Hard stop 8: geography claims outside where ACG self-performs.
source "$(dirname "$0")/_lib.sh"
if cfg_incomplete "$CFG/geography-counties.txt"; then
  n=$(ggi -lE 'nashville|tennessee|\bTN\b|georgia|alabama' | wc -l | tr -d ' ')
  say "CONFIG  geography: county list INCOMPLETE, cannot validate."
  say "        pages naming an out-of-state geography: $n"
  exit 3
fi
say "PASS    geography"; exit 0
