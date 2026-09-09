#!/usr/bin/env bash
# On-page SEO hygiene: title <=60, description <=155, exactly one h1,
# og:title == twitter:title, no HTML comment inside an attribute value.
# Scan logic and its exclusions live in scripts/_seo_hygiene.py.
source "$(dirname "$0")/_lib.sh"
out=$(python3 "$ROOT/scripts/_seo_hygiene.py" "$ROOT" 2>&1)
n=$(printf '%s\n' "$out" | sed -n 's/^COUNT=//p')
printf '%s\n' "$out" | grep -v '^COUNT=' | grep -v '^$'
if [ "${n:-1}" -eq 0 ] 2>/dev/null; then
  say "PASS    seo-hygiene (titles, descriptions, h1, social titles)"; exit 0
fi
say "FAIL    seo-hygiene: ${n:-?} issue(s)"; exit 1
