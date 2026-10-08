#!/usr/bin/env python3
"""D2: no numeric safety statistic about ACG may publish.

The shell regex this replaces ended both branches in [0-9]\\.[0-9], so it
required a decimal point. "0 OSHA recordable incidents" was live in the body
copy AND inside the FAQPage schema of about.html and facts.html, both
index,follow and both listed in sitemap-llm.xml, and the check reported
"no numeric safety statistic published" the entire time.

Widening the regex to accept integers then produced four false positives,
because "OSHA 30", "OSHA 300 log" and generic EMR advice all put a digit next
to a watched term. A statistic is not a course name, a form number, or a
sentence teaching a GC what industry-average EMR means. That distinction needs
a scanner, not a longer regex.

A hit requires all three:
  1. a watched safety term,
  2. a number within 60 characters of it, in either direction,
  3. ACG as the subject of the sentence.
And it must not be one of the excluded forms below.
"""
import os, re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
TERMS = ["EMR", "TRIR", "DART", "recordable", "recordables", "experience modification"]
SUBJECT = re.compile(r"\b(ACG|American Commercial Glass|we|our|us|the company)\b", re.I)

# Course names, log/form names, and document names. A digit beside these is an
# identifier, not a measurement.
NOT_A_STAT = re.compile(
    r"OSHA\s*(10|30|300A?|500|510)\b"
    r"|OSHA\s*300A?\s*log"
    r"|\b(EMR|TRIR|DART)\s+(letter|documentation|history|logs?|report|packet)\b",
    re.I)
# Teaching a GC how to read someone else's number is education, not a claim
# about ACG. D2 does not touch it.
GENERIC = re.compile(
    r"industry average|is a flag|is disqualifying|means below|below-average"
    r"|typically includes|request the|ask (for|the)|provided in|available (up)?on"
    r"|provides .{0,30}documentation|what'?s your", re.I)

def sentences(text):
    for s in re.split(r"(?<=[.!?])\s+|\n", text):
        s = s.strip()
        if s:
            yield s

def scan(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    # strip tags but keep JSON-LD, where the claim also lives
    txt = re.sub(r"<(script(?! type=\"application/ld)|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = txt.replace("&#x27;", "'").replace("&quot;", '"').replace("&amp;", "&")
    hits = []
    for s in sentences(txt):
        for term in TERMS:
            for m in re.finditer(r"\b" + re.escape(term) + r"\b", s, re.I):
                w = s[max(0, m.start() - 60): m.end() + 60]
                if not re.search(r"\d", w):
                    continue
                if NOT_A_STAT.search(w) or GENERIC.search(s):
                    continue
                if not SUBJECT.search(s):
                    continue
                hits.append((term, re.sub(r"\s+", " ", s)[:180]))
                break
    return hits

files = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", "HEAD"],
                       capture_output=True, text=True).stdout.split()
pages = [f for f in files if f.endswith(".html") and not f.startswith(".github/")]
total = 0
for p in pages:
    fp = os.path.join(ROOT, p)
    if not os.path.isfile(fp):
        continue
    for term, s in scan(fp):
        print(f"  {p}: [{term}] {s}")
        total += 1
print(f"COUNT={total}")
