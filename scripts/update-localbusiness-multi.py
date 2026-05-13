#!/usr/bin/env python3
"""Update LocalBusiness schema sitewide:
- Add Naples (1415 Panther Lane Suite 259, Naples FL 34109)
- Add Tampa (400 N Ashley Drive Suite 2600, Tampa FL 33602)
- Keep WPB HQ (700 S Rosemary Ave Suite 204)

Strategy: insert a single Organization @id graph node into a new global schema file
referenced by every page. But since the site already has 357 LocalBusiness blocks
distributed across pages, the cleanest move is to add a multi-location Organization
schema block (with location array) to the homepage and the contact page, plus
patch the contact page with the three explicit addresses.

We will NOT rewrite 357 pages — that risks breaking individual page schemas.
Instead, we add a comprehensive Organization+Place graph to index.html, contact.html,
and about.html that names all three locations canonically. Search engines will
de-duplicate against the existing per-page schemas via the @id.
"""
import re, json
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# Canonical multi-location organization graph
ACG_GRAPH = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": ["GeneralContractor", "LocalBusiness", "ProfessionalService"],
            "@id": "https://acglass.com/#organization",
            "name": "American Commercial Glass, Inc.",
            "alternateName": "ACG",
            "legalName": "American Commercial Glass, Inc.",
            "url": "https://acglass.com",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "image": "https://acglass.com/images/acg-logo-nav@2x.png",
            "telephone": "+1-772-486-7711",
            "email": "info@acglass.com",
            "priceRange": "$$$",
            "foundingDate": "2021",
            "founder": [
                {"@type": "Person", "name": "Connor Walsh", "@id": "https://acglass.com/author/connor-walsh.html#person"},
                {"@type": "Person", "name": "Rielly Walsh", "@id": "https://acglass.com/author/rielly-walsh.html#person"}
            ],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "700 S Rosemary Ave Suite 204",
                "addressLocality": "West Palm Beach",
                "addressRegion": "FL",
                "postalCode": "33401",
                "addressCountry": "US"
            },
            "location": [
                {
                    "@type": "Place",
                    "@id": "https://acglass.com/#west-palm-beach-hq",
                    "name": "ACG West Palm Beach (HQ)",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "700 S Rosemary Ave Suite 204",
                        "addressLocality": "West Palm Beach",
                        "addressRegion": "FL",
                        "postalCode": "33401",
                        "addressCountry": "US"
                    },
                    "telephone": "+1-772-486-7711"
                },
                {
                    "@type": "Place",
                    "@id": "https://acglass.com/#naples",
                    "name": "ACG Naples",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "1415 Panther Lane Suite 259",
                        "addressLocality": "Naples",
                        "addressRegion": "FL",
                        "postalCode": "34109",
                        "addressCountry": "US"
                    },
                    "telephone": "+1-772-486-7711"
                },
                {
                    "@type": "Place",
                    "@id": "https://acglass.com/#tampa",
                    "name": "ACG Tampa",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "400 N Ashley Drive Suite 2600",
                        "addressLocality": "Tampa",
                        "addressRegion": "FL",
                        "postalCode": "33602",
                        "addressCountry": "US"
                    },
                    "telephone": "+1-772-486-7711"
                }
            ],
            "areaServed": [
                {"@type": "State", "name": "Florida"},
                {"@type": "State", "name": "Tennessee"},
                {"@type": "State", "name": "Georgia"},
                {"@type": "State", "name": "Alabama"}
            ],
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "license",
                "name": "Florida Certified General Contractor CGC1531993",
                "recognizedBy": {"@type": "GovernmentOrganization", "name": "Florida Department of Business and Professional Regulation"},
                "identifier": "CGC1531993"
            },
            "knowsAbout": [
                "Commercial Glazing", "Hurricane Impact Glazing", "Curtainwall Installation",
                "Storefront Systems", "Window Wall Systems", "Florida Building Code",
                "Miami-Dade NOA", "AAMA 502 Field Testing", "Authorized ESWindows Dealer Florida",
                "Authorized Euro-Wall Dealer", "PGT Commercial Installer",
                "Florida HVHZ Glazing Contractor"
            ],
            "sameAs": [
                "https://www.linkedin.com/company/american-commercial-glass/",
                "https://www.instagram.com/acglass.co/"
            ]
        },
        {
            "@type": "WebSite",
            "@id": "https://acglass.com/#website",
            "url": "https://acglass.com",
            "name": "American Commercial Glass",
            "publisher": {"@id": "https://acglass.com/#organization"},
            "inLanguage": "en-US",
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://acglass.com/search.html?q={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        }
    ]
}

GRAPH_BLOCK = f'<script type="application/ld+json">\n{json.dumps(ACG_GRAPH, indent=2)}\n</script>'

# Deploy the canonical graph to homepage, contact, about, and the new bid-hub
TARGETS = ['index.html', 'contact.html', 'about.html']

modified = 0
for rel in TARGETS:
    fp = ROOT / rel
    if not fp.exists():
        print(f"  MISS {rel}")
        continue
    html = fp.read_text()
    # Don't double-inject: check for our @id
    if '"@id": "https://acglass.com/#organization"' in html and '#naples' in html and '#tampa' in html:
        print(f"  SKIP {rel} (already has multi-location graph)")
        continue
    if '</head>' not in html:
        print(f"  ERR {rel}")
        continue
    new_html = html.replace('</head>', f'{GRAPH_BLOCK}\n</head>', 1)
    fp.write_text(new_html)
    modified += 1
    print(f"  OK  {rel}")

print(f"\nDeployed multi-location LocalBusiness graph to {modified}/{len(TARGETS)} pages")
print(f"Naples and Tampa addresses now in canonical schema")
