#!/usr/bin/env python3
"""D10: image rights vocabulary and publication rule.

Keyed per IMAGE, not per encoding. The same photo shipped as jpg + webp + avif is
one rights decision, not three. The original CSV had 1,428 encoding rows, which
made the gate read as 1,007 unanswerable questions when it is really 380 images
across 59 directories, most of which are one answer for a whole folder.

D10 obligation 4, the publication rule, is enforced here and was not enforced
before:
    acg_shot + owned                      publishes freely
    acg_commissioned                      needs owned or licensed_written
    gc_supplied / architect_or_photographer / manufacturer_supplied
                                          need licensed_written
    unknown or unverified                 does not publish
"""
import csv, os, re, subprocess, sys, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
CSV = os.path.join(ROOT, ".github/agent-state/state/image-rights.csv")
if not os.path.isfile(CSV):
    print("CONFIG  image-rights: csv missing"); sys.exit(3)
rows = list(csv.DictReader(open(CSV)))
if not rows:
    print("CONFIG  image-rights: 0 rows recorded, cannot validate"); sys.exit(3)

CAT = {"acg_shot", "acg_commissioned", "gc_supplied",
       "architect_or_photographer", "manufacturer_supplied", "unknown"}
ST = {"owned", "licensed_written", "permission_verbal", "unverified"}

offvocab = [r for r in rows
            if r["source_category"] not in CAT or r["rights_status"] not in ST]

def may_publish(r):
    c, s = r["source_category"], r["rights_status"]
    if c == "unknown" or s == "unverified":
        return False
    if c == "acg_shot":
        return s == "owned"
    if c == "acg_commissioned":
        return s in ("owned", "licensed_written")
    return s == "licensed_written"

blocked = [r for r in rows if not may_publish(r)]

# which of the blocked images are actually referenced by a served page
refs = set()
for u in subprocess.run(["git", "-C", ROOT, "grep", "-hoI", "-E",
                         r"images/[A-Za-z0-9._/-]+", "--", "*.html"],
                        capture_output=True, text=True).stdout.split():
    refs.add(os.path.splitext(u)[0])
live = [r for r in blocked if r["image_stem"] in refs]

if offvocab:
    for r in offvocab[:8]:
        print(f"  off-vocabulary: {r['image_stem']} "
              f"({r['source_category']} / {r['rights_status']})")
    print(f"FAIL    image-rights: {len(offvocab)} row(s) outside the D10 vocabulary")
    sys.exit(1)

if not blocked:
    print(f"PASS    image-rights ({len(rows)} images, all clear to publish under D10)")
    sys.exit(0)

dirs = collections.Counter(r["project_group"] for r in blocked)
print(f"  {len(blocked)} of {len(rows)} images may not publish under D10 obligation 4")
print(f"  {len(live)} of those are referenced by a served page right now")
print(f"  they span {len(dirs)} directories, and a directory is usually one answer")
for d, n in dirs.most_common(5):
    print(f"     {n:>3}  {d}")
print(f"FAIL    image-rights: {len(blocked)} image(s) blocked, {len(live)} live")
sys.exit(1)
