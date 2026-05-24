#!/usr/bin/env python3
"""
Wave 17: Statewide storefront-glazier exact-match domination.

Generates 10 city-specific storefront glazier landing pages matching the
quality template established at /storefront-glazier-west-palm-beach-florida/.

Each page has city-specific:
- Hero photo + headline
- Building code context (HVHZ vs FBC Wind Zone)
- AHJ paragraph
- Submarket grid (real neighborhood names)
- Nearby project gallery (verified portfolio only)
- 10+ FAQs (mix of universal + 2-3 city-specific)
- LocalBusiness + Service + FAQPage + Person + Breadcrumb + WebPage schema
- Office routing (which ACG office serves this market)

Cities:
1. Miami (Miami-Dade, HVHZ)
2. Tampa (Hillsborough, FBC)
3. Fort Lauderdale (Broward, HVHZ)
4. Orlando (Orange, FBC inland)
5. Naples (Collier, FBC coastal)
6. Fort Myers (Lee, FBC coastal)
7. Boca Raton (Palm Beach County)
8. Jupiter (Palm Beach County)
9. Delray Beach (Palm Beach County)
10. Palm Beach Gardens (Palm Beach County)
"""
import os
import json
import html

ROOT = "/home/user/workspace/acglass-website"

# All 11 cities (incl. WPB) for cross-linking footer block.
ALL_CITIES = [
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

# City-specific data. Every field below drives unique content on the page.
CITIES = [
    {
        "name": "Miami",
        "slug": "miami",
        "state": "Florida",
        "county": "Miami-Dade County",
        "lat": "25.7617", "lng": "-80.1918",
        "office": "West Palm Beach HQ",
        "hvhz": True,
        "wind_speed": "170-180 mph",
        "ahj": "City of Miami Building Department, Miami-Dade County Department of Regulatory and Economic Resources",
        "hero_img": "/images/projects/ifly-miami-exterior.jpg",
        "hero_img_webp": "/images/projects/ifly-miami-exterior-2.webp",
        "hero_alt": "iFly Miami indoor skydiving facility exterior — commercial glazing installation by American Commercial Glass",
        "og_img": "https://acglass.com/images/projects/ifly-miami-exterior-2.jpg",
        "hero_eyebrow_2": "HVHZ &middot; MIAMI-DADE NOA REQUIRED",
        "code_context_html": """
            <h3>Miami-Dade is HVHZ &mdash; the strictest envelope code in North America</h3>
            <p>Miami-Dade County is a designated High-Velocity Hurricane Zone under the Florida Building Code, Section 1620.2. Every commercial storefront, curtain wall, and impact opening requires a Miami-Dade Notice of Acceptance (NOA) approval, not just Florida Product Approval. NOA testing is harsher than FPA: it includes large missile impact (a 9-pound 2x4 fired at 50 fps), cyclic pressure testing across thousands of cycles, and unit-specific anchor pullout calculations. The NOA approval pathway is what we work in every day on Miami commercial scope.</p>
            <h3>Design wind speeds</h3>
            <p>Coastal Miami-Dade design wind speeds run 175-180 mph for Risk Category II commercial buildings, dropping to roughly 170 mph in western Miami-Dade. Storefront product specifications must match the building's actual exposure zone, not the worst case for the county. We pull the wind speed map and verify before committing to a system.</p>
            <h3>Permit and inspection cadence</h3>
            <p>City of Miami runs storefront permits through Cesar Garcia-Pons' building department with separate threshold review on hurricane-rated assemblies. Unincorporated Miami-Dade routes through RER. Both require an installed mockup inspection before full glass install on most commercial scope &mdash; a step that catches anchor mistakes and saves rework downstream.</p>
            <h3>Why glazier selection matters more in HVHZ</h3>
            <p>The cost difference between an HVHZ-correct install and a non-compliant one shows up at the threshold inspection &mdash; not on bid day. We've seen Miami storefronts fail final because the anchor schedule didn't match the NOA, even though the glass and frames did. Pick a glazier who has actually run NOA-approved scope through Miami-Dade inspection. We have.</p>
        """,
        "submarkets": [
            ("Downtown Miami", "Brickell &middot; Bayfront"),
            ("Wynwood", "Arts District &middot; Retail"),
            ("Design District", "Luxury Retail"),
            ("Coconut Grove", "Coastal Retail / Office"),
            ("Coral Gables", "Office / Hospitality"),
            ("Doral", "Industrial / Office"),
            ("Miami Beach", "Hospitality / Retail"),
            ("South Beach", "Restaurant Corridor"),
            ("Aventura", "Retail / Office"),
            ("Bal Harbour", "Luxury Retail"),
            ("Sunny Isles", "Hospitality / Mixed-Use"),
            ("North Miami", "Mixed-Use"),
            ("Pinecrest", "Retail / Medical"),
            ("Kendall", "Retail / Medical"),
            ("Homestead", "Industrial / Retail"),
            ("Hialeah", "Industrial / Retail"),
        ],
        "projects": [
            {"img": "/images/projects/ifly-miami-exterior-2", "alt": "iFly Miami indoor skydiving facility exterior commercial glazing", "cat": "RECREATION &middot; MIAMI", "name": "iFly Miami", "meta": "Wind tunnel facility &mdash; commercial storefront and curtain wall"},
            {"img": "/images/projects/ifly-miami-wind-tunnel", "alt": "iFly Miami wind tunnel interior glazing detail", "cat": "RECREATION &middot; MIAMI", "name": "iFly Miami Wind Tunnel", "meta": "Specialized impact glazing assembly"},
            {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior", "alt": "Ocean Prime restaurant at Pier Sixty-Six commercial Euro-Wall folding glass exterior", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime at Pier Sixty-Six", "meta": "Euro-Wall folding glass &mdash; South Florida hospitality scope"},
            {"img": "/images/projects/westlake-hialeah/hero", "alt": "Westlake retail center Hialeah commercial storefront installation", "cat": "RETAIL &middot; HIALEAH", "name": "Westlake Hialeah", "meta": "Multi-tenant retail storefront program"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does my Miami storefront need Miami-Dade NOA approval?",
                "a": "Yes, in almost every case. Miami-Dade County requires Miami-Dade Notice of Acceptance (NOA) approval for storefront assemblies in HVHZ. Florida Product Approval alone is not sufficient. We verify NOA at takeoff and confirm the assembly with the manufacturer before bidding the scope."
            },
            {
                "q": "Can ACG handle large unit Miami curtain wall scope?",
                "a": "Yes. We've installed commercial storefront and curtain wall on Miami-area projects including iFly Miami and Westlake at Hialeah, and we're an authorized installer for ESWindows large-unit aluminum systems which are commonly specified on Miami high-end projects. For unitized curtain wall we coordinate fabrication and shipping schedule with the manufacturer."
            },
            {
                "q": "Which office handles Miami commercial glazing for ACG?",
                "a": "Our West Palm Beach headquarters at 700 S Rosemary Ave runs the Miami market. Drive time is 65-75 minutes. We've had crews on Miami sites consistently since 2022 and we keep dedicated Miami project management capacity at HQ."
            },
        ],
    },
    {
        "name": "Tampa",
        "slug": "tampa",
        "state": "Florida",
        "county": "Hillsborough County",
        "lat": "27.9506", "lng": "-82.4572",
        "office": "Tampa office",
        "hvhz": False,
        "wind_speed": "150-160 mph",
        "ahj": "City of Tampa Construction Services, Hillsborough County Development Services",
        "hero_img": "/images/projects/hulett-environmental/sunset-side-angle.jpg",
        "hero_img_webp": "/images/projects/hulett-environmental/sunset-side-angle.webp",
        "hero_alt": "Hulett Environmental Tampa corporate headquarters with commercial storefront glazing at sunset",
        "og_img": "https://acglass.com/images/projects/hulett-environmental/sunset-side-angle.jpg",
        "hero_eyebrow_2": "FBC WIND ZONE &middot; LOCAL OFFICE",
        "code_context_html": """
            <h3>Tampa Bay is not HVHZ &mdash; but it is hurricane country</h3>
            <p>Hillsborough County is outside the HVHZ designation (which only covers Miami-Dade and Broward), but Tampa Bay still sits in FBC Wind Zone with design wind speeds of 150-160 mph for Risk Category II commercial buildings on coastal-exposed sites. Storefront assemblies for new commercial construction default to Florida Product Approval with impact-rated laminated glass. ACG specs Miami-Dade NOA-equivalent assemblies on most Tampa scope because the cost premium over FPA-only is small and the document package travels cleanly across the state.</p>
            <h3>The Gulf storm surge factor</h3>
            <p>Tampa Bay's exposure isn't just wind &mdash; it's storm surge. Helene's 2024 surge demonstrated how vulnerable Pinellas, Hillsborough, and Sarasota waterfront commercial scope is to wind-driven flooding. Storefront installs in the surge zone require elevated anchor specifications, marine-grade sealants, and consideration of breakaway facade detailing on the lowest occupied level. ACG carries this into the Tampa scope by default.</p>
            <h3>Tampa AHJ landscape</h3>
            <p>City of Tampa Construction Services handles permits inside the city limits, with separate review tracks for downtown and the Hyde Park / SoHo historic overlay. Hillsborough County Development Services covers unincorporated Hillsborough, including most of the suburban commercial corridors out toward Brandon, Riverview, and Wesley Chapel. Plant City and Temple Terrace have separate building departments. We handle each AHJ's preferences directly when ACG is prime, or pass clean submittal packages to the GC when we're a sub.</p>
            <h3>Local office, local crew</h3>
            <p>ACG's Tampa office runs Tampa Bay scope with a dedicated project management presence. We're not driving four hours from West Palm Beach for an inspection callback &mdash; we're already here.</p>
        """,
        "submarkets": [
            ("Downtown Tampa", "Riverwalk &middot; Office"),
            ("Hyde Park", "Historic Retail / Restaurant"),
            ("SoHo / South Tampa", "Restaurant Corridor"),
            ("Westshore", "Office / Hospitality"),
            ("International Plaza", "Retail Mall District"),
            ("Channelside", "Mixed-Use / Hospitality"),
            ("Ybor City", "Historic Restaurant / Retail"),
            ("Seminole Heights", "Restaurant / Boutique Retail"),
            ("North Hyde Park", "Office / Retail"),
            ("USF Area", "Medical / Institutional"),
            ("Brandon", "Retail / Office"),
            ("Riverview", "Retail / Mixed-Use"),
            ("Wesley Chapel", "Retail / Medical"),
            ("Plant City", "Industrial / Retail"),
            ("Temple Terrace", "Office / Institutional"),
            ("Carrollwood", "Office / Retail"),
        ],
        "projects": [
            {"img": "/images/projects/hulett-environmental/sunset-side-angle", "alt": "Hulett Environmental corporate headquarters Tampa", "cat": "CORPORATE OFFICE &middot; TAMPA", "name": "Hulett Environmental Headquarters", "meta": "Corporate office storefront and entrance glazing"},
            {"img": "/images/projects/dale-mabry-retail/dale-mabry-retail-exterior-1", "alt": "Dale Mabry retail commercial storefront Tampa", "cat": "RETAIL &middot; TAMPA", "name": "Dale Mabry Retail Corridor", "meta": "Multi-tenant retail storefront install"},
            {"img": "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance", "alt": "Storage King Winter Haven commercial facility glazing", "cat": "COMMERCIAL &middot; WINTER HAVEN", "name": "Storage King Winter Haven", "meta": "Commercial facility storefront and impact glazing"},
            {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse commercial glazing", "cat": "COUNTRY CLUB &middot; FLORIDA", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall (Treasure Coast portfolio reference)"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does ACG have a Tampa office?",
                "a": "Yes. Our Tampa office runs Tampa Bay commercial glazing scope &mdash; Hillsborough, Pinellas, Pasco, Sarasota, Manatee, and Polk counties. Dedicated project management presence, not a satellite. The Tampa office opened to support the Gulf Coast portfolio post-Ian and post-Helene rebuild scope."
            },
            {
                "q": "Is Tampa storefront glass HVHZ-rated?",
                "a": "Tampa is not in the HVHZ designation (only Miami-Dade and Broward are). Storefront assemblies in Tampa default to Florida Product Approval (FPA) impact glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway because the cost difference is minimal and it travels cleanly if you have multi-state projects."
            },
            {
                "q": "Can ACG handle post-Helene storefront rebuild in Tampa Bay?",
                "a": "Yes. Helene caused widespread storefront damage across Pinellas, Hillsborough, Sarasota, and Manatee counties in 2024-2025. We coordinate with insurance adjusters on damage documentation, scope to the adjuster's preferred format, and bid permanent replacement on standard or expedited schedule. Storm-damaged single-pane and IGU replacement is in-stock 2-4 weeks; full storefront replacement is 6-12 weeks depending on system."
            },
        ],
    },
    {
        "name": "Fort Lauderdale",
        "slug": "fort-lauderdale",
        "state": "Florida",
        "county": "Broward County",
        "lat": "26.1224", "lng": "-80.1373",
        "office": "West Palm Beach HQ",
        "hvhz": True,
        "wind_speed": "170 mph",
        "ahj": "City of Fort Lauderdale Building Department, Broward County Building Code Services Division",
        "hero_img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial.jpg",
        "hero_img_webp": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial.webp",
        "hero_alt": "Ocean Prime restaurant marina aerial at Pier Sixty-Six Fort Lauderdale with Euro-Wall folding glazing by ACG",
        "og_img": "https://acglass.com/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial.jpg",
        "hero_eyebrow_2": "HVHZ &middot; BROWARD COUNTY NOA",
        "code_context_html": """
            <h3>Broward County is HVHZ &mdash; same product approval pathway as Miami</h3>
            <p>Broward County, including Fort Lauderdale, Hollywood, Pompano, Deerfield, and the rest of the coastal cities, is designated High-Velocity Hurricane Zone alongside Miami-Dade. Every commercial storefront assembly requires Miami-Dade Notice of Acceptance (NOA) approval. There is no FPA-only path on new commercial scope. Anchor schedules must be unit-specific and verified against the NOA documentation.</p>
            <h3>Design wind speeds</h3>
            <p>Fort Lauderdale and coastal Broward design wind speeds run 170 mph for Risk Category II commercial buildings, scaling up on Risk Category III and IV (hospitals, EOCs, public assembly). The storefront product needs to match the actual exposure zone, not the worst-case county number.</p>
            <h3>Fort Lauderdale AHJ landscape</h3>
            <p>City of Fort Lauderdale Building Department handles permits inside the city, with downtown Las Olas commercial scope going through a separate plan review track. Broward County Building Code Services covers unincorporated Broward. Hollywood, Pompano Beach, Deerfield Beach, and the rest of Broward&rsquo;s 30+ municipalities each run their own building departments. We submit and track directly when ACG is prime, and we hand off a clean submittal package to the GC when we&rsquo;re a sub.</p>
            <h3>The marina and waterfront factor</h3>
            <p>Fort Lauderdale's marine commercial scope &mdash; Pier Sixty-Six, Bahia Mar, the Las Olas Riverfront &mdash; runs into a corrosion environment that standard aluminum and standard fasteners don&rsquo;t survive. ACG specifies marine-grade anchors, isolating Tedlar membranes between aluminum and dissimilar metals, and DOW Corning 795 silicone sealant on every marina-front commercial install. We've installed at Ocean Prime at Pier Sixty-Six &mdash; we've run this exact scope.</p>
        """,
        "submarkets": [
            ("Downtown Las Olas", "Restaurant / Retail"),
            ("Flagler Village", "Mixed-Use / Restaurant"),
            ("Riverwalk", "Mixed-Use"),
            ("Sailboat Bend", "Historic"),
            ("Victoria Park", "Boutique Retail"),
            ("Coral Ridge", "Retail / Medical"),
            ("Galt Ocean Mile", "Hospitality"),
            ("Port Everglades", "Hospitality / Marine Commercial"),
            ("Pier Sixty-Six", "Marina Hospitality"),
            ("Sunrise", "Office / Retail"),
            ("Plantation", "Office / Medical"),
            ("Pembroke Pines", "Retail / Medical"),
            ("Davie", "Industrial / Retail"),
            ("Hollywood", "Hospitality / Retail"),
            ("Pompano Beach", "Hospitality / Retail"),
            ("Deerfield Beach", "Office / Retail"),
        ],
        "projects": [
            {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior", "alt": "Ocean Prime restaurant at Pier Sixty-Six twilight exterior", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime at Pier Sixty-Six", "meta": "Marina-front restaurant &mdash; Euro-Wall folding glass and all-glass entrance"},
            {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial", "alt": "Ocean Prime Pier Sixty-Six marina aerial", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime &mdash; Aerial View", "meta": "Marina-front installation &mdash; corrosion-rated assembly"},
            {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-interior-dining", "alt": "Ocean Prime restaurant interior dining glass partition", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime &mdash; Interior Dining", "meta": "Interior glass partition and curtain wall"},
            {"img": "/images/projects/cubesmart-davie/hero", "alt": "CubeSmart self-storage commercial facility Davie", "cat": "COMMERCIAL &middot; DAVIE", "name": "CubeSmart Davie", "meta": "Self-storage facility storefront and entry"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does Fort Lauderdale storefront need HVHZ-rated glass?",
                "a": "Yes. Broward County is designated High-Velocity Hurricane Zone under the Florida Building Code. Every commercial storefront, curtain wall, and impact opening requires Miami-Dade Notice of Acceptance (NOA) approval, not just Florida Product Approval. ACG runs HVHZ scope every week in Broward."
            },
            {
                "q": "Can ACG handle marina or waterfront commercial scope in Fort Lauderdale?",
                "a": "Yes. We've installed at Ocean Prime at Pier Sixty-Six &mdash; a marina-front restaurant scope. Marina installs require marine-grade anchors, isolating membranes between aluminum and dissimilar metals (stainless versus galvanized), and DOW Corning 795 silicone sealant. We default to that specification on every Fort Lauderdale waterfront commercial install."
            },
            {
                "q": "Which office handles Fort Lauderdale glazing for ACG?",
                "a": "Our West Palm Beach headquarters runs the Fort Lauderdale market. Drive time is 45-55 minutes. We've maintained continuous crew presence in Broward since 2022."
            },
        ],
    },
    {
        "name": "Orlando",
        "slug": "orlando",
        "state": "Florida",
        "county": "Orange County",
        "lat": "28.5383", "lng": "-81.3792",
        "office": "Tampa office",
        "hvhz": False,
        "wind_speed": "130-140 mph",
        "ahj": "City of Orlando Permitting Services, Orange County Building Inspections Division",
        "hero_img": "/images/projects/haines-city-eoc.jpg",
        "hero_img_webp": "/images/projects/haines-city-eoc.webp",
        "hero_alt": "Haines City Emergency Operations Center government facility — central Florida impact glazing by ACG",
        "og_img": "https://acglass.com/images/projects/haines-city-eoc.jpg",
        "hero_eyebrow_2": "CENTRAL FL &middot; FBC WIND ZONE",
        "code_context_html": """
            <h3>Orlando is not HVHZ &mdash; but Florida Building Code still applies</h3>
            <p>Orange County and the Central Florida metro are well outside the HVHZ designation that covers Miami-Dade and Broward. Design wind speeds run 130-140 mph for Risk Category II commercial buildings &mdash; substantially lower than coastal South Florida. Storefront assemblies still need to meet Florida Building Code Chapter 16 wind load requirements, and Florida Product Approval (FPA) is the standard product approval pathway. Impact-rated glass is not required for most Orange County commercial work but is recommended for tornado-prone exposures and where the owner wants enhanced security.</p>
            <h3>Tornado and severe storm exposure</h3>
            <p>Central Florida sees more tornado activity per square mile than most of the country. Storefront assemblies on schools, EOCs, and public-facing commercial buildings increasingly spec impact-rated glass for the wind-borne debris protection it provides &mdash; even when not code-required. We've installed hardened impact glazing on Haines City Emergency Operations Center and similar central Florida government scope.</p>
            <h3>Orlando AHJ landscape</h3>
            <p>City of Orlando Permitting Services handles permits inside the city limits. Orange County Building Inspections covers unincorporated Orange County, including most of the suburban commercial corridors. Lake Buena Vista, Reedy Creek (Disney&rsquo;s former district), Winter Park, and Maitland each have separate building authority tracks. Theme park commercial scope inside the WDW property runs through Disney&rsquo;s own permit office.</p>
            <h3>Theme park and tourism corridor</h3>
            <p>International Drive, the Disney corridor, and Universal&rsquo;s hospitality footprint dominate the central Florida commercial market. Hospitality storefront scope here values speed of completion above all &mdash; tenant fit-out turnaround inside a hotel or resort doesn&rsquo;t tolerate a 16-week storefront lead time. ACG sizes the manufacturer order, fabrication, and on-site install for the schedule that hospitality work actually demands.</p>
        """,
        "submarkets": [
            ("Downtown Orlando", "Office / Restaurant"),
            ("Lake Eola Heights", "Restaurant / Mixed-Use"),
            ("Thornton Park", "Restaurant Corridor"),
            ("Mills 50", "Restaurant / Boutique"),
            ("College Park", "Retail / Office"),
            ("Winter Park", "Boutique Retail / Restaurant"),
            ("Maitland", "Office / Retail"),
            ("International Drive", "Hospitality / Tourist Retail"),
            ("Universal Boulevard", "Hospitality"),
            ("Lake Nona", "Medical / Office / Mixed-Use"),
            ("Hunters Creek", "Retail / Office"),
            ("Sanford", "Mixed-Use / Industrial"),
            ("Altamonte Springs", "Office / Retail"),
            ("Apopka", "Retail / Industrial"),
            ("Ocoee", "Retail / Office"),
            ("Kissimmee", "Hospitality / Retail"),
        ],
        "projects": [
            {"img": "/images/projects/haines-city-eoc", "alt": "Haines City Emergency Operations Center government facility glazing", "cat": "GOVERNMENT &middot; HAINES CITY", "name": "Haines City Emergency Operations Center", "meta": "Central Florida government facility &mdash; hardened impact glazing"},
            {"img": "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance", "alt": "Storage King Winter Haven commercial facility entrance", "cat": "COMMERCIAL &middot; WINTER HAVEN", "name": "Storage King Winter Haven", "meta": "Commercial storefront and impact glass install"},
            {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse exterior", "cat": "COUNTRY CLUB &middot; FLORIDA", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall (Treasure Coast portfolio reference)"},
            {"img": "/images/projects/baron-shoppes-tradition", "alt": "Baron Shoppes at Tradition retail center", "cat": "RETAIL &middot; PORT ST LUCIE", "name": "Baron Shoppes at Tradition", "meta": "Multi-tenant retail storefront program (statewide portfolio reference)"},
        ],
        "city_faqs_extra": [
            {
                "q": "Is impact-rated glass required for Orlando commercial storefront?",
                "a": "No, Orange County is outside the HVHZ designation and Florida Product Approval (FPA) impact-rated glass is not code-required for most commercial work. That said, impact glazing is increasingly specified on schools, EOCs, and public-facing buildings for tornado debris protection and enhanced security &mdash; ACG installs both impact-rated and standard insulating glass storefront across the Central Florida market."
            },
            {
                "q": "Which office handles Orlando commercial glazing?",
                "a": "Our Tampa office runs Central Florida scope. Drive time from Tampa to Orlando is 75-90 minutes. We've delivered government scope in Polk County (Haines City EOC) and statewide portfolio that overlaps the Central Florida market."
            },
            {
                "q": "Can ACG handle hospitality storefront in the I-Drive and Disney corridor?",
                "a": "Yes. Hospitality storefront scope on tenant fit-out inside hotels and resorts is one of our standard project types. The constraint is schedule &mdash; hospitality work doesn't tolerate a 16-week storefront lead time. We size manufacturer order, fabrication, and install for the actual turnaround the project needs."
            },
        ],
    },
    {
        "name": "Naples",
        "slug": "naples",
        "state": "Florida",
        "county": "Collier County",
        "lat": "26.1420", "lng": "-81.7948",
        "office": "Naples office",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "City of Naples Building Department, Collier County Building Review",
        "hero_img": "/images/projects/siena-lakes-naples.jpg",
        "hero_img_webp": "/images/projects/siena-lakes-naples.webp",
        "hero_alt": "Siena Lakes Naples senior living facility commercial glazing installation by American Commercial Glass",
        "og_img": "https://acglass.com/images/projects/siena-lakes-naples.jpg",
        "hero_eyebrow_2": "GULF COAST &middot; LOCAL OFFICE",
        "code_context_html": """
            <h3>Naples is FBC Wind Zone &mdash; coastal exposure with non-HVHZ pathway</h3>
            <p>Collier County sits outside the HVHZ designation that covers Miami-Dade and Broward. Design wind speeds for Naples run 170 mph for Risk Category II commercial buildings on coastal-exposed sites &mdash; the same as Palm Beach County. Storefront assemblies default to Florida Product Approval impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies on most Naples commercial scope because the cost difference is small and the document package travels cleanly.</p>
            <h3>The Ian and Milton rebuild context</h3>
            <p>Hurricane Ian (2022) and Milton (2024) caused extensive commercial storefront damage across Collier and Lee counties. We've run rebuild scope continuously since Ian, including in Naples proper, Marco Island, Bonita Springs, and through to Fort Myers Beach. Insurance-funded replacement, NOA-compliant new install, and code-upgrade scope on existing buildings are still active two years after Ian. ACG documents damage for the adjuster, bids to the adjuster's preferred format, and runs the permanent replacement on the schedule the owner needs.</p>
            <h3>Naples AHJ landscape</h3>
            <p>City of Naples Building Department covers permits inside the city limits and is responsive but exacting on submittal completeness. Collier County Building Review covers unincorporated Collier, including most of the Vanderbilt Beach Road, Pine Ridge, and Immokalee Road corridors. Marco Island and Everglades City run their own permit offices. ACG handles AHJ submittal directly when prime, or hands clean packages to the GC when we&rsquo;re a sub.</p>
            <h3>Local office, local crew</h3>
            <p>ACG's Naples office runs Collier and Lee county scope with a dedicated project management presence. We're not driving in from Tampa or West Palm Beach for an inspection callback &mdash; we're already in Naples.</p>
        """,
        "submarkets": [
            ("Old Naples", "Boutique Retail / Restaurant"),
            ("Fifth Avenue South", "Restaurant / Boutique"),
            ("Third Street South", "Restaurant Corridor"),
            ("Naples Bay", "Marina / Restaurant"),
            ("Park Shore", "Retail / Office"),
            ("Pelican Bay", "Country Club / Retail"),
            ("Vanderbilt Beach", "Hospitality / Restaurant"),
            ("North Naples", "Retail / Medical"),
            ("Pine Ridge", "Office / Retail"),
            ("Immokalee Road", "Retail Corridor"),
            ("Mercato", "Mixed-Use Retail"),
            ("Marco Island", "Hospitality / Resort"),
            ("Bonita Springs", "Retail / Restaurant"),
            ("Estero", "Retail / Office"),
            ("Ave Maria", "Mixed-Use / Institutional"),
            ("Bonita Beach", "Hospitality"),
        ],
        "projects": [
            {"img": "/images/projects/siena-lakes-naples", "alt": "Siena Lakes Naples senior living community glazing", "cat": "SENIOR LIVING &middot; NAPLES", "name": "Siena Lakes Naples", "meta": "Senior living facility storefront and impact glazing"},
            {"img": "/images/projects/wild-blue-clubhouse-hero", "alt": "Wild Blue clubhouse country club commercial glazing", "cat": "COUNTRY CLUB &middot; SW FLORIDA", "name": "Wild Blue Clubhouse", "meta": "Country club amenity storefront and curtain wall"},
            {"img": "/images/projects/gulf-harbour", "alt": "Gulf Harbour renovation commercial glazing Fort Myers", "cat": "RESORT &middot; FORT MYERS", "name": "Gulf Harbour Renovation", "meta": "Resort renovation storefront and impact glass"},
            {"img": "/images/projects/illumina-fort-myers/hero", "alt": "Illumia Fort Myers commercial property exterior glazing", "cat": "RETAIL &middot; FORT MYERS", "name": "Illumia Fort Myers", "meta": "Retail center storefront installation"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does ACG have a Naples office?",
                "a": "Yes. Our Naples office covers Collier and Lee counties for commercial glazing scope. Dedicated project management presence, not a satellite. The Naples office opened to support continuous post-Ian and post-Milton rebuild work plus new commercial construction in the Gulf Coast market."
            },
            {
                "q": "Is Naples storefront HVHZ-rated?",
                "a": "Naples is not in the HVHZ designation (only Miami-Dade and Broward are). Storefront assemblies in Collier County default to Florida Product Approval impact-rated glazing. ACG typically specs Miami-Dade NOA-equivalent assemblies anyway because the cost difference is minimal."
            },
            {
                "q": "Can ACG handle resort and country club commercial scope in Naples?",
                "a": "Yes. We've installed at Siena Lakes Naples, Wild Blue Clubhouse, Gulf Harbour, and a portfolio of Southwest Florida resort and country club projects. Resort and country club commercial work has specific aesthetic and durability requirements &mdash; we run that scope continuously through the Naples office."
            },
        ],
    },
    {
        "name": "Fort Myers",
        "slug": "fort-myers",
        "state": "Florida",
        "county": "Lee County",
        "lat": "26.6406", "lng": "-81.8723",
        "office": "Naples office",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "City of Fort Myers Community Development, Lee County Department of Community Development",
        "hero_img": "/images/projects/gulfside-twelve.jpg",
        "hero_img_webp": "/images/projects/gulfside-twelve.webp",
        "hero_alt": "Gulfside Twelve Fort Myers Beach multifamily condominium with NOA-certified impact glazing by ACG",
        "og_img": "https://acglass.com/images/projects/gulfside-twelve.jpg",
        "hero_eyebrow_2": "GULF COAST &middot; POST-IAN REBUILD MARKET",
        "code_context_html": """
            <h3>Fort Myers is FBC Wind Zone &mdash; same coastal exposure as Naples</h3>
            <p>Lee County sits outside the HVHZ designation. Design wind speeds run 170 mph for Risk Category II commercial buildings on coastal-exposed sites. Storefront assemblies default to Florida Product Approval impact-rated glazing. The reality on the ground is that Lee County's enforcement environment got noticeably stricter after Hurricane Ian devastated the county in 2022 &mdash; product approval documentation now gets scrutinized more carefully than it did pre-Ian, and anchor inspection is more thorough.</p>
            <h3>Post-Ian and post-Milton continued rebuild</h3>
            <p>Hurricane Ian (September 2022) caused catastrophic commercial damage across Fort Myers, Fort Myers Beach, Sanibel, Captiva, Pine Island, and Cape Coral. Hurricane Milton (October 2024) added additional damage. Two years on, the rebuild is still active. ACG has run continuous rebuild scope since Ian, including on Gulfside Twelve at Fort Myers Beach &mdash; a multifamily condo with NOA-certified impact glazing throughout. Insurance-funded replacement, code-upgrade scope on existing buildings, and new commercial construction are all active categories in the Fort Myers market right now.</p>
            <h3>Fort Myers AHJ landscape</h3>
            <p>City of Fort Myers Community Development handles permits inside the city. Lee County Department of Community Development covers unincorporated Lee, which is most of Cape Coral, the Estero / Bonita Springs corridor, Pine Island, and the beach communities. Fort Myers Beach, Cape Coral, and Sanibel each run their own building authorities. ACG submits and tracks directly when prime; we hand clean packages to the GC otherwise.</p>
            <h3>The barrier island factor</h3>
            <p>Sanibel, Captiva, Fort Myers Beach, and Pine Island sit on barrier islands &mdash; the most wind-exposed and surge-exposed commercial real estate in Florida. Storefront installs here require elevated anchor specifications, marine-grade fasteners, and detailing for breakaway facade at the lowest occupied level on Velocity Zone (VE) sites. We carry this into the barrier island scope by default.</p>
        """,
        "submarkets": [
            ("Downtown Fort Myers", "Restaurant / Office"),
            ("River District", "Mixed-Use / Historic"),
            ("Edison Mall Area", "Retail Corridor"),
            ("McGregor Boulevard", "Retail / Office"),
            ("Page Field", "Industrial / Retail"),
            ("Bell Tower Shops", "Retail / Office"),
            ("Gateway", "Mixed-Use"),
            ("Fort Myers Beach", "Hospitality / Restaurant"),
            ("Sanibel Island", "Hospitality / Retail"),
            ("Captiva Island", "Hospitality"),
            ("Cape Coral", "Retail / Office"),
            ("North Fort Myers", "Retail / Industrial"),
            ("Estero", "Retail / Restaurant"),
            ("Bonita Springs", "Retail / Restaurant"),
            ("Lehigh Acres", "Retail / Office"),
            ("Pine Island", "Hospitality / Small Retail"),
        ],
        "projects": [
            {"img": "/images/projects/gulfside-twelve", "alt": "Gulfside Twelve Fort Myers Beach multifamily condo glazing", "cat": "MULTIFAMILY CONDO &middot; FORT MYERS BEACH", "name": "Gulfside Twelve", "meta": "NOA-certified impact glazing &mdash; post-Ian rebuild"},
            {"img": "/images/projects/illumina-fort-myers/hero", "alt": "Illumia Fort Myers retail glazing exterior", "cat": "RETAIL &middot; FORT MYERS", "name": "Illumia Fort Myers", "meta": "Retail center storefront install"},
            {"img": "/images/projects/gulf-harbour", "alt": "Gulf Harbour Fort Myers resort renovation glazing", "cat": "RESORT &middot; FORT MYERS", "name": "Gulf Harbour Renovation", "meta": "Resort renovation storefront and impact glass"},
            {"img": "/images/projects/hca-cape-coral/hero", "alt": "HCA Cape Coral medical facility commercial glazing", "cat": "MEDICAL &middot; CAPE CORAL", "name": "HCA Cape Coral", "meta": "Medical facility storefront and impact glazing"},
        ],
        "city_faqs_extra": [
            {
                "q": "Can ACG handle post-Ian or post-Milton commercial rebuild in Fort Myers?",
                "a": "Yes. We've run continuous rebuild scope since Ian in 2022, including Gulfside Twelve at Fort Myers Beach. We coordinate with insurance adjusters on damage documentation, bid to the adjuster's preferred format, and run permanent replacement on a schedule the owner can plan around. Two years on, the rebuild market in Lee County is still active."
            },
            {
                "q": "Which office handles Fort Myers commercial glazing for ACG?",
                "a": "Our Naples office covers Lee County. Drive time from Naples to downtown Fort Myers is 35-45 minutes. Continuous crew presence in the post-Ian rebuild market since 2022."
            },
            {
                "q": "Are barrier island commercial storefront installs different in Fort Myers?",
                "a": "Yes. Sanibel, Captiva, Fort Myers Beach, and Pine Island are the most exposed commercial real estate in Florida &mdash; wind, surge, and corrosion all elevated. Storefront installs require marine-grade anchors, isolating membranes between dissimilar metals, and DOW Corning marine-grade sealant. On VE-zone properties, breakaway facade detailing at the lowest occupied level is required. ACG carries this specification by default on barrier island commercial scope."
            },
        ],
    },
    {
        "name": "Boca Raton",
        "slug": "boca-raton",
        "state": "Florida",
        "county": "Palm Beach County",
        "lat": "26.3683", "lng": "-80.1289",
        "office": "West Palm Beach HQ",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "City of Boca Raton Building Department, Palm Beach County Planning Zoning & Building",
        "hero_img": "/images/projects/atlantic-fields-golf-house/card-golden-hour.jpg",
        "hero_img_webp": "/images/projects/atlantic-fields-golf-house/card-golden-hour.webp",
        "hero_alt": "Atlantic Fields Golf House clubhouse at golden hour — Palm Beach County country club commercial glazing by ACG",
        "og_img": "https://acglass.com/images/projects/atlantic-fields-golf-house/card-golden-hour.jpg",
        "hero_eyebrow_2": "SOUTHERN PBC &middot; COUNTRY CLUB CORRIDOR",
        "code_context_html": """
            <h3>Boca is Palm Beach County &mdash; HVHZ-adjacent but not HVHZ</h3>
            <p>Boca Raton sits in Palm Beach County, just north of the Broward County HVHZ line. Design wind speeds run 170 mph for Risk Category II commercial buildings &mdash; functionally identical to the HVHZ environment 5 miles south, but with a different product approval pathway. Storefront assemblies in Boca default to Florida Product Approval impact-rated glazing. ACG specs Miami-Dade NOA-equivalent assemblies on most Boca commercial scope because the cost difference is small and many Boca developers also work in Broward/Miami-Dade and value document-package consistency.</p>
            <h3>Boca Raton AHJ landscape</h3>
            <p>City of Boca Raton Building Department is one of the more rigorous commercial permit reviewers in Palm Beach County. Plan review on storefront and curtain wall scope is thorough &mdash; expect first-round comments on most submittals. The CRA overlay covers downtown Boca (Mizner Park, Sanborn Square, the Royal Palm corridor) with separate design review. Unincorporated Boca runs through Palm Beach County PZB.</p>
            <h3>Country club and corporate campus market</h3>
            <p>Boca Raton is the densest country club and corporate campus market in Palm Beach County. Boca Resort, The Polo Club, Broken Sound, Royal Palm Yacht & Country Club, Boca West, St. Andrews, Mizner Country Club &mdash; each runs continuous amenity, clubhouse, and dining facility renovation that calls for commercial storefront, curtain wall, and impact glazing. Corporate campuses including FAU, the Office Depot HQ corridor, and the Yamato Corridor (T-Mobile, Modernizing Medicine, ADT) account for steady ground-up and tenant fit-out scope.</p>
            <h3>Local market</h3>
            <p>ACG's West Palm Beach HQ is 30 minutes from Boca Raton on I-95. We've delivered Palm Beach County country club and amenity scope continuously since 2021. Boca is in our daily territory.</p>
        """,
        "submarkets": [
            ("Downtown Boca", "Mizner Park &middot; Restaurant"),
            ("Mizner Park", "Mixed-Use Retail"),
            ("Royal Palm Place", "Restaurant Corridor"),
            ("East Boca", "Hospitality / Office"),
            ("Boca Beach", "Hospitality"),
            ("Yamato Corridor", "Corporate / Office"),
            ("Glades Road", "Retail / Medical"),
            ("Town Center", "Retail Mall"),
            ("Mizner Country Club", "Country Club Amenity"),
            ("Boca West", "Country Club Amenity"),
            ("Broken Sound", "Country Club Amenity"),
            ("The Polo Club", "Country Club Amenity"),
            ("West Boca", "Retail / Medical"),
            ("FAU Area", "Institutional / Retail"),
            ("Boca Center", "Office / Retail"),
            ("Park at Broken Sound", "Office Park"),
        ],
        "projects": [
            {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse golden hour exterior", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall (PBC region portfolio)"},
            {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center full-height curtain wall interior", "cat": "PERFORMANCE FACILITY &middot; HOBE SOUND", "name": "Atlantic Fields Performance Center", "meta": "Country club performance facility &mdash; full-height curtain wall"},
            {"img": "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort oceanfront aerial", "cat": "RESORT &middot; PALM BEACH", "name": "Eau Palm Beach Resort", "meta": "Hospitality storefront and arched window restoration"},
            {"img": "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool", "alt": "Tradewinds Clubhouse country club amenity glazing", "cat": "COUNTRY CLUB &middot; PBC", "name": "Tradewinds Clubhouse", "meta": "Country club clubhouse storefront"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does Boca Raton storefront need HVHZ-rated glass?",
                "a": "No. Boca Raton is in Palm Beach County, which is not HVHZ. Florida Product Approval (FPA) impact-rated glazing is the standard pathway. That said, ACG specs Miami-Dade NOA-equivalent assemblies on most Boca commercial scope because the cost difference is small and many Boca developers also work in Broward/Miami-Dade and value document consistency."
            },
            {
                "q": "Can ACG handle country club amenity storefront in Boca?",
                "a": "Yes. Country club amenity work is one of our core verticals across Palm Beach County. We've delivered clubhouse and amenity scope at Atlantic Fields, Tradewinds, Wild Blue, and a portfolio of South Florida country clubs. Boca's country club density (Boca West, Broken Sound, Royal Palm Yacht, Mizner, St. Andrews, The Polo Club) is in our daily territory."
            },
            {
                "q": "Which office handles Boca Raton commercial glazing?",
                "a": "Our West Palm Beach headquarters runs the Boca market. Drive time on I-95 is 30 minutes. Continuous crew presence in PBC since 2021."
            },
        ],
    },
    {
        "name": "Jupiter",
        "slug": "jupiter",
        "state": "Florida",
        "county": "Palm Beach County",
        "lat": "26.9342", "lng": "-80.0942",
        "office": "West Palm Beach HQ",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "Town of Jupiter Building Department, Palm Beach County PZB",
        "hero_img": "/images/projects/atlantic-fields-golf-house/hero-golden-hour.jpg",
        "hero_img_webp": "/images/projects/atlantic-fields-golf-house/hero-golden-hour.webp",
        "hero_alt": "Atlantic Fields Golf House clubhouse — north Palm Beach County commercial glazing by ACG",
        "og_img": "https://acglass.com/images/projects/atlantic-fields-golf-house/hero-golden-hour.jpg",
        "hero_eyebrow_2": "NORTHERN PBC &middot; ABACOA / INDIANTOWN",
        "code_context_html": """
            <h3>Jupiter is Palm Beach County &mdash; coastal exposure, FBC Wind Zone</h3>
            <p>Jupiter sits at the northern end of Palm Beach County, with design wind speeds of 170 mph for Risk Category II commercial buildings on coastal sites. Same product approval pathway as the rest of PBC: Florida Product Approval impact-rated glazing is the standard, and ACG specs Miami-Dade NOA-equivalent assemblies on most commercial scope. The coastal wind environment is real here &mdash; Jupiter Inlet, Jupiter Island, and the oceanfront commercial corridor get the same loading as the WPB beachfront 20 miles south.</p>
            <h3>Jupiter AHJ landscape</h3>
            <p>Town of Jupiter Building Department covers permits inside the town limits and is methodical on commercial storefront submittals &mdash; expect complete document packages. Town of Jupiter Island, Tequesta, Juno Beach, and Jupiter Inlet Colony each run their own permit offices. Unincorporated north PBC routes through Palm Beach County PZB. ACG handles direct submittal or hands clean packages to the GC.</p>
            <h3>Abacoa, Indiantown Road, and the Riverwalk corridor</h3>
            <p>Jupiter's commercial density runs along Indiantown Road (east-west) and US-1 (north-south), with Abacoa Town Center as the planned mixed-use district. Restaurant, retail, medical, and office storefront scope is steady through these corridors. The Jupiter Riverwalk and Harbourside Place hospitality corridor sees continuous tenant fit-out turnover.</p>
            <h3>Country club and equestrian market</h3>
            <p>Jupiter Country Club, Trump National Jupiter, Admirals Cove, and Loxahatchee Club drive amenity and clubhouse renovation scope similar to Boca's country club market. Jupiter Farms equestrian commercial scope (vet clinics, feed stores, tack shops) accounts for a smaller but steady commercial vertical.</p>
        """,
        "submarkets": [
            ("Downtown Jupiter", "Restaurant / Office"),
            ("Abacoa Town Center", "Mixed-Use Retail"),
            ("Harbourside Place", "Hospitality / Restaurant"),
            ("Riverwalk", "Mixed-Use"),
            ("Indiantown Road Corridor", "Retail / Office"),
            ("US-1 North", "Retail / Restaurant"),
            ("Jupiter Inlet", "Marina / Hospitality"),
            ("Jupiter Island", "Hospitality / Estate"),
            ("Carlin Park Area", "Retail / Medical"),
            ("Tequesta", "Retail / Restaurant"),
            ("Juno Beach", "Office / Medical"),
            ("Jupiter Farms", "Equestrian Commercial"),
            ("Admirals Cove", "Country Club Amenity"),
            ("Jupiter Country Club", "Country Club Amenity"),
            ("Trump National Jupiter", "Country Club Amenity"),
            ("Loxahatchee Club", "Country Club Amenity"),
        ],
        "projects": [
            {"img": "/images/projects/atlantic-fields-golf-house/hero-golden-hour", "alt": "Atlantic Fields Golf House clubhouse at golden hour", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall (north PBC region)"},
            {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center interior curtain wall", "cat": "PERFORMANCE FACILITY &middot; HOBE SOUND", "name": "Atlantic Fields Performance Center", "meta": "Performance facility full-height curtain wall"},
            {"img": "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool", "alt": "Tradewinds Clubhouse country club amenity glazing", "cat": "COUNTRY CLUB &middot; PBC", "name": "Tradewinds Clubhouse", "meta": "Country club clubhouse storefront"},
            {"img": "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort aerial", "cat": "RESORT &middot; PALM BEACH", "name": "Eau Palm Beach Resort", "meta": "Hospitality storefront and arched window restoration"},
        ],
        "city_faqs_extra": [
            {
                "q": "Can ACG handle Jupiter country club amenity scope?",
                "a": "Yes. Country club amenity and clubhouse work is a core ACG vertical. We've delivered at Atlantic Fields, Tradewinds, Wild Blue, and a portfolio of South Florida country clubs. Jupiter's country club density (Jupiter Country Club, Trump National, Admirals Cove, Loxahatchee Club) is in our daily territory."
            },
            {
                "q": "Does Jupiter have stricter permit requirements than south PBC?",
                "a": "Jupiter, Jupiter Island, and Tequesta each run their own building departments, and they tend to require complete submittal packages on first round &mdash; less back-and-forth than the larger PBC permit office. The Town of Jupiter is methodical but predictable. ACG handles direct submittal or hands clean packages to the GC."
            },
            {
                "q": "Which office handles Jupiter commercial glazing?",
                "a": "Our West Palm Beach headquarters runs the Jupiter market. Drive time on I-95 is 20-30 minutes. Continuous crew presence in north PBC since 2021."
            },
        ],
    },
    {
        "name": "Delray Beach",
        "slug": "delray-beach",
        "state": "Florida",
        "county": "Palm Beach County",
        "lat": "26.4615", "lng": "-80.0728",
        "office": "West Palm Beach HQ",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "City of Delray Beach Building Department, Palm Beach County PZB",
        "hero_img": "/images/projects/atlantic-fields-golf-house/dining-interior.jpg",
        "hero_img_webp": "/images/projects/atlantic-fields-golf-house/dining-interior.webp",
        "hero_alt": "Atlantic Fields Golf House dining interior with commercial curtain wall — Palm Beach County hospitality glazing",
        "og_img": "https://acglass.com/images/projects/atlantic-fields-golf-house/dining-interior.jpg",
        "hero_eyebrow_2": "PBC &middot; ATLANTIC AVE / PINEAPPLE GROVE",
        "code_context_html": """
            <h3>Delray is Palm Beach County &mdash; FBC Wind Zone, coastal exposure</h3>
            <p>Delray Beach sits in Palm Beach County between Boca and Boynton, with design wind speeds of 170 mph for Risk Category II commercial buildings on coastal sites. Same product approval pathway as the rest of PBC: Florida Product Approval impact-rated glazing is standard, and ACG specs Miami-Dade NOA-equivalent assemblies on most commercial scope because the document package travels cleanly.</p>
            <h3>Atlantic Avenue restaurant corridor</h3>
            <p>Delray's Atlantic Avenue is one of the densest restaurant corridors in Palm Beach County &mdash; 100+ restaurants across the East and West Atlantic stretch, with continuous tenant turnover and storefront refresh scope. Hospitality storefront in Delray favors operable folding and multi-slide door systems (Euro-Wall is the dominant spec) to support indoor-outdoor dining year-round. ACG is an authorized Euro-Wall installer and we run continuous restaurant scope through the Atlantic Avenue corridor.</p>
            <h3>Pineapple Grove and the arts district</h3>
            <p>Pineapple Grove Arts District north of Atlantic Avenue is the boutique retail and gallery corridor. Storefront scope here favors traditional aluminum framing with a frameless retail look &mdash; YKK YES 45 FS flush-glazed is the typical specification.</p>
            <h3>Delray AHJ landscape</h3>
            <p>City of Delray Beach Building Department handles permits inside the city. Plan review on Atlantic Avenue commercial scope goes through CRA design review when the property is in the downtown overlay. Unincorporated Delray (parts of west Delray, the Linton corridor) routes through Palm Beach County PZB. ACG submits directly when prime, or hands clean packages to the GC.</p>
            <h3>Country club density</h3>
            <p>Delray's country club market &mdash; Mizner Country Club, Hamlet Country Club, Delaire, Polo Trace, Boca Grove (technically Boca but operationally Delray) &mdash; runs continuous amenity and clubhouse renovation scope that calls for commercial storefront, curtain wall, and impact glazing.</p>
        """,
        "submarkets": [
            ("East Atlantic Avenue", "Restaurant Corridor"),
            ("West Atlantic Avenue", "Restaurant / Retail"),
            ("Pineapple Grove", "Boutique Retail / Galleries"),
            ("Sun Center", "Mixed-Use"),
            ("Old School Square", "Mixed-Use / Cultural"),
            ("Downtown Delray", "Restaurant / Retail"),
            ("Delray Marketplace", "Mixed-Use Retail"),
            ("Linton Boulevard", "Retail / Medical"),
            ("Federal Highway", "Retail / Restaurant"),
            ("Congress Avenue", "Office / Industrial"),
            ("Delray Beach Oceanfront", "Hospitality"),
            ("Atlantic Dunes", "Boutique Retail"),
            ("Hamlet Country Club", "Country Club Amenity"),
            ("Mizner Country Club", "Country Club Amenity"),
            ("Delaire Country Club", "Country Club Amenity"),
            ("Polo Trace", "Country Club Amenity"),
        ],
        "projects": [
            {"img": "/images/projects/atlantic-fields-golf-house/dining-interior", "alt": "Atlantic Fields Golf House dining interior commercial curtain wall", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House Dining", "meta": "Restaurant interior curtain wall (PBC region portfolio)"},
            {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-interior-dining", "alt": "Ocean Prime restaurant interior dining glass", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime &mdash; Interior", "meta": "Restaurant interior storefront and folding glass"},
            {"img": "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool", "alt": "Tradewinds Clubhouse PBC country club", "cat": "COUNTRY CLUB &middot; PBC", "name": "Tradewinds Clubhouse", "meta": "Country club amenity storefront"},
            {"img": "/images/projects/eau-palm-beach/polpo-arched-window", "alt": "Eau Palm Beach Polpo restaurant arched commercial windows", "cat": "RESTAURANT &middot; PALM BEACH", "name": "Eau Palm Beach &mdash; Polpo", "meta": "Restaurant arched window and storefront"},
        ],
        "city_faqs_extra": [
            {
                "q": "Can ACG install Euro-Wall folding glass for Delray restaurants?",
                "a": "Yes. We're an authorized Euro-Wall installer in Florida. The Atlantic Avenue restaurant corridor is one of the densest markets for impact-rated folding and multi-slide glass walls in Palm Beach County, and ACG runs continuous restaurant scope through that corridor. Euro-Wall systems carry Miami-Dade NOA approval and work cleanly with both indoor-outdoor restaurant programs and full storefront facades."
            },
            {
                "q": "Does Delray have specific permit requirements for Atlantic Avenue?",
                "a": "Yes. Commercial scope inside the downtown Delray CRA overlay goes through CRA design review in addition to standard plan review. The CRA is particular about mullion sightlines, sign band integration, and storefront proportion. ACG handles CRA submittal directly when prime."
            },
            {
                "q": "Which office handles Delray Beach commercial glazing?",
                "a": "Our West Palm Beach headquarters runs the Delray market. Drive time on I-95 is 25-30 minutes. Continuous crew presence in PBC since 2021."
            },
        ],
    },
    {
        "name": "Palm Beach Gardens",
        "slug": "palm-beach-gardens",
        "state": "Florida",
        "county": "Palm Beach County",
        "lat": "26.8234", "lng": "-80.1387",
        "office": "West Palm Beach HQ",
        "hvhz": False,
        "wind_speed": "170 mph",
        "ahj": "City of Palm Beach Gardens Building Department, Palm Beach County PZB",
        "hero_img": "/images/projects/atlantic-fields-performance/hero-gym-interior.jpg",
        "hero_img_webp": "/images/projects/atlantic-fields-performance/hero-gym-interior.webp",
        "hero_alt": "Atlantic Fields Performance Center full-height curtain wall — north PBC commercial glazing by ACG",
        "og_img": "https://acglass.com/images/projects/atlantic-fields-performance/hero-gym-interior.jpg",
        "hero_eyebrow_2": "NORTHERN PBC &middot; PGA BOULEVARD CORRIDOR",
        "code_context_html": """
            <h3>Palm Beach Gardens is Palm Beach County &mdash; coastal exposure, FBC Wind Zone</h3>
            <p>Palm Beach Gardens sits in northern Palm Beach County, with design wind speeds of 170 mph for Risk Category II commercial buildings. Same product approval pathway as the rest of PBC: Florida Product Approval impact-rated glazing is standard. ACG specs Miami-Dade NOA-equivalent assemblies on most commercial scope.</p>
            <h3>PGA Boulevard and downtown PBG</h3>
            <p>Palm Beach Gardens' commercial spine runs along PGA Boulevard, with Downtown at the Gardens, Legacy Place, and Midtown PBG as the planned mixed-use destinations. Continuous tenant fit-out turnover plus regular ground-up commercial scope on the PGA corridor and the Alton/Donald Ross Road area. The city has invested heavily in walkable mixed-use density on PGA Boulevard, and the storefront scope follows that pattern: glass-forward facades, operable folding doors at street-level restaurants, and minimal mullion sightlines on retail tenant work.</p>
            <h3>PBG AHJ landscape</h3>
            <p>City of Palm Beach Gardens Building Department covers permits inside the city. Plan review is rigorous on PGA Boulevard commercial scope &mdash; the city protects the corridor aesthetic via separate design review. Unincorporated north PBC routes through Palm Beach County PZB. ACG handles direct submittal or clean packages to the GC.</p>
            <h3>Country club, medical, and corporate market</h3>
            <p>PBG is dense with country club and medical office scope. PGA National, BallenIsles, Mirasol, and Old Marsh drive continuous amenity work. Jupiter Medical, JFK North, and the Gardens Medical Center district account for steady medical office build-out. Corporate scope on the Alton corridor and the Burns Road industrial park rounds out the commercial mix.</p>
        """,
        "submarkets": [
            ("Downtown at the Gardens", "Mixed-Use Retail"),
            ("Legacy Place", "Mixed-Use"),
            ("Midtown PBG", "Mixed-Use"),
            ("PGA Boulevard", "Retail / Office"),
            ("Alton", "Mixed-Use / Office"),
            ("Donald Ross Road", "Retail / Restaurant"),
            ("Burns Road Industrial", "Industrial / Office"),
            ("Northlake Boulevard", "Retail / Restaurant"),
            ("Gardens Mall District", "Retail Mall"),
            ("Gardens Medical Center", "Medical Office"),
            ("PGA National", "Country Club Amenity"),
            ("BallenIsles", "Country Club Amenity"),
            ("Mirasol", "Country Club Amenity"),
            ("Old Marsh", "Country Club Amenity"),
            ("Frenchman's Creek", "Country Club Amenity"),
            ("Eastpointe", "Country Club Amenity"),
        ],
        "projects": [
            {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center full-height curtain wall", "cat": "PERFORMANCE FACILITY &middot; HOBE SOUND", "name": "Atlantic Fields Performance Center", "meta": "Performance facility curtain wall (north PBC portfolio)"},
            {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse exterior", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall"},
            {"img": "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool", "alt": "Tradewinds Clubhouse country club amenity", "cat": "COUNTRY CLUB &middot; PBC", "name": "Tradewinds Clubhouse", "meta": "Country club amenity storefront"},
            {"img": "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort aerial view", "cat": "RESORT &middot; PALM BEACH", "name": "Eau Palm Beach Resort", "meta": "Hospitality storefront and arched window restoration"},
        ],
        "city_faqs_extra": [
            {
                "q": "Does Palm Beach Gardens have specific design review for PGA Boulevard?",
                "a": "Yes. The city protects the PGA Boulevard corridor aesthetic with a separate design review track in addition to standard plan review. Storefront proportion, mullion sightlines, and finish color all matter on PGA Boulevard commercial scope. ACG handles PBG design review directly when prime."
            },
            {
                "q": "Can ACG handle medical office storefront in PBG?",
                "a": "Yes. Medical office build-out is a core ACG vertical &mdash; we've delivered medical scope at Aspen Dental Edgewater, Ginsberg Eye Center, HCA Cape Coral, and a portfolio of South Florida medical facilities. The Gardens Medical Center district and the Jupiter Medical satellites in north PBC are in our daily territory."
            },
            {
                "q": "Which office handles Palm Beach Gardens commercial glazing?",
                "a": "Our West Palm Beach headquarters runs the PBG market. Drive time on I-95 is 15-20 minutes. PBG is one of our most active markets."
            },
        ],
    },
]
print(f"CITIES count: {len(CITIES)}")
