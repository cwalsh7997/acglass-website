#!/usr/bin/env python3
"""Regenerate the pinned content-drift baselines in the unit test suites.

Two suites pin sha256 fingerprints of page fragments so that unrelated edits
cannot silently change protected pages:

  tests/test_no_external_google_fonts.py   PROTECTED_HASHES
      fragments of projects/ocean-prime-ft-lauderdale.html
  tests/test_priority_accessibility.py     LANDMARK_ONLY_FINGERPRINTS
      fragments of the four landmark-only pages

No --write / --update flag existed for either dict, so an intentional sitewide
edit (for example adding a nav element to every page) required hand-editing
hex digests. This script recomputes the digests from the working tree using the
exact fragment extraction logic of each suite and rewrites the literal dicts in
place.

Usage:
    python3 .github/scripts/rebaseline-content-drift.py            # show drift
    python3 .github/scripts/rebaseline-content-drift.py --write    # rewrite

Exit codes:
    0  no drift, or --write and the files were rewritten
    1  drift detected and --write was not passed
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
TESTS = SCRIPTS / "tests"
REPO_ROOT = SCRIPTS.parents[1]

FONTS_TEST = TESTS / "test_no_external_google_fonts.py"
A11Y_TEST = TESTS / "test_priority_accessibility.py"


def _load(path: Path):
    """Import a test module without running it, to reuse its own extractors."""
    spec = importlib.util.spec_from_file_location("drift_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _render(mapping: dict, indent: int) -> str:
    """Render a dict of str->str (or str->dict) as a Python literal block."""
    pad = " " * indent
    inner = " " * (indent + 4)
    lines = ["{"]
    for key, value in mapping.items():
        if isinstance(value, dict):
            lines.append(f'{inner}"{key}": {{')
            for sub_key, sub_value in value.items():
                lines.append(f'{inner}    "{sub_key}": "{sub_value}",')
            lines.append(f"{inner}}},")
        else:
            lines.append(f'{inner}"{key}": "{value}",')
    lines.append(pad + "}")
    return "\n".join(lines)


def _replace_literal(source: str, name: str, rendered: str) -> str:
    """Replace `NAME = { ... }` at module level with the rendered literal."""
    pattern = re.compile(
        r"^" + re.escape(name) + r"\s*=\s*\{.*?^\}", re.S | re.M
    )
    if not pattern.search(source):
        raise SystemExit(f"could not locate literal {name}")
    return pattern.sub(f"{name} = {rendered}", source, count=1)


def compute_fonts() -> dict:
    module = _load(FONTS_TEST)
    source = module.PAGE.read_text(encoding="utf-8")
    fragments = module._protected_fragments(source)
    return {key: module._sha256(fragments[key]) for key in sorted(fragments)}


def compute_a11y() -> dict:
    module = _load(A11Y_TEST)
    computed = {}
    for rel in module.LANDMARK_ONLY_PAGES:
        page = module.REPO_ROOT / rel
        computed[rel] = module._fingerprints(page.read_text(encoding="utf-8"))
    return computed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="rewrite the pinned baselines in place",
    )
    args = parser.parse_args()

    fonts_module = _load(FONTS_TEST)
    a11y_module = _load(A11Y_TEST)

    new_fonts = compute_fonts()
    new_a11y = compute_a11y()
    old_fonts = dict(fonts_module.PROTECTED_HASHES)
    old_a11y = {k: dict(v) for k, v in a11y_module.LANDMARK_ONLY_FINGERPRINTS.items()}

    drift = []
    for key, value in new_fonts.items():
        if old_fonts.get(key) != value:
            drift.append(f"test_no_external_google_fonts PROTECTED_HASHES[{key}]")
    for rel, frags in new_a11y.items():
        for key, value in frags.items():
            if old_a11y.get(rel, {}).get(key) != value:
                drift.append(
                    f"test_priority_accessibility "
                    f"LANDMARK_ONLY_FINGERPRINTS[{rel}][{key}]"
                )

    if not drift:
        print("content-drift baselines already match the working tree")
        return 0

    print(f"{len(drift)} pinned fingerprint(s) drifted:")
    for item in drift:
        print("  " + item)

    if not args.write:
        print("\nre-run with --write to update the pinned baselines")
        return 1

    fonts_source = FONTS_TEST.read_text(encoding="utf-8")
    fonts_source = _replace_literal(
        fonts_source, "PROTECTED_HASHES", _render(new_fonts, 0)
    )
    FONTS_TEST.write_text(fonts_source, encoding="utf-8")

    a11y_source = A11Y_TEST.read_text(encoding="utf-8")
    a11y_source = _replace_literal(
        a11y_source, "LANDMARK_ONLY_FINGERPRINTS", _render(new_a11y, 0)
    )
    A11Y_TEST.write_text(a11y_source, encoding="utf-8")

    print("\nwrote:")
    print("  " + str(FONTS_TEST.relative_to(REPO_ROOT)))
    print("  " + str(A11Y_TEST.relative_to(REPO_ROOT)))
    print(json.dumps({"fonts": new_fonts, "landmark_only": new_a11y}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
