#!/usr/bin/env python3
"""ACG Neighborhood-level pages for top SEO cities.
Captures sub-city / neighborhood / corridor searches that AP Glazing can't reach.
Each neighborhood page is unique, ~600 words, schema-rich, links to parent city + relevant services."""
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
<div><h4>Top Cities</h4><ul><li><a href="/west-palm-beach/">West Palm Beach</a></li><li><a href="/miami/">Miami</a></li><li><a href="/fort-lauderdale/">Fort Lauderdale</a></li><li><a href="/naples/">Naples</a></li><li><a href="/tampa/">Tampa</a></li></ul></div>
<div><h4>Services</h4><ul><li><a href="/commercial-storefronts.html">Storefront</a></li><li><a href="/curtain-wall.html">Curtain Wall</a></li><li><a href="/impact-windows.html">Impact Windows</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">All Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = [
    "https://www.wikidata.org/wiki/Q139858578",
    "https://acglass.ai/",
    "https://www.linkedin.com/company/acglass",
    "https://network.procore.com/p/american-commercial-glass-west-palm-beach",
    "https://www.bbb.org/us/fl/west-palm-beach/profile/window-installation/american-commercial-glass-inc-0633-92045708"
]

NEIGHBORHOODS = [
    # (slug, neighborhood_name, parent_city_slug, parent_city_name, lat, lng, county, hvhz, blurb)
    ("worth-avenue-palm-beach", "Worth Avenue", "palm-beach", "Palm Beach", 26.7026, -80.0364, "Palm Beach", False,
        "Worth Avenue is the highest-end retail corridor in Florida. Hermes, Chanel, Tiffany, Cartier — every flagship brand on Worth has a custom storefront. We have installed glass on three Worth Avenue tenant improvements and one full storefront replacement. The Worth Avenue Association design review is famously strict — frame profile, glass color, sign reveal, and signage must all be coordinated."),
    ("clematis-street-west-palm-beach", "Clematis Street", "west-palm-beach", "West Palm Beach", 26.7142, -80.0532, "Palm Beach", False,
        "Clematis Street is downtown West Palm Beach's primary retail and restaurant corridor. CRA-driven facade improvement grants fund a steady stream of storefront work. We have installed on four Clematis Street tenant improvements and worked with West Palm Beach Downtown Development Authority on permit-track scheduling."),
    ("rosemary-square-west-palm-beach", "Rosemary Square", "west-palm-beach", "West Palm Beach", 26.7144, -80.0533, "Palm Beach", False,
        "Rosemary Square (formerly CityPlace) is West Palm Beach's mixed-use lifestyle center. The 2019-2024 redevelopment added new restaurant and retail in-line spaces, all requiring landlord-criteria storefront. Our office is on Rosemary — we have done several in-line storefronts here."),
    ("brickell-miami", "Brickell", "miami", "Miami", 25.7617, -80.1918, "Miami-Dade", True,
        "Brickell is Miami's financial district — high-rise office, mixed-use retail, and ground-floor restaurant on a HVHZ-driven envelope. Every storefront here needs Miami-Dade NOA and brand-coordinated finish. We have worked on Brickell ground-floor TI and high-rise tower base storefront."),
    ("wynwood-miami", "Wynwood", "miami", "Miami", 25.8014, -80.1995, "Miami-Dade", True,
        "Wynwood is Miami's art and design district — converted warehouses, ground-floor gallery and restaurant, and rapidly redeveloping ground-floor retail. HVHZ-rated storefront is the standard. We have installed several Wynwood ground-floor restaurant fronts."),
    ("design-district-miami", "Miami Design District", "miami", "Miami", 25.8131, -80.1942, "Miami-Dade", True,
        "The Miami Design District is the highest-end luxury retail district in Florida. Hermes, Dior, Bulgari, Prada, Cartier — every flagship has a custom storefront. Permitting goes through both Miami-Dade and Design District design review. Costs typically run 40-60% above standard HVHZ storefront."),
    ("las-olas-fort-lauderdale", "Las Olas Boulevard", "fort-lauderdale", "Fort Lauderdale", 26.1188, -80.1395, "Broward", True,
        "Las Olas is Fort Lauderdale's primary retail and restaurant boulevard. Mid-rise mixed-use plus ground-floor restaurant. Strict City of Fort Lauderdale design review on the corridor. We installed the Ocean Prime Fort Lauderdale storefront on Las Olas in 2024."),
    ("flagler-street-miami", "Downtown Flagler Street", "miami", "Miami", 25.7741, -80.1937, "Miami-Dade", True,
        "Flagler Street is Miami's downtown commercial spine — federal courthouse, jewelry district, and ground-floor commercial. Older buildings, lots of TI work. HVHZ-rated impact retrofit is the most common project type here."),
    ("fifth-avenue-naples", "Fifth Avenue South", "naples", "Naples", 26.1390, -81.7944, "Collier", False,
        "Fifth Avenue South is Naples' primary high-end retail and restaurant corridor. WBDR-rated assemblies required, but technically not HVHZ. City of Naples design review controls finish materials, sign band depth, and operable awning compatibility. We have done several Fifth Avenue restaurant fronts."),
    ("third-street-naples", "Third Street South", "naples", "Naples", 26.1248, -81.8044, "Collier", False,
        "Third Street South is Naples' historic upscale shopping district — Olde Naples charm, courtyard layouts, restored 1920s-era buildings. Sensitive design review. WBDR-rated glass required. The work here is detail-heavy and requires patience."),
    ("hyde-park-tampa", "Hyde Park Village", "tampa", "Tampa", 27.9385, -82.4682, "Hillsborough", False,
        "Hyde Park Village is Tampa's open-air upscale shopping center. WBDR coastal, not HVHZ. Brand-driven design criteria. We have worked on Hyde Park tenant improvement storefront and a freestanding pad-site restaurant."),
    ("water-street-tampa", "Water Street Tampa", "tampa", "Tampa", 27.9396, -82.4503, "Hillsborough", False,
        "Water Street Tampa is the new Vinik/Cascade master-planned mixed-use district. New construction storefront, curtain wall, and amenity-deck glass. WBDR coastal. Modern design criteria, large in-line spaces, high glass-to-frame ratio."),
    ("downtown-orlando", "Downtown Orlando", "orlando", "Orlando", 28.5384, -81.3789, "Orange", False,
        "Downtown Orlando is non-HVHZ inland Florida — standard FBC wind requirements. Ground-floor restaurant and retail TI, mid-rise office curtain wall, and government/courthouse work. Permits move faster than South Florida."),
    ("downtown-st-pete", "Downtown St. Petersburg", "st-petersburg", "St. Petersburg", 27.7676, -82.6403, "Pinellas", False,
        "Downtown St. Pete is rapidly redeveloping — Central Avenue retail and restaurant, EDGE District, and the Innovation District. WBDR coastal. Older buildings being adaptively reused into ground-floor retail."),
    ("sarasota-downtown-main-street", "Downtown Main Street Sarasota", "sarasota", "Sarasota", 27.3364, -82.5404, "Sarasota", False,
        "Sarasota's downtown Main Street is Florida's most walkable downtown core — restaurant, gallery, and boutique retail. WBDR coastal. City of Sarasota design review on the corridor. We have done multiple Main Street restaurant storefronts."),
]

def schema(canonical, name, lat, lng, county, parent_city, hvhz):
    return [
        {
            "@context": "https://schema.org",
            "@type": ["Organization", "LocalBusiness"],
            "@id": canonical + "#org",
            "name": "American Commercial Glass",
            "url": "https://acglass.com",
            "telephone": "+17724867711",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"},
            "sameAs": ORG_SAMEAS,
            "areaServed": {"@type": "Place", "name": f"{name}, {parent_city}, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier — {name}, {parent_city}",
            "serviceType": "Commercial Glazing",
            "areaServed": {"@type": "Place", "name": f"{name}, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}},
            "provider": {"@id": canonical + "#org"}
        }
    ]

def build_neighborhood(n):
    slug, name, parent_slug, parent_city, lat, lng, county, hvhz, blurb = n
    canonical = f"https://acglass.com/{parent_slug}/{slug}/"
    hvhz_text = "HVHZ — Miami-Dade NOA required" if hvhz else "Non-HVHZ — standard FBC or WBDR rules"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Neighborhood &middot; {html_lib.escape(parent_city)}, FL</div>
<h1 style="color:#fff;font-size:clamp(32px,5vw,56px);line-height:1.1;margin:0 0 24px;">Storefront Glazier — {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.65;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:20px;">What we install in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/{parent_slug}/commercial-storefronts/" style="color:#E11320;text-decoration:none;">Commercial storefront systems</a> — aluminum framing with glass, hardware, and code-rated assemblies</li>
<li><a href="/{parent_slug}/impact-windows-hurricane/" style="color:#E11320;text-decoration:none;">Impact-rated windows</a> — for restaurants, retail, and office TI</li>
<li><a href="/{parent_slug}/all-glass-entrances/" style="color:#E11320;text-decoration:none;">All-glass entrances</a> — frameless single and pair doors with continuous hinges</li>
<li><a href="/{parent_slug}/glass-railings/" style="color:#E11320;text-decoration:none;">Glass railings</a> — for balcony, terrace, and stair applications</li>
<li><a href="/curtain-wall.html" style="color:#E11320;text-decoration:none;">Curtain wall</a> — for multi-story projects above 14 feet</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:20px;">Permit and code context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;">{html_lib.escape(name)} is in {html_lib.escape(county)} County. Wind code category: <strong style="color:#fff;">{html_lib.escape(hvhz_text)}</strong>. The local AHJ permit submittal for commercial glazing follows Florida Building Code 2023 (8th Edition) with the additional jurisdictional design review applicable to this corridor or district. ACG prepares submittals to match the specific AHJ submittal format and tracks revisions until approval.</p>

<h2 style="color:#fff;font-size:26px;margin-top:40px;margin-bottom:20px;">Why work with ACG in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993, $3M/$6M bonding capacity, 350+ commercial projects completed.</li>
<li>48-hour bid turnaround on standard commercial glazing plans.</li>
<li>Documented experience with HVHZ NOA, WBDR ASTM, and local jurisdictional design reviews.</li>
<li>AI-first operations stack (Sub.ai, jobcost.ai, CFO Agent) — documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>
<li>Parent city resources: <a href="/{parent_slug}/" style="color:#E11320;">{html_lib.escape(parent_city)} commercial storefront services</a>.</li>
</ul>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(name)} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:26px;">Send us plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    bc = [
        ("Home", "https://acglass.com/"),
        (parent_city, f"https://acglass.com/{parent_slug}/"),
        (name, canonical)
    ]
    schemas = schema(canonical, name, lat, lng, county, parent_city, hvhz) + [
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name} — {parent_city}, FL | Commercial Windows & Doors | ACG"
    description = f"Commercial storefront glazing in {name}, {parent_city}, FL. ACG is Florida-licensed CGC #1531993 with 350+ commercial projects and 48-hour bid turnaround."
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
<meta name="geo.placename" content="{html_lib.escape(name)}, {html_lib.escape(parent_city)}, FL">
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
    full = os.path.join(OUT, parent_slug, slug, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{parent_slug}/{slug}/")

if __name__ == "__main__":
    for n in NEIGHBORHOODS:
        build_neighborhood(n)
    print(f"\n{len(NEIGHBORHOODS)} neighborhood pages built.")
