#!/usr/bin/env bash
# JSON-LD must parse, collection entries must carry a url, and every internal url
# named in structured data must resolve. See _schema_integrity.py for why.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_schema_integrity.py" "$ROOT"
