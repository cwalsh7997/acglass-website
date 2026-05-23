"""ACG 80-city geo data set — used by generator.py
HVHZ = High-Velocity Hurricane Zone (Miami-Dade + Broward primarily, Palm Beach partial)
Exposure: C (inland) / D (direct coastal)
"""
# 80 cities matching AP Glazing's exact target list, augmented with our data
# Format: slug, display_name, county, hvhz, exposure, latitude, longitude, region, anchor_projects (slugs we have)
CITIES = [
    # South Florida — HVHZ
    ("aventura", "Aventura", "Miami-Dade", True, "C", 25.9565, -80.1393, "South Florida", []),
    ("bal-harbour-village", "Bal Harbour Village", "Miami-Dade", True, "D", 25.8884, -80.1267, "South Florida", []),
    ("bay-harbor-islands", "Bay Harbor Islands", "Miami-Dade", True, "D", 25.8884, -80.1278, "South Florida", []),
    ("boca-raton", "Boca Raton", "Palm Beach", False, "C", 26.3683, -80.1289, "South Florida", []),
    ("boynton-beach", "Boynton Beach", "Palm Beach", False, "C", 26.5253, -80.0664, "South Florida", []),
    ("coral-gables", "Coral Gables", "Miami-Dade", True, "C", 25.7215, -80.2684, "South Florida", []),
    ("cutler-bay", "Cutler Bay", "Miami-Dade", True, "C", 25.5783, -80.3460, "South Florida", []),
    ("dania-beach", "Dania Beach", "Broward", True, "D", 26.0512, -80.1439, "South Florida", []),
    ("davie", "Davie", "Broward", True, "C", 26.0628, -80.2331, "South Florida", []),
    ("deerfield-beach", "Deerfield Beach", "Broward", True, "D", 26.3184, -80.0998, "South Florida", []),
    ("delray-beach", "Delray Beach", "Palm Beach", False, "D", 26.4615, -80.0728, "South Florida", []),
    ("fort-lauderdale", "Fort Lauderdale", "Broward", True, "D", 26.1224, -80.1373, "South Florida",
        ["case-study-ocean-prime-fort-lauderdale"]),
    ("golden-beach", "Golden Beach", "Miami-Dade", True, "D", 25.9684, -80.1228, "South Florida", []),
    ("gulfstream", "Gulf Stream", "Palm Beach", False, "D", 26.4778, -80.0639, "South Florida", []),
    ("hallandale-beach", "Hallandale Beach", "Broward", True, "D", 25.9812, -80.1484, "South Florida", []),
    ("highland-beach", "Highland Beach", "Palm Beach", False, "D", 26.4045, -80.0648, "South Florida", []),
    ("hillsboro-beach", "Hillsboro Beach", "Broward", True, "D", 26.2843, -80.0795, "South Florida", []),
    ("hollywood-florida", "Hollywood", "Broward", True, "D", 26.0112, -80.1495, "South Florida", []),
    ("juno-beach", "Juno Beach", "Palm Beach", False, "D", 26.8784, -80.0539, "South Florida", []),
    ("jupiter", "Jupiter", "Palm Beach", False, "D", 26.9342, -80.0942, "South Florida", []),
    ("key-biscayne-village", "Key Biscayne", "Miami-Dade", True, "D", 25.6940, -80.1626, "South Florida", []),
    ("lantana", "Lantana", "Palm Beach", False, "C", 26.5867, -80.0517, "South Florida", []),
    ("lauderdale-by-the-sea", "Lauderdale-by-the-Sea", "Broward", True, "D", 26.1909, -80.0934, "South Florida", []),
    ("lighthouse-point", "Lighthouse Point", "Broward", True, "D", 26.2756, -80.0876, "South Florida", []),
    ("manalapan", "Manalapan", "Palm Beach", False, "D", 26.5817, -80.0386, "South Florida", ["case-study-eau-palm-beach"]),
    ("miami", "Miami", "Miami-Dade", True, "C", 25.7617, -80.1918, "South Florida", []),
    ("miami-beach", "Miami Beach", "Miami-Dade", True, "D", 25.7907, -80.1300, "South Florida", []),
    ("miami-shores-village", "Miami Shores", "Miami-Dade", True, "C", 25.8635, -80.1931, "South Florida", []),
    ("north-bay-village", "North Bay Village", "Miami-Dade", True, "D", 25.8462, -80.1561, "South Florida", []),
    ("north-miami-beach", "North Miami Beach", "Miami-Dade", True, "C", 25.9331, -80.1625, "South Florida", []),
    ("north-palm-beach", "North Palm Beach", "Palm Beach", False, "D", 26.8175, -80.0820, "South Florida", []),
    ("oakland-park", "Oakland Park", "Broward", True, "C", 26.1726, -80.1310, "South Florida", []),
    ("palm-beach", "Palm Beach", "Palm Beach", False, "D", 26.7056, -80.0364, "South Florida", []),
    ("palm-beach-gardens", "Palm Beach Gardens", "Palm Beach", False, "C", 26.8234, -80.1387, "South Florida",
        ["case-study-baron-shoppes-tradition"]),
    ("palm-city", "Palm City", "Martin", False, "C", 27.1689, -80.2664, "South Florida", []),
    ("palmetto-bay-village", "Palmetto Bay", "Miami-Dade", True, "C", 25.6234, -80.3247, "South Florida", []),
    ("parkland", "Parkland", "Broward", True, "C", 26.3098, -80.2371, "South Florida", []),
    ("pinecrest", "Pinecrest", "Miami-Dade", True, "C", 25.6645, -80.3083, "South Florida", []),
    ("pompano-beach", "Pompano Beach", "Broward", True, "D", 26.2379, -80.1248, "South Florida", []),
    ("riviera-beach", "Riviera Beach", "Palm Beach", False, "D", 26.7753, -80.0581, "South Florida", []),
    ("south-miami", "South Miami", "Miami-Dade", True, "C", 25.7079, -80.2934, "South Florida", []),
    ("sunny-isles-beach", "Sunny Isles Beach", "Miami-Dade", True, "D", 25.9462, -80.1228, "South Florida", []),
    ("surfside", "Surfside", "Miami-Dade", True, "D", 25.8779, -80.1267, "South Florida", []),
    ("tequesta", "Tequesta", "Palm Beach", False, "C", 26.9956, -80.1281, "South Florida", []),
    ("virginia-gardens", "Virginia Gardens", "Miami-Dade", True, "C", 25.8128, -80.3034, "South Florida", []),
    ("west-palm-beach", "West Palm Beach", "Palm Beach", False, "C", 26.7153, -80.0534, "South Florida",
        ["case-study-hulett-environmental"]),
    ("weston", "Weston", "Broward", True, "C", 26.1003, -80.3998, "South Florida", []),

    # Treasure Coast
    ("fort-pierce", "Fort Pierce", "St. Lucie", False, "D", 27.4467, -80.3256, "Treasure Coast", []),
    ("hobe-sound", "Hobe Sound", "Martin", False, "D", 27.0658, -80.1395, "Treasure Coast",
        ["case-study-atlantic-fields", "case-study-atlantic-fields-performance-center"]),
    ("jensen-beach", "Jensen Beach", "Martin", False, "D", 27.2531, -80.2298, "Treasure Coast", []),
    ("port-saint-lucie", "Port St. Lucie", "St. Lucie", False, "C", 27.2939, -80.3503, "Treasure Coast", []),
    ("sebastian", "Sebastian", "Indian River", False, "D", 27.8164, -80.4706, "Treasure Coast", []),
    ("stuart", "Stuart", "Martin", False, "D", 27.1973, -80.2528, "Treasure Coast",
        ["case-study-martin-county-fire-training"]),
    ("vero-beach", "Vero Beach", "Indian River", False, "D", 27.6386, -80.3973, "Treasure Coast",
        ["klus-lighting-vero-beach", "sroa-vero-beach"]),

    # Southwest Florida
    ("bonita-springs", "Bonita Springs", "Lee", False, "D", 26.3398, -81.7787, "Southwest Florida",
        ["case-study-causeway-building-bonita-springs"]),
    ("fort-myers", "Fort Myers", "Lee", False, "C", 26.6406, -81.8723, "Southwest Florida",
        ["case-study-illumia-fort-myers"]),
    ("fort-myers-beach", "Fort Myers Beach", "Lee", False, "D", 26.4515, -81.9498, "Southwest Florida",
        ["case-study-gulfside-twelve"]),
    ("englewood", "Englewood", "Sarasota", False, "D", 26.9620, -82.3526, "Southwest Florida", []),
    ("marco-island", "Marco Island", "Collier", False, "D", 25.9412, -81.7184, "Southwest Florida", []),
    ("naples", "Naples", "Collier", False, "D", 26.1420, -81.7948, "Southwest Florida",
        ["case-study-gulf-harbour", "siena-lakes-naples"]),
    ("bradenton", "Bradenton", "Manatee", False, "C", 27.4989, -82.5748, "Southwest Florida", []),
    ("sarasota", "Sarasota", "Sarasota", False, "D", 27.3364, -82.5307, "Southwest Florida", []),
    ("venice", "Venice", "Sarasota", False, "D", 27.0998, -82.4543, "Southwest Florida", []),

    # Tampa Bay / Central FL
    ("clearwater", "Clearwater", "Pinellas", False, "D", 27.9659, -82.8001, "Tampa Bay", []),
    ("lakeland", "Lakeland", "Polk", False, "C", 28.0395, -81.9498, "Central Florida", []),
    ("palm-bay", "Palm Bay", "Brevard", False, "D", 28.0345, -80.5887, "Space Coast", []),
    ("palm-harbor", "Palm Harbor", "Pinellas", False, "D", 28.0780, -82.7637, "Tampa Bay", []),
    ("st-petersburg", "St. Petersburg", "Pinellas", False, "D", 27.7676, -82.6403, "Tampa Bay", []),
    ("tampa", "Tampa", "Hillsborough", False, "C", 27.9506, -82.4572, "Tampa Bay", []),
    ("winter-heaven", "Winter Haven", "Polk", False, "C", 28.0222, -81.7328, "Central Florida",
        ["case-study-haines-city-eoc"]),
    ("kissimmee", "Kissimmee", "Osceola", False, "C", 28.2920, -81.4076, "Central Florida", []),
    ("orlando", "Orlando", "Orange", False, "C", 28.5384, -81.3789, "Central Florida", []),

    # Florida Keys
    ("florida-keys", "Florida Keys", "Monroe", True, "D", 24.7000, -81.0000, "Florida Keys",
        ["case-study-cudjoe-key"]),
    ("islamorada", "Islamorada", "Monroe", True, "D", 24.9242, -80.6275, "Florida Keys", []),
    ("key-largo", "Key Largo", "Monroe", True, "D", 25.0865, -80.4473, "Florida Keys", []),
    ("key-west", "Key West", "Monroe", True, "D", 24.5551, -81.7800, "Florida Keys", []),
    ("marathon", "Marathon", "Monroe", True, "D", 24.7136, -81.0900, "Florida Keys", []),
]

# Florida counties served (matches AP's list)
COUNTIES = [
    "Monroe", "Miami-Dade", "Broward", "Palm Beach", "Martin", "St. Lucie",
    "Indian River", "Brevard", "Collier", "Lee", "Charlotte", "Sarasota",
    "Manatee", "Hillsborough", "Pinellas", "Pasco", "Polk", "Hernando",
    "Orange", "Osceola", "Seminole", "Volusia"
]

# Services AP Glazing covers — plus our specialty services
SERVICES = [
    {
        "slug": "commercial-storefronts",
        "name": "Commercial Storefronts",
        "h1": "Commercial Storefront Installation",
        "intent_keyword": "commercial storefronts",
        "schema_service": "Commercial Storefront Installation",
        "price_low": 66,
        "price_high": 142,
        "price_unit": "SF",
        "intro": "Storefront installation for ground-floor retail, restaurants, and commercial buildings. Aluminum framing, single-source glazing, code-compliant submittal package.",
        "faqs": [
            ("What does a commercial storefront cost in {city}?", "A typical commercial storefront installation in {city} runs $66 to $142 per square foot installed, depending on glass make-up, frame finish, and exposure category. ACG's bids include material, labor, NOA or Florida Product Approval documentation, and full local building department submittal package."),
            ("How long does a storefront install take in {city}?", "Lead times for commercial storefront systems in {city} are typically 10 to 16 weeks from approved shop drawings to factory delivery. Field installation runs 3 to 7 days for a standard 30-foot storefront. ACG locks rough opening dimensions and storm-condition operation in pre-construction so the field schedule holds."),
            ("Are commercial storefronts in {city} HVHZ-rated?", "{hvhz_storefront_answer}"),
            ("Who is the best commercial storefront contractor in {city}?", "ACG is a Florida storefront glazing company (CGC #1531993) serving {city} with 350+ commercial projects completed across the state. We do all things commercial storefront, windows, and doors. We install storefronts for general contractors, restaurant operators, hospitality groups, healthcare systems, and developers. 48-hour bid turnaround on commercial scopes."),
        ]
    },
    {
        "slug": "all-glass-entrances",
        "name": "All-Glass Entrances",
        "h1": "All-Glass Entrance Installation",
        "intent_keyword": "all glass entrances",
        "schema_service": "All-Glass Entrance Installation",
        "price_low": 4500,
        "price_high": 18000,
        "price_unit": "opening",
        "intro": "Frameless and minimally framed all-glass entrance door systems. Pivot doors, automatic sliders, and herculite-style entrances for retail, hospitality, and commercial lobbies.",
        "faqs": [
            ("How much does an all-glass entrance cost in {city}?", "An all-glass entrance system in {city} typically runs $4,500 to $18,000 per opening depending on configuration (single, double, automatic), glass thickness, and hardware finish. ACG provides material + labor + submittal documentation in the all-in number."),
            ("Are all-glass entrances code-compliant in {city}?", "{hvhz_entrance_answer}"),
            ("How long does an all-glass entrance take to install in {city}?", "Lead time is 6 to 10 weeks from approved shop drawings. Field install is 1 to 2 days for a typical opening. ACG's submittal package includes hardware spec, glass make-up, and engineer documentation if the project requires."),
            ("Who installs all-glass entrances in {city}?", "ACG (CGC #1531993) installs all-glass commercial entrance systems across {city} and the rest of Florida. We are a storefront glazing company sourcing hardware from major commercial brands. Single-source from glass to hardware to automatic operator coordination."),
        ]
    },
    {
        "slug": "impact-windows-hurricane",
        "name": "Hurricane Impact Windows & Doors",
        "h1": "Hurricane Impact Windows and Doors",
        "intent_keyword": "hurricane impact windows doors",
        "schema_service": "Hurricane Impact Window and Door Installation",
        "price_low": 78,
        "price_high": 195,
        "price_unit": "SF",
        "intro": "Hurricane-rated impact windows and doors for commercial buildings. ESWindows, PGT, Slimpact authorized installer. HVHZ-rated configurations with Miami-Dade NOA documentation where required.",
        "faqs": [
            ("What's the cost of commercial impact windows in {city}?", "Commercial impact window installations in {city} run $78 to $195 per square foot installed, with HVHZ-rated configurations and Exposure D coastal sites at the upper end of the range. All-in pricing covers material, labor, NOA or product approval documentation."),
            ("Are impact windows required in {city}?", "{hvhz_impact_answer}"),
            ("How long does impact window installation take in {city}?", "Commercial impact window lead times in {city} run 10 to 14 weeks from approved shop drawings. Field installation is 4 to 8 days for a typical commercial scope. ACG coordinates with the GC's schedule and pulls NOAs current at submittal."),
            ("Who is the best impact window installer in {city}?", "ACG is a Florida storefront glazing company specializing in commercial impact windows and doors. CGC #1531993, $3M/$6M bonding, 350+ commercial projects. Authorized installer for major commercial impact glass manufacturers. We install impact windows for restaurants, hospitality, healthcare, multifamily, and institutional projects across {city}."),
        ]
    },
    {
        "slug": "glass-railings",
        "name": "Glass Railings",
        "h1": "Glass Railing Installation",
        "intent_keyword": "glass railings",
        "schema_service": "Glass Railing Installation",
        "price_low": 145,
        "price_high": 385,
        "price_unit": "LF",
        "intro": "Glass railing systems for balconies, terraces, stairs, and pool decks. Tempered or laminated glass infill, top-rail or frameless, stainless or aluminum hardware.",
        "faqs": [
            ("What does a glass railing cost in {city}?", "Glass railings in {city} run $145 to $385 per linear foot installed depending on glass type (tempered vs laminated), hardware finish (anodized aluminum vs stainless), and top-rail vs frameless. Coastal sites with stainless 316 hardware run at the upper end."),
            ("Are glass railings code-compliant in {city}?", "Yes, ACG installs glass railings to Florida Building Code Section 1607.8 (loading), ASTM E2358 (testing standard for guards), and ASTM E1300 (glass strength). Tempered glass meets CPSC 16 CFR 1201 Category II. Heat-soak-tested glass is available on request for spontaneous-breakage mitigation."),
            ("How long does a glass railing install take in {city}?", "Glass railing lead time is 6 to 9 weeks from approved shop drawings. Field install is 2 to 4 days for a typical multifamily balcony stack or commercial terrace. ACG locks structural connection details and dimensions in pre-construction."),
            ("Who installs glass railings in {city}?", "ACG (CGC #1531993), a Florida storefront and commercial glazing company, installs glass railing systems across {city} for multifamily, hospitality, restaurant terrace, and commercial pool deck applications. Stainless 316 hardware for coastal sites available on request."),
        ]
    },
]
