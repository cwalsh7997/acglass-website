#!/usr/bin/env python3
"""Wave 3: vertical x city matrix pages, permit timeline by county, near-me pages, author bios."""
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
<a href="/index.html">Home</a><a href="/portfolio.html">Portfolio</a><a href="/case-studies/">Case Studies</a>
<a href="/tools/">Tools</a><a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Industries</h4><ul><li><a href="/restaurant-glazier-florida/">Restaurants</a></li><li><a href="/hotel-glazing-contractor-florida/">Hotels</a></li><li><a href="/medical-office-glazier-florida/">Medical</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]

# ============================================================
# Vertical x Top-City matrix (6 high-value combos)
# ============================================================

VC_PAGES = [
    {
        "slug": "restaurant-glazier-miami",
        "vertical": "Restaurant",
        "city": "Miami",
        "county": "Miami-Dade",
        "city_slug": "miami",
        "county_slug": "miami-dade-county",
        "vertical_slug": "restaurant-glazier-florida",
        "lat": 25.7617, "lng": -80.1918,
        "blurb": "Miami restaurant storefront is a category of its own. HVHZ-rated assemblies, brand-driven design criteria (Carbone, Cipriani, Komodo level finish), and aggressive substantial-completion targets driven by reservation calendars. We have installed glass on Miami restaurant projects from Brickell to Wynwood to the Design District.",
        "hvhz_note": "All Miami restaurants require Miami-Dade NOA glazing. Folding glass walls and multi-slide doors must use factory-bonded HVHZ-rated assemblies.",
    },
    {
        "slug": "hotel-glazing-contractor-naples",
        "vertical": "Hotel",
        "city": "Naples",
        "county": "Collier",
        "city_slug": "naples",
        "county_slug": "collier-county",
        "vertical_slug": "hotel-glazing-contractor-florida",
        "lat": 26.1420, "lng": -81.7948,
        "blurb": "Naples hotel construction sits at the intersection of WBDR coastal exposure (160 mph design wind), upscale resort finish standards (Ritz-Carlton, Naples Beach Club, Inn on Fifth class), and Collier County / City of Naples design review. Brand-quality envelope work is decisive.",
        "hvhz_note": "Naples is WBDR but not HVHZ. ASTM E1996/E1886 impact-rated assemblies are required for all hotel openings. Florida Product Approval (FL #) is sufficient \u2014 Miami-Dade NOA not required.",
    },
    {
        "slug": "medical-office-glazier-west-palm-beach",
        "vertical": "Medical Office",
        "city": "West Palm Beach",
        "county": "Palm Beach",
        "city_slug": "west-palm-beach",
        "county_slug": "palm-beach-county",
        "vertical_slug": "medical-office-glazier-florida",
        "lat": 26.7153, "lng": -80.0534,
        "blurb": "West Palm Beach is one of Florida's most active medical office building markets. Cleveland Clinic, JFK Medical Center, and Good Samaritan campus expansion plus tenant-improvement clinics on Okeechobee Boulevard, Belvedere, and Forest Hill drive ongoing demand.",
        "hvhz_note": "WPB sits at the HVHZ boundary \u2014 Military Trail is the line. East of Military Trail (most of downtown, hospital corridor) requires HVHZ NOA. West requires WBDR-rated assemblies.",
    },
    {
        "slug": "retail-storefront-installer-tampa",
        "vertical": "Retail",
        "city": "Tampa",
        "county": "Hillsborough",
        "city_slug": "tampa",
        "county_slug": "hillsborough-county",
        "vertical_slug": "retail-storefront-installer-florida",
        "lat": 27.9506, "lng": -82.4572,
        "blurb": "Tampa retail growth is concentrated in Water Street, Hyde Park Village, Westshore, and the Channelside corridor. Brand-driven storefront, mall in-line, and freestanding pad-site retail. WBDR coastal wind exposure.",
        "hvhz_note": "Tampa is WBDR coastal (east of I-275) and standard FBC inland. Most downtown / waterfront retail requires ASTM E1996/E1886 impact-rated assemblies. Hillsborough County issues permits outside city limits.",
    },
    {
        "slug": "school-glazier-orlando",
        "vertical": "School / Education",
        "city": "Orlando",
        "county": "Orange",
        "city_slug": "orlando",
        "county_slug": "orange-county",
        "vertical_slug": "school-glazier-florida",
        "lat": 28.5384, "lng": -81.3789,
        "blurb": "Orlando area school construction is heavy: OCPS (Orange County Public Schools), Seminole County Public Schools, and charter networks deliver summer-turnover projects with security vestibule, classroom impact upgrades, and gym storefront work. Orange and Seminole counties are standard FBC wind, so impact assemblies are not code-required.",
        "hvhz_note": "Orange County is inland \u2014 standard FBC wind code. Impact assemblies optional. Post-Parkland school security mandates still apply (vestibule design, ballistic-rated entries).",
    },
    {
        "slug": "office-building-glazier-fort-lauderdale",
        "vertical": "Office Building",
        "city": "Fort Lauderdale",
        "county": "Broward",
        "city_slug": "fort-lauderdale",
        "county_slug": "broward-county",
        "vertical_slug": "office-building-glazier-florida",
        "lat": 26.1224, "lng": -80.1373,
        "blurb": "Fort Lauderdale office construction has accelerated since 2022 \u2014 Las Olas, downtown, and Cypress Creek corridor all delivering Class-A office space. Broward County is full HVHZ, so all envelope work requires Miami-Dade NOA-rated assemblies.",
        "hvhz_note": "Broward County is full HVHZ. All curtain wall, storefront, window wall, and punch windows require Miami-Dade NOA. Factory-bonded structural silicone for all SSG applications.",
    },
]

def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def build_vc(p):
    canonical = f"https://acglass.com/{p['slug']}/"
    faqs = [
        (f"Does ACG do {p['vertical'].lower()} glazing in {p['city']}?", f"Yes. ACG installs commercial glazing for {p['vertical'].lower()} projects in {p['city']}, {p['county']} County. Florida-licensed CGC #1531993 with 350+ commercial projects and 48-hour bid turnaround."),
        (f"What wind code applies to {p['city']} commercial glazing?", p['hvhz_note']),
        (f"How fast can ACG bid a {p['city']} {p['vertical'].lower()} project?", "ACG returns bids on standard commercial plans in 48 hours. Complex assemblies with structural engineering may take 5-7 business days."),
        (f"What's the typical cost of {p['vertical'].lower()} glazing in {p['city']}?", f"Depends on scope, but for storefront work in {p['city']}, 2026 budget ranges from $66 to $142 per square foot installed. See our detailed cost guide for the full breakdown."),
    ]

    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">{html_lib.escape(p['vertical'])} &middot; {html_lib.escape(p['city'])}, FL</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(p['vertical'])} Glazier in {html_lib.escape(p['city'])}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(p['blurb'])}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Code context for {html_lib.escape(p['city'])}</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:32px;">{html_lib.escape(p['hvhz_note'])}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG for {p['vertical'].lower()} glazing in {html_lib.escape(p['city'])}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Florida-licensed CGC #1531993 with 350+ commercial projects.</li>
<li>Documented experience in <a href="/{p['vertical_slug']}/" style="color:#E11320;">{p['vertical'].lower()} vertical</a> across Florida.</li>
<li>City-specific permit and AHJ knowledge for <a href="/{p['city_slug']}/" style="color:#E11320;">{html_lib.escape(p['city'])}</a>.</li>
<li>County-level submittal experience in <a href="/{p['county_slug']}/" style="color:#E11320;">{p['county']} County</a>.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>AI-first operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Frequently asked</h2>
<div>{"".join(f'<details style="background:#0e284f;padding:20px 24px;margin-bottom:10px;border-radius:6px;border-left:3px solid #E11320;"><summary style="color:#fff;font-size:17px;font-weight:600;cursor:pointer;">{html_lib.escape(q)}</summary><p style="color:rgba(255,255,255,0.8);font-size:15px;line-height:1.7;margin-top:14px;">{html_lib.escape(a)}</p></details>' for q, a in faqs)}</div>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(p['city'])} {p['vertical'].lower()} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Send plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "logo": "https://acglass.com/images/acg-logo-nav@2x.png", "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "sameAs": ORG_SAMEAS, "areaServed": {"@type": "Place", "name": f"{p['city']}, {p['county']} County, FL", "geo": {"@type": "GeoCoordinates", "latitude": p['lat'], "longitude": p['lng']}}},
        {"@context": "https://schema.org", "@type": "Service", "name": f"{p['vertical']} Glazier \u2014 {p['city']}", "serviceType": p['vertical'] + " Glazing", "areaServed": f"{p['city']}, FL", "provider": {"@id": canonical + "#org"}},
        faq_schema(faqs),
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": p['vertical'], "item": f"https://acglass.com/{p['vertical_slug']}/"}, {"@type": "ListItem", "position": 3, "name": p['city'], "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"{p['vertical']} Glazier {p['city']}, FL | Commercial Storefront | ACG"
    description = f"ACG installs commercial {p['vertical'].lower()} glazing in {p['city']}, {p['county']} County, FL. 350+ projects, CGC #1531993, 48-hour bid turnaround."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{p['lat']};{p['lng']}">
<meta name="geo.placename" content="{html_lib.escape(p['city'])}, {html_lib.escape(p['county'])} County, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{p['lat']}, {p['lng']}">
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
    full = os.path.join(OUT, p['slug'], "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{p['slug']}/")


# ============================================================
# Permit timeline by county
# ============================================================

def build_permit_timeline():
    canonical = "https://acglass.com/florida-glazing-permit-timeline-by-county/"
    rows = [
        ("Miami-Dade", "HVHZ", "15-25 days", "30-60 days", "Strict NOA enforcement. Plan extra time for first-submittal rejections.", "miami-dade-county"),
        ("Broward", "HVHZ", "12-22 days", "Standard NOA review", "Generally faster than Miami-Dade. NOA acceptance straightforward.", "broward-county"),
        ("Palm Beach", "HVHZ partial / WBDR", "10-18 days", "Standard", "Faster than HVHZ counties. Military Trail boundary determines NOA requirement.", "palm-beach-county"),
        ("Collier", "WBDR", "10-15 days", "Standard", "Naples has separate municipal review on top. Plan 1-2 extra weeks for City of Naples.", "collier-county"),
        ("Lee", "WBDR", "10-18 days", "Standard", "Fort Myers and Cape Coral have separate municipal reviews. Post-Ian backlog can stretch this.", "lee-county"),
        ("Monroe", "WBDR severe", "12-20 days", "Standard", "Florida Keys severity drives 180 mph design wind. Plan extra time for specialty assemblies.", "monroe-county"),
        ("Hillsborough", "WBDR coastal", "10-15 days", "Standard", "City of Tampa has separate review. Inland Hillsborough is faster.", "hillsborough-county"),
        ("Pinellas", "WBDR", "10-15 days", "Standard", "St Pete and Clearwater have separate municipal reviews.", "pinellas-county"),
        ("Orange", "Standard FBC", "7-12 days", "Standard", "Inland \u2014 no NOA required. Faster permit cycle than coastal counties.", "orange-county"),
        ("Sarasota", "WBDR", "10-15 days", "Standard", "City of Sarasota separate review. Generally efficient AHJ.", "sarasota-county"),
        ("Duval", "WBDR coastal", "10-15 days", "Standard", "Consolidated city-county (Jacksonville). Single AHJ \u2014 simpler than multi-AHJ South Florida.", "duval-county"),
        ("Leon", "Standard FBC", "7-12 days", "Standard", "Tallahassee. Inland. Fast permit cycle.", "leon-county"),
        ("Brevard", "WBDR", "10-15 days", "Standard", "Space Coast. Multiple municipal AHJs (Cocoa, Melbourne, Palm Bay).", "brevard-county"),
    ]
    row_html = "".join(
        f'<tr><td style="padding:14px 16px;"><a href="/{slug}/" style="color:#fff;font-weight:600;text-decoration:none;">{html_lib.escape(c)}</a></td><td style="padding:14px 16px;color:#E11320;font-size:13px;font-weight:600;">{html_lib.escape(z)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.85);font-family:JetBrains Mono,monospace;font-size:13px;">{html_lib.escape(p)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.85);font-family:JetBrains Mono,monospace;font-size:13px;">{html_lib.escape(n)}</td><td style="padding:14px 16px;color:rgba(255,255,255,0.7);font-size:13px;line-height:1.5;">{html_lib.escape(note)}</td></tr>'
        for c, z, p, n, note, slug in rows
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Resource &middot; Permit Cycle Times</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Florida Glazing Permit Timeline by County</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">Average commercial glazing permit review times for Florida's 13 most-active commercial counties. Based on ACG's 350+ project submittal records 2022-2026.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1100px;">
<div style="overflow-x:auto;background:#0e284f;border-radius:8px;border:1px solid rgba(255,255,255,0.1);">
<table style="width:100%;border-collapse:collapse;min-width:880px;">
<thead><tr style="background:#050A12;">
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">County</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Zone</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Permit</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">NOA Review</th>
<th style="padding:16px;color:#E11320;text-align:left;font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;">Notes</th>
</tr></thead>
<tbody>{row_html}</tbody>
</table>
</div>
<p style="color:rgba(255,255,255,0.55);font-size:13px;margin-top:24px;font-style:italic;">Times are typical commercial glazing review windows. Complex assemblies, first-time NOAs, structural deviations, and overloaded review queues can extend these. Always confirm with the specific AHJ before relying on a number for your schedule.</p>

<h2 style="color:#fff;font-size:26px;margin:48px 0 18px;">How to compress your permit timeline</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Submit a complete package the first time. Missing NOA references, design pressure mismatches, and anchorage detail issues are the top three rejection causes.</li>
<li>Use stock NOA assemblies. Custom assemblies that require new NOA review add 30-60 days.</li>
<li>Choose qualified glaziers with documented submittal experience in your AHJ. ACG submits in all 25 Florida commercial counties.</li>
<li>Coordinate structural opening dimensions with the GC BEFORE shop drawings. Re-engineering after framing changes adds 2-3 weeks.</li>
<li>Time the submittal to the AHJ's review queue. Mondays after holidays are the worst; Tuesday-Thursday of mid-month is the best.</li>
</ul>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "Article", "headline": "Florida Glazing Permit Timeline by County", "datePublished": "2026-05-23", "dateModified": "2026-05-23", "author": {"@type": "Organization", "name": "American Commercial Glass"}, "publisher": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Resources", "item": "https://acglass.com/resources/"}, {"@type": "ListItem", "position": 3, "name": "Permit Timeline by County", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Florida Glazing Permit Timeline by County (2026) | ACG"
    description = "Florida commercial glazing permit review timelines for 13 most-active counties. Miami-Dade NOA review windows. Based on ACG's 350+ project submittal records."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="article">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    full = os.path.join(OUT, "florida-glazing-permit-timeline-by-county", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  Wrote /florida-glazing-permit-timeline-by-county/")


# ============================================================
# Author bio pages
# ============================================================

def build_author_pages():
    authors = [
        {
            "slug": "connor-walsh",
            "name": "Connor Walsh",
            "role": "President & Co-founder",
            "blurb": "Connor Walsh is President and co-founder of American Commercial Glass (ACG), the Florida commercial storefront glazing contractor based in West Palm Beach. Connor leads operations, AI-augmented bid engineering, and GC relationships. He co-founded ACG with his wife Rielly Walsh in 2020 and has scaled the company across 350+ commercial projects spanning restaurant, hotel, medical, school, retail, and office building work.",
            "expertise": [
                "Commercial storefront glazing system specification (Series 451T, 501T, 601T, 701T)",
                "Florida HVHZ Miami-Dade NOA and Wind-Borne Debris Region submittal coordination",
                "AI-augmented bid engineering using custom in-house applications (Sub.ai, jobcost.ai, CFO Agent)",
                "Procore-native subcontractor operations for commercial general contractors",
                "Florida commercial glazing market pricing 2020-2026",
                "Multi-vertical project execution: restaurant, hotel, medical, school, retail, office"
            ],
            "achievements": [
                "Co-founded ACG (American Commercial Glass) in 2020",
                "Florida Certified General Contractor (CGC #1531993)",
                "350+ commercial projects executed",
                "Built custom AI applications for construction operations (documented at acglass.ai)",
                "Speaking at construction industry events on AI-first operating models"
            ],
            "linkedin": "https://www.linkedin.com/in/connor-walsh9/",
            "email": "connor@acglass.com"
        },
        {
            "slug": "rielly-walsh",
            "name": "Rielly Walsh",
            "role": "CEO & Co-founder",
            "blurb": "Rielly Walsh is CEO and co-founder of American Commercial Glass (ACG). She leads finance, project intake, vendor relations, and the operational systems that make ACG's AI-augmented stack work in the real world. WBE/SBE-certified leadership of a Florida commercial glazing contractor.",
            "expertise": [
                "Construction company financial operations and bookkeeping at scale",
                "Florida commercial glazing project intake and qualification",
                "Vendor management across Eurowall, ESWindows/Tecnoglass, Kawneer, YKK AP",
                "AIA G702/G703 owner-pay application workflow and certified payroll",
                "Women Business Enterprise (WBE) and Small Business Enterprise (SBE) certification",
                "Construction sector accounts payable, accounts receivable, lien rights"
            ],
            "achievements": [
                "Co-founded ACG in 2020",
                "Built ACG's financial operating system around QuickBooks + Procore + custom AI integrations",
                "WBE-certified leadership of ACG",
                "Active NAWIC (National Association of Women in Construction) Palm Beach member (in process)"
            ],
            "linkedin": "https://www.linkedin.com/company/american-commercial-glass/",
            "email": "rielly@acglass.com"
        }
    ]

    for a in authors:
        canonical = f"https://acglass.com/author/{a['slug']}/"
        exp = "".join(f'<li>{html_lib.escape(e)}</li>' for e in a['expertise'])
        ach = "".join(f'<li>{html_lib.escape(e)}</li>' for e in a['achievements'])
        body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Author &middot; ACG Leadership</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 16px;">{html_lib.escape(a['name'])}</h1>
<div style="color:#E11320;font-size:18px;font-weight:600;margin-bottom:24px;font-family:JetBrains Mono,monospace;">{html_lib.escape(a['role'])}, American Commercial Glass</div>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">{html_lib.escape(a['blurb'])}</p>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Areas of expertise</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">{exp}</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Professional achievements</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">{ach}</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Contact</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:none;padding:0;">
<li>Email: <a href="mailto:{a['email']}" style="color:#E11320;">{a['email']}</a></li>
<li>LinkedIn: <a href="{a['linkedin']}" style="color:#E11320;">{html_lib.escape(a['linkedin'])}</a></li>
<li>Company: <a href="https://acglass.com" style="color:#E11320;">American Commercial Glass</a></li>
<li>AI operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
</ul>

</div>
</section>'''
        schemas = [
            {"@context": "https://schema.org", "@type": "Person", "name": a['name'], "jobTitle": a['role'], "worksFor": {"@type": "Organization", "name": "American Commercial Glass", "url": "https://acglass.com"}, "email": a['email'], "sameAs": [a['linkedin']], "knowsAbout": a['expertise'], "url": canonical, "image": "https://acglass.com/images/acg-logo-nav@2x.png"},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Author", "item": "https://acglass.com/author/"}, {"@type": "ListItem", "position": 3, "name": a['name'], "item": canonical}]}
        ]
        sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
        title = f"{a['name']} \u2014 {a['role']}, American Commercial Glass | ACG"
        description = f"{a['name']}, {a['role']} of American Commercial Glass. Florida commercial storefront glazing contractor (CGC #1531993). Background, expertise, achievements."
        html_str = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="profile">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/acg-logo-nav@2x.png">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
        full = os.path.join(OUT, "author", a['slug'], "index.html")
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html_str)
        print(f"  Wrote /author/{a['slug']}/")


# ============================================================
# Near-me pages
# ============================================================

NEAR_ME = [
    {"slug": "commercial-glazier-near-me-west-palm-beach", "city": "West Palm Beach", "lat": 26.7153, "lng": -80.0534, "county": "Palm Beach", "county_slug": "palm-beach-county", "blurb": "If you're searching for a commercial glazier near you in West Palm Beach, ACG is headquartered downtown at 700 S Rosemary Avenue (Rosemary Square). We are the closest licensed commercial glazing contractor for projects within Palm Beach County, with on-the-ground crews available for site visits, takeoffs, and emergency calls."},
    {"slug": "commercial-glazier-near-me-miami", "city": "Miami", "lat": 25.7617, "lng": -80.1918, "county": "Miami-Dade", "county_slug": "miami-dade-county", "blurb": "Searching for a commercial glazier near you in Miami? ACG serves all of Miami-Dade County with the same crews and project management team that handle 350+ South Florida commercial projects. We respond to Miami area RFPs and site visit requests within 24 hours."},
    {"slug": "commercial-glazier-near-me-tampa", "city": "Tampa", "lat": 27.9506, "lng": -82.4572, "county": "Hillsborough", "county_slug": "hillsborough-county", "blurb": "Searching for a commercial glazier near you in Tampa? ACG covers the entire Tampa Bay area — Hillsborough, Pinellas, Pasco, and Manatee counties — with project management and field crews routed from our Tampa coverage zone."},
]

def build_near_me(p):
    canonical = f"https://acglass.com/{p['slug']}/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Local Coverage &middot; {html_lib.escape(p['city'])}</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">Commercial Glazier Near {html_lib.escape(p['city'])}, FL</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(p['blurb'])}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="tel:+17724867711" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Call (772) 486-7711</a>
<a href="/send-plans.html" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Plans</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">What we install near {html_lib.escape(p['city'])}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Commercial storefront systems</li>
<li>Curtain wall (stick-built and unitized)</li>
<li>Impact-rated windows</li>
<li>All-glass entrances</li>
<li>Folding glass walls and multi-slide doors</li>
<li>Glass railings and partitions</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Local context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:16px;">{html_lib.escape(p['city'])} is in <a href="/{p['county_slug']}/" style="color:#E11320;">{p['county']} County</a>, Florida. See our <a href="/{p['city'].lower().replace(' ', '-')}/" style="color:#E11320;">{html_lib.escape(p['city'])} commercial storefront page</a> for full service details, code context, and submarket coverage.</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG when searching for a local glazier</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993 \u2014 verifiable on the FL DBPR portal</li>
<li>350+ commercial projects across Florida</li>
<li>24-hour response on site visits and emergency calls in this market</li>
<li>48-hour bid turnaround on standard commercial plans</li>
<li>AI-first operations \u2014 fastest takeoff, fastest submittal, fastest install</li>
</ul>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Looking for a local commercial glazier in {html_lib.escape(p['city'])}?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Call (772) 486-7711 or send plans.</p>
<a href="tel:+17724867711" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Call Now</a>
</div>
</section>'''

    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "logo": "https://acglass.com/images/acg-logo-nav@2x.png", "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "sameAs": ORG_SAMEAS, "areaServed": {"@type": "Place", "name": f"{p['city']}, FL", "geo": {"@type": "GeoCoordinates", "latitude": p['lat'], "longitude": p['lng']}}, "openingHours": "Mo-Fr 07:00-17:00"},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": p['city'], "item": f"https://acglass.com/{p['city'].lower().replace(' ', '-')}/"}, {"@type": "ListItem", "position": 3, "name": "Commercial Glazier Near Me", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Commercial Glazier Near Me \u2014 {p['city']}, FL | ACG"
    description = f"Looking for a commercial glazier near you in {p['city']}? ACG is the licensed Florida commercial storefront glazing contractor (CGC #1531993) serving {p['city']}."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{p['lat']};{p['lng']}">
<meta name="geo.placename" content="{html_lib.escape(p['city'])}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{p['lat']}, {p['lng']}">
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
    full = os.path.join(OUT, p['slug'], "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{p['slug']}/")


if __name__ == "__main__":
    print("Building vertical x city pages...")
    for p in VC_PAGES:
        build_vc(p)
    print("\nBuilding permit timeline by county...")
    build_permit_timeline()
    print("\nBuilding author bios...")
    build_author_pages()
    print("\nBuilding near-me pages...")
    for p in NEAR_ME:
        build_near_me(p)
    total = len(VC_PAGES) + 1 + 2 + len(NEAR_ME)
    print(f"\nTotal wave 3 pages: {total}")
