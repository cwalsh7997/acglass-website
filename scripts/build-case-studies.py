#!/usr/bin/env python3
"""T1.4 — Build 4 HTML case studies from the project PDFs.

Strict rule: every fact in the case study text must come from the source PDF.
Use existing /images/projects/<slug>/ images. JSON-LD Article with about: #org.
Self-canonical. Add to sitemap-pages.xml. Link from matching service page.
"""
import json
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# Per-case data — facts read directly from the PDFs above. Image dirs verified to exist.
CASES = [
    {
        'slug': 'wild-blue-clubhouse',
        'pdf': '/pdfs/projects/acg-wild-blue-clubhouse.pdf',
        'images_dir': '/images/projects/wild-blue',
        'hero_basename': 'wild-blue-hero-progress',
        'eyebrow': 'The signature amenity of a Lee County master plan',
        'title_h1': 'Wild Blue Clubhouse',
        'location': 'Wild Blue at Waterside, Fort Myers, FL',
        'meta_title': 'Wild Blue Clubhouse, Fort Myers — Case Study | ACG',  # ≤60
        'meta_desc': 'ACG case study: 35,000 SF amenity at Wild Blue, Fort Myers, FL — dormer storefront on three elevations, feature entry doors, impact-rated to Lee County code.',
        'fact_box': [
            ('Developer', 'Stock Development'),
            ('General Contractor', 'Curran Young Construction'),
            ('Building Type', 'Private Club Amenity'),
            ('Scope', '35,000 SF Amenity Building / Dormer Storefront + Feature Entry Doors'),
            ('Glazing System', 'Impact Storefront + Custom Feature Doors'),
            ('Location', 'Wild Blue at Waterside, Fort Myers, FL'),
        ],
        'paragraphs': [
            "The Wild Blue Clubhouse is the social center of one of Southwest Florida's largest private master plans — a 3,500-acre lakefront community built around two deep-water lakes. The clubhouse had to carry the weight of that promise at street level, which meant the glazing package had to read as architecture, not as millwork.",
            "ACG delivered the full exterior envelope: dormer storefront on three elevations, feature entry door sets at the porte-cochère, and the rear elevation onto the lawn that opens to the waterfront. Everything was hurricane-rated to Lee County's current code, and everything was detailed to sit flush inside the stone and stucco surround that the architect specified.",
            "Curran Young managed the trade stack with ACG holding the critical path on envelope close-in. The clubhouse opened for the 2025 club season on schedule, and has since driven home-site absorption across the community.",
        ],
        'image_alts': {
            'wild-blue-front-elevation': 'Wild Blue Clubhouse front elevation — dormer storefront over stone surround',
            'wild-blue-entry-doors': 'Wild Blue Clubhouse feature entry doors at the porte-cochère',
            'wild-blue-architectural-detail': 'Wild Blue Clubhouse architectural detail — flush frame within stone surround',
            'wild-blue-rear-elevation': 'Wild Blue Clubhouse rear elevation onto the lawn and waterfront',
        },
        'link_from': ['commercial-storefront-systems.html', 'impact-windows-doors.html'],
        'related_service': ('/commercial-storefront-systems.html', 'Commercial Storefront Systems'),
    },
    {
        'slug': 'atlantic-fields-golf-house',
        'pdf': '/pdfs/projects/acg-atlantic-fields-golf-house.pdf',
        'images_dir': '/images/projects/atlantic-fields-golf-house',
        'hero_basename': 'hero-golden-hour',
        'eyebrow': 'A glass amenity building on the course',
        'title_h1': 'Atlantic Fields Golf House',
        'location': 'Atlantic Fields, Hobe Sound, FL',
        'meta_title': 'Atlantic Fields Golf House, Hobe Sound — Case Study | ACG',  # 59
        'meta_desc': 'ACG case study: Discovery Land Golf House at Atlantic Fields, Hobe Sound, FL — oversized lift-and-slide doors with impact storefront balance.',
        'fact_box': [
            ('Developer', 'Discovery Land Company'),
            ('Building Type', 'Private Club Amenity'),
            ('Scope', 'Clubhouse Amenity / Full-Height Glass Walls / Lift-and-Slide Door System'),
            ('Glazing System', 'Lift-and-Slide Doors + Impact Storefront'),
            ('Key Feature', 'Fully Open-Wall to Golf Course'),
            ('Location', 'Atlantic Fields, Hobe Sound, FL'),
        ],
        'paragraphs': [
            "The Golf House at Atlantic Fields is a Discovery Land amenity building set inside one of the most exclusive new private clubs in Florida. The design is simple and severe: a low, wide structure that opens the entire length of one elevation onto the course.",
            "ACG installed the full glass-wall package that makes that gesture work. Oversized lift-and-slide door sets run the length of the course-side elevation. When retracted, the building has no wall between the interior lounge and the first tee. Impact storefront frames the balance of the envelope, and the finished clubhouse reads as architecture, not as a box with windows cut into it.",
            "The install was coordinated with Discovery Land's finish standards — fittings, thresholds, and reveals all specified to the same tolerance as millwork. The result is the amenity building the club uses on every marketing tour.",
        ],
        'image_alts': {
            'hero-golden-hour': 'Atlantic Fields Golf House — exterior at golden hour with course beyond',
            'hero-open-wall': 'Atlantic Fields Golf House — lift-and-slide doors retracted, open to the course',
            'interior-glass-wall': 'Atlantic Fields Golf House — interior view through the full-height glass wall',
            'entry-path': 'Atlantic Fields Golf House — entry path between the palms',
            'dining-interior': 'Atlantic Fields Golf House — interior dining with full-height glass to the course',
        },
        'link_from': ['multi-slide-bifold-doors.html', 'curtainwall-systems.html'],
        'related_service': ('/multi-slide-bifold-doors.html', 'Multi-Slide & Bi-Fold Doors'),
    },
    {
        'slug': 'ocean-prime-ft-lauderdale',
        'pdf': '/pdfs/projects/acg-ocean-prime-ft-lauderdale.pdf',
        'images_dir': '/images/projects/ocean-prime-ft-lauderdale',
        'hero_basename': 'ocean-prime-ftl-twilight-exterior',
        'eyebrow': 'Waterfront Euro-Wall for a flagship restaurant',
        'title_h1': 'Ocean Prime Fort Lauderdale',
        'location': '401 E Las Olas Blvd, Fort Lauderdale, FL',
        'meta_title': 'Ocean Prime Fort Lauderdale — Case Study | ACG',  # 49
        'meta_desc': 'ACG case study: Ocean Prime Fort Lauderdale — full Euro-Wall folding and sliding wall package for a New River waterfront flagship restaurant.',
        'fact_box': [
            ('Owner', 'Cameron Mitchell Restaurants'),
            ('Architect', 'Kobi Karp Architecture'),
            ('Building Type', 'Waterfront Hospitality'),
            ('Scope', '18,000 SF / Waterfront Dining / Full Euro-Wall Folding + Sliding Package'),
            ('Glazing System', 'Euro-Wall Folding & Sliding Walls'),
            ('Location', '401 E Las Olas Blvd, Fort Lauderdale, FL'),
        ],
        'paragraphs': [
            "Ocean Prime Fort Lauderdale sits directly on the New River, and the architectural premise is that the restaurant's interior, exterior terrace, and the water should read as one continuous room. That premise only works if the glazing disappears.",
            "ACG installed the complete Euro-Wall folding and sliding wall package — a system ACG is authorized to install as one of the manufacturer's Florida dealers. When the weather allows, the entire façade folds away, and the dining room spills onto the waterfront terrace. When it closes, the same façade seals against Florida heat, salt air, and wind-borne rain.",
            "The project was coordinated with Kobi Karp Architecture from shop-drawing phase forward. ACG worked through sill detailing, threshold transitions, and structural coordination with the waterfront slab to keep the sightlines low, the frames minimal, and the finished thresholds flush. The building opened on time and has since become one of the highest-visibility restaurants in downtown Fort Lauderdale.",
        ],
        'image_alts': {
            'ocean-prime-ftl-twilight-exterior': 'Ocean Prime Fort Lauderdale exterior at twilight — Euro-Wall facade closed, signage lit',
            'ocean-prime-ftl-marina-aerial': 'Ocean Prime Fort Lauderdale aerial — New River waterfront and restaurant',
            'ocean-prime-ftl-interior-dining': 'Ocean Prime Fort Lauderdale interior dining with glass facade open to terrace',
        },
        'link_from': ['multi-slide-bifold-doors.html', 'restaurant-glazing-florida.html'],
        'related_service': ('/multi-slide-bifold-doors.html', 'Multi-Slide & Bi-Fold Doors'),
    },
    {
        'slug': 'gulfside-twelve',
        'pdf': '/pdfs/projects/acg-gulfside-twelve.pdf',
        'images_dir': '/images/projects/gulfside-twelve',
        'hero_basename': 'hero-twilight-beachfront',
        'eyebrow': 'Rebuilt to withstand the next storm',
        'title_h1': 'Gulfside Twelve',
        'location': 'Fort Myers Beach, Florida',
        'meta_title': 'Gulfside Twelve, Fort Myers Beach — Case Study | ACG',  # 56
        'meta_desc': 'ACG case study: Gulfside Twelve, the post-Ian rebuild on Estero Boulevard — full-building PGT impact package across 12 beachfront residences.',
        'fact_box': [
            ('Developer', 'Gulfside Development'),
            ('General Contractor', 'New Age Development'),
            ('Building Type', 'Luxury Beachfront Multifamily'),
            ('Scope', '12 Residences / Beachfront Condominium / Full-building PGT Impact Package'),
            ('Glazing System', 'PGT Impact Windows + Sliding Glass Doors'),
            ('Location', 'Fort Myers Beach, Florida'),
        ],
        'paragraphs': [
            "When Hurricane Ian tore across Fort Myers Beach in 2022, it left the barrier island unrecognizable. Gulfside Twelve — the rebuild on Estero Boulevard — was designed to answer that damage with a building envelope that will not blink at the next one.",
            "ACG delivered the complete glazing package: PGT impact-rated window walls on the Gulf-facing elevations, oversized sliding glass doors to every residence, interior glass-door systems, and the full lobby and amenity storefront. Each opening was installed to the Florida Product Approval and High-Velocity Hurricane Zone requirements for Lee County coastal construction.",
            "The brief from New Age Development was uncompromising. Hit the tight post-Ian delivery schedule, stage 12 identical units without disrupting the trade stack, and produce a glass-wall experience that justifies the price per square foot of Fort Myers Beach oceanfront. ACG hit every install window on the schedule and turned the building over to commissioning on time.",
            "The finished residences read the way the renderings promised: a continuous plane of glass between the interior and the Gulf. The building is now the reference standard for what hurricane-zone multifamily should look like in the next cycle.",
        ],
        'image_alts': {
            'hero-twilight-beachfront': 'Gulfside Twelve at twilight — beachfront elevation with impact window walls',
            'aerial-pink-sunset': 'Gulfside Twelve aerial at sunset — Gulf-facing facade',
            'aerial-sunset-beach': 'Gulfside Twelve aerial — beachfront context',
            'balcony-sunset-gulf': 'Gulfside Twelve balcony at sunset facing the Gulf',
            'living-room-glass-doors': 'Gulfside Twelve living room — full-height impact sliding glass doors',
        },
        'link_from': ['impact-windows-doors.html', 'multifamily-glazing.html'],
        'related_service': ('/impact-windows-doors.html', 'Impact Windows & Doors'),
    },
]


def render_case(case):
    canonical = f"https://acglass.com/projects/{case['slug']}.html"
    
    fact_rows = ''.join(
        f'<div class="fact-row"><div class="fact-label">{k}</div><div class="fact-value">{v}</div></div>'
        for k, v in case['fact_box']
    )
    
    paragraphs = ''.join(f'<p>{p}</p>' for p in case['paragraphs'])
    
    # Build gallery from existing image basenames
    gallery_html = ''
    for basename, alt in case['image_alts'].items():
        gallery_html += f'''
        <figure class="case-figure">
          <picture>
            <source srcset="{case['images_dir']}/{basename}.avif" type="image/avif">
            <source srcset="{case['images_dir']}/{basename}.webp" type="image/webp">
            <img src="{case['images_dir']}/{basename}.jpg" alt="{alt}" loading="lazy" decoding="async" width="1200" height="800">
          </picture>
          <figcaption>{alt}</figcaption>
        </figure>'''
    
    # JSON-LD Article + BreadcrumbList
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{canonical}#article",
                "headline": case['title_h1'],
                "description": case['meta_desc'],
                "url": canonical,
                "datePublished": "2026-06-11",
                "dateModified": "2026-06-11",
                "image": f"https://acglass.com{case['images_dir']}/{case['hero_basename']}.jpg",
                "author": {"@id": "https://acglass.com/#org"},
                "publisher": {"@id": "https://acglass.com/#org"},
                "about": {"@id": "https://acglass.com/#org"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
                "isPartOf": {"@id": "https://acglass.com/#website"},
                "inLanguage": "en-US",
                "locationCreated": {
                    "@type": "Place",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": case['location'].split(',')[0].strip(),
                        "addressRegion": "FL",
                        "addressCountry": "US"
                    }
                },
                "associatedMedia": [
                    {
                        "@type": "MediaObject",
                        "encodingFormat": "application/pdf",
                        "contentUrl": f"https://acglass.com{case['pdf']}",
                        "name": f"{case['title_h1']} project sheet (PDF)"
                    }
                ]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Projects", "item": "https://acglass.com/projects/"},
                    {"@type": "ListItem", "position": 3, "name": case['title_h1'], "item": canonical}
                ]
            }
        ]
    }
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{case['meta_title']}</title>
  <meta name="description" content="{case['meta_desc']}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{case['meta_title']}">
  <meta property="og:description" content="{case['meta_desc']}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://acglass.com{case['images_dir']}/{case['hero_basename']}.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{case['meta_title']}">
  <meta name="twitter:description" content="{case['meta_desc']}">
  <meta name="theme-color" content="#0e284f">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
  <link rel="icon" href="/images/acg-favicon.svg" type="image/svg+xml">
  <script type="application/ld+json">
{json.dumps(jsonld, indent=2, ensure_ascii=False)}
  </script>
  <style>
    :root {{ --navy:#0e284f; --red:#e11320; --bg:#0a1628; --text:#fff; }}
    *{{box-sizing:border-box;}}
    body{{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);margin:0;line-height:1.65;}}
    a{{color:var(--red);}}
    .nav-bar{{position:sticky;top:0;background:rgba(10,22,40,0.92);backdrop-filter:blur(8px);z-index:50;padding:14px 24px;border-bottom:1px solid rgba(255,255,255,0.06);}}
    .nav-inner{{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:24px;font-size:14px;}}
    .nav-inner ul{{list-style:none;padding:0;margin:0;display:flex;gap:24px;}}
    .nav-inner a{{color:#fff;text-decoration:none;}}
    .case-hero{{padding:60px 24px 40px;max-width:1200px;margin:0 auto;}}
    .case-eyebrow{{font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--red);font-weight:700;margin-bottom:14px;}}
    .case-hero h1{{font-size:clamp(2rem,5vw,3.5rem);margin:0 0 12px;letter-spacing:-0.02em;line-height:1.05;}}
    .case-location{{font-size:14px;letter-spacing:0.06em;text-transform:uppercase;color:rgba(255,255,255,0.6);margin:0 0 28px;}}
    .case-hero-image{{margin:0 -24px 40px;}}
    .case-hero-image img{{width:100%;height:auto;display:block;}}
    .case-content{{max-width:880px;margin:0 auto;padding:0 24px 60px;}}
    .case-fact-box{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;margin:0 0 40px;padding:28px;background:rgba(255,255,255,0.03);border-left:3px solid var(--red);border-radius:6px;}}
    .fact-row{{display:flex;flex-direction:column;gap:4px;}}
    .fact-label{{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--red);font-weight:700;}}
    .fact-value{{font-size:15px;color:rgba(255,255,255,0.95);line-height:1.5;}}
    .case-content p{{font-size:17px;color:rgba(255,255,255,0.88);margin:0 0 22px;}}
    .case-gallery{{max-width:1200px;margin:0 auto;padding:0 24px 60px;display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:24px;}}
    .case-figure{{margin:0;}}
    .case-figure img{{width:100%;height:auto;display:block;border-radius:6px;}}
    .case-figure figcaption{{font-size:13px;color:rgba(255,255,255,0.55);padding:10px 4px 0;font-style:italic;}}
    .case-cta{{max-width:880px;margin:40px auto 60px;padding:32px;text-align:center;background:linear-gradient(135deg,rgba(225,19,32,0.12),rgba(225,19,32,0.04));border:1px solid rgba(225,19,32,0.3);border-radius:8px;}}
    .case-cta h2{{margin:0 0 12px;font-size:1.4rem;}}
    .case-cta a.btn{{display:inline-block;padding:14px 32px;background:var(--red);color:#fff;text-decoration:none;border-radius:6px;font-weight:600;margin-top:8px;}}
    .case-resources{{max-width:880px;margin:24px auto 0;padding:0 24px;font-size:14px;color:rgba(255,255,255,0.7);}}
    .case-resources a{{font-weight:600;}}
    footer{{background:var(--navy);padding:40px 24px;color:rgba(255,255,255,0.7);font-size:13px;text-align:center;}}
  </style>
</head>
<body>
  <nav class="nav-bar"><div class="nav-inner">
    <a href="/" style="font-weight:800;">ACG</a>
    <ul>
      <li><a href="/services.html">Services</a></li>
      <li><a href="/portfolio.html">Projects</a></li>
      <li><a href="/manufacturers.html">Manufacturers</a></li>
      <li><a href="/noa/">NOA Hub</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/contact.html">Contact</a></li>
    </ul>
  </div></nav>

  <main>
    <section class="case-hero">
      <div class="case-eyebrow">{case['eyebrow']}</div>
      <h1>{case['title_h1']}</h1>
      <p class="case-location">{case['location']}</p>
    </section>

    <div class="case-hero-image" style="max-width:1200px;margin:0 auto 40px;padding:0 24px;">
      <picture>
        <source srcset="{case['images_dir']}/{case['hero_basename']}.avif" type="image/avif">
        <source srcset="{case['images_dir']}/{case['hero_basename']}.webp" type="image/webp">
        <img src="{case['images_dir']}/{case['hero_basename']}.jpg" alt="{case['title_h1']} — hero image" loading="eager" decoding="async" width="1600" height="1067" style="border-radius:6px;">
      </picture>
    </div>

    <section class="case-content">
      <div class="case-fact-box">
        {fact_rows}
      </div>
      {paragraphs}
    </section>

    <section class="case-gallery">{gallery_html}
    </section>

    <section class="case-resources">
      <p><strong>Download:</strong> <a href="{case['pdf']}">Project sheet (PDF)</a> · <strong>Related service:</strong> <a href="{case['related_service'][0]}">{case['related_service'][1]}</a></p>
    </section>

    <section class="case-cta">
      <h2>Have a similar scope?</h2>
      <p style="margin:0 0 20px;color:rgba(255,255,255,0.85);">Send drawings and a bid date — ACG returns a Division 08 scope letter within 48 hours.</p>
      <a class="btn" href="/contact.html">Request a scope letter &rarr;</a>
    </section>
  </main>

  <footer>
    &copy; 2026 American Commercial Glass, Inc. · FL CGC #1531993 · <a href="/" style="color:#fff;">acglass.com</a>
  </footer>
</body>
</html>
'''
    return html


# Generate cases
projects_dir = ROOT / 'projects'
projects_dir.mkdir(exist_ok=True)
for case in CASES:
    out = projects_dir / f"{case['slug']}.html"
    out.write_text(render_case(case))
    print(f"WROTE: {out.relative_to(ROOT)}")
    # Validate meta length
    import re as _re
    c = out.read_text()
    t = _re.search(r'<title>([^<]+)</title>', c).group(1)
    d = _re.search(r'<meta name="description" content="([^"]+)"', c).group(1)
    print(f"  T({len(t)}): {t}")
    print(f"  D({len(d)}): {d}")


# Add to sitemap-pages.xml and sitemap.xml
TODAY = '2026-06-11'
NEW_URLS = [f"https://acglass.com/projects/{c['slug']}.html" for c in CASES]
for sm in ['sitemap.xml', 'sitemap-pages.xml']:
    p = ROOT / sm
    c = p.read_text()
    entries = ''.join(
        f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.75</priority>\n  </url>\n'
        for u in NEW_URLS if u not in c
    )
    if entries:
        c = c.replace('</urlset>', entries + '</urlset>', 1)
        p.write_text(c)
        print(f"Added {len(NEW_URLS)} URLs to {sm}")
    else:
        print(f"All URLs already in {sm}")

# Validate XML
import xml.etree.ElementTree as ET
for sm in ['sitemap.xml','sitemap-pages.xml']:
    ET.parse(ROOT / sm)
    print(f"VALID: {sm}")
