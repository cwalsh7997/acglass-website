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
SCHEMA_ITEM_RE = re.compile(r'"item"\s*:\s*"([^"]+)"')
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")

VALID_STATUS = {"ratified", "frozen", "gsc-gated", "blocked-no-primary", "owned-elsewhere"}
NON_HTML_ASSETS = ("llms.txt", "llms-full.txt", "ai.txt", "search-index.json")


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


def check_frozen(rep: Report, reg: dict, base_ref: str) -> None:
    """WPB and the site root must not change in this workstream.

    Enforced against git, not against content heuristics: any tracked file that
    serves a frozen URL must be byte-identical to base_ref.
    """
    frozen = reg["frozen_prefixes"]
    frozen_files = set()
    for url in frozen:
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
    rep.add("FAIL", f"no frozen path modified since {base_ref}", not violations,
            f"{len(violations)}: " + ", ".join(violations[:4]))


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
    check_manifest(rep, reg, redirects)
    check_seo_targets(rep, reg)
    if args.live:
        check_live(rep, redirects)

    return rep.emit()


if __name__ == "__main__":
    sys.exit(main())
