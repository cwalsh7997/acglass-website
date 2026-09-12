#!/usr/bin/env python3
"""Structured data must be well-formed and must describe things that exist.

Three rules:
  1  every JSON-LD block parses
  2  no collection entry (hasPart / itemListElement) is missing its url
  3  every internal url named in JSON-LD resolves to a file on disk

Rule 2 exists because case-studies/index.html carried an entry that was just
{"@type":"CreativeWork","name":"Fort Lauderdale"} with no url and no description.
A truncated Ocean Prime entry. It parsed as valid JSON, so a syntax check saw
nothing, and the real case study sat with zero inbound links as a result.

Rule 3 catches structured data that outlives the page it points at, which is the
same failure one step later.
"""
import json
import os
import re
import subprocess
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

BASE = "https://acglass.com/"
# Entry types that name a page and therefore must carry a url.
PAGE_LIKE = {"ListItem", "CreativeWork", "Article", "BlogPosting", "WebPage",
             "NewsArticle", "CollectionPage", "ItemPage"}
bad = []

def visit(node, page):
    if isinstance(node, dict):
        for key in ("hasPart", "itemListElement"):
            entries = node.get(key, []) or []
            # A BreadcrumbList's LAST item is allowed to omit url: it is the page
            # you are already on, and Google's breadcrumb guidance says so
            # explicitly. Flagging those would be 139 phantom failures.
            is_crumb = node.get("@type") == "BreadcrumbList"
            for idx, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    continue
                if is_crumb and idx == len(entries) - 1:
                    continue
                et = entry.get("@type", "")
                et = et if isinstance(et, str) else "+".join(et)
                # Only entry types where a url is meaningful. An Offer inside an
                # OfferCatalog describes a service, not a page, and legitimately
                # has none. Flagging those was 65 more phantom failures.
                if et not in PAGE_LIKE:
                    continue
                tgt = entry.get("url") or entry.get("item")
                if isinstance(tgt, dict):
                    tgt = tgt.get("@id") or tgt.get("url")
                if not tgt:
                    bad.append((page, f"{key} entry '{entry.get('name','?')}' has no url"))
        u = node.get("url")
        if isinstance(u, str) and u.startswith(BASE):
            t = u[len(BASE):].split("#")[0].split("?")[0]
            if t and not any(os.path.isfile(os.path.join(ROOT, c)) for c in
                             (t, t + "index.html", t.rstrip("/") + "/index.html")):
                bad.append((page, f"url points at {t}, which does not exist"))
        for v in node.values():
            visit(v, page)
    elif isinstance(node, list):
        for v in node:
            visit(v, page)

blocks = 0
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for b in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', d, re.S):
        blocks += 1
        try:
            visit(json.loads(b), p)
        except Exception as e:
            bad.append((p, f"JSON-LD does not parse: {str(e)[:60]}"))

for p, m in bad[:20]:
    print(f"  {p}: {m}")
if not bad:
    print(f"PASS    schema-integrity ({blocks} JSON-LD blocks, all well-formed and resolvable)")
    sys.exit(0)
print(f"FAIL    schema-integrity: {len(bad)} problem(s) across {blocks} blocks")
sys.exit(1)
