#!/usr/bin/env bash
# D10: hard stop 3. Image rights vocabulary and the publication rule.
# See _image_rights.py, which also explains why this is keyed per image and not
# per encoding.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_image_rights.py" "$ROOT"
