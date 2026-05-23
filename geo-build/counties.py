#!/usr/bin/env python3
"""Florida county hub pages — captures "[County] commercial glazier" searches.
25 commercial-active Florida counties. Each page has full schema, county-specific
HVHZ/WBDR/wind context, links to all ACG city pages in that county.
"""
import os, json, html as html_lib

OUT = "/home/user/workspace/acglass-website"

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">'''

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links">
<a href="/index.html">Home</a><a href="/portfolio.html">Portfolio</a><a href="/services.html">Services</a>
<a href="/tools/">Tools</a><a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.6;">Florida commercial storefront glazing contractor.<br>CGC #1531993.</p></div>
<div><h4>Counties</h4><ul><li><a href="/florida-counties/">All Counties</a></li><li><a href="/palm-beach-county/">Palm Beach</a></li><li><a href="/miami-dade-county/">Miami-Dade</a></li><li><a href="/broward-county/">Broward</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">All Resources</a></li><li><a href="/tools/">Free Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = [
    "https://www.wikidata.org/wiki/Q139858578",
    "https://acglass.ai/",
    "https://www.linkedin.com/company/acglass",
    "https://network.procore.com/p/american-commercial-glass-west-palm-beach",
    "https://www.bbb.org/us/fl/west-palm-beach/profile/window-installation/american-commercial-glass-inc-0633-92045708"
]

# County data: slug, name, county_seat, lat, lng, hvhz_status, wind_speed, ahj_notes, city_slugs_in_county
COUNTIES = [
    ("palm-beach-county", "Palm Beach County", "West Palm Beach", 26.65, -80.20,
        "HVHZ partial — east of Military Trail. West of Military Trail is WBDR.", "165 mph (east) / 150 mph (west)",
        "Palm Beach County issues permits through Planning, Zoning & Building Department. Municipalities (WPB, Boca, Delray, Jupiter) issue their own permits for projects within municipal boundaries.",
        ["west-palm-beach", "boca-raton", "boynton-beach", "delray-beach", "jupiter", "palm-beach-gardens", "palm-beach", "lake-worth-beach", "wellington", "riviera-beach", "tequesta", "juno-beach", "gulfstream", "highland-beach", "manalapan", "north-palm-beach", "lantana", "palm-city", "atlantis"]),
    ("miami-dade-county", "Miami-Dade County", "Miami", 25.55, -80.45,
        "Full HVHZ. Miami-Dade NOA required for all glazing.", "175 mph (Risk Cat II)",
        "Miami-Dade County Product Control Section reviews all NOA submittals. Individual cities (Miami, Coral Gables, Aventura, etc.) issue construction permits using county-approved products.",
        ["miami", "miami-beach", "coral-gables", "aventura", "doral", "homestead", "hialeah", "key-biscayne-village", "cutler-bay", "palmetto-bay-village", "pinecrest", "south-miami", "sunny-isles-beach", "bal-harbour-village", "bay-harbor-islands", "surfside", "miami-shores-village", "north-miami-beach", "north-bay-village", "golden-beach"]),
    ("broward-county", "Broward County", "Fort Lauderdale", 26.15, -80.30,
        "Full HVHZ. Miami-Dade NOA accepted.", "170 mph (Risk Cat II)",
        "Broward County Building Department + individual municipalities. Most HVHZ NOA submittals reference Miami-Dade NOAs.",
        ["fort-lauderdale", "hollywood-florida", "pembroke-pines", "davie", "weston", "parkland", "deerfield-beach", "dania-beach", "hallandale-beach", "lauderdale-by-the-sea", "lighthouse-point", "oakland-park", "hillsboro-beach"]),
    ("collier-county", "Collier County", "Naples", 26.00, -81.50,
        "Wind-Borne Debris Region. Impact-rated assemblies required.", "160 mph (Risk Cat II)",
        "Collier County Growth Management Department issues most permits. City of Naples and Marco Island have separate building departments.",
        ["naples", "marco-island", "bonita-springs"]),
    ("lee-county", "Lee County", "Fort Myers", 26.55, -81.85,
        "Wind-Borne Debris Region. Heavy Hurricane Ian impact zone (2022).", "160 mph (Risk Cat II)",
        "Lee County DCD + Fort Myers, Cape Coral, Sanibel, Bonita Springs municipal departments.",
        ["cape-coral", "fort-myers", "estero", "sanibel"]),
    ("hillsborough-county", "Hillsborough County", "Tampa", 27.95, -82.45,
        "WBDR east of I-275 / coastal areas; Standard FBC inland.", "145 mph (Risk Cat II)",
        "Hillsborough County DCM + City of Tampa Construction Services Center.",
        ["tampa", "plant-city", "temple-terrace"]),
    ("pinellas-county", "Pinellas County", "Clearwater", 27.85, -82.75,
        "Full WBDR — peninsula geography means all coastal exposure.", "150 mph (Risk Cat II)",
        "Pinellas County BD + St Petersburg, Clearwater, Largo municipal departments.",
        ["st-petersburg", "clearwater", "palm-harbor"]),
    ("orange-county", "Orange County", "Orlando", 28.55, -81.30,
        "Standard FBC. Inland — no WBDR exposure.", "140 mph (Risk Cat II)",
        "Orange County BD + City of Orlando Permitting.",
        ["orlando", "winter-heaven"]),
    ("monroe-county", "Monroe County", "Key West", 24.85, -80.85,
        "Wind-Borne Debris Region (severe). Florida Keys.", "180 mph (Risk Cat II)",
        "Monroe County BD. Highest design wind in continental US for this Risk Category.",
        ["key-west", "marathon", "key-largo"]),
    ("brevard-county", "Brevard County", "Titusville", 28.30, -80.70,
        "WBDR — Space Coast / Atlantic exposure.", "150 mph (Risk Cat II)",
        "Brevard County Permitting + Melbourne, Palm Bay, Cocoa, Cape Canaveral municipal departments.",
        ["palm-bay"]),
    ("indian-river-county", "Indian River County", "Vero Beach", 27.65, -80.45,
        "WBDR — Treasure Coast.", "155 mph (Risk Cat II)",
        "Indian River County Community Development + City of Vero Beach.",
        ["vero-beach", "sebastian"]),
    ("st-lucie-county", "St. Lucie County", "Fort Pierce", 27.40, -80.40,
        "WBDR — Treasure Coast.", "160 mph (Risk Cat II)",
        "St. Lucie County DCM + Port St Lucie, Fort Pierce municipal departments.",
        ["port-saint-lucie"]),
    ("martin-county", "Martin County", "Stuart", 27.10, -80.30,
        "WBDR — Treasure Coast.", "160 mph (Risk Cat II)",
        "Martin County Growth Management + Stuart, Jupiter Island, Sewall's Point municipal departments.",
        ["stuart"]),
    ("sarasota-county", "Sarasota County", "Sarasota", 27.10, -82.35,
        "WBDR — Gulf coast exposure.", "155 mph (Risk Cat II)",
        "Sarasota County DCM + City of Sarasota, Venice, North Port.",
        ["sarasota", "venice"]),
    ("manatee-county", "Manatee County", "Bradenton", 27.45, -82.40,
        "WBDR — Gulf coast.", "150 mph (Risk Cat II)",
        "Manatee County BD + Bradenton, Anna Maria, Holmes Beach, Bradenton Beach municipal departments.",
        ["bradenton"]),
    ("duval-county", "Duval County", "Jacksonville", 30.30, -81.65,
        "WBDR coastal areas; Standard FBC inland.", "140 mph (Risk Cat II)",
        "Duval County / City of Jacksonville Building Inspection Division (consolidated city-county).",
        []),
    ("polk-county", "Polk County", "Bartow", 27.95, -81.70,
        "Standard FBC. Inland.", "140 mph (Risk Cat II)",
        "Polk County BD + Lakeland, Winter Haven, Bartow municipal departments.",
        ["lakeland"]),
    ("seminole-county", "Seminole County", "Sanford", 28.75, -81.30,
        "Standard FBC. Inland.", "140 mph (Risk Cat II)",
        "Seminole County BD + Sanford, Lake Mary, Altamonte Springs municipal departments.",
        []),
    ("volusia-county", "Volusia County", "DeLand", 29.05, -81.20,
        "WBDR coastal; Standard FBC inland.", "145 mph (Risk Cat II)",
        "Volusia County Growth Management + Daytona Beach, Port Orange, DeLand municipal departments.",
        []),
    ("osceola-county", "Osceola County", "Kissimmee", 28.30, -81.40,
        "Standard FBC. Inland.", "140 mph (Risk Cat II)",
        "Osceola County BD + Kissimmee, St. Cloud municipal departments.",
        ["kissimmee"]),
    ("pasco-county", "Pasco County", "Dade City", 28.30, -82.40,
        "WBDR coastal; Standard FBC inland.", "145 mph (Risk Cat II)",
        "Pasco County BCD + Dade City, New Port Richey, Zephyrhills municipal departments.",
        []),
    ("alachua-county", "Alachua County", "Gainesville", 29.65, -82.35,
        "Standard FBC. Inland.", "130 mph (Risk Cat II)",
        "Alachua County BD + City of Gainesville Building Inspection.",
        []),
    ("leon-county", "Leon County", "Tallahassee", 30.45, -84.25,
        "Standard FBC. Inland — but North Florida hurricane exposure (Michael 2018).", "130 mph (Risk Cat II)",
        "Leon County Growth Management + City of Tallahassee Growth Management.",
        []),
    ("escambia-county", "Escambia County", "Pensacola", 30.55, -87.30,
        "WBDR — Panhandle Gulf coast. Hurricane Sally (2020), Ivan (2004) impact zone.", "150 mph (Risk Cat II)",
        "Escambia County BD + City of Pensacola.",
        []),
    ("marion-county", "Marion County", "Ocala", 29.10, -82.05,
        "Standard FBC. Inland.", "135 mph (Risk Cat II)",
        "Marion County BD + City of Ocala.",
        [])
]

def county_schema(canonical, name, county_seat, lat, lng):
    return [
        {
            "@context": "https://schema.org",
            "@type": ["Organization", "LocalBusiness"],
            "@id": canonical + "#org",
            "name": "American Commercial Glass",
            "url": "https://acglass.com",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "telephone": "+17724867711",
            "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"},
            "sameAs": ORG_SAMEAS,
            "areaServed": {"@type": "AdministrativeArea", "name": name, "containedInPlace": {"@type": "State", "name": "Florida"}, "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier — {name}",
            "serviceType": "Commercial Glazing",
            "areaServed": {"@type": "AdministrativeArea", "name": name},
            "provider": {"@id": canonical + "#org"}
        }
    ]

CITY_DISPLAY = {
    "west-palm-beach": "West Palm Beach", "boca-raton": "Boca Raton", "boynton-beach": "Boynton Beach",
    "delray-beach": "Delray Beach", "jupiter": "Jupiter", "palm-beach-gardens": "Palm Beach Gardens",
    "palm-beach": "Palm Beach", "lake-worth-beach": "Lake Worth Beach", "wellington": "Wellington",
    "riviera-beach": "Riviera Beach", "tequesta": "Tequesta", "juno-beach": "Juno Beach",
    "gulfstream": "Gulf Stream", "highland-beach": "Highland Beach", "manalapan": "Manalapan",
    "north-palm-beach": "North Palm Beach", "lantana": "Lantana", "palm-city": "Palm City",
    "atlantis": "Atlantis", "miami": "Miami", "miami-beach": "Miami Beach", "coral-gables": "Coral Gables",
    "aventura": "Aventura", "doral": "Doral", "homestead": "Homestead", "hialeah": "Hialeah",
    "key-biscayne-village": "Key Biscayne", "cutler-bay": "Cutler Bay", "palmetto-bay-village": "Palmetto Bay",
    "pinecrest": "Pinecrest", "south-miami": "South Miami", "sunny-isles-beach": "Sunny Isles Beach",
    "bal-harbour-village": "Bal Harbour", "bay-harbor-islands": "Bay Harbor Islands", "surfside": "Surfside",
    "miami-shores-village": "Miami Shores", "north-miami-beach": "North Miami Beach",
    "north-bay-village": "North Bay Village", "golden-beach": "Golden Beach",
    "fort-lauderdale": "Fort Lauderdale", "hollywood-florida": "Hollywood", "pembroke-pines": "Pembroke Pines",
    "davie": "Davie", "weston": "Weston", "parkland": "Parkland", "deerfield-beach": "Deerfield Beach",
    "dania-beach": "Dania Beach", "hallandale-beach": "Hallandale Beach",
    "lauderdale-by-the-sea": "Lauderdale-by-the-Sea", "lighthouse-point": "Lighthouse Point",
    "oakland-park": "Oakland Park", "hillsboro-beach": "Hillsboro Beach",
    "naples": "Naples", "marco-island": "Marco Island", "bonita-springs": "Bonita Springs",
    "cape-coral": "Cape Coral", "fort-myers": "Fort Myers", "estero": "Estero", "sanibel": "Sanibel",
    "tampa": "Tampa", "plant-city": "Plant City", "temple-terrace": "Temple Terrace",
    "st-petersburg": "St. Petersburg", "clearwater": "Clearwater", "palm-harbor": "Palm Harbor",
    "orlando": "Orlando", "winter-heaven": "Winter Haven", "key-west": "Key West",
    "marathon": "Marathon", "key-largo": "Key Largo", "palm-bay": "Palm Bay",
    "vero-beach": "Vero Beach", "sebastian": "Sebastian", "port-saint-lucie": "Port St. Lucie",
    "stuart": "Stuart", "sarasota": "Sarasota", "venice": "Venice", "bradenton": "Bradenton",
    "lakeland": "Lakeland", "kissimmee": "Kissimmee"
}

def build_county(slug, name, seat, lat, lng, hvhz, wind, ahj, cities):
    canonical = f"https://acglass.com/{slug}/"
    cities_html = ""
    if cities:
        items = "".join(
            f'<a href="/{c}/" style="background:#0e284f;padding:18px 22px;border-radius:6px;color:#fff;text-decoration:none;display:block;border-left:3px solid #E11320;"><strong>{html_lib.escape(CITY_DISPLAY.get(c, c.title().replace("-"," ")))}</strong></a>'
            for c in cities
        )
        cities_html = f'<h2 style="color:#fff;font-size:26px;margin:32px 0 18px;">Cities we serve in {html_lib.escape(name)}</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:32px;">{items}</div>'

    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">County &middot; Florida</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">Commercial Storefront Glazier — {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">ACG installs commercial storefront, curtain wall, impact-rated glazing, and architectural glass throughout {html_lib.escape(name)}. Florida-licensed CGC #1531993 with documented HVHZ and Florida Product Approval submittal experience. County seat: {html_lib.escape(seat)}.</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1000px;">

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-bottom:40px;">
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;">
<div style="color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Wind Code Zone</div>
<div style="color:#fff;font-size:16px;line-height:1.5;">{html_lib.escape(hvhz)}</div>
</div>
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;">
<div style="color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Design Wind Speed</div>
<div style="color:#fff;font-size:18px;font-weight:700;">{html_lib.escape(wind)}</div>
</div>
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;">
<div style="color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">County Seat</div>
<div style="color:#fff;font-size:18px;font-weight:700;">{html_lib.escape(seat)}</div>
</div>
</div>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Permit and code context in {html_lib.escape(name)}</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:24px;">{html_lib.escape(ahj)}</p>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:32px;">Florida Building Code 8th Edition (2023) governs all glazing in {html_lib.escape(name)}. Wind load is calculated per ASCE 7-22. {('Impact-rated assemblies (or approved shutters) are required for all openings exposed to design wind pressure.' if 'WBDR' in hvhz or 'HVHZ' in hvhz else 'Impact-rated assemblies are not required by code. Standard glazing meeting wind load requirements is acceptable.')}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/commercial-storefronts.html" style="color:#E11320;">Aluminum commercial storefront</a> — Series 451T, 501T, 601T, 701T thermally-broken systems</li>
<li><a href="/curtain-wall.html" style="color:#E11320;">Curtain wall</a> — stick-built and unitized for multi-story commercial</li>
<li><a href="/impact-windows.html" style="color:#E11320;">Impact-rated windows</a> — operable and fixed assemblies</li>
<li>All-glass entrances — frameless single and pair doors with continuous hinges</li>
<li>Folding glass walls and multi-slide doors — for restaurant and hospitality work</li>
<li>Glass railings — for balconies, terraces, and interior stairs</li>
</ul>

{cities_html}

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Industries we serve in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/restaurant-glazier-florida/" style="color:#E11320;">Restaurants</a></li>
<li><a href="/hotel-glazing-contractor-florida/" style="color:#E11320;">Hotels and hospitality</a></li>
<li><a href="/medical-office-glazier-florida/" style="color:#E11320;">Medical office buildings</a></li>
<li><a href="/school-glazier-florida/" style="color:#E11320;">K-12 and higher-ed schools</a></li>
<li><a href="/retail-storefront-installer-florida/" style="color:#E11320;">Retail and mall in-line</a></li>
<li><a href="/office-building-glazier-florida/" style="color:#E11320;">Office buildings</a></li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993 — verifiable at Florida DBPR portal</li>
<li>$3M per project / $6M aggregate bonding capacity</li>
<li>350+ completed commercial projects across Florida</li>
<li>48-hour bid turnaround on standard commercial plans</li>
<li>AI-first operating stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
<li>Documented HVHZ NOA and Florida Product Approval submittal experience</li>
</ul>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(name)} commercial glazing project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Send plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = county_schema(canonical, name, seat, lat, lng)
    bc = [("Home", "https://acglass.com/"), ("Counties", "https://acglass.com/florida-counties/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})

    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Commercial Storefront Glazier {name}, FL | ACG"
    description = f"Commercial storefront, curtain wall, and impact-rated glazing across {name}, Florida. ACG is licensed CGC #1531993 with 350+ commercial projects and 48-hour bid turnaround."

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{GTAG}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(name)}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lng}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
{sblocks}
</head>
<body>
{NAV}
{body}
{FOOTER}
</body>
</html>
'''
    full = os.path.join(OUT, slug, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{slug}/")

def build_counties_hub():
    canonical = "https://acglass.com/florida-counties/"
    cards = ""
    for slug, name, seat, lat, lng, hvhz, wind, ahj, cities in COUNTIES:
        cards += f'<a href="/{slug}/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">{html_lib.escape(name)}</h3><div style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.5;">Seat: {html_lib.escape(seat)}<br>Design wind: {html_lib.escape(wind)}</div></a>'
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Coverage &middot; Florida Counties</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Florida Counties We Serve</h1>
<p style="color:rgba(255,255,255,0.8);font-size:18px;line-height:1.6;max-width:900px;">ACG installs commercial glazing in {len(COUNTIES)} commercially-active Florida counties. Each county page has wind code zone, design wind speed, AHJ permit notes, and links to ACG cities within that county.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;">{cards}</div>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Florida Counties", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Florida Counties We Serve — Commercial Glazing Coverage | ACG"
    description = f"ACG installs commercial glazing in {len(COUNTIES)} Florida counties. County pages include wind code zone, design wind speed, AHJ permit notes, and city coverage."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>
{NAV}
{body}
{FOOTER}
</body>
</html>'''
    full = os.path.join(OUT, "florida-counties", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /florida-counties/")

if __name__ == "__main__":
    print(f"Building {len(COUNTIES)} Florida county pages...")
    for c in COUNTIES:
        build_county(*c)
    build_counties_hub()
    print(f"\nDone: {len(COUNTIES)} counties + 1 hub = {len(COUNTIES)+1} pages.")
