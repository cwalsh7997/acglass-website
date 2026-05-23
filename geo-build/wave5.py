#!/usr/bin/env python3
"""Wave 5 final expansion:
- Tennessee: Memphis, Knoxville, Chattanooga + 3 Nashville neighborhoods
- 10 more vertical x city combos
- /glazier-cost-by-city-florida/ data hub
- /florida-glazing-faq/ master FAQ aggregator
"""
import os, json, sys, html as html_lib

OUT = "/home/user/workspace/acglass-website"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">'''

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links">
<a href="/index.html">Home</a><a href="/case-studies/">Case Studies</a><a href="/tools/">Tools</a>
<a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]


# ============================================================
# Tennessee expansion: 3 new TN cities + 3 Nashville neighborhoods
# ============================================================

TN_NEW = [
    ("memphis", "Memphis", "Shelby", 35.1495, -90.0490, "Standard FBC + TN amendments.", "115 mph",
        "Memphis is Tennessee's largest city by metro population and one of the South's major commercial construction markets. FedEx world headquarters, St Jude Children's Research Hospital, Methodist Le Bonheur Healthcare, and rapidly growing East Memphis / Germantown / Cordova commercial corridors drive ongoing demand. Memphis is not HVHZ; standard IBC + Tennessee state amendments apply.",
        ["Downtown / Beale Street", "East Memphis / Poplar Ave", "Germantown", "Cordova", "Bartlett", "Olive Branch / DeSoto County"]),
    ("knoxville", "Knoxville", "Knox", 35.9606, -83.9207, "Standard IBC + TN amendments.", "115 mph",
        "Knoxville is East Tennessee's commercial center and home to the University of Tennessee. Downtown / Market Square, Bearden, West Knoxville, Cedar Bluff, and the Turkey Creek retail corridor drive the commercial market. Strong office, medical, retail, and restaurant construction. Standard IBC wind code.",
        ["Downtown / Market Square", "Bearden / West Knoxville", "Turkey Creek", "Cedar Bluff", "Hardin Valley", "Farragut"]),
    ("chattanooga", "Chattanooga", "Hamilton", 35.0456, -85.3097, "Standard IBC + TN amendments.", "115 mph",
        "Chattanooga combines an active downtown waterfront commercial market with growing North Shore and East Brainerd commercial corridors. Strong restaurant and tourism-driven commercial. EPB Fiber Network has attracted tech-sector commercial growth. Chattanooga is not HVHZ.",
        ["Downtown / Riverfront", "North Shore", "East Brainerd", "Hamilton Place", "Hixson", "Northshore (north)"])
]

NASHVILLE_NEIGHBORHOODS = [
    ("the-gulch-nashville", "The Gulch", "nashville", "Nashville", 36.1547, -86.7860, "Davidson",
        "The Gulch is Nashville's premier mixed-use district. Restaurant, retail, office, and high-end residential ground-floor commercial. Restaurant concepts (Adele's, Whiskey Kitchen, Virago) and ground-floor retail drive commercial glazing demand."),
    ("sobro-nashville", "SoBro", "nashville", "Nashville", 36.1582, -86.7747, "Davidson",
        "SoBro (South of Broadway) is downtown Nashville's rapidly redeveloping district. Music City Center, JW Marriott, Westin, and the new Convention Center area drive commercial construction. Restaurant, hotel ground floor, and Class-A office are the dominant verticals."),
    ("east-nashville", "East Nashville", "nashville", "Nashville", 36.1801, -86.7567, "Davidson",
        "East Nashville is the city's hippest neighborhood with the strongest indie restaurant and retail commercial market. 5 Points, Riverside Village, Eastland Avenue, and Main Street drive ground-floor commercial. Restaurant glazing dominates the bid mix.")
]


def schema_tn(canonical, name, lat, lng, area_name):
    return [
        {
            "@context": "https://schema.org",
            "@type": ["Organization", "LocalBusiness"],
            "@id": canonical + "#org",
            "name": "American Commercial Glass",
            "url": "https://acglass.com",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "telephone": "+17724867711",
            "address": {"@type": "PostalAddress", "addressLocality": "Nashville", "addressRegion": "TN", "addressCountry": "US"},
            "sameAs": ORG_SAMEAS,
            "areaServed": {"@type": "Place", "name": area_name, "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier \u2014 {name}",
            "serviceType": "Commercial Glazing",
            "areaServed": area_name,
            "provider": {"@id": canonical + "#org"}
        }
    ]


def write_html(rel, html_str):
    full = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"  Wrote /{rel}")


def build_tn_city(slug, name, county, lat, lng, code, wind, blurb, submarkets):
    canonical = f"https://acglass.com/{slug}/"
    sub_html = "".join(f'<li>{html_lib.escape(s)}</li>' for s in submarkets)
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Tennessee &middot; {html_lib.escape(county)} County &middot; Q3 2026</div>
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
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Submarkets and corridors</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">{sub_html}</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Aluminum commercial storefront (Kawneer, YKK AP, Tubelite, EFCO)</li>
<li>Curtain wall \u2014 stick-built and unitized</li>
<li>Window wall systems for multi-family ground-floor commercial</li>
<li>Insulated low-E glass meeting Tennessee IECC energy code</li>
<li>All-glass entrances with continuous hinge hardware</li>
<li>Restaurant folding glass walls and multi-slide doors</li>
<li>Glass railings for balcony, terrace, stair</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Code context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:16px;">{html_lib.escape(name)} follows {html_lib.escape(code)} Design wind speed: <strong style="color:#fff;">{html_lib.escape(wind)}</strong>. Impact-rated glazing is not required by code in Tennessee. IECC energy code applies; Climate Zone 4A (Middle TN) or 3A (Memphis area).</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>350+ commercial projects in Florida \u2014 the same operating playbook applied to Tennessee.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>Nashville office opening Q3 2026 with permanent crew and project management.</li>
<li>AI-first operations stack documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>
</ul>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(name)} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Bidding Q3 2026 and beyond install dates now.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = schema_tn(canonical, name, lat, lng, f"{name}, {county} County, TN")
    bc = [("Home", "https://acglass.com/"), ("Tennessee", "https://acglass.com/tennessee/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})

    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name} TN | Commercial Windows & Doors | ACG"
    description = f"Commercial storefront, curtain wall, and architectural glazing in {name}, {county} County, Tennessee. ACG opens Nashville Q3 2026. 350+ FL projects."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(name)}, TN">
<meta name="geo.region" content="US-TN">
<meta name="ICBM" content="{lat}, {lng}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html(f"{slug}/index.html", html)


def build_nashville_neighborhood(slug, name, parent_slug, parent, lat, lng, county, blurb):
    canonical = f"https://acglass.com/{parent_slug}/{slug}/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Neighborhood &middot; {html_lib.escape(parent)}, TN</div>
<h1 style="color:#fff;font-size:clamp(32px,5vw,52px);line-height:1.1;margin:0 0 24px;">Storefront Glazier \u2014 {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">What we install in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Restaurant storefront and folding glass walls</li>
<li>Retail in-line and freestanding storefront</li>
<li>Ground-floor commercial for mixed-use buildings</li>
<li>Hotel ground-floor and amenity-deck glazing</li>
<li>Office tenant improvements</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Permit context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:24px;">{html_lib.escape(name)} is in {html_lib.escape(parent)}, {html_lib.escape(county)} County, TN. Permits issue through Nashville Metro Codes. ASCE 7-22 wind code; 115 mph design wind. Standard IBC + Tennessee state amendments apply.</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Same operating playbook that built 350+ Florida commercial projects.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>Nashville office opening Q3 2026 \u2014 bidding {html_lib.escape(name)} work now.</li>
<li>Parent city resources: <a href="/{parent_slug}/" style="color:#E11320;">{html_lib.escape(parent)} commercial storefront services</a>.</li>
</ul>
</div>
</section>'''
    schemas = schema_tn(canonical, name, lat, lng, f"{name}, {parent}, TN")
    bc = [("Home", "https://acglass.com/"), ("Tennessee", "https://acglass.com/tennessee/"), (parent, f"https://acglass.com/{parent_slug}/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})

    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name} \u2014 {parent}, TN | ACG"
    description = f"Commercial storefront glazing in {name}, {parent}, TN. ACG opens Nashville Q3 2026. 350+ FL project track record."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(name)}, {html_lib.escape(parent)}, TN">
<meta name="geo.region" content="US-TN">
<meta name="ICBM" content="{lat}, {lng}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html(f"{parent_slug}/{slug}/index.html", html)


# ============================================================
# 10 more vertical x city pages
# ============================================================

VC2 = [
    ("restaurant-glazier-naples", "Restaurant", "Naples", "Collier", "naples", "collier-county", "restaurant-glazier-florida", 26.1420, -81.7948,
        "Naples restaurant construction is driven by upscale resort tourism and a year-round dining economy. Fifth Avenue South, Third Street South, Mercato, and Bayfront drive the restaurant bid market. Indoor-outdoor concepts with folding glass walls are the standard. WBDR coastal impact-rated assemblies required.",
        "Naples is WBDR coastal \u2014 ASTM E1996/E1886 impact-rated assemblies required. Not HVHZ \u2014 Florida Product Approval (FL #) is sufficient."),
    ("restaurant-glazier-fort-lauderdale", "Restaurant", "Fort Lauderdale", "Broward", "fort-lauderdale", "broward-county", "restaurant-glazier-florida", 26.1224, -80.1373,
        "Fort Lauderdale restaurant construction concentrates on Las Olas Boulevard, Flagler Village, the Galleria area, and waterfront / Intracoastal-facing concepts. HVHZ-rated assemblies required; brand-quality finishes expected.",
        "Fort Lauderdale is HVHZ \u2014 Miami-Dade NOA required for all glazing including folding walls and multi-slide doors."),
    ("hotel-glazing-contractor-miami", "Hotel", "Miami", "Miami-Dade", "miami", "miami-dade-county", "hotel-glazing-contractor-florida", 25.7617, -80.1918,
        "Miami hotel construction is the most demanding hotel envelope work in Florida \u2014 HVHZ-rated assemblies, brand-driven design (Faena, Edition, 1 Hotel, Aman, Mandarin Oriental class), and aggressive substantial-completion targets. Curtain wall, balcony rail glass, and ground-floor lobby storefront all in scope.",
        "All Miami hotel envelope work requires Miami-Dade NOA. Unitized curtain wall typical above 8 stories. Factory-bonded structural silicone for SSG."),
    ("hotel-glazing-contractor-tampa", "Hotel", "Tampa", "Hillsborough", "tampa", "hillsborough-county", "hotel-glazing-contractor-florida", 27.9506, -82.4572,
        "Tampa hotel construction is concentrated in Water Street, downtown, Westshore, and the Channelside corridor. Vinik / Strategic Property Partners development, JW Marriott, AC Hotel, and brand-driven Hilton / Marriott / IHG construction. WBDR coastal exposure.",
        "Tampa coastal/downtown is WBDR \u2014 ASTM E1996/E1886 impact-rated assemblies required. Inland Hillsborough is standard FBC."),
    ("medical-office-glazier-miami", "Medical Office", "Miami", "Miami-Dade", "miami", "miami-dade-county", "medical-office-glazier-florida", 25.7617, -80.1918,
        "Miami medical office construction is driven by Baptist Health, Jackson Health System, Cleveland Clinic Florida, and a deep specialty clinic market. Imaging centers, surgical centers, urgent care, and multi-tenant MOB campuses all in active construction. HVHZ-rated assemblies required.",
        "All Miami MOB envelope work requires Miami-Dade NOA. ADA-compliant entrances with auto-operators standard. Privacy glazing (smart glass, frit) common."),
    ("retail-storefront-installer-miami", "Retail", "Miami", "Miami-Dade", "miami", "miami-dade-county", "retail-storefront-installer-florida", 25.7617, -80.1918,
        "Miami retail construction is the highest-pressure retail glazing market in Florida. Design District luxury, Brickell ground-floor retail, Wynwood gallery and showroom, and Aventura mall in-line all driving demand. Brand-driven finishes with full HVHZ NOA submittals.",
        "All Miami retail requires Miami-Dade NOA. Design District luxury retail typically uses structural silicone glazing (factory-bonded HVHZ assemblies)."),
    ("office-building-glazier-tampa", "Office Building", "Tampa", "Hillsborough", "tampa", "hillsborough-county", "office-building-glazier-florida", 27.9506, -82.4572,
        "Tampa office construction has accelerated since 2022. Water Street, downtown, Westshore, Channelside, and Cypress Creek corridor all delivering Class-A office. Strong medical office sub-market driven by Tampa General, BayCare, and AdventHealth.",
        "Tampa is WBDR coastal (east of I-275). ASTM E1996/E1886 impact assemblies required on downtown / waterfront office. Inland Hillsborough is standard FBC."),
    ("office-building-glazier-orlando", "Office Building", "Orlando", "Orange", "orlando", "orange-county", "office-building-glazier-florida", 28.5384, -81.3789,
        "Orlando office construction concentrates on downtown, Lake Mary / Heathrow corridor, Maitland, and the Lake Nona Medical City area. Strong office, medical office, and specialty office (tech, BPO) market. Standard FBC wind code.",
        "Orlando is inland \u2014 standard FBC wind code. Impact-rated glazing optional. ADA, energy, and FBC accessibility requirements apply."),
    ("restaurant-glazier-tampa", "Restaurant", "Tampa", "Hillsborough", "tampa", "hillsborough-county", "restaurant-glazier-florida", 27.9506, -82.4572,
        "Tampa restaurant construction concentrates on Hyde Park Village, Water Street, downtown, Channelside, and the Westshore / International Plaza area. Strong chef-driven restaurant market with brand-driven national concept rollouts.",
        "Tampa coastal restaurants require ASTM E1996/E1886 impact-rated assemblies. Indoor-outdoor concepts use HVHZ-style multi-slide doors with factory-bonded glazing."),
    ("school-glazier-tampa", "School / Education", "Tampa", "Hillsborough", "tampa", "hillsborough-county", "school-glazier-florida", 27.9506, -82.4572,
        "Hillsborough County Public Schools (HCPS) is one of Florida's largest school districts, with ongoing construction across K-12 facilities. Charter network expansion plus University of Tampa and University of South Florida capital programs drive education sector demand.",
        "Tampa schools follow WBDR coastal requirements for most district facilities. Inland HCPS schools may follow standard FBC. Post-Parkland security vestibule design standards apply.")
]


def build_vc2(slug, vertical, city, county, city_slug, county_slug, vert_slug, lat, lng, blurb, hvhz_note):
    canonical = f"https://acglass.com/{slug}/"
    faqs = [
        (f"Does ACG do {vertical.lower()} glazing in {city}?", f"Yes. ACG installs commercial glazing for {vertical.lower()} projects in {city}, {county} County. Florida-licensed CGC #1531993 with 350+ commercial projects and 48-hour bid turnaround."),
        (f"What wind code applies to {city} commercial glazing?", hvhz_note),
        (f"How fast can ACG bid a {city} {vertical.lower()} project?", "ACG returns bids on standard commercial plans in 48 hours. Complex assemblies may take 5-7 business days."),
        (f"What's the typical cost of {vertical.lower()} glazing in {city}?", f"Florida commercial storefront in 2026 ranges from $66-$142/SF installed. {city} HVHZ work sits at the upper end of this range. See our detailed cost guide for full breakdown.")
    ]
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">{html_lib.escape(vertical)} &middot; {html_lib.escape(city)}, FL</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(vertical)} Glazier in {html_lib.escape(city)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Code context for {html_lib.escape(city)}</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:32px;">{html_lib.escape(hvhz_note)}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Florida-licensed CGC #1531993 with 350+ commercial projects.</li>
<li>Documented experience in <a href="/{vert_slug}/" style="color:#E11320;">{vertical.lower()} vertical</a> across Florida.</li>
<li>City-specific knowledge for <a href="/{city_slug}/" style="color:#E11320;">{html_lib.escape(city)}</a>.</li>
<li>County submittal experience in <a href="/{county_slug}/" style="color:#E11320;">{county} County</a>.</li>
<li>48-hour bid turnaround. AI-first operations at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Frequently asked</h2>
<div>{"".join(f'<details style="background:#0e284f;padding:20px 24px;margin-bottom:10px;border-radius:6px;border-left:3px solid #E11320;"><summary style="color:#fff;font-size:17px;font-weight:600;cursor:pointer;">{html_lib.escape(q)}</summary><p style="color:rgba(255,255,255,0.8);font-size:15px;line-height:1.7;margin-top:14px;">{html_lib.escape(a)}</p></details>' for q, a in faqs)}</div>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(city)} {vertical.lower()} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Send plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "logo": "https://acglass.com/images/acg-logo-nav@2x.png", "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "sameAs": ORG_SAMEAS, "areaServed": {"@type": "Place", "name": f"{city}, {county} County, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}},
        {"@context": "https://schema.org", "@type": "Service", "name": f"{vertical} Glazier \u2014 {city}", "serviceType": vertical + " Glazing", "areaServed": f"{city}, FL", "provider": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": vertical, "item": f"https://acglass.com/{vert_slug}/"}, {"@type": "ListItem", "position": 3, "name": city, "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"{vertical} Glazier {city}, FL | Commercial Storefront | ACG"
    description = f"ACG installs {vertical.lower()} commercial glazing in {city}, {county} County, FL. 350+ projects, CGC #1531993, 48-hour bid turnaround."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(city)}, {html_lib.escape(county)} County, FL">
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
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html(f"{slug}/index.html", html)


# ============================================================
# Cost-by-city comparison hub
# ============================================================

def build_cost_by_city():
    canonical = "https://acglass.com/glazier-cost-by-city-florida/"
    rows = [
        ("Miami", "Miami-Dade", "HVHZ", "$96-$142", "$135-$240", "Highest cost zone. NOA-required."),
        ("Fort Lauderdale", "Broward", "HVHZ", "$94-$140", "$130-$232", "Full HVHZ. NOA required."),
        ("West Palm Beach", "Palm Beach", "HVHZ partial", "$78-$132", "$110-$210", "East of Military Trail HVHZ. West cheaper."),
        ("Naples", "Collier", "WBDR", "$78-$125", "$105-$195", "Coastal WBDR. Not HVHZ \u2014 FL # OK."),
        ("Cape Coral / Fort Myers", "Lee", "WBDR", "$76-$120", "$100-$185", "WBDR. Lower than South FL."),
        ("Tampa", "Hillsborough", "WBDR coastal", "$74-$118", "$98-$180", "Coastal WBDR. Inland is FBC standard."),
        ("St. Petersburg", "Pinellas", "WBDR", "$75-$120", "$100-$185", "WBDR. Peninsula geography."),
        ("Orlando", "Orange", "Standard FBC", "$66-$98", "$95-$155", "Cheapest \u2014 inland, no impact required."),
        ("Jacksonville", "Duval", "WBDR coastal", "$72-$115", "$95-$170", "Coastal WBDR. Inland is FBC."),
        ("Sarasota", "Sarasota", "WBDR", "$74-$118", "$98-$180", "Coastal WBDR."),
        ("Tallahassee", "Leon", "Standard FBC", "$66-$96", "$92-$148", "Inland. Cheapest tier."),
        ("Pensacola", "Escambia", "WBDR", "$76-$120", "$100-$180", "Panhandle Gulf coast. WBDR.")
    ]
    row_html = "".join(
        f'<tr><td style="padding:14px 16px;"><strong style="color:#fff;">{html_lib.escape(c)}</strong><br><span style="color:rgba(255,255,255,0.45);font-size:13px;">{html_lib.escape(co)} County</span></td><td style="padding:14px 16px;color:#E11320;font-size:13px;font-weight:600;">{html_lib.escape(z)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.85);font-family:JetBrains Mono,monospace;font-size:14px;font-weight:600;text-align:right;">{html_lib.escape(sf)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.85);font-family:JetBrains Mono,monospace;font-size:14px;font-weight:600;text-align:right;">{html_lib.escape(cw)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.7);font-size:13px;">{html_lib.escape(n)}</td></tr>'
        for c, co, z, sf, cw, n in rows
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Data &middot; 2026 Pricing</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Commercial Glazier Cost by City (Florida, 2026)</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">2026 commercial glazing pricing benchmarks for Florida's 12 most-active commercial markets. Storefront and curtain wall ranges in dollars per square foot installed, based on 350+ ACG bid records.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1100px;">
<div style="overflow-x:auto;background:#0e284f;border-radius:8px;border:1px solid rgba(255,255,255,0.1);">
<table style="width:100%;border-collapse:collapse;min-width:880px;">
<thead><tr style="background:#050A12;">
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">City</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Code Zone</th>
<th style="padding:16px;color:#E11320;text-align:right;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Storefront $/SF</th>
<th style="padding:16px;color:#E11320;text-align:right;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Curtain Wall $/SF</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Notes</th>
</tr></thead>
<tbody>{row_html}</tbody>
</table>
</div>
<p style="color:rgba(255,255,255,0.55);font-size:13px;margin-top:24px;font-style:italic;">Ranges represent typical 2026 commercial work, complete installed scope (glass, framing, hardware, sealants, shop drawings, NOA submittal, labor). Excludes permit fees, structural opening prep by GC, and access (lifts/scaffolding). HVHZ premium typically 20-30% above non-HVHZ; inland Florida sits at the floor of the range. Free to cite with attribution.</p>

<h2 style="color:#fff;font-size:26px;margin:48px 0 18px;">What drives the city-to-city variance</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li><strong style="color:#fff;">Wind code zone</strong> (HVHZ vs WBDR vs standard FBC) drives 20-30% of variance via glass spec and engineering requirements.</li>
<li><strong style="color:#fff;">Labor pool size and rates</strong> \u2014 South Florida glazier hourly rates run 12-18% above Tampa, 20-25% above Orlando.</li>
<li><strong style="color:#fff;">Material logistics</strong> \u2014 Miami and Fort Lauderdale have local Kawneer/YKK/Tubelite stocking distributors. Pensacola and Tallahassee ship from Birmingham or Atlanta.</li>
<li><strong style="color:#fff;">Brand-quality finish expectations</strong> \u2014 Worth Avenue and Design District retail pulls finishes 30-50% above standard commercial.</li>
<li><strong style="color:#fff;">Permit cycle time</strong> \u2014 longer permit cycles in HVHZ counties tie up bid validity periods and influence bid pricing.</li>
</ul>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "Dataset", "name": "Florida Commercial Glazier Cost by City 2026", "description": "Per-square-foot commercial glazing pricing for Florida's 12 most-active commercial markets in 2026.", "creator": {"@id": canonical + "#org"}, "license": "https://creativecommons.org/licenses/by/4.0/", "datePublished": "2026-05-23"},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Resources", "item": "https://acglass.com/resources/"}, {"@type": "ListItem", "position": 3, "name": "Cost by City", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Commercial Glazier Cost by City Florida 2026 \u2014 12 Markets Compared | ACG"
    description = "2026 commercial glazing cost ($/SF) for Florida's 12 most-active markets: Miami, Fort Lauderdale, WPB, Naples, Tampa, Orlando, Jacksonville, and more."
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
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html("glazier-cost-by-city-florida/index.html", html)


# ============================================================
# Master FAQ aggregator hub
# ============================================================

ALL_FAQS = [
    ("How much does commercial storefront cost in Florida in 2026?", "/how-much-does-commercial-storefront-cost-florida/", "$66 to $142 per square foot installed in 2026, including aluminum framing, glass, hardware, sealants, and labor."),
    ("How much does curtain wall cost in Florida in 2026?", "/curtain-wall-cost-florida/", "$95 to $240 per square foot installed in 2026. Stick-built is the lower end; unitized is the upper end."),
    ("What is HVHZ-rated glass?", "/what-is-hvhz-rated-glass/", "Glazing tested for Florida's High-Velocity Hurricane Zone \u2014 Miami-Dade, Broward, parts of Palm Beach. Must pass TAS 201/202/203."),
    ("Where is HVHZ applied in Florida?", "/what-is-hvhz-rated-glass/", "All of Miami-Dade and Broward Counties, plus the portion of Palm Beach east of Military Trail."),
    ("What's the difference between storefront and curtain wall?", "/storefront-vs-curtain-wall/", "Storefront is single-story, span-by-span. Curtain wall is multi-story, hung from the slab edge."),
    ("What's the difference between window wall and curtain wall?", "/what-is-window-wall-system/", "Window wall sits on the floor slab. Curtain wall hangs from the slab edge. Window wall is cheaper."),
    ("Is impact glass better than hurricane shutters?", "/impact-glass-vs-hurricane-shutters/", "For most upscale commercial, impact glass wins on appearance and operational simplicity. Shutters are cheaper but require deployment."),
    ("How long does commercial glass installation take?", "/commercial-glass-installation-timeline/", "6-16 weeks from contract to substantial completion. Material lead time is the dominant variable."),
    ("What is a Miami-Dade NOA?", "/miami-dade-noa-explained/", "Notice of Acceptance \u2014 a document issued by Miami-Dade County certifying a product passes HVHZ testing."),
    ("What's the difference between Florida Product Approval and Miami-Dade NOA?", "/florida-product-approval-vs-noa/", "FL # is statewide approval issued by FL DBPR. NOA is issued by Miami-Dade and required in HVHZ counties."),
    ("What's the difference between tempered and laminated glass?", "/tempered-vs-laminated-glass/", "Tempered is heat-treated for strength. Laminated is two layers bonded to an interlayer. Different code requirements."),
    ("What is low-E glass and why does Florida need it?", "/low-e-glass-explained-florida/", "Glass with a metallic coating that reflects heat. Required by FL Energy Code to meet SHGC \u2264 0.25 in South Florida."),
    ("What's the difference between Kawneer and YKK AP storefront?", "/kawneer-vs-ykk-ap-storefront/", "Both are top commercial aluminum storefront brands. YKK AP is typically 8-15% cheaper and faster on lead time."),
    ("What is structural silicone glazing?", "/structural-silicone-glazing-explained/", "A curtain wall technique where glass is bonded to aluminum with silicone, eliminating exterior pressure caps."),
    ("What is spandrel glass?", "/what-is-spandrel-glass/", "Opaque glass used in curtain walls at slab lines to conceal interior structure."),
    ("What are ADA requirements for storefront doors?", "/ada-storefront-door-requirements-florida/", "32-inch clear width, 5-pound max opening force, level landings, accessible hardware."),
    ("What is fire-rated glazing?", "/fire-rated-glazing-explained/", "Glass tested to maintain integrity during a fire for 20-120 minutes. Required at rated walls and exits."),
    ("What is smart glass?", "/smart-glass-explained-florida-commercial/", "Glass that electronically controls light transmission \u2014 tinting or switching opaque on demand."),
    ("What about glass railings for FL commercial?", "/glass-railing-systems-florida/", "Need structural laminated glass, 50 lb/ft load capacity, and approved post-and-shoe systems."),
    ("Can commercial glass be repaired or replaced?", "/commercial-glass-replacement-vs-repair/", "Most damage requires replacement. Glass cannot be patched or welded. Surface scratches under 1/16 inch may be polished."),
    ("How do I evaluate Florida commercial glaziers?", "/florida-commercial-glaziers-compared/", "Six-criterion framework: license, bonding, HVHZ experience, portfolio fit, response speed, warranty terms."),
    ("How do I find a good commercial glazier in South Florida?", "/best-glaziers-south-florida/", "Verify license, check bonding, document HVHZ submittal experience, match portfolio to your project type."),
    ("What's the best glass for FL restaurant storefronts?", "/best-glass-for-restaurant-storefronts-florida/", "Laminated impact for HVHZ; low-iron for indoor-outdoor concepts; low-E for brand-quality urban restaurants."),
    ("What is blast-resistant glazing?", "/blast-resistant-glazing-florida/", "Heavily laminated glass for federal courthouses, military, security \u2014 ASTM F1642 + GSA Performance Conditions."),
    ("What about automatic door operators for FL commercial?", "/automatic-door-operators-commercial-florida/", "Required for most ADA compliance. Stanley, ASSA ABLOY Besam, Horton are common. $1,800-$4,200/swing operator."),
    ("What aluminum storefront series should I spec?", "/aluminum-storefront-systems-compared/", "Series 451T (basic), 501T (HVHZ standard), 601T (heavy-duty), 701T (high-wind). Each has different face dimensions and wind ratings."),
    ("What are FL Building Code glass requirements?", "/florida-building-code-glass-requirements/", "FBC 2023 governs wind, impact (HVHZ/WBDR), energy (SHGC \u2264 0.25 South FL), and ADA accessibility."),
    ("What does a commercial glass warranty cover?", "/commercial-glass-warranty-explained/", "Insulated seal (10 yr), low-E coating (5-10 yr), aluminum finish (10-20 yr), installer workmanship (1-5 yr).")
]

def build_master_faq():
    canonical = "https://acglass.com/florida-glazing-faq/"
    qa_html = "".join(
        f'<div style="background:#0e284f;padding:24px 28px;margin-bottom:14px;border-radius:6px;border-left:3px solid #E11320;"><a href="{url}" style="text-decoration:none;color:#fff;"><h3 style="color:#fff;font-size:18px;margin:0 0 10px;font-weight:600;">{html_lib.escape(q)}</h3><p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.7;margin:0 0 12px;">{html_lib.escape(a)}</p><div style="color:#E11320;font-size:13px;font-family:JetBrains Mono,monospace;letter-spacing:0.05em;">Read full answer &rarr;</div></a></div>'
        for q, url, a in ALL_FAQS
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Master FAQ &middot; Florida Commercial Glazing</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Florida Commercial Glazing FAQ</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">28 questions architects, GCs, owners, and developers ask about Florida commercial glazing \u2014 with plain-English answers and links to detailed guides. Built for AI engines and humans alike.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
{qa_html}
</div>
</section>'''
    # FAQPage schema for ALL questions in one document
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a in ALL_FAQS]}
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        faq_schema,
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "FAQ", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Florida Commercial Glazing FAQ \u2014 28 Questions Answered | ACG"
    description = "28 plain-English answers on Florida commercial glazing: cost, HVHZ, NOA, storefront vs curtain wall, low-E, impact glass, ADA, fire-rated, smart glass. From ACG."
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
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html("florida-glazing-faq/index.html", html)


if __name__ == "__main__":
    print("Building TN cities...")
    for c in TN_NEW:
        build_tn_city(*c)
    print("\nBuilding Nashville neighborhoods...")
    for n in NASHVILLE_NEIGHBORHOODS:
        build_nashville_neighborhood(*n)
    print("\nBuilding vertical x city wave 2...")
    for v in VC2:
        build_vc2(*v)
    print("\nBuilding cost-by-city hub...")
    build_cost_by_city()
    print("\nBuilding master FAQ...")
    build_master_faq()
    total = len(TN_NEW) + len(NASHVILLE_NEIGHBORHOODS) + len(VC2) + 2
    print(f"\nTotal wave 5: {total} pages.")
