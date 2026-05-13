#!/usr/bin/env python3
"""Add missing schema blocks to 5 indexable pages flagged by the audit."""
import json, re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

ACG_ORG_REF = {"@id": "https://acglass.com/#organization"}

ACG_ORG = {
    "@type": ["GeneralContractor", "LocalBusiness"],
    "@id": "https://acglass.com/#organization",
    "name": "American Commercial Glass, Inc.",
    "alternateName": "ACG",
    "url": "https://acglass.com",
    "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
    "telephone": "+1-772-486-7711",
}

PAGES = {
    'approvals/index.html': {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://acglass.com/approvals/#webpage",
                "name": "Florida Product Approval & NOA Index",
                "description": "Searchable index of Florida Product Approvals (FPA) and Miami-Dade Notices of Acceptance (NOA) for commercial glazing assemblies installed by ACG.",
                "url": "https://acglass.com/approvals/",
                "publisher": ACG_ORG_REF,
                "isPartOf": {"@type": "WebSite", "url": "https://acglass.com", "name": "American Commercial Glass"},
                "breadcrumb": {"@id": "https://acglass.com/approvals/#breadcrumb"}
            },
            ACG_ORG,
            {
                "@type": "BreadcrumbList",
                "@id": "https://acglass.com/approvals/#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Florida Approvals & NOAs", "item": "https://acglass.com/approvals/"}
                ]
            }
        ]
    },
    'architect-specs/index.html': {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://acglass.com/architect-specs/#webpage",
                "name": "CSI MasterFormat Division 08 Spec Library",
                "description": "Architect-ready CSI MasterFormat Division 08 specification sections for commercial glazing — storefront, curtainwall, fire-rated, automatic entrances, and impact-rated assemblies.",
                "url": "https://acglass.com/architect-specs/",
                "publisher": ACG_ORG_REF,
                "audience": {"@type": "Audience", "audienceType": "Architects, Specifiers, General Contractors"},
                "isPartOf": {"@type": "WebSite", "url": "https://acglass.com", "name": "American Commercial Glass"},
                "breadcrumb": {"@id": "https://acglass.com/architect-specs/#breadcrumb"}
            },
            ACG_ORG,
            {
                "@type": "BreadcrumbList",
                "@id": "https://acglass.com/architect-specs/#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Architect Spec Library", "item": "https://acglass.com/architect-specs/"}
                ]
            }
        ]
    },
    'news/index.html': {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://acglass.com/news/#webpage",
                "name": "ACG News & Press Releases",
                "description": "Latest news, press releases, and announcements from American Commercial Glass.",
                "url": "https://acglass.com/news/",
                "publisher": ACG_ORG_REF,
                "isPartOf": {"@type": "WebSite", "url": "https://acglass.com", "name": "American Commercial Glass"},
                "breadcrumb": {"@id": "https://acglass.com/news/#breadcrumb"}
            },
            ACG_ORG,
            {
                "@type": "BreadcrumbList",
                "@id": "https://acglass.com/news/#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "News", "item": "https://acglass.com/news/"}
                ]
            }
        ]
    },
    'project-map.html': {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": "https://acglass.com/project-map.html#webpage",
                "name": "ACG Commercial Glazing Project Map",
                "description": "Interactive map of 350+ commercial glazing projects installed by American Commercial Glass across Florida and the Southeast — storefront, curtainwall, hospitality, healthcare, multifamily, and federal.",
                "url": "https://acglass.com/project-map.html",
                "publisher": ACG_ORG_REF,
                "isPartOf": {"@type": "WebSite", "url": "https://acglass.com", "name": "American Commercial Glass"},
                "breadcrumb": {"@id": "https://acglass.com/project-map.html#breadcrumb"},
                "mainContentOfPage": {"@type": "Map", "mapType": "https://schema.org/VenueMap"}
            },
            ACG_ORG,
            {
                "@type": "BreadcrumbList",
                "@id": "https://acglass.com/project-map.html#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Project Map", "item": "https://acglass.com/project-map.html"}
                ]
            }
        ]
    },
    'security-policy.html': {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": "https://acglass.com/security-policy.html#webpage",
                "name": "Security Policy",
                "description": "American Commercial Glass website security policy and vulnerability disclosure information.",
                "url": "https://acglass.com/security-policy.html",
                "publisher": ACG_ORG_REF,
                "isPartOf": {"@type": "WebSite", "url": "https://acglass.com", "name": "American Commercial Glass"},
                "breadcrumb": {"@id": "https://acglass.com/security-policy.html#breadcrumb"}
            },
            ACG_ORG,
            {
                "@type": "BreadcrumbList",
                "@id": "https://acglass.com/security-policy.html#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Security Policy", "item": "https://acglass.com/security-policy.html"}
                ]
            }
        ]
    }
}

def inject(html_path: Path, schema: dict):
    html = html_path.read_text()
    if '"@id": "https://acglass.com/#organization"' in html and 'CollectionPage' in html or 'WebPage' in html and 'BreadcrumbList' in html and '@graph' in html:
        # already has the graph (partial check)
        pass
    if 'application/ld+json' in html and html.count('application/ld+json') > 0:
        # check whether our specific graph is missing — simple text check
        if '"@graph"' in html and html_path.name in ['index.html','project-map.html','security-policy.html']:
            print(f"  SKIP {html_path} (already has graph)")
            return False
    script = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
    if '</head>' not in html:
        print(f"  ERR  {html_path} no </head>")
        return False
    new = html.replace('</head>', f'{script}\n</head>', 1)
    html_path.write_text(new)
    print(f"  OK   {html_path.relative_to(ROOT)} (+{len(script)} chars)")
    return True

count = 0
for rel, schema in PAGES.items():
    fp = ROOT / rel
    if not fp.exists():
        print(f"  MISS {rel}")
        continue
    if inject(fp, schema):
        count += 1
print(f"\nDone. {count}/{len(PAGES)} pages updated.")
