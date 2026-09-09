#!/usr/bin/env bash
# Every visible form control must have an accessible name. See _form_a11y.py for
# the four ways that can be satisfied, including wrapping labels, which a naive
# for= check misses and then reports 28 phantom failures on send-plans.html.
source "$(dirname "$0")/_lib.sh"
python3 "$ROOT/scripts/_form_a11y.py" "$ROOT"
