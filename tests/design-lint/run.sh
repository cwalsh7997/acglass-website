#!/usr/bin/env bash
# Validates the design lint against a known-broken fixture AND a known-clean tree.
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT" || exit 2
mkdir -p src/components
cp tests/design-lint/broken-fixture.css src/components/_fixture.css
n=$(bash scripts/check-design-lint.sh 2>&1 | grep -c '::')
rm -f src/components/_fixture.css
bash scripts/check-design-lint.sh >/dev/null 2>&1; clean=$?
echo "broken fixture -> $n violations (expect >=8)"
echo "clean tree     -> exit $clean (expect 0)"
[ "$n" -ge 8 ] && [ "$clean" -eq 0 ] && { echo "design-lint VALIDATED"; exit 0; }
echo "design-lint NOT VALIDATED"; exit 1
