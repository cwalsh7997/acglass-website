#!/usr/bin/env bash
# Every internal href must resolve to a file on disk.
#
# All 68 occurrences found here came from drafts/cornerstones/, where the drafts
# cross-link each other at the ROOT paths they will have once published rather
# than the draft paths they live at today. Written for a future that had not
# happened yet, so every link was dead on a page that is actually served.
#
# One target, /florida-hvhz-glazing-contractor.html, did not exist anywhere in the
# repo. It was a link to a page nobody ever wrote. Repointed to the published
# blog/hvhz-certified-glazing-contractor-florida.html.
#
# PUBLISH NOTE: the 7 draft-to-draft links now point at /drafts/cornerstones/*.
# When those cornerstones publish to root, that rewrite has to be undone. It is
# recorded in consolidation-plan.md. Broken today is worse than a documented
# rewrite later.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_broken_links.py" "$ROOT"
