#!/usr/bin/env bash
# D10: hard stop 3. Every published image must have a recorded rights status.
#
# Keyed per IMAGE, not per encoding. The same photo shipped as jpg + webp + avif
# is one rights decision, not three. The prior CSV had 1,428 encoding rows, which
# made the gate read as 1,007 unanswerable questions when it is really 380 images
# across 59 directories, and most directories are one answer for the whole folder.
#
# Column 5 is rights_status. Columns: image_stem, encodings, project_group,
# source_category, rights_status, evidence_ref, note, recorded_date.
source "$(dirname "$0")/_lib.sh"
CSV="$ROOT/.github/agent-state/state/image-rights.csv"
[ -f "$CSV" ] || { say "CONFIG  image-rights: csv missing"; exit 3; }
rows=$(($(wc -l < "$CSV") - 1))
[ "$rows" -le 0 ] && { say "CONFIG  image-rights: 0 rows recorded, cannot validate"; exit 3; }
bad=$(awk -F, 'NR>1 && ($5=="unverified" || $5=="" || $5=="unknown")' "$CSV" | wc -l | tr -d ' ')
dirs=$(awk -F, 'NR>1 && ($5=="unverified"||$5==""||$5=="unknown"){print $3}' "$CSV" | sort -u | wc -l | tr -d ' ')
[ "$bad" -eq 0 ] && { say "PASS    image-rights ($rows images, all verified)"; exit 0; }
printf '  %s of %s images unverified, across %s directories\n' "$bad" "$rows" "$dirs"
printf '  each directory is normally one answer for the whole folder\n'
say "FAIL    image-rights: $bad of $rows unverified"; exit 1
