#!/usr/bin/env bash
# The sitemap must agree with canonical tags and robots meta.
#
# Three contradictions Google treats as conflicting signals:
#   A  a URL is in the sitemap but its page canonicals somewhere else
#   B  a URL is in the sitemap but its page is noindex
#   C  a page is self-canonical and indexable but absent from the sitemap
#
# A and B are hard failures: they tell Google two different things about the same
# URL. C is also a failure, but the fix is not always "add it" — a page that
# canonicals elsewhere belongs OUT of the sitemap, and 93 pages here are correctly
# excluded for exactly that reason. Only self-canonical indexable pages are
# counted, so the check cannot push a duplicate into the sitemap.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_sitemap_integrity.py" "$ROOT"
