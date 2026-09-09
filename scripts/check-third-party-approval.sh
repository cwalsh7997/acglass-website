#!/usr/bin/env bash
# D3: no third-party name publishes without an approval row. See
# _third_party_approval.py, including why this is not implemented with awk.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_third_party_approval.py" "$ROOT"
