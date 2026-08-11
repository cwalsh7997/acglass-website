#!/usr/bin/env python3
"""
crawl-check.py — Offline crawl/asset/sitemap regression checker for acglass.com

Complements seo-verify.py, which checks the *deployed* site over HTTP. This one
runs against the repo with no network at all, so it can gate a PR before merge.

Two tiers, same convention as seo-verify.py:
  FAIL  — invariants that must never regress (non-zero exit)
  WARN  — pre-existing debt, pinned to a measured baseline (exit 1 only with
          --strict-warn, or if the debt grows past its baseline)

Usage:
  python .github/scripts/crawl-check.py
  python .github/scripts/crawl-check.py --strict-warn

Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter
from urllib.parse import unquote, urlsplit

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "https://acglass.com"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

# Hero LCP asset guarded by the FAIL tier.
HERO_JPG = "images/hero/tower-360.jpg"
HERO_WEBP = "images/hero/tower-360.webp"

# City hubs named as target markets in the indexation audit. Each one must be
# represented in a child sitemap either directly (self-canonical) or through the
# URL it canonicalises to — otherwise the market has no sitemap representation.
TARGET_MARKET_HUBS = [
    "west-palm-beach",
    "miami",
    "tampa",
    "orlando",
    "naples",
    "fort-lauderdale",
    "boca-raton",
    "jacksonville",
]

# Paths whose parent directory must serve an index (the /author/ 404 class).
MASTER_SITEMAP = "sitemap.xml"
SITEMAP_INDEX = "sitemap-index.xml"

# Refs produced by JS string concatenation in inline <script>-adjacent markup.
# They are not real URLs and can never resolve on disk.
JS_ARTIFACT = re.compile(r"\$\{|\+\s*[A-Za-z_$]|['\"]\s*\+")

# Pre-existing debt measured on the merge base. These are NOT introduced by the
# crawl-defect work; they belong to the internal-linking workstream. Pinned so
# the numbers cannot grow without CI noticing.
BASELINE_MISSING_ASSET_REFS = 2
BASELINE_MISSING_LINK_TARGETS = 9
BASELINE_MISSING_LINK_REFS = 70
TITLE_MAX = 60
DESC_MIN = 80
DESC_MAX = 155

# Copy on these pages intersects approval-gated claims. Keep the exception
# path-specific so another overlength description still fails immediately.
HELD_LONG_DESCRIPTIONS = {
    "buildingconnected-basisboard-glazing.html",
    "government-glazing-contractor-florida.html",
    "government-public-sector-glazing.html",
    "index.html",
}


class Result:
    def __init__(self, tier: str, name: str, ok: bool, detail: str = ""):
        self.tier = tier
        self.name = name
        self.ok = ok
        self.detail = detail

    def fmt(self) -> str:
        sym = "✓" if self.ok else "✗"
        return f"  [{sym}] {self.tier:4}  {self.name}{('  — ' + self.detail) if self.detail else ''}"


# ============================================================
# Repo helpers
# ============================================================

SKIP_DIRS = {".git", ".github", "_internal", "node_modules"}


def html_files() -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return sorted(out)


def read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def exists(rel: str) -> bool:
    return os.path.exists(os.path.join(ROOT, rel))


def resolve(ref: str, from_file: str) -> str | None:
    """Map an href/src to a repo-relative path, or None if it is not local."""
    ref = ref.strip()
    if not ref or JS_ARTIFACT.search(ref):
        return None
    low = ref.lower()
    if low.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:", "#")):
        return None
    path = unquote(urlsplit(ref).path)
    if not path:
        return None
    if path.startswith("/"):
        rel = path.lstrip("/")
    else:
        rel = os.path.normpath(os.path.join(os.path.dirname(from_file), path))
    if rel.startswith(".."):
        return rel  # escapes the repo — always a miss, report it as-is
    return rel


def target_exists(rel: str) -> bool:
    """A directory-style path resolves through its index.html."""
    if rel.endswith("/") or rel == "":
        return exists(os.path.join(rel, "index.html"))
    if exists(rel):
        return True
    if os.path.isdir(os.path.join(ROOT, rel)):
        return exists(os.path.join(rel, "index.html"))
    return False


REF_ATTR = re.compile(r'\b(?:src|href|poster)\s*=\s*"([^"]*)"', re.I)
SRCSET_ATTR = re.compile(r'\bsrcset\s*=\s*"([^"]*)"', re.I)
ASSET_EXT = re.compile(r"\.(?:jpe?g|png|webp|avif|gif|svg|ico|css|js|mp4|webm|woff2?|txt|xml|pdf|json)$", re.I)


def refs_in(html: str) -> list[str]:
    out = [m.group(1) for m in REF_ATTR.finditer(html)]
    for m in SRCSET_ATTR.finditer(html):
        for cand in m.group(1).split(","):
            cand = cand.strip().split()
            if cand:
                out.append(cand[0])
    return out


META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
META_ATTR = re.compile(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", re.S)


def meta_content(html: str, name: str) -> str:
    for tag in META_TAG.findall(html):
        attrs = {key.lower(): value for key, _, value in META_ATTR.findall(tag)}
        if attrs.get("name", "").lower() == name.lower():
            return attrs.get("content", "").strip()
    return ""


# ============================================================
# Scan (single pass, shared by several checks)
# ============================================================

class Scan:
    def __init__(self) -> None:
        self.files = html_files()
        self.missing_assets: Counter[str] = Counter()
        self.missing_links: Counter[str] = Counter()
        self.linked_pages: set[str] = set()
        for f in self.files:
            html = read(f)
            for ref in refs_in(html):
                rel = resolve(ref, f)
                if rel is None:
                    continue
                if target_exists(rel):
                    if not ASSET_EXT.search(rel) or rel.endswith(".html"):
                        self.linked_pages.add(rel)
                    continue
                if ASSET_EXT.search(rel) and not rel.endswith(".html"):
                    self.missing_assets[ref] += 1
                else:
                    self.missing_links[ref] += 1


# ============================================================
# FAIL tier
# ============================================================

def check_hero(results: list[Result]) -> None:
    """Homepage LCP image: modern format with a working fallback, plus dims."""
    html = read("index.html")

    results.append(
        Result("FAIL", "hero webp exists", exists(HERO_WEBP), HERO_WEBP)
    )
    results.append(
        Result("FAIL", "hero jpg fallback exists", exists(HERO_JPG), HERO_JPG)
    )

    if exists(HERO_WEBP) and exists(HERO_JPG):
        w = os.path.getsize(os.path.join(ROOT, HERO_WEBP))
        j = os.path.getsize(os.path.join(ROOT, HERO_JPG))
        pct = (1 - w / j) * 100
        results.append(
            Result(
                "FAIL",
                "hero webp smaller than jpg",
                w < j,
                f"{w:,}B vs {j:,}B ({pct:.1f}% smaller)",
            )
        )

    pic = re.search(r"<picture>(.*?)</picture>", html, re.S | re.I)
    results.append(Result("FAIL", "hero uses <picture>", bool(pic)))
    if pic:
        inner = pic.group(1)
        results.append(
            Result(
                "FAIL",
                "hero <source> is image/webp",
                'type="image/webp"' in inner and HERO_WEBP in inner,
            )
        )
        results.append(
            Result("FAIL", "hero <img> falls back to jpg", HERO_JPG in inner)
        )

    # Every referenced hero asset must be a real file — this is the exact class
    # of defect (a .webp reference with no .webp on disk) that this guards.
    hero_refs = [r for r in refs_in(html) if "/images/hero/" in r]
    bad = [r for r in hero_refs if (rel := resolve(r, "index.html")) and not exists(rel)]
    results.append(
        Result("FAIL", "no broken hero asset refs", not bad, ", ".join(bad[:3]))
    )

    # CLS: intrinsic dimensions on every homepage <img>.
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    nodim = [
        t for t in imgs
        if not (re.search(r'\bwidth="\d+"', t) and re.search(r'\bheight="\d+"', t))
    ]
    results.append(
        Result(
            "FAIL",
            "homepage <img> all have width+height",
            not nodim,
            f"{len(nodim)}/{len(imgs)} missing",
        )
    )


def check_metadata_limits(results: list[Result], scan: Scan) -> None:
    """Every real indexable page must satisfy the binding metadata limits."""
    short: list[str] = []
    long: list[str] = []
    held_long: list[str] = []
    for f in scan.files:
        html = read(f)
        if not re.search(r"<html\b", html, re.I):
            continue
        if "noindex" in meta_content(html, "robots").lower():
            continue
        desc = meta_content(html, "description")
        if len(desc) < DESC_MIN:
            short.append(f)
        elif len(desc) > DESC_MAX:
            if f in HELD_LONG_DESCRIPTIONS:
                held_long.append(f)
            else:
                long.append(f)

    results.append(
        Result(
            "FAIL",
            f"indexable descriptions are at least {DESC_MIN} chars",
            not short,
            f"{len(short)} page(s): {', '.join(short[:3])}",
        )
    )
    results.append(
        Result(
            "FAIL",
            f"indexable descriptions are at most {DESC_MAX} chars",
            not long,
            f"{len(long)} page(s): {', '.join(long[:3])}",
        )
    )
    results.append(
        Result(
            "FAIL",
            "held long descriptions stay inside the exact exception set",
            set(held_long) <= HELD_LONG_DESCRIPTIONS,
            f"{len(held_long)} held page(s): {', '.join(held_long)}",
        )
    )


def check_email_obfuscation(results: list[Result], scan: Scan) -> None:
    """Cloudflare Email Obfuscation rewrites mailto: to /cdn-cgi/l/email-protection,
    which 404s. The only repo-side opt-out is the <!--email_off--> marker pair."""
    SKIP = re.compile(r"<script\b.*?</script>|<style\b.*?</style>", re.S | re.I)
    EMAIL = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|net|org|gov|edu|io|co)\b", re.I
    )
    OPEN, CLOSE = "<!--email_off-->", "<!--/email_off-->"

    unwrapped: list[str] = []
    unbalanced: list[str] = []
    hardcoded: list[str] = []

    for f in scan.files:
        html = read(f)

        if "/cdn-cgi/l/email-protection" in html:
            hardcoded.append(f)

        n_open, n_close = html.count(OPEN), html.count(CLOSE)
        if n_open != n_close:
            unbalanced.append(f"{f} ({n_open}/{n_close})")

        # Blank out script/style, then blank out every email_off region; any
        # anchor mailto: or visible address still standing is unprotected.
        # Cloudflare only rewrites <a href="mailto:"> and text nodes — it leaves
        # other attributes (e.g. a <form action="mailto:">) alone.
        stripped = SKIP.sub(lambda m: " " * len(m.group(0)), html)
        stripped = re.sub(
            re.escape(OPEN) + r".*?" + re.escape(CLOSE),
            lambda m: " " * len(m.group(0)),
            stripped,
            flags=re.S,
        )
        if re.search(r'<a\b[^>]*\bhref="mailto:', stripped, re.I) or EMAIL.search(
            re.sub(r"<[^>]+>", " ", stripped)
        ):
            unwrapped.append(f)

    results.append(
        Result(
            "FAIL",
            "email_off markers balanced",
            not unbalanced,
            "; ".join(unbalanced[:3]),
        )
    )
    results.append(
        Result(
            "FAIL",
            "every mailto/visible email is email_off wrapped",
            not unwrapped,
            f"{len(unwrapped)} file(s): " + ", ".join(unwrapped[:3]),
        )
    )
    results.append(
        Result(
            "FAIL",
            "no hardcoded /cdn-cgi/l/email-protection links",
            not hardcoded,
            ", ".join(hardcoded[:3]),
        )
    )


def sitemap_children() -> list[str]:
    root = ET.fromstring(read(SITEMAP_INDEX))
    out = []
    for el in root.iter(SM_NS + "loc"):
        out.append(el.text.strip().replace(BASE + "/", ""))
    return out


def locs(rel: str) -> list[str]:
    root = ET.fromstring(read(rel))
    return [el.text.strip() for el in root.iter(SM_NS + "loc")]


def loc_to_path(loc: str) -> str:
    return unquote(urlsplit(loc).path).lstrip("/")


def check_sitemaps(results: list[Result]) -> None:
    children = sitemap_children()
    results.append(
        Result("FAIL", "sitemap-index lists children", len(children) >= 7, f"{len(children)}")
    )

    all_child_locs: set[str] = set()
    unparsed: list[str] = []
    for c in children + [MASTER_SITEMAP]:
        if not exists(c):
            unparsed.append(f"{c} missing")
            continue
        try:
            ET.fromstring(read(c))
        except ET.ParseError as e:
            unparsed.append(f"{c}: {e}")
    results.append(
        Result("FAIL", "all sitemaps parse as XML", not unparsed, "; ".join(unparsed[:3]))
    )
    if unparsed:
        return

    for c in children:
        all_child_locs.update(locs(c))
    master = set(locs(MASTER_SITEMAP))

    # An image sitemap legitimately cross-lists pages, so compare on the
    # non-image children only.
    page_children = [c for c in children if "image" not in c]
    page_locs: set[str] = set()
    for c in page_children:
        page_locs.update(locs(c))

    orphan_master = sorted(master - page_locs)
    orphan_child = sorted(page_locs - master)
    results.append(
        Result(
            "FAIL",
            "master sitemap == union of children",
            not orphan_master and not orphan_child,
            f"master-only={len(orphan_master)} child-only={len(orphan_child)} "
            + ", ".join((orphan_master + orphan_child)[:3]),
        )
    )

    nonhtml, missing, noindexed, cross_canon, badparent = [], [], [], [], []
    STUB = re.compile(r'<meta[^>]+http-equiv="refresh"', re.I)
    NOINDEX = re.compile(r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex', re.I)
    CANON = re.compile(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I)
    stubs = []

    for loc in sorted(all_child_locs | master):
        path = loc_to_path(loc)
        if path and not path.endswith("/") and not path.endswith(".html"):
            nonhtml.append(loc)
            continue
        rel = os.path.join(path, "index.html") if (path == "" or path.endswith("/")) else path
        if not exists(rel):
            missing.append(loc)
            continue
        html = read(rel)
        if STUB.search(html):
            stubs.append(loc)
        if NOINDEX.search(html):
            noindexed.append(loc)
        m = CANON.search(html)
        if m and m.group(1).rstrip("/") != loc.rstrip("/"):
            cross_canon.append(f"{loc} -> {m.group(1)}")
        # Every ancestor directory of a sitemap URL must itself resolve, or the
        # crawler walks into a 404 parent (the /author/, /blog-2026/, /doral/ bug).
        parts = [p for p in path.split("/")[:-1] if p]
        for i in range(len(parts)):
            parent = "/".join(parts[: i + 1])
            if not exists(os.path.join(parent, "index.html")):
                badparent.append(f"/{parent}/ (parent of {loc})")

    results.append(Result("FAIL", "no non-HTML entries in urlsets", not nonhtml, ", ".join(nonhtml[:3])))
    results.append(Result("FAIL", "every sitemap URL has a file", not missing, ", ".join(missing[:3])))
    results.append(Result("FAIL", "no meta-refresh stubs in sitemaps", not stubs, ", ".join(stubs[:3])))
    results.append(Result("FAIL", "no noindex pages in sitemaps", not noindexed, ", ".join(noindexed[:3])))
    results.append(
        Result("FAIL", "sitemap URLs are self-canonical", not cross_canon, "; ".join(cross_canon[:3]))
    )
    results.append(
        Result(
            "FAIL",
            "no 404 parent paths above sitemap URLs",
            not badparent,
            "; ".join(sorted(set(badparent))[:3]),
        )
    )

    # Market representation: each named hub is either in a sitemap itself or
    # canonicalises to a URL that is.
    unrepresented = []
    for hub in TARGET_MARKET_HUBS:
        index = os.path.join(hub, "index.html")
        if not exists(index):
            continue
        url = f"{BASE}/{hub}/"
        if url in page_locs:
            continue
        m = CANON.search(read(index))
        if m and m.group(1) in page_locs:
            continue
        unrepresented.append(hub + (f" -> {m.group(1)}" if m else " (no canonical)"))
    results.append(
        Result(
            "FAIL",
            "target markets represented in a sitemap",
            not unrepresented,
            "; ".join(unrepresented[:4]),
        )
    )


def check_parent_paths(results: list[Result], scan: Scan) -> None:
    """A crawler that trims an internally-linked URL back to its parent
    directory must not hit a 404. Directories nothing links into (unpublished
    drafts, the gated dealer portal) are out of scope by construction."""
    missing: set[str] = set()
    for rel in scan.linked_pages:
        parts = [p for p in rel.split("/")[:-1] if p and p != "."]
        for i in range(len(parts)):
            parent = "/".join(parts[: i + 1])
            if not exists(os.path.join(parent, "index.html")):
                missing.add(f"/{parent}/")
    results.append(
        Result(
            "FAIL",
            "every linked directory path has an index",
            not missing,
            f"{len(missing)}: " + ", ".join(sorted(missing)[:4]),
        )
    )


# ============================================================
# WARN tier — pinned pre-existing debt
# ============================================================

def check_link_debt(results: list[Result], scan: Scan) -> None:
    a_refs = sum(scan.missing_assets.values())
    l_distinct = len(scan.missing_links)
    l_refs = sum(scan.missing_links.values())

    results.append(
        Result(
            "WARN",
            f"missing local assets <= baseline {BASELINE_MISSING_ASSET_REFS}",
            a_refs <= BASELINE_MISSING_ASSET_REFS,
            f"{a_refs} ref(s): " + ", ".join(list(scan.missing_assets)[:4]),
        )
    )
    results.append(
        Result(
            "WARN",
            f"missing link targets <= baseline {BASELINE_MISSING_LINK_TARGETS}",
            l_distinct <= BASELINE_MISSING_LINK_TARGETS,
            f"{l_distinct} distinct / {l_refs} refs: "
            + ", ".join(t for t, _ in scan.missing_links.most_common(4)),
        )
    )
    results.append(
        Result(
            "WARN",
            f"missing link refs <= baseline {BASELINE_MISSING_LINK_REFS}",
            l_refs <= BASELINE_MISSING_LINK_REFS,
            f"{l_refs} refs",
        )
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-warn", action="store_true", help="WARN misses also exit non-zero")
    args = ap.parse_args()

    started = time.time()
    print(f"\ncrawl-check against {ROOT}\n")

    scan = Scan()
    results: list[Result] = []

    check_hero(results)
    check_metadata_limits(results, scan)
    check_email_obfuscation(results, scan)
    check_sitemaps(results)
    check_parent_paths(results, scan)
    check_link_debt(results, scan)

    for r in results:
        print(r.fmt())

    fail_misses = sum(1 for r in results if r.tier == "FAIL" and not r.ok)
    warn_misses = sum(1 for r in results if r.tier == "WARN" and not r.ok)
    print(
        f"\nSummary: {len(scan.files)} HTML files scanned, FAIL miss={fail_misses}, "
        f"WARN miss={warn_misses}, total checks={len(results)}, {time.time() - started:.1f}s"
    )

    if fail_misses or (args.strict_warn and warn_misses):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
