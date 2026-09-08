#!/usr/bin/env bash
# D1: SAM.gov status identical across copy, JSON-LD, OG, Twitter, llms.txt.
# WARN-ONLY until llms.txt ships in phase 6 (ACG_FEDERAL_WARN_ONLY=1).
source "$(dirname "$0")/_lib.sh"
out=$(ggi -E 'registration in process|not yet registered|pending SAM')
n=$(printf '%s' "$out" | grep -c . )
if [ "$n" -gt 0 ]; then
  printf '%s\n' "$out" | cut -c1-140 | sed 's/^/  /'
  if [ "${ACG_FEDERAL_WARN_ONLY:-0}" = "1" ]; then
    say "CONFIG  federal-status: $n contradiction(s), WARN-ONLY (llms.txt ships phase 6)"; exit 3
  fi
  say "FAIL    federal-status: $n contradiction(s) with D1"; exit 1
fi
say "PASS    federal-status (UEI QTQYMLLL9PS4, CAGE 234B0, no contradictions)"; exit 0
