#!/usr/bin/env bash
# Runs every check and prints a summary table.
# Three outcomes: PASS, FAIL, CONFIG. CONFIG means a required list is incomplete.
# CONFIG IS NOT A PASS. verify.sh exits 0 only when everything is PASS.
cd "$(dirname "$0")/.." || exit 2
CHECKS="design-lint seo-hygiene license-attribution safety-claims placeholders volume-claims bonding geography federal-status deny-list image-rights out-of-state-claims litigation-exposure sitemap-integrity broken-links office-claims form-a11y schema-integrity qualifier-claim crew-training-claims third-party-approval"
NAMES=()
RESULTS=()
pass=0; fail=0; config=0
for c in $CHECKS; do
  out=$(bash "scripts/check-$c.sh" 2>&1); code=$?
  case $code in
    0) r=PASS;   pass=$((pass+1));;
    3) r=CONFIG; config=$((config+1));;
    *) r=FAIL;   fail=$((fail+1));;
  esac
  NAMES+=("$c"); RESULTS+=("$r")
  printf '\n=== %s [%s] ===\n%s\n' "$c" "$r" "$out"
done
printf '\n%s\n' "------------------------------------------------------------"
printf '%-26s %s\n' "CHECK" "RESULT"
printf '%s\n' "------------------------------------------------------------"
for i in "${!NAMES[@]}"; do printf '%-26s %s\n' "${NAMES[$i]}" "${RESULTS[$i]}"; done
printf '%s\n' "------------------------------------------------------------"
printf 'PASS %d   FAIL %d   CONFIG %d   (config is not a pass)\n' "$pass" "$fail" "$config"
[ "$fail" -eq 0 ] && [ "$config" -eq 0 ] && exit 0
[ "$fail" -gt 0 ] && exit 1
exit 3
