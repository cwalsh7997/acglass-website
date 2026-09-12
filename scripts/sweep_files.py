#!/usr/bin/env python3
"""The only sanctioned way to get a file list for a sitewide sweep.

Three times this session a never-touch Buy American page was edited. The first
two were targeted edits and the lesson looked like "run check-deny-list.sh before
you edit, not after". The third was a sitewide footer sweep across 1,438 pages,
which no amount of remembering to check first would have prevented, because the
sweep never named the page it was about to modify.

So the exclusion moves out of my habits and into the tooling. Any sweep that asks
this module for its file list cannot touch a deny-listed page, whether or not
whoever wrote the sweep remembered the deny list exists.

    from sweep_files import sweep_files
    for p in sweep_files("*.html"):
        ...

Returns tracked files matching the pattern, minus .github/ and minus every path
on deny-list-buy-american.txt.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DENY = os.path.join(ROOT, ".github/agent-state/state/deny-list-buy-american.txt")


FROZEN = os.path.join(ROOT, ".github/agent-state/state/byte-frozen-paths.txt")


def denied():
    """Paths no sweep may touch: the D8 never-touch list AND the byte-frozen
    West Palm Beach pages.

    The frozen list was added 2026-09-09. A sitewide stat-bar sweep modified
    impact-windows-palm-beach.html, which is byte-frozen because it is one of four
    contested candidates for the organic #1 and nobody knows which one ranks.
    canonical-verify caught it, but only after the edit. Excluding both lists here
    means a sweep cannot reach either, whether or not whoever wrote the sweep
    remembered they exist.
    """
    if not os.path.isfile(DENY):
        raise SystemExit("sweep_files: deny list missing, refusing to sweep blind")
    out = {l.strip() for l in open(DENY) if l.strip() and not l.startswith("#")}
    if os.path.isfile(FROZEN):
        out |= {l.strip() for l in open(FROZEN) if l.strip() and not l.startswith("#")}
    return out


def sweep_files(pattern="*.html"):
    out = subprocess.run(["git", "-C", ROOT, "ls-files", pattern],
                         capture_output=True, text=True).stdout.split()
    d = denied()
    return [p for p in out if not p.startswith(".github/") and p not in d]


if __name__ == "__main__":
    import sys
    fs = sweep_files(sys.argv[1] if len(sys.argv) > 1 else "*.html")
    print(f"{len(fs)} sweepable files ({len(denied())} deny-listed excluded)")
