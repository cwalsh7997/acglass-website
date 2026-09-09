#!/usr/bin/env bash
# D2: no numeric safety statistic publishes. Regression guard.
source "$(dirname "$0")/_lib.sh"
pat=$(paste -sd'|' "$CFG/safety-terms.txt")
out=$(ggi -E "($pat)[^a-z0-9]{0,12}[0-9]")
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    safety-claims (no numeric safety statistic published)"; exit 0; }
printf '%s\n' "$out" | sed 's/^/  /' | head -20
say "FAIL    safety-claims: $n numeric claims"; exit 1
