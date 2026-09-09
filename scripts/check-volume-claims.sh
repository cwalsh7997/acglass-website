#!/usr/bin/env bash
# D6: "350+" projects and "1,000,000+ SF" are APPROVED. One value, one format.
#
# REWRITTEN 2026-09-09, because the old version could not fail on a wrong number.
# It printed the variants for review and only failed if "350+" vanished entirely.
# That is how the site carried "200+ commercial projects in the county since 2021"
# on 11 pages and "500+ projects in South Florida" on another, both unapproved and
# the second one 43% above the figure Connor actually confirmed, straight through a
# green check for the whole refresh.
#
# It now fails on any company-volume claim that is not the approved figure. Project
# SCALE measurements are not company volume and are left alone: "Board-up
# (curtainwall section, 100+ SF)" describes an opening, not a portfolio.
source "$(dirname "$0")/_lib.sh"
fail=0

bad=$(gg -oE '\b[0-9,]+\+ [a-z ]*(commercial )?projects' | grep -v '350+ ' | head -8)
if [ -n "$bad" ]; then
  printf '%s\n' "$bad" | cut -c1-120 | sed 's/^/  unapproved project count: /'
  fail=$((fail + $(printf '%s' "$bad" | grep -c .)))
fi

# company-volume square footage only: a figure attached to delivered work
badsf=$(gg -oE '[0-9,]+\+ ?(SF|sq\.? ?ft|square feet) (of |delivered|installed|across)' \
        | grep -v '1,000,000+' | head -5)
if [ -n "$badsf" ]; then
  printf '%s\n' "$badsf" | cut -c1-120 | sed 's/^/  unapproved volume SF: /'
  fail=$((fail + $(printf '%s' "$badsf" | grep -c .)))
fi

p=$(gg -lF '350+' | wc -l | tr -d ' ')
[ "$p" -eq 0 ] && { say "FAIL    volume-claims: approved '350+' claim has disappeared"; exit 1; }
[ "$fail" -eq 0 ] && { say "PASS    volume-claims (350+ on $p pages, no unapproved variant)"; exit 0; }
say "FAIL    volume-claims: $fail unapproved variant(s)"
exit 1
