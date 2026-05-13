#!/usr/bin/env python3
"""
EXECUTION-MODE FIX: Strip Florida-specific code language from non-Florida pages.

Per user direction: impact glass + HVHZ + Florida Building Code is FLORIDA-ONLY.
On Tennessee, Southeast, and other out-of-state pages, position LAMINATED GLASS
(not impact glass) vs monolithic — benefits: acoustic STC, UV blockage, safety,
security, thermal performance via IGU pairing. Code references should be IBC,
ASHRAE 90.1, ANSI Z97.1, CPSC 16 CFR 1201 — not FBC/NOA/TAS/Miami-Dade.

Approach: targeted string replacements that fix the obvious cases. Manual
review of each file post-script is required.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUT_OF_STATE_FILES = [
    'commercial-glazing-al.html',
    'commercial-glazing-asheville-nc.html',
    'commercial-glazing-atlanta-ga.html',
    'commercial-glazing-birmingham-al.html',
    'commercial-glazing-chattanooga-tn.html',
    'commercial-glazing-cincinnati-oh.html',
    'commercial-glazing-huntsville-al.html',
    'commercial-glazing-knoxville-tn.html',
    'commercial-glazing-ky.html',
    'commercial-glazing-lexington-ky.html',
    'commercial-glazing-louisville-ky.html',
    'commercial-glazing-memphis-tn.html',
    'commercial-glazing-nashville-tn.html',
    'commercial-glazing-southeast.html',
    'commercial-glazing-tn.html',
    'commercial-glazing-ga.html',
]

# Replacement rules — order matters (longest first).
RULES = [
    # === META DESCRIPTIONS / TITLES ===
    (
        'Storefront, curtainwall, impact, Division 08',
        'Storefront, curtainwall, laminated glass, Division 08'
    ),
    (
        'Storefront, curtainwall, impact, Euro-Wall',
        'Storefront, curtainwall, laminated glass, Euro-Wall'
    ),

    # === Strip Florida Building Code claims ===
    (
        'If your Knoxville commercial project is in a wind-borne debris region (WBDR) or High-Velocity Hurricane Zone (HVHZ \u2014 Miami-Dade and Broward counties), impact-rated glazing or code-equivalent shutters are required by the Florida Building Code 8th Edition (2026). Most modern commercial buildings in Knoxville specify impact glazing to reduce insurance, speed post-storm reopening, and avoid shutter logistics.',
        'Knoxville commercial buildings follow the 2018 International Building Code (IBC) as adopted by Tennessee, with local jurisdictional amendments. Laminated glass is the dominant specification choice for Knoxville Class-A office, healthcare, hospitality, and retail because it delivers acoustic, UV, safety, and security performance simultaneously. Laminated assemblies use a PVB or SentryGlas interlayer between two glass lites, holding the glass together upon impact, blocking 99% of UV, and reaching STC 35-45 depending on lite thickness.'
    ),
    (
        'Do I need impact windows for a Knoxville commercial building?',
        'What glazing specification is used on Knoxville commercial buildings?'
    ),
    (
        'Do I need impact windows for a Memphis commercial building?',
        'What glazing specification is used on Memphis commercial buildings?'
    ),
    (
        'Do I need impact windows for a Chattanooga commercial building?',
        'What glazing specification is used on Chattanooga commercial buildings?'
    ),

    # === Generic HVHZ -> laminated reframe ===
    (
        "Florida HVHZ engineering discipline transfers directly to Tennessee tornado-zone envelope specifications where owners require it. Structural glazing and impact-rated assemblies available on spec.",
        "Our Florida structural-glazing engineering discipline transfers directly to Tennessee commercial specifications. Laminated glass assemblies are our specialty for Tennessee Class-A office, healthcare, hospitality, education, and retail \u2014 the same engineering rigor, optimized for Tennessee code and climate."
    ),
    (
        "Florida HVHZ background transfers.</strong> Tennessee tornado-zone and Kentucky/Ohio severe-weather glazing requirements share substantial DNA with Florida HVHZ &mdash; structural glazing engineering, impact-rated assemblies, signed/sealed product approvals. The same playbook works.",
        "Structural-glazing engineering transfers.</strong> Tennessee commercial glazing specifications benefit from the same engineering discipline ACG applies in Florida \u2014 structural glazing, sealed-assembly design, signed/sealed shop drawings, and full Division 08 coordination. Laminated glass is the dominant material for Tennessee commercial buildings."
    ),
    (
        "Florida HVHZ background transfers",
        "Structural-glazing engineering transfers"
    ),
    (
        "Florida HVHZ expertise",
        "Florida structural-glazing engineering experience"
    ),
    (
        "HVHZ-grade technical expertise applied everywhere",
        "Florida-grade structural-glazing engineering applied everywhere"
    ),
    (
        "ACG navigates all of it. Our Florida HVHZ expertise is the highest standard in the country.",
        "ACG navigates all of it. Our Florida structural-glazing engineering background is among the most demanding in the country."
    ),

    # Permit timelines — strip FPA / NOA references
    (
        "2 to 6 weeks typical for commercial glazing permits in this region. ACG handles Florida Product Approval verification, Miami-Dade NOA documentation where applicable, and signed/sealed engineering calculations as part of the bid-to-submittal process.",
        "2 to 6 weeks typical for commercial glazing permits in this region. ACG handles signed/sealed engineering calculations, manufacturer-approved shop drawings, code-compliant laminated glass make-up specifications, and full submittal coordination as part of the bid-to-submittal process."
    ),

    # Cost paragraph — strip impact references
    (
        "glazing type (annealed, tempered, laminated impact), and project complexity",
        "glazing type (annealed, tempered, laminated), and project complexity"
    ),

    # Manufacturer lineup — clarify ESWindows is offered as laminated outside FL
    (
        "ESWindows (laminated impact storefront and curtainwall &mdash; ES-50, ES-7000, ES-8000), Euro-Wall (multi-slide, bi-fold Vistafold, pivot, DirectSet), PGT (laminated impact-resistant fenestration), Allegion (commercial hardware, LCN automatic operators), TGP (fire-rated laminated glazing &mdash; UL 9, UL 10B, UL 263), and Slimpact (impact-rated steel framing)",
        "ESWindows (laminated storefront and curtainwall \u2014 ES-50, ES-7000, ES-8000), Euro-Wall (multi-slide, bi-fold Vistafold, pivot, DirectSet), PGT (laminated commercial fenestration), Allegion (commercial hardware, LCN automatic operators), TGP (fire-rated laminated glazing \u2014 UL 9, UL 10B, UL 263), and Slimpact (steel framing systems)"
    ),
    (
        "ESWindows (impact storefront and curtainwall &mdash; ES-50, ES-7000, ES-8000), Euro-Wall (multi-slide, bi-fold Vistafold, pivot, DirectSet), PGT (impact-resistant residential and light commercial), Allegion (commercial hardware, LCN automatic operators), TGP (fire-rated glazing &mdash; UL 9, UL 10B, UL 263), and Slimpact (impact-rated steel framing)",
        "ESWindows (laminated storefront and curtainwall \u2014 ES-50, ES-7000, ES-8000), Euro-Wall (multi-slide, bi-fold Vistafold, pivot, DirectSet), PGT (commercial fenestration), Allegion (commercial hardware, LCN automatic operators), TGP (fire-rated laminated glazing \u2014 UL 9, UL 10B, UL 263), and Slimpact (steel framing systems)"
    ),

    # Southeast page sweeping fixes
    (
        "impact zone designations that change by county. ACG\u2019s Florida-based technical expertise &mdash; HVHZ certification, Florida Product Approval processes, impact-rated system specification &mdash; directly translates to the most demanding Southeast markets.",
        "varying state building codes that change by county. ACG\u2019s Florida structural-glazing engineering background \u2014 sealed-assembly design, manufacturer-approved shop drawings, full Division 08 coordination \u2014 transfers directly to Southeast commercial markets, where laminated glass is the dominant specification."
    ),
    (
        "impact zone designations that change by county. ACG's Florida-based technical expertise \u2014 HVHZ certification, Florida Product Approval processes, impact-rated system specification \u2014 directly translates to the most demanding Southeast markets.",
        "varying state building codes that change by county. ACG's Florida structural-glazing engineering background \u2014 sealed-assembly design, manufacturer-approved shop drawings, full Division 08 coordination \u2014 transfers directly to Southeast commercial markets, where laminated glass is the dominant specification."
    ),
    (
        "Yes. ACG provides the complete Division 08 scope across the Southeast: impact windows and doors, commercial storefronts, curtainwall, window wall, fire-rated assemblies, and specialty glazing.",
        "Yes. ACG provides the complete Division 08 scope across the Southeast: laminated commercial storefronts, curtainwall, window wall, fire-rated assemblies, automatic entrances, and specialty glazing."
    ),
    (
        "Yes. ACG provides the complete Division 08 scope across the Southeast: impact windows and doors, commercial storefronts, curtainwall, window wall, fire-rated assemblies, automatic entrances, and specialty glazing.",
        "Yes. ACG provides the complete Division 08 scope across the Southeast: laminated commercial storefronts, curtainwall, window wall, fire-rated assemblies, automatic entrances, and specialty glazing."
    ),
    (
        "Storefronts, curtainwall, impact glazing, automatic entrances.",
        "Storefronts, curtainwall, laminated glazing, automatic entrances."
    ),

    # Keyword meta — strip impact windows from non-FL keyword lists
    (
        "impact windows Southeast US,",
        "laminated glass Southeast US,"
    ),
]

# Files to also patch with broader sweep
EXTRA_SWEEP_PATTERNS = [
    # Replace "impact-rated" with "laminated" in body copy only when not in
    # a navigation/footer breadcrumb. We'll only replace in <p> and <li> text.
]


def patch_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    orig = html
    changes = 0
    for old, new in RULES:
        if old in html:
            html = html.replace(old, new)
            changes += 1
    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return changes


total = 0
for fname in OUT_OF_STATE_FILES:
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        print(f'  SKIP {fname} (not found)')
        continue
    c = patch_file(path)
    total += c
    print(f'  {fname}: {c} replacements')

print(f'\nTotal replacements: {total}')
print('\nNOTE: This script handles known phrases. Manual review needed for residual')
print('      impact/HVHZ/NOA mentions on out-of-state pages.')
