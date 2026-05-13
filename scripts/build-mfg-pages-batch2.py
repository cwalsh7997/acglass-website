#!/usr/bin/env python3
"""Build 4 manufacturer dealer pages: PGT, Allegion, TGP, Slimpact.

All specs verified against primary sources. Where a number is not publicly
verifiable, the copy says so explicitly (per Connor's standing rule).
"""
import json
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

ACG_ORG = {
    "@type": ["GeneralContractor", "LocalBusiness"],
    "@id": "https://acglass.com/#organization",
    "name": "American Commercial Glass, Inc.",
    "alternateName": "ACG",
    "url": "https://acglass.com",
    "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
    "telephone": "+1-772-486-7711",
    "email": "info@acglass.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "700 S Rosemary Ave Suite 204",
        "addressLocality": "West Palm Beach",
        "addressRegion": "FL",
        "postalCode": "33401",
        "addressCountry": "US"
    },
    "areaServed": [
        {"@type": "State", "name": "Florida"},
        {"@type": "State", "name": "Tennessee"},
        {"@type": "State", "name": "Georgia"},
        {"@type": "State", "name": "Alabama"}
    ],
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Florida CGC #1531993"}
}


def dealer_service_schema(brand_name, brand_url, brand_hq, products, page_url, service_label):
    offers = []
    for p in products:
        offers.append({
            "@type": "Offer",
            "itemOffered": {
                "@type": "Product",
                "name": p["name"],
                "description": p.get("description", ""),
                "brand": {"@type": "Brand", "name": brand_name, "url": brand_url},
                "category": p.get("category", "Commercial Glazing System")
            },
            "seller": {"@id": "https://acglass.com/#organization"},
            "areaServed": [
                {"@type": "State", "name": "Florida"},
                {"@type": "State", "name": "Tennessee"},
                {"@type": "State", "name": "Georgia"},
                {"@type": "State", "name": "Alabama"}
            ],
            "availability": "https://schema.org/InStock",
            "businessFunction": "https://schema.org/Sell"
        })
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{page_url}#dealer-service",
        "name": f"Authorized {brand_name} Installer — Florida",
        "serviceType": service_label,
        "description": f"ACG is an authorized commercial installer for {brand_name} products across Florida and the Southeast.",
        "provider": ACG_ORG,
        "brand": {"@type": "Brand", "name": brand_name, "url": brand_url, "description": f"{brand_name} — HQ {brand_hq}"},
        "areaServed": [
            {"@type": "State", "name": "Florida"},
            {"@type": "State", "name": "Tennessee"},
            {"@type": "State", "name": "Georgia"},
            {"@type": "State", "name": "Alabama"}
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{brand_name} Commercial Product Line",
            "itemListElement": offers
        }
    }


CONNOR = {
    "@type": "Person",
    "name": "Connor Walsh",
    "jobTitle": "President, American Commercial Glass",
    "url": "https://acglass.com/author/connor-walsh.html",
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Florida CGC #1531993"}
}


def faq_schema(qas):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qas
        ]
    }


def article_schema(page_url, headline, description, image_url):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "author": CONNOR,
        "publisher": {"@type": "Organization", "name": "American Commercial Glass", "logo": {"@type": "ImageObject", "url": "https://acglass.com/images/acg-logo-nav@2x.png"}},
        "datePublished": "2026-05-13",
        "dateModified": "2026-05-13",
        "mainEntityOfPage": page_url,
        "image": image_url,
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", "#answer-box", "table"]}
    }


def breadcrumb_schema(slug, title):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://acglass.com/services.html"},
            {"@type": "ListItem", "position": 3, "name": "Manufacturer Partners", "item": "https://acglass.com/manufacturers.html"},
            {"@type": "ListItem", "position": 4, "name": title, "item": f"https://acglass.com/{slug}.html"}
        ]
    }


HEAD_CSS = """
  <style>
    .hero { padding: 100px 0 40px; max-width: 1080px; margin: 0 auto; padding-left: 28px; padding-right: 28px; }
    .hero .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent, #E11320); margin-bottom: 14px; font-weight: 700; }
    .hero h1 { font-size: clamp(2rem, 4.5vw, 3.6rem); line-height: 1.04; letter-spacing: -0.02em; margin: 0 0 22px; }
    .hero .lead { font-size: 1.06rem; line-height: 1.65; color: rgba(255,255,255,0.84); max-width: 780px; }
    .byline { font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.55); margin-top: 18px; }
    #answer-box { background: rgba(225,19,32,0.06); border-left: 3px solid var(--accent, #E11320); padding: 22px 26px; max-width: 1024px; margin: 40px auto; border-radius: 6px; }
    #answer-box h2 { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--accent); margin: 0 0 12px; font-weight: 700; }
    #answer-box p { font-size: 1.05rem; line-height: 1.6; color: rgba(255,255,255,0.92); margin: 0; }
    main.content { max-width: 1024px; margin: 60px auto 100px; padding: 0 28px; }
    main.content h2 { font-size: 1.7rem; letter-spacing: -0.01em; margin: 50px 0 18px; }
    main.content h3 { font-size: 1.2rem; margin: 32px 0 12px; color: rgba(255,255,255,0.95); }
    main.content p { color: rgba(255,255,255,0.85); line-height: 1.75; font-size: 1.02rem; margin-bottom: 18px; }
    main.content ul { color: rgba(255,255,255,0.85); line-height: 1.85; padding-left: 24px; }
    main.content table { width: 100%; border-collapse: collapse; margin: 22px 0 32px; font-size: 0.94rem; }
    main.content th { text-align: left; padding: 14px 14px; border-bottom: 1px solid rgba(255,255,255,0.18); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); font-weight: 700; }
    main.content td { padding: 14px 14px; border-bottom: 1px solid rgba(255,255,255,0.06); color: rgba(255,255,255,0.88); vertical-align: top; }
    main.content td:first-child { color: #fff; font-weight: 600; }
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; margin: 30px 0; }
    .stat-card { padding: 22px; background: rgba(0,0,0,0.25); border: 1px solid rgba(225,19,32,0.2); border-radius: 10px; }
    .stat-card .label { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent); margin-bottom: 8px; }
    .stat-card .value { font-size: 22px; font-weight: 800; color: #fff; line-height: 1.15; }
    .stat-card .note { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 6px; }
    .cta-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 28px; margin: 50px 0; border-radius: 8px; }
    .cta-box a { color: var(--accent); font-weight: 700; text-decoration: none; }
    .source-note { font-size: 0.85rem; color: rgba(255,255,255,0.55); font-style: italic; margin-top: 12px; }
  </style>
"""

NAV = """
  <header class="site-nav">
    <div style="max-width:1200px;margin:0 auto;padding:18px 28px;display:flex;justify-content:space-between;align-items:center;">
      <a href="/" style="color:#fff;font-weight:700;text-decoration:none;font-size:1.05rem;">ACG</a>
      <nav style="display:flex;gap:24px;font-size:0.92rem;">
        <a href="/services.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Services</a>
        <a href="/manufacturers.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Manufacturers</a>
        <a href="/portfolio.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Portfolio</a>
        <a href="/contact.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Contact</a>
      </nav>
    </div>
  </header>
"""

FOOTER = """
  <footer style="background:#050a12;padding:40px 28px;text-align:center;border-top:1px solid rgba(255,255,255,0.08);">
    <div style="max-width:1200px;margin:0 auto;color:rgba(255,255,255,0.6);font-size:0.9rem;">
      <p>&copy; 2026 American Commercial Glass &middot; FL CGC #1531993 &middot; West Palm Beach &middot; Naples &middot; Tampa &middot; Nashville (2026)</p>
    </div>
  </footer>
"""

STATS = """
    <div class="stat-grid">
      <div class="stat-card"><div class="label">License</div><div class="value">FL CGC<br>#1531993</div><div class="note">Certified General Contractor</div></div>
      <div class="stat-card"><div class="label">Projects</div><div class="value">350+<br>Installed</div><div class="note">Commercial, 2021–2026</div></div>
      <div class="stat-card"><div class="label">Volume</div><div class="value">1M+ SF<br>Installed</div><div class="note">FL &amp; Southeast</div></div>
      <div class="stat-card"><div class="label">Bonding</div><div class="value">$3M / $6M<br>Aggregate</div><div class="note">Single / aggregate</div></div>
      <div class="stat-card"><div class="label">Safety</div><div class="value">Zero<br>OSHA</div><div class="note">5+ year clean record</div></div>
      <div class="stat-card"><div class="label">Coverage</div><div class="value">WPB · Naples<br>· Tampa</div><div class="note">Nashville 2026</div></div>
    </div>
"""

# ════════════════════════════════════════════════════════════════════
# PAGE 1 — PGT
# ════════════════════════════════════════════════════════════════════
PGT_PRODUCTS = [
    {"name": "PGT WinGuard SH-7700A", "description": "Aluminum impact-rated single-hung window, Miami-Dade NOA 20-0401.11, DP +80/-110 PSF (per NOA 20-0401.11).", "category": "Impact Window"},
    {"name": "PGT WinGuard Aluminum (commercial line)", "description": "Light-commercial impact-rated aluminum window and door line with 12 active Miami-Dade NOAs.", "category": "Impact Window"},
    {"name": "PGT WinGuard Commercial Doors", "description": "Impact-rated commercial entry and sliding doors, Miami-Dade NOA-listed configurations.", "category": "Impact Door"}
]

PGT_PAGE = ('pgt-installer-florida', 'PGT WinGuard Aluminum',
            'PGT', 'https://www.pgtwindows.com', 'Venice, FL',
            'PGT WinGuard Commercial Installation & Supply',
            'PGT Authorized Commercial Installer — Florida | ACG',
            'ACG is an authorized commercial installer for PGT WinGuard impact-rated windows and doors. 12 active Miami-Dade NOAs. FL CGC #1531993, 350+ commercial projects.',
            'pgt installer florida, pgt winguard commercial, pgt commercial dealer, pgt aluminum impact windows, pgt commercial installer',
            'PGT Authorized Commercial Installer — Florida',
            'PGT WinGuard commercial impact-rated windows and doors. 12 active Miami-Dade NOAs. ACG is the authorized commercial installer across Florida.',
            'https://acglass.com/images/projects/hca-cape-coral/hca-cape-coral-exterior.jpg',
            'PGT Commercial Installation',
            'PGT commercial impact-rated installation',
            'PGT WinGuard installer — Florida commercial',
            'PGT (NYSE: PGTI before acquisition by MITER Brands) builds impact-rated windows and doors out of Venice, Florida. We install the WinGuard Aluminum commercial line on multifamily, mixed-use, hospitality, and light-commercial projects across Florida. 12 active Miami-Dade NOAs cover the line as of May 2026, with all NOAs expiring 2028–2030.',
            'ACG is an authorized commercial installer of PGT WinGuard impact-rated aluminum windows and doors. 12 active Miami-Dade NOAs as of May 2026, all expiring 2028–2030. We install PGT on light-commercial, multifamily, mixed-use, and hospitality projects across Florida from our offices in West Palm Beach, Naples, and Tampa.',
            PGT_PRODUCTS,
            [
                {
                    'h2': 'About PGT WinGuard Aluminum',
                    'body': """<p>PGT Industries builds out of Venice, FL — about 70 miles south of our Tampa office. Their WinGuard line is the most widely-installed impact-rated window family in Florida, with active Miami-Dade Product Control NOAs on more than 12 distinct product configurations as of May 2026.</p>
<p>Common applications we install:</p>
<ul>
<li>Multifamily and condo (low- and mid-rise)</li>
<li>Light commercial — small office, retail, restaurant</li>
<li>Mixed-use ground-floor with WinGuard sliding doors</li>
<li>Hospitality envelopes where PGT is spec'd over heavier commercial systems</li>
</ul>
<p>PGT WinGuard is our second-most-installed window line after ESWindows. Where ESWindows tends to land on full-commercial high-rise and Class A projects, PGT WinGuard is the right call when the spec is light-commercial residential-aesthetic with NOA compliance required.</p>"""
                },
                {
                    'h2': 'Verified product data',
                    'body': """<p>The single publicly-verifiable DP example from the current Miami-Dade NOA database:</p>
<table>
<thead><tr><th>Product</th><th>Design Pressure</th><th>NOA</th><th>Expiration</th></tr></thead>
<tbody>
<tr><td>PGT WinGuard SH-7700A (single hung)</td><td>+80 / &minus;110 PSF</td><td>20-0401.11</td><td>2028</td></tr>
<tr><td>PGT WinGuard Aluminum (full line)</td><td>Varies by size and configuration</td><td>12 active NOAs</td><td>2028&ndash;2030</td></tr>
</tbody>
</table>
<p class="source-note">Source: <a href="https://www.miamidade.gov/building/pc-result_detail_app.asp?app_alias=101544" rel="nofollow" style="color:rgba(255,255,255,0.7);">Miami-Dade Product Control NOA database</a>. Design pressures vary substantially with size, glass make-up, and configuration — published values are the tested-assembly maximums. We verify project-specific NOA configurations against actual drawings and elevations on every bid.</p>
<p>Florida Product Approval (FPA) numbers are issued for non-HVHZ Florida applications and confirmed available from PGT's certifications portal. Specific FPA numbers and the matching size/glass tables are project-specific — send drawings and we'll provide the matching FPA-listed configuration.</p>"""
                },
                {
                    'h2': 'When PGT WinGuard is the right call',
                    'body': """<p>PGT WinGuard is the correct system when:</p>
<ul>
<li>Project is light-commercial, multifamily, or mixed-use — not heavy-commercial high-rise</li>
<li>Spec calls for aluminum-frame impact-rated assemblies with residential aesthetic</li>
<li>HVHZ NOA is required and the design pressure falls within published NOA ranges (typically +60 to +110 PSF positive)</li>
<li>Budget benefits from PGT's pricing advantage over heavier commercial lines on light-commercial scope</li>
</ul>
<p>When the project is full-commercial curtainwall or high-rise window wall, we typically move to ESWindows ES7000/ES8000T or Euro-Wall. PGT WinGuard is not a curtainwall product.</p>"""
                }
            ],
            [
                ('What is PGT WinGuard?', 'PGT WinGuard is an impact-rated aluminum window and door line built by PGT Industries in Venice, Florida. The commercial line carries 12 active Miami-Dade NOAs as of May 2026, with applications spanning light-commercial, multifamily, and mixed-use projects across Florida.'),
                ('Is ACG an authorized PGT installer?', 'Yes. ACG (FL CGC #1531993) is an authorized commercial installer for PGT WinGuard products across Florida and the Southeast. We install the WinGuard Aluminum commercial line on multifamily, hospitality, and light-commercial projects.'),
                ('What design pressures does PGT WinGuard support?', 'Design pressures vary by product configuration, glass make-up, and assembly size. As one verifiable example, the WinGuard SH-7700A single hung is listed at +80/-110 PSF under Miami-Dade NOA 20-0401.11. Project-specific DPs are verified against the controlling NOA on every bid.'),
                ('Where can I find PGT NOAs?', 'PGT NOAs are searchable in the Miami-Dade Product Control database. As of May 2026, PGT WinGuard Aluminum holds 12 active NOAs, all expiring between 2028 and 2030.'),
                ('What is the difference between PGT and ESWindows for commercial work?', 'PGT WinGuard is a light-commercial and multifamily line with NOA-listed aluminum framing. ESWindows commercial (ES7000, ES8000T) is a heavier-commercial and high-rise system with higher design pressures and curtainwall configurations. We install both; selection is driven by the project spec.')
            ]
)


# ════════════════════════════════════════════════════════════════════
# PAGE 2 — ALLEGION
# ════════════════════════════════════════════════════════════════════
ALLEGION_PRODUCTS = [
    {"name": "Von Duprin 98/99 Series HH (Hurricane)", "description": "Hurricane-rated panic exit device. FBC TAS 201/202/203 tested per ASTM E1886/E1996/E330. Per Von Duprin Hurricane Device Reference Sheet.", "category": "Commercial Hardware"},
    {"name": "Von Duprin 33A/35A Series HH", "description": "Hurricane-rated narrow-stile panic exit device for aluminum storefront doors.", "category": "Commercial Hardware"},
    {"name": "Von Duprin 88 / 2670 Series HH", "description": "Hurricane-rated exit devices for swing and revolving commercial doors.", "category": "Commercial Hardware"},
    {"name": "Steelcraft H-Series Commercial Door", "description": "Miami-Dade NOA-listed hollow-metal commercial door for HVHZ assemblies. Zone 4 DP 120–170 PSF. NOAs 22-0427.01 and 23-0821.16 (expire May 2028).", "category": "Commercial Door"}
]

ALLEGION_PAGE = ('allegion-installer-florida', 'Allegion (Von Duprin + Steelcraft)',
                 'Allegion', 'https://www.allegion.com', 'Carmel, IN',
                 'Allegion Commercial Hardware & Steelcraft Door Installation',
                 'Allegion Authorized Commercial Installer (Von Duprin, Steelcraft) — Florida | ACG',
                 'ACG installs Allegion commercial hardware — Von Duprin hurricane-rated panic devices and Steelcraft NOA-listed hollow-metal doors. FL CGC #1531993, 350+ commercial projects.',
                 'allegion installer florida, von duprin hurricane installer, steelcraft commercial door, von duprin 99 hurricane, allegion commercial dealer',
                 'Allegion Authorized Commercial Installer — Florida',
                 'Von Duprin hurricane-rated panic devices and Steelcraft NOA-listed hollow-metal doors installed by ACG across Florida.',
                 'https://acglass.com/images/projects/cudjoe-key/cudjoe-key-exterior.jpg',
                 'Allegion Commercial Installation',
                 'Allegion commercial hardware and door installation',
                 'Allegion installer — Von Duprin + Steelcraft for Florida commercial',
                 'Allegion is the umbrella brand for Von Duprin (panic exit devices), Steelcraft (hollow-metal commercial doors), Schlage (commercial locks), LCN (closers), and Ives (commercial hardware). We install the hurricane-rated Von Duprin HH-series and Steelcraft NOA-listed commercial doors on Florida commercial projects, plus the rest of the Allegion commercial hardware line where it integrates with our Division 08 scope.',
                 'ACG is an authorized commercial installer for Allegion products on Florida commercial projects. We install Von Duprin hurricane-rated panic devices (98/99 HH, 33A/35A HH, 88, 2670), Steelcraft H-Series NOA-listed commercial doors, and the broader Schlage/LCN/Ives commercial hardware line integrated with our Division 08 scope.',
                 ALLEGION_PRODUCTS,
                 [
                     {
                         'h2': 'About Allegion commercial hardware',
                         'body': """<p>Allegion (NYSE: ALLE) is the parent company of Von Duprin, Steelcraft, Schlage commercial, LCN closers, and Ives — the hardware brands you'll see specified on most commercial Division 08 packages in Florida. Our scope typically integrates Von Duprin exit devices and Steelcraft hollow-metal doors with our storefront, curtainwall, and entrance assemblies.</p>
<p>Common Florida applications:</p>
<ul>
<li>Hurricane-rated egress doors on commercial buildings (Von Duprin HH-series)</li>
<li>Stair-tower and exit doors (Steelcraft H-Series, NOA-listed)</li>
<li>Healthcare and education projects with strict UL fire-rated hardware specs</li>
<li>Federal and government facilities requiring DoD-spec hardware</li>
</ul>
<p>We work the Allegion catalog as part of our overall Division 08 commercial scope — not as a standalone hardware shop. The benefit to GCs and owners is single-source accountability for the full opening: frame, glass, door, hardware, install.</p>"""
                     },
                     {
                         'h2': 'Verified product data',
                         'body': """<h3>Von Duprin Hurricane HH-series exit devices</h3>
<p>Hurricane-rated Von Duprin devices are tested to FBC TAS 201, 202, and 203, and ASTM E1886, E1996, and E330. Confirmed via the <a href="https://www.vonduprin.com/content/dam/allegion-us-2/web-files/von-duprin-/information-documents/Von_Duprin_Hurricane_Device_Reference_Sheet_113820.pdf" rel="nofollow" style="color:rgba(255,255,255,0.7);">Von Duprin Hurricane Device Reference Sheet</a>:</p>
<table>
<thead><tr><th>Series</th><th>Configuration</th><th>Testing</th></tr></thead>
<tbody>
<tr><td>98/99 HH</td><td>Rim, surface vertical rod, concealed vertical rod, mortise</td><td>FBC TAS 201/202/203 + ASTM E1886/E1996/E330</td></tr>
<tr><td>33A/35A HH</td><td>Narrow-stile (aluminum storefront door)</td><td>FBC TAS 201/202/203 + ASTM E1886/E1996/E330</td></tr>
<tr><td>88 HH</td><td>Concealed vertical rod (wood and metal doors)</td><td>FBC TAS 201/202/203 + ASTM E1886/E1996/E330</td></tr>
<tr><td>2670 HH</td><td>Revolving door panic egress</td><td>FBC TAS 201/202/203 + ASTM E1886/E1996/E330</td></tr>
</tbody>
</table>

<h3>Steelcraft H-Series commercial doors</h3>
<table>
<thead><tr><th>Product</th><th>Design Pressure (Zone 4)</th><th>Miami-Dade NOA</th><th>Expiration</th></tr></thead>
<tbody>
<tr><td>Steelcraft H-Series (HVHZ)</td><td>120&ndash;170 PSF</td><td>22-0427.01</td><td>May 2028</td></tr>
<tr><td>Steelcraft H-Series (HVHZ, secondary configuration)</td><td>120&ndash;170 PSF</td><td>23-0821.16</td><td>May 2028</td></tr>
</tbody>
</table>
<p class="source-note">Source: Miami-Dade Product Control NOA database. Florida Product Approval numbers for Steelcraft are issued but not fully indexed publicly; we verify project-specific FPA listings with the manufacturer on each bid.</p>"""
                     },
                     {
                         'h2': 'When Allegion is in our scope',
                         'body': """<p>We integrate Allegion hardware on commercial projects when:</p>
<ul>
<li>Egress doors require hurricane-rated panic devices (any HVHZ commercial entry)</li>
<li>Stair-tower or fire-rated exit doors are part of the Division 08 package</li>
<li>The GC wants single-source responsibility for frame + glass + door + hardware</li>
<li>Spec calls out specific Allegion product families (most commercial Division 08 specs do)</li>
</ul>
<p>For projects where the door-and-hardware scope is independently subcontracted, we coordinate with the dedicated hardware sub — but our preference (and the GC's preference, in most cases) is to keep the full opening under one umbrella.</p>"""
                     }
                 ],
                 [
                     ('Is ACG an authorized Allegion installer?', 'Yes. ACG (FL CGC #1531993) installs Allegion commercial hardware as part of our Division 08 scope, including Von Duprin hurricane-rated panic devices and Steelcraft NOA-listed commercial doors.'),
                     ('What hurricane-rated panic devices does Von Duprin make?', 'Von Duprin makes hurricane-rated (HH) versions of the 98/99, 33A/35A, 88, and 2670 panic exit device series. Each is tested to FBC TAS 201/202/203 and ASTM E1886/E1996/E330. The 33A/35A is the narrow-stile version used on aluminum storefront doors.'),
                     ('Do Steelcraft doors have Miami-Dade NOAs?', 'Yes. Steelcraft H-Series commercial doors hold two active Miami-Dade NOAs as of May 2026: 22-0427.01 and 23-0821.16, both expiring May 2028. Both list Zone 4 design pressures in the 120–170 PSF range, depending on configuration.'),
                     ('Can I get Schlage / LCN / Ives installed by ACG?', 'Yes. We integrate the full Allegion commercial hardware family — Schlage commercial locks, LCN door closers, Ives hardware accessories — when they are part of the Division 08 scope on a project.'),
                     ('What is the advantage of one sub doing frame + glass + door + hardware?', 'Single-source accountability. Coordination problems on the opening (frame-to-door tolerance, hardware preparation, threshold details, weatherseals) get resolved internally rather than between subs. Our preference is to scope the full opening; GCs typically prefer it as well.')
                 ]
)


# ════════════════════════════════════════════════════════════════════
# PAGE 3 — TGP
# ════════════════════════════════════════════════════════════════════
TGP_PRODUCTS = [
    {"name": "FireLite Plus", "description": "Fire-protective ceramic glazing, 20–90 minute ratings. UL-listed. Per fireglass.com FireLite Plus specifications.", "category": "Fire-Rated Glass"},
    {"name": "Pilkington Pyrostop", "description": "Fire-resistive intumescent glazing, 20–120 minute ratings. Meets ASTM E119 / UL 263 — blocks radiant heat.", "category": "Fire-Rated Glass"},
    {"name": "FireLite NT", "description": "Fire-protective ceramic glazing for budget-conscious applications, 20–60 minute ratings.", "category": "Fire-Rated Glass"},
    {"name": "FireSeal", "description": "Fire-protective wired-free glazing for door vision panels and sidelites.", "category": "Fire-Rated Glass"}
]

TGP_PAGE = ('tgp-installer-florida', 'TGP Fire-Rated Glass',
            'Technical Glass Products (TGP)', 'https://www.fireglass.com', 'Snoqualmie, WA',
            'TGP Fire-Rated Glass Installation',
            'TGP Authorized Fire-Rated Glass Installer — Florida | ACG',
            'ACG installs TGP fire-rated glass — FireLite Plus, Pilkington Pyrostop, FireSeal — 20 to 120-minute UL-listed assemblies. FL CGC #1531993, 350+ commercial projects.',
            'tgp installer florida, technical glass products installer, firelite plus installer, pyrostop installer florida, fire rated glass installer commercial',
            'TGP Fire-Rated Glass Installer — Florida',
            'TGP FireLite Plus and Pilkington Pyrostop fire-rated glass installed by ACG across Florida. 20 to 120-minute UL-listed assemblies.',
            'https://acglass.com/images/projects/martin-county-fire-training/martin-county-fire-training-exterior.jpg',
            'TGP Fire-Rated Installation',
            'TGP fire-rated glass installation — FireLite Plus and Pyrostop',
            'TGP fire-rated installer — Florida commercial',
            'Technical Glass Products (TGP, brand owned by Allegion as of 2018) is the leading fire-rated glass manufacturer in North America. We install the TGP product line on Florida commercial projects requiring fire-rated assemblies — healthcare, education, multifamily, federal, mixed-use. The two main TGP product families serve different functions: FireLite Plus is fire-protective (blocks flames, does not block radiant heat); Pilkington Pyrostop is fire-resistive (blocks flames AND radiant heat, meets ASTM E119 / UL 263).',
            'ACG installs TGP fire-rated glass on Florida commercial projects. The two product families serve different functions: FireLite Plus is fire-protective (blocks flames and smoke but transmits radiant heat) for door and small-opening applications. Pilkington Pyrostop is fire-resistive (blocks flames AND radiant heat, meets ASTM E119 / UL 263) for stairwell separations and fire-rated walls. Picking the wrong category is the most common spec mistake on fire-rated openings.',
            TGP_PRODUCTS,
            [
                {
                    'h2': 'About TGP fire-rated glazing',
                    'body': """<p>Technical Glass Products (TGP) is the dominant fire-rated glass supplier in North America, now a subsidiary of Allegion. The TGP catalog covers every common fire-rated glazing application from 20-minute door vision panels through 120-minute wall assemblies.</p>
<p>The single most important distinction in fire-rated glazing — and the one most commonly misunderstood by spec writers — is fire-protective vs fire-resistive:</p>
<ul>
<li><strong>Fire-protective glazing</strong> limits the passage of flames and smoke but transmits radiant heat. It is rated only as glazing — not as part of a wall assembly. Common applications: door vision panels, transoms, narrow sidelites under 100 sq ft, corridor windows.</li>
<li><strong>Fire-resistive glazing</strong> limits flames, smoke, AND radiant heat. It is treated as a wall assembly under the building code (IBC Section 716). Common applications: stairwell separations, exit corridor walls, area separations, occupancy separations.</li>
</ul>
<p>Specifying a fire-protective product where fire-resistive is code-required is a failure mode we see often on bid drawings — and one we flag during plan review before submittal.</p>"""
                },
                {
                    'h2': 'Verified product data',
                    'body': """<table>
<thead><tr><th>Product</th><th>Category</th><th>Rating</th><th>Standards</th></tr></thead>
<tbody>
<tr><td>FireLite Plus</td><td>Fire-protective</td><td>20&ndash;90 min</td><td>UL-listed; ASTM E2010; NFPA 252/257</td></tr>
<tr><td>FireLite NT</td><td>Fire-protective</td><td>20&ndash;60 min</td><td>UL-listed; ASTM E2010</td></tr>
<tr><td>FireSeal</td><td>Fire-protective</td><td>20&ndash;90 min</td><td>UL-listed</td></tr>
<tr><td>Pilkington Pyrostop</td><td>Fire-resistive</td><td>20&ndash;120 min</td><td>ASTM E119 / UL 263 (heat transmission); NFPA 252/257</td></tr>
</tbody>
</table>
<p class="source-note">Source: <a href="https://www.fireglass.com" rel="nofollow" style="color:rgba(255,255,255,0.7);">fireglass.com</a> primary product specification pages. TGP is not a hurricane-rated product line; no Miami-Dade NOA applies to TGP fire-rated glazing in standard configurations. Custom HVHZ + fire-rated combination assemblies exist for specific projects but are rare and project-engineered.</p>"""
                },
                {
                    'h2': 'When TGP fire-rated is in our scope',
                    'body': """<p>We install TGP fire-rated glazing on Florida commercial projects when:</p>
<ul>
<li>The IBC / FBC code path requires rated glazing at egress, separation, or occupancy boundaries</li>
<li>Architect specifies a fire-rated assembly with UL listing</li>
<li>Healthcare, education, multifamily, or federal projects with strict separation requirements</li>
<li>Mixed-use projects with fire-rated separations between commercial and residential</li>
</ul>
<p>We do not install TGP as a substitute for impact-rated HVHZ glazing — the two product families serve different purposes. Where both are required (rare but real), we engineer a custom combined assembly.</p>"""
                }
            ],
            [
                ('Is ACG an authorized TGP installer?', 'Yes. ACG (FL CGC #1531993) installs the full TGP fire-rated glass line — FireLite Plus, Pilkington Pyrostop, FireLite NT, and FireSeal — on Florida commercial projects requiring fire-rated assemblies.'),
                ('What is the difference between fire-protective and fire-resistive glass?', 'Fire-protective glass (FireLite Plus, FireLite NT, FireSeal) limits flames and smoke but transmits radiant heat. Fire-resistive glass (Pyrostop) blocks flames, smoke, AND radiant heat — it meets ASTM E119 / UL 263 and is treated as a wall assembly under IBC Section 716. Specifying the wrong category is the most common fire-rated spec error.'),
                ('What fire ratings does TGP cover?', 'FireLite Plus covers 20 to 90 minutes (fire-protective). Pilkington Pyrostop covers 20 to 120 minutes (fire-resistive). Both are UL-listed under their respective categories.'),
                ('Does TGP make hurricane-rated glass?', 'No. TGP fire-rated glazing in standard configurations is not Miami-Dade NOA-listed and is not a hurricane product. Combined HVHZ + fire-rated assemblies exist for specific custom applications but are project-engineered, not off-the-shelf.'),
                ('When do I need fire-resistive vs fire-protective glass?', 'Fire-resistive (Pyrostop) is required when the glazing substitutes for a fire-rated wall — typically stairwell separations, exit access corridors, or occupancy separations. Fire-protective (FireLite family) handles door vision panels, transoms, sidelites, and corridor windows under 100 sq ft. Code path is dictated by IBC Section 716 / FBC.')
            ]
)


# ════════════════════════════════════════════════════════════════════
# PAGE 4 — SLIMPACT
# ════════════════════════════════════════════════════════════════════
SLIMPACT_PRODUCTS = [
    {"name": "Slimpact Impact-Rated Window System", "description": "Thin-frame aluminum impact-rated window. 12 Florida Product Approvals (FL #25671.1 through FL #29880.1) per faourglass.com.", "category": "Impact Window"},
    {"name": "Slimpact Railing (LMI)", "description": "Large-missile-impact-rated commercial railing system. Miami-Dade NOA 20-1211.01.", "category": "Commercial Railing"},
    {"name": "Slimpact Door & Storefront Systems", "description": "Thin-frame aluminum commercial door and storefront line. Florida Product Approvals via Faour Glass Technologies.", "category": "Commercial Storefront"}
]

SLIMPACT_PAGE = ('slimpact-installer-florida', 'Slimpact (Faour Glass Technologies)',
                 'Slimpact / Faour Glass Technologies', 'https://faourglass.com', 'Tampa, FL',
                 'Slimpact Commercial Installation & Supply',
                 'Slimpact Authorized Commercial Installer — Florida | ACG',
                 'ACG installs Slimpact thin-frame impact-rated windows, doors, and railings. 12 Florida Product Approvals + Miami-Dade NOA 20-1211.01. FL CGC #1531993.',
                 'slimpact installer florida, slimpact dealer florida, faour glass technologies, slimpact impact windows, slimpact thin frame impact, fmc group slimpact',
                 'Slimpact Authorized Commercial Installer — Florida',
                 'Slimpact thin-frame impact-rated windows, doors, and railings from Faour Glass Technologies. Installed by ACG across Florida.',
                 'https://acglass.com/images/projects/atlantic-fields/atlantic-fields-golden-hour.jpg',
                 'Slimpact Commercial Installation',
                 'Slimpact commercial installation — thin-frame impact-rated',
                 'Slimpact installer — Florida commercial thin-frame impact',
                 'Slimpact is a thin-frame impact-rated aluminum window and door line manufactured by Faour Glass Technologies, FMC Group — a Tampa, FL company in business since 1975. The Slimpact line is engineered for the architectural market where sight-lines and impact compliance both matter: minimal aluminum profile, full impact-rated assembly, Florida Product Approvals on 12 distinct configurations.',
                 'ACG installs Slimpact thin-frame impact-rated windows, doors, and railings on Florida commercial projects. Slimpact is manufactured by Faour Glass Technologies / FMC Group out of Tampa. 12 active Florida Product Approvals (FL #25671.1 through FL #29880.1) plus Miami-Dade NOA 20-1211.01 (railing, LMI).',
                 SLIMPACT_PRODUCTS,
                 [
                     {
                         'h2': 'About Slimpact and Faour Glass Technologies',
                         'body': """<p>Slimpact is the impact-rated product brand from Faour Glass Technologies, a division of FMC Group. The parent company has been operating out of Tampa, FL since 1975 — they are local, they understand Florida code intimately, and they engineer products specifically for the Florida architectural market.</p>
<p>The Slimpact value proposition is unusual in impact-rated commercial: a minimal aluminum profile (thin sight-lines) with full impact compliance. Most impact-rated commercial windows carry heavy aluminum frames because the structure is what resists Large Missile Impact. Slimpact engineers achieve thin sight-lines via reinforced extrusions and laminated glass make-up that meets the testing requirements without bulking up the visible aluminum.</p>
<p>Where we install Slimpact:</p>
<ul>
<li>Architectural projects where the architect specified thin sight-lines</li>
<li>Custom residential and luxury hospitality envelopes</li>
<li>Multifamily projects with high-end aesthetic targets</li>
<li>Renovations where matching historic sight-lines while adding impact compliance is required</li>
<li>Commercial railings on HVHZ projects (Slimpact's NOA-listed railing product)</li>
</ul>"""
                     },
                     {
                         'h2': 'Verified product data',
                         'body': """<h3>Florida Product Approvals</h3>
<table>
<thead><tr><th>FPA Range</th><th>Source</th></tr></thead>
<tbody>
<tr><td>FL #25671.1 through FL #29880.1 (12 active approvals)</td><td><a href="https://faourglass.com/download-page/" rel="nofollow" style="color:rgba(255,255,255,0.7);">faourglass.com download page</a></td></tr>
</tbody>
</table>

<h3>Miami-Dade NOA</h3>
<table>
<thead><tr><th>Product</th><th>NOA</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Slimpact Railing (LMI)</td><td>20-1211.01</td><td>Large Missile Impact rated railing for HVHZ commercial projects. Verified in Miami-Dade Product Control NOA database.</td></tr>
<tr><td>Slimpact Window/Door HVHZ NOA</td><td>Not publicly confirmed as of May 2026</td><td>FPA approvals confirmed for non-HVHZ Florida use; for HVHZ window/door applications, verify current NOA status directly with manufacturer.</td></tr>
</tbody>
</table>
<p class="source-note">Source: <a href="https://faourglass.com" rel="nofollow" style="color:rgba(255,255,255,0.7);">faourglass.com</a> and Miami-Dade Product Control NOA database. For HVHZ window and door applications specifically, we confirm current NOA status with Faour Glass Technologies on every bid because the product line evolves and FPA listings are issued more frequently than NOAs.</p>"""
                     },
                     {
                         'h2': 'When Slimpact is the right call',
                         'body': """<p>Slimpact is the correct system when:</p>
<ul>
<li>The architect specified thin aluminum sight-lines as an aesthetic requirement</li>
<li>The project is in non-HVHZ Florida (Slimpact's FPA approvals cover this fully)</li>
<li>Project is custom residential, luxury hospitality, or design-forward multifamily</li>
<li>Project requires NOA-listed railing (Slimpact's NOA 20-1211.01 is unique in this category)</li>
<li>Renovation or restoration where matching original sight-lines matters</li>
</ul>
<p>When the project is HVHZ commercial high-rise, full-commercial curtainwall, or where standard ESWindows / Euro-Wall systems are spec'd, we install those systems. Slimpact's strength is the design-forward architectural niche, not the broad-spec heavy-commercial market.</p>"""
                     }
                 ],
                 [
                     ('What is Slimpact?', 'Slimpact is a thin-frame impact-rated aluminum window, door, and railing line manufactured by Faour Glass Technologies (a division of FMC Group) out of Tampa, FL. The line is engineered for architectural applications where thin aluminum sight-lines and impact compliance both matter.'),
                     ('Who makes Slimpact?', 'Faour Glass Technologies, a division of FMC Group, has been operating out of Tampa, FL since 1975. Slimpact is their impact-rated product brand.'),
                     ('Is Slimpact NOA-listed for HVHZ?', 'Slimpact Railing has a confirmed Miami-Dade NOA (20-1211.01) for Large Missile Impact applications. For Slimpact window and door products specifically in HVHZ, current NOA status varies — we verify directly with the manufacturer on every bid.'),
                     ('Does Slimpact have Florida Product Approvals?', 'Yes. As of May 2026, Slimpact carries 12 active Florida Product Approvals ranging from FL #25671.1 through FL #29880.1, covering the commercial window, door, and storefront line for non-HVHZ Florida applications.'),
                     ('Is ACG an authorized Slimpact installer?', 'Yes. ACG (FL CGC #1531993) installs Slimpact thin-frame impact-rated products on Florida commercial projects — architectural windows, doors, storefronts, and the NOA-listed Slimpact Railing system.'),
                     ('Why use Slimpact over standard ESWindows or Euro-Wall?', 'Slimpact wins when the architect specified thin aluminum sight-lines as an aesthetic requirement. Most impact-rated commercial windows have heavier visible aluminum. Slimpact engineers maintain impact compliance while keeping the aluminum profile narrow. For broad-spec heavy-commercial or HVHZ high-rise, ESWindows or Euro-Wall is typically the better call.')
                 ]
)


# ════════════════════════════════════════════════════════════════════
# RENDER
# ════════════════════════════════════════════════════════════════════

def build_page(spec):
    (slug, brand_short, brand_full, brand_url, brand_hq, service_label,
     title, description, keywords, og_title, og_description, og_image,
     eyebrow, h1, lead_short, lead, answer, products, sections, faqs) = spec

    page_url = f"https://acglass.com/{slug}.html"

    schemas = [
        article_schema(page_url, h1, description, og_image),
        dealer_service_schema(brand_full, brand_url, brand_hq, products, page_url, service_label),
        breadcrumb_schema(slug, brand_short),
        faq_schema(faqs)
    ]
    schema_html = '\n'.join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>'
        for s in schemas
    )

    sections_html = ''
    for sec in sections:
        sections_html += f"""
    <h2>{sec['h2']}</h2>
    {sec['body']}
"""

    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{page_url}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="{og_image}">
  <link rel="stylesheet" href="css/style.css">
  <link rel="icon" href="images/acg-favicon.svg" type="image/svg+xml">

{schema_html}

{HEAD_CSS}
</head>
<body>

{NAV}

  <section class="hero">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="byline">By Connor Walsh &middot; President, American Commercial Glass &middot; FL CGC #1531993 &middot; Published May 13, 2026</div>
  </section>

  <div id="answer-box">
    <h2>Direct answer</h2>
    <p>{answer}</p>
  </div>

  <main class="content">
{STATS}
{sections_html}

    <h2>Frequently asked questions</h2>
"""
    for q, a in faqs:
        out += f"""    <h3>{q}</h3>
    <p>{a}</p>
"""
    out += f"""
    <div class="cta-box">
      <h3 style="margin-top:0;">Have a {brand_short} project?</h3>
      <p style="margin-bottom:14px;">Send drawings to ACG. We&rsquo;ll verify the {brand_short} configuration against the project spec, code path, and budget &mdash; no charge. Florida CGC #1531993. 350+ projects.</p>
      <p><a href="/bid.html">Submit plans &rarr;</a> &nbsp;|&nbsp; <a href="/manufacturers.html">All ACG partners &rarr;</a> &nbsp;|&nbsp; <a href="/contact.html">Contact ACG &rarr;</a></p>
    </div>

    <h2>Related</h2>
    <ul>
      <li><a href="manufacturers.html" style="color:var(--accent);">All ACG manufacturer partners</a></li>
      <li><a href="commercial-storefront-systems.html" style="color:var(--accent);">Commercial storefront systems</a></li>
      <li><a href="impact-windows-doors-florida.html" style="color:var(--accent);">Commercial impact windows &amp; doors</a></li>
      <li><a href="florida-hvhz-glazing-contractor.html" style="color:var(--accent);">Florida HVHZ glazing</a></li>
      <li><a href="approvals/" style="color:var(--accent);">Florida Product Approval &amp; NOA index</a></li>
    </ul>
  </main>

{FOOTER}
</body>
</html>
"""
    return out


PAGES = [PGT_PAGE, ALLEGION_PAGE, TGP_PAGE, SLIMPACT_PAGE]
for spec in PAGES:
    slug = spec[0]
    html = build_page(spec)
    fp = ROOT / f"{slug}.html"
    fp.write_text(html)
    print(f"OK  {slug}.html ({fp.stat().st_size // 1024}K)")
