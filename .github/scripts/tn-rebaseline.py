#!/usr/bin/env python3
"""
tn-rebaseline.py - recompute the governed Tennessee reference baseline.

The guard pins the normalized reference surface of every Tennessee-referencing
file with a SHA256. A content-wide mechanical edit (for example the em-dash to
ASCII normalization) changes those surfaces without changing any claim, so the
guard fails on drift alone. This script recomputes the baseline.

It deliberately does NOT invent classifications. If the set of Tennessee
reference documents changes, group membership must be edited by hand, because
group membership digests are pinned inside tn-claim-guard.py as a governance
control.

Usage:
  python .github/scripts/tn-rebaseline.py --check   # report drift, change nothing
  python .github/scripts/tn-rebaseline.py --write   # rewrite the inventory
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
INVENTORY = os.path.join(REPO_ROOT, ".github", "tn-reference-inventory.json")


def load_guard():
    path = os.path.join(HERE, "tn-claim-guard.py")
    spec = importlib.util.spec_from_file_location("tn_claim_guard", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("pass --check or --write")

    g = load_guard()

    sources = {}
    for rel, full in g.iter_html_files():
        with open(full, encoding="utf-8") as fh:
            sources[rel] = fh.read()

    css_sources = {}
    for rel, full in g.iter_css_files():
        with open(full, encoding="utf-8") as fh:
            css_sources[rel] = fh.read()

    with open(INVENTORY, encoding="utf-8") as fh:
        inv = json.load(fh)

    groups = inv["reference_groups"]
    classified = sorted({p for paths in groups.values() for p in paths})

    # Recompute the discovery + content-token document set exactly as the guard does.
    discovery = {rel for rel, src in sources.items() if g.is_tn_page(rel, src)}
    external_css = "\n".join(src for _, src in sorted(css_sources.items()))
    content_vars = g.css_content_custom_property_names(external_css)
    content_attrs = g.css_content_attribute_names(external_css)

    import re as _re

    def contextual(src):
        own = {m.group(1) for m in g.CSS_CUSTOM_PROPERTY_START.finditer(src)}
        if own & content_vars:
            return external_css
        for name in content_attrs:
            if _re.search(rf"(?<![-\w]){_re.escape(name)}\s*=", src, _re.IGNORECASE):
                return external_css
        return ""

    tokens = {
        rel for rel, src in sources.items()
        if g.has_tennessee_reference_token(src, contextual(src))
    }
    fragments = set(inv["excluded_non_page_fragments"])
    documents = discovery | (tokens - fragments)

    drift_membership = set(documents) != set(classified)
    if drift_membership:
        added = sorted(set(documents) - set(classified))
        removed = sorted(set(classified) - set(documents))
        print("MEMBERSHIP CHANGED - manual classification required")
        for p in added:
            print("  + unclassified:", p)
        for p in removed:
            print("  - stale:", p)
        print("\nGroup membership digests are pinned in tn-claim-guard.py.")
        print("Refusing to guess. Classify by hand, then rerun.")
        return 2

    old_fp = inv.get("reference_surface_sha256", {})
    new_fp = {}
    changed = []
    for rel in classified:
        digest = g.reference_surface_digest(sources[rel])
        new_fp[rel] = digest
        if old_fp.get(rel) != digest:
            changed.append(rel)

    frag_changed = {}
    for rel in sorted(fragments):
        digest = g.reference_surface_digest(sources[rel])
        if g.EXCLUDED_FRAGMENT_SURFACE_SHA256.get(rel) != digest:
            frag_changed[rel] = digest

    counts = {
        "document_sources": len(documents),
        "path_or_title_discovery": len(discovery),
        "outside_discovery": len(documents - discovery),
        "known_edge_301_sources": len(inv["known_edge_301_sources"]),
        "document_sources_excluding_recorded_edge_sources":
            len(documents) - len(inv["known_edge_301_sources"]),
        "excluded_non_page_fragments": len(fragments),
    }

    print(f"classified documents: {len(classified)}")
    print(f"surface digests changed: {len(changed)}")
    print(f"counts: {counts}")
    print(f"counts match existing: {counts == inv.get('expected_counts')}")
    if frag_changed:
        print("\nEXCLUDED FRAGMENT SURFACE CHANGED - update the constant in")
        print("tn-claim-guard.py EXCLUDED_FRAGMENT_SURFACE_SHA256:")
        for rel, digest in frag_changed.items():
            print(f'    "{rel}":\n        "{digest}",')

    if args.check:
        return 0

    inv["reference_surface_sha256"] = {k: new_fp[k] for k in sorted(new_fp)}
    inv["expected_counts"] = counts
    with open(INVENTORY, "w", encoding="utf-8") as fh:
        json.dump(inv, fh, indent=2, ensure_ascii=True, sort_keys=False)
        fh.write("\n")
    print(f"\nwrote {INVENTORY}")
    if frag_changed:
        print("fragment constant still needs a manual edit (see above)")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
