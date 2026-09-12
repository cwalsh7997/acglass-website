#!/usr/bin/env bash
# D2: no numeric safety statistic about ACG publishes. Regression guard.
#
# The scan moved to scripts/_safety_claims.py on 2026-09-09. The shell regex it
# replaces ended both branches in [0-9]\.[0-9], so it required a decimal point,
# and "0 OSHA recordable incidents" was live on about.html and facts.html, in
# the body copy and inside the FAQPage schema of both, while this check printed
# "no numeric safety statistic published".
#
# Generic advice is still deliberately excluded, and so are OSHA course and log
# names. A page may tell a GC that industry average EMR is 1.0, and may say ACG
# runs OSHA 30 trained crews and keeps an OSHA 300 log. Neither is a statistic
# about ACG's safety record. That distinction is what the scanner encodes.
source "$(dirname "$0")/_lib.sh"
out=$(python3 "$ROOT/scripts/_safety_claims.py" "$ROOT" 2>&1)
n=$(printf '%s\n' "$out" | sed -n 's/^COUNT=//p')
printf '%s\n' "$out" | grep -v '^COUNT=' | grep -v '^$'
if [ "${n:-1}" -eq 0 ] 2>/dev/null; then
  say "PASS    safety-claims (no numeric safety statistic published)"; exit 0
fi
say "FAIL    safety-claims: ${n:-?} numeric claim(s)"; exit 1
