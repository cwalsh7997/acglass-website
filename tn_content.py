# -*- coding: utf-8 -*-
"""Per-page content for 8 Middle TN / Nashville glazing pages.
All facts checked against ACG-GROUND-TRUTH.md.
Code context standardized: IBC 2018 + Tennessee state amendments, ASCE 7-16,
V=115 mph (Risk Category II), IECC Climate Zone 4A, no HVHZ in Tennessee.
"""

# Shared building-code section (IBC 2018, TN amendments, ASCE 7-16 V=115, no HVHZ)
def code_section(city, county, permit_authority):
    return f'''  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Building code &amp; permits</div>
      <h2 class="section-h">Code context for {city} <span class="accent">commercial glazing.</span></h2>
      <p class="body-p"><strong>Model code.</strong> Tennessee builds to the 2018 International Building Code (IBC 2018) with Tennessee state amendments. {city} commercial fenestration is engineered to the structural and component-and-cladding wind provisions of <strong>ASCE 7-16</strong>, the referenced load standard for IBC 2018. There is <strong>no High-Velocity Hurricane Zone (HVHZ)</strong> anywhere in Tennessee, so Miami-Dade NOA product approval is not part of the {county} permit path the way it is in South Florida.</p>
      <p class="body-p"><strong>Wind load.</strong> Most {city} commercial sites design to an ultimate wind speed of <strong>V = 115 mph (Risk Category II)</strong> under ASCE 7-16, with Exposure B or C depending on terrain. ACG sizes mullions, anchors, and glass thickness to the actual component-and-cladding pressures for each elevation rather than to a single blanket number, and we deliver engineer-stamped shop drawings where the {permit_authority} or the EOR requires them.</p>
      <p class="body-p"><strong>Energy code.</strong> {county} sits in <strong>IECC Climate Zone 4A</strong>. Commercial fenestration typically targets a U-factor near 0.38&ndash;0.45 and SHGC near 0.40 on the prescriptive path, met with insulating low-E glass and thermally broken aluminum. ACG specifies framing and glass make-ups that hold the energy compliance path while meeting the structural and acoustic requirements of the building. See our <a href="/laminated-glass-tennessee.html">laminated glass guidance for Tennessee</a> and our <a href="/preglazed-systems-tennessee.html">pre-glazed systems overview</a> for how we shorten field schedule on these scopes.</p>
    </div>
  </section>'''


def acg_section(city):
    return f'''  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">ACG in {city}</div>
      <h2 class="section-h">Bidding {city} now, <span class="accent">crews on the ground Q3 2026.</span></h2>
      <p class="body-p"><strong>The honest version.</strong> American Commercial Glass is opening its <strong>Nashville office in Q3 2026</strong>. We do not yet have a Tennessee project portfolio &mdash; we are building it. What we bring to {city} is the operating system that delivered <strong>350+ commercial projects and more than 1M square feet of installed glazing across Florida</strong> since the company was founded in February 2021, with zero OSHA recordables and OSHA 30 on 100% of field crew.</p>
      <p class="body-p"><strong>Accepting bids today.</strong> You do not have to wait for the office to open. ACG is pricing {city} commercial glazing scopes now for Q3 2026 and later install windows, with the same <strong>48-hour bid turnaround</strong> we run in Florida. Send drawings, a BuildingConnected invite, or a written scope and you get budget and schedule back in two days.</p>
      <p class="body-p"><strong>Licensing, stated plainly.</strong> ACG holds Florida Certified General Contractor license CGC #1531993; that Florida license does not transfer to Tennessee. ACG <strong>secures Tennessee licensing on award</strong> &mdash; we obtain the required Tennessee contractor licensure for each project as it is awarded, so the paperwork is in place before mobilization. We carry <strong>$3M single / $6M aggregate</strong> bonding through Arch Insurance (A+ XV), plus general liability, workers&rsquo; comp, and commercial auto with additional-insured language standard.</p>
      <p class="body-p"><strong>How we run jobs.</strong> ACG is the only glazing contractor we know of running custom AI agents in production &mdash; subcontractor coordination and bid management, real-time job costing, and an autonomous CFO assistant &mdash; on top of a Procore-native submittal, RFI, and schedule workflow. For a GC, that means tighter submittals, faster RFI turns, and a dimension-locked rough opening before the field crew shows up. Start from the <a href="/nashville/">Nashville commercial glazing hub</a> or the statewide <a href="/tennessee-commercial-glazing/">Tennessee commercial glazing</a> page.</p>
    </div>
  </section>'''


PAGES = [
    # 1. DOWNTOWN NASHVILLE
    {
        "path": "nashville/downtown-nashville/index.html",
        "url": "https://acglass.com/nashville/downtown-nashville/",
        "city": "Downtown Nashville",
        "county": "Davidson County",
        "state_word": "TN",
        "nashville_child": True,
        "lat": 36.1627, "lon": -86.7816,
        "title": "Commercial Glazing Downtown Nashville TN | Curtain Wall",
        "meta": "Commercial glazing in Downtown Nashville, TN \u2014 high-rise curtain wall and Lower Broadway storefront. ACG opens Nashville Q3 2026; bidding now.",
        "answer": "Commercial glazing in Downtown Nashville means two scopes: high-rise unitized curtain wall and window wall on residential and office towers, and ground-floor storefront, entrances, and bar-front systems along Lower Broadway and the SoBro core. ACG bids both, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Unitized curtain wall</strong> &mdash; high-rise office and residential towers",
            "<strong>Stick-built curtain wall</strong> &mdash; mid-rise and podium levels",
            "Window wall for multifamily and hotel tower floors",
            "Ground-floor <strong>aluminum storefront</strong> for retail, lobby, and restaurant bays",
            "All-glass and herculite entrances, automatic sliders for lobbies",
            "Lower Broadway bar-front and operable wall systems",
            "Fire-rated glass at stair, exit, and tenant-separation assemblies",
            "Glass railings for amenity decks, mezzanines, and rooftop bars",
        ],
        "faqs": [
            ("Does ACG install high-rise curtain wall in Downtown Nashville?",
             "Yes. ACG installs both unitized and stick-built curtain wall for high-rise office and residential towers, plus window wall for hotel and multifamily floors. We engineer mullions, anchors, and glass make-ups to ASCE 7-16 component-and-cladding pressures for each elevation and deliver engineer-stamped shop drawings where required."),
            ("Can ACG handle ground-floor storefront for a Lower Broadway venue?",
             "Yes. The Lower Broadway and SoBro ground plane is storefront, entrance, and bar-front work \u2014 high-traffic, brand-driven, schedule-sensitive. ACG installs aluminum storefront, all-glass and herculite entrances, automatic sliders, and operable window walls for restaurants, bars, and retail in mixed-use towers."),
            ("Is Downtown Nashville in a hurricane impact zone?",
             "No. There is no High-Velocity Hurricane Zone in Tennessee, so Miami-Dade NOA product approval is not part of the Metro Nashville permit path. Downtown commercial glazing is engineered to IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II."),
            ("When can ACG mobilize on a Downtown Nashville project?",
             "ACG's Nashville office opens Q3 2026 and we are pricing Downtown scopes now. We secure Tennessee licensing on award, and standard commercial bids return within 48 hours."),
            ("Who does ACG bid to Downtown?",
             "ACG bids directly to general contractors, tower developers, hospitality groups, and commercial property owners in the Downtown and SoBro core, and is active on Procore and BuildingConnected."),
        ],
        "sections": [],  # filled below
    },
    # 2. GREEN HILLS
    {
        "path": "nashville/green-hills-nashville/index.html",
        "url": "https://acglass.com/nashville/green-hills-nashville/",
        "city": "Green Hills",
        "county": "Davidson County",
        "state_word": "Nashville, TN",
        "nashville_child": True,
        "lat": 36.1047, "lon": -86.8158,
        "title": "Commercial Glazing Green Hills Nashville TN | Storefront",
        "meta": "Commercial glazing in Green Hills, Nashville TN \u2014 retail storefront, medical office, and multifamily glazing. ACG opens Nashville Q3 2026.",
        "answer": "Green Hills commercial glazing is driven by upscale retail, medical office near Vanderbilt and Saint Thomas, and dense multifamily. The mix is storefront and curtain wall for retail and clinics plus window wall on residential podiums. ACG bids Green Hills now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Retail storefront</strong> &mdash; in-line and freestanding for The Mall at Green Hills corridor",
            "<strong>Medical office</strong> curtain wall and storefront for clinics and MOBs",
            "Window wall for multifamily and mixed-use podiums",
            "All-glass entrances and automatic sliders for retail and clinic lobbies",
            "Insulated low-E glass meeting Tennessee energy code",
            "Fire-rated glass at corridor, stair, and occupancy-separation assemblies",
            "Sound-attenuating laminated glass for clinics on busy corridors",
            "Glass railings for terraces and amenity levels",
        ],
        "faqs": [
            ("What commercial glazing does ACG do in Green Hills?",
             "ACG covers the full Division 08 envelope: retail storefront, medical office curtain wall and storefront, window wall for multifamily podiums, all-glass entrances, fire-rated assemblies, and glass railings. Green Hills leans retail and healthcare, so storefront and clinic glazing dominate the mix."),
            ("Can ACG glaze a medical office building near Vanderbilt?",
             "Yes. Medical office buildings near Vanderbilt and Saint Thomas need curtain wall or storefront, controlled entrances, and often acoustic laminated glass on busy corridors. ACG specifies thermally broken framing and insulating low-E make-ups that hold the IECC Zone 4A energy path while meeting clinic acoustic and infection-control detailing."),
            ("Does Green Hills require impact-rated glass?",
             "No. Tennessee has no HVHZ and does not require Miami-Dade impact-rated glass. Green Hills commercial glazing follows IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, generally V=115 mph Risk Category II. Laminated glass is specified for acoustics or safety, not hurricane code."),
            ("How fast can ACG turn a Green Hills retail bid?",
             "ACG returns bids on standard commercial plans within 48 hours. We are pricing Green Hills scopes now for the Q3 2026 Nashville office opening, with Tennessee licensing secured on award."),
            ("Does ACG work with national retail tenants and their GCs?",
             "Yes. ACG bids directly to general contractors, retail developers, healthcare systems, and multifamily developers. We are active on Procore and BuildingConnected and run a brand-driven, schedule-sensitive storefront process that fits national tenant timelines."),
        ],
        "sections": [],
    },
    # 3. BELLEVUE
    {
        "path": "nashville/bellevue-nashville/index.html",
        "url": "https://acglass.com/nashville/bellevue-nashville/",
        "city": "Bellevue",
        "county": "Davidson County",
        "state_word": "Nashville, TN",
        "nashville_child": True,
        "lat": 36.0756, "lon": -86.9486,
        "title": "Commercial Glazing Bellevue Nashville TN | Window Wall",
        "meta": "Commercial glazing in Bellevue, Nashville TN \u2014 multifamily window wall, retail storefront, and mixed-use on the west Nashville corridor. ACG opens Q3 2026.",
        "answer": "Bellevue is one of west Nashville's fastest-growing corridors, driven by multifamily and retail along the Highway 70 / Bellevue Place spine. The glazing mix is window wall and storefront for apartments and mixed-use, plus retail entrances. ACG bids Bellevue now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Window wall</strong> &mdash; garden and podium multifamily",
            "<strong>Retail storefront</strong> &mdash; Bellevue Place and Highway 70 corridor",
            "Mixed-use ground-floor commercial glazing",
            "Insulated low-E glass meeting Tennessee IECC Zone 4A energy code",
            "All-glass entrances and automatic sliders for retail and leasing offices",
            "Sound-attenuating laminated glass for units fronting busy roads",
            "Fire-rated glass at corridor and stair assemblies",
            "Glass railings for balconies, terraces, and amenity decks",
        ],
        "faqs": [
            ("What does ACG install in Bellevue?",
             "Bellevue's growth is multifamily and retail, so ACG's mix here is window wall and storefront for apartment podiums and mixed-use, plus retail entrances, leasing-office glazing, balcony railings, and corridor fire-rated assemblies. The full Division 08 envelope, single-source."),
            ("Does ACG do multifamily window wall in west Nashville?",
             "Yes. Window wall is a core ACG scope for garden and podium multifamily. We engineer the system to ASCE 7-16 component-and-cladding pressures, hit the IECC Zone 4A energy targets with insulating low-E glass, and add acoustic laminated make-ups for units fronting Highway 70."),
            ("Is impact glass required in Bellevue?",
             "No. Tennessee has no High-Velocity Hurricane Zone. Bellevue commercial glazing is built to IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II. Laminated glass is used for sound and safety, not hurricane approval."),
            ("Can ACG hold a multifamily delivery schedule?",
             "Yes. ACG locks rough-opening dimensions in pre-construction and runs a Procore-native submittal and RFI workflow, so field install runs on schedule. Lead times are typically 8\u201316 weeks from approved shop drawings plus field installation."),
            ("When can ACG start in Bellevue?",
             "ACG opens its Nashville office Q3 2026 and is pricing Bellevue scopes now for Q3 2026 and later install windows. Tennessee licensing is secured on award; bids return within 48 hours."),
        ],
        "sections": [],
    },
    # 4. BELLE MEADE
    {
        "path": "nashville/belle-meade-nashville/index.html",
        "url": "https://acglass.com/nashville/belle-meade-nashville/",
        "city": "Belle Meade",
        "county": "Davidson County",
        "state_word": "Nashville, TN",
        "nashville_child": True,
        "lat": 36.0964, "lon": -86.8597,
        "title": "Commercial Glazing Belle Meade Nashville TN | Storefront",
        "meta": "Commercial glazing in Belle Meade, Nashville TN \u2014 boutique retail, professional office, and private-club storefront and entrances. ACG opens Q3 2026.",
        "answer": "Belle Meade is a high-end residential city; its commercial glazing demand sits in the adjacent retail and professional-office corridors along Harding Pike and West End. The mix is boutique storefront, all-glass entrances, and small professional-office curtain wall. ACG bids Belle Meade now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Boutique retail storefront</strong> &mdash; Harding Pike and adjacent corridors",
            "<strong>All-glass and minimally framed entrances</strong> for upscale tenants",
            "Professional-office curtain wall and storefront",
            "Private-club and institutional glazing",
            "Insulated low-E glass meeting Tennessee energy code",
            "Decorative and low-iron glass for high-finish tenants",
            "Fire-rated glass where occupancy separations require it",
            "Glass railings for terraces and entries",
        ],
        "faqs": [
            ("What commercial glazing exists in Belle Meade?",
             "Belle Meade itself is predominantly high-end residential, so commercial glazing demand concentrates in the adjacent retail and professional-office corridors along Harding Pike and toward West End: boutique storefront, all-glass entrances, small office curtain wall, and private-club or institutional work."),
            ("Does ACG do high-finish, minimally framed storefront?",
             "Yes. Upscale Belle Meade-adjacent tenants often want minimally framed or all-glass entrances, low-iron or decorative glass, and clean sightlines. ACG installs herculite and pivot entrances, frameless systems, and high-finish storefront with the detailing those tenants expect."),
            ("Is impact-rated glass required around Belle Meade?",
             "No. Tennessee has no HVHZ and no impact-glass mandate. Commercial glazing here follows IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, generally V=115 mph Risk Category II. Laminated and low-iron glass are chosen for acoustics, security, or finish."),
            ("Will ACG bid a small professional-office scope?",
             "Yes. ACG bids small professional-office storefront and curtain wall as readily as large towers, with the same 48-hour bid turnaround and single-source Division 08 scope from frame to hardware to submittal."),
            ("When can ACG start near Belle Meade?",
             "ACG opens its Nashville office Q3 2026 and is pricing Belle Meade-area scopes now. Tennessee licensing is secured on award; bonding is $3M single / $6M aggregate."),
        ],
        "sections": [],
    },
    # 5. BERRY HILL
    {
        "path": "nashville/berry-hill-nashville/index.html",
        "url": "https://acglass.com/nashville/berry-hill-nashville/",
        "city": "Berry Hill",
        "county": "Davidson County",
        "state_word": "Nashville, TN",
        "nashville_child": True,
        "lat": 36.1142, "lon": -86.7689,
        "title": "Commercial Glazing Berry Hill Nashville TN | Storefront",
        "meta": "Commercial glazing in Berry Hill, Nashville TN \u2014 restaurant folding glass walls, creative-office storefront, and studio glazing. ACG opens Q3 2026.",
        "answer": "Berry Hill is Nashville's creative and restaurant district \u2014 recording studios, design firms, and chef-driven restaurants in converted bungalows and infill buildings. The glazing mix is restaurant folding glass walls, storefront, and creative-office entrances. ACG bids Berry Hill now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Euro-Wall folding glass walls</strong> and multi-slide doors for restaurants and patios",
            "<strong>Restaurant and cafe storefront</strong> with operable openings",
            "Creative-office and studio storefront and entrances",
            "All-glass and herculite entrances for boutique tenants",
            "Insulated low-E glass meeting Tennessee energy code",
            "Acoustic laminated glass for studios and music spaces",
            "Fire-rated glass where occupancy separations require it",
            "Glass railings for patios, mezzanines, and rooftop seating",
        ],
        "faqs": [
            ("Does ACG install folding glass walls for Berry Hill restaurants?",
             "Yes. ACG is an authorized installer for Euro-Wall folding glass walls and multi-slide systems \u2014 the indoor-outdoor patio openings that Berry Hill's chef-driven restaurants and bars want. We handle the operable system, the storefront around it, and the structural opening detailing as one scope."),
            ("What is the glazing mix in Berry Hill?",
             "Berry Hill is creative and hospitality: recording studios, design firms, and restaurants in converted bungalows and infill buildings. ACG's mix here is restaurant folding glass walls and storefront, creative-office and studio glazing, boutique entrances, acoustic laminated glass for music spaces, and patio railings."),
            ("Can ACG provide acoustic glazing for a recording studio?",
             "Yes. Studios need sound isolation. ACG specifies laminated and asymmetric insulating glass make-ups in thermally broken framing to raise STC while holding the IECC Zone 4A energy path. See our Tennessee laminated glass guidance for how we approach acoustic assemblies."),
            ("Is impact-rated glass required in Berry Hill?",
             "No. Tennessee has no High-Velocity Hurricane Zone. Berry Hill commercial glazing is engineered to IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II. Laminated glass is used for acoustics and safety."),
            ("When can ACG bid a Berry Hill restaurant build-out?",
             "Now. ACG returns standard commercial bids within 48 hours and is pricing Berry Hill scopes for the Q3 2026 Nashville office opening. Tennessee licensing is secured on award."),
        ],
        "sections": [],
    },
    # 6. HENDERSONVILLE
    {
        "path": "hendersonville-tn/index.html",
        "url": "https://acglass.com/hendersonville-tn/",
        "city": "Hendersonville",
        "county": "Sumner County",
        "state_word": "Tennessee",
        "nashville_child": False,
        "lat": 36.3048, "lon": -86.6200,
        "title": "Commercial Glazing Hendersonville TN | Storefront | ACG",
        "meta": "Commercial glazing in Hendersonville, TN \u2014 multifamily window wall, retail storefront, and medical office across Sumner County. ACG opens Q3 2026.",
        "answer": "Hendersonville, in Sumner County on Old Hickory Lake, is growing fast along the Vietnam Veterans Parkway and Gallatin Pike corridors with multifamily, retail, and medical office. The glazing mix is window wall and storefront. ACG bids Hendersonville now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Window wall</strong> &mdash; garden and podium multifamily",
            "<strong>Retail storefront</strong> &mdash; Gallatin Pike and Indian Lake corridors",
            "Medical office curtain wall and storefront",
            "Mixed-use ground-floor commercial glazing",
            "Insulated low-E glass meeting Tennessee IECC Zone 4A energy code",
            "All-glass entrances and automatic sliders",
            "Fire-rated glass at corridor and stair assemblies",
            "Glass railings for balconies and amenity decks",
        ],
        "faqs": [
            ("What does ACG install in Hendersonville?",
             "Hendersonville's growth in Sumner County is multifamily, retail, and medical office. ACG's mix is window wall and storefront for apartments and mixed-use, retail entrances, medical office curtain wall, fire-rated corridor assemblies, and balcony railings \u2014 the full Division 08 envelope, single-source."),
            ("Does ACG serve Sumner County?",
             "Yes. Hendersonville and the wider Sumner County corridor along Vietnam Veterans Parkway and Gallatin Pike are within ACG's Middle Tennessee service area from the Nashville office opening Q3 2026. We are pricing Sumner County scopes now."),
            ("Is impact-rated glass required in Hendersonville?",
             "No. Tennessee has no High-Velocity Hurricane Zone, so there is no Miami-Dade NOA requirement. Hendersonville commercial glazing follows IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II. Laminated glass is used for acoustics and safety."),
            ("Can ACG hold a multifamily delivery schedule in Hendersonville?",
             "Yes. ACG locks rough-opening dimensions in pre-construction and runs a Procore-native submittal and RFI workflow. Lead times are typically 8\u201316 weeks from approved shop drawings plus field installation, sequenced to the GC's schedule."),
            ("When can ACG start in Hendersonville?",
             "ACG's Nashville office opens Q3 2026 and we are pricing Hendersonville scopes now for Q3 2026 and later install windows. Tennessee licensing is secured on award; bids return within 48 hours."),
        ],
        "sections": [],
    },
    # 7. MT. JULIET
    {
        "path": "mt-juliet-tn/index.html",
        "url": "https://acglass.com/mt-juliet-tn/",
        "city": "Mt. Juliet",
        "county": "Wilson County",
        "state_word": "Tennessee",
        "nashville_child": False,
        "lat": 36.2001, "lon": -86.5186,
        "title": "Commercial Glazing Mt. Juliet TN | Storefront | ACG",
        "meta": "Commercial glazing in Mt. Juliet, TN \u2014 retail storefront, corporate office, and distribution glazing on the Wilson County I-40 corridor. ACG opens Q3 2026.",
        "answer": "Mt. Juliet, in Wilson County along I-40 east of Nashville, is one of Middle Tennessee's fastest-growing retail and corporate markets, anchored by Providence and major distribution and office development. The mix is retail storefront and corporate curtain wall. ACG bids Mt. Juliet now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Retail storefront</strong> &mdash; Providence Marketplace and I-40 corridor",
            "<strong>Corporate office</strong> curtain wall and storefront",
            "Industrial and distribution-center glazing and entrances",
            "Window wall for multifamily and mixed-use",
            "Insulated low-E glass meeting Tennessee IECC Zone 4A energy code",
            "All-glass entrances and automatic sliders",
            "Fire-rated glass at occupancy-separation and stair assemblies",
            "Glass railings for terraces and amenity levels",
        ],
        "faqs": [
            ("What commercial glazing does ACG do in Mt. Juliet?",
             "Mt. Juliet's growth in Wilson County is retail, corporate office, and distribution along I-40. ACG installs retail storefront, corporate curtain wall and storefront, distribution-center glazing and entrances, multifamily window wall, fire-rated assemblies, and railings \u2014 single-source Division 08."),
            ("Does ACG serve Wilson County?",
             "Yes. Mt. Juliet and the Wilson County I-40 corridor are within ACG's Middle Tennessee service area from the Nashville office opening Q3 2026. We are pricing Wilson County scopes now for Q3 2026 and later install windows."),
            ("Can ACG glaze a corporate office or Class A building in Mt. Juliet?",
             "Yes. Corporate office work calls for stick-built or unitized curtain wall, thermally broken framing, and insulating low-E glass that holds the IECC Zone 4A energy path. ACG engineers these systems to ASCE 7-16 pressures and delivers engineer-stamped shop drawings where required."),
            ("Is impact-rated glass required in Mt. Juliet?",
             "No. Tennessee has no High-Velocity Hurricane Zone. Mt. Juliet commercial glazing is built to IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II. Laminated glass is used for acoustics and safety, not hurricane code."),
            ("When can ACG start in Mt. Juliet?",
             "ACG opens its Nashville office Q3 2026 and is pricing Mt. Juliet scopes now. Tennessee licensing is secured on award; bonding is $3M single / $6M aggregate; bids return within 48 hours."),
        ],
        "sections": [],
    },
    # 8. COOL SPRINGS
    {
        "path": "cool-springs-tn/index.html",
        "url": "https://acglass.com/cool-springs-tn/",
        "city": "Cool Springs",
        "county": "Williamson County",
        "state_word": "Tennessee",
        "nashville_child": False,
        "lat": 35.9678, "lon": -86.8133,
        "title": "Commercial Glazing Cool Springs TN | Curtain Wall | ACG",
        "meta": "Commercial glazing in Cool Springs, TN \u2014 Class A office curtain wall, corporate HQ, retail, and healthcare in Williamson County. ACG opens Q3 2026.",
        "answer": "Cool Springs, spanning Franklin and Brentwood in Williamson County, is Middle Tennessee's premier Class A office and corporate-headquarters market, with deep retail and healthcare alongside. The glazing mix is multi-story curtain wall plus retail and clinic storefront. ACG bids Cool Springs now, opening its Nashville office Q3 2026.",
        "services": [
            "<strong>Class A office curtain wall</strong> &mdash; stick-built and unitized",
            "<strong>Corporate headquarters</strong> facade and entrance glazing",
            "Retail storefront along the McEwen and Mallory Lane corridors",
            "Healthcare and medical office curtain wall and storefront",
            "Window wall for mid-rise office and multifamily",
            "Insulated low-E glass meeting Tennessee IECC Zone 4A energy code",
            "All-glass entrances and automatic sliders for corporate lobbies",
            "Fire-rated glass and glass railings for atria and terraces",
        ],
        "faqs": [
            ("Does ACG install Class A office curtain wall in Cool Springs?",
             "Yes. Cool Springs is Williamson County's Class A office and corporate-headquarters market. ACG installs stick-built and unitized curtain wall, corporate facade and entrance glazing, and window wall for mid-rise office, engineered to ASCE 7-16 component-and-cladding pressures with engineer-stamped shop drawings where required."),
            ("What submarkets does ACG cover in Cool Springs?",
             "ACG covers the full Cool Springs footprint across Franklin and Brentwood \u2014 the McEwen Drive and Mallory Lane office and retail corridors, the Cool Springs Galleria area, and Maryland Way. Office curtain wall, retail storefront, and healthcare glazing are the dominant scopes."),
            ("Is impact-rated glass required in Cool Springs?",
             "No. Tennessee has no High-Velocity Hurricane Zone, so Miami-Dade NOA approval is not part of the Williamson County permit path. Cool Springs commercial glazing follows IBC 2018 with Tennessee amendments and ASCE 7-16 wind loads, typically V=115 mph Risk Category II."),
            ("Can ACG meet a corporate tenant's finish and energy requirements?",
             "Yes. Corporate Class A work demands tight sightlines, high-performance low-E glass, and thermally broken framing that holds the IECC Zone 4A energy path. ACG specifies make-ups that meet the structural, energy, acoustic, and finish requirements as one coordinated package."),
            ("When can ACG start in Cool Springs?",
             "ACG opens its Nashville office Q3 2026 and is pricing Cool Springs scopes now. We secure Tennessee licensing on award; bonding is $3M single / $6M aggregate; bids return within 48 hours."),
        ],
        "sections": [],
    },
]

# Assemble the 4 body sections for each page in spec order:
# 1) City context  2) ACG service from Nashville  3) Service mix  4) Code context
CONTEXT = {
    "Downtown Nashville": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Downtown Nashville context</div>
      <h2 class="section-h">What's being built <span class="accent">Downtown.</span></h2>
      <p class="body-p"><strong>Two distinct glazing markets stacked together.</strong> Downtown Nashville is in the middle of a high-rise cycle &mdash; office, residential, and hotel towers rising across the SoBro district and the Central Business District, while Lower Broadway runs a parallel boom of multi-story entertainment venues, bars, and restaurants. Above grade, the dominant scope is curtain wall and window wall on towers. At the street, it is storefront, entrances, and operable bar-front systems on a high-traffic, brand-driven ground plane.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are tower development (office and multifamily), hospitality and hotels, and the Lower Broadway entertainment district. Each carries different glazing requirements: towers need engineered curtain wall on tight crane and hoist schedules; hotels need lobby, amenity, and tower-floor glazing; and the entertainment venues need durable, operable storefront that takes heavy public use. ACG bids across all three.</p>
    </div>
  </section>''',
    "Green Hills": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Green Hills context</div>
      <h2 class="section-h">What's being built in <span class="accent">Green Hills.</span></h2>
      <p class="body-p"><strong>Retail, healthcare, and multifamily, tightly packed.</strong> Green Hills is one of Nashville's densest upscale submarkets, anchored by The Mall at Green Hills and a steady stream of retail redevelopment, multifamily, and mixed-use along Hillsboro Pike. Its position adjacent to Vanderbilt and near Saint Thomas keeps a strong medical-office and clinic pipeline running alongside the retail.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are upscale retail, medical office, and multifamily. That makes the glazing mix storefront and curtain wall for retail and clinics plus window wall on residential podiums &mdash; often with acoustic laminated glass where buildings front busy corridors. ACG bids the retail, the healthcare, and the residential ground-floor commercial as one Division 08 scope.</p>
    </div>
  </section>''',
    "Bellevue": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Bellevue context</div>
      <h2 class="section-h">What's being built in <span class="accent">Bellevue.</span></h2>
      <p class="body-p"><strong>A west Nashville multifamily corridor.</strong> Bellevue has shifted from a quiet suburban edge to one of west Nashville's fastest-growing corridors, with apartment and mixed-use development clustered around Bellevue Place and the Highway 70 spine, plus steady retail redevelopment serving the growing rooftops. The commercial glazing pipeline here tracks the residential growth.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are multifamily and the retail that follows it. The glazing mix is window wall and storefront for apartment podiums and mixed-use, retail entrances, leasing-office glazing, and balcony railings &mdash; with acoustic laminated make-ups for units fronting busy roads. ACG runs this scope single-source from frame to hardware to submittal.</p>
    </div>
  </section>''',
    "Belle Meade": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Belle Meade context</div>
      <h2 class="section-h">What's being built near <span class="accent">Belle Meade.</span></h2>
      <p class="body-p"><strong>High-end residential with adjacent commercial corridors.</strong> Belle Meade is one of Nashville's most established affluent cities, predominantly residential within its limits. The commercial glazing demand concentrates in the retail and professional-office corridors that ring it &mdash; along Harding Pike and toward West End &mdash; where boutique retail, professional services, and institutional buildings serve the surrounding neighborhoods.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are boutique retail, professional office, and private-club or institutional buildings. The glazing mix is high-finish storefront, minimally framed and all-glass entrances, small-scale curtain wall, and decorative or low-iron glass for tenants that want clean sightlines and a premium finish. ACG handles that detailing as readily as large commercial scopes.</p>
    </div>
  </section>''',
    "Berry Hill": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Berry Hill context</div>
      <h2 class="section-h">What's being built in <span class="accent">Berry Hill.</span></h2>
      <p class="body-p"><strong>A creative and restaurant district.</strong> Berry Hill is a small, dense city surrounded by Nashville, known for its recording studios, design and creative firms, and a growing roster of chef-driven restaurants and bars set in converted bungalows and infill buildings. The scale is intimate, the finishes are high, and the openings are often operable &mdash; indoor-outdoor patios that define the district's hospitality.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are hospitality (restaurants and bars), creative office, and recording and production studios. The glazing mix is restaurant folding glass walls and multi-slide systems, storefront with operable openings, creative-office and studio glazing, and acoustic laminated glass for music spaces. ACG is an authorized Euro-Wall installer for exactly this kind of operable, indoor-outdoor restaurant work.</p>
    </div>
  </section>''',
    "Hendersonville": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Hendersonville context</div>
      <h2 class="section-h">What's being built in <span class="accent">Hendersonville.</span></h2>
      <p class="body-p"><strong>Sumner County growth on Old Hickory Lake.</strong> Hendersonville is the largest city in Sumner County and one of the Nashville metro's strongest suburban growth markets, expanding along the Vietnam Veterans Parkway and Gallatin Pike corridors and around Indian Lake. New multifamily, retail centers, and medical office are the engine of its commercial construction.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are multifamily, retail, and medical office. The glazing mix is window wall and storefront for apartments and mixed-use, retail entrances, medical office curtain wall and storefront, and balcony railings &mdash; with acoustic laminated glass where units front busy roads. ACG bids the Sumner County corridor as part of its Middle Tennessee coverage.</p>
    </div>
  </section>''',
    "Mt. Juliet": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Mt. Juliet context</div>
      <h2 class="section-h">What's being built in <span class="accent">Mt. Juliet.</span></h2>
      <p class="body-p"><strong>Wilson County's I-40 growth engine.</strong> Mt. Juliet sits on I-40 just east of Nashville and has been one of Middle Tennessee's fastest-growing cities for years, anchored by the Providence retail district and a widening base of corporate office and distribution development that takes advantage of the interstate logistics access.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are retail, corporate office, and industrial and distribution. The glazing mix is retail storefront, corporate curtain wall and storefront, distribution-center glazing and entrances, and multifamily window wall as the residential base grows. ACG bids the Wilson County corridor as part of its Middle Tennessee coverage from the Nashville office.</p>
    </div>
  </section>''',
    "Cool Springs": '''  <section class="section">
    <div class="container">
      <div class="loc-label">Cool Springs context</div>
      <h2 class="section-h">What's being built in <span class="accent">Cool Springs.</span></h2>
      <p class="body-p"><strong>Middle Tennessee's Class A office market.</strong> Cool Springs spans Franklin and Brentwood in Williamson County and is the region's premier corporate and Class A office market, home to corporate headquarters, multi-story office buildings, healthcare campuses, and a deep retail and restaurant base anchored by the Cool Springs Galleria. The office pipeline here is the defining commercial glazing opportunity in the Nashville metro outside Downtown.</p>
      <p class="body-p"><strong>The dominant commercial sectors</strong> are Class A corporate office, healthcare, and retail. The glazing mix is multi-story stick-built and unitized curtain wall for office and headquarters buildings, retail storefront along the McEwen and Mallory Lane corridors, and clinic and medical-office glazing. ACG bids the office curtain wall, the retail, and the healthcare as one coordinated Division 08 scope.</p>
    </div>
  </section>''',
}

SVC_HEADERS = {
}

def service_section(p):
    li = "\n".join(f"        <li>{s}</li>" for s in p["services"])
    return f'''  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Service mix in {p['city']}</div>
      <h2 class="section-h">What ACG installs in <span class="accent">{p['city']}.</span></h2>
      <p class="body-p">ACG runs the full Division 08 envelope single-source &mdash; from the storefront frame to the hardware to the submittal package &mdash; and tailors the system mix to the {p['city']} submarket. As an authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora, we match the right manufacturer to each scope:</p>
      <ul class="svc-list">
{li}
      </ul>
    </div>
  </section>'''

PERMIT_AUTH = {
    "Davidson County": "Metro Nashville Codes office",
    "Sumner County": "City of Hendersonville codes office",
    "Wilson County": "City of Mt. Juliet codes office",
    "Williamson County": "Franklin or Brentwood codes office",
}

for _p in PAGES:
    pa = PERMIT_AUTH[_p["county"]]
    _p["sections"] = [
        CONTEXT[_p["city"]],
        acg_section(_p["city"]),
        service_section(_p),
        code_section(_p["city"], _p["county"], pa),
    ]
