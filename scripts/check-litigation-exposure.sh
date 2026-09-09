#!/usr/bin/env bash
# Published material about a project that is in active litigation.
#
# WHY THIS IS NOT A CONTENT RULE. Panther National was terminated 2026-05-22 and
# ACG is in an active payment dispute over $311,125.31. Published marketing about
# a litigated project is discoverable, and what ACG says publicly can be quoted
# back by the other side.
#
# SCOPE CORRECTION 2026-09-08. The first version of this check counted references
# to images/projects/panther-national/ and reported 29 pages. That undercounted
# badly, because the exposure is not only photographs:
#
#   126  served pages mention the project by name
#     3  dedicated pages, all indexable and all in the sitemap
#     1  1.4MB case-study PDF, linked from no page but publicly served at its URL
#        photographs of ACG's CEO on site, published on leadership.html
#
# It now measures name mentions across the served surface, which is the number
# that actually matters to counsel.
#
# This check does NOT remove anything and must never be made to. Removing content
# about a live dispute is itself a gated act, and doing it quietly is worse than
# leaving it. The charter routes Panther and Verdex to counsel. This reports the
# exposure and fails so it cannot drift while nobody is looking.
#
# To clear: counsel rules, the ruling goes in decisions.md, and this check is
# updated to match the ruling. Not before.
source "$(dirname "$0")/_lib.sh"

pages=$(git -C "$ROOT" grep -lIi 'panther' -- '*.html' | grep -vc '^\.github/')
dedicated=$(git -C "$ROOT" ls-files '*panther*.html' | grep -vc '^\.github/')
pdf=$(git -C "$ROOT" ls-files '*[Pp]anther*.pdf' | wc -l | tr -d ' ')

printf '  %s served pages mention Panther National by name\n' "$pages"
printf '  %s dedicated pages, %s publicly served PDF(s)\n' "$dedicated" "$pdf"
printf '  photographs of ACG leadership on the litigated site are published on leadership.html\n'
say "FAIL    litigation-exposure: $pages page(s) publish material about a litigated project"
exit 1
