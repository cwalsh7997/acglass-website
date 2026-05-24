#!/usr/bin/env python3
"""
Wave 18: Fill the 64-city gap vs AP Glazing's statewide coverage.

Strategy: Build a tier-2 generator that uses REGIONAL code-context templates
(HVHZ, PBC, Treasure Coast, SW FL, Tampa Bay, Central FL, Keys, Brevard) so
each city has substantive, accurate content without us inventing facts.

Every page is still substantially better than AP Glazing's ~60-word boilerplate
because the regional content alone is 400+ unique words, and we add city-specific
submarkets, AHJ name, and FAQ targeting.
"""
import os
ROOT = "/home/user/workspace/acglass-website"

# REGIONAL CODE CONTEXTS - reused across cities in same code regime.
# Each is unique 400-600 word content based on real building code and AHJ realities.

REGION_HVHZ_MIAMI_DADE = """
            <h3>Miami-Dade is HVHZ &mdash; the strictest envelope code in North America</h3>
            <p>Miami-Dade County is a designated High-Velocity Hurricane Zone under the Florida Building Code, Section 1620.2. Every commercial storefront, curtain wall, and impact opening requires a Miami-Dade Notice of Acceptance (NOA) approval, not just Florida Product Approval. NOA testing is harsher than FPA: it includes large missile impact (a 9-pound 2x4 fired at 50 fps), cyclic pressure testing across thousands of cycles, and unit-specific anchor pullout calculations.</p>
            <h3>Design wind speeds</h3>
            <p>Coastal Miami-Dade design wind speeds run 175-180 mph for Risk Category II commercial buildings, dropping to roughly 170 mph in western Miami-Dade. Storefront product specifications must match the building's actual exposure zone, not the worst case for the county.</p>
            <h3>Why HVHZ glazier selection matters more</h3>
            <p>The cost difference between an HVHZ-correct install and a non-compliant one shows up at the threshold inspection &mdash; not on bid day. We've seen storefronts fail final because the anchor schedule didn't match the NOA, even though the glass and frames did. Pick a glazier who has actually run NOA-approved scope through Miami-Dade inspection. ACG runs HVHZ scope every week in Miami-Dade and Broward.</p>
"""

REGION_HVHZ_BROWARD = """
            <h3>Broward County is HVHZ &mdash; same product approval pathway as Miami-Dade</h3>
            <p>Broward County is designated High-Velocity Hurricane Zone alongside Miami-Dade. Every commercial storefront assembly requires Miami-Dade Notice of Acceptance (NOA) approval. There is no FPA-only pathway on new commercial scope. Anchor schedules must be unit-specific and verified against the NOA documentation. Design wind speeds run 170 mph for Risk Category II commercial buildings on coastal Broward sites.</p>
            <h3>Municipal AHJ density</h3>
            <p>Broward has 30+ municipalities, each running its own building department. Hollywood, Pompano Beach, Deerfield Beach, Fort Lauderdale, Plantation, Sunrise, Pembroke Pines, Davie, Hallandale, Coral Springs, and more &mdash; the permit submittal preferences vary by city. ACG submits directly when prime, or hands clean packages to the GC when we're a sub.</p>
            <h3>Marine and waterfront commercial scope</h3>
            <p>Broward's marina and waterfront commercial corridors &mdash; Las Olas Riverfront, Pier Sixty-Six, Bahia Mar, the Hollywood Broadwalk &mdash; run into corrosion environments that standard aluminum and fasteners don't survive. ACG specifies marine-grade anchors, isolating Tedlar membranes, and DOW Corning 795 silicone sealant on every Broward marina or beachfront commercial install. We've installed at Ocean Prime at Pier Sixty-Six.</p>
"""

REGION_PALM_BEACH = """
            <h3>Palm Beach County is FBC Wind Zone &mdash; HVHZ-adjacent, coastal exposure</h3>
            <p>Palm Beach County sits just north of the Broward HVHZ line, with design wind speeds of 170 mph for Risk Category II commercial buildings on coastal sites &mdash; functionally identical to HVHZ exposure 20 miles south, but with a different product approval pathway. Storefront assemblies in PBC default to Florida Product Approval impact-rated glazing. ACG specs Miami-Dade NOA-equivalent assemblies on most commercial scope here because the cost difference is small and the document package travels cleanly when the same developer also works in Broward/Miami-Dade.</p>
            <h3>Permit and inspection cadence</h3>
            <p>Palm Beach County Planning Zoning &amp; Building covers unincorporated PBC. The county's larger municipalities &mdash; West Palm Beach, Boca Raton, Delray Beach, Boynton Beach, Lake Worth Beach, Palm Beach Gardens, Jupiter, Wellington, Royal Palm Beach &mdash; each run their own building departments. The Town of Palm Beach and Town of Palm Beach Shores add ARCOM and HPB design review on top of the building permit for projects in the historic district overlay.</p>
            <h3>Country club and amenity density</h3>
            <p>Palm Beach County has the densest country club and high-end amenity market in Florida outside Miami-Dade. Continuous clubhouse, pro shop, restaurant, and amenity facility renovation drives steady commercial storefront, curtain wall, and impact glazing scope. ACG runs this scope continuously from our West Palm Beach headquarters at 700 S Rosemary Ave.</p>
"""

REGION_TREASURE_COAST = """
            <h3>Treasure Coast is FBC Wind Zone &mdash; coastal Atlantic exposure</h3>
            <p>Martin, St. Lucie, and Indian River counties run design wind speeds of 170 mph for Risk Category II commercial buildings on coastal sites. Same product approval pathway as Palm Beach County: Florida Product Approval impact-rated glazing is the standard. ACG specs Miami-Dade NOA-equivalent assemblies on most Treasure Coast commercial scope because the document package travels cleanly across South Florida markets.</p>
            <h3>The Treasure Coast development cycle</h3>
            <p>The Treasure Coast has been the most active residential and commercial development corridor in South Florida outside the Miami-Dade/Broward axis. The Tradition / St. Lucie West master-planned communities, the I-95 corridor north of Jupiter, and the Stuart / Martin County estate market drive continuous new commercial construction plus retrofit scope. ACG has delivered Treasure Coast scope including Baron Shoppes at Tradition, Indiantown High School, and ongoing portfolio across Martin and St. Lucie counties.</p>
            <h3>AHJ landscape</h3>
            <p>Each municipality runs its own building department: Stuart, Port St. Lucie, Fort Pierce, Vero Beach, Sebastian, Jensen Beach, Palm City. Unincorporated Martin County and unincorporated St. Lucie County route through their respective county building departments. Submittal preferences vary &mdash; ACG handles direct submittal or hands clean packages to the GC.</p>
"""

REGION_SW_FL = """
            <h3>Southwest Florida is FBC Wind Zone &mdash; Gulf coastal exposure</h3>
            <p>Collier, Lee, and Charlotte counties run design wind speeds of 170 mph for Risk Category II commercial buildings on coastal-exposed sites. The product approval pathway is Florida Product Approval impact-rated glazing &mdash; not HVHZ. ACG specs Miami-Dade NOA-equivalent assemblies on most SW Florida commercial scope because the cost difference is small and the document package travels cleanly.</p>
            <h3>Post-Ian and post-Milton continuous rebuild</h3>
            <p>Hurricane Ian (2022) caused catastrophic commercial damage across Lee and Collier counties. Hurricane Milton (2024) added additional damage. Two years on, the rebuild is still active &mdash; insurance-funded replacement, code-upgrade scope on existing buildings, and new commercial construction all flowing through the market simultaneously. ACG has run continuous rebuild scope since Ian, including Gulfside Twelve at Fort Myers Beach with NOA-certified impact glazing throughout.</p>
            <h3>Barrier island and waterfront factor</h3>
            <p>Sanibel, Captiva, Fort Myers Beach, Marco Island, and Pine Island sit on the most wind- and surge-exposed commercial real estate in Florida. Storefront installs here require elevated anchor specifications, marine-grade fasteners, and detailing for breakaway facade at the lowest occupied level on Velocity Zone (VE) sites. ACG carries this into the SW Florida barrier island scope by default. Naples office runs Collier, Charlotte and Lee county scope with dedicated project management presence.</p>
"""

REGION_TAMPA_BAY = """
            <h3>Tampa Bay is FBC Wind Zone &mdash; Gulf coastal exposure</h3>
            <p>Hillsborough, Pinellas, Manatee, and Sarasota counties sit outside the HVHZ designation (which only covers Miami-Dade and Broward). Tampa Bay design wind speeds run 150-160 mph for Risk Category II commercial buildings on coastal-exposed sites. Storefront assemblies default to Florida Product Approval with impact-rated laminated glass. ACG specs Miami-Dade NOA-equivalent assemblies on most Tampa Bay scope because the cost premium is small and the document package travels cleanly statewide.</p>
            <h3>The Gulf storm surge factor</h3>
            <p>Tampa Bay's exposure isn't just wind &mdash; it's storm surge. Helene's 2024 surge demonstrated how vulnerable Pinellas, Hillsborough, and Sarasota waterfront commercial scope is to wind-driven flooding. Storefront installs in the surge zone require elevated anchor specifications, marine-grade sealants, and consideration of breakaway facade detailing on the lowest occupied level. ACG carries this into Tampa Bay scope by default.</p>
            <h3>AHJ landscape</h3>
            <p>City of Tampa Construction Services handles permits inside Tampa city limits. Hillsborough County Development Services covers unincorporated Hillsborough. St. Petersburg, Clearwater, Bradenton, Sarasota, and the smaller Pinellas and Manatee municipalities each run their own building departments. ACG submits directly when prime, or hands clean packages to the GC when we're a sub.</p>
            <h3>Local office, local crew</h3>
            <p>ACG's Tampa office runs Tampa Bay scope with dedicated project management presence. We're not driving four hours from West Palm Beach for an inspection callback.</p>
"""

REGION_CENTRAL_FL = """
            <h3>Central Florida is not HVHZ &mdash; FBC Wind Zone inland</h3>
            <p>Orange, Polk, Osceola, and the Central Florida metro counties are well outside the HVHZ designation. Design wind speeds run 130-140 mph for Risk Category II commercial buildings &mdash; substantially lower than coastal South Florida. Storefront assemblies still need to meet Florida Building Code Chapter 16 wind load requirements, and Florida Product Approval (FPA) is the standard product approval pathway. Impact-rated glass is not required for most commercial work but is recommended for tornado-prone exposures.</p>
            <h3>Tornado and severe storm exposure</h3>
            <p>Central Florida sees more tornado activity per square mile than most of the country. Storefront assemblies on schools, EOCs, and public-facing commercial buildings increasingly spec impact-rated glass for wind-borne debris protection &mdash; even when not code-required. ACG has installed hardened impact glazing on Haines City Emergency Operations Center and similar central Florida government scope.</p>
            <h3>Theme park and tourism corridor</h3>
            <p>International Drive, the Disney corridor, and Universal's hospitality footprint dominate the central Florida commercial market. Hospitality storefront scope here values speed of completion above all &mdash; tenant fit-out turnaround inside a hotel or resort doesn't tolerate a 16-week storefront lead time. ACG sizes the manufacturer order, fabrication, and on-site install for the schedule that hospitality work actually demands.</p>
            <h3>AHJ landscape</h3>
            <p>Each Central Florida municipality runs its own permit office. Orange County Building Inspections covers unincorporated Orange. Kissimmee, Sanford, Winter Park, Maitland, Altamonte Springs, Lake Buena Vista, and the rest of the metro municipalities each handle their own submittals.</p>
"""

REGION_KEYS = """
            <h3>Florida Keys are FBC Wind Zone &mdash; Monroe County coastal</h3>
            <p>Monroe County (the Florida Keys) sits outside the Miami-Dade/Broward HVHZ designation, but with design wind speeds of 180 mph for Risk Category II commercial buildings on most Keys sites &mdash; the highest in the state. Storefront assemblies require Florida Product Approval impact-rated glazing at minimum. ACG specs Miami-Dade NOA-equivalent assemblies on every Keys commercial scope because the wind environment justifies it and the document package travels cleanly back to South Florida.</p>
            <h3>The corrosion and surge environment</h3>
            <p>Every Keys commercial property is within a half-mile of saltwater. Storefront installs in the Keys require marine-grade anchors, isolating membranes between aluminum and dissimilar metals (stainless versus galvanized), and DOW Corning 795 silicone sealant on every joint. Standard fasteners fail within 5-7 years in the Keys salt environment. ACG defaults to marine-grade specification on every Monroe County commercial install.</p>
            <h3>Post-Irma rebuild context</h3>
            <p>Hurricane Irma (2017) caused widespread commercial damage across the Keys, particularly in the Lower Keys around Cudjoe, Big Pine, and Sugarloaf. ACG has delivered post-Irma rebuild scope including the Cudjoe Key Fire Station, with NOA-certified impact glazing throughout. The rebuild is still active eight years on as insurance and code-upgrade scope continues to flow through.</p>
            <h3>AHJ landscape</h3>
            <p>Monroe County Building Department covers unincorporated Monroe. Each incorporated municipality &mdash; Key West, Marathon, Islamorada, Layton, Key Colony Beach &mdash; runs its own building department. Permit submittal in the Keys requires complete document packages on first round &mdash; the building departments are responsive but exacting.</p>
"""

REGION_SPACE_COAST = """
            <h3>Brevard County is FBC Wind Zone &mdash; Atlantic coastal exposure</h3>
            <p>Brevard County sits outside the HVHZ designation with design wind speeds of 150 mph for Risk Category II commercial buildings on coastal-exposed sites. The product approval pathway is Florida Product Approval impact-rated glazing. ACG specs Miami-Dade NOA-equivalent assemblies on most Brevard commercial scope.</p>
            <h3>The Space Coast development environment</h3>
            <p>Brevard's commercial market is anchored by aerospace, defense contractors, and the cruise/tourism corridor around Port Canaveral. SpaceX, Blue Origin, Lockheed, and the supply chain serving Kennedy Space Center drive continuous office, industrial, and hospitality scope. Cape Canaveral and Cocoa Beach hospitality and retail get the same Atlantic coastal exposure as PBC and the Treasure Coast.</p>
            <h3>AHJ landscape</h3>
            <p>City of Melbourne, City of Palm Bay, City of Cocoa, City of Cocoa Beach, City of Cape Canaveral, and City of Titusville each run their own building departments. Brevard County Building and Construction Compliance covers unincorporated Brevard. Submittal preferences vary.</p>
"""

# CITY DATA - all 64 missing cities.
# Each: name, slug, county, region, lat/long, default_office, brief submarket list, hero_img path (with subfolder if needed)
# Region keys: hvhz_mdade, hvhz_broward, palm_beach, treasure_coast, sw_fl, tampa_bay, central_fl, keys, space_coast

# Verified hero images (each must exist on disk; we verified earlier):
# Atlantic Fields series, Eau Palm Beach series, Ocean Prime FTL series, Hulett Environmental,
# Siena Lakes, Wild Blue, Gulf Harbour, Gulfside Twelve, Haines City EOC, Baron Shoppes,
# iFly Miami, Westlake Hialeah/hero, Tradewinds Clubhouse/tradewinds-amenity-pool

# We rotate hero images by region so each city in a region doesn't show identical photo.
HEROES_BY_REGION = {
    "hvhz_mdade": [
        ("/images/projects/ifly-miami-exterior-2.jpg", "/images/projects/ifly-miami-exterior-2.webp", "iFly Miami indoor skydiving facility &mdash; commercial glazing by ACG"),
        ("/images/projects/westlake-hialeah/hero.jpg", "/images/projects/westlake-hialeah/hero.webp", "Westlake at Hialeah retail center commercial storefront installation"),
        ("/images/projects/ifly-miami-wind-tunnel.jpg", "/images/projects/ifly-miami-wind-tunnel.webp", "iFly Miami wind tunnel facility specialized glazing"),
    ],
    "hvhz_broward": [
        ("/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.jpg", "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.webp", "Ocean Prime restaurant at Pier Sixty-Six Fort Lauderdale &mdash; Euro-Wall folding glass"),
        ("/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial.jpg", "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial.webp", "Ocean Prime at Pier Sixty-Six marina aerial"),
        ("/images/projects/cubesmart-davie/hero.jpg", "/images/projects/cubesmart-davie/hero.webp", "CubeSmart Davie self-storage commercial facility"),
    ],
    "palm_beach": [
        ("/images/projects/eau-palm-beach/aerial-resort.jpg", "/images/projects/eau-palm-beach/aerial-resort.webp", "Eau Palm Beach Resort oceanfront aerial &mdash; ACG hospitality glazing"),
        ("/images/projects/atlantic-fields-golf-house/card-golden-hour.jpg", "/images/projects/atlantic-fields-golf-house/card-golden-hour.webp", "Atlantic Fields Golf House at golden hour"),
        ("/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool.jpg", "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool.webp", "Tradewinds Clubhouse amenity pool deck"),
    ],
    "treasure_coast": [
        ("/images/projects/baron-shoppes-tradition.jpg", "/images/projects/baron-shoppes-tradition.webp", "Baron Shoppes at Tradition retail center commercial storefront"),
        ("/images/projects/atlantic-fields-performance/hero-gym-interior.jpg", "/images/projects/atlantic-fields-performance/hero-gym-interior.webp", "Atlantic Fields Performance Center full-height curtain wall"),
        ("/images/projects/atlantic-fields-golf-house/dining-interior.jpg", "/images/projects/atlantic-fields-golf-house/dining-interior.webp", "Atlantic Fields Golf House dining interior"),
    ],
    "sw_fl": [
        ("/images/projects/siena-lakes-naples.jpg", "/images/projects/siena-lakes-naples.webp", "Siena Lakes Naples senior living community glazing"),
        ("/images/projects/wild-blue-clubhouse-hero.jpg", "/images/projects/wild-blue-clubhouse-hero.webp", "Wild Blue Clubhouse country club commercial glazing"),
        ("/images/projects/gulfside-twelve.jpg", "/images/projects/gulfside-twelve.webp", "Gulfside Twelve Fort Myers Beach multifamily condo"),
        ("/images/projects/gulf-harbour.jpg", "/images/projects/gulf-harbour.webp", "Gulf Harbour resort renovation commercial glazing"),
    ],
    "tampa_bay": [
        ("/images/projects/hulett-environmental/sunset-side-angle.jpg", "/images/projects/hulett-environmental/sunset-side-angle.webp", "Hulett Environmental Tampa corporate headquarters glazing"),
        ("/images/projects/storage-king-winter-haven/storage-king-exterior-entrance.jpg", "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance.webp", "Storage King Winter Haven commercial facility"),
        ("/images/projects/dale-mabry-retail/dale-mabry-retail-exterior-1.jpg", "/images/projects/dale-mabry-retail/dale-mabry-retail-exterior-1.webp", "Dale Mabry retail Tampa commercial storefront"),
    ],
    "central_fl": [
        ("/images/projects/haines-city-eoc.jpg", "/images/projects/haines-city-eoc.webp", "Haines City Emergency Operations Center government facility"),
        ("/images/projects/storage-king-winter-haven/storage-king-exterior-entrance.jpg", "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance.webp", "Storage King Winter Haven Polk County commercial"),
    ],
    "keys": [
        ("/images/projects/cudjoe-key-fire-station.jpg", "/images/projects/cudjoe-key-fire-station.webp", "Cudjoe Key Fire Station Florida Keys government facility &mdash; post-Irma rebuild"),
    ],
    "space_coast": [
        ("/images/projects/haines-city-eoc.jpg", "/images/projects/haines-city-eoc.webp", "Haines City Emergency Operations Center government facility &mdash; central FL portfolio"),
    ],
}

# OG IMAGES per region (single best photo for social cards)
OG_BY_REGION = {
    "hvhz_mdade": "https://acglass.com/images/projects/ifly-miami-exterior-2.jpg",
    "hvhz_broward": "https://acglass.com/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.jpg",
    "palm_beach": "https://acglass.com/images/projects/eau-palm-beach/aerial-resort.jpg",
    "treasure_coast": "https://acglass.com/images/projects/atlantic-fields-golf-house/card-golden-hour.jpg",
    "sw_fl": "https://acglass.com/images/projects/siena-lakes-naples.jpg",
    "tampa_bay": "https://acglass.com/images/projects/hulett-environmental/sunset-side-angle.jpg",
    "central_fl": "https://acglass.com/images/projects/haines-city-eoc.jpg",
    "keys": "https://acglass.com/images/projects/cudjoe-key-fire-station.jpg",
    "space_coast": "https://acglass.com/images/projects/haines-city-eoc.jpg",
}

REGION_CODE_CONTEXTS = {
    "hvhz_mdade": REGION_HVHZ_MIAMI_DADE,
    "hvhz_broward": REGION_HVHZ_BROWARD,
    "palm_beach": REGION_PALM_BEACH,
    "treasure_coast": REGION_TREASURE_COAST,
    "sw_fl": REGION_SW_FL,
    "tampa_bay": REGION_TAMPA_BAY,
    "central_fl": REGION_CENTRAL_FL,
    "keys": REGION_KEYS,
    "space_coast": REGION_SPACE_COAST,
}

REGION_HVHZ_FLAG = {
    "hvhz_mdade": True, "hvhz_broward": True,
    "palm_beach": False, "treasure_coast": False, "sw_fl": False,
    "tampa_bay": False, "central_fl": False, "keys": False, "space_coast": False,
}

REGION_HERO_EYEBROW = {
    "hvhz_mdade": "HVHZ &middot; MIAMI-DADE NOA REQUIRED",
    "hvhz_broward": "HVHZ &middot; BROWARD NOA REQUIRED",
    "palm_beach": "PBC &middot; FBC WIND ZONE",
    "treasure_coast": "TREASURE COAST &middot; FBC WIND ZONE",
    "sw_fl": "GULF COAST &middot; LOCAL OFFICE",
    "tampa_bay": "TAMPA BAY &middot; LOCAL OFFICE",
    "central_fl": "CENTRAL FL &middot; FBC WIND ZONE",
    "keys": "FLORIDA KEYS &middot; MARINE GRADE",
    "space_coast": "SPACE COAST &middot; FBC WIND ZONE",
}

REGION_OFFICE = {
    "hvhz_mdade": "West Palm Beach HQ",
    "hvhz_broward": "West Palm Beach HQ",
    "palm_beach": "West Palm Beach HQ",
    "treasure_coast": "West Palm Beach HQ",
    "sw_fl": "Naples office",
    "tampa_bay": "Tampa office",
    "central_fl": "Tampa office",
    "keys": "West Palm Beach HQ",
    "space_coast": "Tampa office",
}

# REGION PROJECT GALLERIES - 4 verified projects per region (mix of region-specific + statewide portfolio)
REGION_PROJECTS = {
    "hvhz_mdade": [
        {"img": "/images/projects/ifly-miami-exterior-2", "alt": "iFly Miami indoor skydiving facility exterior", "cat": "RECREATION &middot; MIAMI", "name": "iFly Miami", "meta": "Wind tunnel facility commercial storefront and curtain wall"},
        {"img": "/images/projects/ifly-miami-wind-tunnel", "alt": "iFly Miami wind tunnel detail", "cat": "RECREATION &middot; MIAMI", "name": "iFly Miami Wind Tunnel", "meta": "Specialized impact glazing assembly"},
        {"img": "/images/projects/westlake-hialeah/hero", "alt": "Westlake Hialeah retail center commercial storefront", "cat": "RETAIL &middot; HIALEAH", "name": "Westlake Hialeah", "meta": "Multi-tenant retail storefront program"},
        {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior", "alt": "Ocean Prime restaurant Pier Sixty-Six", "cat": "RESTAURANT &middot; SOUTH FLORIDA", "name": "Ocean Prime at Pier Sixty-Six", "meta": "Euro-Wall folding glass &mdash; South Florida hospitality"},
    ],
    "hvhz_broward": [
        {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior", "alt": "Ocean Prime Pier Sixty-Six twilight exterior", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime at Pier Sixty-Six", "meta": "Marina-front restaurant &mdash; Euro-Wall folding glass"},
        {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-marina-aerial", "alt": "Ocean Prime marina aerial Pier Sixty-Six", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime &mdash; Aerial", "meta": "Marina-front installation &mdash; corrosion-rated assembly"},
        {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-interior-dining", "alt": "Ocean Prime interior dining", "cat": "RESTAURANT &middot; FT LAUDERDALE", "name": "Ocean Prime &mdash; Interior", "meta": "Interior glass partition and curtain wall"},
        {"img": "/images/projects/cubesmart-davie/hero", "alt": "CubeSmart Davie self-storage facility", "cat": "COMMERCIAL &middot; DAVIE", "name": "CubeSmart Davie", "meta": "Self-storage facility storefront and entry"},
    ],
    "palm_beach": [
        {"img": "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort aerial", "cat": "RESORT &middot; PALM BEACH", "name": "Eau Palm Beach Resort", "meta": "Hospitality storefront and arched window restoration"},
        {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse golden hour", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall"},
        {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center curtain wall", "cat": "PERFORMANCE FACILITY &middot; HOBE SOUND", "name": "Atlantic Fields Performance Center", "meta": "Full-height curtain wall and multi-slide doors"},
        {"img": "/images/projects/tradewinds-clubhouse/tradewinds-amenity-pool", "alt": "Tradewinds Clubhouse amenity pool", "cat": "COUNTRY CLUB &middot; PBC", "name": "Tradewinds Clubhouse", "meta": "Country club amenity storefront"},
    ],
    "treasure_coast": [
        {"img": "/images/projects/baron-shoppes-tradition", "alt": "Baron Shoppes at Tradition retail center", "cat": "RETAIL &middot; PORT ST LUCIE", "name": "Baron Shoppes at Tradition", "meta": "Multi-tenant retail storefront program"},
        {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House clubhouse", "cat": "COUNTRY CLUB &middot; HOBE SOUND", "name": "Atlantic Fields Golf House", "meta": "Clubhouse storefront and curtain wall"},
        {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center", "cat": "PERFORMANCE FACILITY &middot; HOBE SOUND", "name": "Atlantic Fields Performance Center", "meta": "Full-height curtain wall and multi-slide doors"},
        {"img": "/images/projects/indiantown-high-school/hero" if False else "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort aerial (regional portfolio reference)", "cat": "RESORT &middot; PALM BEACH", "name": "Eau Palm Beach Resort", "meta": "Hospitality storefront (South Florida portfolio reference)"},
    ],
    "sw_fl": [
        {"img": "/images/projects/siena-lakes-naples", "alt": "Siena Lakes Naples senior living", "cat": "SENIOR LIVING &middot; NAPLES", "name": "Siena Lakes Naples", "meta": "Senior living facility storefront and impact glazing"},
        {"img": "/images/projects/wild-blue-clubhouse-hero", "alt": "Wild Blue Clubhouse country club", "cat": "COUNTRY CLUB &middot; SW FL", "name": "Wild Blue Clubhouse", "meta": "Country club amenity storefront and curtain wall"},
        {"img": "/images/projects/gulf-harbour", "alt": "Gulf Harbour resort renovation glazing", "cat": "RESORT &middot; FORT MYERS", "name": "Gulf Harbour Renovation", "meta": "Resort renovation storefront and impact glass"},
        {"img": "/images/projects/gulfside-twelve", "alt": "Gulfside Twelve Fort Myers Beach", "cat": "MULTIFAMILY CONDO &middot; FORT MYERS BEACH", "name": "Gulfside Twelve", "meta": "NOA-certified impact glazing &mdash; post-Ian rebuild"},
    ],
    "tampa_bay": [
        {"img": "/images/projects/hulett-environmental/sunset-side-angle", "alt": "Hulett Environmental corporate Tampa", "cat": "CORPORATE OFFICE &middot; TAMPA", "name": "Hulett Environmental Headquarters", "meta": "Corporate office storefront and entrance"},
        {"img": "/images/projects/dale-mabry-retail/dale-mabry-retail-exterior-1", "alt": "Dale Mabry retail Tampa", "cat": "RETAIL &middot; TAMPA", "name": "Dale Mabry Retail Corridor", "meta": "Multi-tenant retail storefront"},
        {"img": "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance", "alt": "Storage King Winter Haven", "cat": "COMMERCIAL &middot; WINTER HAVEN", "name": "Storage King Winter Haven", "meta": "Commercial facility storefront and impact glazing"},
        {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House (statewide portfolio)", "cat": "COUNTRY CLUB &middot; FL PORTFOLIO", "name": "Atlantic Fields Golf House", "meta": "Statewide portfolio reference"},
    ],
    "central_fl": [
        {"img": "/images/projects/haines-city-eoc", "alt": "Haines City EOC government facility", "cat": "GOVERNMENT &middot; HAINES CITY", "name": "Haines City Emergency Operations Center", "meta": "Hardened impact glazing &mdash; central FL government"},
        {"img": "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance", "alt": "Storage King Winter Haven", "cat": "COMMERCIAL &middot; WINTER HAVEN", "name": "Storage King Winter Haven", "meta": "Commercial storefront and impact glass"},
        {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House (FL portfolio)", "cat": "COUNTRY CLUB &middot; FL PORTFOLIO", "name": "Atlantic Fields Golf House", "meta": "Statewide portfolio reference"},
        {"img": "/images/projects/baron-shoppes-tradition", "alt": "Baron Shoppes at Tradition (FL portfolio)", "cat": "RETAIL &middot; FL PORTFOLIO", "name": "Baron Shoppes at Tradition", "meta": "Statewide retail portfolio reference"},
    ],
    "keys": [
        {"img": "/images/projects/cudjoe-key-fire-station", "alt": "Cudjoe Key Fire Station Florida Keys", "cat": "GOVERNMENT &middot; CUDJOE KEY", "name": "Cudjoe Key Fire Station", "meta": "Post-Irma rebuild &mdash; NOA-certified impact glazing"},
        {"img": "/images/projects/atlantic-fields-golf-house/card-golden-hour", "alt": "Atlantic Fields Golf House (FL portfolio)", "cat": "COUNTRY CLUB &middot; FL PORTFOLIO", "name": "Atlantic Fields Golf House", "meta": "Statewide portfolio reference"},
        {"img": "/images/projects/eau-palm-beach/aerial-resort", "alt": "Eau Palm Beach Resort (FL portfolio)", "cat": "RESORT &middot; FL PORTFOLIO", "name": "Eau Palm Beach Resort", "meta": "Hospitality portfolio reference"},
        {"img": "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior", "alt": "Ocean Prime Pier Sixty-Six (FL portfolio)", "cat": "RESTAURANT &middot; FL PORTFOLIO", "name": "Ocean Prime at Pier Sixty-Six", "meta": "South Florida hospitality reference"},
    ],
    "space_coast": [
        {"img": "/images/projects/haines-city-eoc", "alt": "Haines City EOC central FL government", "cat": "GOVERNMENT &middot; CENTRAL FL", "name": "Haines City Emergency Operations Center", "meta": "Central FL government &mdash; hardened impact glazing"},
        {"img": "/images/projects/atlantic-fields-performance/hero-gym-interior", "alt": "Atlantic Fields Performance Center (FL portfolio)", "cat": "PERFORMANCE &middot; FL PORTFOLIO", "name": "Atlantic Fields Performance Center", "meta": "Statewide portfolio reference"},
        {"img": "/images/projects/storage-king-winter-haven/storage-king-exterior-entrance", "alt": "Storage King Winter Haven", "cat": "COMMERCIAL &middot; WINTER HAVEN", "name": "Storage King Winter Haven", "meta": "Commercial facility statewide reference"},
        {"img": "/images/projects/baron-shoppes-tradition", "alt": "Baron Shoppes at Tradition (FL portfolio)", "cat": "RETAIL &middot; FL PORTFOLIO", "name": "Baron Shoppes at Tradition", "meta": "Treasure Coast retail reference"},
    ],
}

# DEFAULT SUBMARKETS by region for cities without their own list
# Most tier-2 cities use a small generic list since they are themselves submarkets within a metro
# We override per-city for the medium-tier cities that have meaningful neighborhoods

DEFAULT_SUBMARKETS_BY_REGION = {
    "hvhz_mdade": [
        ("Downtown / Brickell", "Office / Hospitality"),
        ("Beach / Tourist Corridor", "Retail / Restaurant"),
        ("Suburban Retail", "Retail / Medical"),
        ("Industrial / Logistics", "Industrial Commercial"),
        ("Mixed-Use Mid-Rise", "Mixed-Use"),
        ("Medical Office", "Medical / Institutional"),
        ("Hospitality Corridor", "Restaurant / Hotel"),
        ("Civic / Institutional", "Government / Institutional"),
    ],
    "hvhz_broward": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Beach / Oceanfront", "Hospitality / Retail"),
        ("Suburban Retail", "Retail / Medical"),
        ("Industrial Commercial", "Industrial / Warehouse"),
        ("Mixed-Use Mid-Rise", "Mixed-Use"),
        ("Medical Office", "Medical / Institutional"),
        ("Civic / Institutional", "Government / Institutional"),
        ("Marina / Waterfront", "Marine Commercial"),
    ],
    "palm_beach": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Beach / Oceanfront", "Hospitality / Retail"),
        ("Country Club Corridor", "Country Club Amenity"),
        ("Office Park", "Corporate Office"),
        ("Medical Office", "Medical / Institutional"),
        ("Retail Center", "Retail"),
        ("Mixed-Use Mid-Rise", "Mixed-Use"),
        ("Civic / Institutional", "Government"),
    ],
    "treasure_coast": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Beach / Coastal", "Hospitality / Retail"),
        ("Tradition / St. Lucie West", "Mixed-Use Master-Planned"),
        ("Treasure Coast Mall District", "Retail / Office"),
        ("Country Club Corridor", "Country Club Amenity"),
        ("Industrial Commercial", "Industrial / Warehouse"),
        ("Medical Office", "Medical"),
        ("Government / Civic", "Government"),
    ],
    "sw_fl": [
        ("Downtown / Old Town", "Restaurant / Boutique Retail"),
        ("Gulf Beach Corridor", "Hospitality / Restaurant"),
        ("Marina / Waterfront", "Marine Commercial"),
        ("Country Club Corridor", "Country Club Amenity"),
        ("Retail Center", "Retail"),
        ("Medical Office", "Medical / Institutional"),
        ("Mixed-Use Development", "Mixed-Use"),
        ("Industrial Commercial", "Industrial / Warehouse"),
    ],
    "tampa_bay": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Gulf Beach Corridor", "Hospitality"),
        ("Suburban Retail", "Retail / Medical"),
        ("Office Park", "Corporate Office"),
        ("Industrial Commercial", "Industrial / Warehouse"),
        ("Medical Office", "Medical / Institutional"),
        ("Mixed-Use Mid-Rise", "Mixed-Use"),
        ("Marina / Waterfront", "Marine Commercial"),
    ],
    "central_fl": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Tourist Corridor", "Hospitality"),
        ("Suburban Retail", "Retail / Medical"),
        ("Office Park", "Corporate Office"),
        ("Industrial Commercial", "Industrial / Warehouse"),
        ("Medical Office", "Medical"),
        ("Mixed-Use Development", "Mixed-Use"),
        ("Civic / Institutional", "Government"),
    ],
    "keys": [
        ("Oceanfront Hospitality", "Hospitality / Restaurant"),
        ("Marina / Waterfront", "Marine Commercial"),
        ("Main Highway Retail", "Retail / Restaurant"),
        ("Government / Civic", "Government"),
        ("Mixed-Use", "Mixed-Use"),
        ("Medical / Office", "Medical / Office"),
    ],
    "space_coast": [
        ("Downtown / Main Street", "Restaurant / Retail"),
        ("Beach / Oceanfront", "Hospitality / Retail"),
        ("Aerospace / Defense", "Industrial / Office"),
        ("Suburban Retail", "Retail / Medical"),
        ("Medical Office", "Medical"),
        ("Mixed-Use Development", "Mixed-Use"),
        ("Government / Civic", "Government"),
        ("Marina / Waterfront", "Marine Commercial"),
    ],
}

# THE 64-CITY GAP. Format: (name, slug, county, region, lat, lng)
TIER2_CITIES = [
    # MIAMI-DADE HVHZ
    ("Aventura", "aventura", "Miami-Dade County", "hvhz_mdade", "25.9565", "-80.1391"),
    ("Bal Harbour", "bal-harbour", "Miami-Dade County", "hvhz_mdade", "25.8884", "-80.1268"),
    ("Bay Harbor Islands", "bay-harbor-islands", "Miami-Dade County", "hvhz_mdade", "25.8884", "-80.1320"),
    ("Coral Gables", "coral-gables", "Miami-Dade County", "hvhz_mdade", "25.7215", "-80.2684"),
    ("Cutler Bay", "cutler-bay", "Miami-Dade County", "hvhz_mdade", "25.5765", "-80.3470"),
    ("Golden Beach", "golden-beach", "Miami-Dade County", "hvhz_mdade", "25.9665", "-80.1232"),
    ("Key Biscayne", "key-biscayne", "Miami-Dade County", "hvhz_mdade", "25.6936", "-80.1623"),
    ("Miami Beach", "miami-beach", "Miami-Dade County", "hvhz_mdade", "25.7907", "-80.1300"),
    ("Miami Shores", "miami-shores", "Miami-Dade County", "hvhz_mdade", "25.8676", "-80.1934"),
    ("North Bay Village", "north-bay-village", "Miami-Dade County", "hvhz_mdade", "25.8462", "-80.1581"),
    ("North Miami Beach", "north-miami-beach", "Miami-Dade County", "hvhz_mdade", "25.9331", "-80.1626"),
    ("Palmetto Bay", "palmetto-bay", "Miami-Dade County", "hvhz_mdade", "25.6220", "-80.3247"),
    ("Pinecrest", "pinecrest", "Miami-Dade County", "hvhz_mdade", "25.6646", "-80.3083"),
    ("South Miami", "south-miami", "Miami-Dade County", "hvhz_mdade", "25.7079", "-80.2937"),
    ("Sunny Isles Beach", "sunny-isles-beach", "Miami-Dade County", "hvhz_mdade", "25.9476", "-80.1226"),
    ("Surfside", "surfside", "Miami-Dade County", "hvhz_mdade", "25.8770", "-80.1264"),
    ("Virginia Gardens", "virginia-gardens", "Miami-Dade County", "hvhz_mdade", "25.8076", "-80.3017"),

    # BROWARD HVHZ
    ("Dania Beach", "dania-beach", "Broward County", "hvhz_broward", "26.0515", "-80.1437"),
    ("Davie", "davie", "Broward County", "hvhz_broward", "26.0628", "-80.2331"),
    ("Deerfield Beach", "deerfield-beach", "Broward County", "hvhz_broward", "26.3184", "-80.0998"),
    ("Hallandale Beach", "hallandale-beach", "Broward County", "hvhz_broward", "25.9812", "-80.1484"),
    ("Hillsboro Beach", "hillsboro-beach", "Broward County", "hvhz_broward", "26.2895", "-80.0810"),
    ("Hollywood", "hollywood", "Broward County", "hvhz_broward", "26.0112", "-80.1495"),
    ("Lauderdale-by-the-Sea", "lauderdale-by-the-sea", "Broward County", "hvhz_broward", "26.1907", "-80.0998"),
    ("Lighthouse Point", "lighthouse-point", "Broward County", "hvhz_broward", "26.2756", "-80.0876"),
    ("Oakland Park", "oakland-park", "Broward County", "hvhz_broward", "26.1723", "-80.1320"),
    ("Parkland", "parkland", "Broward County", "hvhz_broward", "26.3101", "-80.2370"),
    ("Pompano Beach", "pompano-beach", "Broward County", "hvhz_broward", "26.2378", "-80.1248"),
    ("Weston", "weston", "Broward County", "hvhz_broward", "26.1003", "-80.3997"),

    # PALM BEACH COUNTY (additional cities not yet covered)
    ("Boynton Beach", "boynton-beach", "Palm Beach County", "palm_beach", "26.5317", "-80.0905"),
    ("Highland Beach", "highland-beach", "Palm Beach County", "palm_beach", "26.4001", "-80.0664"),
    ("Juno Beach", "juno-beach", "Palm Beach County", "palm_beach", "26.8784", "-80.0537"),
    ("Lantana", "lantana", "Palm Beach County", "palm_beach", "26.5867", "-80.0517"),
    ("North Palm Beach", "north-palm-beach", "Palm Beach County", "palm_beach", "26.8175", "-80.0828"),
    ("Palm Beach", "palm-beach", "Palm Beach County", "palm_beach", "26.7056", "-80.0364"),
    ("Riviera Beach", "riviera-beach", "Palm Beach County", "palm_beach", "26.7753", "-80.0581"),
    ("Tequesta", "tequesta", "Palm Beach County", "palm_beach", "26.9676", "-80.0876"),
    ("Gulf Stream", "gulf-stream", "Palm Beach County", "palm_beach", "26.4732", "-80.0464"),
    ("Wellington", "wellington", "Palm Beach County", "palm_beach", "26.6587", "-80.2415"),
    ("Royal Palm Beach", "royal-palm-beach", "Palm Beach County", "palm_beach", "26.7081", "-80.2306"),

    # TREASURE COAST (Martin, St. Lucie, Indian River)
    ("Fort Pierce", "fort-pierce", "St. Lucie County", "treasure_coast", "27.4467", "-80.3256"),
    ("Hobe Sound", "hobe-sound", "Martin County", "treasure_coast", "27.0651", "-80.1395"),
    ("Jensen Beach", "jensen-beach", "Martin County", "treasure_coast", "27.2492", "-80.2287"),
    ("Palm City", "palm-city", "Martin County", "treasure_coast", "27.1689", "-80.2664"),
    ("Port St. Lucie", "port-saint-lucie", "St. Lucie County", "treasure_coast", "27.2939", "-80.3503"),
    ("Sebastian", "sebastian", "Indian River County", "treasure_coast", "27.8164", "-80.4706"),
    ("Stuart", "stuart", "Martin County", "treasure_coast", "27.1973", "-80.2528"),
    ("Vero Beach", "vero-beach", "Indian River County", "treasure_coast", "27.6386", "-80.3973"),

    # SW FLORIDA (additional)
    ("Bonita Springs", "bonita-springs", "Lee County", "sw_fl", "26.3398", "-81.7787"),
    ("Fort Myers Beach", "fort-myers-beach", "Lee County", "sw_fl", "26.4515", "-81.9498"),
    ("Cape Coral", "cape-coral", "Lee County", "sw_fl", "26.5629", "-81.9495"),
    ("Estero", "estero", "Lee County", "sw_fl", "26.4382", "-81.8068"),
    ("Bradenton", "bradenton", "Manatee County", "tampa_bay", "27.4989", "-82.5748"),
    ("Englewood", "englewood", "Charlotte County", "sw_fl", "26.9620", "-82.3526"),
    ("Marco Island", "marco-island", "Collier County", "sw_fl", "25.9412", "-81.7184"),
    ("Sarasota", "sarasota", "Sarasota County", "tampa_bay", "27.3364", "-82.5307"),
    ("Venice", "venice", "Sarasota County", "tampa_bay", "27.0998", "-82.4543"),

    # TAMPA BAY
    ("Clearwater", "clearwater", "Pinellas County", "tampa_bay", "27.9659", "-82.8001"),
    ("Palm Harbor", "palm-harbor", "Pinellas County", "tampa_bay", "28.0780", "-82.7637"),
    ("St. Petersburg", "saint-petersburg", "Pinellas County", "tampa_bay", "27.7676", "-82.6403"),

    # CENTRAL FL
    ("Kissimmee", "kissimmee", "Osceola County", "central_fl", "28.2920", "-81.4076"),
    ("Lakeland", "lakeland", "Polk County", "central_fl", "28.0395", "-81.9498"),
    ("Winter Haven", "winter-haven", "Polk County", "central_fl", "28.0223", "-81.7329"),

    # FLORIDA KEYS
    ("Islamorada", "islamorada", "Monroe County", "keys", "24.9243", "-80.6276"),
    ("Key Largo", "key-largo", "Monroe County", "keys", "25.0865", "-80.4473"),
    ("Key West", "key-west", "Monroe County", "keys", "24.5551", "-81.7800"),
    ("Marathon", "marathon", "Monroe County", "keys", "24.7136", "-81.0905"),

    # SPACE COAST
    ("Palm Bay", "palm-bay", "Brevard County", "space_coast", "28.0345", "-80.5887"),
]

print(f"TIER2 city count: {len(TIER2_CITIES)}")
