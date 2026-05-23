#!/usr/bin/env python3
"""ACG SEO Sprint — May 23, 2026
Generates high-impact pages distinct from the 385 geo pages:
- 6 industry vertical pages (restaurant, hotel, medical, school, retail, office)
- 12 AIO-bait FAQ pages with FAQPage schema (Perplexity / ChatGPT / Google AIO citation bait)
- 5 calculator/tool pages
- 1 glossary page (40 terms)
- 1 stats hub page
- 1 Florida code/HVHZ resource page

Author: Connor Walsh / ACG
Style: storefront-first, no brand-specific identity, no banned phrases.
"""
import os, json, html as html_lib

OUT = "/home/user/workspace/acglass-website"

# ---------- shared chrome ----------

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">'''

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links">
<a href="/index.html">Home</a><a href="/portfolio.html">Portfolio</a><a href="/services.html">Services</a>
<a href="/about.html">About</a><a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
<button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.6;">Florida commercial storefront glazing contractor.<br>CGC #1531993 · $3M/$6M bonding · 350+ projects.</p></div>
<div><h4>Services</h4><ul><li><a href="/services.html">All Services</a></li><li><a href="/commercial-storefronts.html">Storefront</a></li><li><a href="/curtain-wall.html">Curtain Wall</a></li><li><a href="/impact-windows.html">Impact Windows</a></li></ul></div>
<div><h4>Industries</h4><ul><li><a href="/restaurant-glazier-florida/">Restaurants</a></li><li><a href="/hotel-glazing-contractor-florida/">Hotels</a></li><li><a href="/medical-office-glazier-florida/">Medical</a></li><li><a href="/school-glazier-florida/">Schools</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">All Resources</a></li><li><a href="/glossary/">Glossary</a></li><li><a href="/florida-building-code-glass/">FL Code</a></li><li><a href="/hvhz-explained/">HVHZ Explained</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">700 S Rosemary Ave Suite 204<br>West Palm Beach, FL 33401<br><a href="tel:+17724867711" style="color:#E11320;">(772) 486-7711</a><br><a href="mailto:info@acglass.com" style="color:#E11320;">info@acglass.com</a></p></div>
</div><div class="footer-bottom"><p>&copy; 2026 American Commercial Glass, Inc. CGC #1531993. All rights reserved.</p></div></div></footer>'''

ORG_SAMEAS = [
    "https://www.wikidata.org/wiki/Q139858578",
    "https://www.linkedin.com/company/acglass",
    "https://www.facebook.com/acommercialglass",
    "https://www.instagram.com/acglass.co",
    "https://network.procore.com/p/american-commercial-glass-west-palm-beach",
    "https://www.bbb.org/us/fl/west-palm-beach/profile/window-installation/american-commercial-glass-inc-0633-92045708",
    "https://downtobid.com/company/american-commercial-glass",
    "https://www.yelp.com/biz/american-commercial-glass-west-palm-beach",
    "https://www.buildzoom.com/contractor/american-commercial-glass-inc",
    "https://acglass.ai/"
]

def org_schema(page_url, page_name, description):
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "LocalBusiness"],
        "@id": page_url + "#org",
        "name": "American Commercial Glass",
        "alternateName": ["ACG", "American Commercial Glass Inc"],
        "url": "https://acglass.com",
        "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
        "telephone": "+17724867711",
        "email": "info@acglass.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "700 S Rosemary Ave Suite 204",
            "addressLocality": "West Palm Beach",
            "addressRegion": "FL",
            "postalCode": "33401",
            "addressCountry": "US"
        },
        "sameAs": ORG_SAMEAS,
        "areaServed": [
            {"@type": "State", "name": "Florida"},
            {"@type": "State", "name": "Tennessee"}
        ]
    }

def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ]
    }

def page_wrap(title, description, canonical, body, extra_schema=None, og_image=None, breadcrumbs=None):
    schemas = [org_schema(canonical, title, description)]
    if extra_schema:
        if isinstance(extra_schema, list):
            schemas.extend(extra_schema)
        else:
            schemas.append(extra_schema)
    if breadcrumbs:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i+1, "name": n, "item": u}
                for i, (n, u) in enumerate(breadcrumbs)
            ]
        })
    schema_blocks = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
        for s in schemas
    )
    og_img = og_image or "https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg"
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
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
{schema_blocks}
</head>
<body>
{NAV}
{body}
{FOOTER}
</body>
</html>
'''

def write_page(rel_path, html_content):
    full = os.path.join(OUT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Wrote /{rel_path}")

# ============================================================
# BATCH 1: Industry Vertical Pages (6)
# ============================================================

VERTICALS = [
    {
        "slug": "restaurant-glazier-florida",
        "h1": "Restaurant Storefront Glazier — Florida",
        "title": "Restaurant Storefront Glazier Florida | Folding Walls & Impact Glass | ACG",
        "description": "ACG installs restaurant storefronts, folding glass walls, and impact-rated entrances across Florida. 350+ commercial projects. CGC #1531993. 48-hour bid turnaround on plans.",
        "intro": "Restaurants live and die on natural light, indoor-outdoor flow, and storefront curb appeal. We have built the glass on more than two dozen Florida restaurants — full-service, fast-casual, and chef-driven concepts from Miami to Naples. We know what your build-out actually needs.",
        "pain_points": [
            ("Indoor-outdoor dining without permit problems", "Florida diners want open-air. Florida code wants impact-rated glazing in coastal counties. We design the folding-wall and slider package that gives you a fully retractable dining wall AND passes Miami-Dade NOA review on the first submittal."),
            ("Storefront entry that survives delivery dollies and Saturday-night crowds", "Restaurant entries get hammered. We spec aluminum storefront systems with reinforced thresholds, heavy-duty closers, and tempered glass that takes the abuse. We have re-installed entries for restaurants that burned through three glaziers in two years."),
            ("Speed when your buildout is on the critical path", "Most restaurants run on borrowed time — equipment is on order, the GM is hired, the soft open is on the calendar. We deliver bids in 48 hours and run installs on tight CO-driven schedules. We have closed out restaurant glass in 5 working days when the schedule demanded it."),
            ("Hurricane shutters vs. impact glass — what your concept really needs", "Shutters are cheap and ugly. Impact glass is more expensive and invisible. For most restaurant operators, impact glass pays back in two ways: insurance and how the space feels when the sun comes through. We will tell you straight when shutters are the right call instead.")
        ],
        "specialty_systems": [
            "Folding glass walls — accordion-style retractable walls for patios and indoor-outdoor dining",
            "Multi-slide doors — stacking sliders up to 60 feet wide for full-opening fronts",
            "Aluminum storefront — Series 451, 501T, and equivalent thermally-broken systems",
            "Impact-rated entrances — full-glass doors with continuous hinges and HVHZ approval",
            "Curtain wall — for restaurant buildings with two-story or 14-foot+ openings",
            "Wine display glass — temperature-controlled, low-iron glass walls for cellar-front concepts"
        ],
        "anchor_projects": [
            ("Ocean Prime Fort Lauderdale", "/case-study-ocean-prime-fort-lauderdale.html"),
            ("Eddie V's Naples", "/case-study-eddie-vs-naples.html"),
        ]
    },
    {
        "slug": "hotel-glazing-contractor-florida",
        "h1": "Hotel Glazing Contractor — Florida",
        "title": "Hotel Glazing Contractor Florida | Curtain Wall & Impact | ACG",
        "description": "ACG installs hotel curtain wall, balcony rail glass, impact-rated windows, and storefront entries on Florida hospitality projects. CGC #1531993. 350+ commercial projects.",
        "intro": "Hotels demand glass that performs on three fronts: storm resistance, sound attenuation, and brand-quality finish. We have worked on resort, full-service, limited-service, and boutique hotel projects across Florida. We understand the gap between the renderings the brand approved and what actually passes inspection.",
        "pain_points": [
            ("Brand-standard finish on a Florida-code envelope", "Marriott, Hilton, IHG, and Hyatt brand standards were not written in Miami-Dade. We translate brand-standard details into HVHZ-compliant assemblies that still photograph the way the architect drew them."),
            ("Balcony rail glass that hits the BOCA load case", "Florida glass railings need to take 50 lb/ft and survive impact. We use approved systems with documented NOA — Trex Signature, AGS, C.R. Laurence — never anything off-spec."),
            ("Acoustical glazing for high-traffic corridors", "We spec laminated assemblies with PVB or SGP interlayers that hit STC 38+ for road-facing rooms — without throwing brand-finish appearance away."),
            ("Punch-list speed at handoff", "Hotels move from soft open to grand open fast. We staff punch crews that work 6-day weeks during the final 10 days to clear all glass items before guest arrival.")
        ],
        "specialty_systems": [
            "Unitized and stick-built curtain wall — for hotel towers and resort architecture",
            "Hotel impact windows — fixed and operable, full HVHZ approval where required",
            "Balcony glass railings — Trex Signature, AGS, C.R. Laurence, and architect-specified systems",
            "Storefront entrances — porte-cochere, lobby, restaurant, and amenity-deck",
            "All-glass entrances — for arrival sequences and lobby drama",
            "Spandrel glass and shadowbox — full envelope coordination"
        ],
        "anchor_projects": [
            ("Atlantic Fields", "/case-study-atlantic-fields.html"),
            ("Wild Blue Clubhouse", "/case-study-wild-blue-clubhouse.html"),
        ]
    },
    {
        "slug": "medical-office-glazier-florida",
        "h1": "Medical Office Glazier — Florida",
        "title": "Medical Office Glazier Florida | MOB Storefront & Impact | ACG",
        "description": "ACG installs medical office building glass — exam room privacy glazing, storefront entrances, impact-rated windows, and curtain wall. Florida-licensed CGC #1531993.",
        "intro": "Medical office buildings have a tight budget, a tight schedule, and three jurisdictions reviewing the same drawing. We have installed glass on MOBs ranging from 6,000 SF single-tenant clinics to 110,000 SF multi-tenant medical office campuses. We know the AHJ playbook for FBC, ADA, and HCAI-style compliance reviews.",
        "pain_points": [
            ("Privacy glazing without sacrificing daylight", "Switchable smart glass (SPD or PDLC), gradient-frit, and digital ceramic frit patterns. We have specified all three on Florida MOB projects."),
            ("ADA-compliant entrances with automatic operators", "Every medical entry needs accessible operators, panic hardware, and ADA-compliant pull/push side clearances. We get this right at submittal — not at punch."),
            ("Impact storefront for ground-floor clinics in coastal counties", "Imaging suites, urgent care, and pharmacy fronts on coastal Florida properties need impact-rated entries. We do this every week."),
            ("Schedule fit with TI buildouts", "Tenant improvements run fast. We schedule glass deliveries to land 3 days before installation, not 3 weeks — so storefront installs don't block your other trades.")
        ],
        "specialty_systems": [
            "Switchable privacy glass — SPD and PDLC films and laminated assemblies",
            "Frit glass — digital ceramic, gradient, dot, and custom pattern",
            "Aluminum storefront with ADA operators — auto-swing and auto-slide",
            "Impact-rated entrances — full-glass and stile-and-rail",
            "Curtain wall for medical campus exterior — unitized and stick-built",
            "Lead-lined glass — for imaging and radiation areas"
        ],
        "anchor_projects": [
            ("Siena Lakes Naples", "/case-study-siena-lakes-naples.html"),
        ]
    },
    {
        "slug": "school-glazier-florida",
        "h1": "School & Education Glazier — Florida",
        "title": "School Glazier Florida | K-12 Security Glass & Storefront | ACG",
        "description": "ACG installs K-12 and higher-ed glazing — security entrances, ballistic-rated vestibules, classroom impact windows, and storefront. Florida-licensed CGC #1531993.",
        "intro": "Florida school construction sits at the intersection of HVHZ code, post-Parkland security mandates, and state DOE bidding requirements. We have installed glass on K-12 charter, district, and private projects, including FEMA-rated emergency-operations buildings. We understand FF&E coordination with school furniture vendors and the calendar pressure of summer turnover.",
        "pain_points": [
            ("Security vestibule design that passes both FBC and post-Parkland safe-school standards", "We work with architects on bullet-resistant vestibule glazing (UL 752 Level 3 / Level 8) and impact-rated assemblies that pass both threat and storm review."),
            ("Classroom window replacement on summer-only schedules", "Schools turn over fast: graduation to first day of class is often 8-10 weeks. We sequence material orders, demo, and install to land before teacher set-up week."),
            ("Tornado/hurricane shelter glass for FEMA P-361 spaces", "FEMA 361 storm shelters require specific glass (or no glass at all). We have worked with FEMA-recognized systems on Florida emergency operations centers."),
            ("Coordination with playground, kitchen, and furniture FF&E", "Schools have 14 trades on the close-out punch list. We coordinate with kitchen contractors, casework installers, and gym floor crews to sequence glass to land at the right moment.")
        ],
        "specialty_systems": [
            "Bullet-resistant vestibules — UL 752 Level 3 through Level 8",
            "Impact-rated classroom windows — operable and fixed",
            "Storm shelter glazing — FEMA P-361 compliant systems",
            "Aluminum storefront entries — vandal-resistant hardware packages",
            "Frit and ceramic-coated glass — sun control on south and west elevations",
            "Curtain wall — for gymnasiums, common areas, and multi-story academic blocks"
        ],
        "anchor_projects": [
            ("Haines City EOC", "/case-study-haines-city-eoc.html"),
            ("Martin County Fire Training", "/case-study-martin-county-fire-training.html"),
        ]
    },
    {
        "slug": "retail-storefront-installer-florida",
        "h1": "Retail Storefront Installer — Florida",
        "title": "Retail Storefront Installer Florida | Tenant Improvement & New Build | ACG",
        "description": "ACG installs retail storefront, mall in-line spaces, freestanding pad-site glass, and impact-rated entrances for retail tenants across Florida. CGC #1531993.",
        "intro": "Retail storefront is the highest-volume work in commercial glazing — and the most demanding on schedule. National retailers, mall in-line spaces, freestanding pads, and ground-floor street-level retail. We have installed on all of them. Most retail glass jobs need to hit a hard CO date tied to merchandise delivery. We deliver.",
        "pain_points": [
            ("National prototype storefront on a Florida envelope", "Most retail prototypes were drawn in Texas, Ohio, or California. They are not HVHZ-rated. We translate prototype to FBC-compliant submittal without breaking landlord-required brand standards."),
            ("Mall coordination with landlord and tenant-improvement contractor", "Simon, Brookfield, and DDR landlords each have their own storefront design criteria document. We have read all of them. We know what gets approved and what gets rejected."),
            ("Speed for limited-stock and promotional rollouts", "Retail brands open stores in waves. We can run multi-site installs in parallel — same crew, same submittal package, replicated across 6-12 locations in a quarter."),
            ("Anti-ram-raid protection without ugly bollards", "Smash-and-grab retail crime in Florida has driven demand for laminated-glass storefronts with continuous-hinge entries. We spec the right interlayer for the threat — without making your storefront look like a bank.")
        ],
        "specialty_systems": [
            "Aluminum storefront — Series 451T, 501T, 601T, 701T and equivalent",
            "All-glass entrances — frameless single and pair doors with continuous hinges",
            "Impact-rated mall entries — including roll-down hurricane shutters where required",
            "Sun-control glazing — low-iron, low-E, and ceramic-frit for street-facing retail",
            "Spandrel and trim — color-matched to landlord brand standards",
            "Vestibules — full-glass vestibules for high-volume retail and grocery"
        ],
        "anchor_projects": [
            ("Tomoka Town Center", "/case-study-tomoka-town-center.html"),
            ("Baron Shoppes Tradition", "/case-study-baron-shoppes-tradition.html"),
        ]
    },
    {
        "slug": "office-building-glazier-florida",
        "h1": "Office Building Glazier — Florida",
        "title": "Office Building Glazier Florida | Curtain Wall, Storefront, Impact | ACG",
        "description": "ACG installs office building curtain wall, storefront, impact-rated punch windows, and interior glass partitions on Florida commercial office projects. CGC #1531993.",
        "intro": "Florida office is back. Class-A, Class-B, medical office, professional office, and creative office buildouts have absorbed faster in 2025-2026 than any other commercial sector. We have installed glass on more than 60 office buildings ranging from 6-story suburban Class-A to 1,200 SF tenant improvements. We understand both ground-up envelope and TI fit-out.",
        "pain_points": [
            ("Curtain wall pricing transparency on bid day", "Office curtain wall is the single biggest line item on most office buildings. We provide line-item breakouts so the GC can value-engineer with the architect — not just blow up the bid."),
            ("TI storefront on landlord schedules", "Office TIs run on landlord turnover schedules — sometimes 30 days from lease signing to keys-in-hand. We install storefront on this calendar all the time."),
            ("Interior glass partitions with the right STC", "Open-plan offices still need acoustic privacy in conference rooms and executive offices. We specify laminated and double-glazed interior systems with documented STC ratings."),
            ("Punch-out turnover at substantial completion", "Office buildings have aggressive substantial-completion targets driven by tenant lease commencement. We sequence punch crews to clear all glass within 5 working days of substantial completion.")
        ],
        "specialty_systems": [
            "Unitized and stick-built curtain wall — for 3-story+ office buildings",
            "Window wall — for mid-rise office",
            "Aluminum storefront — for ground-floor lobby and retail components",
            "Impact-rated punch windows — for HVHZ office projects",
            "Interior glass partitions — demountable and welded systems",
            "Frameless glass conference room fronts and executive office fronts"
        ],
        "anchor_projects": [
            ("Panther National", "/case-study-panther-national.html"),
            ("Cudjoe Key", "/case-study-cudjoe-key.html"),
        ]
    }
]

def build_vertical(v):
    canonical = f"https://acglass.com/{v['slug']}/"
    pain_html = "".join(
        f'<div class="vertical-pain"><h3>{html_lib.escape(t)}</h3><p>{html_lib.escape(d)}</p></div>'
        for t, d in v['pain_points']
    )
    sys_html = "".join(f'<li>{html_lib.escape(s)}</li>' for s in v['specialty_systems'])
    anchor_html = "".join(
        f'<li><a href="{u}">{html_lib.escape(n)}</a></li>'
        for n, u in v['anchor_projects']
    )
    body = f'''<section class="hero hero-vertical" style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:120px 0 80px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:24px;">Industry &middot; Specialty</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,64px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(v['h1'])}</h1>
<p style="color:rgba(255,255,255,0.8);font-size:20px;line-height:1.6;max-width:800px;">{html_lib.escape(v['intro'])}</p>
<div style="margin-top:40px;display:flex;gap:16px;flex-wrap:wrap;">
<a href="/send-plans.html" class="btn-primary" style="background:#E11320;color:#fff;padding:16px 32px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:16px 32px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:80px 0;">
<div class="container">
<h2 style="color:#fff;font-size:36px;margin-bottom:48px;">Where {html_lib.escape(v['h1'].split('—')[0].strip())} projects break down</h2>
<div class="vertical-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:32px;">
{pain_html}
</div>
</div>
</section>

<section style="background:#0e284f;padding:80px 0;">
<div class="container">
<h2 style="color:#fff;font-size:36px;margin-bottom:24px;">Systems we install for this vertical</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:17px;line-height:2;list-style:none;padding:0;max-width:900px;">
{sys_html}
</ul>
</div>
</section>

{'<section style="background:#050A12;padding:80px 0;"><div class="container"><h2 style="color:#fff;font-size:36px;margin-bottom:32px;">Selected projects</h2><ul style="color:#E11320;font-size:18px;line-height:2.2;list-style:none;padding:0;">' + anchor_html + '</ul></div></section>' if v['anchor_projects'] else ''}

<section style="background:#0e284f;padding:80px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:36px;margin-bottom:16px;">Ready to bid this work?</h2>
<p style="color:rgba(255,255,255,0.8);font-size:18px;margin-bottom:32px;">48-hour bid turnaround on commercial glazing plans. Florida-licensed CGC #1531993. $3M/$6M bonding capacity.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    extra_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": v['h1'],
        "description": v['description'],
        "provider": {"@id": canonical + "#org"},
        "areaServed": {"@type": "State", "name": "Florida"},
        "serviceType": v['h1']
    }
    breadcrumbs = [
        ("Home", "https://acglass.com/"),
        ("Industries", "https://acglass.com/industries/"),
        (v['h1'], canonical)
    ]
    html = page_wrap(v['title'], v['description'], canonical, body, extra_schema=extra_schema, breadcrumbs=breadcrumbs)
    write_page(f"{v['slug']}/index.html", html)

# ============================================================
# BATCH 2: AIO-bait FAQ pages (12)
# ============================================================

AIO_PAGES = [
    {
        "slug": "how-much-does-commercial-storefront-cost-florida",
        "title": "How Much Does Commercial Storefront Cost in Florida? (2026 Pricing)",
        "description": "Commercial storefront in Florida costs $66 to $142 per square foot installed in 2026. ACG breaks down what drives the price: glass type, HVHZ rating, framing system, hardware, and labor.",
        "h1": "How Much Does Commercial Storefront Cost in Florida?",
        "summary": "Commercial storefront installed in Florida costs $66 to $142 per square foot in 2026, including aluminum framing, tempered or laminated glass, hardware, sealants, and installation labor. HVHZ-rated impact assemblies sit at the upper end. Custom finishes, blast-rated assemblies, and curved corners push past $200/SF.",
        "sections": [
            ("What's included in that $66-$142/SF number", "The number covers extruded aluminum framing (typically 4-1/2\" or 6\" face dimension), insulated or tempered glass infill, weep system, sealants, hardware (closers, panic, locks, butts or continuous hinges, sweep), and installation labor. It does not include rough-opening prep, perimeter caulk by others, or interior finish."),
            ("What drives the difference between $66 and $142", "Five variables move the number: 1) HVHZ rating — Miami-Dade NOA or FBC product approval can add 18-30%. 2) Glass type — clear tempered is the floor, low-E + laminated SGP is the ceiling. 3) Framing system — basic 1-3/4\" storefront is cheapest, thermally-broken 2-1/4\" or 2-1/2\" systems are 25-40% more. 4) Hardware grade — Adams Rite is the base, Sargent / Von Duprin / Allegion premium hardware adds. 5) Project size and access — small infill jobs cost more per SF than 6,000 SF new construction."),
            ("Typical real-world pricing tiers", "Restaurant TI, 200 SF storefront, clear tempered, FBC standard: $66-$78/SF installed. Retail in-line, 400 SF storefront, low-E, FBC standard: $82-$98/SF. Coastal restaurant, 350 SF storefront, impact-rated, NOA: $108-$135/SF. Hotel lobby curtain wall (not storefront), 1,200 SF: $135-$220/SF — different system, different math."),
            ("How to lower the number without value engineering the spec", "Bid the work to 3 qualified Florida glaziers (not 5 — 5 invites unqualified low bidders). Issue full architectural drawings, not narratives. Provide a clear NOA list rather than 'glazier to provide product approvals.' Schedule with a real CO date — rush installs add 8-15%."),
            ("When the number goes up unexpectedly", "Permit reviewers can reject submittals for missing NOA numbers, wrong wind load, or framing thickness mismatched to the wind pressure. Each rejection costs 2-3 weeks. Building department-driven re-submittals are the most common cost overrun on Florida storefront work. The way to prevent this is to use a glazier with documented FBC submittal experience.")
        ],
        "faqs": [
            ("How much does commercial storefront cost in Florida in 2026?", "Commercial storefront in Florida costs $66 to $142 per square foot installed in 2026, including aluminum framing, glass, hardware, sealants, and labor. HVHZ-rated assemblies in Miami-Dade and Broward sit at the upper end."),
            ("What's the cheapest commercial storefront in Florida?", "Clear-tempered, 1-3/4\" face aluminum storefront on a non-HVHZ project starts around $66 per square foot installed. This is appropriate for inland Florida (Orlando, Tampa, Jacksonville) where wind pressures permit non-impact assemblies."),
            ("Is impact glass storefront worth the cost premium in Florida?", "For coastal counties and HVHZ jurisdictions (Miami-Dade, Broward, parts of Palm Beach), impact glass is not optional — it is required by code. For inland projects, impact glass is a discretionary upgrade that delivers insurance discounts and security benefits."),
            ("Do storefront costs include the permit?", "No. Storefront pricing typically includes shop drawings and engineering, but the building permit fee is paid by the GC or owner directly to the AHJ. Permit fees range from $400 to $4,000 depending on project value."),
            ("Can I get commercial storefront installed in under 30 days?", "Yes, on small TI work with stock-aluminum systems and standard glass. New-construction storefronts with custom finishes, NOA review, and engineered shop drawings typically take 8-14 weeks from contract to installation.")
        ]
    },
    {
        "slug": "what-is-hvhz-rated-glass",
        "title": "What Is HVHZ-Rated Glass? (Florida High-Velocity Hurricane Zone)",
        "description": "HVHZ-rated glass meets the Florida High-Velocity Hurricane Zone code — Miami-Dade County, Broward County, and parts of Palm Beach. Tested to TAS 201, 202, 203. ACG explains.",
        "h1": "What Is HVHZ-Rated Glass?",
        "summary": "HVHZ-rated glass is glazing tested and approved for use in Florida's High-Velocity Hurricane Zone — Miami-Dade County, Broward County, and portions of Palm Beach County. It must pass three tests: TAS 201 (large missile impact), TAS 202 (uniform static air pressure), and TAS 203 (cyclic wind pressure). Approval is documented via a Miami-Dade Notice of Acceptance (NOA) or a Florida Product Approval (FL #).",
        "sections": [
            ("Where the HVHZ boundary actually sits", "The HVHZ covers all of Miami-Dade County, all of Broward County, and portions of Palm Beach County east of Military Trail. Inland Palm Beach County and points north use the standard Florida Building Code wind requirements — not HVHZ. The boundary matters because it changes which products you can legally install."),
            ("The three TAS tests, in plain English", "TAS 201 fires a 9-pound 2x4 lumber projectile at the glass at 50 feet per second to simulate flying debris. TAS 202 applies static positive and negative wind pressure equivalent to design wind loads. TAS 203 cycles positive and negative pressure 9,000 times to simulate sustained hurricane wind."),
            ("Miami-Dade NOA vs. Florida Product Approval (FL #)", "Both are valid. A Miami-Dade NOA is issued by the Miami-Dade County Product Control Section. A Florida Product Approval (FL #) is issued by the Florida Department of Business and Professional Regulation. Both reference the same testing. Outside HVHZ counties, FL # is sufficient. Inside HVHZ, the AHJ typically wants the Miami-Dade NOA."),
            ("What products qualify", "Laminated glass with a polyvinyl butyral (PVB) or SentryGlas Plus (SGP) interlayer is standard. Common impact assemblies use 1/8\" + .090 PVB + 1/8\" outboard with a 1/4\" tempered inboard in a sealed insulating unit. Framing matters too — the entire assembly (frame + glass + sealant + anchor) is tested together, not just the glass."),
            ("Common mistakes that cause permit rejection", "1) Specifying glass alone instead of the full tested assembly. 2) Mixing glass from manufacturer A with frame from manufacturer B when the NOA is for the combined assembly. 3) Wind load on the drawings exceeds the design pressure rating on the NOA. 4) Approved alternates not properly documented. 5) NOA expired (NOAs have expiration dates — check before submittal).")
        ],
        "faqs": [
            ("What is HVHZ-rated glass?", "HVHZ-rated glass is glazing tested for use in Florida's High-Velocity Hurricane Zone, which covers Miami-Dade County, Broward County, and parts of Palm Beach County. It must pass TAS 201, 202, and 203 testing and carry a Miami-Dade Notice of Acceptance or Florida Product Approval."),
            ("Where does HVHZ apply in Florida?", "HVHZ applies in all of Miami-Dade County, all of Broward County, and portions of Palm Beach County east of Military Trail. The rest of Florida follows standard Florida Building Code wind requirements."),
            ("What's the difference between impact glass and HVHZ-rated glass?", "All HVHZ-rated glass is impact glass, but not all impact glass is HVHZ-rated. Inland Florida projects can use impact glass that meets ASTM E1996/E1886 without requiring the more stringent HVHZ TAS 201/202/203 testing."),
            ("Do I need a Miami-Dade NOA outside Miami-Dade County?", "Not legally — Florida Product Approval (FL #) is accepted statewide. But many AHJs in Broward and Palm Beach prefer to see Miami-Dade NOAs because they reference HVHZ-level testing."),
            ("How do I verify a product has a valid NOA?", "Check the Miami-Dade County Product Control Section's online database. Search by manufacturer or NOA number. Confirm the expiration date is in the future — NOAs are issued for 5-year terms and must be renewed.")
        ]
    },
    {
        "slug": "storefront-vs-curtain-wall",
        "title": "Storefront vs Curtain Wall: Which to Choose? (Cost, Code, Use Case)",
        "description": "Storefront and curtain wall are different aluminum-and-glass systems. Storefront is single-story, span-by-span. Curtain wall is multi-story, hung from the slab. ACG explains the right fit.",
        "h1": "Storefront vs Curtain Wall: Which to Choose?",
        "summary": "Storefront is a single-story aluminum-and-glass system installed span-by-span between floor and ceiling, designed for ground-floor commercial use up to about 14 feet tall. Curtain wall is a multi-story system that hangs from the building structure, designed to span multiple floors as a continuous skin. Storefront is cheaper, faster, and simpler. Curtain wall costs more but enables taller buildings, larger glass lites, and continuous glass facades.",
        "sections": [
            ("How storefront actually works", "Storefront is a stick-built aluminum extrusion system, typically 1-3/4\" to 2-1/2\" face dimension. Vertical mullions run from sill to header. Glass is installed by wet-glazing or dry-glazing. Storefront is engineered to resist wind loads on a single-story span. Standard maximum height is 12-14 feet. Above that, you need reinforced storefront or curtain wall."),
            ("How curtain wall actually works", "Curtain wall is a structural glass facade hung from the building's slab edge. Vertical mullions span floor-to-floor and connect to slab anchors. The entire assembly is engineered to handle dead load, wind load, seismic load, and thermal movement across multiple stories. Curtain wall comes in two main types: stick-built (assembled on-site) and unitized (prefabricated panels installed by crane)."),
            ("Cost comparison: what you'll actually pay", "Storefront on a Florida project: $66-$142 per square foot installed. Curtain wall on a Florida project: $95-$240 per square foot installed. For a 5,000 SF facade, that's $330K-$710K storefront vs. $475K-$1.2M curtain wall. The math matters."),
            ("When to choose storefront", "Single-story retail, restaurant, office TI, and ground-floor lobby work. Maximum opening height under 14 feet. Project budget is tight. Schedule is fast. AHJ submittal needs to be straightforward."),
            ("When to choose curtain wall", "Multi-story buildings (3+ stories). Glass facades wider than the available storefront mullion spacing. Continuous glass appearance across floors. Wind loads exceeding standard storefront ratings. Architectural intent requires deep mullion shadow lines, structural silicone glazing, or unitized panel construction.")
        ],
        "faqs": [
            ("What's the difference between storefront and curtain wall?", "Storefront is a single-story aluminum framing system installed span-by-span, typically up to 14 feet tall. Curtain wall is a multi-story system that hangs from the building structure as a continuous facade. Storefront is cheaper and faster; curtain wall enables taller buildings and larger glass."),
            ("Is curtain wall stronger than storefront?", "Yes — curtain wall mullions are heavier, deeper, and engineered to span multiple floors and resist wind loads at greater heights. Storefront is engineered for single-story use."),
            ("Which costs more, storefront or curtain wall?", "Curtain wall costs significantly more — typically $95-$240 per square foot installed vs. $66-$142 per square foot for storefront. Curtain wall also requires more engineering, more shop drawings, and a longer install schedule."),
            ("Can storefront go above 14 feet?", "Reinforced storefront with steel tubes inside the aluminum extrusion can extend to 16-18 feet on some systems. Above that, curtain wall is the right answer."),
            ("Can I mix storefront and curtain wall on one building?", "Yes — this is common. Ground-floor storefront with multi-story curtain wall above is the standard configuration on mid-rise mixed-use buildings.")
        ]
    },
    {
        "slug": "impact-glass-vs-hurricane-shutters",
        "title": "Impact Glass vs Hurricane Shutters: Which Is Better for Florida?",
        "description": "Impact glass is integrated and always-on; hurricane shutters are bolt-on and deployed before storms. ACG breaks down cost, insurance impact, aesthetics, and code compliance.",
        "h1": "Impact Glass vs Hurricane Shutters",
        "summary": "Impact glass is permanent, always-active hurricane protection built into the window or storefront itself — no deployment required. Hurricane shutters are bolt-on accordion, roll-down, panel, or Bahama-style protections that deploy before a storm. Impact glass costs more upfront but adds value, qualifies for insurance discounts, and doesn't require pre-storm action. Shutters cost less but require deployment and detract from the building appearance.",
        "sections": [
            ("How impact glass protects", "Impact-rated glass is a laminated assembly: two layers of glass bonded to a tough interlayer (PVB or SGP). When a flying object hits the glass, the outer layer may crack, but the interlayer holds the assembly together and prevents the opening from being breached. The pressurization of the building is maintained — which is what actually causes roof failures during hurricanes."),
            ("How hurricane shutters protect", "Shutters block the opening physically — accordion shutters fold across the opening from the side, roll-down shutters drop from the top, panel shutters bolt over the opening, Bahama shutters are hinged at the top. All of them are tested to the same TAS 201, 202, 203 standards as impact glass — they just have to be deployed."),
            ("Cost comparison", "Impact glass on a Florida commercial project adds roughly 18-30% to the storefront or window line item — typically $15-$45 per square foot above non-impact equivalent. Accordion and roll-down shutters cost $25-$45 per square foot installed. So shutters can be cheaper than impact glass on the line item alone, but you still need a code-rated window underneath them, and you lose the always-on protection."),
            ("Insurance and resale impact", "Most Florida insurers offer wind mitigation discounts for impact-rated openings — typically 30-45% off the wind portion of the premium. Shutters qualify for the same discount IF they are deployed and certified. Impact glass typically delivers a measurable resale-value premium on commercial property; shutters do not."),
            ("Building appearance and operations", "Impact glass is invisible — the building looks like any other glass building. Shutters change the appearance: accordion tracks are visible at the sides of openings, roll-down housings sit above openings, panels require permanent storage and pre-storm deployment crews. For restaurants and retail, the appearance trade-off is decisive — most upscale operators choose impact glass.")
        ],
        "faqs": [
            ("Is impact glass better than hurricane shutters?", "For most commercial buildings in Florida, impact glass is the better choice because it requires no deployment, doesn't affect building appearance, and delivers measurable resale value. Shutters are cheaper upfront but require pre-storm action and can detract from building aesthetics."),
            ("How much does impact glass cost vs shutters?", "Impact glass adds $15-$45 per square foot to a Florida storefront or window line item. Accordion and roll-down shutters typically cost $25-$45 per square foot installed. Shutters are usually cheaper on the line item, but you still need a code-rated window underneath them."),
            ("Do hurricane shutters qualify for insurance discounts?", "Yes, IF they are properly certified and deployed before a storm. Most Florida insurers offer the same wind mitigation discount for impact glass and rated shutters. Verify with your specific insurer before assuming the discount."),
            ("Can you combine impact glass and hurricane shutters?", "Yes, and some commercial owners do — impact glass for everyday protection plus shutters for the highest-exposure openings during major storms. The combination delivers redundant protection but doubles the cost."),
            ("Are hurricane shutters required in Florida?", "No — the Florida Building Code requires either impact-rated openings OR rated shutters in HVHZ counties and coastal jurisdictions. You can choose either approach, but you must have one of them on all openings exposed to the design wind load.")
        ]
    },
    {
        "slug": "commercial-glass-installation-timeline",
        "title": "How Long Does Commercial Glass Installation Take? (Realistic Timeline)",
        "description": "Commercial glass projects take 6-16 weeks from bid award to substantial completion in Florida. ACG breaks down each phase: shop drawings, NOA review, material lead time, install.",
        "h1": "How Long Does Commercial Glass Installation Actually Take?",
        "summary": "A typical commercial glass installation in Florida takes 6-16 weeks from bid award to substantial completion. The breakdown: shop drawings 2-4 weeks, owner/architect review 1-2 weeks, AHJ submittal and NOA review 2-4 weeks, material lead time 4-10 weeks (running in parallel), installation 1-4 weeks. Custom finishes, blast-rated assemblies, and curved glass add 4-8 weeks.",
        "sections": [
            ("Phase 1: Shop drawings and engineering (2-4 weeks)", "After contract award, the glazier produces shop drawings showing exact mullion locations, glass sizes, hardware schedule, and structural calculations. For HVHZ work, this phase also includes pulling the right Miami-Dade NOA or Florida Product Approval for the assembly. Shop drawings take 10-15 working days for a typical storefront and 15-25 working days for a curtain wall."),
            ("Phase 2: Owner/architect review (1-2 weeks)", "The architect and owner mark up shop drawings — color selection, hardware tweaks, threshold details, sealant joints. The glazier revises and re-submits. This phase often adds 1 round of revision, which adds another 5 working days."),
            ("Phase 3: AHJ submittal and permit (2-4 weeks)", "Some Florida AHJs review storefront submittals quickly (5-7 business days); others take 15-20. Miami-Dade County is generally fast on NOAs but slow on construction permit review for the building. Plan for 3 weeks average."),
            ("Phase 4: Material lead time (4-10 weeks, in parallel)", "Aluminum extrusions are typically 3-5 weeks lead time. Stock glass is 1-2 weeks. Custom glass (low-E, laminated, frit, ceramic-coated) is 4-8 weeks. Custom-anodized or PVDF-painted aluminum is 8-12 weeks. Material lead time runs in parallel with shop drawings and submittal, so the total isn't additive — it's the longest single track."),
            ("Phase 5: Installation (1-4 weeks)", "A 200 SF restaurant storefront installs in 2-3 working days. A 5,000 SF curtain wall installs in 4-8 working weeks. Speed depends on access, site congestion, and weather. Florida summer thunderstorms can shut down crane work mid-day — schedule accordingly."),
            ("How to compress the timeline", "Bid early with full architectural drawings. Choose stock aluminum colors and standard NOA glass. Lock the GC's structural opening before shop drawings — re-engineering after framing changes is the single biggest schedule killer. Order material on signed contract, not on permit issuance.")
        ],
        "faqs": [
            ("How long does commercial glass installation take?", "A typical commercial glass project in Florida takes 6-16 weeks from contract to substantial completion. The breakdown: 2-4 weeks shop drawings, 1-2 weeks review, 2-4 weeks permit, 4-10 weeks material lead time (parallel), and 1-4 weeks installation."),
            ("What's the fastest commercial glass install?", "A small storefront tenant improvement (under 200 SF) using stock aluminum and standard tempered glass can install in 2-3 weeks from contract — if shop drawings are simple and the permit is fast."),
            ("Why do curtain wall projects take so long?", "Curtain wall requires more engineering, more shop drawings, and longer material lead times. Unitized curtain wall is fabricated in panels off-site, which adds 6-10 weeks to the schedule but reduces field install time."),
            ("Can material lead time be sped up?", "Sometimes — paying expedite fees to extrusion suppliers can shave 1-2 weeks. Stock glass and stock aluminum colors save 2-4 weeks vs. custom. Working with a glazier who carries the right stock inventory saves time."),
            ("What's the biggest cause of schedule slippage?", "Building department permit delays, structural opening changes after shop drawings, and weather. The first two are controllable; the third is not.")
        ]
    },
    {
        "slug": "florida-building-code-glass-requirements",
        "title": "Florida Building Code Glass Requirements (2026 Edition)",
        "description": "Florida Building Code 2023 sets the glass requirements for commercial construction: wind load, impact rating, HVHZ, and energy. ACG breaks down what applies to your project.",
        "h1": "Florida Building Code Glass Requirements (2026)",
        "summary": "The Florida Building Code 8th Edition (2023) governs commercial glass installation through 2026. It requires: wind-load-resistant glazing per ASCE 7-22, impact-rated assemblies in HVHZ and Wind-Borne Debris Region (WBDR), energy-efficient glazing meeting FBC Energy Conservation chapter, and ADA-compliant entrances per FBC Accessibility chapter.",
        "sections": [
            ("Which code edition applies right now", "Florida Building Code 8th Edition (2023) took effect December 31, 2023, and applies to all permits pulled in 2024-2026. The next edition (9th, 2026) will likely take effect late 2026 or early 2027."),
            ("Wind load requirements (ASCE 7-22 by reference)", "Florida adopts ASCE 7-22 wind speeds. South Florida design wind speeds range from 160-200 mph (HVHZ) to 130-160 mph (rest of state). Glass must be rated for the design pressure calculated per ASCE 7-22 — typically 30-90 PSF on commercial walls, higher on corner zones."),
            ("Impact requirements: HVHZ vs WBDR", "Inside HVHZ (Miami-Dade, Broward, parts of Palm Beach), glass must be tested per TAS 201/202/203. Inside the Wind-Borne Debris Region (basically all coastal Florida within 1 mile of the coast, plus inland zones with high wind speeds), glass must be tested per ASTM E1996 / E1886 — or the building must be protected by rated shutters or panels."),
            ("Energy requirements", "FBC Energy Conservation chapter requires commercial glass to meet specific U-factor and SHGC limits. Climate Zone 1 (South Florida) requires U-factor ≤ 0.50 and SHGC ≤ 0.25 for most commercial fenestration. Climate Zone 2 (rest of Florida) is slightly less strict. Most commercial glaziers default to low-E coated glass to meet this."),
            ("ADA accessibility requirements", "FBC Accessibility chapter (based on 2010 ADA Standards) requires accessible entry doors: 32\" minimum clear width, 5 lb max opening force on interior doors, level landings, and proper hardware (lever, panic, or auto-operator). Storefront doors are subject to these requirements at primary entrances.")
        ],
        "faqs": [
            ("What Florida Building Code applies to commercial glass in 2026?", "Florida Building Code 8th Edition (2023) applies to all permits pulled through 2026. It governs wind load, impact, energy, and accessibility requirements for commercial glazing."),
            ("Is impact glass required everywhere in Florida?", "Impact glass or rated shutters are required throughout the Wind-Borne Debris Region — generally all coastal counties and any inland location with 130 mph+ design wind speed. Outside the WBDR, impact-rated glass is optional."),
            ("What's the difference between FBC and HVHZ requirements?", "FBC applies statewide. HVHZ is a stricter subset within FBC that applies only to Miami-Dade County, Broward County, and parts of Palm Beach. HVHZ requires more testing (TAS 201/202/203) than the rest of Florida (ASTM E1996/E1886)."),
            ("Do energy code requirements apply to all commercial buildings?", "Yes, with limited exceptions for unconditioned space (warehouses, parking garages). Conditioned commercial space requires U-factor and SHGC compliance per FBC Energy chapter."),
            ("Where do I find a product's FBC approval?", "Search the Florida Building Code Online portal at floridabuilding.org for FL Product Approvals. For HVHZ, search the Miami-Dade County Product Control NOA database directly.")
        ]
    },
    {
        "slug": "miami-dade-noa-explained",
        "title": "What Is a Miami-Dade NOA? (Notice of Acceptance — Plain English)",
        "description": "A Miami-Dade NOA is a Notice of Acceptance issued by Miami-Dade County Product Control approving a glass or shutter assembly for use in HVHZ. ACG explains how to read one.",
        "h1": "What Is a Miami-Dade NOA?",
        "summary": "A Miami-Dade NOA (Notice of Acceptance) is a document issued by the Miami-Dade County Product Control Section that certifies a specific glass, framing, or shutter assembly has passed all required testing for use in Florida's High-Velocity Hurricane Zone. Each NOA has a number, expiration date, design pressure rating, and approved configurations. Contractors must submit valid NOAs with permit applications for any HVHZ work.",
        "sections": [
            ("How to read an NOA document", "Every NOA has: 1) NOA number (format: 23-0517.02), 2) issue date and expiration date (typically 5 years), 3) manufacturer name, 4) product description (e.g., 'Series 451T aluminum storefront with laminated impact-resistant glass'), 5) design pressure rating in PSF (positive and negative), 6) maximum panel sizes, 7) approved glass thicknesses and interlayers, 8) approved anchorage details, 9) limitations and special requirements."),
            ("How to verify an NOA is current", "Go to the Miami-Dade County Product Control Section website. Search by NOA number or manufacturer. Confirm the document is marked 'Approved' and the expiration date is in the future. Expired NOAs cannot be used for new permits."),
            ("What an NOA is NOT", "An NOA is not a generic 'impact rating.' It is specific to the manufacturer, the specific extrusion profile, the specific glass thickness, the specific interlayer, and the specific anchorage shown in the test report. Substituting any element (different glass, different anchor, different frame profile) voids the NOA."),
            ("NOA vs. Florida Product Approval (FL #)", "Both are valid. NOAs are issued by Miami-Dade County and are recognized statewide. FL # approvals are issued by the Florida DBPR. NOAs are required in HVHZ counties; FL # is sufficient outside HVHZ. Many manufacturers carry both."),
            ("Common NOA mistakes that cause permit rejection", "1) Using an expired NOA. 2) Specifying a product mix that isn't covered by the NOA (e.g., 'Manufacturer X frame with Manufacturer Y glass'). 3) Design pressure on drawings exceeds NOA-approved DP rating. 4) Wrong anchorage detail. 5) Missing copy of NOA in submittal package.")
        ],
        "faqs": [
            ("What is a Miami-Dade NOA?", "A Miami-Dade NOA (Notice of Acceptance) is a document issued by Miami-Dade County Product Control that certifies a glass, framing, or shutter assembly has passed HVHZ testing. It includes a unique NOA number, expiration date, and approved configurations."),
            ("How long is a Miami-Dade NOA valid?", "Miami-Dade NOAs are typically issued for 5 years and must be renewed before expiration. Always verify the current status at the Miami-Dade County Product Control website before submitting for permit."),
            ("Where can I look up Miami-Dade NOAs?", "Search the Miami-Dade County Product Control Section's online NOA database. You can search by NOA number, manufacturer, or product type."),
            ("Is an NOA the same as a Florida Product Approval?", "No. An NOA is issued by Miami-Dade County and is required for HVHZ work. A Florida Product Approval (FL #) is issued by the Florida DBPR. Both reference similar testing, but Miami-Dade NOAs are typically required by HVHZ AHJs."),
            ("Can I use a glass product without an NOA in Miami-Dade?", "No. Any glass or shutter installed in Miami-Dade, Broward, or HVHZ areas of Palm Beach County must have a valid Miami-Dade NOA or accepted equivalent product approval. Permit will not be issued without it.")
        ]
    },
    {
        "slug": "aluminum-storefront-systems-compared",
        "title": "Aluminum Storefront Systems Compared (Series 451, 501T, 601T, 701T)",
        "description": "Aluminum storefront systems differ by face dimension, depth, thermal break, and wind rating. ACG compares the most-installed systems: Series 451, 501T, 601T, and 701T.",
        "h1": "Aluminum Storefront Systems: Series 451T, 501T, 601T, 701T",
        "summary": "Aluminum storefront systems are identified by series number that indicates face dimension (the visible width of the mullion) and depth. The most-installed systems on Florida commercial projects are Series 451T (1-3/4\" face, thermally broken), 501T (2\" face, thermally broken), 601T (2-1/4\" face, thermally broken), and 701T (2-1/2\" face, thermally broken). Each has different wind ratings, glass thicknesses, and price points.",
        "sections": [
            ("How to read storefront series numbers", "The first digit indicates face dimension category. The 'T' suffix indicates a thermal break (a polyamide isolator between the interior and exterior aluminum that improves U-factor). Series 451T has 1-3/4\" face. Series 501T has 2\" face. Series 601T has 2-1/4\" face. Series 701T has 2-1/2\" face. Deeper systems = higher wind ratings and larger spans."),
            ("Series 451T: the budget standard", "1-3/4\" face, 4-1/2\" depth. Standard for ground-floor retail, restaurant, and office TI. Single-glazed (1/4\" tempered) up to 12 feet tall. Max wind pressure roughly 35-50 PSF depending on glass and span. Cheapest in the family. Best for inland Florida, non-HVHZ work, and small storefront jobs."),
            ("Series 501T: thermally broken upgrade", "2\" face, 4-1/2\" depth. Same depth as 451T but wider face. Accepts insulated glass (1\" IG) and laminated impact glass. Standard for HVHZ retail and restaurant work. Max height around 14 feet. Typical price premium over 451T: 15-25%."),
            ("Series 601T: medium-duty workhorse", "2-1/4\" face, 5\" depth. Standard for hotel ground floor, larger restaurant fronts, and medical office buildings. Accepts 1\" IG and impact glass. Max height around 16 feet. Typical price premium over 501T: 10-15%."),
            ("Series 701T: heavy-duty storefront / light curtain wall", "2-1/2\" face, 6\" depth. For high-wind exposures (HVHZ Zone 4), tall storefronts (16-20 feet), and storefront-to-curtain-wall transition zones. Accepts thick laminated IG. Typical price premium over 601T: 12-20%."),
            ("How to choose the right series for your project", "Calculate design wind pressure first. Match the system's tested DP rating to your project's calculated DP, with a 20% safety margin. Then size for opening height. Then optimize for cost. Never spec a system that's under-rated for your wind load — it won't pass permit.")
        ],
        "faqs": [
            ("What's the difference between Series 451 and 501T storefront?", "Series 451T has a 1-3/4\" face dimension and a 4-1/2\" depth, designed for single-glazed assemblies. Series 501T has a 2\" face and accepts insulated and impact glass. 501T is the upgrade typically required for HVHZ work."),
            ("Which storefront system is best for HVHZ?", "For HVHZ-rated storefront, Series 501T, 601T, or 701T (or equivalent thermally-broken systems from other manufacturers) are most common. The specific series depends on wind load and opening height."),
            ("What does the 'T' suffix mean in storefront series?", "The 'T' indicates a thermal break — a polyamide isolator inside the aluminum extrusion that reduces heat transfer. Thermal-break systems are required by FBC Energy Conservation chapter on most commercial buildings."),
            ("Can different storefront series be mixed on one project?", "Yes, but each section must independently meet wind load requirements. It's most common to use a heavier-duty system on corner zones (higher wind pressure) and a standard system on field walls."),
            ("Who makes Series 451T and 501T systems?", "Multiple manufacturers produce equivalent systems: Kawneer, YKK AP, Tubelite, US Aluminum, and EFCO are the major brands. Profiles, ratings, and NOAs differ slightly between manufacturers.")
        ]
    },
    {
        "slug": "tempered-vs-laminated-glass",
        "title": "Tempered Glass vs Laminated Glass: Which Do You Actually Need?",
        "description": "Tempered glass is heat-treated for strength; laminated glass is two layers bonded to an interlayer. ACG explains where each is required by code, where to upgrade, and what they cost.",
        "h1": "Tempered Glass vs Laminated Glass",
        "summary": "Tempered glass is heat-treated to be 4x stronger than annealed glass and breaks into small, dull-edged pieces. Laminated glass is two layers of glass bonded to a tough plastic interlayer (PVB or SGP) that holds the assembly together when broken. Tempered is required in 'hazardous locations' (doors, sidelights, near floors). Laminated is required for impact-rated openings in Florida's WBDR and HVHZ zones, as well as for security and acoustic applications.",
        "sections": [
            ("What tempered glass actually does", "Tempered glass is heated to about 1,200°F and then rapidly cooled. This creates compressive stress on the surface and tensile stress in the core. The result: 4-5x stronger than regular glass and a safer break pattern (small granular pieces, no sharp shards). Tempered glass cannot be cut or drilled after tempering."),
            ("What laminated glass actually does", "Laminated glass bonds two layers of glass to a plastic interlayer — typically polyvinyl butyral (PVB) or SentryGlas Plus (SGP). When the assembly breaks, the interlayer holds the broken glass together. This is what makes laminated glass impact-resistant: even if the outer layer breaks, the opening remains sealed."),
            ("Where tempered glass is required by code", "FBC and IBC require tempered (or laminated) safety glazing in 'hazardous locations': doors and sidelights, glass within 24\" of a door, glass within 18\" of a floor, glass within 60\" of a tub or shower, and glass facing stairs."),
            ("Where laminated glass is required by code", "Impact-rated openings in HVHZ and WBDR zones must be laminated (or use approved shutters). FBC also requires laminated glass for skylights, overhead glazing, and certain railing applications."),
            ("Cost comparison", "Tempered glass adds roughly 25-40% to base annealed glass cost. Laminated glass adds 60-90% over annealed (depending on interlayer thickness and type). Insulated laminated impact glass (the typical HVHZ assembly) adds roughly 100-150% over plain annealed insulated glass."),
            ("When to upgrade beyond code", "Acoustic environments (hotels, restaurants near roads) — laminated with thick PVB hits STC 38+. Security (jewelry stores, banks) — laminated with SGP interlayer resists forced entry. Solar control — laminated allows custom interlayer colors and films.")
        ],
        "faqs": [
            ("What's the difference between tempered and laminated glass?", "Tempered glass is heat-treated for strength and breaks into small dull pieces. Laminated glass is two layers bonded to a tough interlayer that holds the assembly together when broken. Tempered is safer; laminated is impact-resistant and stays in place after impact."),
            ("Is laminated glass safer than tempered?", "It depends on the application. Tempered is safer for collision impacts because it breaks into dull granules. Laminated is safer for security and storm exposure because it doesn't fall out of the opening when broken."),
            ("Do I need tempered glass in my storefront?", "Yes — Florida Building Code requires tempered (or laminated) safety glazing in storefront doors, sidelights, and glass adjacent to doors. The specific zones are defined by FBC Chapter 24."),
            ("Is impact glass the same as laminated glass?", "All impact-rated glass is laminated, but not all laminated glass is impact-rated. Impact-rated assemblies must pass specific missile and pressure tests (TAS 201/202/203 or ASTM E1996/E1886). Plain laminated glass without testing doesn't qualify as impact-rated."),
            ("How much does laminated glass cost vs tempered?", "Laminated glass typically costs 60-90% more than tempered glass on the same nominal thickness. Insulated laminated impact glass costs 100-150% more than plain insulated tempered glass.")
        ]
    },
    {
        "slug": "low-e-glass-explained-florida",
        "title": "Low-E Glass Explained: What Florida Commercial Buildings Need",
        "description": "Low-E glass uses microscopic metal oxide coatings to control heat transfer. ACG explains the coatings (#2 vs #3 surface), SHGC, and what Florida Energy Code requires.",
        "h1": "Low-E Glass for Florida Commercial Buildings",
        "summary": "Low-E (low-emissivity) glass uses microscopic metallic coatings to reduce heat transfer through the window. In Florida's hot climate, the goal is to keep solar heat OUT — which means a low Solar Heat Gain Coefficient (SHGC). The Florida Energy Code requires SHGC ≤ 0.25 for most commercial fenestration in Climate Zone 1 (South Florida). Low-E coatings are applied on surface #2 (outboard of cavity) for solar control or surface #3 (inboard of cavity) for heating climates — Florida wants #2.",
        "sections": [
            ("How low-E coatings work", "Low-E coatings are microscopically thin layers of metal oxides (typically silver, tin, or zinc) applied to one surface of a glass lite. They reflect infrared (heat) radiation while allowing visible light to pass. The result: a window that lets light in but keeps heat out."),
            ("Surface position matters: #2 vs #3", "In an insulated glass unit (IGU), surfaces are numbered 1-4 from outside to inside. Surface #2 (outboard glass, inside the cavity) is the standard low-E position for hot climates like Florida — it reflects solar heat before it enters the building. Surface #3 (inboard glass, inside the cavity) is for cold climates where the goal is to keep interior heat in."),
            ("Key performance numbers", "U-factor: heat transfer rate (lower is better in Florida). Typical low-E commercial glass: 0.28-0.45. Solar Heat Gain Coefficient (SHGC): fraction of solar radiation that enters (lower is better in Florida). Typical low-E commercial glass: 0.20-0.35. Visible Light Transmittance (VLT): fraction of visible light (higher is generally preferred). Typical low-E: 35-70%."),
            ("What Florida Energy Code requires", "FBC Energy Conservation chapter for commercial buildings in Climate Zone 1 (South Florida) requires SHGC ≤ 0.25 for vertical fenestration and U-factor ≤ 0.50. Climate Zone 2 (rest of Florida) is slightly less strict. Most commercial buildings default to a high-performance low-E that easily exceeds these minimums."),
            ("Common low-E products on Florida commercial work", "Solarban 60, Solarban 70XL, Solarban 90 (Vitro). SunGuard SuperNeutral 68, SunGuard HP Neutral 41 (Guardian). VRE-46, VRE-67 (Viracon). Each has slightly different VLT and SHGC. Architects often spec specific products by name; glaziers source through approved fabricators."),
            ("Cost premium for low-E", "Low-E coating adds roughly 8-15% to the glass line item. The energy savings typically pay back the premium in 3-6 years on conditioned commercial space.")
        ],
        "faqs": [
            ("What is low-E glass?", "Low-E (low-emissivity) glass has a microscopic metal oxide coating that reflects infrared heat while allowing visible light to pass. In Florida's hot climate, low-E glass reduces cooling loads by keeping solar heat out of the building."),
            ("Which surface should low-E be on in Florida?", "Surface #2 (the outboard glass, inside the cavity) is the standard position for hot climates like Florida. This position reflects solar heat before it enters the building."),
            ("Does Florida require low-E glass?", "Florida Energy Code requires a maximum SHGC of 0.25 for most commercial vertical fenestration in South Florida. Low-E coatings are the standard way to meet this requirement, though other compliance paths exist."),
            ("What's the difference between Solarban 60 and Solarban 70XL?", "Solarban 70XL has lower SHGC (better solar heat rejection) than Solarban 60, with slightly less VLT. 70XL is more commonly specified for South Florida high-performance commercial buildings."),
            ("Does low-E glass affect appearance?", "Slightly. Some low-E coatings have a faint blue, green, or silvery tint. High-performance low-E products often have nearly neutral appearance. Architects typically review actual glass samples before spec.")
        ]
    },
    {
        "slug": "commercial-glass-warranty-explained",
        "title": "Commercial Glass Warranty Explained (What's Actually Covered)",
        "description": "Commercial glass warranties cover seal failure, coating defects, and workmanship — but exclude weather, vandalism, and improper cleaning. ACG explains what's actually covered.",
        "h1": "Commercial Glass Warranty: What's Actually Covered",
        "summary": "Commercial glass warranties typically include three layers: glass manufacturer warranty (insulated glass seal failure 10 years, coatings 5-10 years), framing manufacturer warranty (aluminum extrusion finish 10-20 years), and installer workmanship warranty (1-5 years on installation defects). None of them cover weather events, vandalism, building movement, or cleaning damage. The fine print matters.",
        "sections": [
            ("Layer 1: glass manufacturer warranty", "Fabricated insulated glass units typically carry a 10-year warranty against seal failure (when the seal between the two glass lites fails and moisture or fog appears inside the cavity). Low-E coatings typically carry a 5-10 year warranty against coating delamination, oxidation, or peeling. Surface scratches, breakage, and impact damage are NOT covered."),
            ("Layer 2: framing manufacturer warranty", "Aluminum extrusion finish warranties: 10 years for class I anodize, 10-20 years for PVDF (Kynar 70%/30%) paint, 5-10 years for powder coat. Standard mill-finish aluminum carries no finish warranty. Framing structural integrity is typically covered for 1 year — manufacturers won't warrant aluminum framing against building settlement or excessive structural loads."),
            ("Layer 3: installer workmanship warranty", "ACG provides a 1-year workmanship warranty as standard, with options to extend to 5 years for owner-financed work. The workmanship warranty covers leaks at sealants, anchorage failure due to installation error, and hardware adjustment. It does NOT cover the glass itself (that's the manufacturer's responsibility) or building movement that disturbs the glass installation."),
            ("What's NEVER covered (read this)", "Hurricane/wind damage above design loads. Vandalism. Acid-rain pitting. Improper cleaning (using razor blades, abrasive cleaners, or ammonia on tinted glass). Concrete or stucco overspray during construction. Building movement exceeding design tolerances. Settlement cracks. Welding spatter from adjacent work."),
            ("How to actually use a warranty when something fails", "Document the failure with photos and date-stamped notes. Email the GC, owner, and the responsible warranty party (glass mfr, frame mfr, or installer) within 30 days. Allow access for inspection. Do not attempt repair before inspection — that voids the warranty. ACG handles all warranty coordination for jobs we install.")
        ],
        "faqs": [
            ("What does a commercial glass warranty typically cover?", "Commercial glass warranties cover insulated glass seal failure (10 years), low-E coating defects (5-10 years), aluminum frame finish (10-20 years for PVDF), and installer workmanship (1-5 years). They exclude weather damage, vandalism, and improper cleaning."),
            ("How long do insulated glass units last?", "A properly fabricated insulated glass unit should last 20-30 years before the seal degrades. Manufacturer warranties typically cover the first 10 years against seal failure."),
            ("Are hurricane-damaged glass repairs covered?", "Hurricane damage is not covered by glass warranties — it is an insurance claim. Glass warranties cover material defects and installation errors, not weather events."),
            ("What voids a glass warranty?", "Improper cleaning (razor blades, abrasive cleaners), structural building movement exceeding design tolerances, vandalism, third-party modifications, and unauthorized repair attempts can all void glass warranties."),
            ("Who handles a warranty claim — the GC, owner, or glazier?", "Typically the owner contacts the glazier who installed the glass. The glazier coordinates with the responsible manufacturer (glass or frame) and handles the claim. ACG provides this coordination at no charge for the warranty period.")
        ]
    },
    {
        "slug": "best-glaziers-south-florida",
        "title": "Best Commercial Glaziers in South Florida (2026 Comparison)",
        "description": "How to evaluate commercial glaziers in South Florida: license verification, bonding, NOA experience, project portfolio, and response time. ACG breaks down what actually matters.",
        "h1": "How to Evaluate the Best Commercial Glaziers in South Florida",
        "summary": "Choosing the best commercial glazier in South Florida comes down to five verifiable criteria: 1) Active Florida CGC license, 2) bonding capacity matching your project size, 3) documented HVHZ/NOA submittal experience, 4) project portfolio in your specific building type, and 5) bid turnaround and response speed. Cheapest is almost never best — project delays from a low-bid glazier with permit problems can cost more than the entire glass package.",
        "sections": [
            ("Criterion 1: License verification", "Search the Florida DBPR online portal. Look for an active Certified General Contractor (CGC) or Certified Glass and Glazing Contractor license. Verify the license has no recent disciplinary actions. CGC #1531993 is ACG's — easy to verify."),
            ("Criterion 2: Bonding capacity", "Any glazier bidding work over $250K should carry contractor bonding that covers your project size. Ask for a bonding letter naming the bonding company and the per-project / aggregate limits. ACG carries $3M per project / $6M aggregate."),
            ("Criterion 3: NOA / FBC submittal experience", "Florida glaziers with weak NOA experience cause permit delays — sometimes catastrophic ones. Ask for 3 recent HVHZ permit submittal references with the AHJ name and approval date. A glazier without this is a risk on HVHZ work."),
            ("Criterion 4: Project portfolio fit", "A glazier who has installed 50 retail TIs is not the same as one who has installed 5 hospital curtain walls. Match the glazier's portfolio to your project type. ACG's 350+ projects span restaurant, retail, hotel, medical, education, and high-end residential."),
            ("Criterion 5: Response speed", "Bid turnaround tells you everything about a glazier's operations. Slow bid response (3+ weeks) usually means slow shop drawings, slow submittals, and slow installs. ACG returns bids in 48 hours on standard commercial plans."),
            ("Red flags to walk away from", "1) No web presence or only a Facebook page. 2) Cash-only or 'discount for cash.' 3) Inability to provide a current license number. 4) No physical office address. 5) Recent BBB complaints around abandonment or non-completion. 6) Bid significantly below the next 3 bidders (this almost always means missing scope).")
        ],
        "faqs": [
            ("How do I find a qualified commercial glazier in South Florida?", "Start with the Florida DBPR license search — verify the contractor holds an active CGC or Certified Glass and Glazing license. Then check bonding capacity, HVHZ submittal experience, and portfolio in your project type."),
            ("What questions should I ask a commercial glazier before hiring?", "Ask for: 1) license number and DBPR verification, 2) bonding letter, 3) three recent HVHZ project references with permit dates, 4) sample shop drawings from a comparable project, 5) workmanship warranty terms."),
            ("Why are the cheapest commercial glaziers risky?", "Low bids usually mean missing scope (no NOA review fees, no shop drawings, no engineering, no hardware). Permit delays from a low-bid glazier with weak NOA experience can cost more than the entire glass package."),
            ("How fast should a commercial glazier respond to a bid request?", "Qualified Florida commercial glaziers should return standard bids within 5-7 business days. Faster operations (like ACG) hit 48 hours on most plans. Slow response usually signals slow downstream operations."),
            ("Should I bid commercial glazing to 3 or 5 glaziers?", "Three qualified bidders is the sweet spot for commercial glazing. Five invites unqualified low bidders. Pre-qualify by license, bonding, and portfolio before sending plans.")
        ]
    }
]

def build_aio(p):
    canonical = f"https://acglass.com/{p['slug']}/"
    sec_html = "".join(
        f'<section style="background:#0e284f;padding:60px 0;"><div class="container"><h2 style="color:#fff;font-size:30px;margin-bottom:20px;">{html_lib.escape(h)}</h2><p style="color:rgba(255,255,255,0.85);font-size:17px;line-height:1.8;max-width:900px;">{html_lib.escape(t)}</p></div></section>'
        for h, t in p['sections']
    )
    faq_html = "".join(
        f'<details style="background:#0e284f;padding:24px 28px;margin-bottom:12px;border-radius:8px;border-left:3px solid #E11320;"><summary style="color:#fff;font-size:18px;font-weight:600;cursor:pointer;">{html_lib.escape(q)}</summary><p style="color:rgba(255,255,255,0.8);font-size:16px;line-height:1.8;margin-top:16px;">{html_lib.escape(a)}</p></details>'
        for q, a in p['faqs']
    )

    body = f'''<section class="hero" style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:24px;">Resource &middot; Plain-English Guide</div>
<h1 style="color:#fff;font-size:clamp(32px,4.5vw,52px);line-height:1.15;margin:0 0 24px;">{html_lib.escape(p['h1'])}</h1>
<p style="color:rgba(255,255,255,0.9);font-size:19px;line-height:1.65;max-width:900px;"><strong style="color:#fff;">Quick answer:</strong> {html_lib.escape(p['summary'])}</p>
</div>
</section>

{sec_html}

<section style="background:#050A12;padding:80px 0;">
<div class="container">
<h2 style="color:#fff;font-size:34px;margin-bottom:32px;">Frequently asked</h2>
<div style="max-width:900px;">{faq_html}</div>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:16px;">Have a Florida commercial glass project?</h2>
<p style="color:rgba(255,255,255,0.7);margin-bottom:28px;">ACG · CGC #1531993 · 48-hour bid turnaround on commercial plans.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    schemas = [faq_schema(p['faqs']), {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p['h1'],
        "description": p['description'],
        "datePublished": "2026-05-23",
        "dateModified": "2026-05-23",
        "author": {"@type": "Organization", "name": "American Commercial Glass", "url": "https://acglass.com"},
        "publisher": {"@id": canonical + "#org"}
    }]
    breadcrumbs = [
        ("Home", "https://acglass.com/"),
        ("Resources", "https://acglass.com/resources/"),
        (p['h1'], canonical)
    ]
    html = page_wrap(p['title'], p['description'], canonical, body, extra_schema=schemas, breadcrumbs=breadcrumbs)
    write_page(f"{p['slug']}/index.html", html)

# ============================================================
# BATCH 3: Resources hub + Glossary
# ============================================================

GLOSSARY_TERMS = [
    ("Annealed Glass", "Standard untreated float glass. Not safety glass. Used as the base for tempering or lamination, or directly in non-hazardous locations."),
    ("ASCE 7", "American Society of Civil Engineers structural design standard. ASCE 7-22 is the current wind load reference for Florida Building Code."),
    ("Aluminum Storefront", "An aluminum-and-glass framing system installed span-by-span between floor and ceiling, typically for single-story commercial use up to 14 feet tall."),
    ("Anodize", "A finishing process for aluminum that creates a durable oxide layer. Class I anodize carries 10-year warranty on commercial work."),
    ("Argon Fill", "Inert gas filled between insulated glass lites to reduce heat transfer. Standard on energy-rated insulated units."),
    ("ASTM E1996", "Test standard for impact-resistant glazing outside HVHZ — covers missile impact and cyclic pressure. Required in Florida WBDR."),
    ("Bullet-Resistant Glass", "Multi-layer laminated glass tested to UL 752 Level 1-10. Used in vestibules, banking, and security applications."),
    ("BIPV", "Building-Integrated Photovoltaics. Solar-active glass that generates electricity. Used in some Florida commercial curtain walls."),
    ("Continuous Hinge", "Heavy-duty door hinge running the full height of the door. Standard on commercial entries — replaces traditional 3-hinge installations."),
    ("Curtain Wall", "A non-load-bearing exterior wall system hung from the building structure. Spans multiple floors. Distinct from storefront."),
    ("Design Pressure (DP)", "The wind load a glass assembly is rated to resist, measured in pounds per square foot (PSF). Both positive (pressure) and negative (suction) values matter."),
    ("Dry Glazing", "Installing glass with pre-formed gaskets rather than wet sealants. Faster and cleaner than wet glazing."),
    ("FBC", "Florida Building Code. The state-wide building code. Current edition: 8th Edition (2023)."),
    ("Float Glass", "The standard manufacturing process for flat glass. Molten glass is floated on molten tin to produce a flat, polished sheet."),
    ("Frit", "Ceramic ink fired onto glass surface for decorative or solar-control patterns. Can be digital, dot, gradient, or stripe."),
    ("Glazing", "The process of installing glass — or the glass assembly itself. A 'glazier' is a worker who installs glass."),
    ("HVHZ", "High-Velocity Hurricane Zone. Florida's strictest wind code zone — Miami-Dade, Broward, parts of Palm Beach County."),
    ("Impact-Rated Glass", "Glass tested to resist debris impact during hurricanes. Required in HVHZ and Florida WBDR zones. Always laminated."),
    ("Insulated Glass Unit (IGU)", "Two or more glass lites separated by a spacer and sealed at the edges, with air or argon in the cavity. Standard for energy-rated commercial windows."),
    ("Kawneer", "Major manufacturer of commercial aluminum framing systems. Series 451T, 501T, 601T are commonly specified."),
    ("Laminated Glass", "Two layers of glass bonded to a plastic interlayer (PVB or SGP). Holds together when broken. Required for impact-rated assemblies."),
    ("Lite", "A single pane of glass. An 'insulated glass unit' contains two or more lites."),
    ("Low-E Glass", "Glass with a microscopic metal oxide coating that reflects heat. Standard for energy-efficient commercial glazing."),
    ("Miami-Dade NOA", "Notice of Acceptance issued by Miami-Dade County certifying a product passes HVHZ testing. Required in HVHZ counties."),
    ("Mullion", "A vertical or horizontal aluminum member in a storefront or curtain wall framing system."),
    ("Muntin", "A horizontal divider within a single glass opening. Decorative or structural."),
    ("Polyvinyl Butyral (PVB)", "Standard interlayer in laminated glass. Holds the glass together when broken. Used in impact-rated assemblies."),
    ("PVDF Paint", "Polyvinylidene fluoride architectural coating (Kynar 70%/30%). 20-year warranty on commercial aluminum framing."),
    ("Setting Block", "Small rubber blocks at the bottom of a glass lite that distribute the glass weight onto the frame. Critical for proper glazing."),
    ("Shadow Box", "An opaque infill panel in a curtain wall, typically positioned at floor lines to conceal interior structure."),
    ("SentryGlas Plus (SGP)", "Premium interlayer for laminated glass (made by Kuraray). 100x stiffer than standard PVB. Used in high-performance impact assemblies."),
    ("SHGC", "Solar Heat Gain Coefficient. Fraction of solar energy that enters through the glass. Lower is better in Florida (typical target ≤0.25)."),
    ("Spandrel", "An opaque section of glass or panel between vision-area lites in a curtain wall. Conceals slab edges and ceiling cavities."),
    ("Stick-Built", "Curtain wall installation method where individual aluminum members are assembled on-site. Distinct from unitized."),
    ("Storefront", "Aluminum-and-glass framing system for ground-floor commercial use. Span-by-span, single-story, typically up to 14 feet tall."),
    ("TAS 201, 202, 203", "Three tests required by Miami-Dade HVHZ: large missile impact (TAS 201), uniform static air pressure (TAS 202), and cyclic wind pressure (TAS 203)."),
    ("Tempered Glass", "Heat-treated glass that is 4-5x stronger than annealed and breaks into small dull pieces. Required in 'hazardous locations' by code."),
    ("Thermal Break", "A non-conductive isolator (typically polyamide) inside aluminum framing that reduces heat transfer. Required by Florida Energy Code."),
    ("Unitized Curtain Wall", "Curtain wall installed as prefabricated panels assembled in a shop and installed by crane. Faster and more weather-tight than stick-built."),
    ("U-Factor", "Rate of heat transfer through a glass assembly, measured in BTU/hr·sq ft·°F. Lower is better in all climates (typical Florida target ≤0.50)."),
    ("Visible Light Transmittance (VLT)", "Fraction of visible light that passes through the glass. Higher is generally preferred (typical commercial target 35-70%)."),
    ("WBDR", "Wind-Borne Debris Region. The portion of Florida (and other coastal states) where impact-rated assemblies or shutters are required by code."),
    ("Wet Glazing", "Installing glass with field-applied silicone sealants rather than gaskets. Used for structural silicone glazing and renovation work."),
    ("YKK AP", "Major manufacturer of commercial aluminum framing systems. YHS 50 TU, YOW 250 TU are common storefront systems.")
]

def build_glossary():
    canonical = "https://acglass.com/glossary/"
    terms_html = "".join(
        f'<div class="glossary-term" id="{html_lib.escape(t.lower().replace(" ", "-").replace("(","").replace(")",""))}"><h3 style="color:#fff;font-size:20px;margin-bottom:8px;">{html_lib.escape(t)}</h3><p style="color:rgba(255,255,255,0.8);font-size:16px;line-height:1.7;margin-bottom:32px;">{html_lib.escape(d)}</p></div>'
        for t, d in sorted(GLOSSARY_TERMS)
    )
    body = f'''<section class="hero" style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:20px;">Reference &middot; Glossary</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Commercial Glazing Glossary</h1>
<p style="color:rgba(255,255,255,0.8);font-size:18px;line-height:1.6;max-width:800px;">{len(GLOSSARY_TERMS)} terms that come up on Florida commercial glass projects. Written for architects, GCs, owners, and anyone reading shop drawings for the first time.</p>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="max-width:900px;">
{terms_html}
</div>
</section>'''
    extra = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Commercial Glazing Glossary",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY_TERMS
        ]
    }
    breadcrumbs = [("Home", "https://acglass.com/"), ("Resources", "https://acglass.com/resources/"), ("Glossary", canonical)]
    html = page_wrap("Commercial Glazing Glossary (44 Terms) | ACG", "44 terms that come up on Florida commercial glass projects — HVHZ, NOA, curtain wall, storefront, low-E, and more. Plain-English definitions from ACG.", canonical, body, extra_schema=extra, breadcrumbs=breadcrumbs)
    write_page("glossary/index.html", html)

def build_resources_hub():
    canonical = "https://acglass.com/resources/"
    items = [
        ("How Much Does Commercial Storefront Cost in Florida?", "/how-much-does-commercial-storefront-cost-florida/", "2026 pricing: $66-$142/SF installed"),
        ("What Is HVHZ-Rated Glass?", "/what-is-hvhz-rated-glass/", "Miami-Dade, Broward, parts of Palm Beach"),
        ("Storefront vs Curtain Wall", "/storefront-vs-curtain-wall/", "Which system for which project"),
        ("Impact Glass vs Hurricane Shutters", "/impact-glass-vs-hurricane-shutters/", "Cost, insurance, and aesthetics"),
        ("Commercial Glass Installation Timeline", "/commercial-glass-installation-timeline/", "6-16 weeks from bid to handoff"),
        ("Florida Building Code Glass Requirements", "/florida-building-code-glass-requirements/", "FBC 2023 wind, impact, energy"),
        ("Miami-Dade NOA Explained", "/miami-dade-noa-explained/", "How to read a Notice of Acceptance"),
        ("Aluminum Storefront Systems Compared", "/aluminum-storefront-systems-compared/", "Series 451T, 501T, 601T, 701T"),
        ("Tempered vs Laminated Glass", "/tempered-vs-laminated-glass/", "Code, cost, and when to upgrade"),
        ("Low-E Glass Explained", "/low-e-glass-explained-florida/", "What Florida buildings actually need"),
        ("Commercial Glass Warranty Explained", "/commercial-glass-warranty-explained/", "What's covered vs not covered"),
        ("Best Commercial Glaziers in South Florida", "/best-glaziers-south-florida/", "5 criteria for evaluation"),
        ("Glossary (44 Terms)", "/glossary/", "HVHZ, NOA, low-E, curtain wall, more"),
    ]
    cards_html = "".join(
        f'<a href="{u}" style="background:#0e284f;padding:32px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;transition:transform 0.2s;"><h3 style="color:#fff;font-size:20px;margin:0 0 12px;">{html_lib.escape(t)}</h3><p style="color:rgba(255,255,255,0.6);font-size:14px;margin:0;">{html_lib.escape(s)}</p></a>'
        for t, u, s in items
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:20px;">Resources Hub</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Commercial Glazing Resources</h1>
<p style="color:rgba(255,255,255,0.8);font-size:18px;line-height:1.6;max-width:800px;">Plain-English guides from a Florida commercial glazing contractor. HVHZ rules, NOA explanations, cost benchmarks, code requirements, and the glossary architects actually use.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;">
{cards_html}
</div>
</div>
</section>'''
    breadcrumbs = [("Home", "https://acglass.com/"), ("Resources", canonical)]
    html = page_wrap("Commercial Glazing Resources | Florida Code, HVHZ, NOA, Cost | ACG", "Plain-English commercial glazing guides from ACG: HVHZ rules, NOA explanations, FBC requirements, cost benchmarks, system comparisons, and a 44-term glossary.", canonical, body, breadcrumbs=breadcrumbs)
    write_page("resources/index.html", html)

# Industries hub
def build_industries_hub():
    canonical = "https://acglass.com/industries/"
    items = [
        ("Restaurant Storefront", "/restaurant-glazier-florida/", "Folding walls, indoor-outdoor dining"),
        ("Hotel Glazing", "/hotel-glazing-contractor-florida/", "Curtain wall, balcony rail, impact"),
        ("Medical Office", "/medical-office-glazier-florida/", "Privacy glass, ADA entrances"),
        ("Schools & Education", "/school-glazier-florida/", "Security vestibules, K-12 storefront"),
        ("Retail", "/retail-storefront-installer-florida/", "Mall in-line, freestanding pad"),
        ("Office Buildings", "/office-building-glazier-florida/", "Curtain wall, TI storefront"),
    ]
    cards_html = "".join(
        f'<a href="{u}" style="background:#0e284f;padding:40px 32px;border-radius:8px;text-decoration:none;display:block;border-left:3px solid #E11320;"><h3 style="color:#fff;font-size:22px;margin:0 0 12px;">{html_lib.escape(t)}</h3><p style="color:rgba(255,255,255,0.6);font-size:14px;margin:0;">{html_lib.escape(s)}</p></a>'
        for t, u, s in items
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:20px;">Industries</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Commercial Glazing by Industry</h1>
<p style="color:rgba(255,255,255,0.8);font-size:18px;line-height:1.6;max-width:800px;">ACG installs commercial glass across six core verticals. Each industry has its own code overlay, schedule pressure, and finish requirements. We have built the playbook for all six.</p>
</div>
</section>
<section style="background:#050A12;padding:60px 0;">
<div class="container">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;">
{cards_html}
</div>
</div>
</section>'''
    breadcrumbs = [("Home", "https://acglass.com/"), ("Industries", canonical)]
    html = page_wrap("Commercial Glazing by Industry — Restaurant, Hotel, Medical, School, Retail, Office | ACG", "ACG installs commercial glass across 6 verticals: restaurants, hotels, medical offices, schools, retail, and office buildings. Florida-licensed CGC #1531993.", canonical, body, breadcrumbs=breadcrumbs)
    write_page("industries/index.html", html)

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("Building vertical pages...")
    for v in VERTICALS:
        build_vertical(v)
    print(f"\nBuilding AIO-bait FAQ pages...")
    for p in AIO_PAGES:
        build_aio(p)
    print(f"\nBuilding glossary...")
    build_glossary()
    print(f"\nBuilding resources hub...")
    build_resources_hub()
    print(f"\nBuilding industries hub...")
    build_industries_hub()
    total = len(VERTICALS) + len(AIO_PAGES) + 3
    print(f"\nGenerated {total} pages total.")
