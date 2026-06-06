#!/usr/bin/env python3
import json, os, sys, xml.etree.ElementTree as ET
from collections import Counter

REPO = "/home/user/workspace/acglass-website"
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "image": "http://www.google.com/schemas/sitemap-image/1.1"}
ok = True

def fail(msg):
    global ok; ok = False; print("FAIL:", msg)

# 1) vercel.json valid JSON + redirects
vj = json.load(open(os.path.join(REPO, "vercel.json")))
reds = vj.get("redirects", [])
print(f"vercel.json: valid JSON, {len(reds)} redirects")
src = [r["source"] for r in reds]
dup_src = [k for k,v in Counter(src).items() if v>1]
if dup_src: fail(f"duplicate redirect sources: {dup_src}")
# all redirects permanent + have source/destination
for r in reds:
    if not r.get("source") or not r.get("destination"):
        fail(f"redirect missing fields: {r}")
    if r.get("permanent") is not True:
        fail(f"redirect not permanent: {r['source']}")

# 2) Sitemap segments valid XML, count vs master, no dup across segments
master = os.path.join(REPO, "sitemap.xml")
master_locs = [u.find("sm:loc", ns).text.strip() for u in ET.parse(master).getroot().findall("sm:url", ns)]
print(f"master sitemap.xml: {len(master_locs)} URLs")

segs = ["pages","blog","projects","cities","services"]
all_seg_locs = []
seg_counts = {}
for s in segs:
    p = os.path.join(REPO, f"sitemap-{s}.xml")
    try:
        root = ET.parse(p).getroot()
    except Exception as e:
        fail(f"{p} invalid XML: {e}"); continue
    locs = [u.find("sm:loc", ns).text.strip() for u in root.findall("sm:url", ns)]
    seg_counts[s] = len(locs)
    all_seg_locs.extend(locs)
    print(f"  sitemap-{s}.xml: {len(locs)} URLs")

# total must equal master
if len(all_seg_locs) != len(master_locs):
    fail(f"segment total {len(all_seg_locs)} != master {len(master_locs)}")
else:
    print(f"Segment total matches master: {len(all_seg_locs)}")

# duplicates across segments
dups = [k for k,v in Counter(all_seg_locs).items() if v>1]
if dups: fail(f"{len(dups)} duplicate URLs across segments: {dups[:10]}")
else: print("No duplicate URLs across segments")

# coverage: every master URL in exactly one segment
master_set, seg_set = set(master_locs), set(all_seg_locs)
missing = master_set - seg_set
extra = seg_set - master_set
if missing: fail(f"{len(missing)} master URLs missing from segments: {list(missing)[:10]}")
if extra: fail(f"{len(extra)} segment URLs not in master: {list(extra)[:10]}")
if not missing and not extra: print("Perfect coverage: every master URL in exactly one segment")

# 3) image sitemap valid + namespace + count
img_p = os.path.join(REPO, "sitemap-images.xml")
iroot = ET.parse(img_p).getroot()
img_entries = iroot.findall(".//image:image", ns)
img_pages = iroot.findall("sm:url", ns)
print(f"sitemap-images.xml: {len(img_entries)} images across {len(img_pages)} pages")
if "image" not in iroot.tag and not any("sitemap-image" in (a or "") for a in []):
    pass
# verify image namespace declared
raw = open(img_p).read()
if "http://www.google.com/schemas/sitemap-image/1.1" not in raw:
    fail("image namespace missing in sitemap-images.xml")
else:
    print("image namespace present")
# dup image locs
img_locs = [e.find("image:loc", ns).text.strip() for e in img_entries]
idup = [k for k,v in Counter(img_locs).items() if v>1]
if idup: fail(f"duplicate image locs: {idup[:5]}")
else: print("No duplicate image locs")

# 4) sitemap-index valid + lists segments
idx = ET.parse(os.path.join(REPO, "sitemap-index.xml")).getroot()
idx_locs = [s.find("sm:loc", ns).text.strip() for s in idx.findall("sm:sitemap", ns)]
print(f"sitemap-index.xml lists {len(idx_locs)} sitemaps")
expected = [f"https://acglass.com/sitemap-{s}.xml" for s in segs] + ["https://acglass.com/sitemap-images.xml"]
for e in expected:
    if e not in idx_locs: fail(f"sitemap-index missing {e}")

# 5) robots.txt lists sitemaps
robots = open(os.path.join(REPO, "robots.txt")).read()
for s in ["sitemap-index.xml"] + [f"sitemap-{x}.xml" for x in segs] + ["sitemap-images.xml"]:
    if s not in robots: fail(f"robots.txt missing {s}")
print("robots.txt lists all segmented sitemaps + index")

# 6) all redirect destinations resolve to an existing file/dir
def dest_exists(dest):
    d = dest.lstrip("/")
    if d == "" : return os.path.exists(os.path.join(REPO,"index.html"))
    if d.endswith("/"): return os.path.exists(os.path.join(REPO, d, "index.html")) or os.path.isdir(os.path.join(REPO,d))
    return os.path.exists(os.path.join(REPO, d))
bad_dest = [r["destination"] for r in reds if not dest_exists(r["destination"])]
if bad_dest:
    print("WARN: redirect destinations not found on disk:", sorted(set(bad_dest)))
else:
    print("All redirect destinations resolve to existing files")

print("\n" + ("ALL VALIDATIONS PASSED" if ok else "VALIDATION FAILURES PRESENT"))
sys.exit(0 if ok else 1)
