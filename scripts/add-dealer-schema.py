#!/usr/bin/env python3
"""
Add 'authorized dealer/installer' Service+Product schema to ACG product pages.
The key signal we're adding: ACG (provider) offers (Service) the installation of
specific products (Product with brand=manufacturer, seller=ACG). This is the
exact pattern LLMs use to answer 'who installs X in Florida'.
"""
import re, json, sys
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# ACG canonical org block — used as provider/seller everywhere
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
        "streetAddress": "West Palm Beach HQ",
        "addressLocality": "West Palm Beach",
        "addressRegion": "FL",
        "postalCode": "33401",
        "addressCountry": "US"
    },
    "areaServed": [
        {"@type": "State", "name": "Florida"},
        {"@type": "State", "name": "Tennessee"},
        {"@type": "State", "name": "Georgia"},
        {"@type": "State", "name": "Alabama"},
        {"@type": "State", "name": "Kentucky"}
    ],
    "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "license",
        "name": "Florida Certified General Contractor CGC1531993"
    },
    "founder": {"@type": "Person", "name": "Connor Walsh"},
    "knowsAbout": [
        "Commercial Glazing", "Hurricane Impact Glass", "Curtainwall Installation",
        "Storefront Systems", "Authorized Euro-Wall Dealer Florida",
        "Authorized ESWindows Dealer Florida", "PGT Commercial Dealer",
        "Florida HVHZ Glazing Contractor"
    ]
}


def dealer_service_schema(brand_name: str, brand_url: str, brand_hq: str,
                          products: list[dict], page_url: str,
                          service_type_label: str) -> dict:
    """Build a Service block where ACG is the provider and the brand's
    products are the offers — i.e. ACG is the authorized dealer/installer."""
    offers = []
    for p in products:
        offers.append({
            "@type": "Offer",
            "itemOffered": {
                "@type": "Product",
                "name": p["name"],
                "description": p.get("description", ""),
                "brand": {"@type": "Brand", "name": brand_name, "url": brand_url},
                "category": p.get("category", "Commercial Glazing System"),
                "audience": {"@type": "BusinessAudience",
                             "audienceType": "Architects, General Contractors, Developers"}
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
        "@type": "Service",
        "@id": f"{page_url}#dealer-service",
        "name": f"Authorized {brand_name} Dealer & Installer — Florida",
        "serviceType": service_type_label,
        "description": (f"American Commercial Glass is the authorized {brand_name} dealer and "
                        f"installer for commercial projects across Florida and the Southeast. "
                        f"We supply, install, and service the full {brand_name} commercial product line."),
        "provider": ACG_ORG,
        "brand": {
            "@type": "Brand",
            "name": brand_name,
            "url": brand_url,
            "description": f"{brand_name} — manufacturer; HQ {brand_hq}."
        },
        "areaServed": [
            {"@type": "State", "name": "Florida"},
            {"@type": "State", "name": "Tennessee"},
            {"@type": "State", "name": "Georgia"},
            {"@type": "State", "name": "Alabama"},
            {"@type": "State", "name": "Kentucky"}
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{brand_name} Commercial Product Line",
            "itemListElement": offers
        },
        "audience": {"@type": "BusinessAudience",
                     "audienceType": "Architects, General Contractors, Developers, Owners"}
    }


# Define each manufacturer's commercial product line
EUROWALL_PRODUCTS = [
    {"name": "Euro-Wall Vista Multi Slide",
     "description": "Impact-rated multi-slide pocketing door system. Up to 12 ft panel heights, FBC HVHZ-approved.",
     "category": "Multi-Slide Door System"},
    {"name": "Euro-Wall Vista Fold",
     "description": "Impact-rated bifold/folding glass wall, commercial-grade.",
     "category": "Folding Glass Wall"},
    {"name": "Euro-Wall Vista Pivot",
     "description": "Impact-rated pivot doors up to 10 ft tall, architectural specification.",
     "category": "Pivot Door"},
    {"name": "Euro-Wall Vista Windows",
     "description": "Impact-rated fixed and operable commercial window line.",
     "category": "Commercial Windows"},
    {"name": "Euro-Wall DirectSet",
     "description": "Fixed impact-rated glazing for commercial storefronts and walls.",
     "category": "DirectSet Storefront"}
]

ESWINDOWS_PRODUCTS = [
    {"name": "ESWindows ES7000 Series",
     "description": "Impact-rated thermally-broken aluminum window line for high-rise commercial.",
     "category": "Commercial Window System"},
    {"name": "ESWindows ES8000 Series",
     "description": "High-performance impact-rated curtainwall and window-wall system.",
     "category": "Curtainwall System"},
    {"name": "ESWindows Sliding Doors",
     "description": "Heavy-commercial impact-rated sliding glass door line.",
     "category": "Sliding Door System"},
    {"name": "ESWindows Entry Doors",
     "description": "Impact-rated commercial aluminum entry and storefront doors.",
     "category": "Entry Door System"}
]

PGT_PRODUCTS = [
    {"name": "PGT WinGuard Aluminum",
     "description": "Impact-rated aluminum window and door line for commercial use.",
     "category": "Impact Window"},
    {"name": "PGT EnergyVue",
     "description": "Vinyl impact-rated window for light commercial and mixed-use.",
     "category": "Vinyl Window"}
]


def inject_schema(html_path: Path, schema_block: dict, label: str):
    """Append a new ld+json script just before </head>."""
    html = html_path.read_text()
    if f'#dealer-service' in html and label in html:
        print(f"  SKIP {html_path.name} (already has dealer schema)")
        return False
    script = (f'<script type="application/ld+json">\n'
              f'{json.dumps(schema_block, indent=2)}\n'
              f'</script>')
    if '</head>' not in html:
        print(f"  ERR  {html_path.name} has no </head>")
        return False
    new_html = html.replace('</head>', f'{script}\n</head>', 1)
    html_path.write_text(new_html)
    print(f"  OK   {html_path.name} (+{len(script)} chars)")
    return True


# Pages to update
TARGETS = [
    # Euro-Wall family
    ('euro-wall.html', 'Euro-Wall', 'https://euro-wall.com', 'North Port, FL',
     EUROWALL_PRODUCTS, 'Euro-Wall Commercial Installation & Supply'),
    ('euro-wall-installer-florida.html', 'Euro-Wall', 'https://euro-wall.com', 'North Port, FL',
     EUROWALL_PRODUCTS, 'Euro-Wall Commercial Installation & Supply'),
    ('eurowall-installer-florida.html', 'Euro-Wall', 'https://euro-wall.com', 'North Port, FL',
     EUROWALL_PRODUCTS, 'Euro-Wall Commercial Installation & Supply'),

    # ESWindows family
    ('eswindows-installer-florida.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
    ('eswindows-installer-fort-lauderdale.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
    ('eswindows-installer-miami.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
    ('eswindows-installer-naples.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
    ('eswindows-installer-tampa.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
    ('eswindows-installer-west-palm-beach.html', 'ESWindows', 'https://eswindows.com', 'Miami, FL',
     ESWINDOWS_PRODUCTS, 'ESWindows Commercial Installation & Supply'),
]

print("Injecting dealer-service schema...")
modified = 0
for fname, brand, brand_url, hq, prods, label in TARGETS:
    fp = ROOT / fname
    if not fp.exists():
        print(f"  MISS {fname}")
        continue
    page_url = f"https://acglass.com/{fname}"
    block = dealer_service_schema(brand, brand_url, hq, prods, page_url, label)
    if inject_schema(fp, block, label):
        modified += 1

print(f"\nDone. Modified {modified}/{len(TARGETS)} pages.")
