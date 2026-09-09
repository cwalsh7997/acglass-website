#!/usr/bin/env bash
# No two indexable pages may compete on the same title or description. See
# _dup_meta.py, including why a shared title behind one canonical is not a defect.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_dup_meta.py" "$ROOT"
