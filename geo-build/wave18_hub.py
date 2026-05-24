#!/usr/bin/env python3
"""Master hub page at /storefront-glazier-florida/ listing all 79 city pages.
This is the canonical entry point for the storefront-glazier network."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from wave18_cities import TIER2_CITIES

ROOT = "/home/user/workspace/acglass-website"

# Group by region for organized display
REGIONS_DISPLAY = [
    ("Palm Beach County", "palm_beach", "Coastal Atlantic · FBC Wind Zone"),
    ("Miami-Dade County (HVHZ)", "hvhz_mdade", "High-Velocity Hurricane Zone"),
    ("Broward County (HVHZ)", "hvhz_broward", "High-Velocity Hurricane Zone"),
    ("Treasure Coast", "treasure_coast", "Martin · St. Lucie · Indian River"),
    ("Southwest Florida", "sw_fl", "Collier · Lee · Charlotte"),
    ("Tampa Bay", "tampa_bay", "Hillsborough · Pinellas · Sarasota · Manatee"),
    ("Central Florida", "central_fl", "Orange · Polk · Osceola"),
    ("Florida Keys", "keys", "Monroe County · marine-grade"),
    ("Space Coast", "space_coast", "Brevard County"),
]

# Build city lists per region (combining wave 17 + wave 18)
WAVE17 = [
    ("West Palm Beach", "west-palm-beach", "palm_beach"),
    ("Boca Raton", "boca-raton", "palm_beach"),
    ("Jupiter", "jupiter", "palm_beach"),
    ("Delray Beach", "delray-beach", "palm_beach"),
    ("Palm Beach Gardens", "palm-beach-gardens", "palm_beach"),
    ("Miami", "miami", "hvhz_mdade"),
    ("Fort Lauderdale", "fort-lauderdale", "hvhz_broward"),
    ("Naples", "naples", "sw_fl"),
    ("Fort Myers", "fort-myers", "sw_fl"),
    ("Tampa", "tampa", "tampa_bay"),
    ("Orlando", "orlando", "central_fl"),
]

# Combine
all_cities_by_region = {r: [] for _, r, _ in REGIONS_DISPLAY}
for name, slug, region in WAVE17:
    all_cities_by_region[region].append((name, slug))
for name, slug, _, region, _, _ in TIER2_CITIES:
    all_cities_by_region[region].append((name, slug))

# Sort each list alphabetically
for r in all_cities_by_region:
    all_cities_by_region[r].sort(key=lambda x: x[0])

total = sum(len(v) for v in all_cities_by_region.values())


def render_region_block(name, region_key, subtitle):
    cities = all_cities_by_region[region_key]
    cards = "\n".join(
        f'        <a href="/storefront-glazier-{slug}-florida/" class="city-link">{city_name}</a>'
        for city_name, slug in cities
    )
    return f"""      <div class="region-block">
        <div class="region-header">
          <h3>{name}</h3>
          <div class="region-meta">{subtitle} · {len(cities)} {('cities' if len(cities) != 1 else 'city')}</div>
        </div>
        <div class="city-grid">
{cards}
        </div>
      </div>"""


# Build ItemList schema for the directory
item_list_items = []
position = 1
for region_name, region_key, _ in REGIONS_DISPLAY:
    for city_name, slug in all_cities_by_region[region_key]:
        item_list_items.append({
            "@type": "ListItem",
            "position": position,
            "name": f"Storefront Glazier in {city_name}, Florida",
            "url": f"https://acglass.com/storefront-glazier-{slug}-florida/"
        })
        position += 1

schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "CollectionPage",
            "@id": "https://acglass.com/storefront-glazier-florida/#page",
            "url": "https://acglass.com/storefront-glazier-florida/",
            "name": "Storefront Glazier in Florida — 79 Cities Served",
            "description": f"American Commercial Glass provides licensed commercial storefront glazier services across {total} Florida cities. Florida CGC #1531993. 350+ commercial projects. 48-hour bid.",
            "datePublished": "2026-05-24T15:00:00-04:00",
            "dateModified": "2026-05-24T15:00:00-04:00",
            "publisher": {"@id": "https://acglass.com/#organization"},
            "isPartOf": {"@id": "https://acglass.com/#website"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": total,
                "itemListElement": item_list_items
            }
        },
        {
            "@type": ["LocalBusiness", "GeneralContractor"],
            "additionalType": "https://schema.org/Glazier",
            "@id": "https://acglass.com/storefront-glazier-florida/#localbusiness",
            "name": "American Commercial Glass — Florida Statewide Storefront Glazier",
            "alternateName": ["ACG", "ACG Glass", "ACG Florida"],
            "description": f"Commercial storefront glazier serving {total} Florida cities. Florida CGC #1531993.",
            "url": "https://acglass.com/storefront-glazier-florida/",
            "telephone": "+17724867711",
            "email": "connor@acglass.com",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "700 S Rosemary Ave #204",
                "addressLocality": "West Palm Beach",
                "addressRegion": "FL",
                "postalCode": "33401",
                "addressCountry": "US"
            },
            "areaServed": {"@type": "State", "name": "Florida"},
            "sameAs": [
                "https://www.wikidata.org/wiki/Q139858578",
                "https://www.linkedin.com/company/acglass",
                "https://network.procore.com/p/american-commercial-glass-west-palm-beach"
            ]
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                {"@type": "ListItem", "position": 2, "name": "Storefront Glazier in Florida", "item": "https://acglass.com/storefront-glazier-florida/"}
            ]
        }
    ]
}

regions_html = "\n".join(render_region_block(n, k, s) for n, k, s in REGIONS_DISPLAY)

html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storefront Glazier in Florida — {total} Cities Served | American Commercial Glass</title>
<meta name="description" content="Licensed commercial storefront glazier serving {total} Florida cities. FL CGC #1531993, $6M bonded, 350+ commercial projects, 48-hour bid turnaround. Find your city below.">
<meta name="keywords" content="storefront glazier florida, commercial storefront florida, florida glazing contractor, commercial glass florida">
<link rel="canonical" href="https://acglass.com/storefront-glazier-florida/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="Connor Walsh, President, American Commercial Glass">
<meta property="og:title" content="Storefront Glazier in Florida — {total} Cities Served | ACG">
<meta property="og:description" content="Licensed commercial storefront glazier serving {total} Florida cities. FL CGC #1531993, 350+ commercial projects.">
<meta property="og:url" content="https://acglass.com/storefront-glazier-florida/">
<meta property="og:image" content="https://acglass.com/images/projects/eau-palm-beach/aerial-resort.jpg">
<meta property="og:type" content="website">
<link rel="preload" as="image" href="/images/projects/eau-palm-beach/aerial-resort.webp" type="image/webp" fetchpriority="high">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<script type="application/ld+json">
{json.dumps(schema, indent=2)}
</script>

<style>
  body {{ margin:0; font-family:'Inter',-apple-system,sans-serif; background:#050a12; color:#e8ecf2; line-height:1.6; -webkit-font-smoothing:antialiased; }}
  .nav {{ position:sticky; top:0; z-index:50; background:rgba(5,10,18,.92); backdrop-filter:blur(14px); border-bottom:1px solid rgba(255,255,255,.06); }}
  .nav-inner {{ max-width:1280px; margin:0 auto; padding:18px 28px; display:flex; align-items:center; justify-content:space-between; }}
  .nav-logo img {{ height:32px; width:auto; }}
  .nav-links {{ display:flex; gap:28px; align-items:center; }}
  .nav-links a {{ color:rgba(232,236,242,.75); text-decoration:none; font-size:14px; font-weight:500; }}
  .nav-links a:hover {{ color:#fff; }}
  .nav-cta {{ background:#e11320; color:#fff !important; padding:10px 18px; border-radius:6px; font-weight:600; }}

  .hero {{ position:relative; min-height:70vh; display:flex; align-items:center; padding:80px 0; overflow:hidden; }}
  .hero-bg {{ position:absolute; inset:0; z-index:0; }}
  .hero-bg img {{ width:100%; height:100%; object-fit:cover; transform:scale(1.06); }}
  .hero-overlay {{ position:absolute; inset:0; z-index:1; background:linear-gradient(180deg,rgba(5,10,18,.6) 0%,rgba(5,10,18,.78) 50%,rgba(5,10,18,.96) 100%); }}
  .hero-content {{ position:relative; z-index:2; max-width:1280px; margin:0 auto; padding:0 28px; }}
  .eyebrow {{ display:inline-flex; align-items:center; gap:12px; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.18em; text-transform:uppercase; color:rgba(255,255,255,.7); font-weight:600; margin-bottom:32px; }}
  .eyebrow .dot {{ width:6px; height:6px; background:#e11320; border-radius:50%; }}
  .eyebrow .bar {{ width:28px; height:1px; background:rgba(255,255,255,.3); }}
  h1 {{ font-size:clamp(40px,6vw,84px); font-weight:800; line-height:1.02; letter-spacing:-.025em; color:#fff; margin:0 0 28px; max-width:980px; }}
  h1 .accent {{ color:#e11320; }}
  .hero-sub {{ font-size:clamp(17px,1.6vw,22px); line-height:1.55; color:rgba(232,236,242,.85); max-width:780px; margin:0 0 40px; }}
  .hero-actions {{ display:flex; gap:14px; flex-wrap:wrap; }}
  .btn-primary {{ background:#e11320; color:#fff; padding:16px 30px; border-radius:6px; text-decoration:none; font-weight:600; font-size:16px; display:inline-flex; align-items:center; gap:10px; border:1px solid #e11320; }}
  .btn-primary:hover {{ background:#c10f1c; border-color:#c10f1c; }}
  .btn-ghost {{ background:transparent; color:#fff; padding:16px 30px; border-radius:6px; text-decoration:none; font-weight:600; font-size:16px; display:inline-flex; align-items:center; gap:10px; border:1px solid rgba(255,255,255,.25); }}

  section {{ padding:clamp(72px,8vw,120px) 0; }}
  section.alt {{ background:rgba(255,255,255,.018); border-top:1px solid rgba(255,255,255,.05); border-bottom:1px solid rgba(255,255,255,.05); }}
  .container {{ max-width:1280px; margin:0 auto; padding:0 28px; }}
  .section-eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.2em; text-transform:uppercase; color:#e11320; font-weight:600; margin-bottom:18px; }}
  h2 {{ font-size:clamp(30px,3.8vw,52px); font-weight:800; letter-spacing:-.025em; color:#fff; line-height:1.1; margin:0 0 24px; max-width:880px; }}
  .lede {{ font-size:clamp(17px,1.4vw,20px); line-height:1.65; color:rgba(232,236,242,.82); max-width:780px; margin:0 0 56px; }}
  p {{ font-size:17px; line-height:1.7; color:rgba(232,236,242,.82); max-width:780px; margin:0 0 22px; }}
  a {{ color:#e11320; text-decoration:underline; text-underline-offset:3px; }}
  a:hover {{ color:#fff; }}

  .stats-strip {{ display:grid; grid-template-columns:repeat(4,1fr); gap:0; border-top:1px solid rgba(255,255,255,.12); padding-top:32px; max-width:980px; margin-top:40px; }}
  .stat {{ padding-right:28px; }}
  .stat-num {{ font-size:clamp(32px,3.4vw,44px); font-weight:800; letter-spacing:-.02em; color:#fff; line-height:1; margin-bottom:6px; }}
  .stat-num .accent {{ color:#e11320; }}
  .stat-label {{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.6); font-weight:600; }}

  .region-block {{ margin-bottom:56px; }}
  .region-header {{ margin-bottom:20px; padding-bottom:14px; border-bottom:1px solid rgba(255,255,255,.1); }}
  .region-header h3 {{ font-size:24px; font-weight:700; color:#fff; margin:0 0 6px; letter-spacing:-.015em; }}
  .region-meta {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:#e11320; font-weight:600; }}
  .city-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:8px; }}
  .city-link {{ display:block; padding:14px 18px; background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.07); border-radius:6px; color:#fff; text-decoration:none; font-size:15px; font-weight:500; letter-spacing:-.005em; transition:all .2s; }}
  .city-link:hover {{ border-color:rgba(225,19,32,.5); background:rgba(225,19,32,.06); color:#fff; }}

  .quick-answer {{ background:linear-gradient(180deg,rgba(225,19,32,.04) 0%,rgba(225,19,32,.01) 100%); border:1px solid rgba(225,19,32,.18); border-left:3px solid #e11320; padding:36px 40px; border-radius:6px; }}
  .quick-answer-label {{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:.18em; text-transform:uppercase; color:#e11320; font-weight:600; margin-bottom:14px; }}
  .quick-answer p {{ font-size:19px; line-height:1.65; color:#fff; max-width:none; margin:0; }}
  .quick-answer p + p {{ margin-top:16px; }}
  .quick-answer strong {{ color:#fff; }}

  .final-cta {{ background:linear-gradient(135deg,#0e284f 0%,#050a12 100%); border-top:1px solid rgba(225,19,32,.25); padding:clamp(80px,9vw,120px) 0; text-align:center; position:relative; overflow:hidden; }}
  .final-cta::before {{ content:''; position:absolute; inset:0; background:radial-gradient(circle at 50% 30%,rgba(225,19,32,.12) 0%,transparent 60%); }}
  .final-cta-inner {{ position:relative; z-index:1; max-width:880px; margin:0 auto; padding:0 28px; }}
  .final-cta h2 {{ font-size:clamp(32px,4.5vw,60px); }}

  footer {{ background:#030610; border-top:1px solid rgba(255,255,255,.06); padding:56px 0 36px; color:rgba(232,236,242,.6); font-size:13px; }}
  footer .footer-inner {{ max-width:1280px; margin:0 auto; padding:0 28px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:14px; }}

  @media (max-width:880px) {{
    .nav-links a:not(.nav-cta) {{ display:none; }}
    .stats-strip {{ grid-template-columns:repeat(2,1fr); gap:24px 0; }}
    .city-grid {{ grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); }}
  }}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo"><img src="/images/acg-logo-nav@2x.png" alt="American Commercial Glass"></a>
    <div class="nav-links">
      <a href="/portfolio.html">Portfolio</a>
      <a href="/services.html">Services</a>
      <a href="/about.html">About</a>
      <a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="hero-bg">
    <picture>
      <source type="image/webp" srcset="/images/projects/eau-palm-beach/aerial-resort.webp">
      <img src="/images/projects/eau-palm-beach/aerial-resort.jpg" alt="Eau Palm Beach Resort — Florida commercial glazing by ACG" loading="eager" fetchpriority="high">
    </picture>
  </div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="eyebrow">
      <span class="dot"></span> FLORIDA STATEWIDE COVERAGE
      <span class="bar"></span> {total} CITIES &middot; LICENSED &middot; BONDED
    </div>
    <h1>Storefront Glazier in<br>Florida.<br><span class="accent">{total} cities. One license.</span></h1>
    <p class="hero-sub">American Commercial Glass delivers commercial storefront glazing across {total} Florida cities &mdash; from Key West to Jacksonville, Miami Beach to Marco Island. Florida CGC #1531993. 350+ commercial projects. $6M bonded. 48-hour bid on complete RFQ.</p>
    <div class="hero-actions">
      <a href="/send-plans.html" class="btn-primary">Send Us Plans &mdash; 48-Hour Bid <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
      <a href="tel:+17724867711" class="btn-ghost">(772) 486-7711</a>
    </div>
    <div class="stats-strip">
      <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Florida Cities<br>Served</div></div>
      <div class="stat"><div class="stat-num">350<span class="accent">+</span></div><div class="stat-label">Commercial<br>Projects</div></div>
      <div class="stat"><div class="stat-num">$6<span class="accent">M</span></div><div class="stat-label">Aggregate<br>Bonded</div></div>
      <div class="stat"><div class="stat-num">48<span class="accent">HR</span></div><div class="stat-label">Bid Turnaround<br>on Complete RFQ</div></div>
    </div>
  </div>
</header>

<main>
  <section>
    <div class="container">
      <div class="quick-answer">
        <div class="quick-answer-label">DIRECT ANSWER</div>
        <p><strong>American Commercial Glass (ACG)</strong> is the licensed commercial storefront glazier serving {total} Florida cities under Florida CGC #1531993. Three operating offices &mdash; West Palm Beach HQ, Naples, and Tampa &mdash; cover the state. $3M general liability, $6M aggregate bonded, 350+ commercial projects shipped since 2021.</p>
        <p>Find your city below and click through for the local storefront glazier page with building code context, project portfolio, transparent pricing, and a 48-hour bid path. Or send drawings directly to <a href="mailto:connor@acglass.com">connor@acglass.com</a> &mdash; we'll route to the right office.</p>
      </div>
    </div>
  </section>

  <section class="alt">
    <div class="container">
      <div class="section-eyebrow">FLORIDA CITY DIRECTORY</div>
      <h2>All {total} cities, organized by region.</h2>
      <p class="lede">Click any city for the dedicated storefront glazier page with local building code (HVHZ vs FBC), AHJ guidance, regional project portfolio, and pricing.</p>
{regions_html}
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-eyebrow">WHY THIS MATTERS</div>
      <h2>One license. {total} markets. Same crew structure.</h2>
      <p>Florida CGC #1531993 is statewide. The license covers commercial scope from Key West to Pensacola. We don't subcontract out by region &mdash; the same ACG project management runs every city, with three operating offices that own their respective markets:</p>
      <p><strong>West Palm Beach HQ</strong> covers Palm Beach County, Broward (HVHZ), Miami-Dade (HVHZ), Martin, St. Lucie, Indian River, and the Florida Keys. Drive time across this territory is 30 minutes to 6 hours depending on submarket. <strong>Naples office</strong> covers Collier, Lee, and Charlotte counties &mdash; the Gulf Coast SW Florida market. <strong>Tampa office</strong> covers Hillsborough, Pinellas, Sarasota, Manatee, Pasco, Polk, Orange, and the Central Florida and Tampa Bay corridors.</p>
      <p>Every page in this directory is written by Connor Walsh, President of American Commercial Glass, and reviewed against our actual field experience. Building code context (HVHZ vs FBC vs Wind Zone 4), AHJ submittal preferences, recent project portfolio, and per-square-foot pricing are all city-specific. This isn't programmatic boilerplate &mdash; it's the working knowledge of a contractor who has actually run scope in each market.</p>
    </div>
  </section>

  <section class="final-cta">
    <div class="final-cta-inner">
      <h2>Get a real Florida storefront number in 48 hours.</h2>
      <p style="font-size:clamp(17px,1.5vw,21px);line-height:1.55;color:rgba(232,236,242,.8);margin:0 auto 36px;max-width:640px;">Send drawings, scope, and schedule. We'll come back with a line-itemized bid, system recommendation, and a lead-time commitment. No mystery numbers.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
        <a href="/send-plans.html" class="btn-primary">Send Us Plans</a>
        <a href="tel:+17724867711" class="btn-ghost">Call (772) 486-7711</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="footer-inner">
    <div>&copy; 2026 American Commercial Glass, LLC. FL CGC #1531993. 700 S Rosemary Ave #204, West Palm Beach, FL 33401.</div>
    <div>Florida statewide storefront glazier &middot; <a href="/acg-glass-florida/" style="color:rgba(232,236,242,.75);">ACG Glass = American Commercial Glass</a></div>
  </div>
</footer>

</body>
</html>
"""

os.makedirs(os.path.join(ROOT, "storefront-glazier-florida"), exist_ok=True)
out_path = os.path.join(ROOT, "storefront-glazier-florida", "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_out)
print(f"OK {len(html_out):,} bytes: /storefront-glazier-florida/")
print(f"Total cities listed: {total}")
