#!/usr/bin/env python3
"""Segment master sitemap.xml into content-type sitemaps.
Preserves <lastmod>/<changefreq>/<priority>. Image entries are stripped from the
split sitemaps (a dedicated sitemap-images.xml is built separately) to keep them clean,
EXCEPT we keep them out to avoid double-counting — split files contain URL metadata only.
"""
import re, os, json, xml.etree.ElementTree as ET
from collections import OrderedDict

REPO = "/home/user/workspace/acglass-website"
SM = os.path.join(REPO, "sitemap.xml")
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
IMG_NS = "http://www.google.com/schemas/sitemap-image/1.1"
ET.register_namespace("", SM_NS)
ET.register_namespace("image", IMG_NS)
ns = {"sm": SM_NS, "image": IMG_NS}

tree = ET.parse(SM)
root = tree.getroot()
url_elems = root.findall("sm:url", ns)

def path_of(loc):
    return loc.replace("https://acglass.com", "").replace("https://www.acglass.com", "")

# ---- Project page slugs (from case-study-* set + bare equivalents) ----
PROJECT_BASE = {
    "1172-s-harbor","2143-carib-circle","736-lagoon-dr","aspen-dental-edgewater",
    "atlantic-fields-golf-house","atlantic-fields-performance-center",
    "atlantic-fields-sales-center","atlantic-fields","baron-shoppes-tradition",
    "bobcat-treasure-coast","bradley-daytona","causeway-building-bonita-springs",
    "cudjoe-key","gulf-harbour","gulfside-twelve","haines-city-eoc",
    "city-of-haines-emergency","illumia-fort-myers","martin-county-fire-training",
    "panther-national","panther-national-clubhouse","rome-collective",
    "siena-lakes-naples","tomoka-town-center","tradewinds-clubhouse",
    "westlake-hialeah-retrofit","wild-blue-clubhouse","eau-palm-beach-resort",
}

# ---- Florida + TN city / county / neighborhood slugs (bare dir city pages) ----
CITY_SLUGS = {
    "aventura","bal-harbour-village","bay-harbor-islands","boca-raton","bonita-springs",
    "boynton-beach","bradenton","brentwood-tn","brevard-county","broward-county",
    "cape-coral","chattanooga","clearwater","coconut-grove","collier-county",
    "cool-springs-tn","coral-gables","cutler-bay","dania-beach","davie","daytona-beach",
    "deerfield-beach","delray-beach","duval-county","englewood","escambia-county","estero",
    "florida-counties","florida-keys","fort-lauderdale","fort-myers-beach","fort-myers",
    "fort-pierce","franklin-tn","gainesville","golden-beach","gulfstream","hallandale-beach",
    "hendersonville-tn","highland-beach","hillsboro-beach","hillsborough-county","hobe-sound",
    "hollywood-florida","indian-river-county","islamorada","jacksonville","jensen-beach",
    "juno-beach","jupiter","key-biscayne-village","key-largo","key-west","kissimmee",
    "kissimmee-tourism","knoxville","lakeland","lantana","lauderdale-by-the-sea","lee-county",
    "leon-county","lighthouse-point","manalapan","manatee-county","marathon","marco-island",
    "marion-county","martin-county","memphis","miami-beach","miami-dade-county",
    "miami-shores-village","miami","monroe-county","murfreesboro-tn","naples","nashville",
    "north-bay-village","north-miami-beach","north-palm-beach","oakland-park","ocala",
    "orange-county","orlando","osceola-county","palm-bay","palm-beach-county",
    "palm-beach-gardens","palm-beach","palm-city","palm-harbor","palmetto-bay-village",
    "parkland","pasco-county","pensacola","pinecrest","pinellas-county","plant-city",
    "polk-county","pompano-beach","ponte-vedra-beach","port-orange","port-saint-lucie",
    "riviera-beach","sanford","sanibel","sarasota-county","sarasota","sebastian",
    "seminole-county","south-miami","st-augustine","st-lucie-county","st-petersburg",
    "stuart","sunny-isles-beach","surfside","tallahassee","tampa","temple-terrace",
    "tennessee","tequesta","venice","vero-beach","virginia-gardens","volusia-county",
    "west-palm-beach","weston","winter-heaven","winter-park","wynwood","alachua-county",
}

# City-targeted service slug PREFIXES (these are local landing pages -> cities bucket)
CITY_SERVICE_PREFIXES = (
    "storefront-glazier-", "commercial-glazier-", "medical-office-glazier-",
    "office-building-glazier-", "school-glazier-", "restaurant-glazier-",
    "hotel-glazing-contractor-", "healthcare-glazing-", "multifamily-glazing-",
    "gym-fitness-glazing-", "religious-glazing-", "university-college-glazing-",
    "assisted-living-glazing-", "automotive-showroom-glazing-", "bar-brewery-glazing-",
    "government-municipal-glazing-", "marina-glazing-", "showroom-glazing-",
    "country-club-glazing-", "retail-storefront-installer-",
    "emergency-commercial-glass-repair-", "hurricane-glass-replacement-",
    "eswindows-impact-window-installer-", "euro-wall-folding-door-installer-",
    "commercial-glazing-",  # commercial-glazing-<city>.html legacy
)

# Generic statewide / national service landing pages -> services bucket
SERVICE_KEYWORDS = (
    "curtainwall","curtain-wall","storefront-systems","impact-windows","impact-glass",
    "folding-glass-walls","glass-railing","balcony-glass-railing","multi-slide-doors",
    "multi-slide-bifold","all-glass-entrance","automatic-entrance","automatic-door-operators",
    "fire-rated","decorative-glass","skylight","office-glass-partitions","smart-glass",
    "blast-resistant","commercial-glass-replacement","storefront-renovation",
    "storefront-replacement","window-wall","spider-glass","structural-silicone",
    "commercial-storefront-systems","division-08","glass-types","low-e-glass","low-iron-glass",
    "tempered","laminated-glass","spandrel","igu-construction","thermal-break",
)

# Top-level marketing / core pages (exact path match, dir or html)
CORE_PAGES = {
    "/","/about.html","/about-acg-for-ai.html","/capabilities.html","/locations.html",
    "/leadership.html","/manufacturers.html","/qualifications.html","/reviews.html",
    "/reviews/","/careers.html","/contact.html","/portfolio.html","/case-studies/",
    "/industries.html","/industries/","/services.html","/services/","/resources/",
    "/glossary/","/news/","/press/","/blog.html","/blog/","/tools/","/ask.html",
    "/ai-overview.html","/ai-operations-whitepaper.html","/ai-managed-glazing-contractor.html",
    "/architect-resources.html","/architect-resources/","/architect-specs/",
    "/service-areas-map/","/project-map.html","/approvals/","/for-general-contractors/",
    "/privacy-policy.html","/terms-of-use.html","/acg.html","/acg-glass.html",
    "/author-connor-walsh.html","/author-rielly-walsh.html","/author/connor-walsh/",
    "/author/rielly-walsh/","/florida-counties/","/manufacturers/",
}

def classify(loc):
    p = path_of(loc)
    segs = [s for s in p.strip("/").split("/") if s]
    first = segs[0] if segs else ""
    base = first[:-5] if first.endswith(".html") else first  # strip .html

    # 1. Blog
    if p.startswith("/blog/") or p.startswith("/blog-2026/") or p.startswith("/news/") and len(segs) > 1:
        return "blog"

    # 2. Projects: case-study-*, /projects/*, known project slugs
    if base.startswith("case-study-") or p.startswith("/projects/"):
        return "projects"
    if base in PROJECT_BASE or base in PROJECT_SLUGS:
        return "projects"

    # 3. Core marketing pages (exact)
    if p in CORE_PAGES:
        return "pages"

    # 4. Cities: bare city/county dir, nested neighborhood under a city, or city-service landing
    if base in CITY_SLUGS:
        return "cities"
    if len(segs) >= 2 and segs[0] in CITY_SLUGS:
        return "cities"
    if any(base.startswith(pre) for pre in CITY_SERVICE_PREFIXES):
        return "cities"

    # 5. Services: statewide/national service landing pages
    if any(k in base for k in SERVICE_KEYWORDS):
        return "services"

    # 6. Default -> pages (educational guides, FAQs, comparisons, misc)
    return "pages"

# Load definitive project slugs derived from images/projects dirs
try:
    PROJECT_SLUGS = set(json.load(open("/tmp/project_slugs.json")))
except Exception:
    PROJECT_SLUGS = set()

buckets = OrderedDict((k, []) for k in ["pages","blog","projects","cities","services"])
all_locs = []
for ue in url_elems:
    loc = ue.find("sm:loc", ns).text.strip()
    all_locs.append(loc)
    cat = classify(loc)
    buckets[cat].append(ue)

print("Total URLs:", len(url_elems))
total = 0
for k, v in buckets.items():
    print(f"  {k:10s}: {len(v)}")
    total += len(v)
print("Sum:", total)
assert total == len(url_elems), "Count mismatch!"

# Duplicate check across buckets
seen = {}
for k, v in buckets.items():
    for ue in v:
        loc = ue.find("sm:loc", ns).text.strip()
        if loc in seen:
            print("DUPLICATE across buckets:", loc, seen[loc], k)
        seen[loc] = k

LASTMOD = "2026-06-06"

def write_bucket(name, elems):
    fn = os.path.join(REPO, f"sitemap-{name}.xml")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for ue in elems:
        loc = ue.find("sm:loc", ns).text.strip()
        lastmod = ue.find("sm:lastmod", ns)
        changefreq = ue.find("sm:changefreq", ns)
        priority = ue.find("sm:priority", ns)
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod.text.strip() if lastmod is not None else LASTMOD}</lastmod>")
        if changefreq is not None:
            lines.append(f"    <changefreq>{changefreq.text.strip()}</changefreq>")
        if priority is not None:
            lines.append(f"    <priority>{priority.text.strip()}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(fn, "w") as f:
        f.write("\n".join(lines) + "\n")
    return fn

written = {}
for k, v in buckets.items():
    fn = write_bucket(k, v)
    written[k] = len(v)
    print("Wrote", fn, len(v))

# Save report
with open("/tmp/segment_report.txt", "w") as f:
    f.write(f"Total: {len(url_elems)}\n")
    for k, v in buckets.items():
        f.write(f"{k}: {len(v)}\n")
print("DONE")
