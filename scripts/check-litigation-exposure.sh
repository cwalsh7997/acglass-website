#!/usr/bin/env bash
# Published imagery from a project that is in active litigation.
#
# WHY THIS IS NOT A CONTENT RULE. Panther National was terminated 2026-05-22 and
# ACG is in an active payment dispute over it. Twenty-nine served pages publish
# project imagery from that job and name the project in body text. Marketing
# copy about a litigated project is discoverable, and what ACG says publicly can
# be quoted back by the other side.
#
# This check does NOT remove anything and must never be made to. Removing content
# about a live dispute is itself a gated act, and doing it quietly is worse than
# leaving it. The charter routes Panther and Verdex to counsel. This reports the
# exposure so counsel can decide, and it fails so the number cannot drift upward
# unnoticed while nobody is looking at it.
#
# To clear: counsel rules, the ruling goes in decisions.md, and the CSV rows move
# off litigated-project. Not before.
source "$(dirname "$0")/_lib.sh"
CSV="$ROOT/.github/agent-state/state/image-rights.csv"
[ -f "$CSV" ] || { say "CONFIG  litigation-exposure: image-rights.csv missing"; exit 3; }

groups=$(awk -F, 'NR>1 && $4=="litigated-project"{print $3}' "$CSV" | sort -u)
[ -z "$groups" ] && { say "PASS    litigation-exposure (no litigated-project imagery recorded)"; exit 0; }

total=0
for g in $groups; do
  n=$(git -C "$ROOT" grep -lI "$g" -- '*.html' | grep -vc '^\.github/')
  printf '  %s :: published on %s served page(s)\n' "$g" "$n"
  total=$((total+n))
done
say "FAIL    litigation-exposure: $total page(s) publish imagery from a litigated project"
exit 1
