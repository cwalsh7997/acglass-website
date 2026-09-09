#!/usr/bin/env bash
# The published licence number is correct and is never misattributed.
#
# REWRITTEN 2026-09-09, because the rule it used to enforce lost its premise.
#
# It previously required D9a's same-block attribution: every rendered occurrence of
# CGC 1531993 had to carry "Jeff Walsh" within three lines, or the number could not
# ship. That rule existed for one stated reason, quoting D9: "an unattributed
# license number on a contractor site reads as the signer's own credential. If the
# number belongs to the qualifying agent, publishing it bare next to Connor's name
# and title misattributes it."
#
# Connor confirmed on 2026-09-09 that he IS the qualifier of record. The number is
# his own credential, so a bare occurrence is accurate and 10,896 attribution
# sentences would be noise. This is not a check being weakened to pass. It is a
# check whose "if" turned out to be false, so its "then" no longer applies. The
# obligation it enforced came with its own confirmation step and that step returned
# the opposite answer. See decisions.md.
#
# What it guards now, which is what is actually at risk:
#   1. no OTHER licence number is published, which would be a wrong credential
#   2. the superseded qualifying agent is never named, since he is not one
#   3. the bracketed placeholder never returns
source "$(dirname "$0")/_lib.sh"
NUM=$(grep '^NUMBER=' "$CFG/license.txt" | cut -d= -f2)
ATTR=$(grep '^ATTRIBUTION=' "$CFG/license.txt" | cut -d= -f2)
fail=0

total=$(gg -F "$NUM" | grep -c . )

# 1. any CGC-style number that is NOT the confirmed one.
#    Excludes placeholder= and value= attributes: become-a-dealer.html carries
#    placeholder="CGC1234567" as a format hint on a form input, which is an example
#    of the shape, not a credential ACG is publishing about itself.
wrong=$(gg -E 'CGC[ #]*[0-9]{6,8}' | grep -v "$NUM" \
        | grep -vE '(placeholder|value)="[^"]*CGC' | head -10)
if [ -n "$wrong" ]; then
  printf '%s\n' "$wrong" | cut -c1-120 | sed 's/^/  wrong number: /'
  fail=$((fail + $(printf '%s' "$wrong" | grep -c .)))
fi

# 2. the superseded name published as qualifying agent
sup=$(gg -iE 'qualifying agent[^.<]{0,30}jeff|jeff[^.<]{0,30}qualifying agent' | head -5)
if [ -n "$sup" ]; then
  printf '%s\n' "$sup" | cut -c1-120 | sed 's/^/  superseded attribution: /'
  fail=$((fail + $(printf '%s' "$sup" | grep -c .)))
fi

# 3. the placeholder
ph=$(gg -F 'insert DBPR license number here' | head -5)
if [ -n "$ph" ]; then
  printf '%s\n' "$ph" | cut -c1-120 | sed 's/^/  placeholder: /'
  fail=$((fail + $(printf '%s' "$ph" | grep -c .)))
fi

[ "$fail" -eq 0 ] && {
  say "PASS    license-attribution ($total occurrences of CGC $NUM, qualifier $ATTR confirmed)"
  exit 0; }
say "FAIL    license-attribution: $fail problem(s)"
exit 1
