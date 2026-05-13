#!/usr/bin/env python3
"""Deploy the 59 approved meta description drafts to live pages.
Source: ACG-Meta-Descriptions-Batch-2026-05-13.md (Connor approved all 59 in this turn).
"""
import re, sys
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# (path_relative_to_repo_root, new_description)
META_UPDATES = [
    ('acg-vs-competitors.html', 'ACG vs other Florida commercial glaziers — how 350+ projects, FL CGC #1531993, and AI-managed PM compare to A Christian Glass and Key Glass.'),
    ('blog/atlantic-fields-glazing.html', 'Atlantic Fields golf community glazing envelope in Hobe Sound, FL, delivered by ACG with Proctor Construction. Euro-Wall HVHZ commercial systems.'),
    ('blog/compass-alton-town-center-glazing.html', 'Compass at Alton Town Center commercial glazing in Boca Raton, FL — ACG installed the ESWindows storefront envelope under SISCA Construction.'),
    ('blog/gulf-harbour-country-club-glazing.html', 'Gulf Harbour Country Club glazing in Estero, FL — ACG installed the ESWindows commercial storefront envelope under Waypoint.'),
    ('blog/lucie-at-tradition-clubhouse-glazing.html', "Lucie at Tradition Clubhouse storefront glazing in Port St. Lucie, FL — ACG's full Division 08 package for the multifamily clubhouse."),
    ('blog/siena-lakes-naples-glazing.html', 'Siena Lakes senior-living glazing in Naples, FL — ACG installed the ESWindows commercial storefront envelope direct with ownership.'),
    ('blog/stayapt-suites-lafayette-glazing.html', 'StayAPT Suites Lafayette extended-stay glazing — ACG installed the ESWindows commercial envelope under Rycon Construction.'),
    ('blog/westlake-hialeah-retrofit-glazing.html', 'Westlake Hialeah retrofit glazing project — ACG installed the PGT impact-rated commercial retrofit envelope under SISCA Construction.'),
    ('blog/wild-blue-clubhouse-glazing.html', 'Wild Blue Clubhouse luxury glazing in Estero, FL — ACG delivered the ESWindows commercial storefront envelope direct with ownership.'),
    ('cudjoe-key-fire-station.html', 'Cudjoe Key Fire Station 11 commercial glazing in the Florida Keys — ACG installed the HVHZ-rated ESWindows envelope for this municipal project.'),
    ('dale-mabry-retail-tampa.html', 'Dale Mabry retail glazing in Tampa, FL — ACG installed the ESWindows commercial storefront envelope under Wallace Construction.'),
    ('el-car-wash-northlake.html', 'El Car Wash Northlake commercial glazing in West Palm Beach, FL — ACG installed the ESWindows storefront envelope for this retail build-out.'),
    ('gulf-harbour-country-club.html', 'Gulf Harbour Yacht & Country Club glazing in Fort Myers, FL — ACG installed Euro-Wall commercial systems under Curran Young Construction.'),
    ('harbour-cay-fort-pierce.html', 'Harbour Cay II coastal multifamily glazing in Fort Pierce, FL — ACG installed the ESWindows commercial envelope under Mason Development.'),
    ('hca-cape-coral-emergency.html', 'HCA Florida Cape Coral Emergency Room glazing — ACG installed the PGT impact-rated commercial envelope on this critical-care expansion.'),
    ('illumina-fort-myers.html', 'Illumina at Gulf Coast Town Center retail glazing in Fort Myers, FL — ACG delivered the ESWindows commercial storefront envelope.'),
    ('klus-lighting-vero-beach.html', 'KLUS Lighting showroom glazing in Vero Beach, FL — ACG installed the ESWindows commercial storefront envelope under Proctor Construction.'),
    ('lake-park-innovation-center.html', 'Lake Park Innovation Center commercial glazing in West Palm Beach, FL — ACG delivered the ESWindows storefront envelope for this office project.'),
    ('panther-national-clubhouse.html', 'Panther National Clubhouse — 60,000 SF modern golf clubhouse glazing in Palm Beach Gardens, FL, by Max Strang. Installed by ACG.'),
    ('pointe-palm-bay.html', 'The Pointe at Palm Bay multifamily glazing in Palm Bay, FL — ACG installed the ESWindows commercial envelope with Olympus Construction.'),
    ('savannas-ridge-clubhouse.html', 'Savannas Ridge Clubhouse glazing in Fort Pierce, FL — ACG installed the ESWindows commercial storefront envelope for this amenity center.'),
    ('shoppes-westlake-point.html', 'Shoppes at Westlake Point retail glazing in Westlake, FL — ACG delivered the ESWindows commercial storefront envelope under SISCA Construction.'),
    ('stayapt-suites-lafayette.html', 'StayAPT Suites extended-stay glazing in Lafayette, LA — ACG installed the ESWindows commercial envelope under Rycon Construction.'),
    ('storage-king-winter-haven.html', 'Storage King USA self-storage glazing in Winter Haven, FL — ACG installed the ESWindows commercial envelope under Rycon Construction.'),
    ('waxins-west-palm-beach.html', "Waxin's West Palm Beach hospitality glazing — ACG installed the Euro-Wall commercial envelope for this premium service-retail build-out."),
    # Section 2 — Blog
    ('blog/aluminum-vs-vinyl-windows-commercial-florida.html', 'Aluminum vs vinyl windows for Florida commercial buildings — compare cost, hurricane performance, code path, and 25-year lifespan side-by-side.'),
    ('blog/commercial-glass-types-explained.html', 'Commercial glass types — tempered, laminated, insulated (IGU), Low-E, and impact-rated — explained in plain language for GCs and owners.'),
    ('blog/commercial-glazing-project-timeline.html', 'Realistic commercial glazing project timelines — from bid award through shop drawings, fabrication, install, and final FBC inspection in Florida.'),
    ('blog/commercial-glazing-project-turnaround-time-florida.html', 'Commercial glazing turnaround time in Florida — typical 2026 lead times from plans submission through installation, including HVHZ permit windows.'),
    ('blog/frameless-glass-doors-commercial-spaces.html', 'Frameless entry doors, pivot doors, and interior glass walls for commercial offices, retail, and hospitality projects across Florida.'),
    ('blog/glass-partition-walls-office-commercial-guide.html', 'Glass partition walls for offices — frameless, framed, sliding, demountable, and fire-rated types. Cost, STC ratings, and Florida code compliance.'),
    ('blog/noise-reducing-glass-florida-businesses.html', 'Noise-reducing laminated IGU glass can drop interior decibels 10-15 dB for restaurants, hotels, and offices facing Florida traffic or aircraft.'),
    ('blog/reduce-glare-commercial-glass-solutions.html', 'Screen glare, interior reflection, and parking-lot glare on commercial buildings — Low-E coatings, tints, and frit patterns that actually work.'),
    ('blog/storefront-vs-curtainwall-when-to-use-which.html', 'Storefront vs curtainwall — when to use each on commercial projects. Decision framework by height, span, wind load, and 2026 Florida pricing.'),
    ('blog/uv-protective-glass-commercial-florida.html', 'UV-protective commercial glass for Florida prevents interior fading, protects merchandise, and reduces solar heat load by 60-80% in retail and hospitality.'),
    ('blog/wesley-chapel-brandon-commercial-construction.html', "Wesley Chapel and Brandon — two of Florida's fastest-growing commercial construction markets. Glazing trends and 2026 outlook from ACG."),
    ('blog/what-does-a-glazing-contractor-do.html', 'What does a commercial glazing contractor do — installs storefronts, curtainwall, window wall, impact doors, and Division 08 scope on AIA contracts.'),
    ('blog/what-is-a-window-wall-system.html', 'A window wall system sits between floor slabs — different from curtainwall, which hangs in front of the structure. Cost, code, and use cases.'),
    ('blog/what-is-division-08-construction.html', 'Division 08 in the CSI MasterFormat covers Openings — doors, windows, storefronts, curtainwall, and hardware. Plain-language guide for GCs.'),
    ('blog/why-commercial-windows-crack-prevention-florida.html', 'Commercial glass cracks from thermal stress, impact, installation error, or edge defects — prevention checklist and Florida-specific causes.'),
    # Section 3 — Pillar
    ('contact.html', 'Send commercial glazing plans to ACG — scoped bid in 48 hours. Three Florida offices: West Palm Beach HQ, Naples, Tampa. (772) 486-7711.'),
    ('es-windows.html', 'ESWindows commercial systems installed by ACG across Florida — ES7000 window wall, ES8000T curtainwall, ES-6500 sliding doors. FL CGC #1531993.'),
    ('gc.html', 'The commercial glazing sub GCs build with. 48-hour scope turnaround, full Division 08, single point of contact, FL CGC #1531993.'),
    ('index.html', 'Florida commercial glazing subcontractor — 350+ projects, 1M+ SF installed, $3M/$6M bonded, zero OSHA recordables. FL CGC #1531993. Three offices.'),
    ('infographics-index.html', '207 visual briefs on Florida commercial glazing — project case studies, code guides, system comparisons, and material spotlights from ACG.'),
    ('manufacturers.html', 'ACG installs only the manufacturers on our partner list — ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact. No substitutions, no value-engineering surprises.'),
    ('resources.html', 'The ACG Knowledge Center — everything GCs, architects, and owners need to know about commercial glazing in Florida and the Southeast.'),
    ('security-policy.html', 'ACG website security policy. How to report vulnerabilities found on acglass.com. Responsible disclosure to security@acglass.com.'),
    ('terms-of-use.html', 'Terms of Use for the American Commercial Glass website — the rules governing access to and use of acglass.com and related ACG digital assets.'),
    # Section 4 — GC partners
    ('curran-young-construction.html', 'ACG is a repeat commercial glazing subcontractor for Curran Young Construction — Gulf Harbour Country Club, Estero FL, and additional projects in pipeline.'),
    ('hooks-construction.html', 'ACG is a repeat commercial glazing subcontractor for Hooks Construction across Florida — multifamily, hospitality, and mixed-use Division 08 packages.'),
    ('made-in-rio-construction.html', 'ACG is a repeat commercial glazing subcontractor for Made In Rio — Florida commercial Division 08 scope, design-assist, and full bid support.'),
    ('proctor-construction.html', 'ACG is a repeat commercial glazing subcontractor for Proctor Construction — Atlantic Fields, KLUS Lighting, and other multi-million-dollar Florida builds.'),
    ('rycon-construction.html', 'ACG is a repeat commercial glazing subcontractor for Rycon Construction — Storage King, StayAPT Suites, and other Florida and Southeast projects.'),
    # Section 5 — Impact-windows locations
    ("impact-windows-lakewood-ranch.html", "Commercial impact windows for Lakewood Ranch, FL — America's #1 master-planned community. HVHZ-adjacent installations, FBC compliance, FL CGC #1531993."),
    ('impact-windows-old-naples.html', 'Commercial impact windows for Old Naples — historic Gulf-front luxury, boutique hospitality, and private clubs. FBC HVHZ compliance, FL CGC #1531993.'),
    ('impact-windows-pelican-bay-naples.html', 'Commercial impact windows for Pelican Bay, Naples — luxury multifamily, amenity buildings, and Waterside Shops retail. HVHZ-rated NOA assemblies.'),
    ('impact-windows-venice-fl.html', 'Commercial impact windows for Venice, FL — downtown Venice, Venice Island, Nokomis, Casey Key, and North Port. FBC compliance, FL CGC #1531993.'),
    # Section 6 — News
    ('news/acg-tampa-office-expansion.html', 'ACG opened its third Florida office in Tampa in 2026, expanding commercial glazing coverage along the I-75 corridor. FL CGC #1531993.'),
]

META_RE = re.compile(r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\']\s*/?>)', re.IGNORECASE | re.DOTALL)

modified = 0
missing = []
unchanged = []
for rel_path, new_desc in META_UPDATES:
    fp = ROOT / rel_path
    if not fp.exists():
        missing.append(rel_path)
        continue
    html = fp.read_text()
    new_html, n = META_RE.subn(rf'\1{new_desc}\3', html, count=1)
    if n == 0:
        missing.append(f"{rel_path} (no meta description tag)")
        continue
    if new_html == html:
        unchanged.append(rel_path)
        continue
    fp.write_text(new_html)
    modified += 1

print(f"Modified: {modified}/{len(META_UPDATES)}")
if missing:
    print(f"Missing/unfixable: {len(missing)}")
    for m in missing[:20]:
        print(f"  - {m}")
if unchanged:
    print(f"Unchanged: {len(unchanged)}")
