#!/usr/bin/env bash
# Company-wide project-count and installed-SF totals are unpublished.
# Connor cancelled unverified 350+ / 1M+ / 1,000,000+ SF figures on 2026-09-14.
#
# Fail if public HTML still publishes those company-volume claims.
# Leave alone:
#   - $350+ / $150–$350+ unit prices
#   - $1,000,000 insurance limits (no plus)
#   - 3.6 million square feet (manufacturer campus, not ACG volume)
#   - 350-square-foot project openings
#   - legacy URL slugs (do not delete pages)
source "$(dirname "$0")/_lib.sh"
fail=0

# 350+ that is not a dollar price ($350+ or $150–$350+).
bad350=$(gg -nE '350\+' | grep -Ev '\$[0-9,]*350\+' | grep -Ev 'lessons-from-350-|acg-350-projects-milestone' | head -20)
if [ -n "$bad350" ]; then
  printf '%s\n' "$bad350" | cut -c1-160 | sed 's/^/  unpublished 350+ volume claim: /'
  fail=$((fail + $(printf '%s' "$bad350" | grep -c .)))
fi

bad1m=$(gg -nF '1M+' | head -20)
if [ -n "$bad1m" ]; then
  printf '%s\n' "$bad1m" | cut -c1-160 | sed 's/^/  unpublished 1M+ volume claim: /'
  fail=$((fail + $(printf '%s' "$bad1m" | grep -c .)))
fi

# 1,000,000+ is company SF volume. Plain $1,000,000 insurance has no plus.
badsf=$(gg -nE '1,000,000\+' | head -20)
if [ -n "$badsf" ]; then
  printf '%s\n' "$badsf" | cut -c1-160 | sed 's/^/  unpublished 1,000,000+ volume claim: /'
  fail=$((fail + $(printf '%s' "$badsf" | grep -c .)))
fi

# Phrase forms. Do not use a bare "350-project" prefix: that matches the
# legacy slug acg-350-projects-milestone / lessons-from-350-..., which stay.
badphrase=$(gg -nE '350-project (dataset|glazing)|350 commercial glazing projects|million square feet of glazing|1 million SF' | head -20)
if [ -n "$badphrase" ]; then
  printf '%s\n' "$badphrase" | cut -c1-160 | sed 's/^/  unpublished volume phrase: /'
  fail=$((fail + $(printf '%s' "$badphrase" | grep -c .)))
fi

# Public SVG assets.
svg_hits=$(git -C "$ROOT" grep -nI -E '350\+|1M\+|1,000,000\+' -- 'images/*.svg' 2>/dev/null | head -20)
if [ -n "$svg_hits" ]; then
  printf '%s\n' "$svg_hits" | cut -c1-160 | sed 's/^/  unpublished volume claim in SVG: /'
  fail=$((fail + $(printf '%s' "$svg_hits" | grep -c .)))
fi

# Served search index: company volume only, not $350+ unit prices or legacy slugs.
idx_hits=$(git -C "$ROOT" grep -nI -E '350\+|1M\+|1,000,000\+' -- search-index.json 2>/dev/null \
  | grep -Ev '\$[0-9,]*350\+|acg-350-projects-milestone|lessons-from-350-' | head -20)
if [ -n "$idx_hits" ]; then
  printf '%s\n' "$idx_hits" | cut -c1-160 | sed 's/^/  unpublished volume claim in search-index: /'
  fail=$((fail + $(printf '%s' "$idx_hits" | grep -c .)))
fi

if [ "$fail" -eq 0 ]; then
  say "PASS    volume-claims (no unpublished 350+/1M+/1,000,000+ SF company totals)"
  exit 0
fi
say "FAIL    volume-claims: $fail unpublished volume claim(s)"
exit 1
