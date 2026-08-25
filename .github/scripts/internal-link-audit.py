#!/usr/bin/env python3
"""
internal-link-audit.py: Internal link architecture audit for acglass.com

Static analysis of the repository (no HTTP), so it runs on a pull request
before anything is deployed. It builds the site's internal link graph from the
tracked .html files and enforces the link architecture:

  FAIL: the home link resolves to "/", no internal link is aimed at a URL
          vercel.json already 301s, no internal link is broken, the homepage
          reaches every priority market and service hub, and every priority
          page clears its inbound-link floor. Indexable pages must not link to
          noindex pages, meta-refresh stubs, or known redirect sources.
  WARN: anchor-text quality on the priority market pages (bare toponyms such
          as "Miami" carry no intent; "commercial glazing contractor in Miami"
          does), and the link defects stranded on pages that
          .github/seo/url-primaries.json freezes byte-identical to main.

Usage:
  python .github/scripts/internal-link-audit.py            # audit + exit code
  python .github/scripts/internal-link-audit.py --report   # inbound-link table
  python .github/scripts/internal-link-audit.py --strict-warn

Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import html as htmllib
import json
import os
import re
import sys
from collections import defaultdict
from posixpath import normpath

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://acglass.com"

# Directories that are not part of the served page graph. "drafts" is a staging
# area whose pages cross-link at the root URLs they will occupy once published,
# so its outbound links are forward references, not breakage.
SKIP_DIRS = {
    ".git",
    ".github",
    "_internal",
    "node_modules",
    "images",
    "fonts",
    "videos",
    "drafts",
}

# Pages that are fragments/previews rather than real documents. They are not
# crawled for outbound links and never count as an inbound linker.
NON_PAGES = {
    "/location-template-snippet.html",
    "/services-schema-block.html",
    "/redesign-preview.html",
    "/index-proof.html",
}

# Authentication destinations are intentionally noindex but remain valid
# navigation targets for users who need to sign in.
ALLOWED_NOINDEX_LINK_TARGETS = {
    "/dealer/login.html",
}

# These exact source-target pairs are held behind approval gates. The exception
# is edge-specific, so any new indexable page linking to the same targets still
# fails the audit.
HELD_INDEXABILITY_EDGE_HASHES = {
    # The two /federal-glazing-contractor-tennessee.html edges were retired in the
    # 2026-08 compliance scrub: the links were removed at source, so the held
    # exception is no longer needed and must not be re-granted.
    (
        "/government-glazing-contractor-florida.html",
        "/wbe-sbe-procurement.html",
    ): "a27662a84b12946fdcbca76e78aa733e66cb58fbc555ffb024fe0f95a5d293a7",
    (
        "/government-public-sector-glazing.html",
        "/wbe-sbe-procurement.html",
    ): "ec11f1072b94998b39fcd47378aed5acb5ca874626221190d3856ef29ea6c497",
    (
        "/scope-engine.html",
        "/commercial-glazing-nashville-tn.html",
    ): "56d53a3423a0f149726ca6defe5809c4256c2828902950d85c70fbce3d8a4bdc",
    (
        "/blog/ocean-prime-ft-lauderdale-glazing.html",
        "/author-connor-walsh.html",
    ): "4851026cd8413cbe3492ad886acb4f030df4e1a341be229b1872c9e16bdab560",
}

A_TAG = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.IGNORECASE | re.DOTALL)
HREF = re.compile(r"""href\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
TAG = re.compile(r"<[^>]+>")
META_TAG = re.compile(r"<meta\b[^>]*>", re.IGNORECASE | re.DOTALL)
HTML_ATTR = re.compile(
    r"""([^\s=/>]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""",
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# Priority architecture: what this audit exists to protect
# ---------------------------------------------------------------------------

# Market hub → (label, minimum distinct inbound linking pages)
PRIORITY_MARKETS = {
    "/glazing-contractor-florida.html": ("Florida", 12),
    "/commercial-glazing-south-florida.html": ("South Florida", 10),
    "/storefront-glazier-west-palm-beach-florida/": ("West Palm Beach", 10),
    "/storefront-glazier-miami-florida/": ("Miami", 10),
    "/commercial-glazing-jacksonville.html": ("Jacksonville", 8),
    "/storefront-glazier-tampa-florida/": ("Tampa", 10),
    "/storefront-glazier-orlando-florida/": ("Orlando", 8),
    "/storefront-glazier-naples-florida/": ("Naples", 8),
    "/storefront-glazier-fort-lauderdale-florida/": ("Fort Lauderdale", 8),
    "/storefront-glazier-boca-raton-florida/": ("Boca Raton", 6),
}

# Service hub → (label, minimum distinct inbound linking pages)
PRIORITY_SERVICES = {
    "/commercial-storefront-installer-florida.html": ("Storefront glazing", 10),
    "/curtainwall-contractor-florida.html": ("Curtain wall", 10),
    "/impact-windows-doors-florida.html": ("Commercial impact windows", 8),
    "/division-08-subcontractor-florida.html": ("Division 08 / preconstruction", 10),
    "/government-public-sector-glazing.html": ("Federal & security glazing", 8),
    "/portfolio.html": ("Case studies", 10),
    "/florida-commercial-glazing-complete-guide/": ("Florida pillar guide", 8),
}

PRIORITY = {**PRIORITY_MARKETS, **PRIORITY_SERVICES}

# Pages that must link to every priority hub. The homepage is the site's
# strongest page; service-areas is the browseable geographic index.
MUST_LINK_ALL_MARKETS = ["/", "/service-areas.html"]
MUST_LINK_ALL_SERVICES = ["/", "/services.html"]

# A market anchor is "vague" when it is only the place name. Anchors are
# compared after lowercasing and stripping punctuation.
INTENT_TOKENS = (
    "glazing",
    "glazier",
    "storefront",
    "curtain wall",
    "curtainwall",
    "impact window",
    "glass",
    "contractor",
    "subcontractor",
    "installer",
    "division 08",
)

# How many distinct pages must describe a market hub with an intent-bearing
# anchor. See check_anchor_intent for why this is a page count, not a share.
ANCHOR_INTENT_FLOOR = 6

# Non-canonical links stranded on the West Palm Beach pages that
# url-primaries.json freezes: 14 "/index.html" logo hrefs plus 5 links into 301
# sources, all on files this PR is forbidden to touch. See load_frozen.
FROZEN_LINK_DEBT_BASELINE = 19


# ---------------------------------------------------------------------------
# Link graph
# ---------------------------------------------------------------------------


def iter_html_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def url_for(path: str, root: str) -> str:
    """Repo file path → the canonical served URL path."""
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def anchor_text(inner: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(TAG.sub(" ", inner))).strip()


def meta_attributes(tag: str) -> dict[str, str]:
    """Return case-normalized attributes from one meta tag."""
    attrs = {}
    for match in HTML_ATTR.finditer(tag):
        value = next(v for v in match.groups()[1:] if v is not None)
        attrs[match.group(1).lower()] = htmllib.unescape(value).strip()
    return attrs


def page_indexing_flags(doc: str) -> tuple[bool, bool]:
    """Return (noindex, meta_refresh) for an HTML document.

    A robots or googlebot directive of ``none`` is equivalent to noindex plus
    nofollow. Attribute order, quoting style, and case are intentionally
    ignored so a harmless markup reformat cannot bypass the gate.
    """
    noindex = False
    meta_refresh = False
    for tag in META_TAG.findall(doc):
        attrs = meta_attributes(tag)
        name = attrs.get("name", "").lower()
        if name in {"robots", "googlebot"}:
            directives = {
                token
                for token in re.split(r"[\s,]+", attrs.get("content", "").lower())
                if token
            }
            noindex = noindex or bool(directives & {"noindex", "none"})
        meta_refresh = meta_refresh or attrs.get("http-equiv", "").lower() == "refresh"
    return noindex, meta_refresh


def classify_pages(pages: dict[str, str]) -> tuple[set[str], set[str]]:
    """Return the noindex and meta-refresh URL sets for the served page map."""
    noindex = set()
    meta_refresh = set()
    for url, path in pages.items():
        with open(path, encoding="utf-8", errors="replace") as fh:
            flags = page_indexing_flags(fh.read())
        if flags[0]:
            noindex.add(url)
        if flags[1]:
            meta_refresh.add(url)
    return noindex, meta_refresh


def normalize(href: str, from_url: str, known: set[str]) -> str | None:
    """Resolve an href to a site-internal URL path, or None if not internal.

    The returned path is the *served* form: directory URLs keep their trailing
    slash, extension URLs keep ".html". "/index.html" is deliberately NOT
    folded into "/". Routing every page's home link through a non-canonical
    duplicate is one of the things this audit checks for.
    """
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if href.startswith("//"):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        if not href.startswith(SITE):
            return None
        href = href[len(SITE) :] or "/"
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    if not href.startswith("/"):
        base = from_url if from_url.endswith("/") else from_url.rsplit("/", 1)[0] + "/"
        href = base + href
    trailing = href.endswith("/")
    href = normpath(href)
    if trailing and not href.endswith("/"):
        href += "/"
    if not href.startswith("/"):
        return None
    # Extensionless hrefs: the site serves them with cleanUrls/trailingSlash,
    # so resolve to whichever form actually exists in the repo.
    if not href.endswith("/") and "." not in href.rsplit("/", 1)[-1]:
        if href + "/" in known:
            return href + "/"
        if href + ".html" in known:
            return href + ".html"
    return href


def build_graph(root: str):
    files = sorted(iter_html_files(root))
    pages = {}
    for f in files:
        u = url_for(f, root)
        if u in NON_PAGES:
            continue
        pages[u] = f
    known = set(pages)

    # url -> {source_url -> [anchor, ...]}
    inbound: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    outbound: dict[str, set[str]] = defaultdict(set)

    for u, f in pages.items():
        with open(f, encoding="utf-8", errors="replace") as fh:
            doc = fh.read()
        for attrs, inner in A_TAG.findall(doc):
            m = HREF.search(attrs)
            if not m:
                continue
            target = normalize(m.group(1), u, known)
            if target is None or target == u:
                continue
            inbound[target][u].append(anchor_text(inner))
            outbound[u].add(target)

    return pages, known, inbound, outbound


def load_redirects(root: str) -> dict[str, str]:
    with open(os.path.join(root, "vercel.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
    return {r["source"]: r["destination"] for r in cfg.get("redirects", [])}


def load_frozen(root: str) -> set[str]:
    """Page URLs that url-primaries.json freezes byte-identical to main.

    canonical-verify.py gates those files against git, so this audit cannot ask
    for a link on one to be rewritten. The two gates would be unsatisfiable
    together. Their defects move to check_frozen_page_debt instead of being
    dropped, so the set cannot grow unnoticed while the freeze holds.
    """
    path = os.path.join(root, ".github", "seo", "url-primaries.json")
    if not os.path.isfile(path):
        return set()
    with open(path, encoding="utf-8") as fh:
        prefixes = json.load(fh).get("frozen_prefixes", [])
    frozen = set()
    for url in prefixes:
        rel = url.lstrip("/")
        rel = rel + "index.html" if (rel == "" or rel.endswith("/")) else rel
        if os.path.isfile(os.path.join(root, rel)):
            frozen.add(url_for(os.path.join(root, rel), root))
        if url.endswith("/") and url != "/":
            for dirpath, _, names in os.walk(os.path.join(root, url.strip("/"))):
                for n in names:
                    if n.endswith(".html"):
                        frozen.add(url_for(os.path.join(dirpath, n), root))
    return frozen


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


class Result:
    def __init__(self, tier: str, name: str, ok: bool, detail: str = ""):
        self.tier = tier
        self.name = name
        self.ok = ok
        self.detail = detail

    def fmt(self) -> str:
        sym = "✓" if self.ok else "✗"
        return f"  [{sym}] {self.tier:4}  {self.name}{(': ' + self.detail) if self.detail else ''}"


def check_home_link(results, inbound, frozen):
    linkers = sorted(set(inbound.get("/index.html", {})) - frozen)
    results.append(
        Result(
            "FAIL",
            "No internal link targets /index.html (use /)",
            not linkers,
            f"{len(linkers)} page(s), e.g. {linkers[:5]}" if linkers else "",
        )
    )


def check_no_links_to_redirects(results, inbound, redirects, frozen):
    offenders = {}
    for source, dest in redirects.items():
        linkers = sorted(set(inbound.get(source, {})) - frozen)
        if linkers:
            offenders[source] = (dest, linkers)
    detail = ""
    if offenders:
        worst = sorted(offenders.items(), key=lambda kv: -len(kv[1][1]))[:5]
        detail = "; ".join(f"{s} ({len(l)} linkers) → {d}" for s, (d, l) in worst)
    results.append(
        Result("FAIL", "No internal link targets a 301 source", not offenders, detail)
    )


def check_no_broken_links(results, inbound, known, redirects, frozen):
    broken = {}
    for target, linkers in inbound.items():
        if target in known or target in redirects:
            continue
        # Non-HTML assets and directory URLs served by other means are out of
        # scope; only flag things that look like pages.
        leaf = target.rstrip("/").rsplit("/", 1)[-1]
        if "." in leaf and not target.endswith(".html"):
            continue
        live = sorted(set(linkers) - frozen)
        if live:
            broken[target] = live
    detail = ""
    if broken:
        worst = sorted(broken.items(), key=lambda kv: -len(kv[1]))[:6]
        detail = "; ".join(f"{t} ({len(l)})" for t, l in worst)
    results.append(
        Result("FAIL", "No internal link targets a missing page", not broken, detail)
    )
    return broken


def _offender_detail(offenders: dict[str, list[str]]) -> str:
    if not offenders:
        return ""
    worst = sorted(offenders.items(), key=lambda item: (-len(item[1]), item[0]))[:5]
    return "; ".join(
        f"{target} ({len(linkers)} indexable linker(s), e.g. {linkers[:3]})"
        for target, linkers in worst
    )


def edge_fingerprint(anchors: list[str]) -> str:
    payload = json.dumps(tuple(anchors), ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def check_indexable_link_targets(results, inbound, pages, redirects, frozen):
    """Block indexable pages from linking into crawl and routing dead ends.

    A noindex or meta-refresh source is not an indexable linker, and an edge
    redirect source is not a served page. Frozen source pages stay excluded in
    the same way as the existing redirect and broken-link checks. Their known
    non-canonical debt remains governed by ``check_frozen_page_debt``.
    """
    noindex, meta_refresh = classify_pages(pages)
    redirect_sources = set(redirects)
    indexable_sources = set(pages) - noindex - meta_refresh - redirect_sources
    blocked_any = noindex | meta_refresh | redirect_sources
    exact_held_edges = {
        (source, target)
        for (source, target), fingerprint in HELD_INDEXABILITY_EDGE_HASHES.items()
        if source in indexable_sources
        and target in blocked_any
        and edge_fingerprint(inbound.get(target, {}).get(source, [])) == fingerprint
    }

    checks = (
        (
            "Indexable pages do not link to noindex pages",
            noindex - ALLOWED_NOINDEX_LINK_TARGETS,
        ),
        ("Indexable pages do not link to meta-refresh stubs", meta_refresh),
        ("Indexable pages do not link to known redirect sources", redirect_sources),
    )
    for name, blocked_targets in checks:
        offenders = {}
        for target in blocked_targets:
            linkers = sorted(
                source
                for source in (
                    (set(inbound.get(target, {})) & indexable_sources) - frozen
                )
                if (source, target) not in exact_held_edges
            )
            if linkers:
                offenders[target] = linkers
        results.append(
            Result("FAIL", name, not offenders, _offender_detail(offenders))
        )
    missing_or_changed = sorted(
        set(HELD_INDEXABILITY_EDGE_HASHES) - exact_held_edges
    )
    results.append(
        Result(
            "FAIL",
            "held indexability edges match exact anchor and count fingerprints",
            not missing_or_changed,
            f"changed or stale: {missing_or_changed[:3]}" if missing_or_changed else "",
        )
    )


def check_frozen_page_debt(results, inbound, redirects, frozen):
    """The link defects the freeze makes unfixable, held at a baseline.

    Reported rather than waived: if the freeze lifts these become FAILs again,
    and while it holds the count must not grow.
    """
    refs = 0
    for target in ["/index.html", *redirects]:
        refs += len(set(inbound.get(target, {})) & frozen)
    results.append(
        Result(
            "WARN",
            f"non-canonical links on frozen pages ≤ baseline {FROZEN_LINK_DEBT_BASELINE}",
            refs <= FROZEN_LINK_DEBT_BASELINE,
            f"{refs} ref(s) on pages url-primaries.json freezes",
        )
    )


def check_hub_coverage(results, outbound, known):
    for hub in MUST_LINK_ALL_MARKETS:
        if hub not in known:
            continue
        missing = [t for t in PRIORITY_MARKETS if t not in outbound.get(hub, ())]
        results.append(
            Result(
                "FAIL",
                f"{hub} links to all {len(PRIORITY_MARKETS)} priority markets",
                not missing,
                f"missing={missing}" if missing else "",
            )
        )
    for hub in MUST_LINK_ALL_SERVICES:
        if hub not in known:
            continue
        missing = [t for t in PRIORITY_SERVICES if t not in outbound.get(hub, ())]
        results.append(
            Result(
                "FAIL",
                f"{hub} links to all {len(PRIORITY_SERVICES)} priority service hubs",
                not missing,
                f"missing={missing}" if missing else "",
            )
        )


def check_inbound_floors(results, inbound):
    for target, (label, floor) in PRIORITY.items():
        n = len(inbound.get(target, {}))
        results.append(
            Result(
                "FAIL",
                f"{label} ≥{floor} inbound",
                n >= floor,
                f"{target} has {n}",
            )
        )


def check_anchor_intent(results, inbound):
    """Count *pages* that link with an intent-bearing anchor, not the share.

    A share metric would penalise the city directories and county pages, where a
    bare toponym is the correct anchor for a list entry. Raising a percentage
    means rewriting those list anchors into keyword phrases, which is the
    stuffing this audit exists to discourage. What matters is that a real number
    of pages describe the target with intent, so that is what is measured.
    """
    for target, (label, _floor) in PRIORITY_MARKETS.items():
        linkers = inbound.get(target, {})
        intentful = sorted(
            src
            for src, anchors in linkers.items()
            if any(t in a.lower() for a in anchors for t in INTENT_TOKENS)
        )
        results.append(
            Result(
                "WARN",
                f"{label}: ≥{ANCHOR_INTENT_FLOOR} pages link with an intent-bearing anchor",
                len(intentful) >= ANCHOR_INTENT_FLOOR,
                f"{len(intentful)}/{len(linkers)} linking pages",
            )
        )


def report(inbound, outbound):
    print(f"\n{'PRIORITY PAGE':<52}{'INBOUND':>8}  ANCHORS (top 3)")
    print("-" * 110)
    for target, (label, floor) in PRIORITY.items():
        linkers = inbound.get(target, {})
        anchors = [a for lst in linkers.values() for a in lst if a]
        top = sorted({a: anchors.count(a) for a in anchors}.items(), key=lambda kv: -kv[1])[:3]
        top_s = ", ".join(f"{a!r}×{c}" for a, c in top)
        flag = " " if len(linkers) >= floor else "!"
        print(f"{flag}{target:<51}{len(linkers):>8}  {top_s[:60]}")
    print(f"\nhomepage outbound internal links: {len(outbound.get('/', ()))}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=REPO)
    ap.add_argument("--report", action="store_true", help="print the inbound-link table")
    ap.add_argument("--strict-warn", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    pages, known, inbound, outbound = build_graph(root)
    redirects = load_redirects(root)
    frozen = load_frozen(root)

    print(f"\ninternal-link-audit: {len(pages)} pages, {sum(len(v) for v in outbound.values())} internal links\n")

    results: list[Result] = []
    check_home_link(results, inbound, frozen)
    check_no_links_to_redirects(results, inbound, redirects, frozen)
    check_no_broken_links(results, inbound, known, redirects, frozen)
    check_indexable_link_targets(results, inbound, pages, redirects, frozen)
    check_frozen_page_debt(results, inbound, redirects, frozen)
    check_hub_coverage(results, outbound, known)
    check_inbound_floors(results, inbound)
    check_anchor_intent(results, inbound)

    for r in results:
        print(r.fmt())

    if args.report:
        report(inbound, outbound)

    fails = sum(1 for r in results if r.tier == "FAIL" and not r.ok)
    warns = sum(1 for r in results if r.tier == "WARN" and not r.ok)
    print(f"\nSummary: FAIL miss={fails}, WARN miss={warns}, total checks={len(results)}")

    if fails:
        return 1
    if args.strict_warn and warns:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
