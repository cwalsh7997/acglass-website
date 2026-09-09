#!/usr/bin/env bash
# D2: no numeric safety statistic publishes. Regression guard.
source "$(dirname "$0")/_lib.sh"
pat=$(paste -sd'|' "$CFG/safety-terms.txt")
# Window widened from 12 to 60 chars, and only ACG self-claims are matched.
# "EMR (Experience Modification Rate): 0.81" sat on a live prequal page and this
# check passed, because the parenthetical pushed the number 31 characters past
# the term and the old window stopped at 12.
#
# Generic advice is deliberately excluded. A page may tell a GC that industry
# average EMR is 1.0 and that above 1.0 is a red flag. That is education, not a
# statistic about ACG, and D2 does not touch it.
out=$(ggi -E "(ACG|American Commercial Glass|our|we)[^.<>]{0,60}($pat)[^.<>]{0,60}[0-9]\\.[0-9]|($pat)[^.<>]{0,45}:[^.<>]{0,6}[0-9]\\.[0-9]")
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    safety-claims (no numeric safety statistic published)"; exit 0; }
printf '%s\n' "$out" | sed 's/^/  /' | head -20
say "FAIL    safety-claims: $n numeric claims"; exit 1
