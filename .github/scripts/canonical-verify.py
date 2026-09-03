#!/usr/bin/env python3
"""Verify the one-primary-per-intent URL map in .github/seo/url-primaries.json.

SCOPE, STATED PLAINLY
---------------------
By default this script verifies INTENT ONLY. It reads files on disk and answers
"does the repository declare the primaries it says it declares, consistently?"
It does NOT and CANNOT verify deployed behaviour:

  * The site is GitHub Pages behind Cloudflare. GitHub Pages does not read
    vercel.json, so every 301 on the live site is executed at the Cloudflare
    edge, outside this repository.
  * vercel.json is an accurate MIRROR of that edge config, not the deploy
    mechanism. Editing it ships nothing.

Deployed behaviour is checked only under --live, which performs real HTTP HEAD
requests and asserts that the edge agrees with vercel.json. --live is not part
of the CI gate: it needs network access and it fails on edge changes that have
nothing to do with the commit under test.

Exit 1 on any FAIL. WARN never fails the build.
"""

from __future__ import annotations

import argparse
import hashlib
import html as htmllib
import json
import os
import re
import subprocess
import sys

BASE = "https://acglass.com"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, ".github", "seo", "url-primaries.json")
TARGETS = os.path.join(ROOT, ".github", "seo", "seo-targets.json")
MANIFEST = os.path.join(ROOT, ".github", "cloudflare", "redirects.manifest.json")
VERCEL = os.path.join(ROOT, "vercel.json")

CANONICAL_RE = re.compile(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I)
ANCHOR_RE = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
ANCHOR_PAIR_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
SCHEMA_ITEM_RE = re.compile(r'"item"\s*:\s*"([^"]+)"')
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")

META_TAG_RE = re.compile(r"<meta\b[^>]*>", re.I)
LINK_TAG_RE = re.compile(r"<link\b[^>]*>", re.I)
ATTR_RE = re.compile(r"""([\w:.\-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
LD_JSON_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
DROP_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
WPB_RE = re.compile(r"West\s+Palm\s+Beach", re.I)
SEGMENT_RE = re.compile(r"[·|\n]|(?<=\.)\s+")
# Flattening the whole homepage first made one WPB link inside #markets
# freeze the entire markets nav. Split on block/link boundaries so a
# Tennessee furnish/consult reword is not treated as a WPB deletion.
VISIBLE_BLOCK_RE = re.compile(
    r"</(?:p|div|h[1-6]|li|section|article|nav|header|footer|td|th|blockquote|a|br)\s*>",
    re.I,
)

# The entity identity the map pack resolves against.
SCHEMA_IDENTITY_TYPES = {"Organization", "LocalBusiness", "HomeAndConstructionBusiness", "WebSite"}
SCHEMA_IDENTITY_KEYS = ("@type", "name", "legalName", "url", "telephone",
                        "address", "geo", "sameAs", "areaServed", "logo")

VALID_STATUS = {"ratified", "frozen", "gsc-gated", "blocked-no-primary", "owned-elsewhere"}
NON_HTML_ASSETS = ("llms.txt", "llms-full.txt", "ai.txt", "search-index.json")
SKIP_SERVED_DIRS = {".git", ".github", "_internal", "node_modules", "drafts"}

# Exact debt that this workstream is not allowed to edit. The fingerprint covers
# href value, visible anchor text and occurrence count. A changed or missing
# edge fails, and a new source cannot inherit the exception.
HELD_CROSS_CANONICAL_EDGE_HASHES = {
    # /boca-raton/ is now self-canonical so the market stays in a sitemap after
    # wave-2 noindex of /storefront-glazier-boca-raton-florida/. The prior hold
    # on west-palm-beach/index.html -> /boca-raton is retired.
    ("medical-office-glazier-fort-lauderdale/index.html", "/fort-lauderdale"):
        "2406e8fb96ec2a68083ad6c5dff229c1f8362979b7eac38ceb98ad6da3137fd0",
    # /naples/ is now self-canonical (office metro), so this is no longer a
    # cross-canonical edge and the prior hold is retired.
    ("nashville/belle-meade-nashville/index.html", "/nashville"):
        "c8c55cc0a6c624e9551272b9a0bbd04bfbc4c853eb10366f3246bf0486f081ba",
    ("nashville/bellevue-nashville/index.html", "/nashville"):
        "c8c55cc0a6c624e9551272b9a0bbd04bfbc4c853eb10366f3246bf0486f081ba",
    ("nashville/berry-hill-nashville/index.html", "/nashville"):
        "c8c55cc0a6c624e9551272b9a0bbd04bfbc4c853eb10366f3246bf0486f081ba",
    ("nashville/downtown-nashville/index.html", "/nashville"):
        "c8c55cc0a6c624e9551272b9a0bbd04bfbc4c853eb10366f3246bf0486f081ba",
    ("nashville/east-nashville/index.html", "/nashville"):
        "4b1824e64f7bee664049e299815644693f16b234540d920a7a14f2d69daed6ae",
    ("nashville/green-hills-nashville/index.html", "/nashville"):
        "c8c55cc0a6c624e9551272b9a0bbd04bfbc4c853eb10366f3246bf0486f081ba",
    ("nashville/sobro-nashville/index.html", "/nashville"):
        "4b1824e64f7bee664049e299815644693f16b234540d920a7a14f2d69daed6ae",
    ("nashville/the-gulch-nashville/index.html", "/nashville"):
        "4b1824e64f7bee664049e299815644693f16b234540d920a7a14f2d69daed6ae",
    # Surfaced by registering the florida-statewide storefront-systems and
    # division-08 intents (2026-08-28). Both new primaries already had an
    # in-repo page rel=canonical'ing to them, so those two pages became
    # declared aliases and their pre-existing inbound links became visible to
    # this gate. Nothing here is a mislink: each edge is a listing card, a
    # resource card, or a related-reading link whose visible subject IS the
    # aliased document, and the alias forwards its signal to the primary by
    # canonical already. Rewriting a blog listing row or a resource card to
    # point at a service page would misstate what the row links to, so the
    # edges are pinned exactly instead. The two edges whose anchor text was
    # about the Division 08 scope itself were repointed to the primary rather
    # than pinned (atlantic-fields-golf-house.html and
    # tools/glazing-spec-checklist/index.html).
    ("blog/best-glass-options-florida-storefronts.html",
     "/blog/best-commercial-storefront-systems-florida.html"):
        "c66299422def48da84998f74294aa1a1b457a6180d281a4730d770ac65c196e9",
    ("infographics-index.html", "/blog/best-commercial-storefront-systems-florida.html"):
        "473b4f30254b1ebd220f037cedae5fadb90d3dfde570b8941ac28979f28f6449",
    ("division-08-subcontractor-florida.html", "/division-08-scope.html"):
        "7c5c5fad09c591864adcf7365390c03b45e4b63c8d1f0d153212aade49adc275",
    ("gulfside-twelve.html", "/division-08-scope.html"):
        "08aef69ae538f9485cdd79b8eef5f694ff7c65f4c349a34931a07c310ac6b031",
    ("resources/index.html", "/division-08-scope.html"):
        "274de0d24be2d17225d493ae67c6f48656aeabb245b0cbe1662199989dd0b24f",
}


def read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def norm(url: str) -> str:
    """Strip the origin and any trailing slash so /x/ and /x compare equal."""
    if url.startswith(BASE):
        url = url[len(BASE) :]
    return url.rstrip("/") or "/"


def file_for(url: str) -> str | None:
    """Map a site-relative URL to the file that serves it, or None."""
    path = url.split("#")[0].split("?")[0]
    if path.startswith(BASE):
        path = path[len(BASE) :]
    if not path.startswith("/"):
        return None
    path = path.lstrip("/")
    if path == "" or path.endswith("/"):
        path += "index.html"
    if not path.endswith(".html"):
        return None
    return path if os.path.isfile(os.path.join(ROOT, path)) else None


def canonical_of(url: str) -> str | None:
    rel = file_for(url)
    if not rel:
        return None
    m = CANONICAL_RE.search(read(rel))
    return m.group(1) if m else None


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, bool, str]] = []

    def add(self, level: str, name: str, ok: bool, detail: str = "") -> None:
        self.rows.append((level, name, ok, detail))

    def emit(self) -> int:
        fails = 0
        for level, name, ok, detail in self.rows:
            mark = "✓" if ok else ("✗" if level == "FAIL" else "!")
            print(f"  [{mark}] {level:4s} {name}" + (f"  — {detail}" if detail else ""))
            if not ok and level == "FAIL":
                fails += 1
        passed = sum(1 for _, _, ok, _ in self.rows if ok)
        print(f"\nSummary: {passed} passed / {fails} failed, {len(self.rows)} checks")
        return 1 if fails else 0


# ---------------------------------------------------------------------------
# static checks
# ---------------------------------------------------------------------------


def redirect_sources() -> dict[str, str]:
    """Source -> destination for every rule in vercel.json.

    vercel.json is treated as an OBSERVED MIRROR of Cloudflare, never as a
    deploy target. It is read here only to know which in-repo files are never
    actually served, so that links into them can be flagged.
    """
    if not os.path.isfile(VERCEL):
        return {}
    rules = json.loads(read("vercel.json")).get("redirects", [])
    return {norm(r["source"]): r["destination"] for r in rules if r.get("source")}


def check_registry(rep: Report, reg: dict) -> None:
    bad_status = [i for i in reg["intents"] if i["status"] not in VALID_STATUS]
    rep.add("FAIL", "every intent has a known status", not bad_status,
            ", ".join(f"{i['market']}/{i['intent']}" for i in bad_status[:3]))

    missing = [
        f"{i['market']}/{i['intent']} -> {i['primary']}"
        for i in reg["intents"]
        if i["primary"] and not file_for(i["primary"])
    ]
    rep.add("FAIL", "every declared primary resolves to a file", not missing, "; ".join(missing[:3]))

    needs_primary = [
        f"{i['market']}/{i['intent']}"
        for i in reg["intents"]
        if i["status"] in {"ratified", "gsc-gated"} and not i["primary"]
    ]
    rep.add("FAIL", "ratified and gsc-gated intents name a primary", not needs_primary,
            ", ".join(needs_primary[:3]))

    seen: dict[str, str] = {}
    dupes = []
    for i in reg["intents"]:
        if not i["primary"]:
            continue
        key = norm(i["primary"])
        label = f"{i['market']}/{i['intent']}"
        if key in seen:
            dupes.append(f"{i['primary']} claimed by {seen[key]} and {label}")
        else:
            seen[key] = label
    rep.add("FAIL", "no URL is primary for two intents", not dupes, "; ".join(dupes[:3]))

    # A storefront-glazier directory page must never hold the broad intent.
    wrong_kind = [
        f"{i['market']} -> {i['primary']}"
        for i in reg["intents"]
        if i["intent"] == "commercial-glazing"
        and i["primary"]
        and "storefront-glazier" in i["primary"]
    ]
    rep.add("FAIL", "no storefront-glazier page is a commercial-glazing primary",
            not wrong_kind, "; ".join(wrong_kind))

    near_me = [
        i["primary"] for i in reg["intents"]
        if i["market"] == "florida-statewide" and i["intent"] == "commercial-glazing"
        and i["primary"] and "near-me" in i["primary"]
    ]
    rep.add("FAIL", "statewide primary is not a near-me page", not near_me, "; ".join(near_me))


def check_primaries_self_canonical(rep: Report, reg: dict) -> None:
    bad = []
    for i in reg["intents"]:
        url = i["primary"]
        if not url or i["status"] == "frozen":
            continue
        canon = canonical_of(url)
        if canon is None:
            bad.append(f"{url} has no canonical")
        elif norm(canon) != norm(url):
            bad.append(f"{url} -> {canon}")
    rep.add("FAIL", "declared primaries are self-canonical", not bad, "; ".join(bad[:4]))


def check_consolidations(rep: Report, reg: dict, sitemap_locs: dict[str, set[str]]) -> None:
    wrong_canon, still_listed = [], []
    for i in reg["intents"]:
        for c in i.get("consolidate_in_repo", []):
            canon = canonical_of(c["url"])
            if canon is None or norm(canon) != norm(i["primary"]):
                wrong_canon.append(f"{c['url']} -> {canon} (want {i['primary']})")
            for name, locs in sitemap_locs.items():
                if norm(c["url"]) in {norm(u) for u in locs}:
                    still_listed.append(f"{c['url']} in {name}")
    rep.add("FAIL", "consolidated URLs canonicalise to their primary", not wrong_canon,
            "; ".join(wrong_canon[:4]))
    rep.add("FAIL", "consolidated URLs are absent from every sitemap", not still_listed,
            "; ".join(still_listed[:4]))


def _attrs(tag: str) -> dict[str, str]:
    out = {}
    for m in ATTR_RE.finditer(tag):
        out[m.group(1).lower()] = m.group(2) if m.group(2) is not None else m.group(3)
    return out


def _tag_content(text: str, tag_re: re.Pattern, key: str, value: str, want: str) -> str | None:
    """First <meta>/<link> whose `key` equals `value`, returning attribute `want`.

    Attribute-order independent; a regex keyed on source order would miss
    `content="..." name="robots"`.
    """
    for tag in tag_re.findall(text):
        a = _attrs(tag)
        if a.get(key, "").strip().lower() == value:
            return a.get(want)
    return None


def _text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _anchor_text_of(html: str) -> str:
    return htmllib.unescape(_text_of(html))


def _served_html_files():
    for dirpath, dirnames, names in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_SERVED_DIRS]
        for name in names:
            if name.endswith(".html"):
                yield os.path.relpath(os.path.join(dirpath, name), ROOT)


def _served_url(rel: str) -> str:
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def _resolve_internal_href(raw: str, source_rel: str) -> str | None:
    href = raw.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if href.startswith("//"):
        return None
    if href.startswith(("http://", "https://")):
        if not href.startswith(BASE):
            return None
        href = href[len(BASE):] or "/"
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    if not href.startswith("/"):
        href = "/" + os.path.normpath(
            os.path.join(os.path.dirname(source_rel), href)
        )
    return norm(href)


def _source_is_indexable(html: str, own: str, redirects: dict[str, str]) -> bool:
    if own in redirects:
        return False
    for tag in META_TAG_RE.findall(html):
        attrs = _attrs(tag)
        if attrs.get("http-equiv", "").strip().lower() == "refresh":
            return False
        if attrs.get("name", "").strip().lower() not in {"robots", "googlebot"}:
            continue
        directives = {
            token for token in re.split(r"[\s,]+", attrs.get("content", "").lower())
            if token
        }
        if directives & {"noindex", "none"}:
            return False
    return True


def _frozen_files(reg: dict) -> set[str]:
    frozen = set()
    for url in reg.get("frozen_prefixes", []):
        rel = file_for(url)
        if rel:
            frozen.add(rel)
        if url.endswith("/") and url != "/":
            directory = os.path.join(ROOT, url.strip("/"))
            for dirpath, _, names in os.walk(directory):
                for name in names:
                    if name.endswith(".html"):
                        frozen.add(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return frozen


def declared_primary_aliases(reg: dict) -> dict[str, str]:
    """Return normalized alias URL to declared primary URL."""
    primaries = {
        norm(intent["primary"]): intent["primary"]
        for intent in reg["intents"] if intent.get("primary")
    }
    aliases = {}
    for rel in _served_html_files():
        html = read(rel)
        match = CANONICAL_RE.search(html)
        if not match:
            continue
        own = norm(_served_url(rel))
        target = norm(match.group(1))
        if target in primaries and target != own:
            aliases[own] = primaries[target]
    return aliases


def cross_canonical_edge_fingerprint(entries: list[str]) -> str:
    payload = json.dumps(sorted(entries), ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def cross_canonical_inventory(reg: dict, redirects: dict[str, str]):
    """Collect href edges into aliases whose primary is declared by the registry."""
    aliases = declared_primary_aliases(reg)
    edges: dict[tuple[str, str], list[str]] = {}
    indexable_files = set()
    for rel in _served_html_files():
        html = read(rel)
        own = norm(_served_url(rel))
        if _source_is_indexable(html, own, redirects):
            indexable_files.add(rel)
        for match in ANCHOR_PAIR_RE.finditer(html):
            raw = _attrs(match.group(1)).get("href")
            if not raw:
                continue
            target = _resolve_internal_href(raw, rel)
            if target not in aliases:
                continue
            edges.setdefault((rel, target), []).append(
                f"{raw} :: {_anchor_text_of(match.group(2))}"
            )
    return aliases, edges, indexable_files, _frozen_files(reg)


def classify_cross_canonical_edges(
    edges: dict[tuple[str, str], list[str]],
    indexable_files: set[str],
    frozen_files: set[str],
    held_hashes: dict[tuple[str, str], str],
):
    offenders = []
    unpinned_frozen = []
    matched_holds = set()
    for edge, entries in sorted(edges.items()):
        fingerprint = cross_canonical_edge_fingerprint(entries)
        if held_hashes.get(edge) == fingerprint:
            matched_holds.add(edge)
            continue
        rel, target = edge
        detail = f"{rel} -> {target} ({len(entries)} href(s))"
        if rel in frozen_files:
            unpinned_frozen.append(detail)
        elif rel in indexable_files:
            offenders.append(detail)
    stale_or_changed = sorted(set(held_hashes) - matched_holds)
    return offenders, unpinned_frozen, matched_holds, stale_or_changed


def check_cross_canonical_links(rep: Report, reg: dict, redirects: dict[str, str]) -> None:
    aliases, edges, indexable_files, frozen_files = cross_canonical_inventory(
        reg, redirects
    )
    offenders, unpinned_frozen, matched_holds, stale_or_changed = (
        classify_cross_canonical_edges(
            edges,
            indexable_files,
            frozen_files,
            HELD_CROSS_CANONICAL_EDGE_HASHES,
        )
    )
    rep.add(
        "FAIL",
        "indexable safe pages link to declared primaries, not cross-canonical aliases",
        not offenders,
        f"{len(offenders)}: " + "; ".join(offenders[:4]),
    )
    rep.add(
        "FAIL",
        "frozen cross-canonical debt has an exact pinned edge",
        not unpinned_frozen,
        f"{len(unpinned_frozen)}: " + "; ".join(unpinned_frozen[:4]),
    )
    rep.add(
        "FAIL",
        "held cross-canonical edge fingerprints remain exact",
        not stale_or_changed,
        f"{len(matched_holds)} exact of {len(HELD_CROSS_CANONICAL_EDGE_HASHES)}; "
        f"changed or stale: {stale_or_changed[:3]}",
    )
    rep.add(
        "WARN",
        "cross-canonical aliases remain contained to declared primaries",
        True,
        f"{len(aliases)} aliases, {len(edges)} source-target edge(s), "
        f"{len(matched_holds)} exact held edge(s)",
    )


def _visible_text(html: str) -> str:
    return _text_of(DROP_RE.sub(" ", html))


def _ld_nodes(data):
    if isinstance(data, list):
        for item in data:
            yield from _ld_nodes(item)
    elif isinstance(data, dict):
        if "@graph" in data:
            yield from _ld_nodes(data["@graph"])
        yield data


def _schema_identity(html: str) -> dict[str, str]:
    """@id -> canonical JSON of the identity fields, for identity-bearing nodes."""
    out: dict[str, str] = {}
    for i, m in enumerate(LD_JSON_RE.finditer(html)):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError as exc:
            out[f"_unparseable_block_{i}"] = str(exc)
            continue
        for node in _ld_nodes(data):
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if not {t for t in types if isinstance(t, str)} & SCHEMA_IDENTITY_TYPES:
                continue
            key = node.get("@id") or f"{sorted(str(t) for t in types)}:{node.get('name', '')}"
            out[key] = json.dumps({k: node[k] for k in SCHEMA_IDENTITY_KEYS if k in node},
                                  sort_keys=True)
    return out


def _wpb_links(html: str, frozen_urls: set[str]) -> set[str]:
    """(href, anchor text) pairs whose target is a byte-frozen WPB URL."""
    found = set()
    for m in ANCHOR_PAIR_RE.finditer(html):
        href = _attrs(m.group(1)).get("href")
        if not href:
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        if not (target.startswith("/") or target.startswith(BASE)):
            target = "/" + target.lstrip("./")
        if norm(target) in frozen_urls:
            found.add(f"{href} :: {_text_of(m.group(2))}")
    return found


def _json_strings(data):
    if isinstance(data, dict):
        for value in data.values():
            yield from _json_strings(value)
    elif isinstance(data, list):
        for item in data:
            yield from _json_strings(item)
    elif isinstance(data, str):
        yield data


def _visible_blocks(html: str) -> list[str]:
    """Visible text, one block/link at a time.

    `_visible_text` collapses the page to a single string. That is too coarse
    for the WPB freeze: a storefront-glazier-in-West-Palm-Beach link then
    freezes every neighbor in #markets, including Tennessee geography.
    """
    body = DROP_RE.sub(" ", html)
    return [text for chunk in VISIBLE_BLOCK_RE.split(body)
            if (text := _text_of(chunk))]


def _wpb_text(html: str) -> set[str]:
    """Every West Palm Beach mention, in visible copy and in JSON-LD prose alike.

    The two strongest WPB associations on the root are inside JSON-LD
    `description` values, which visible-text extraction strips. Reading the
    parsed strings rather than the raw block keeps this insensitive to JSON
    reformatting while leaving no hole to reword through.
    """
    sources = _visible_blocks(html)
    for m in LD_JSON_RE.finditer(html):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue  # a broken block is already a schema-identity failure
        sources.extend(_json_strings(data))
    return {s.strip() for src in sources for s in SEGMENT_RE.split(src)
            if WPB_RE.search(s)}


def semantic_freeze_diff(base: str, new: str,
                         frozen_urls: set[str]) -> tuple[dict[str, str], set[str]]:
    """Compare the protected fields of one page across two versions.

    Returns (field -> failure detail) for fields that changed, plus any newly
    added links into a byte-frozen WPB URL. A field absent from both versions
    compares equal: for meta-robots, absence is the protected value.
    """
    scalars = {
        "title": lambda t: (TITLE_RE.search(t).group(1).strip() if TITLE_RE.search(t) else None),
        "meta-description": lambda t: _tag_content(t, META_TAG_RE, "name", "description", "content"),
        "canonical": lambda t: _tag_content(t, LINK_TAG_RE, "rel", "canonical", "href"),
        "meta-robots": lambda t: _tag_content(t, META_TAG_RE, "name", "robots", "content"),
        "og:title": lambda t: _tag_content(t, META_TAG_RE, "property", "og:title", "content"),
        "og:url": lambda t: _tag_content(t, META_TAG_RE, "property", "og:url", "content"),
        "h1": lambda t: " ¦ ".join(_text_of(x) for x in H1_RE.findall(t)),
    }
    failures: dict[str, str] = {}
    for field, extract in scalars.items():
        was, now = extract(base), extract(new)
        if was != now:
            failures[field] = f"was {was!r}, now {now!r}"

    was_id, now_id = _schema_identity(base), _schema_identity(new)
    if was_id != now_id:
        detail = []
        for key in sorted(set(was_id) | set(now_id)):
            if was_id.get(key) != now_id.get(key):
                if key not in now_id:
                    detail.append(f"{key} removed")
                elif key not in was_id:
                    detail.append(f"{key} added")
                else:
                    detail.append(f"{key} altered")
        failures["schema-identity"] = "; ".join(detail[:4])

    was_links, now_links = _wpb_links(base, frozen_urls), _wpb_links(new, frozen_urls)
    lost = sorted(was_links - now_links)
    if lost:
        failures["wpb-links"] = f"{len(lost)} removed or reworded: " + "; ".join(lost[:3])

    lost_text = sorted(_wpb_text(base) - _wpb_text(new))
    if lost_text:
        failures["wpb-text"] = f"{len(lost_text)} removed or reworded: " + "; ".join(
            repr(s[:70]) for s in lost_text[:3])

    return failures, now_links - was_links


def check_frozen(rep: Report, reg: dict, base_ref: str) -> None:
    """WPB and the site root must not change in this workstream.

    Two modes, both measured against base_ref rather than against content
    heuristics:

    * Byte freeze — the dedicated WPB pages. Any tracked file serving one of
      these URLs must be byte-identical. They are the contested candidates for
      the organic #1 and the ranking URL among them is unknown, so body copy is
      as frozen as the head.
    * Semantic freeze — the site root. It is the WPB Google Business Profile
      landing page, so its identity and ranking signals are frozen field by
      field, but its body is open. A byte freeze here would block ordinary
      internal-linking work for as long as the WPB freeze lasts, which is
      until a GSC baseline exists.
    """
    semantic = reg.get("semantic_freeze", {})
    byte_urls = [u for u in reg["frozen_prefixes"] if u not in semantic and not u.startswith("_")]
    frozen_norm = {norm(u) for u in byte_urls}

    frozen_files = set()
    for url in byte_urls:
        rel = file_for(url)
        if rel:
            frozen_files.add(rel)
        # Directory prefixes freeze everything beneath them.
        if url.endswith("/") and url != "/":
            d = url.strip("/")
            for dirpath, _, names in os.walk(os.path.join(ROOT, d)):
                for n in names:
                    frozen_files.add(os.path.relpath(os.path.join(dirpath, n), ROOT))

    try:
        # Diff base against the WORKING TREE, not against HEAD: this must fail
        # before an uncommitted WPB edit can be committed, not after.
        out = subprocess.run(
            ["git", "diff", "--name-only", base_ref],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        rep.add("WARN", f"frozen-path guard could not run against {base_ref}", True, str(exc)[:120])
        return

    changed = {line.strip() for line in out.splitlines() if line.strip()}
    violations = sorted(changed & frozen_files)
    rep.add("FAIL", f"no byte-frozen WPB path modified since {base_ref}", not violations,
            f"{len(violations)} of {len(frozen_files)}: " + ", ".join(violations[:4]))

    for url, spec in sorted(semantic.items()):
        if url.startswith("_"):
            continue
        rel = spec["file"]
        try:
            base_text = subprocess.run(
                ["git", "show", f"{base_ref}:{rel}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            rep.add("WARN", f"semantic freeze of {url} could not read {base_ref}:{rel}",
                    True, str(exc)[:120])
            continue

        failures, added = semantic_freeze_diff(base_text, read(rel), frozen_norm)
        for field in spec["protected_fields"]:
            detail = failures.get(field, "")
            rep.add("FAIL", f"{url} semantic freeze: {field} unchanged since {base_ref}",
                    not detail, detail)
        unexpected = sorted(set(failures) - set(spec["protected_fields"]))
        rep.add("FAIL", f"{url} semantic freeze declares every field it enforces",
                not unexpected, ", ".join(unexpected))
        rep.add("WARN", f"{url} adds no new link into a byte-frozen WPB URL", not added,
                f"{len(added)} added, nudging one contested candidate: "
                + "; ".join(sorted(added)[:3]))


def check_no_canonical_into_redirect(rep: Report, redirects: dict[str, str], sitemap_locs) -> None:
    listed = {norm(u) for locs in sitemap_locs.values() for u in locs}
    bad = []
    for url in sorted(listed):
        canon = canonical_of(url)
        if canon and norm(canon) in redirects:
            bad.append(f"{url} -> {canon} (a 301 source)")
    rep.add("FAIL", "no sitemap page canonicalises into a redirect source", not bad,
            "; ".join(bad[:4]))

    also = sorted(u for u in listed if u in redirects)
    rep.add("FAIL", "no sitemap lists a redirect source", not also, ", ".join(also[:4]))


def check_internal_references(rep: Report, reg: dict, redirects: dict[str, str]) -> None:
    """Internal links must not point at a URL that redirects or is consolidated.

    Two exemptions, both because the link is inert rather than because it is
    tolerable:

    * A file that is itself a redirect source is never served, so its own
      outbound links never reach a crawler.
    * A descendant keeps its breadcrumb link to its own parent directory. That
      parent still returns 200, the edge is a true hierarchy edge, and the
      parent's rel=canonical already forwards the signal to the primary.
      Rewriting /nashville/downtown-nashville/'s "Nashville" breadcrumb to point
      at a root-level .html file would misstate the hierarchy to fix nothing.
    """
    consolidated: set[str] = set()
    stale: dict[str, str] = {src: dest for src, dest in redirects.items()}
    for i in reg["intents"]:
        for c in i.get("consolidate_in_repo", []):
            key = norm(c["url"])
            stale[key] = i["primary"]
            consolidated.add(key)

    hits: list[str] = []
    debt: set[str] = set()
    for dirpath, dirnames, names in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for name in names:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
            own = norm("/" + rel[: -len("index.html")] if rel.endswith("index.html") else "/" + rel)
            if own in redirects:
                continue  # never served
            text = read(rel)
            for raw in set(ANCHOR_RE.findall(text)) | set(SCHEMA_ITEM_RE.findall(text)):
                if raw.startswith(("mailto:", "tel:", "#", "http://", "https://")) and not raw.startswith(BASE):
                    continue
                if raw.startswith(BASE):
                    key = norm(raw)
                elif raw.startswith("/"):
                    key = norm(raw)
                else:
                    # Relative href, resolved against the containing directory.
                    # The nearby-city nav grids use these, so a check that only
                    # understands absolute paths reports a false all-clear.
                    base_dir = os.path.dirname(rel)
                    key = norm("/" + os.path.normpath(os.path.join(base_dir, raw.split("#")[0])))
                if key not in stale or key == own:
                    continue
                if key in consolidated:
                    if own.startswith(key + "/"):
                        continue  # breadcrumb link to its own parent
                    hits.append(f"{rel} -> {raw} (want {stale[key]})")
                else:
                    debt.add(f"{rel} -> {raw}")
    rep.add("FAIL", "no internal link points at a URL this registry consolidates",
            not hits, f"{len(hits)}: " + "; ".join(sorted(hits)[:4]))
    # Links into the ~40 city 301 sources are pre-existing debt owned by the open
    # internal-link-architecture PR, which rewrites links across ~1,486 pages and
    # detects this itself. Baselined here so it cannot grow, not fixed here.
    # Counted from served pages only: the nearby-city nav grids live mostly on the
    # commercial-glazing-*.html files, which are themselves 301 sources and inert.
    rep.add("WARN", "links into edge 301 sources <= baseline 197", len(debt) <= 197,
            f"{len(debt)} ref(s) from served pages, owned by the internal-link-architecture PR")

    asset_hits: list[str] = []
    for name in NON_HTML_ASSETS:
        if not os.path.isfile(os.path.join(ROOT, name)):
            continue
        text = read(name)
        for url, dest in stale.items():
            # The optional slash lets /nashville match /nashville/ while the
            # boundary guard keeps /tennessee off /tennessee-commercial-glazing/.
            absolute = re.compile(re.escape(BASE + url) + r"/?(?![\w\-])")
            quoted = f'"{url}"' in text or f'"{url}/"' in text
            if absolute.search(text) or quoted:
                asset_hits.append(f"{name} references {url} instead of {dest}")
    rep.add("FAIL", "non-HTML assets reference primaries, not redirect sources",
            not asset_hits, "; ".join(sorted(asset_hits)[:4]))


def check_manifest(rep: Report, reg: dict, redirects: dict[str, str]) -> None:
    required = {
        norm(r["source"]): r
        for i in reg["intents"]
        for r in i.get("requires_external_redirect", [])
    }
    if not os.path.isfile(MANIFEST):
        rep.add("FAIL", "Cloudflare manifest exists", not required,
                f"{len(required)} required redirect(s) with no manifest")
        return

    man = json.loads(read(os.path.relpath(MANIFEST, ROOT)))
    rep.add("FAIL", "Cloudflare manifest is not activated", man.get("activated") is False,
            f"activated={man.get('activated')!r}")

    listed = {norm(r["source"]): r for r in man.get("rules", [])}
    rep.add("FAIL", "manifest covers exactly the registry's required redirects",
            set(listed) == set(required),
            f"registry-only={sorted(set(required) - set(listed))[:3]} "
            f"manifest-only={sorted(set(listed) - set(required))[:3]}")

    drift = []
    for src, rule in listed.items():
        if src in redirects and norm(redirects[src]) != norm(rule["current_destination"]):
            drift.append(f"{src}: mirror={redirects[src]} manifest={rule['current_destination']}")
        if src not in redirects:
            drift.append(f"{src}: absent from the vercel.json mirror")
    rep.add("FAIL", "manifest current_destination matches the vercel.json mirror", not drift,
            "; ".join(drift[:3]))

    unbuilt = [r["source"] for r in man.get("rules", []) if not file_for(r["required_destination"])]
    rep.add("FAIL", "every manifest destination exists on disk", not unbuilt, ", ".join(unbuilt[:3]))


def check_seo_targets(rep: Report, reg: dict) -> None:
    if not os.path.isfile(TARGETS):
        rep.add("WARN", "seo-targets.json present for reconciliation", True, "absent")
        return
    targets = json.loads(read(os.path.relpath(TARGETS, ROOT)))
    target_markets = {m["id"] for m in targets.get("markets", [])}
    reg_markets = {i["market"] for i in reg["intents"]}
    unknown = sorted(reg_markets - target_markets)
    rep.add("FAIL", "every registry market exists in seo-targets.json", not unknown,
            ", ".join(unknown))

    # Two pages sharing one role in one market is the cannibalization pattern.
    roles: dict[tuple[str, str], list[str]] = {}
    for p in targets.get("pages", []):
        if "market" in p:
            roles.setdefault((p["market"], p["role"]), []).append(p["path"])
        else:
            roles.setdefault(("-", p["role"]), []).append(p["path"])
    collisions = [
        f"{m}/{role}: {', '.join(paths)}"
        for (m, role), paths in sorted(roles.items())
        if len(paths) > 1 and role in {"statewide-hub", "regional-hub"}
    ]
    rep.add("WARN", "seo-targets.json hub roles are unambiguous", not collisions,
            "; ".join(collisions[:3]))

    for entry in reg.get("seo_targets_reconciliation", []):
        if entry["severity"] == "warn":
            rep.add("WARN", "reconciliation noted", False, entry["finding"][:150])


# ---------------------------------------------------------------------------
# live mode
# ---------------------------------------------------------------------------


def check_live(rep: Report, redirects: dict[str, str]) -> None:
    """Assert the deployed Cloudflare edge agrees with the vercel.json mirror.

    This is the only check in this file that observes deployed behaviour. If it
    fails, the mirror is stale and every static conclusion drawn from it about
    which files are never served is suspect.
    """
    import urllib.error
    import urllib.request

    class NoFollow(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *_args, **_kwargs):
            return None

    opener = urllib.request.build_opener(NoFollow)
    drift, unreachable = [], []
    for src, dest in sorted(redirects.items()):
        url = BASE + (src if src != "/" else "/")
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "acglass-canonical-verify/1"})
        try:
            opener.open(req, timeout=20)
            drift.append(f"{src}: expected 301, got 200")
        except urllib.error.HTTPError as exc:
            if exc.code not in (301, 308):
                drift.append(f"{src}: expected 301, got {exc.code}")
                continue
            loc = norm(exc.headers.get("Location", ""))
            if loc != norm(dest):
                drift.append(f"{src}: edge -> {exc.headers.get('Location')}, mirror -> {dest}")
        except Exception as exc:  # network, DNS, TLS
            unreachable.append(f"{src}: {type(exc).__name__}")

    rep.add("FAIL", f"deployed edge matches the vercel.json mirror ({len(redirects)} rules)",
            not drift, f"{len(drift)}: " + "; ".join(drift[:4]))
    rep.add("WARN", "every mirror rule was reachable", not unreachable,
            f"{len(unreachable)}: " + "; ".join(unreachable[:3]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", action="store_true",
                    help="also HEAD-probe acglass.com and assert the edge matches vercel.json")
    ap.add_argument("--base-ref", default=os.environ.get("CANONICAL_BASE_REF", "main"),
                    help="git ref the frozen-path guard diffs against (default: main)")
    args = ap.parse_args()

    reg = json.loads(read(os.path.relpath(REGISTRY, ROOT)))
    redirects = redirect_sources()

    sitemap_locs: dict[str, set[str]] = {}
    for name in sorted(os.listdir(ROOT)):
        if name.startswith("sitemap") and name.endswith(".xml") and "index" not in name:
            sitemap_locs[name] = set(LOC_RE.findall(read(name)))

    print("canonical-verify — INTENT ONLY unless --live is passed.")
    print("  Redirects are deployed at the Cloudflare edge, outside this repo.")
    print("  vercel.json is an observed mirror of that edge, not a deploy target.")
    raw_rules = len(json.loads(read("vercel.json")).get("redirects", [])) if os.path.isfile(VERCEL) else 0
    print(f"  registry: {len(reg['intents'])} intents  "
          f"mirror: {raw_rules} rules ({len(redirects)} distinct sources)  "
          f"sitemaps: {len(sitemap_locs)}\n")

    rep = Report()
    check_registry(rep, reg)
    check_primaries_self_canonical(rep, reg)
    check_consolidations(rep, reg, sitemap_locs)
    check_frozen(rep, reg, args.base_ref)
    check_no_canonical_into_redirect(rep, redirects, sitemap_locs)
    check_internal_references(rep, reg, redirects)
    check_cross_canonical_links(rep, reg, redirects)
    check_manifest(rep, reg, redirects)
    check_seo_targets(rep, reg)
    if args.live:
        check_live(rep, redirects)

    return rep.emit()


if __name__ == "__main__":
    sys.exit(main())
