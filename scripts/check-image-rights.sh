#!/usr/bin/env bash
# D10: hard stop 3. Any image whose rights status is unverified or unknown.
source "$(dirname "$0")/_lib.sh"
CSV="$ROOT/_internal/agent/state/image-rights.csv"
[ -f "$CSV" ] || { say "CONFIG  image-rights: csv missing"; exit 3; }
rows=$(($(wc -l < "$CSV") - 1))
[ "$rows" -le 0 ] && { say "CONFIG  image-rights: 0 rows recorded, cannot validate"; exit 3; }
bad=$(awk -F, 'NR>1 && ($4=="unverified" || $4=="" || $4=="unknown")' "$CSV" | wc -l | tr -d ' ')
[ "$bad" -eq 0 ] && { say "PASS    image-rights ($rows rows, all verified)"; exit 0; }
say "FAIL    image-rights: $bad of $rows unverified"; exit 1
