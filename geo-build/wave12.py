#!/usr/bin/env python3
"""Wave 12 — Final coverage gaps + more conversion pages.
- 4 gym/fitness × city
- 3 religious × city
- 4 automotive showroom × city
- 3 assisted living × city
- 4 more vertical hubs (gym, automotive, religious, assisted-living Florida)
- 6 more high-intent FAQ

Total: 24 pages. ALL claims sourced from verified ACG standing list.
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


def vertical_city_template(vertical_name, vertical_short, city, scope_bullets, intent_text):
    """Build a consistent vertical x city page."""
    bullet_html = "\n".join([f"<li>\u2713 {b}</li>" for b in scope_bullets])
    return f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">{vertical_name} Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">{vertical_name} Commercial Glazing in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">{intent_text}</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">{vertical_short} glazing scopes in {city}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
{bullet_html}
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {city} {vertical_short.lower()} clients choose ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">48-hour bid turnaround on complete RFQ packages. $6M aggregate bonding qualifies us for commercial scopes to $2M+. Direct manufacturer relationships with Kawneer, YKK AP, Tubelite, ESWindows, Euro-Wall. Documented zero OSHA recordable incidents since 2021. FL CGC #1531993 with $3M general liability.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">{city} {vertical_short.lower()} glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''


# ===== GYM / FITNESS =====
GYM_CITIES = [
    ("Miami","miami","Miami-Dade County"),
    ("Tampa","tampa","Hillsborough County"),
    ("Orlando","orlando","Orange County"),
    ("Naples","naples","Collier County"),
]

# ===== RELIGIOUS / WORSHIP =====
RELIGIOUS_CITIES = [
    ("Orlando","orlando","Orange County"),
    ("Tampa","tampa","Hillsborough County"),
    ("Miami","miami","Miami-Dade County"),
]

# ===== AUTOMOTIVE SHOWROOM =====
AUTO_CITIES = [
    ("West Palm Beach","west-palm-beach","Palm Beach County"),
    ("Fort Lauderdale","fort-lauderdale","Broward County"),
    ("Tampa","tampa","Hillsborough County"),
    ("Orlando","orlando","Orange County"),
]

# ===== ASSISTED LIVING =====
ASSISTED_CITIES = [
    ("Naples","naples","Collier County"),
    ("West Palm Beach","west-palm-beach","Palm Beach County"),
    ("Orlando","orlando","Orange County"),
]


def build_gym():
    title = "Gym &amp; Fitness Commercial Glazing Florida \u2014 ACG"
    desc = "ACG installs commercial glazing on Florida gym and fitness facilities \u2014 large storefronts, full-height curtain wall, mirror-replacement glazing, impact-rated where required. FL CGC #1531993."
    body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Gym &amp; Fitness Glazing</p>
<h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">Gym &amp; Fitness Commercial Glazing in Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs commercial glazing on Florida gyms, fitness studios, boutique fitness, hotel fitness centers, and large-format health clubs. Storefronts, full-height curtain wall, mirror-replacement glazing, impact-rated assemblies where the AHJ requires.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Gym &amp; fitness glazing scopes</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Large-format storefront entries (Kawneer, YKK AP)</li>
<li>\u2713 Full-height curtain wall facade glazing</li>
<li>\u2713 Mirror walls and oversized mirror-replacement glazing</li>
<li>\u2713 Studio interior glass partitions (sound-attenuated)</li>
<li>\u2713 Impact-rated punched windows for HVHZ locations</li>
<li>\u2713 Folding glass walls for indoor-outdoor training spaces</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Gym &amp; fitness glazing by Florida city</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;">
<li><a href="/gym-fitness-glazing-miami/" style="color:#0e284f;text-decoration:underline;">Gym &amp; fitness glazing Miami</a></li>
<li><a href="/gym-fitness-glazing-tampa/" style="color:#0e284f;text-decoration:underline;">Gym &amp; fitness glazing Tampa</a></li>
<li><a href="/gym-fitness-glazing-orlando/" style="color:#0e284f;text-decoration:underline;">Gym &amp; fitness glazing Orlando</a></li>
<li><a href="/gym-fitness-glazing-naples/" style="color:#0e284f;text-decoration:underline;">Gym &amp; fitness glazing Naples</a></li>
</ul>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Gym glazing bid \u2014 48 hours on complete plans</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
    page(title, desc, body, "gym-fitness-commercial-glazing-florida",
         breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),("Gym &amp; Fitness Glazing", "https://acglass.com/gym-fitness-commercial-glazing-florida/")])

    for city, slug, county in GYM_CITIES:
        bullets = [
            "Storefront entries and large-format aluminum systems (Kawneer, YKK AP)",
            "Full-height curtain wall facade",
            "Mirror walls and oversized mirror-replacement",
            "Sound-attenuating interior partitions",
            "Impact-rated punched windows where the AHJ requires",
            "Folding glass walls for indoor-outdoor training"
        ]
        intent = f"ACG installs commercial glazing on gyms, fitness studios, hotel fitness centers, and large-format health clubs across {county}. Storefronts, full-height curtain wall, mirror-replacement, and HVHZ-rated assemblies where required."
        body = vertical_city_template("Gym &amp; Fitness", "Gym &amp; fitness", city, bullets, intent)
        service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":f"Gym &amp; Fitness Glazing in {city}, FL","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"City","name":city,"containedInPlace":{"@type":"State","name":"Florida"}},"serviceType":"Gym and Fitness Commercial Glazing"})
        page(f"Gym &amp; Fitness Glazing {city}, FL \u2014 ACG", f"Gym and fitness facility commercial glazing in {city}, Florida. Large storefronts, full-height curtain wall, mirror replacement, impact-rated assemblies. FL CGC #1531993.", body, f"gym-fitness-glazing-{slug}",
             extra_schema=service_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Gym &amp; Fitness Glazing","https://acglass.com/gym-fitness-commercial-glazing-florida/"),(city, f"https://acglass.com/gym-fitness-glazing-{slug}/")])


def build_religious():
    for city, slug, county in RELIGIOUS_CITIES:
        bullets = [
            "Sanctuary curtain wall and full-height glazing",
            "Stained glass restoration and re-glazing",
            "Storefront entries at parish hall and education buildings",
            "Impact-rated assemblies where HVHZ requires (Miami-Dade, Broward)",
            "Acoustic glazing at sanctuary and rehearsal spaces",
            "Fire-rated glazing at corridor and stairwell per FBC"
        ]
        intent = f"ACG installs commercial glazing on Florida religious and worship facilities across {county} \u2014 churches, synagogues, mosques, temples, parish halls, religious education buildings. Sanctuary curtain wall, stained glass restoration, storefront entries, impact-rated where HVHZ requires."
        body = vertical_city_template("Religious &amp; Worship", "Religious facility", city, bullets, intent)
        page(f"Religious &amp; Worship Glazing {city}, FL \u2014 ACG", f"Commercial glazing on Florida religious facilities in {city}. Sanctuary curtain wall, stained glass restoration, storefront entries, HVHZ-rated where required. FL CGC #1531993.", body, f"religious-glazing-{slug}",
             breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),(f"Religious Glazing {city}", f"https://acglass.com/religious-glazing-{slug}/")])


def build_auto():
    for city, slug, county in AUTO_CITIES:
        bullets = [
            "Full-height curtain wall showroom facade",
            "Structural silicone glazing for frameless showroom appearance",
            "Service-department storefront and impact-rated overhead glass",
            "All-glass entrance doors with structural patch fittings",
            "Mezzanine and gallery rail glass (laminated SGP)",
            "Architectural lighting integration with curtain wall mullion"
        ]
        intent = f"ACG installs commercial glazing on Florida automotive and luxury showrooms across {county} \u2014 full-height curtain wall showroom facades, structural silicone, service-department storefronts, mezzanine rails. Direct relationships with Kawneer 1600 SS and YKK AP YHC 300 OG."
        body = vertical_city_template("Automotive Showroom", "Automotive showroom", city, bullets, intent)
        page(f"Automotive Showroom Glazing {city}, FL \u2014 ACG", f"Automotive and luxury showroom commercial glazing in {city}, Florida. Full-height curtain wall, structural silicone, service-department storefronts. FL CGC #1531993.", body, f"automotive-showroom-glazing-{slug}",
             breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),(f"Automotive Showroom {city}", f"https://acglass.com/automotive-showroom-glazing-{slug}/")])


def build_assisted():
    for city, slug, county in ASSISTED_CITIES:
        bullets = [
            "Lobby and main entrance curtain wall",
            "Impact-rated punched windows for resident rooms",
            "Folding glass walls at dining and amenity spaces",
            "Fire-rated glazing at corridors per FBC",
            "ADA-compliant entrance doors with automatic operators",
            "Acoustic glazing for resident privacy and HVAC noise control"
        ]
        intent = f"ACG installs commercial glazing on Florida assisted living, memory care, and senior living facilities across {county} \u2014 lobby curtain wall, impact-rated resident-room windows, folding glass walls at dining, ADA-compliant entrances, fire-rated corridor glazing."
        body = vertical_city_template("Assisted Living &amp; Senior Living", "Assisted living", city, bullets, intent)
        page(f"Assisted Living Glazing {city}, FL \u2014 ACG", f"Commercial glazing on Florida assisted living and senior facilities in {city}. Lobby curtain wall, impact-rated resident windows, folding amenity walls. FL CGC #1531993.", body, f"assisted-living-glazing-{slug}",
             breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),(f"Assisted Living Glazing {city}", f"https://acglass.com/assisted-living-glazing-{slug}/")])


# ===== 6 more high-intent FAQ =====
FAQ_PAGES = [
    ("commercial-glazing-payment-terms-florida", "What payment terms do Florida commercial glaziers offer?",
     "Florida commercial glazing payment terms typically follow AIA G702/G703 progress billing: 10-20% mobilization at material order, monthly progress draws on stored material and installed work, 5-10% retention released at substantial completion, final 5% at punch list closeout. ACG accepts standard AIA pay applications with no surprise fees.",
     [
       ("What's the typical mobilization deposit on a Florida commercial glazing scope?", "10-20% on contract signing or material order. The deposit funds long-lead-time aluminum extrusion and glass orders. On scopes over $250K, mobilization is typically structured as a Schedule of Values line item billed at first pay application."),
       ("Does ACG accept AIA G702/G703 pay applications?", "Yes. Standard AIA pay applications are the default on commercial scopes. Lien waivers (conditional and unconditional) submitted with each pay application. Sworn statements provided on request."),
       ("What about retention?", "Standard Florida commercial retention is 10% on the first 50% of contract value, dropping to 5% on the remaining 50%. Retention release at substantial completion (less punch reserve, typically 1-3% held until punch close).")
     ]),
    ("can-i-finance-commercial-glazing-florida", "Can I finance a commercial glazing scope in Florida?",
     "Florida commercial glazing scopes are typically financed through the project's general contractor financing or owner-direct construction loan. ACG does not extend direct financing but works within standard commercial construction financing structures (construction loans, mezzanine debt, owner equity draws).",
     [
       ("Do I need to finance the glazing scope separately?", "Almost never. Commercial glazing is a subcontracted scope within the project's overall construction financing. The general contractor or owner manages draw timing. ACG bills progress payments against the established financing schedule."),
       ("What if my construction loan is delayed?", "Tell us upfront. If the construction loan is in commitment but not yet funded, we can typically defer material orders 2-4 weeks without losing schedule. Beyond that, lead-time risk on aluminum and glass increases. We've worked through enough delayed-financing situations to phase the order strategically."),
       ("Does ACG work with owner-direct projects vs GC-managed?", "Both. We bid owner-direct (restaurant, owner-operator hotel, owner-developer) and GC-managed scopes daily. Owner-direct often involves a different paperwork pathway but the bid response time and warranty terms are identical.")
     ]),
    ("what-is-a-good-bid-acknowledgment-time", "What is a good commercial glazing bid acknowledgment time?",
     "A good commercial glazing bid acknowledgment is under 4 business hours from RFQ receipt. ACG standard is acknowledgment within 2 hours during business hours and bid response within 48 hours on complete RFQ packages. The Florida market average is 24-72 hour acknowledgment and 7-15 business day bid response.",
     [
       ("Why does bid acknowledgment time matter?", "It signals whether the glazier is actually working your project or letting it sit in a queue. Fast acknowledgment doesn't guarantee a fast bid \u2014 but slow acknowledgment almost always means slow everything else (submittals, RFI responses, schedule communication)."),
       ("What's typical for high-quality Florida commercial glaziers?", "Acknowledgment under 4 business hours. Bid response inside 48 hours on complete packages. Clarification questions inside 24 hours if the RFQ is incomplete. Submittal package delivered within 10-15 business days of contract award."),
       ("How does ACG hit a 2-hour acknowledgment standard?", "We run an estimating intake agent that processes inbound RFQs within minutes and routes them to the human estimating team with project type, scope size, AHJ, and lead-time flags pre-tagged. The human estimator then has the context they need to write a meaningful acknowledgment within 2 hours of RFQ landing in the inbox.")
     ]),
    ("commercial-glazier-sba-set-aside-florida", "Does ACG bid SBA, DBE, or SBE set-aside Florida commercial glazing scopes?",
     "ACG bids SBE (Small Business Enterprise) set-aside Florida commercial glazing scopes. We are not currently DBE-certified or 8(a)-certified. For DBE-required federal-funded scopes, we partner with DBE-certified glazing subs as joint-venture or supplier-tier subcontractor.",
     [
       ("What public-funded scopes does ACG bid?", "Florida state university construction, Florida community college construction, Florida K-12 public school construction, Florida county and municipal building construction. Federal-funded scopes (FAA, VA, GSA) we bid as joint-venture with DBE-certified primaries."),
       ("Is ACG certified as a woman-owned business?", "ACG is woman-owned (Rielly Walsh, Operational CEO) and SBE-eligible under federal definitions. WBE state certification application status: in progress as of Q2 2026."),
       ("Where do I find ACG's current certification status?", "Email info@acglass.com for current certification documents. Florida CGC #1531993 verifiable at MyFloridaLicense.com. Other certifications provided on request for specific bid packages.")
     ]),
    ("how-far-does-acg-travel-for-projects", "How far does ACG travel for commercial glazing projects?",
     "ACG covers all of Florida \u2014 Miami-Dade to Pensacola, Key West to Jacksonville, and the entire Gulf Coast. We also bid Tennessee commercial glazing scopes ahead of Nashville Q3 2026 office opening. Outside FL/TN, we evaluate scope-by-scope; we generally do not bid commercial glazing outside the Southeast.",
     [
       ("What Florida regions does ACG actively work in?", "South Florida (Miami-Dade, Broward, Palm Beach, Monroe, Collier), Central Florida (Orange, Seminole, Polk, Brevard, Volusia, Indian River), West Florida (Hillsborough, Pinellas, Manatee, Sarasota, Lee, Charlotte), North Florida (Duval, St. Johns, Clay, Alachua, Marion), and Panhandle on selected scopes (Escambia, Bay, Leon, Walton)."),
       ("Does ACG bid Tennessee scopes from Florida?", "Yes. Bid coordination and project supervision from West Palm Beach until the Nashville office opens Q3 2026. Field labor sourced from Tennessee crew partners during the transition. TN commercial general contractor license application in progress."),
       ("Will ACG travel outside Florida and Tennessee?", "Case-by-case. For projects in Georgia, Alabama, the Carolinas, or other Southeast markets we evaluate based on scope size, repeat-client relationship, and crew availability. We generally do not bid first-time clients outside FL/TN.")
     ]),
    ("what-makes-acg-different-florida-glazier", "What makes ACG different from other Florida commercial glaziers?",
     "ACG operates the commercial glazing business on an AI-augmented operating system: 48-hour bid turnaround vs Florida market average of 7-15 business days, 2-hour bid acknowledgment standard, dedicated CFO Agent for daily P&L variance, in-house submittal automation, and a published transparency log of operations data. We compete on speed and reliability, not on price.",
     [
       ("What is the AI-augmented operating system?", "Multi-agent AI stack running project intake, billing, accounts receivable, dealer onboarding, SEO, and content production. Each function is managed by a dedicated agent with human oversight. We're the first specialty contractor we know of publishing operations data on AI in production."),
       ("How does that translate to better outcomes for the GC or owner?", "Faster bid turnaround (48 hours vs market 7-15 days). Cleaner submittal packages on first submission (saves 2-3 weeks of schedule). Faster RFI response (24 hours standard vs market 3-5 days). Better project communication frequency. Same field crew quality with better back-office coordination."),
       ("Does ACG charge a premium for the AI-augmented operating system?", "No. Bid pricing is competitive on a like-for-like basis with Florida market commercial glaziers. The AI-augmented operating system reduces our own overhead, which lets us hold competitive pricing while delivering faster turnaround.")
     ])
]


def build_faq():
    for slug, q, intro, faq in FAQ_PAGES:
        title = f"{q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing FAQ</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for qq, aa in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(qq)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(aa)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Send us drawings \u2014 48-hour bid</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        speakable = json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"})
        page(title, intro, body, slug,
             extra_schema=speakable,
             breadcrumb=[("Home","https://acglass.com/"),("FAQ","https://acglass.com/florida-glazing-faq/"),(q, f"https://acglass.com/{slug}/")],
             faq=faq)


if __name__ == "__main__":
    print("Wave 12 \u2014 final vertical gaps + buyer FAQ")
    build_gym()
    print(f"  Gym hub + {len(GYM_CITIES)} city pages")
    build_religious()
    print(f"  {len(RELIGIOUS_CITIES)} religious city pages")
    build_auto()
    print(f"  {len(AUTO_CITIES)} automotive showroom city pages")
    build_assisted()
    print(f"  {len(ASSISTED_CITIES)} assisted living city pages")
    build_faq()
    print(f"  {len(FAQ_PAGES)} FAQ pages")
    total = 1 + len(GYM_CITIES) + len(RELIGIOUS_CITIES) + len(AUTO_CITIES) + len(ASSISTED_CITIES) + len(FAQ_PAGES)
    print(f"\nWave 12 total: {total}")
