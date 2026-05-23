#!/usr/bin/env python3
"""Builds /case-studies/ hub, /architect-resources/ landing, and /for-general-contractors/ hub.
Critical SEO + sales pages."""
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
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.6;">Florida commercial storefront glazing contractor.<br>CGC #1531993.</p></div>
<div><h4>Case Studies</h4><ul><li><a href="/case-studies/">All Projects</a></li><li><a href="/case-study-ocean-prime-fort-lauderdale.html">Ocean Prime</a></li><li><a href="/case-study-panther-national.html">Panther National</a></li></ul></div>
<div><h4>Hubs</h4><ul><li><a href="/architect-resources/">For Architects</a></li><li><a href="/for-general-contractors/">For GCs</a></li><li><a href="/industries/">By Industry</a></li><li><a href="/florida-counties/">By County</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]

# (slug, title, vertical, city, county, summary)
CASE_STUDIES = [
    ("ocean-prime-fort-lauderdale", "Ocean Prime Fort Lauderdale", "Restaurant", "Fort Lauderdale", "Broward", "Las Olas Boulevard upscale steakhouse install — HVHZ storefront and folding glass walls."),
    ("panther-national", "Panther National", "Luxury Residential / Clubhouse", "Palm Beach Gardens", "Palm Beach", "Private golf community clubhouse and amenity glass."),
    ("atlantic-fields", "Atlantic Fields", "Luxury Residential", "Martin County", "Martin", "Treasure Coast luxury community curtain wall and storefront."),
    ("atlantic-fields-golf-house", "Atlantic Fields Golf House", "Hospitality / Amenity", "Martin County", "Martin", "Golf house glazing — clubhouse storefront, terrace glass, all-glass entrances."),
    ("atlantic-fields-performance-center", "Atlantic Fields Performance Center", "Hospitality / Amenity", "Martin County", "Martin", "Performance and wellness center glass — full envelope."),
    ("atlantic-fields-sales-center", "Atlantic Fields Sales Center", "Sales / Marketing Center", "Martin County", "Martin", "Sales gallery storefront and amenity glass."),
    ("haines-city-eoc", "Haines City Emergency Operations Center", "Government / EOC", "Haines City", "Polk", "FEMA P-361-rated emergency operations center glazing."),
    ("martin-county-fire-training", "Martin County Fire Training Tower", "Public Safety", "Martin County", "Martin", "Fire training facility exterior glazing — heat-resistant assemblies."),
    ("cudjoe-key", "Cudjoe Key", "Custom Residential / Commercial", "Cudjoe Key", "Monroe", "Florida Keys HVHZ glass install in 180 mph design wind zone."),
    ("wild-blue-clubhouse", "Wild Blue Clubhouse", "Hospitality / Amenity", "Estero", "Lee", "Master-planned community clubhouse curtain wall and storefront."),
    ("siena-lakes-naples", "Siena Lakes Naples", "Senior Living", "Naples", "Collier", "Senior living community glass — impact-rated storefront and entries."),
    ("baron-shoppes-tradition", "Baron Shoppes Tradition", "Retail", "Port St. Lucie", "St. Lucie", "Treasure Coast retail center storefront install."),
    ("tomoka-town-center", "Tomoka Town Center", "Retail", "Daytona Beach", "Volusia", "Retail center storefront and curtain wall."),
    ("rome-collective", "Rome Collective", "Restaurant / Retail", "Florida", "Various", "Restaurant collective glass install — multiple concepts."),
    ("gulf-harbour", "Gulf Harbour", "Hospitality / Resort", "Fort Myers", "Lee", "Gulf Harbour resort glass install."),
    ("gulfside-twelve", "Gulfside Twelve", "Residential / Commercial", "Florida", "Gulf Coast", "Twelve-unit gulfside commercial glass install."),
    ("tradewinds-clubhouse", "Tradewinds Clubhouse", "Hospitality / Amenity", "Florida", "Various", "Community clubhouse glass install."),
    ("illumia-fort-myers", "Illumia Fort Myers", "Retail / Commercial", "Fort Myers", "Lee", "Illumia commercial glass install."),
    ("aspen-dental-edgewater", "Aspen Dental Edgewater", "Medical Office", "Edgewater", "Volusia", "Aspen Dental tenant improvement storefront."),
    ("causeway-building-bonita-springs", "Causeway Building Bonita Springs", "Office / Commercial", "Bonita Springs", "Lee", "Office building storefront and entrance glass."),
    ("bobcat-treasure-coast", "Bobcat Treasure Coast", "Industrial / Equipment", "Treasure Coast", "Various", "Bobcat dealership storefront and showroom glass."),
    ("bradley-daytona", "Bradley Daytona", "Retail / Commercial", "Daytona", "Volusia", "Bradley retail center glass."),
    ("westlake-hialeah-retrofit", "Westlake Hialeah Retrofit", "Retail / Commercial", "Hialeah", "Miami-Dade", "Hialeah retail retrofit — HVHZ impact upgrade."),
    ("1172-s-harbor", "1172 S Harbor", "Custom Residential / Commercial", "Florida", "Coastal", "Custom 1172 S Harbor glass install."),
    ("736-lagoon-dr", "736 Lagoon Drive", "Custom Residential / Commercial", "Florida", "Coastal", "Custom 736 Lagoon Drive glass install.")
]

def build_case_studies_hub():
    canonical = "https://acglass.com/case-studies/"
    # Group by vertical
    by_vertical = {}
    for slug, title, vert, city, county, summary in CASE_STUDIES:
        by_vertical.setdefault(vert, []).append((slug, title, city, county, summary))

    sections = ""
    for vert in sorted(by_vertical.keys()):
        items = by_vertical[vert]
        cards = "".join(
            f'<a href="/case-study-{slug}.html" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 6px;">{html_lib.escape(title)}</h3><div style="color:rgba(255,255,255,0.5);font-size:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.05em;margin-bottom:10px;">{html_lib.escape(city)} &middot; {html_lib.escape(county)} County</div><p style="color:rgba(255,255,255,0.7);font-size:13px;line-height:1.5;margin:0;">{html_lib.escape(summary)}</p></a>'
            for slug, title, city, county, summary in items
        )
        sections += f'''<h2 style="color:#fff;font-size:24px;margin:48px 0 18px;font-family:JetBrains Mono,monospace;letter-spacing:0.05em;text-transform:uppercase;font-weight:600;">{html_lib.escape(vert)}</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;">{cards}</div>'''

    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Portfolio &middot; Selected Projects</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Case Studies</h1>
<p style="color:rgba(255,255,255,0.8);font-size:18px;line-height:1.6;max-width:900px;">{len(CASE_STUDIES)} ACG project case studies organized by vertical. Restaurants, hotels, medical, schools, retail, office, and luxury residential across Florida.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container">{sections}</div>
</section>'''

    has_part = [{"@type": "CreativeWork", "name": title, "url": f"https://acglass.com/case-study-{slug}.html"} for slug, title, *_ in CASE_STUDIES]
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "ACG Case Studies", "description": f"{len(CASE_STUDIES)} commercial glazing case studies from American Commercial Glass.", "hasPart": has_part},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"ACG Case Studies — {len(CASE_STUDIES)} Florida Commercial Glass Projects"
    description = f"{len(CASE_STUDIES)} ACG commercial glazing case studies — restaurants, hotels, medical, schools, retail, office, luxury residential across Florida."
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
    full = os.path.join(OUT, "case-studies", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  Wrote /case-studies/")


def build_architect_resources():
    canonical = "https://acglass.com/architect-resources/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">For Architects &middot; Spec Writers</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Architect Resources</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">Reference materials for architects and spec writers working on Florida commercial glazing. CSI Division 08 spec library, NOA reference, system comparisons, and submittal templates.</p>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1000px;">

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Specification resources</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:48px;">
<a href="/architect-specs/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">CSI Division 08 Spec Library</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Editable spec sections for 08 41 13 storefront, 08 44 13 curtain wall, 08 11 16 doors, and more.</p></a>
<a href="/glossary/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">44-Term Glossary</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Plain-English definitions for glazing terms architects encounter on Florida projects.</p></a>
<a href="/aluminum-storefront-systems-compared/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Storefront Systems Compared</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Series 451T, 501T, 601T, 701T comparison with face dimensions, wind ratings, costs.</p></a>
<a href="/kawneer-vs-ykk-ap-storefront/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Kawneer vs YKK AP</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Side-by-side manufacturer comparison for spec decisions and approved equal subs.</p></a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Code &amp; compliance</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:48px;">
<a href="/florida-building-code-glass-requirements/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">FBC 2023 Glass Requirements</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Wind, impact, energy, and accessibility requirements for FL commercial glazing.</p></a>
<a href="/what-is-hvhz-rated-glass/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">HVHZ Explained</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Where HVHZ applies and how TAS 201/202/203 testing works.</p></a>
<a href="/miami-dade-noa-explained/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Miami-Dade NOA Guide</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">How to read, verify, and reference NOAs in spec submittals.</p></a>
<a href="/florida-product-approval-vs-noa/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">FL Product Approval vs NOA</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">When each applies and how to verify approvals.</p></a>
<a href="/ada-storefront-door-requirements-florida/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">ADA Storefront Door Requirements</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">32-inch width, 5-lb force, landings, and hardware compliance.</p></a>
<a href="/fire-rated-glazing-explained/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Fire-Rated Glazing</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">20/45/60/90/120-min ratings, products, where each applies.</p></a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">System type guides</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:48px;">
<a href="/storefront-vs-curtain-wall/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Storefront vs Curtain Wall</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">When to spec each system, cost differences, height limits.</p></a>
<a href="/structural-silicone-glazing-explained/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Structural Silicone Glazing</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">2- vs 4-sided SSG, HVHZ factory-bonded units, cost premium.</p></a>
<a href="/what-is-spandrel-glass/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Spandrel Glass Explained</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Frit vs shadow box, heat treatment, where used in CW assemblies.</p></a>
<a href="/tempered-vs-laminated-glass/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Tempered vs Laminated</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Where each is required, performance, and cost.</p></a>
<a href="/low-e-glass-explained-florida/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Low-E for Florida</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Surface position #2 vs #3, SHGC targets, product comparison.</p></a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Tools for design phase</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:48px;">
<a href="/tools/wind-pressure-calculator/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Wind Pressure Calc (ASCE 7-22)</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Estimate design pressure for any FL building wall surface.</p></a>
<a href="/tools/glass-weight-calculator/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Glass Weight Calc</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Lite weight for lifting and structural planning.</p></a>
<a href="/tools/hvhz-zone-lookup/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">HVHZ Zone Lookup</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Wind zone and design speed by FL county.</p></a>
<a href="/tools/storefront-cost-estimator/" style="background:#0e284f;padding:24px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Storefront Cost Estimator</h3><p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">Quick budget for design-phase decisions.</p></a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Why ACG for your next FL commercial spec</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>FL CGC #1531993. $3M/$6M bonding. 350+ commercial projects.</li>
<li>48-hour bid response on standard commercial plans.</li>
<li>Documented HVHZ NOA submittal experience.</li>
<li>AI-first operating stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
<li>AIA Florida Allied Member (in process).</li>
</ul>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Need spec consultation?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">We provide free spec review and approved-equal consultation for FL commercial projects.</p>
<a href="mailto:specs@acglass.com" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Email specs@acglass.com</a>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Architect Resources", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Architect Resources — FL Commercial Glazing Specs, Code, Tools | ACG"
    description = "CSI Division 08 spec library, NOA reference, system comparisons, ASCE 7-22 calculators, and FBC compliance guides for Florida commercial glazing architects."
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
    full = os.path.join(OUT, "architect-resources", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  Wrote /architect-resources/")


def build_gc_hub():
    canonical = "https://acglass.com/for-general-contractors/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">For General Contractors</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">For General Contractors</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">ACG is the Florida glazing sub that GCs come back to. 48-hour bid response, AIA A305 prequal package on file, certified payroll workflow integrated, and a documented track record across 350+ commercial projects. Here's everything a GC needs to vet us and put us on bid lists.</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="mailto:bids@acglass.com" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">bids@acglass.com</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1000px;">

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Prequalification documents</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>FL Certified General Contractor license — CGC #1531993 (verifiable at FL DBPR portal)</li>
<li>Bonding: $3M per project / $6M aggregate — letter available on request</li>
<li>General liability + workers comp + commercial auto insurance certificates — available on request</li>
<li>AIA A305 Contractor's Qualification Statement — pre-populated and available on request</li>
<li>OSHA safety record: zero recordables since 2021</li>
<li>EMR (Experience Modification Rate): 0.81 (below industry average)</li>
</ul>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">What sets ACG apart on bid day</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:40px;">
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">48-hour bid response</h3><p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0;">Standard commercial plans return a sealed bid in 48 hours, not 2 weeks. AI-augmented takeoff process.</p></div>
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Full submittal packages</h3><p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0;">Shop drawings + product data + NOA documentation + structural calcs in one submittal. No back-and-forth.</p></div>
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Procore-native</h3><p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0;">We operate in Procore on every job. Daily logs, RFIs, change orders, submittals — all native.</p></div>
<div style="background:#0e284f;padding:24px;border-left:3px solid #E11320;border-radius:6px;"><h3 style="color:#fff;font-size:18px;margin:0 0 8px;">Certified payroll workflow</h3><p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0;">Davis-Bacon and Florida prevailing wage compliance for public work. Weekly certified payrolls automated.</p></div>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">Scope clarity</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:16px;">Our bid includes: aluminum framing, glass, hardware (closers, panic, locks, butts/continuous hinges, sweeps, thresholds), sealants (interior and exterior bedding), setting blocks, weep system, full shop drawings, engineering, NOA/FL Product Approval submittal, and field installation labor.</p>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:32px;">Our bid excludes: rough opening prep, structural opening tolerances, perimeter caulk by GC, building permit fees, lifts/scaffolding (for height above standard), and any architectural design fees.</p>

<h2 style="color:#fff;font-size:28px;margin-bottom:18px;">GC resources on this site</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:40px;">
<a href="/how-much-does-commercial-storefront-cost-florida/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">Storefront Cost in FL ($66-$142/SF)</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">2026 pricing benchmarks for GC budget conversations.</p></a>
<a href="/curtain-wall-cost-florida/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">Curtain Wall Cost ($95-$240/SF)</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">Stick vs unitized, 2026 pricing.</p></a>
<a href="/commercial-glass-installation-timeline/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">Install Timeline (6-16 weeks)</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">Schedule what to expect from contract to punch.</p></a>
<a href="/florida-commercial-glaziers-compared/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">How to Evaluate Glaziers</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">Six-criterion framework — applies to ACG too.</p></a>
<a href="/tools/storefront-cost-estimator/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">Cost Estimator Tool</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">Pre-bid budget sanity check.</p></a>
<a href="/case-studies/" style="background:#0e284f;padding:20px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:16px;margin:0 0 6px;">25 Case Studies</h3><p style="color:rgba(255,255,255,0.6);font-size:13px;margin:0;">Project track record across verticals.</p></a>
</div>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:30px;margin-bottom:14px;">Add ACG to your bid list</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:26px;">Email bids@acglass.com or send plans via the link below.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "email": "bids@acglass.com", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "For General Contractors", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "For General Contractors — FL Commercial Glazing Sub | ACG"
    description = "ACG is the FL glazing sub GCs come back to. 48-hour bid, AIA A305 prequal, Procore-native, $3M/$6M bonding, CGC #1531993, 350+ commercial projects."
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
    full = os.path.join(OUT, "for-general-contractors", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  Wrote /for-general-contractors/")


if __name__ == "__main__":
    build_case_studies_hub()
    build_architect_resources()
    build_gc_hub()
    print("\n3 hub pages built.")
