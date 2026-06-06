#!/usr/bin/env python3
import re, os, xml.etree.ElementTree as ET
from collections import Counter

REPO = "/home/user/workspace/acglass-website"
SM = os.path.join(REPO, "sitemap.xml")

ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "image": "http://www.google.com/schemas/sitemap-image/1.1"}
tree = ET.parse(SM)
root = tree.getroot()

urls = root.findall("sm:url", ns)
print("Total <url> entries:", len(urls))

locs = []
for u in urls:
    loc = u.find("sm:loc", ns).text.strip()
    locs.append(loc)

# dedupe check
dup = [k for k,v in Counter(locs).items() if v>1]
print("Duplicate locs in master:", len(dup))
for d in dup[:20]:
    print("  DUP:", d)

# Categorize by path
def path_of(loc):
    return loc.replace("https://acglass.com", "").replace("https://www.acglass.com","")

cats = Counter()
samples = {}
for loc in locs:
    p = path_of(loc)
    seg = p.strip("/").split("/")[0] if p.strip("/") else "(root)"
    if p.startswith("/blog/"):
        c = "blog"
    elif p.startswith("/case-study-") or p.startswith("/projects/") or "/projects/" in p:
        c = "projects"
    else:
        c = "other"
    cats[c]+=1
print("\nRough cats:", dict(cats))

# Show distribution of top path patterns
firstseg = Counter()
for loc in locs:
    p = path_of(loc).strip("/")
    fs = p.split("/")[0] if p else "(root)"
    firstseg[fs]+=1

# Print unique top-level .html files vs directories
print("\nSample of all paths (first 60):")
for loc in sorted(locs)[:60]:
    print("  ", path_of(loc))
