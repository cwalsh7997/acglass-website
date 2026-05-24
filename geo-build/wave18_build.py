#!/usr/bin/env python3
"""Wave 18 generator. Builds pages for 66 tier-2 Florida cities using
regional code-context templates. Imports wave17_build for the actual HTML
template so we maintain ONE source of truth on layout/style."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))

from wave18_cities import (
    ROOT, TIER2_CITIES, REGION_CODE_CONTEXTS, REGION_HVHZ_FLAG,
    REGION_HERO_EYEBROW, REGION_OFFICE, REGION_PROJECTS, HEROES_BY_REGION,
    OG_BY_REGION, DEFAULT_SUBMARKETS_BY_REGION
)
from wave17_build import build_page

# ALL_CITIES_FULL for the cross-link footer strip — combines wave 17 + wave 18.
WAVE17_CITIES = [
    ("West Palm Beach", "west-palm-beach"),
    ("Miami", "miami"),
    ("Tampa", "tampa"),
    ("Fort Lauderdale", "fort-lauderdale"),
    ("Orlando", "orlando"),
    ("Naples", "naples"),
    ("Fort Myers", "fort-myers"),
    ("Boca Raton", "boca-raton"),
    ("Jupiter", "jupiter"),
    ("Delray Beach", "delray-beach"),
    ("Palm Beach Gardens", "palm-beach-gardens"),
]
ALL_CITY_LIST = WAVE17_CITIES + [(n, s) for n, s, _, _, _, _ in TIER2_CITIES]


def make_city_dict(name, slug, county, region, lat, lng):
    """Convert tier-2 tuple into the dict format wave17_build.build_page expects."""
    heroes = HEROES_BY_REGION[region]
    # rotate hero by slug hash for variety
    idx = sum(ord(c) for c in slug) % len(heroes)
    hero_jpg, hero_webp, hero_alt = heroes[idx]

    # City-specific FAQs - 3 per city, tied to region context
    city_faqs = build_city_faqs(name, slug, county, region)

    return {
        "name": name,
        "slug": slug,
        "state": "Florida",
        "county": county,
        "lat": lat, "lng": lng,
        "office": REGION_OFFICE[region],
        "hvhz": REGION_HVHZ_FLAG[region],
        "wind_speed": "170 mph" if REGION_HVHZ_FLAG[region] else "170 mph",
        "ahj": f"{name} Building Department, {county} Building",
        "hero_img": hero_jpg,
        "hero_img_webp": hero_webp,
        "hero_alt": hero_alt,
        "og_img": OG_BY_REGION[region],
        "hero_eyebrow_2": REGION_HERO_EYEBROW[region],
        "code_context_html": REGION_CODE_CONTEXTS[region],
        "submarkets": DEFAULT_SUBMARKETS_BY_REGION[region],
        "projects": REGION_PROJECTS[region],
        "city_faqs_extra": city_faqs,
    }


def build_city_faqs(name, slug, county, region):
    """3 city-specific FAQs per city, regionally tailored."""
    if region in ("hvhz_mdade", "hvhz_broward"):
        county_label = "Miami-Dade" if region == "hvhz_mdade" else "Broward"
        return [
            {"q": f"Does {name} require HVHZ-rated storefront glass?",
             "a": f"Yes. {county} is designated High-Velocity Hurricane Zone under the Florida Building Code, and every commercial storefront, curtain wall, and impact opening requires {county_label} Notice of Acceptance (NOA) approval. There is no Florida Product Approval-only pathway on new commercial scope. ACG runs HVHZ scope every week in {county}."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": f"Our West Palm Beach headquarters at 700 S Rosemary Ave runs the {county} market, with continuous crew presence since 2022. Drive time to {name} is typically 45-75 minutes depending on submarket."},
            {"q": f"Can ACG handle large or complex commercial scope in {name}?",
             "a": "Yes. ACG is an authorized commercial installer for ESWindows large-unit aluminum systems and for Euro-Wall impact-rated folding glass walls. We handle full Division 08 scope from $50K tenant fit-out up to $2M+ flagship commercial installations across South Florida."},
        ]
    elif region == "palm_beach":
        return [
            {"q": f"Does {name} require HVHZ-rated storefront glass?",
             "a": "No. Palm Beach County is not HVHZ &mdash; that designation applies only to Miami-Dade and Broward. PBC uses Florida Product Approval (FPA) impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway because the cost difference is small and document packages travel cleanly to projects in HVHZ counties."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": "Our West Palm Beach headquarters at 700 S Rosemary Ave runs all Palm Beach County scope. Drive time within PBC is typically 15-45 minutes. PBC is our daily territory &mdash; we've delivered 200+ commercial projects in the county since 2021."},
            {"q": f"Can ACG handle country club and amenity scope near {name}?",
             "a": "Yes. PBC has the densest country club and amenity market in Florida outside Miami-Dade. ACG has delivered amenity, clubhouse, and dining facility scope at Atlantic Fields, Tradewinds, Wild Blue, and a portfolio of PBC country clubs. We run this scope continuously."},
        ]
    elif region == "treasure_coast":
        return [
            {"q": f"Does {name} require HVHZ-rated storefront glass?",
             "a": "No. The Treasure Coast (Martin, St. Lucie, Indian River counties) is not HVHZ. Florida Product Approval (FPA) impact-rated glazing is the standard pathway. ACG typically specs Miami-Dade NOA-equivalent assemblies on Treasure Coast commercial scope for document consistency with South Florida."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": "Our West Palm Beach headquarters runs the Treasure Coast market. Drive time to most Treasure Coast submarkets is 30-75 minutes. We've delivered Treasure Coast scope including Baron Shoppes at Tradition, Indiantown High School, and ongoing portfolio across Martin and St. Lucie counties."},
            {"q": f"Can ACG handle Tradition / master-planned community scope near {name}?",
             "a": "Yes. The Tradition / St. Lucie West master-planned community is one of the most active commercial corridors on the Treasure Coast. We've delivered the multi-tenant retail program at Baron Shoppes at Tradition and run continuous scope through the Tradition development cycle."},
        ]
    elif region == "sw_fl":
        return [
            {"q": f"Does ACG have an office near {name}?",
             "a": "Yes. Our Naples office covers Collier and Lee counties &mdash; the SW Florida market. Dedicated project management presence, not a satellite. The Naples office opened to support continuous post-Ian and post-Milton commercial rebuild work plus new construction."},
            {"q": f"Is {name} storefront HVHZ-rated?",
             "a": "No. SW Florida is not HVHZ (only Miami-Dade and Broward are). Storefront assemblies default to Florida Product Approval impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway because the cost difference is small."},
            {"q": f"Can ACG handle post-Ian or post-Milton rebuild scope in {name}?",
             "a": "Yes. We've run continuous rebuild scope across Lee and Collier counties since Hurricane Ian in 2022, including Gulfside Twelve at Fort Myers Beach with NOA-certified impact glazing throughout. We coordinate with insurance adjusters on damage documentation and bid permanent replacement on the schedule the owner needs."},
        ]
    elif region == "tampa_bay":
        return [
            {"q": f"Does ACG have an office near {name}?",
             "a": "Yes. Our Tampa office runs Tampa Bay commercial glazing scope &mdash; Hillsborough, Pinellas, Pasco, Sarasota, Manatee, and Polk counties. Dedicated project management presence, not a satellite. The Tampa office opened to support continuous post-Helene rebuild work plus new commercial construction."},
            {"q": f"Is {name} storefront HVHZ-rated?",
             "a": "No. Tampa Bay is not HVHZ (only Miami-Dade and Broward are). Storefront assemblies default to Florida Product Approval impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway because the cost difference is minimal."},
            {"q": f"Can ACG handle post-Helene storefront rebuild near {name}?",
             "a": "Yes. Helene caused widespread storefront damage across Pinellas, Hillsborough, Sarasota, and Manatee counties in 2024-2025. We coordinate with insurance adjusters on damage documentation and bid permanent replacement on standard or expedited schedule."},
        ]
    elif region == "central_fl":
        return [
            {"q": f"Is impact-rated glass required for {name} commercial storefront?",
             "a": "No, Central Florida is outside the HVHZ designation and Florida Product Approval (FPA) impact-rated glass is not code-required for most commercial work. Impact glazing is increasingly specified on schools, EOCs, and public-facing buildings for tornado debris protection."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": "Our Tampa office runs Central Florida scope. Drive time from Tampa to most Central FL submarkets is 60-90 minutes. We've delivered government scope in Polk County (Haines City EOC) and statewide portfolio that overlaps the Central Florida market."},
            {"q": f"Can ACG handle hospitality storefront in tourist corridor near {name}?",
             "a": "Yes. Hospitality storefront scope inside hotels and resorts is one of our standard project types. The constraint is schedule &mdash; hospitality work doesn't tolerate a 16-week storefront lead time. We size manufacturer order, fabrication, and install for the actual turnaround the project needs."},
        ]
    elif region == "keys":
        return [
            {"q": f"Does {name} require marine-grade storefront installation?",
             "a": "Yes. Every Keys commercial property is within a half-mile of saltwater. ACG defaults to marine-grade anchors, isolating membranes between aluminum and dissimilar metals, and DOW Corning 795 silicone sealant on every Monroe County commercial install. Standard fasteners fail within 5-7 years in the Keys salt environment."},
            {"q": f"Can ACG handle post-Irma rebuild scope in {name}?",
             "a": "Yes. Hurricane Irma (2017) caused widespread commercial damage across the Keys. ACG has delivered post-Irma rebuild scope including the Cudjoe Key Fire Station with NOA-certified impact glazing throughout. The rebuild is still active as insurance and code-upgrade scope continues to flow through."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": "Our West Palm Beach headquarters at 700 S Rosemary Ave runs the Florida Keys market. Drive time from WPB to the Upper Keys is approximately 3 hours, and to Key West approximately 5-6 hours. We've maintained continuous Keys project presence since 2022."},
        ]
    elif region == "space_coast":
        return [
            {"q": f"Is {name} storefront HVHZ-rated?",
             "a": "No. Brevard County is not HVHZ (only Miami-Dade and Broward are). Storefront assemblies default to Florida Product Approval impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway."},
            {"q": f"Which office handles {name} commercial glazing for ACG?",
             "a": "Our Tampa office runs the Space Coast market. Drive time from Tampa to most Brevard submarkets is 2-3 hours. We bid Brevard scope when the project economics support the route."},
            {"q": f"Can ACG handle aerospace or industrial commercial scope in {name}?",
             "a": "Yes. Industrial and corporate commercial scope is core ACG work &mdash; we've delivered Hulett Environmental's corporate headquarters in Tampa and a portfolio of industrial commercial across the state. SpaceX, Blue Origin, and the Kennedy Space Center supply chain are in our territory."},
        ]
    return []


def main():
    out_count = 0
    failed = []
    for tup in TIER2_CITIES:
        name, slug, county, region, lat, lng = tup
        try:
            city = make_city_dict(name, slug, county, region, lat, lng)
            dir_path = os.path.join(ROOT, f"storefront-glazier-{slug}-florida")
            os.makedirs(dir_path, exist_ok=True)
            out_path = os.path.join(dir_path, "index.html")
            html_out = build_page(city)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html_out)
            size = len(html_out)
            out_count += 1
            print(f"OK ({size:>6,}): /storefront-glazier-{slug}-florida/  [{region}]")
        except Exception as e:
            failed.append((slug, str(e)))
            print(f"FAIL {slug}: {e}")
    print(f"\nGenerated {out_count} tier-2 city pages. Failed: {len(failed)}")


if __name__ == "__main__":
    main()
