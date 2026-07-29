#!/usr/bin/env python3
"""
canonical-verify.py — static guard against canonical/redirect cannibalization.

Reads the repo as it will be deployed (no network) and enforces the consolidation
model declared in .github/scripts/money-pages.json:

  1. redirect-chain          no 301 lands on another 301, or on a page that
                             canonicals somewhere else (the 301->canonical two-hop)
  2. duplicate-primary       exactly one primary URL per market, unique across
                             markets, and every cluster member consolidates into it
  3. sitemap-conflict        no sitemap lists a 301 source or a non-self-canonical
                             URL; every primary and every 'distinct' page is listed
  4. self-canonical-dupe     no cluster member (hub / near-me / legacy money page)
                             is left self-canonical alongside its primary
  5. internal-references     no <a href> or schema "item" points at a 301 source or
                             at a URL that canonicals elsewhere

Usage:  python .github/scripts/canonical-verify.py [--quiet]
Exit 0 = clean, 1 = at least one violation.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

BASE = "https://acglass.com"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, ".github", "scripts", "money-pages.json")

CANONICAL_RE = re.compile(r'<link[^>]+rel\s*=\s*"canonical"[^>]+href\s*=\s*"([^"]+)"', re.I)
ANCHOR_RE = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
SCHEMA_ITEM_RE = re.compile(r'"item"\s*:\s*"([^"]+)"')
LOC_RE = re.compile(r"<loc>(.*?)</loc>", re.S)

# Assets that legitimately appear in a urlset without being an HTML page.
NON_HTML_SUFFIXES = (".txt", ".pdf", ".xml", ".json")


def read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def same_url(a: str, b: str) -> bool:
    return a.rstrip("/") == b.rstrip("/")


def file_for(url_path: str) -> str | None:
    """Map a site path to the file that serves it, or None if nothing serves it."""
    rel = url_path.lstrip("/")
    if url_path.endswith("/") or rel == "":
        rel += "index.html"
    full = os.path.join(ROOT, rel)
    return full if os.path.isfile(full) else None


def canonical_of(url_path: str) -> str | None:
    """Canonical href declared by the page at url_path. None if no page/no tag."""
    path = file_for(url_path)
    if path is None:
        return None
    match = CANONICAL_RE.search(read(path))
    return match.group(1) if match else None


def to_path(href: str) -> tuple[str, bool]:
    """Normalize an href to a site path. Second value is False for off-site hrefs."""
    url = href.split("#")[0].split("?")[0]
    if url.startswith(BASE):
        url = url[len(BASE):] or "/"
    elif re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", url, re.I):
        return "", False
    if not url.startswith("/"):
        url = "/" + url
    return url, True


class Report:
    def __init__(self) -> None:
        self.failures: list[tuple[str, str]] = []
        self.passes: list[str] = []

    def check(self, group: str, ok: bool, detail: str) -> None:
        if ok:
            self.passes.append(f"{group}: {detail}")
        else:
            self.failures.append((group, detail))


def load_redirects() -> dict[str, str]:
    cfg = json.loads(read(os.path.join(ROOT, "vercel.json")))
    return {r["source"]: r["destination"] for r in cfg.get("redirects", [])}


# ----------------------------------------------------------------------------
# 1. redirect chains
# ----------------------------------------------------------------------------

def check_redirect_chains(rep: Report, redirects: dict[str, str]) -> None:
    for source, dest in sorted(redirects.items()):
        if dest in redirects:
            rep.check(
                "redirect-chain", False,
                f"{source} -> {dest} -> {redirects[dest]} (301 lands on another 301)",
            )
            continue
        canonical = canonical_of(dest)
        if canonical and not same_url(canonical, BASE + dest):
            rep.check(
                "redirect-chain", False,
                f"{source} -> {dest} but {dest} canonicals to "
                f"{canonical[len(BASE):]} (301->canonical two-hop)",
            )
    if not any(g == "redirect-chain" for g, _ in rep.failures):
        rep.check("redirect-chain", True, f"{len(redirects)} redirects resolve in one hop")


# ----------------------------------------------------------------------------
# 2 + 4. one primary per market, no self-canonical duplicates in the cluster
# ----------------------------------------------------------------------------

def check_primaries(rep: Report, markets: dict, redirects: dict[str, str]) -> None:
    owner: dict[str, str] = {}
    for key, market in markets.items():
        primary = market["primary"]

        if primary in owner:
            rep.check(
                "duplicate-primary", False,
                f"{primary} is the primary for both '{owner[primary]}' and '{key}'",
            )
        owner[primary] = key

        if file_for(primary) is None:
            rep.check("duplicate-primary", False, f"[{key}] primary {primary} has no page")
            continue

        canonical = canonical_of(primary)
        rep.check(
            "duplicate-primary",
            bool(canonical) and same_url(canonical, BASE + primary),
            f"[{key}] primary {primary} self-canonical (found {canonical})",
        )

        if primary in redirects:
            rep.check(
                "duplicate-primary", False,
                f"[{key}] primary {primary} is itself a 301 source",
            )

        for url in market["canonicalize"]:
            canonical = canonical_of(url)
            if canonical is None:
                rep.check("self-canonical-dupe", False, f"[{key}] {url} has no page or no canonical tag")
                continue
            if same_url(canonical, BASE + url):
                rep.check(
                    "self-canonical-dupe", False,
                    f"[{key}] {url} is still self-canonical — it competes with {primary}",
                )
            elif not same_url(canonical, BASE + primary):
                rep.check(
                    "self-canonical-dupe", False,
                    f"[{key}] {url} canonicals to {canonical[len(BASE):]}, expected {primary}",
                )
            if url in redirects:
                rep.check(
                    "self-canonical-dupe", False,
                    f"[{key}] {url} carries both a 301 and a rel=canonical — pick one",
                )

        for source, dest in market["redirect"].items():
            actual = redirects.get(source)
            rep.check(
                "duplicate-primary",
                actual == dest,
                f"[{key}] 301 {source} -> {dest} (vercel.json has {actual!r})",
            )

        for url in market["distinct"]:
            canonical = canonical_of(url)
            rep.check(
                "self-canonical-dupe",
                bool(canonical) and same_url(canonical, BASE + url),
                f"[{key}] distinct page {url} stays self-canonical (found {canonical})",
            )


# ----------------------------------------------------------------------------
# 3. sitemap membership
# ----------------------------------------------------------------------------

def check_sitemaps(rep: Report, markets: dict, redirects: dict[str, str]) -> None:
    listed: set[str] = set()
    for sitemap in sorted(glob.glob(os.path.join(ROOT, "sitemap*.xml"))):
        name = os.path.basename(sitemap)
        for loc in LOC_RE.findall(read(sitemap)):
            url = loc.strip()
            path = url[len(BASE):] if url.startswith(BASE) else url
            if path.endswith(".xml"):  # sitemap index entries
                continue
            listed.add(path)
            if path in redirects:
                rep.check(
                    "sitemap-conflict", False,
                    f"{name} lists {path} which 301s to {redirects[path]}",
                )
                continue
            if path.endswith(NON_HTML_SUFFIXES):
                continue
            if file_for(path) is None:
                rep.check("sitemap-conflict", False, f"{name} lists {path} but no file serves it")
                continue
            canonical = canonical_of(path)
            if canonical and not same_url(canonical, BASE + path):
                rep.check(
                    "sitemap-conflict", False,
                    f"{name} lists {path} which canonicals to {canonical[len(BASE):]}",
                )

    for key, market in markets.items():
        for url in [market["primary"]] + market["distinct"]:
            rep.check(
                "sitemap-conflict",
                url in listed,
                f"[{key}] {url} is listed in a sitemap",
            )

    if not any(g == "sitemap-conflict" for g, _ in rep.failures):
        rep.check("sitemap-conflict", True, f"{len(listed)} sitemap URLs are canonical and reachable")


# ----------------------------------------------------------------------------
# 5. internal references
# ----------------------------------------------------------------------------

def check_internal_references(rep: Report, markets: dict, redirects: dict[str, str]) -> None:
    stale: dict[str, str] = dict(redirects)
    for market in markets.values():
        for url in market["canonicalize"]:
            stale[url] = market["primary"]

    offenders: dict[str, list[str]] = {}
    for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if os.path.relpath(path, ROOT).startswith((".github", "_internal")):
            continue
        html = read(path)
        hrefs = ANCHOR_RE.findall(html) + SCHEMA_ITEM_RE.findall(html)
        for href in hrefs:
            url, on_site = to_path(href)
            if on_site and url in stale:
                offenders.setdefault(url, []).append(os.path.relpath(path, ROOT))

    for url, pages in sorted(offenders.items()):
        rep.check(
            "internal-references", False,
            f"{len(pages)} page(s) still link to {url} instead of {stale[url]} "
            f"(e.g. {', '.join(sorted(pages)[:3])})",
        )
    if not offenders:
        rep.check("internal-references", True, "no internal link targets a 301 or a canonicalized-away URL")

    # The AI/search surfaces are hand-maintained and drift out of sync with the
    # HTML, so they get the same treatment as an <a href>.
    asset_hits: list[str] = []
    for name in ("llms.txt", "llms-full.txt", "ai.txt", "search-index.json"):
        path = os.path.join(ROOT, name)
        if not os.path.isfile(path):
            continue
        text = read(path)
        for url, dest in stale.items():
            # Boundary guard so /tennessee does not match /tennessee-commercial-glazing/.
            absolute = re.compile(re.escape(BASE + url) + r"(?![\w\-/])")
            if absolute.search(text) or f'"{url}"' in text:
                asset_hits.append(f"{name} references {url} instead of {dest}")

    for hit in sorted(asset_hits):
        rep.check("internal-references", False, hit)
    if not asset_hits:
        rep.check("internal-references", True, "llms.txt / ai.txt / search-index.json are free of stale URLs")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    registry = json.loads(read(REGISTRY))
    markets = registry["markets"]
    redirects = load_redirects()
    rep = Report()

    check_redirect_chains(rep, redirects)
    check_primaries(rep, markets, redirects)
    check_sitemaps(rep, markets, redirects)
    check_internal_references(rep, markets, redirects)

    if not args.quiet:
        for line in rep.passes:
            print(f"  [ok]   {line}")
    for group, detail in rep.failures:
        print(f"  [FAIL] {group}: {detail}")

    print(
        f"\ncanonical-verify: {len(markets)} markets, {len(redirects)} redirects, "
        f"{len(rep.passes)} passed, {len(rep.failures)} failed"
    )
    return 1 if rep.failures else 0


if __name__ == "__main__":
    sys.exit(main())
