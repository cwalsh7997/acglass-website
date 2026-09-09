#!/usr/bin/env bash
# Shared helpers. Three outcomes: PASS, FAIL, CONFIG. CONFIG is not a PASS.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$ROOT/.github/agent-state/config"
# One tree-wide grep. Excludes .github (not served) and _internal (git-ignored).
gg() { git -C "$ROOT" grep -nI "$@" -- '*.html' ':!.github/*' 2>/dev/null; }
ggi() { gg -i "$@"; }
say()  { printf '%s\n' "$*"; }
hit()  { printf '  %s:%s: %s\n' "$1" "$2" "$3"; }
cfg_incomplete() { grep -q 'STATUS: INCOMPLETE\|STATUS: UNCONFIRMED' "$1" 2>/dev/null; }
