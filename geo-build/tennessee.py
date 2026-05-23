#!/usr/bin/env python3
"""Tennessee seed pages — for Q3 2026 ACG Nashville office launch.
Goal: indexed and ranking by launch date. AP Glazing has zero TN presence.

Tennessee context (key differences from Florida):
- NOT HVHZ. NOT WBDR. Standard wind code per IBC + Tennessee state amendments.
- Tornado-prone (not hurricane). Storm shelters per FEMA P-361 may apply.
- Different AHJ structure: state of TN building code + local municipal review.
- Different commercial market: Nashville/Brentwood/Franklin are booming; Memphis is industrial.
- Lower wind load = cheaper glass. ASCE 7-22 wind speed: 90-115 mph (Risk Cat II).
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
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.6;">Florida + Tennessee commercial storefront glazing.<br>CGC #1531993 (FL).</p></div>
<div><h4>Tennessee</h4><ul><li><a href="/tennessee/">Tennessee Hub</a></li><li><a href="/nashville/">Nashville</a></li><li><a href="/brentwood-tn/">Brentwood</a></li><li><a href="/franklin-tn/">Franklin</a></li></ul></div>
<div><h4>Florida</h4><ul><li><a href="/west-palm-beach/">West Palm Beach</a></li><li><a href="/miami/">Miami</a></li><li><a href="/tampa/">Tampa</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">All Resources</a></li><li><a href="/tools/">Free Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]

def schema(canonical, name, lat, lng, area_name):
    return [
        {
            "@context": "https://schema.org",
            "@type": ["Organization", "LocalBusiness"],
            "@id": canonical + "#org",
            "name": "American Commercial Glass",
            "url": "https://acglass.com",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "telephone": "+17724867711",
            "address": {"@type": "PostalAddress", "addressLocality": "Nashville", "addressRegion": "TN", "addressCountry": "US", "description": "Tennessee office opening Q3 2026"},
            "sameAs": ORG_SAMEAS,
            "areaServed": {"@type": "Place", "name": area_name, "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier — {name}",
            "serviceType": "Commercial Glazing",
            "areaServed": area_name,
            "provider": {"@id": canonical + "#org"}
        }
    ]

def page_wrap(title, description, canonical, body, schemas, breadcrumbs=None):
    if breadcrumbs:
        schemas = schemas + [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(breadcrumbs)]}]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{GTAG}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-TN">
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

def write_page(rel, html_content):
    full = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Wrote /{rel}")

# ============================================================
# Tennessee state hub
# ============================================================

def build_tennessee_hub():
    canonical = "https://acglass.com/tennessee/"
    body = '''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Tennessee &middot; Opening Q3 2026</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,60px);line-height:1.1;margin:0 0 24px;">Commercial Storefront Glazier — Tennessee</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">ACG is opening a Nashville office in Q3 2026 to serve Middle Tennessee commercial construction. Same operating playbook that built 350+ commercial projects across Florida — adapted for Tennessee code, climate, and contractor relationships.</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Tennessee Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1000px;">
<h2 style="color:#fff;font-size:30px;margin-bottom:24px;">Why ACG in Tennessee</h2>
<p style="color:rgba(255,255,255,0.85);font-size:17px;line-height:1.8;margin-bottom:20px;">Middle Tennessee construction is doing what South Florida did from 2018 to 2024: rapid commercial growth, high-end restaurant and retail in-fill, multi-family ground-floor commercial, and explosive office market. ACG has done all of that.</p>
<p style="color:rgba(255,255,255,0.85);font-size:17px;line-height:1.8;margin-bottom:32px;">We bring an AI-first operating stack (Sub.ai, jobcost.ai, CFO Agent) that lets a small Nashville office deliver bid response and shop-drawing speed that traditional regional glaziers can't match. Tennessee glass costs less than Florida (no HVHZ, no impact requirement), so the dollar value per linear foot of opening is lower — but the schedule pressure and finish expectations are identical.</p>

<h2 style="color:#fff;font-size:30px;margin-bottom:24px;">Markets we will serve</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-bottom:48px;">
<a href="/nashville/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Nashville</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Davidson County. Primary office.</p></a>
<a href="/brentwood-tn/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Brentwood</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Williamson County. Class-A office, retail.</p></a>
<a href="/franklin-tn/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Franklin</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Williamson County. Cool Springs, downtown.</p></a>
<a href="/murfreesboro-tn/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Murfreesboro</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Rutherford County. MTSU corridor.</p></a>
<a href="/hendersonville-tn/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Hendersonville</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Sumner County. North of Nashville.</p></a>
<a href="/cool-springs-tn/" style="background:#0e284f;padding:24px;border-left:3px solid #E11320;text-decoration:none;display:block;border-radius:6px;"><h3 style="color:#fff;font-size:20px;margin:0 0 6px;">Cool Springs</h3><p style="color:rgba(255,255,255,0.7);font-size:14px;margin:0;">Franklin/Brentwood corridor. Office, retail.</p></a>
</div>

<h2 style="color:#fff;font-size:30px;margin-bottom:24px;">Tennessee commercial glazing context</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li><strong style="color:#fff;">Wind code:</strong> Tennessee follows IBC + Tennessee state amendments. ASCE 7-22 design wind speeds: 90-115 mph Risk Category II in Middle Tennessee. Far below Florida HVHZ (170-180 mph).</li>
<li><strong style="color:#fff;">No impact-glass requirement:</strong> Tennessee does not require impact-rated glazing. This drops the per-SF glass cost roughly 18-30% below Florida HVHZ projects.</li>
<li><strong style="color:#fff;">Tornado considerations:</strong> Middle Tennessee is tornado-prone. FEMA P-361 storm shelters may apply on schools, EOCs, and select commercial. We do this work in Florida already.</li>
<li><strong style="color:#fff;">Energy code:</strong> Tennessee adopted IECC with state amendments. Climate Zone 4A (Middle TN) and 3A (Memphis area). Typical commercial fenestration target: U-factor ≤ 0.42, SHGC ≤ 0.40.</li>
<li><strong style="color:#fff;">AHJ structure:</strong> Tennessee permits are issued by individual municipalities (Nashville Metro Codes, Williamson County, etc.). State plumbing/electrical/mechanical inspectors are separate. We have mapped the AHJ network.</li>
</ul>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:30px;margin-bottom:14px;">Have a Tennessee commercial glazing project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">We are bidding Tennessee work now for Q3 2026 and beyond install dates.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    schemas = schema(canonical, "Tennessee", 36.1627, -86.7816, "Tennessee")
    bc = [("Home", "https://acglass.com/"), ("Tennessee", canonical)]
    html = page_wrap("Commercial Storefront Glazier Tennessee | Nashville Office Q3 2026 | ACG", "ACG opens Nashville office Q3 2026 to serve Middle Tennessee commercial glazing. 350+ Florida projects of operating experience. Commercial storefront, curtain wall, impact-rated.", canonical, body, schemas, bc)
    write_page("tennessee/index.html", html)

# ============================================================
# Nashville
# ============================================================

TN_CITIES = [
    ("nashville", "Nashville", "Davidson", 36.1627, -86.7816,
        "Nashville's commercial construction market is doing what Miami did in 2018-2022: explosive growth in mixed-use, office, restaurant, and ground-floor retail. The Gulch, SoBro, East Nashville, 12 South, and Germantown are all delivering new commercial buildings on aggressive schedules. ACG is opening a Nashville office in Q3 2026 to serve this market directly.",
        ["The Gulch", "SoBro", "East Nashville", "12 South", "Germantown", "Wedgewood-Houston", "Downtown / Broadway"]),
    ("brentwood-tn", "Brentwood", "Williamson", 36.0331, -86.7828,
        "Brentwood is the affluent suburban core of Williamson County — Class-A office buildings, high-end retail, and corporate headquarters concentrated along Maryland Way, Franklin Road, and Old Hickory Boulevard. The commercial glazing market here is sophisticated: brand-quality finishes, ADA-compliant entrances, and sustainability spec packages (LEED, WELL).",
        ["Maryland Farms", "Cool Springs (south)", "Old Hickory Blvd", "Brentwood Place"]),
    ("franklin-tn", "Franklin", "Williamson", 35.9251, -86.8688,
        "Franklin Tennessee combines a historic Main Street downtown with the explosive growth of Cool Springs. Both submarkets need storefront glazing — downtown for sensitive infill and adaptive reuse, Cool Springs for new-construction office and retail.",
        ["Downtown Main Street", "Cool Springs corridor", "McEwen", "Berry Farms"]),
    ("murfreesboro-tn", "Murfreesboro", "Rutherford", 35.8456, -86.3903,
        "Murfreesboro is one of Tennessee's fastest-growing cities and home to MTSU. Commercial growth concentrated on Medical Center Parkway, Old Fort Parkway, and the I-24 corridor. Office, medical, retail, and restaurant.",
        ["Medical Center Parkway", "MTSU corridor", "Old Fort Parkway", "Downtown Square"]),
    ("hendersonville-tn", "Hendersonville", "Sumner", 36.3048, -86.6200,
        "Hendersonville Tennessee sits north of Nashville on Old Hickory Lake — strong commercial growth along Indian Lake Boulevard and Highway 31E. Suburban retail, office, and lakeside hospitality.",
        ["Indian Lake Village", "Old Hickory Lake waterfront", "Highway 31E corridor"]),
    ("cool-springs-tn", "Cool Springs", "Williamson", 35.9678, -86.8133,
        "Cool Springs is the dense office/retail core spanning Brentwood and Franklin in Williamson County. Major office occupiers, healthcare campuses, retail, and a deep restaurant market. The commercial glazing market here is brand-driven and schedule-sensitive.",
        ["McEwen Drive corridor", "Mallory Lane", "Maryland Way (south end)", "Cool Springs Galleria area"])
]

def build_tn_city(slug, name, county, lat, lng, blurb, sub_areas):
    canonical = f"https://acglass.com/{slug}/"
    sub = "".join(f'<li>{html_lib.escape(a)}</li>' for a in sub_areas)
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
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Aluminum storefront — Series 451T, 501T, 601T, 701T or equivalent</li>
<li>Curtain wall — stick-built and unitized for multi-story commercial</li>
<li>Window wall — mid-rise office and multi-family ground-floor commercial</li>
<li>Insulated low-E glass — meeting Tennessee IECC energy code</li>
<li>All-glass entrances — frameless single and pair doors</li>
<li>Restaurant folding glass walls and multi-slide doors</li>
<li>Glass railings — for terraces, stairs, balconies</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Submarkets and corridors</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">{sub}</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Permit and code context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:16px;">{html_lib.escape(name)} is in {html_lib.escape(county)} County, Tennessee. Permits issue through the local municipal codes office. Wind code: ASCE 7-22 with Tennessee state amendments — design wind speeds 90-115 mph Risk Category II. Impact-rated glazing is not required by code.</p>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;">Energy code: IECC Climate Zone 4A. Typical commercial fenestration target: U-factor ≤ 0.42, SHGC ≤ 0.40. ACG carries Tennessee-rated low-E glass products and aluminum framing approved for the energy compliance path.</p>

<h2 style="color:#fff;font-size:26px;margin-top:36px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>350+ commercial projects executed in Florida — same playbook, applied to Tennessee.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>AI-first operating stack documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>
<li>$3M per project / $6M aggregate bonding capacity.</li>
<li>Nashville office opening Q3 2026 with permanent crew and project management.</li>
</ul>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Bidding {html_lib.escape(name)} commercial glazing now</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:26px;">Send plans for a 48-hour response. Q3 2026+ install dates available.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    schemas = schema(canonical, name, lat, lng, f"{name}, {county} County, TN")
    bc = [("Home", "https://acglass.com/"), ("Tennessee", "https://acglass.com/tennessee/"), (name, canonical)]
    title = f"Storefront Glazier {name} TN | Commercial Windows & Doors | ACG"
    description = f"Commercial storefront, curtain wall, and impact-rated glazing in {name}, {county} County, Tennessee. ACG opens Nashville office Q3 2026. 350+ Florida project track record."
    html = page_wrap(title, description, canonical, body, schemas, bc)
    write_page(f"{slug}/index.html", html)

if __name__ == "__main__":
    build_tennessee_hub()
    for c in TN_CITIES:
        build_tn_city(*c)
    print(f"\nTennessee: 1 hub + {len(TN_CITIES)} city pages = {len(TN_CITIES)+1} total.")
