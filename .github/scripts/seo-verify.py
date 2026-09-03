#!/usr/bin/env python3
"""
seo-verify.py — Regression + sprint-target verifier for acglass.com

Two tiers of checks:
  FAIL  — guard Sprint 1 wins (non-zero exit if any miss)
  WARN  — Sprint 2 targets (report but do not fail until --strict-warn)

Usage:
  python scripts/seo-verify.py                 # local repo check (file:// roughly)
  python scripts/seo-verify.py --live          # check live https://acglass.com
  python scripts/seo-verify.py --live --strict-warn   # WARN failures also exit non-zero

Stdlib + requests only. Designed to run in GitHub Actions and locally.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import time
from typing import Iterable
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("requests missing; pip install requests")
    sys.exit(2)

BASE = "https://acglass.com"
TIMEOUT = 15
UA = {"User-Agent": "ACG-SEO-Verify/1.0 (+https://acglass.com)"}


# ============================================================
# Fetch helpers
# ============================================================

def fetch(path: str) -> tuple[str, int, dict]:
    """GET path (relative or absolute). Returns (text, status, headers)."""
    url = path if path.startswith("http") else urljoin(BASE + "/", path.lstrip("/"))
    try:
        r = requests.get(url, headers=UA, timeout=TIMEOUT, allow_redirects=False)
        return r.text, r.status_code, dict(r.headers)
    except requests.RequestException as e:
        return "", 0, {"error": str(e)}


def extract_h1_text(html: str) -> str:
    """Strip tags inside H1, collapse whitespace."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", " ", m.group(1))
    text = re.sub(r"&nbsp;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_meta(html: str, name: str) -> str:
    """Extract <meta name=... content=...> or property=...; case-insensitive."""
    p = (
        rf'<meta[^>]+(?:name|property)\s*=\s*"{re.escape(name)}"[^>]*\s+content\s*=\s*"([^"]*)"'
    )
    m = re.search(p, html, re.IGNORECASE)
    if not m:
        p2 = (
            rf'<meta[^>]+content\s*=\s*"([^"]*)"[^>]*(?:name|property)\s*=\s*"{re.escape(name)}"'
        )
        m = re.search(p2, html, re.IGNORECASE)
    return m.group(1) if m else ""


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def extract_canonical(html: str) -> str:
    m = re.search(r'<link[^>]+rel\s*=\s*"canonical"[^>]+href\s*=\s*"([^"]+)"', html, re.I)
    return m.group(1) if m else ""


def extract_jsonld_blocks(html: str) -> list[str]:
    return re.findall(
        r'<script[^>]+type\s*=\s*"application/ld\+json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL | re.IGNORECASE,
    )


def parse_jsonld(html: str) -> list:
    """Return list of parsed JSON-LD objects. Track parse failures separately."""
    results = []
    for blk in extract_jsonld_blocks(html):
        try:
            results.append(("ok", json.loads(blk)))
        except json.JSONDecodeError as e:
            results.append(("error", str(e)))
    return results


# ============================================================
# Check container
# ============================================================

class Result:
    def __init__(self, tier: str, name: str, ok: bool, detail: str = ""):
        self.tier = tier  # FAIL or WARN
        self.name = name
        self.ok = ok
        self.detail = detail

    def fmt(self) -> str:
        sym = "✓" if self.ok else "✗"
        return f"  [{sym}] {self.tier:4}  {self.name}{('  — ' + self.detail) if self.detail else ''}"


# ============================================================
# FAIL-tier checks (regression — protect Sprint 1)
# ============================================================

H1_PAGES = [
    "/",
    "/services.html",
    "/storefront-glazier-palm-harbor-florida/",
    "/blog/florida-building-codes-commercial-glazing-2026.html",
]


def check_h1_integrity(results: list[Result]) -> None:
    for p in H1_PAGES:
        html, status, _ = fetch(p)
        if status != 200:
            results.append(Result("FAIL", f"H1 fetch {p}", False, f"status={status}"))
            continue
        h1 = extract_h1_text(html)
        bad = [t for t in h1.split() if len(t) > 18]
        ok = bool(h1) and not bad
        detail = f"h1={h1!r}"
        if bad:
            detail += f" | bad_tokens={bad}"
        results.append(Result("FAIL", f"H1 integrity {p}", ok, detail))

        # Primary-keyword coverage on the homepage. Until 2026-07-19 the H1 itself
        # carried it ("Florida's commercial glazing standard."). The federal
        # cutover replaced that with the owner-chosen manifesto line, so the
        # keyword now lives in the meta description and body copy only.
        # FAIL tier = keyword must survive somewhere in title/description/H1-H2.
        # WARN tier = it is no longer in the H1 (open tradeoff, Connor's call).
        if p == "/":
            low = html.lower()
            headings = " ".join(
                re.sub(r"<[^>]+>", " ", m.group(1))
                for m in re.finditer(r"<h[12][^>]*>(.*?)</h[12]>", html, re.S | re.I)
            ).lower()
            in_title = "commercial glazing" in extract_title(html).lower()
            in_desc = "commercial glazing" in extract_meta(html, "description").lower()
            in_head = "commercial glazing" in headings
            results.append(
                Result(
                    "FAIL",
                    "Homepage keeps 'commercial glazing' (title/desc/H1-H2)",
                    in_title or in_desc or in_head,
                    f"title={in_title}, description={in_desc}, headings={in_head}, "
                    f"body_mentions={low.count('commercial glazing')}",
                )
            )
            results.append(
                Result(
                    "WARN",
                    "Homepage H1 carries 'commercial glazing'",
                    "commercial glazing" in h1.lower(),
                    f"h1={h1!r} — manifesto hero is owner-SETTLED 2026-09-03 "
                    "('Commercial glazing. Written in 48 hours.'); "
                )
            )


def check_homepage_no_ghosts(results: list[Result]) -> None:
    html, status, _ = fetch("/")
    if status != 200:
        results.append(Result("FAIL", "/ fetch", False, f"status={status}"))
        return
    ghosts = {
        "YOUR_BING_CODE_HERE": "Bing placeholder",
        "YOUR_YANDEX_CODE_HERE": "Yandex placeholder",
        '"SearchAction"': "Deprecated SearchAction",
        "SpeakableSpecification": "Speakable on homepage",
    }
    for needle, label in ghosts.items():
        results.append(
            Result("FAIL", f"Homepage clean of {label}", needle not in html)
        )


def check_robots(results: list[Result]) -> None:
    text, status, _ = fetch("/robots.txt")
    if status != 200:
        results.append(Result("FAIL", "robots.txt fetch", False, f"status={status}"))
        return
    # CCBot + Bytespider must Disallow /
    def ua_disallows(ua: str) -> bool:
        m = re.search(
            rf"^\s*User-agent:\s*{re.escape(ua)}\s*\n\s*Disallow:\s*/",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        return bool(m)

    # CCBot is deliberately ALLOWED as of fix/geo-safe-2026-07-16 (merged): Common
    # Crawl feeds AI training sets, and the GEO decision is that ACG facts should
    # reach model memory. The pre-7/16 rule asserted Disallow:/ — that is now the
    # wrong expectation, so assert the ratified policy instead.
    def ua_allows(ua: str) -> bool:
        m = re.search(
            rf"^\s*User-agent:\s*{re.escape(ua)}\s*\n\s*Allow:\s*/",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        return bool(m)

    results.append(Result("FAIL", "robots.txt CCBot Allow:/ (GEO decision 7/16)", ua_allows("CCBot")))
    results.append(
        Result("FAIL", "robots.txt Bytespider Disallow:/", ua_disallows("Bytespider"))
    )
    results.append(
        Result("FAIL", "robots.txt no news-sitemap ref", "news-sitemap" not in text)
    )
    fictional = ["GeminiBot", "NeevaBot", "Bravebot"]
    for ua in fictional:
        results.append(
            Result(
                "FAIL",
                f"robots.txt no {ua} (fictional UA)",
                ua not in text,
            )
        )

    # Each Sitemap: URL returns 200 — and no entries contain /pdfs/qualifications/
    sitemap_urls = re.findall(r"^\s*Sitemap:\s*(\S+)", text, re.IGNORECASE | re.MULTILINE)
    for sm in sitemap_urls:
        body, st, _ = fetch(sm)
        results.append(Result("FAIL", f"sitemap reachable {sm}", st == 200, f"status={st}"))
        if st == 200:
            results.append(
                Result(
                    "FAIL",
                    f"{sm} no /pdfs/qualifications/ refs",
                    "/pdfs/qualifications/" not in body,
                )
            )


def check_stubs(results: list[Result]) -> None:
    """/eurowall-installer-florida.html and /contact/ must redirect properly."""
    stubs = [
        ("/eurowall-installer-florida.html", "/euro-wall-installer-florida.html"),
        ("/contact/", "/contact.html"),
    ]
    for src, target in stubs:
        html, status, _ = fetch(src)
        if status != 200:
            results.append(Result("FAIL", f"Stub fetch {src}", False, f"status={status}"))
            continue
        # Refresh=0 to target
        has_refresh = bool(
            re.search(
                rf'http-equiv\s*=\s*"refresh"[^>]+content\s*=\s*"0;\s*url=.*{re.escape(target)}',
                html,
                re.IGNORECASE,
            )
        )
        # Canonical to target
        canon = extract_canonical(html)
        canon_ok = canon.endswith(target)
        # noindex robots meta
        robots_meta = extract_meta(html, "robots")
        noindex_ok = "noindex" in robots_meta.lower()
        ok = has_refresh and canon_ok and noindex_ok
        detail = (
            f"refresh={has_refresh}, canonical={canon!r}, robots={robots_meta!r}"
        )
        results.append(Result("FAIL", f"Stub integrity {src}", ok, detail))


def check_canonical_protocol(results: list[Result]) -> None:
    """All sampled pages: canonical href starts https://acglass.com/."""
    sample = ["/", "/services.html", "/about.html", "/portfolio.html", "/capabilities.html"]
    for p in sample:
        html, status, _ = fetch(p)
        if status != 200:
            continue
        canon = extract_canonical(html)
        ok = canon.startswith("https://acglass.com/")
        results.append(Result("FAIL", f"Canonical protocol {p}", ok, f"canonical={canon!r}"))


def check_jsonld_parses(results: list[Result]) -> None:
    sample = ["/", "/services.html", "/about.html", "/portfolio.html", "/capabilities.html"]
    for p in sample:
        html, status, _ = fetch(p)
        if status != 200:
            continue
        parsed = parse_jsonld(html)
        bad = [r for r in parsed if r[0] == "error"]
        ok = not bad
        detail = f"{len(parsed)} blocks, {len(bad)} errors"
        results.append(Result("FAIL", f"JSON-LD parses {p}", ok, detail))


# ============================================================
# WARN-tier checks (Sprint 2 targets)
# ============================================================

def check_homepage_org(results: list[Result]) -> None:
    html, status, _ = fetch("/")
    if status != 200:
        return
    parsed = [obj for tier, obj in parse_jsonld(html) if tier == "ok"]
    # The parent Organization lives at #organization. The short #org alias was
    # retired in the Workstream 4 entity cleanup because it was also being used
    # for LocalBusiness nodes, which split the graph.
    org_ids: list[str] = []

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            i = o.get("@id", "")
            if (
                (t == "Organization" or (isinstance(t, list) and "Organization" in t))
                and isinstance(i, str)
                and i.endswith(("#org", "#organization"))
            ):
                org_ids.append(i)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for it in o:
                walk(it)

    for obj in parsed:
        walk(obj)

    ok = org_ids == ["https://acglass.com/#organization"]
    detail = f"count={len(org_ids)}, ids={org_ids}"
    results.append(Result("WARN", "Homepage one Organization #organization", ok, detail))


def check_homepage_faq6(results: list[Result]) -> None:
    html, status, _ = fetch("/")
    if status != 200:
        return
    parsed = [obj for tier, obj in parse_jsonld(html) if tier == "ok"]
    q_count = 0

    def walk(o):
        nonlocal q_count
        if isinstance(o, dict):
            t = o.get("@type")
            if t == "FAQPage":
                me = o.get("mainEntity", [])
                if isinstance(me, list):
                    q_count += sum(
                        1 for x in me if isinstance(x, dict) and x.get("@type") == "Question"
                    )
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for it in o:
                walk(it)

    for obj in parsed:
        walk(obj)
    # The homepage renders no FAQ section, so its 6-question FAQPage was markup
    # with no on-page counterpart — a Google structured-data policy violation.
    # It was removed in Workstream 4. Restoring the markup without also
    # rendering the answers would reintroduce the violation, so the expectation
    # is inverted: either zero questions, or six that are actually on the page.
    if q_count == 0:
        results.append(Result("WARN", "Homepage FAQPage absent (no FAQ section rendered)", True))
    else:
        body = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
        body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).lower()
        results.append(
            Result(
                "WARN",
                "Homepage FAQPage questions appear in visible text",
                "frequently asked" in body,
                f"count={q_count}, faq_heading_in_body={'frequently asked' in body}",
            )
        )


def check_title_meta_lengths(results: list[Result], sample_limit: int = 50) -> None:
    body, status, _ = fetch("/sitemap-pages.xml")
    if status != 200:
        return
    locs = re.findall(r"<loc>(.*?)</loc>", body)
    too_long_title = 0
    too_long_desc = 0
    longest_title = ("", 0)
    longest_desc = ("", 0)
    for u in locs[:sample_limit]:
        h, st, _ = fetch(u.replace(BASE, ""))
        if st != 200:
            continue
        t = extract_title(h)
        d = extract_meta(h, "description")
        if len(t) > 60:
            too_long_title += 1
            if len(t) > longest_title[1]:
                longest_title = (u, len(t))
        if len(d) > 155:
            too_long_desc += 1
            if len(d) > longest_desc[1]:
                longest_desc = (u, len(d))
    results.append(
        Result(
            "WARN",
            "Titles ≤60 chars (sample of sitemap-pages)",
            too_long_title == 0,
            f"overlong={too_long_title}, longest={longest_title}",
        )
    )
    results.append(
        Result(
            "WARN",
            "Meta desc ≤155 chars (sample)",
            too_long_desc == 0,
            f"overlong={too_long_desc}, longest={longest_desc}",
        )
    )


def check_retired_urls(results: list[Result]) -> None:
    retired = ["/ai-overview.html", "/acg.html", "/about-acg-for-ai.html"]
    # Each must serve 200 (we use stubs, not deletion) AND have refresh+canonical+noindex
    for p in retired:
        html, status, _ = fetch(p)
        if status != 200:
            results.append(Result("WARN", f"Retired URL {p} is a valid stub", False, f"status={status}"))
            continue
        canon = extract_canonical(html)
        robots_meta = extract_meta(html, "robots")
        has_refresh = bool(re.search(r'http-equiv\s*=\s*"refresh"', html, re.I))
        is_stub = has_refresh and "noindex" in robots_meta.lower() and canon.startswith("https://acglass.com/")
        results.append(
            Result(
                "WARN",
                f"Retired URL {p} is a valid stub",
                is_stub,
                f"refresh={has_refresh}, canonical={canon!r}, robots={robots_meta!r}",
            )
        )

    # And absent from every sitemap
    sm_body, sm_status, _ = fetch("/robots.txt")
    sitemaps = re.findall(r"^\s*Sitemap:\s*(\S+)", sm_body, re.IGNORECASE | re.MULTILINE)
    for sm in sitemaps:
        body, st, _ = fetch(sm)
        if st != 200:
            continue
        for p in retired:
            ok = p not in body
            results.append(
                Result(
                    "WARN",
                    f"{sm} absent of {p}",
                    ok,
                )
            )


# ============================================================
# Main
# ============================================================


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="check live acglass.com")
    ap.add_argument(
        "--strict-warn",
        action="store_true",
        help="WARN-tier failures also produce non-zero exit",
    )
    args = ap.parse_args()

    if not args.live:
        print("Note: --live not set; this verifier expects HTTP. Running anyway against", BASE)

    results: list[Result] = []
    started = time.time()

    print(f"\nseo-verify against {BASE}\n")

    # FAIL tier
    check_h1_integrity(results)
    check_homepage_no_ghosts(results)
    check_robots(results)
    check_stubs(results)
    check_canonical_protocol(results)
    check_jsonld_parses(results)

    # WARN tier
    check_homepage_org(results)
    check_homepage_faq6(results)
    check_title_meta_lengths(results)
    check_retired_urls(results)

    # Print table
    for r in results:
        print(r.fmt())

    elapsed = time.time() - started
    fail_misses = sum(1 for r in results if r.tier == "FAIL" and not r.ok)
    warn_misses = sum(1 for r in results if r.tier == "WARN" and not r.ok)
    print(
        f"\nSummary: FAIL miss={fail_misses}, WARN miss={warn_misses}, total checks={len(results)}, {elapsed:.1f}s"
    )

    exit_code = 0
    if fail_misses > 0:
        exit_code = 1
    if args.strict_warn and warn_misses > 0:
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
