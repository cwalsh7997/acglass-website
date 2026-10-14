#!/usr/bin/env python3
"""add-shop-link.py - add "09 Shop glass" to the main menu on every page, linking to the online glass store.

Connor, 2026-10-14: the menu should send people to the new store at acglass.ai. The menu is copied into
every page (ax- chrome and the homepage's own menu), so this inserts one link right after
"08 Your project". Idempotent: pages that already have it are skipped. File list from sweep_files, so
deny-listed and byte-frozen pages are never touched. arch-chrome-migrate.py carries the same link for
pages migrated later.

Usage:
  python3 .github/site-checks/add-shop-link.py            # dry run, prints counts
  python3 .github/site-checks/add-shop-link.py --write    # rewrite files
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sweep_files import ROOT, sweep_files  # noqa: E402

AFTER = '<span>08</span>Your project</a>'
LINK = '<a href="https://acglass.ai/"><span>09</span>Shop glass</a>'


def main(write: bool) -> None:
    counts = {"added": 0, "already": 0, "no-menu": 0}
    for rel in sweep_files("*.html"):
        path = pathlib.Path(ROOT) / rel
        text = path.read_text(encoding="utf-8")
        if LINK in text:
            counts["already"] += 1
            continue
        n = text.count(AFTER)
        if n == 0:
            counts["no-menu"] += 1
            continue
        if n != 1:
            raise SystemExit(f"{rel}: menu appears {n} times; refusing to guess where the link goes")
        counts["added"] += 1
        if write:
            path.write_text(text.replace(AFTER, AFTER + LINK), encoding="utf-8")
    print(("wrote " if write else "dry run: ") + ", ".join(f"{k} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main("--write" in sys.argv)
