#!/usr/bin/env python3
"""Build sitemap-images.xml pairing project/team images with canonical parent pages."""
import os, re, json, xml.etree.ElementTree as ET

REPO = "/home/user/workspace/acglass-website"
IMG = os.path.join(REPO, "images")
BASE = "https://acglass.com"
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# All valid URLs currently in master sitemap (for parent-page validation)
sm_locs = {u.find("sm:loc", ns).text.strip() for u in
           ET.parse(os.path.join(REPO,"sitemap.xml")).getroot().findall("sm:url", ns)}
def page_exists_path(rel):  # rel like 'portfolio.html'
    return os.path.exists(os.path.join(REPO, rel))

# ---- Map each images/projects/<dir> to its canonical project page ----
# Prefer a bare slug page that exists, else the case-study-<slug> page, else portfolio.
def project_page_for(slug):
    candidates = [
        f"{slug}.html",
        f"case-study-{slug}.html",
    ]
    # known slug remaps (image dir name -> page slug)
    remap = {
        "atlantic-fields-performance": "atlantic-fields-performance-center",
        "carib-circle": "2143-carib-circle",
        "causeway-building": "causeway-building-bonita-springs",
        "eau-palm-beach": "eau-palm-beach-resort",
        "illumina-fort-myers": "illumia-fort-myers",  # note spelling in case-study
        "westlake-hialeah": "westlake-hialeah-retrofit",
        "wild-blue": "wild-blue-clubhouse",
        "harbour-cay": "harbour-cay-fort-pierce",
        "hardy-world": "hardy-world-melbourne",
        "hca-cape-coral": "hca-cape-coral-emergency",
        "hulett-environmental": "hulett-environmental-port-st-lucie",
        "imperial-crossings": "imperial-crossings-bonita-springs",
        "klus-lighting": "klus-lighting-vero-beach",
        "lake-park-innovation": "lake-park-innovation-center",
        "prestige-marble": "prestige-marble-bonita-springs",
        "project-lift": "project-lift-hobe-sound",
        "turbine-technologies": "turbine-technologies-jupiter",
        "villa-lonz": "villa-lonz-riviera-beach",
        "wave-food-hall": "wave-food-hall-cocoa-beach",
        "wave-haven": "wave-haven-cocoa-beach",
        "cudjoe-key-fire-station": "cudjoe-key-fire-station",
        "compass-alton": "compass-alton-town-center",
        "dale-mabry-retail": "dale-mabry-retail-tampa",
        "estero-vista": "estero-vista-fort-myers",
        "stayapt-lafayette": "stayapt-suites-lafayette",
    }
    if slug in remap:
        candidates = [f"{remap[slug]}.html", f"case-study-{remap[slug]}.html"] + candidates
    for c in candidates:
        if page_exists_path(c):
            return "/" + c
    # try case-study with remapped
    return "/portfolio.html"

# ---- Human-readable names & captions from slugs ----
PROJECT_NAMES = {
    "1172-s-harbor": "1172 S Harbor Drive luxury residence",
    "736-lagoon-dr": "736 Lagoon Drive waterfront residence",
    "carib-circle": "2143 Carib Circle residence",
    "aspen-dental-edgewater": "Aspen Dental Edgewater",
    "atlantic-fields": "Atlantic Fields",
    "atlantic-fields-golf-house": "Atlantic Fields Golf House",
    "atlantic-fields-performance": "Atlantic Fields Performance Center",
    "atlantic-fields-sales-center": "Atlantic Fields Sales Center",
    "bobcat-treasure-coast": "Bobcat of the Treasure Coast",
    "causeway-building": "Causeway Building, Bonita Springs",
    "compass-alton": "Compass at Alton Town Center",
    "stayapt-lafayette": "StayAPT Suites, Lafayette",
    "cressey-sports-center": "Cressey Sports Performance Center",
    "cubesmart-davie": "CubeSmart Self-Storage, Davie",
    "cudjoe-key-fire-station": "Cudjoe Key Fire Station",
    "dale-mabry-retail": "Dale Mabry Retail Center, Tampa",
    "eau-palm-beach": "Eau Palm Beach Resort",
    "el-car-wash-northlake": "El Car Wash, Northlake",
    "estero-vista": "Estero Vista, Fort Myers",
    "ginsberg-eye-center": "Ginsberg Eye Center",
    "gulfside-twelve": "Gulfside Twelve",
    "haines-city-eoc": "Haines City Public Safety Complex & EOC",
    "harbour-cay": "Harbour Cay, Fort Pierce",
    "hardy-world": "Hardy World, Melbourne",
    "hca-cape-coral": "HCA Cape Coral Emergency",
    "hulett-environmental": "Hulett Environmental, Port St. Lucie",
    "illumina-fort-myers": "Illumia, Fort Myers",
    "imperial-crossings": "Imperial Crossings, Bonita Springs",
    "indiantown-high-school": "Indiantown High School",
    "klus-lighting": "Klus Lighting, Vero Beach",
    "lake-park-innovation": "Lake Park Innovation Center",
    "medley-business-park": "Medley Business Park",
    "ocean-prime-ft-lauderdale": "Ocean Prime, Fort Lauderdale",
    "panther-national": "Panther National Clubhouse",
    "pointe-palm-bay": "Pointe Palm Bay",
    "prestige-marble": "Prestige Marble, Bonita Springs",
    "project-lift": "Project LIFT, Hobe Sound",
    "savannas-ridge-clubhouse": "Savannas Ridge Clubhouse",
    "sroa-vero-beach": "SROA Self-Storage, Vero Beach",
    "stayapt-lafayette": "StayAPT Suites, Lafayette",
    "storage-king-winter-haven": "Storage King, Winter Haven",
    "tradewinds-clubhouse": "Tradewinds Clubhouse",
    "tradewinds-hobe-sound": "Tradewinds, Hobe Sound",
    "turbine-technologies": "Turbine Technologies, Jupiter",
    "villa-lonz": "Villa Lonz, Riviera Beach",
    "wave-food-hall": "Wave Food Hall, Cocoa Beach",
    "wave-haven": "Wave Haven, Cocoa Beach",
    "westlake-hialeah": "Westlake Hialeah Retrofit",
    "wild-blue": "WildBlue Clubhouse",
}

def humanize_feature(fname, project_name):
    stem = re.sub(r"\.(jpg|jpeg|png|webp)$", "", fname, flags=re.I)
    # strip project-slug prefix repeated in filename
    words = stem.replace("_", "-").split("-")
    # remove leading tokens that duplicate the project slug words
    desc = " ".join(w for w in words if w).strip()
    desc = re.sub(r"\b\d{4}-\d{2}\b", "", desc).strip()  # date codes
    desc = desc.replace("  ", " ")
    if not desc:
        desc = "glazing installation"
    return desc

entries = []  # (page_url, image_url, caption, title)
seen_images = set()

# 1) PROJECT PHOTOS
proj_root = os.path.join(IMG, "projects")
for d in sorted(os.listdir(proj_root)):
    dpath = os.path.join(proj_root, d)
    if not os.path.isdir(dpath):
        continue
    pname = PROJECT_NAMES.get(d, d.replace("-", " ").title())
    page = BASE + project_page_for(d)
    jpgs = sorted(f for f in os.listdir(dpath) if f.lower().endswith((".jpg", ".jpeg")))
    for f in jpgs:
        img_url = f"{BASE}/images/projects/{d}/{f}"
        if img_url in seen_images:
            continue
        seen_images.add(img_url)
        feat = humanize_feature(f, pname)
        caption = f"{pname} — {feat} | commercial glazing & storefront installation by American Commercial Glass"
        title = f"{pname} — {feat}"
        entries.append((page, img_url, caption, title))

# 2) TEAM + LEADERSHIP HEADSHOTS -> /leadership.html (fallback /about.html)
team_page = BASE + ("/leadership.html" if page_exists_path("leadership.html") else "/about.html")
for sub in ["team", "leadership"]:
    sp = os.path.join(IMG, sub)
    if not os.path.isdir(sp):
        continue
    for f in sorted(os.listdir(sp)):
        if not f.lower().endswith((".jpg", ".jpeg")):
            continue
        if "original" in f.lower():
            continue  # skip raw originals
        img_url = f"{BASE}/images/{sub}/{f}"
        if img_url in seen_images:
            continue
        seen_images.add(img_url)
        person = re.sub(r"\.(jpg|jpeg)$", "", f, flags=re.I)
        person = person.replace("-portrait", "").replace("-card", "").replace("-square", "")
        person = person.replace("-", " ").title()
        caption = f"{person} — American Commercial Glass leadership team"
        title = f"{person} | American Commercial Glass"
        entries.append((team_page, img_url, caption, title))

# 3) PROJECT INFOGRAPHICS (signature graphics) -> canonical project page
# Only those tied to a known project slug to keep it high-quality.
info_root = os.path.join(IMG, "infographics")
proj_dirs = {d for d in os.listdir(proj_root) if os.path.isdir(os.path.join(proj_root, d))}
# build name->slug lookup using remap-aware page resolution
for f in sorted(os.listdir(info_root)):
    if not f.lower().endswith(".png"):
        continue
    m = re.match(r"infographic-(.+)-glazing\.png$", f)
    if not m:
        continue
    key = m.group(1)
    # match to a project image dir
    matched = None
    for d in proj_dirs:
        dn = d.replace("-", "")
        if key == d or dn in key.replace("-", ""):
            matched = d
            break
    # also allow direct page-slug matches (e.g. lucie-at-tradition, shoppes-westlake-point)
    if matched:
        page = BASE + project_page_for(matched)
        pname = PROJECT_NAMES.get(matched, matched.replace("-", " ").title())
    else:
        # try page slug directly
        if page_exists_path(f"{key}.html"):
            page = f"{BASE}/{key}.html"
            pname = key.replace("-", " ").title()
        elif page_exists_path(f"case-study-{key}.html"):
            page = f"{BASE}/case-study-{key}.html"
            pname = key.replace("-", " ").title()
        else:
            continue  # skip infographics with no clear parent page
    img_url = f"{BASE}/images/infographics/{f}"
    if img_url in seen_images:
        continue
    seen_images.add(img_url)
    caption = f"{pname} glazing scope infographic by American Commercial Glass"
    title = f"{pname} — glazing project infographic"
    entries.append((page, img_url, caption, title))

# ---- Group images by parent page, write XML ----
from collections import OrderedDict
by_page = OrderedDict()
for page, img, cap, title in entries:
    by_page.setdefault(page, []).append((img, cap, title))

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
lines.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
for page, imgs in by_page.items():
    lines.append("  <url>")
    lines.append(f"    <loc>{esc(page)}</loc>")
    for img, cap, title in imgs:
        lines.append("    <image:image>")
        lines.append(f"      <image:loc>{esc(img)}</image:loc>")
        lines.append(f"      <image:caption>{esc(cap)}</image:caption>")
        lines.append(f"      <image:title>{esc(title)}</image:title>")
        lines.append("    </image:image>")
    lines.append("  </url>")
lines.append("</urlset>")

out = os.path.join(REPO, "sitemap-images.xml")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Total image entries: {len(entries)}")
print(f"Parent pages: {len(by_page)}")
print(f"Wrote {out}")
# Report parent pages that resolved to portfolio (couldn't find dedicated page)
fb = sum(1 for page,_,_,_ in entries if page.endswith("/portfolio.html"))
print(f"Images falling back to /portfolio.html: {fb}")
