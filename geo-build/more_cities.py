#!/usr/bin/env python3
"""Additional Florida cities — Jacksonville, Pensacola, Tallahassee, Gainesville,
Daytona, Cape Coral, Fort Myers, and 8 more major commercial markets we hadn't covered."""
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
<div><h4>North Florida</h4><ul><li><a href="/jacksonville/">Jacksonville</a></li><li><a href="/tallahassee/">Tallahassee</a></li><li><a href="/gainesville/">Gainesville</a></li><li><a href="/pensacola/">Pensacola</a></li></ul></div>
<div><h4>SW Florida</h4><ul><li><a href="/cape-coral/">Cape Coral</a></li><li><a href="/fort-myers/">Fort Myers</a></li><li><a href="/estero/">Estero</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]

# slug, name, county, county_slug, lat, lng, hvhz_status, wind, blurb
CITIES = [
    ("jacksonville", "Jacksonville", "Duval", "duval-county", 30.3322, -81.6557, "WBDR coastal; Standard FBC inland.", "140 mph",
        "Jacksonville is Florida's largest city by area and one of its fastest-growing commercial construction markets. Downtown waterfront, Riverside, San Marco, and Town Center submarkets all show strong commercial activity. Duval County is consolidated city-county, simplifying permit submittal vs. the multi-AHJ stacks in South Florida."),
    ("tallahassee", "Tallahassee", "Leon", "leon-county", 30.4383, -84.2807, "Standard FBC. Inland.", "130 mph",
        "Tallahassee is the state capital and home to FSU and FAMU. State government, university, and healthcare drive commercial construction. Standard FBC wind code — no impact glass requirement. Inland location keeps glass costs 18-25% below South Florida HVHZ market."),
    ("gainesville", "Gainesville", "Alachua", "alachua-county", 29.6516, -82.3248, "Standard FBC. Inland.", "130 mph",
        "Gainesville is home to UF and a strong medical and biotech corridor. Innovation Square, downtown, and Midtown submarkets show active commercial construction. Standard FBC wind code."),
    ("pensacola", "Pensacola", "Escambia", "escambia-county", 30.4213, -87.2169, "WBDR — Panhandle Gulf coast.", "150 mph",
        "Pensacola is the Florida Panhandle's primary city. Naval Air Station Pensacola, downtown, and Pensacola Beach drive commercial demand. WBDR-rated impact glass or shutters required. Hurricane exposure (Sally 2020, Ivan 2004)."),
    ("cape-coral", "Cape Coral", "Lee", "lee-county", 26.5629, -81.9495, "WBDR — Gulf coast.", "160 mph",
        "Cape Coral is one of Florida's largest cities by population and is rapidly growing commercially. Pine Island Road corridor, downtown Cape Coral, and Veterans Pkwy show active retail and office construction. WBDR-rated impact glazing required. Hurricane Ian (2022) impact zone."),
    ("fort-myers", "Fort Myers", "Lee", "lee-county", 26.6406, -81.8723, "WBDR — Gulf coast.", "160 mph",
        "Fort Myers is the commercial center of Southwest Florida and the Lee County seat. Downtown River District, Fort Myers Beach, Page Field, and Daniels Pkwy corridor are all active commercial submarkets. Hurricane Ian impact zone."),
    ("estero", "Estero", "Lee", "lee-county", 26.4384, -81.8068, "WBDR — Gulf coast.", "160 mph",
        "Estero is between Fort Myers and Naples on US 41. Coconut Point, Miromar Outlets, and the Hertz Arena area drive commercial construction. Strong retail and office markets."),
    ("daytona-beach", "Daytona Beach", "Volusia", "volusia-county", 29.2108, -81.0228, "WBDR coastal.", "145 mph",
        "Daytona Beach is the Volusia County commercial center. Tourist corridor (A1A, International Speedway Blvd), downtown, and the One Daytona development drive commercial construction."),
    ("port-orange", "Port Orange", "Volusia", "volusia-county", 29.1383, -80.9956, "WBDR coastal; Standard FBC inland.", "145 mph",
        "Port Orange is the suburban core south of Daytona Beach. Dunlawton Avenue and Port Orange Causeway drive retail and office construction."),
    ("ocala", "Ocala", "Marion", "marion-county", 29.1872, -82.1401, "Standard FBC. Inland.", "135 mph",
        "Ocala is central North Florida's commercial center. Downtown, US 27, and SR 200 corridors drive commercial construction. Strong equestrian-economy and medical markets."),
    ("sanford", "Sanford", "Seminole", "seminole-county", 28.8005, -81.2731, "Standard FBC. Inland.", "140 mph",
        "Sanford is the Seminole County seat. Historic downtown, RiverWalk, and SR 46 corridor drive commercial activity. Orlando-Sanford International Airport supports industrial commercial."),
    ("kissimmee-tourism", "Kissimmee Tourism Corridor", "Osceola", "osceola-county", 28.3072, -81.4178, "Standard FBC. Inland.", "140 mph",
        "Kissimmee is the gateway to Disney and Universal. US 192, Celebration, and Lake Buena Vista corridors drive significant restaurant, hotel, and retail commercial construction."),
    ("winter-park", "Winter Park", "Orange", "orange-county", 28.6000, -81.3392, "Standard FBC. Inland.", "140 mph",
        "Winter Park is metropolitan Orlando's upscale suburb. Park Avenue retail corridor and Hannibal Square drive boutique commercial construction. Sensitive design review."),
    ("st-augustine", "St. Augustine", "St. Johns", "duval-county", 29.9012, -81.3124, "WBDR coastal.", "140 mph",
        "St. Augustine is North Florida's historic coastal city. Old Town, Vilano Beach, and World Golf Village drive commercial construction. WBDR coastal exposure with strict historic preservation review downtown."),
    ("ponte-vedra-beach", "Ponte Vedra Beach", "St. Johns", "duval-county", 30.2391, -81.3853, "WBDR coastal.", "140 mph",
        "Ponte Vedra Beach is North Florida's upscale coastal community. TPC Sawgrass area and Nocatee drive luxury commercial and resort construction. WBDR coastal exposure.")
]

def schema(canonical, name, lat, lng, county):
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
            "areaServed": {"@type": "Place", "name": f"{name}, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier — {name}",
            "serviceType": "Commercial Glazing",
            "areaServed": {"@type": "Place", "name": f"{name}, {county} County, FL"},
            "provider": {"@id": canonical + "#org"}
        }
    ]

def build_city(slug, name, county, county_slug, lat, lng, hvhz, wind, blurb):
    canonical = f"https://acglass.com/{slug}/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">City &middot; {html_lib.escape(county)} County, FL</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">Storefront Glazier in {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">

<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:36px;">
<div style="background:#0e284f;padding:22px;border-left:3px solid #E11320;border-radius:6px;">
<div style="color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Wind Code</div>
<div style="color:#fff;font-size:15px;line-height:1.5;">{html_lib.escape(hvhz)}</div>
</div>
<div style="background:#0e284f;padding:22px;border-left:3px solid #E11320;border-radius:6px;">
<div style="color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Design Wind Speed</div>
<div style="color:#fff;font-size:18px;font-weight:700;">{html_lib.escape(wind)}</div>
</div>
</div>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/commercial-storefronts.html" style="color:#E11320;">Aluminum commercial storefront</a></li>
<li><a href="/curtain-wall.html" style="color:#E11320;">Curtain wall</a> — stick-built and unitized</li>
<li><a href="/impact-windows.html" style="color:#E11320;">Impact-rated windows</a></li>
<li>All-glass entrances — frameless single and pair doors</li>
<li>Folding glass walls and multi-slide doors</li>
<li>Glass railings for balconies, terraces, stairs</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Permit and code context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:24px;">{html_lib.escape(name)} is in <a href="/{county_slug}/" style="color:#E11320;">{html_lib.escape(county)} County</a>, Florida. Wind code zone: {html_lib.escape(hvhz)} Florida Building Code 8th Edition (2023) applies. {('Impact-rated assemblies or approved shutters are required by code for openings exposed to design wind pressure.' if 'WBDR' in hvhz or 'HVHZ' in hvhz else 'Impact-rated glazing is not required by code in this market. Standard wind-rated glass is acceptable.')}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Industries we serve in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/restaurant-glazier-florida/" style="color:#E11320;">Restaurants</a></li>
<li><a href="/hotel-glazing-contractor-florida/" style="color:#E11320;">Hotels and hospitality</a></li>
<li><a href="/medical-office-glazier-florida/" style="color:#E11320;">Medical office buildings</a></li>
<li><a href="/school-glazier-florida/" style="color:#E11320;">K-12 and higher-ed schools</a></li>
<li><a href="/retail-storefront-installer-florida/" style="color:#E11320;">Retail</a></li>
<li><a href="/office-building-glazier-florida/" style="color:#E11320;">Office buildings</a></li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993, $3M/$6M bonding capacity</li>
<li>350+ completed commercial projects across Florida</li>
<li>48-hour bid turnaround on standard commercial plans</li>
<li>AI-first operating stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
<li>Documented Florida Product Approval submittal experience</li>
</ul>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(name)} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:26px;">Send plans for a 48-hour response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = schema(canonical, name, lat, lng, county)
    bc = [("Home", "https://acglass.com/"), (county + " County", f"https://acglass.com/{county_slug}/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})

    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name}, FL | Commercial Windows & Doors | ACG"
    description = f"Commercial storefront, curtain wall, and impact-rated glazing in {name}, {county} County, Florida. ACG is licensed CGC #1531993 with 350+ commercial projects."

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
<meta name="geo.placename" content="{html_lib.escape(name)}, {html_lib.escape(county)} County, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lng}">
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
</html>
'''
    full = os.path.join(OUT, slug, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{slug}/")

if __name__ == "__main__":
    for c in CITIES:
        build_city(*c)
    print(f"\n{len(CITIES)} cities built.")
