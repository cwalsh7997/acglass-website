#!/usr/bin/env python3
"""Wave 13 — Tennessee depth ahead of Q3 2026 Nashville office opening.
- TN master commercial glazing hub
- 4 TN city × vertical (Nashville healthcare, Nashville multifamily, Franklin hotel, Memphis restaurant)
- 6 Nashville neighborhood pages not yet built
- 4 TN AIO FAQ
- 2 Knoxville + Chattanooga deeper city content

Total: 17 pages. Brand-audited claims only.
"""
import os, html as html_lib, json

OUT = "/home/user/workspace/acglass-website"

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '<link rel="stylesheet" href="/css/style.css?v=1777031720"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG - American Commercial Glass" class="logo-img" loading="lazy"></a>
<div class="nav-links"><a href="/index.html">Home</a><a href="/blog.html">Blog</a><a href="/case-studies/">Case Studies</a><a href="/resources/">Resources</a><a href="/send-plans.html" class="nav-cta">Send Us Plans</a></div></div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Services</h4><ul><li><a href="/folding-glass-walls-florida/">Folding Glass Walls</a></li><li><a href="/multi-slide-doors-florida/">Multi-Slide Doors</a></li><li><a href="/curtainwall-installation.html">Curtain Wall</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Glossary &amp; FAQ</a></li><li><a href="/tools/">Free Tools</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

LOCALBIZ = '''{"@context":"https://schema.org","@type":"GeneralContractor","@id":"https://acglass.com/#org","name":"American Commercial Glass","url":"https://acglass.com","telephone":"+1-772-486-7711","email":"info@acglass.com","address":{"@type":"PostalAddress","streetAddress":"1601 N Flagler Dr Ste 100","addressLocality":"West Palm Beach","addressRegion":"FL","postalCode":"33401","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":26.7153,"longitude":-80.0534},"areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"Tennessee"}]}'''


def page(title, description, body_html, slug, extra_schema=None, breadcrumb=None, faq=None):
    bc_json = ""
    if breadcrumb:
        items = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(breadcrumb)]
        bc_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    faq_json = ""
    if faq:
        faq_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    extra = ',\n' + extra_schema if extra_schema else ""
    speakable_block = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"}) + '</script>'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="https://acglass.com/{slug}/">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="https://acglass.com/{slug}/">
<meta property="og:type" content="website">
{FONTS}
{GTAG}
<script type="application/ld+json">
[
{LOCALBIZ}{extra}{bc_json}{faq_json}
]
</script>
{speakable_block}
</head>
<body>
{NAV}
<main class="page-main" style="padding-top:100px;">
<div class="container" style="max-width:980px;padding:60px 24px 100px;">
{body_html}
</div>
</main>
{FOOTER}
</body></html>'''
    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)


def build_tn_hub():
    title = "Tennessee Commercial Glazing \u2014 ACG | Nashville, Franklin, Memphis, Knoxville, Chattanooga"
    desc = "ACG Tennessee commercial glazing \u2014 Nashville Q3 2026 office opening. Storefronts, curtain wall, impact-rated assemblies. Commercial scopes across Davidson, Williamson, Shelby, Knox, Hamilton counties."
    body = '''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Tennessee Commercial Glazing</p>
<h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">Tennessee Commercial Glazing</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG is opening a Nashville office in Q3 2026 to serve Tennessee commercial glazing scopes \u2014 Nashville, Franklin, Brentwood, Memphis, Knoxville, and Chattanooga. Storefronts, curtain wall, punched windows, all-glass entrances, balcony rails. Florida CGC #1531993; Tennessee commercial general contractor credential in progress.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:28px;color:#050a12;margin-bottom:16px;">Tennessee submarkets we cover</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 <a href="/nashville/" style="color:#0e284f;text-decoration:underline;">Nashville</a> \u2014 downtown, Gulch, SoBro, East Nashville, Music Row, West End</li>
<li>\u2713 <a href="/franklin-tn/" style="color:#0e284f;text-decoration:underline;">Franklin</a> \u2014 Cool Springs, downtown Franklin, Westhaven</li>
<li>\u2713 <a href="/brentwood-tn/" style="color:#0e284f;text-decoration:underline;">Brentwood</a> \u2014 Maryland Farms commercial corridor</li>
<li>\u2713 <a href="/memphis/" style="color:#0e284f;text-decoration:underline;">Memphis</a> \u2014 downtown, East Memphis Poplar, Midtown</li>
<li>\u2713 <a href="/knoxville/" style="color:#0e284f;text-decoration:underline;">Knoxville</a> \u2014 downtown, Turkey Creek, West Knoxville</li>
<li>\u2713 <a href="/chattanooga/" style="color:#0e284f;text-decoration:underline;">Chattanooga</a> \u2014 downtown and Northshore</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Tennessee commercial glazing differences from Florida</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">Tennessee follows IBC 2018 with TN-specific amendments. No HVHZ requirement; no FBC 1626 impact-rated assembly mandate. Wind pressure calculations per ASCE 7-22 with TN-specific basic wind speed (typically 115 mph for most commercial). Result: 10-20% lower per-square-foot commercial glazing cost vs Florida HVHZ markets. Read our detailed comparison: <a href="/commercial-glazing-cost-florida-vs-tennessee/" style="color:#0e284f;text-decoration:underline;">Florida vs Tennessee commercial glazing cost</a>.</p>
</section>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why bid ACG on Tennessee commercial glazing</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;padding-left:20px;">
<li>48-hour bid turnaround on complete RFQ packages</li>
<li>$6M aggregate bonding capacity</li>
<li>350+ commercial projects completed (Florida portfolio)</li>
<li>Direct manufacturer relationships with Kawneer, YKK AP, Tubelite, Euro-Wall</li>
<li>Zero OSHA recordable incidents since 2021</li>
<li>FL CGC #1531993 \u2014 TN commercial general contractor credential in progress for Q3 2026 office</li>
</ul>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Tennessee commercial glazing bid \u2014 48 hours on complete plans</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
    page(title, desc, body, "tennessee-commercial-glazing",
         breadcrumb=[("Home","https://acglass.com/"),("Tennessee Commercial Glazing", "https://acglass.com/tennessee-commercial-glazing/")])


# Nashville x vertical pages
NASHVILLE_VERTICALS = [
    ("healthcare","Healthcare","Nashville's hospital cluster includes Vanderbilt University Medical Center, HCA TriStar, Saint Thomas, and Vanderbilt Children's. Commercial glazing scopes include hospital exterior curtain wall, medical office building punched windows, fire-rated corridor glazing, ICRA-compliant phased install on occupied facilities."),
    ("multifamily","Multifamily","Nashville multifamily construction is concentrated in the Gulch, SoBro, East Nashville, and West End. Commercial glazing scopes include ground-floor amenity storefront, building exterior punched windows, balcony glass railings, folding glass walls at amenity decks, full-height curtain wall lobbies."),
    ("hotel","Hotel","Nashville hospitality development continues across downtown, SoBro, and the Gulch. Commercial glazing scopes include curtain wall, balcony glass railings, all-glass entrance doors, folding glass walls at restaurant and rooftop bar, impact-resistant assemblies where TN code requires."),
    ("restaurant","Restaurant","Nashville restaurant glazing concentrates in Germantown, East Nashville, the Gulch, and 12 South. Folding glass walls (Euro-Wall, NanaWall), large-format storefronts, all-glass entrance doors, indoor-outdoor dining patio enclosures."),
]


def build_nashville_verticals():
    for vert_slug, vert_name, intent in NASHVILLE_VERTICALS:
        slug = f"{vert_slug}-glazing-nashville"
        title = f"{vert_name} Commercial Glazing Nashville, TN \u2014 ACG"
        desc = f"{vert_name} commercial glazing in Nashville, Tennessee. ACG Nashville office opens Q3 2026. {intent[:100]}..."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">{vert_name} Commercial Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">{vert_name} Commercial Glazing in Nashville, Tennessee</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">{intent}</p></header>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why Nashville {vert_name.lower()} clients bid ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">48-hour bid turnaround on complete RFQ packages. $6M aggregate bonding qualifies us for Nashville {vert_name.lower()} commercial scopes to $2M+. Direct manufacturer relationships shorten material lead time. 350+ commercial projects in Florida portfolio. Nashville office opens Q3 2026; bid coordination and project supervision running from West Palm Beach until then.</p>
</section>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Tennessee code differences from Florida</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">Tennessee follows IBC 2018 with TN-specific amendments. Nashville commercial glazing wind pressure per ASCE 7-22 with TN-specific basic wind speed (typically 115 mph). No HVHZ. No FBC 1626 impact-rated assembly requirement. Net: typically 10-20% lower per-square-foot commercial glazing cost vs Florida HVHZ markets.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:28px;margin-bottom:16px;">Nashville {vert_name.lower()} glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
        service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":f"{vert_name} Commercial Glazing in Nashville, TN","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"City","name":"Nashville","containedInPlace":{"@type":"State","name":"Tennessee"}},"serviceType":f"{vert_name} Commercial Glazing"})
        page(title, desc, body, slug,
             extra_schema=service_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Tennessee","https://acglass.com/tennessee-commercial-glazing/"),(f"Nashville {vert_name}", f"https://acglass.com/{slug}/")])


# Nashville neighborhoods not yet built
NASHVILLE_NEIGHBORHOODS = [
    ("Music Row", "music-row-nashville", "Nashville's Music Row hosts record labels, publishing houses, recording studios, and the music industry support cluster. Commercial glazing includes office building storefronts, recording studio sound-attenuating glazing, and mixed-use development facades."),
    ("West End", "west-end-nashville", "Nashville West End runs from Vanderbilt University into Belle Meade. Commercial glazing includes office tower curtain wall, medical office punched windows, university-adjacent retail storefronts."),
    ("Germantown", "germantown-nashville", "Germantown is one of Nashville's oldest neighborhoods turned restaurant and brewery district. Commercial glazing includes folding glass walls at restaurants, mixed-use mid-rise curtain wall, brewery storefronts."),
    ("12 South", "twelve-south-nashville", "12 South is Nashville's compact retail and restaurant strip with mixed-use development pressure. Commercial glazing includes retail storefronts, restaurant folding glass walls, mixed-use mid-rise curtain wall."),
    ("Wedgewood-Houston", "wedgewood-houston-nashville", "Wedgewood-Houston (\"WeHo\") is south Nashville's industrial-to-creative conversion district. Commercial glazing includes adaptive-reuse curtain wall, brewery and distillery storefronts, art gallery glazing."),
    ("Donelson", "donelson-nashville", "Donelson is east Nashville near BNA airport, a commercial corridor for hotel, hospitality, and aviation-adjacent industry. Commercial glazing includes hotel curtain wall, conference space storefronts, and impact-resistant facades for airport-area buildings."),
]


def build_nashville_neighborhoods():
    for nbhd_name, slug, intent in NASHVILLE_NEIGHBORHOODS:
        full_slug = f"nashville/{slug}"
        title = f"Commercial Glazier {nbhd_name}, Nashville TN \u2014 ACG"
        desc = f"Commercial glazing in {nbhd_name}, Nashville. ACG Nashville office opens Q3 2026. Storefronts, curtain wall, restaurant folding walls, mixed-use facade glazing."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">{nbhd_name} Commercial Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">Commercial Glazier in {nbhd_name}, Nashville</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">{intent}</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">{nbhd_name} commercial glazing scopes</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Commercial storefront aluminum systems (Kawneer Trifab VG 451, YKK AP YES 45 IG)</li>
<li>\u2713 Curtain wall and full-height architectural glazing</li>
<li>\u2713 Folding glass walls and multi-slide doors (Euro-Wall, NanaWall)</li>
<li>\u2713 All-glass entrance doors with structural patch fittings</li>
<li>\u2713 Balcony glass railings (laminated SGP)</li>
<li>\u2713 Impact-resistant punched windows where TN code or owner spec requires</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {nbhd_name} clients bid ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">48-hour bid turnaround on complete RFQ packages. $6M aggregate bonding capacity. 350+ commercial projects across Florida. Direct manufacturer relationships with Kawneer, YKK AP, Tubelite, Euro-Wall. Zero OSHA recordable incidents since 2021. FL CGC #1531993 with TN commercial general contractor credential in progress for Q3 2026 Nashville office opening.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">{nbhd_name} commercial glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
        page(title, desc, body, full_slug,
             breadcrumb=[("Home","https://acglass.com/"),("Nashville","https://acglass.com/nashville/"),(nbhd_name, f"https://acglass.com/{full_slug}/")])


# TN AIO FAQ
TN_FAQ = [
    ("does-tennessee-require-impact-rated-glass", "Does Tennessee require impact-rated commercial glass?",
     "Tennessee does not require impact-rated commercial glass at the state code level. Tennessee follows IBC 2018 with state-specific amendments. Wind pressure design is per ASCE 7-22, but no HVHZ designation and no FBC 1626 impact-rated assembly requirement applies. Owner-specified upgrade to impact-resistant glass remains optional.",
     [
       ("Is any Tennessee region wind-zone designated?", "Tennessee does not have HVHZ-equivalent wind zones. Memphis (West TN) sits in a higher seismic zone (per the New Madrid Seismic Zone), which affects structural design but not glass impact rating. Nashville and East TN are lower seismic risk."),
       ("Do Tennessee owners ever spec impact glass voluntarily?", "Yes \u2014 owner-specified for higher-end commercial (hospitality, healthcare, government) and for buildings where the owner prioritizes long-term durability and storm performance. Voluntary impact-glass spec typically adds 8-15% to the glass line item."),
       ("Can ACG install impact-rated commercial glass in Tennessee?", "Yes. ACG carries direct relationships with impact-glass manufacturers (Solarban laminated, Viracon laminated, SentryGlas Plus interlayer) and installs impact-rated assemblies in Tennessee on owner-specified scopes.")
     ]),
    ("nashville-commercial-glazing-cost-2026", "How much does commercial glazing cost in Nashville in 2026?",
     "Nashville 2026 commercial glazing per-square-foot installed cost runs: storefront aluminum $80-130/sq ft installed (non-impact), curtain wall $115-195/sq ft installed (non-impact), punched windows $70-140/sq ft installed. Owner-specified impact-rated assemblies add 8-15%.",
     [
       ("Why is Nashville commercial glazing cheaper than Florida HVHZ?", "No HVHZ Product Approval requirement, no FBC 1626 impact-rated assembly mandate, lower glass-thickness and interlayer requirements at code level. Net: 10-20% lower per-square-foot vs Florida HVHZ markets for the same aluminum system and glass package."),
       ("Is Nashville commercial labor cheaper than Florida?", "Nashville commercial glazier labor is roughly comparable to Tampa/Orlando/Jacksonville and slightly below Miami/Broward/Palm Beach. The TN market labor differential vs FL is typically within 5% on the labor line item."),
       ("What's the right Nashville commercial glazing bid range to expect?", "For a typical 5,000 sq ft Nashville commercial storefront scope: $400K-650K all-in (non-impact). For a 10,000 sq ft mid-rise curtain wall scope: $1.15M-1.95M all-in. Specific scope, glass package, finish, and schedule drive bid range.")
     ]),
    ("acg-nashville-office-opening", "When does ACG Nashville office open and what scopes does it cover?",
     "ACG Nashville office opens Q3 2026. The office serves Tennessee commercial glazing scopes \u2014 Nashville, Franklin, Brentwood, Memphis, Knoxville, and Chattanooga. Bid coordination and project supervision currently run from West Palm Beach with Tennessee crew partners; office opening transitions field operations to in-state.",
     [
       ("Can ACG bid Tennessee scopes today?", "Yes. We are actively bidding Tennessee commercial glazing scopes ahead of office opening. Bid response standard remains 48 hours on complete RFQ packages. Project supervision and submittal coordination from West Palm Beach during the transition."),
       ("What's the Q3 2026 Nashville office address?", "Address to be announced at office opening. Currently in lease negotiation for Nashville office space. Project mailing and bid submittal route through info@acglass.com until office is staffed."),
       ("Will ACG keep Florida coverage after Nashville opens?", "Yes. Florida remains ACG's primary market. Nashville expansion adds Tennessee coverage without reducing Florida capacity. West Palm Beach headquarters, Naples office, and Tampa coverage continue unchanged.")
     ]),
    ("tennessee-commercial-glazier-license-requirements", "What license does a Tennessee commercial glazier need?",
     "Tennessee commercial glazing scopes over $25K require a Tennessee Contractor's License (BC \u2014 General Building, or BC-A \u2014 Industrial / Commercial). The Tennessee Board for Licensing Contractors administers credentials. ACG holds Florida CGC #1531993 and has the Tennessee commercial general contractor credential application in progress for Q3 2026 office opening.",
     [
       ("What scope size triggers the Tennessee Contractor's License requirement?", "Commercial projects above $25,000 require a Tennessee Contractor's License at the prime contractor level. Subcontractors on bid-listed scopes above $25,000 also require licensing for the trade. Below $25,000 \u2014 limited license category applies."),
       ("Can a Florida-licensed contractor bid Tennessee work?", "Yes, with proper Tennessee licensure. Many southeastern commercial contractors hold licenses in multiple states. ACG's Tennessee credential application is in progress for the Q3 2026 office opening."),
       ("How does ACG ensure compliance during the transition period?", "Bid coordination and project supervision from West Palm Beach with Tennessee licensed crew partners until the Nashville office is staffed and the TN credential is issued. All bids include licensure-pathway documentation up front so GCs and owners know the compliance framework.")
     ])
]


def build_tn_faq():
    for slug, q, intro, faq in TN_FAQ:
        title = f"{q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Tennessee Commercial Glazing FAQ</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for qq, aa in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(qq)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(aa)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Send us drawings \u2014 48-hour bid</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        page(title, intro, body, slug,
             breadcrumb=[("Home","https://acglass.com/"),("Tennessee","https://acglass.com/tennessee-commercial-glazing/"),(q, f"https://acglass.com/{slug}/")],
             faq=faq)


if __name__ == "__main__":
    print("Wave 13 \u2014 Tennessee depth")
    build_tn_hub()
    print("  TN hub built")
    build_nashville_verticals()
    print(f"  {len(NASHVILLE_VERTICALS)} Nashville x vertical pages")
    build_nashville_neighborhoods()
    print(f"  {len(NASHVILLE_NEIGHBORHOODS)} Nashville neighborhood pages")
    build_tn_faq()
    print(f"  {len(TN_FAQ)} TN AIO FAQ pages")
    total = 1 + len(NASHVILLE_VERTICALS) + len(NASHVILLE_NEIGHBORHOODS) + len(TN_FAQ)
    print(f"\nWave 13 total: {total}")
