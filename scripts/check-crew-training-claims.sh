#!/usr/bin/env bash
# D2 obligation 4: crew training claims are FROZEN until questionnaire items 25
# and 26 are answered.
#
# D2, locked, prohibits "OSHA 30 for all workers" and "AAMA InstallationMasters
# trained crews" until Connor answers those two items. It also records that the
# InstallationMasters claim "currently appears only on the Nashville page" and
# says to remove it in phase 0.
#
# It was not removed, and it did not stay on the Nashville page. It is now on 5
# pages including architect-specs/section-08-41-13-aluminum-storefront.html.
# A spec section is worse than a marketing page: spec sections get incorporated
# into contract documents, so an unverified certification claim there stops being
# marketing and becomes a representation.
#
# WHY check-safety-claims.sh MISSED THIS. That check enforces the numeric half of
# D2, the EMR and TRIR figures, by matching a safety term followed by a number.
# A crew training claim carries no number, so it sailed straight through. The
# check was not wrong, it was only ever half of D2.
#
# ALLOWLIST, not a keyword sweep. It matches assertive ACG self-claims and leaves
# generic industry advice alone. A page may tell a reader that field crews should
# hold OSHA 10 and foremen OSHA 30. That is advice, not a claim about ACG.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_crew_claims.py" "$ROOT"
