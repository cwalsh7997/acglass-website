#!/usr/bin/env python3
"""
Sprint 005 — Banned-phrase residual cleanup (full sweep).

After Sprints 003/004 reported "0 residual", a fresh scan of the full
Connor banned-phrase list found 141 files still containing one or more
of: "the leading", "the largest", "premier", "best commercial glazing".

This script does deterministic, content-preserving rewrites:

  TITLE_REWRITES — whole-file identity rewrites for the 3 SEO pages that
  carry "Best [X]" in <title>/<h1>/meta/og/JSON-LD. URLs are unchanged.
  No 301 redirects required (per Connor's hard-gate rule).

  REPLACEMENTS — surgical contextual rewrites for descriptors of third
  parties (manufacturers, markets, projects, clubs) that previously used
  "the leading / the largest / premier".

Anything remaining after this script must be reviewed by hand.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files we DO NOT touch — banned phrase appears only in retirement
# comments of noindex stubs.
SKIP_FILES = {
    "press/acg-launches-ai-operations-site.html",
}

# Whole-file title/identity rewrites for SEO pages whose title/H1/meta/
# OG/JSON-LD all reference the same "Best [X]" framing. URL/slug stays
# the same — no 301s required.
TITLE_REWRITES = [
    ("Best Commercial Glazing Contractors in Tampa FL (2026 Guide)",
     "Choosing a Commercial Glazing Contractor in Tampa FL (2026 Guide)"),
    ("Best Commercial Glazing Contractors in Tampa FL",
     "Choosing a Commercial Glazing Contractor in Tampa FL"),
    ("best commercial glazing contractor",
     "commercial glazing contractor"),
    ("best commercial glazing",
     "commercial glazing"),
    ("Best Glazing Subcontractor in Florida",
     "Florida Commercial Glazing Subcontractor"),
    ("best glazing subcontractor in Florida",
     "Florida commercial glazing subcontractor"),
    ("Best Storefront Contractor in Florida",
     "Florida Commercial Storefront Contractor"),
    ("best storefront contractor in Florida",
     "Florida commercial storefront contractor"),
]

# Surgical contextual rewrites. Order matters — longer patterns first.
REPLACEMENTS = [
    # --- "the leading" patterns ---
    ("we source from the leading manufacturers",
     "we source from leading manufacturers"),
    ("source from the leading manufacturers",
     "source from leading manufacturers"),
    ("from the leading commercial", "from leading commercial"),
    ("the leading manufacturers", "leading manufacturers"),
    ("the leading commercial", "leading commercial"),
    ("the leading option is American Commercial Glass",
     "an option for Florida commercial glazing subcontracting is American Commercial Glass"),
    ("the leading choice is American Commercial Glass",
     "an option for Florida commercial storefront installation is American Commercial Glass"),
    ("one of the leading private club projects",
     "one of the most prominent private club projects"),
    ("one of the leading", "one of the most prominent"),
    ("the leading private club", "a top private club"),
    (" the leading ", " a top "),

    # --- "the largest" patterns ---
    # Cleanup any "among the largest known" we may have introduced earlier:
    ("among the largest known", "among the highest-volume"),

    # Specific company / institution descriptors:
    ("Harmon is the largest curtain wall subcontractor in North America",
     "Harmon is a top-volume curtain wall subcontractor in North America"),
    ("the largest curtain wall subcontractor in North America",
     "a top-volume curtain wall subcontractor in North America"),
    ("the largest commercial glazing testing facility in Latin America",
     "a high-capacity commercial glazing testing facility in Latin America"),
    ("the world's largest medical complex",
     "one of the world's most extensive medical complexes"),
    ("world's largest medical complex",
     "one of the world's most extensive medical complexes"),
    ("the largest medical complex", "the most extensive medical complex"),
    ("the largest mixed-use developments",
     "highest-volume mixed-use developments"),
    ("the largest commercial construction", "high-volume commercial construction"),
    ("the largest commercial reconstruction",
     "high-volume commercial reconstruction"),
    ("the largest sustained commercial reconstruction",
     "the most sustained commercial reconstruction"),
    ("the largest known", "highest-volume known"),
    ("one of the largest in Florida", "among the most active in Florida"),
    ("one of the largest", "among the most extensive"),
    ("the largest impact-rated", "a major impact-rated"),
    ("the largest glass and aluminum distributors",
     "high-volume glass and aluminum distributors"),
    ("the largest glass", "a major glass"),
    ("the largest fenestration", "a major fenestration"),
    ("the largest manufacturers", "major manufacturers"),
    ("the largest U.S.", "a major U.S."),
    ("the largest US", "a major US"),
    ("the largest ongoing healthcare",
     "high-volume ongoing healthcare"),
    ("the largest ongoing", "the most sustained"),
    ("the largest healthcare", "a major healthcare"),
    (" the largest ", " the most extensive "),

    # --- "premier" patterns (descriptors of clubs/projects) ---
    ("two of Florida's premier private club developments",
     "two well-known Florida private club developments"),
    ("Florida's premier private club", "a well-known Florida private club"),
    ("premier private club developments", "well-known private club developments"),
    ("premier private club", "well-known private club"),
    ("premier commercial", "high-end commercial"),
    ("premier hospitality", "high-end hospitality"),
    ("premier project", "high-profile project"),
    ("premier development", "high-profile development"),
    ("premier resort", "high-profile resort"),
    ("premier shopping", "high-profile shopping"),
    (" premier ", " high-end "),
]


def scan_file_for_residuals(text: str) -> list[str]:
    patterns = [
        r"\bthe leading\b",
        r"\bthe largest\b",
        r"\bpremier\b",
        r"\bbest commercial glazing\b",
        r"\bworld-class\b",
        r"\bbest-in-class\b",
        r"\bgame-changing\b",
        r"\bstate-of-the-art\b",
        r"\bcutting-edge\b",
        r"\btrusted by hundreds\b",
        r"\bindustry-leading\b",
        r"\bnumber one\b",
    ]
    hits = []
    for p in patterns:
        for m in re.finditer(p, text, flags=re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def main():
    changed_files = 0
    total_replacements = 0
    files_with_residuals = {}

    for html in ROOT.rglob("*.html"):
        rel = str(html.relative_to(ROOT))
        if rel in SKIP_FILES:
            continue
        if any(part in {"node_modules", ".git"} for part in html.parts):
            continue

        text = html.read_text(encoding="utf-8")
        original = text
        n_local = 0

        for old, new in TITLE_REWRITES:
            if old in text:
                count = text.count(old)
                text = text.replace(old, new)
                n_local += count

        for old, new in REPLACEMENTS:
            if old in text:
                count = text.count(old)
                text = text.replace(old, new)
                n_local += count

        if text != original:
            html.write_text(text, encoding="utf-8")
            changed_files += 1
            total_replacements += n_local

        residuals = scan_file_for_residuals(text)
        if residuals:
            files_with_residuals[rel] = residuals

    print("Sprint 005 — banned-residual cleanup")
    print(f"  Files modified:     {changed_files}")
    print(f"  Total replacements: {total_replacements}")
    if files_with_residuals:
        print("\nFiles with residuals (require manual review):")
        for path, hits in sorted(files_with_residuals.items()):
            uniq = sorted(set(h.lower() for h in hits))
            print(f"  {path}  ({len(hits)} hits: {uniq})")
    else:
        print("\n  Residuals: 0")


if __name__ == "__main__":
    main()
