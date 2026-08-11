#!/usr/bin/env python3
"""Reject prohibited long-dash characters added by a change.

The repository contains legacy debt, so this gate reads only added diff lines.
It blocks the two Unicode long-dash code points and their HTML entity forms.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass


PROHIBITED = {
    chr(0x2013): "U+2013",
    chr(0x2014): "U+2014",
}
ENTITY_RE = re.compile(r"&(?:n|m)dash;", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    token: str


def scan_patch(patch: str) -> list[Finding]:
    findings: list[Finding] = []
    path = ""
    new_line = 0

    for raw in patch.splitlines():
        if raw.startswith("+++ b/"):
            path = raw[6:]
            continue
        if raw.startswith("@@"):
            match = re.search(r"\+(\d+)", raw)
            new_line = int(match.group(1)) if match else 0
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            added = raw[1:]
            for character, label in PROHIBITED.items():
                if character in added:
                    findings.append(Finding(path, new_line, label))
            if ENTITY_RE.search(added):
                findings.append(Finding(path, new_line, "HTML long-dash entity"))
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            continue
        elif raw and not raw.startswith(("diff ", "index ")):
            new_line += 1

    return findings


def git_patch(base: str | None) -> str:
    if base:
        command = ["git", "diff", "--unified=0", f"{base}...HEAD"]
    else:
        worktree = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        if worktree:
            unstaged = subprocess.run(
                ["git", "diff", "--unified=0"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            staged = subprocess.run(
                ["git", "diff", "--cached", "--unified=0"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            return staged + unstaged
        command = ["git", "diff", "--unified=0", "HEAD^...HEAD"]

    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="base commit for a committed change")
    args = parser.parse_args()

    try:
        patch = git_patch(args.base)
    except subprocess.CalledProcessError as exc:
        print(f"character audit could not read git diff: {exc}", file=sys.stderr)
        return 2

    findings = scan_patch(patch)
    if not findings:
        print("character audit passed: no prohibited long-dash additions")
        return 0

    print(f"character audit failed: {len(findings)} prohibited addition(s)")
    for finding in findings:
        print(f"  {finding.path}:{finding.line}: {finding.token}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
