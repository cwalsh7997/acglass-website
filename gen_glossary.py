# -*- coding: utf-8 -*-
import json, html

# Each term: (term, category, definition_html, link_text_or_None, link_href_or_None)
# definition is 50-100 words. Internal links use ../ relative to /glossary/
T = [
# ---- SYSTEMS ----
("Curtain Wall","systems",
 "A non-load-bearing aluminum-and-glass facade hung off the building structure rather than resting on it. The wall carries only its own weight plus wind and seismic loads, which transfer back to the floor slabs. Curtain wall spans multiple floors as a continuous skin and is engineered for water management, thermal movement, and high design pressures. ACG installs glazed aluminum curtain wall on commercial and institutional projects across Florida.",
 "curtain wall systems","../curtainwall-systems.html"),
("Window Wall","systems",
 "An aluminum-and-glass system installed floor-to-floor between slabs, bearing on the slab below and sealed to the slab above. Unlike curtain wall, which hangs past the slab edge, window wall sits within each floor and is common in multifamily and mid-rise construction because it ships in shippable, slab-height units and simplifies edge-of-slab detailing. The trade-off is more horizontal joints to weatherproof.",
 "curtain wall vs window wall","../curtainwall-vs-window-wall.html"),
("Storefront","systems",
 "A non-residential, front-set aluminum framing system glazed at grade or first-floor level, typically up to about 10 feet tall. Storefront uses center-set or front-set glazing in a stick-built frame and is the most common entrance-and-glass system for retail, restaurant, and ground-floor commercial space. It is engineered for pedestrian traffic and door integration rather than the multi-story spans of curtain wall.",
 "commercial storefront systems","../commercial-storefront-systems.html"),
("Multi-Slide Door","systems",
 "A large-format glass door system whose panels slide and stack along a track to open a wall to the outdoors. Multi-slide units can span very wide openings with minimal frame, pocketing into a wall cavity or stacking at the jamb. In Florida they must carry impact and design-pressure ratings for hurricane zones. ACG supplies and installs multi-slide systems from Euro-Wall and ESWindows.",
 "multi-slide and bifold doors","../multi-slide-bifold-doors.html"),
("Bifold Door","systems",
 "A folding glass wall whose panels are hinged together and concertina to one or both sides of the opening, fully clearing the span when open. Common in hospitality and restaurant spaces that open to a patio, bifold systems run on a top track or bottom track. Florida applications require impact-rated glass and tested design pressures. ACG installs bifold systems on commercial projects.",
 "bifold glass walls","../blog/bi-fold-glass-walls-restaurants-hospitality.html"),
("All-Glass Entrance","systems",
 "A frameless or minimally framed entrance built from tempered glass with patch fittings, rails, and floor-mounted pivots rather than a full aluminum frame. All-glass entrances give a clean, transparent storefront look and are common in lobbies and high-end retail. They require tempered safety glass, careful hardware coordination, and ADA-compliant operation. ACG fabricates and installs all-glass entrance systems.",
 "frameless glass doors","../blog/frameless-glass-doors-commercial-spaces.html"),
("Structural Silicone Glazing (SSG)","systems",
 "A glazing method that bonds glass to the aluminum frame with structural silicone adhesive instead of mechanical pressure plates and caps. SSG produces a flush, gasket-free exterior with continuous glass planes and no visible metal on the captured edges. It demands strict quality control on surface prep, silicone cure, and bite dimensions, and is engineered to transfer wind load through the sealant joint.",
 None,None),
("Unitized vs. Stick System","systems",
 "Two ways to build a curtain wall. A stick system is assembled piece by piece on site — mullions, then glass — which is flexible and lower in tooling cost but slower in the field. A unitized system arrives as factory-assembled, pre-glazed panels that crews hang in sequence, cutting field labor and weather exposure on larger jobs. The choice trades shop cost against field speed and quality control.",
 "how we spec storefront","../blog/how-to-spec-commercial-storefront.html"),
# ---- GLASS TYPES ----
("Tempered Glass","glass-types",
 "Glass that is heat-treated to roughly four times the strength of standard annealed glass and, when broken, fragments into small blunt pieces instead of sharp shards. It is a safety glazing required by code in doors, sidelites, and other hazardous locations. Tempered glass cannot be cut or drilled after treatment, so all fabrication happens before tempering.",
 "commercial glass types","../blog/commercial-glass-types-explained.html"),
("Laminated Glass","glass-types",
 "Two or more glass plies permanently bonded to an interlayer (typically PVB or SGP) that holds fragments in place when the glass breaks. Lamination provides safety, security, sound control, and UV reduction, and it is the core of most impact-resistant hurricane glazing. The interlayer keeps the opening sealed after a missile strike, which is what lets laminated assemblies pass large-missile impact testing.",
 "impact glass vs laminated glass","../blog/impact-glass-vs-laminated-glass-commercial.html"),
("Low-E Glass","glass-types",
 "Glass coated with a microscopically thin, transparent layer that reflects infrared and ultraviolet energy while letting visible light pass. Low-emissivity coatings cut solar heat gain and improve insulating performance, which is central to meeting Florida's energy code on commercial buildings. Coating placement on a specific surface of an insulating unit tunes the balance between heat rejection and daylight.",
 "what is low-E glass","../blog/what-is-low-e-glass-commercial.html"),
("Insulating Glass Unit (IGU)","glass-types",
 "Two or more glass lites separated by a sealed spacer with a dry or gas-filled cavity between them, assembled to reduce heat transfer and condensation. The perimeter seal is what determines IGU service life — seal failure lets moisture in and causes the fogging seen in older units. Commercial IGUs often combine low-E coatings and laminated lites for energy and impact performance together.",
 "why commercial glass fogs","../blog/why-does-commercial-glass-fog-up-and-how-to-fix-it.html"),
("SGCC","glass-types",
 "The Safety Glazing Certification Council, the independent body that certifies safety glazing materials (tempered and laminated glass) to ANSI Z97.1 and federal CPSC 16 CFR 1201. An SGCC-listed permanent mark on a lite tells the inspector and the AHJ that the product was tested and is monitored under an ongoing certification program — a routine requirement on commercial glazing submittals.",
 None,None),
("FBC-Approved Glass","glass-types",
 "Glass and glazing assemblies that carry the approvals required for use under the Florida Building Code — either a statewide Florida Product Approval or, in High-Velocity Hurricane Zones, a Miami-Dade Notice of Acceptance. \u201CFBC-approved\u201D is shorthand for a product whose test data, installation instructions, and limitations have been accepted for use in Florida. ACG only specifies glazing with current, valid Florida approvals.",
 "Florida product approval","../florida-hvhz-glazing-requirements.html"),
("Monolithic Glass","glass-types",
 "A single, solid lite of glass with no interlayer and no insulating cavity — as opposed to laminated or insulating units. Monolithic glass may be annealed, heat-strengthened, or tempered, and is used where impact, energy, or acoustic performance is not required, such as some interior partitions or non-rated openings. Most exterior commercial Florida glazing uses laminated or insulating assemblies instead.",
 "glass thickness pros and cons","../blog/glass-thickness-commercial-pros-cons.html"),
# ---- PERFORMANCE ----
("SHGC (Solar Heat Gain Coefficient)","performance",
 "The fraction of solar radiation admitted through a glazing assembly, expressed from 0 to 1 — the lower the number, the less solar heat enters the building. SHGC is a primary lever for meeting Florida's energy code, where cooling load dominates. Low-E coatings and tinting drive SHGC down, and product approvals list the certified value for each glazing make-up.",
 "energy-efficient glass options","../blog/energy-efficient-glass-options-florida-businesses.html"),
("U-Value (U-Factor)","performance",
 "The rate of non-solar heat transfer through a glazing assembly, expressed as Btu/hr\u00B7ft\u00B2\u00B7\u00B0F — a lower U-value means better insulation. It is the inverse of R-value. In a cooling-dominated climate like Florida, U-value matters most overnight and on the conditioned side; insulating units, warm-edge spacers, and thermally broken frames all lower it. Code prescribes maximum U-values by climate zone.",
 None,None),
("VLT (Visible Light Transmittance)","performance",
 "The percentage of visible light that passes through a glazing assembly, from 0 to 100. High VLT brings daylight and views; low VLT reduces glare and, often, solar gain. Tints and coatings trade VLT against SHGC, and the design goal is usually to keep daylight high while pushing solar heat low — a balance spelled out in the glass make-up on the submittal.",
 "how tinting affects performance","../blog/how-tinting-affects-commercial-glass-performance.html"),
("STC (Sound Transmission Class)","performance",
 "A single-number rating of how well a glazing assembly blocks airborne sound — the higher the STC, the more noise it stops. Laminated glass, thicker lites, and wider air gaps raise STC, which matters for hospitality, healthcare, and offices near traffic or flight paths. ACG specifies acoustic laminated make-ups where the project calls for noise control.",
 "noise-reducing glass","../blog/noise-reducing-glass-florida-businesses.html"),
("Design Pressure (DP)","performance",
 "The structural wind load a glazing system is tested and rated to withstand, expressed in pounds per square foot (psf), with positive (inward) and negative (outward) values. Design pressure is derived from the building's wind-load calculations and exposure, and every product approval lists the DP a system carries. Matching the system DP to the project's required pressure is a core part of glazing review.",
 "wind pressure calculator","../tools/wind-pressure-calculator/"),
# ---- FRAME MATERIALS ----
("Aluminum Extrusion","frame",
 "Aluminum alloy pushed through a shaped die to form the mullions, sills, and framing profiles of storefront, curtain wall, and window systems. Extrusions can be cut, machined, and finished (anodized or painted) to a project's needs, and their cross-section determines a frame's strength, thermal behavior, and glazing detail. Nearly all commercial aluminum glazing framing starts as an extrusion.",
 None,None),
("Thermally Broken Frame","frame",
 "An aluminum frame split into interior and exterior halves joined by a low-conductivity insulating barrier, so heat does not travel straight through the metal. Thermal breaks raise the assembly's insulating performance, lower condensation risk, and help frames meet energy code. They are standard on conditioned commercial openings where the unbroken aluminum would otherwise be a thermal short-circuit.",
 "aluminum vs vinyl windows","../blog/aluminum-vs-vinyl-windows-commercial-florida.html"),
("Polyamide Thermal Break","frame",
 "A specific type of thermal break that uses glass-reinforced polyamide (nylon) strips mechanically locked into the inner and outer aluminum profiles. The polyamide strips carry structural load while insulating the two halves, giving a stronger, more durable break than poured-and-debridged urethane in many systems. Polyamide breaks are common in higher-performance commercial framing.",
 None,None),
("Structural Mullion","frame",
 "The vertical (or horizontal) framing member in a curtain wall or storefront that carries wind and dead loads back to the structure and supports the glass infill. Mullion depth and wall thickness are sized to the span and design pressure; deeper mullions resist higher loads. The mullion grid sets the visual rhythm of a facade and is the backbone of the system's structural engineering.",
 None,None),
# ---- HARDWARE ----
("Panic Device (Exit Device)","hardware",
 "Door hardware that unlatches under pressure on a horizontal push bar, allowing fast egress without a knob or key — required by code on many exit doors in assembly, educational, and high-occupancy spaces. Panic and fire-exit hardware must be listed for the application, and on rated openings it must be fire-rated. ACG coordinates exit devices through its Allegion partnership.",
 "Allegion installer","../allegion-installer-florida.html"),
("Automatic Operator","hardware",
 "A powered mechanism that opens a door on a sensor or push-plate signal, used at accessible and high-traffic entrances. Operators must be tuned for opening force, speed, and hold-open time to meet ADA and ANSI/BHMA standards, and they integrate with the door, hardware, and any security or access control. ACG installs automatic entrance systems on commercial buildings.",
 "automatic entrance systems","../automatic-entrance-systems.html"),
("ADA Threshold","hardware",
 "The floor transition at a doorway, limited by the Americans with Disabilities Act to a maximum height (generally \u00BD inch, beveled) so wheelchairs and walkers can pass without a barrier. Compliant thresholds balance accessibility against weather-sealing on exterior doors. Getting the threshold, hardware reach, and opening force right together is central to an ADA-compliant commercial entrance.",
 "ADA compliance for glass doors","../blog/ada-compliance-commercial-glass-doors.html"),
("Mortise Lock","hardware",
 "A heavy-duty lock body recessed into a pocket (mortise) machined into the door edge, as opposed to a surface-mounted or cylindrical lock. Mortise locks are durable and accept a wide range of functions and trim, which makes them the standard for commercial entrances. They must be coordinated with door prep, hardware function, and any fire or access-control requirements.",
 None,None),
("Continuous Hinge","hardware",
 "A geared or pin-and-barrel hinge that runs the full height of the door, distributing load along the entire edge instead of at two or three points. Continuous (or \u201Cgeared\u201D) hinges extend the service life of high-traffic commercial doors and resist sagging on heavy glass or aluminum leaves. They are common on storefront and entrance doors that cycle thousands of times.",
 None,None),
# ---- STANDARDS & CODES ----
("ASTM E1996","standards",
 "The standard specification that defines the impact and cyclic-pressure performance criteria a glazing assembly must meet in windborne-debris regions, including missile size and design-pressure cycling. It works in tandem with ASTM E1886 (the test method). Florida hurricane glazing approvals reference E1996 to establish whether a product qualifies for small-missile or large-missile zones.",
 "HVHZ glazing requirements","../hvhz-glazing-requirements.html"),
("ASTM E1886","standards",
 "The standard test method for impact and cyclic pressure of fenestration, doors, and shutters in hurricane regions. E1886 describes how a missile is fired at the specimen and how the assembly is then cycled through positive and negative pressures, while ASTM E1996 sets the pass/fail criteria. Together they form the basis of Florida and Miami-Dade impact approvals.",
 "what are impact windows","../blog/what-are-impact-windows-commercial-guide.html"),
("TAS 201 / 202 / 203","standards",
 "The Miami-Dade Testing Application Standards for High-Velocity Hurricane Zones. TAS 201 is the large-missile impact test, TAS 202 is uniform static air-pressure (structural) testing, and TAS 203 is cyclic wind-pressure loading. A product earns a Miami-Dade Notice of Acceptance for HVHZ use only after passing the applicable TAS protocols. ACG specifies HVHZ-rated systems for South Florida jurisdictions.",
 "Florida HVHZ requirements","../florida-hvhz-glazing-requirements.html"),
("NFPA 252","standards",
 "The standard fire test for door assemblies, measuring how long a door system resists fire and, where required, hose-stream impact. Fire-rated glass doors are tested to NFPA 252 (or UL 10C) to earn a rating in minutes. The result governs where a given fire-rated door assembly may be used in an opening within a rated wall.",
 "fire-rated glass requirements","../blog/fire-rated-glass-requirements-commercial-buildings.html"),
("NFPA 257","standards",
 "The standard fire test for window assemblies and glass-block, including a hose-stream test, used to rate fire-protective glazing in window openings. NFPA 257 ratings establish how long a glazed window assembly resists fire passage. Along with NFPA 252 for doors, it is one of the protocols that determine where fire-rated glazing can legally be installed.",
 "fire-rated glass systems","../fire-rated-glass-systems.html"),
("UL 9","standards",
 "Underwriters Laboratories' fire test standard for window assemblies, the UL counterpart used to rate fire-protective glazing in window openings. A UL 9 listing tells the AHJ that a window assembly was tested to a recognized protocol and carries a specific fire rating. It is often referenced alongside NFPA 257 in fire-rated glazing submittals.",
 None,None),
("UL 10C","standards",
 "Underwriters Laboratories' positive-pressure fire test for door assemblies, widely adopted because positive-pressure testing better reflects real fire conditions than older neutral-pressure methods. A UL 10C (or NFPA 252) listing establishes a fire-rated door's rating in minutes. Fire-rated glass doors carry the rating only as part of the listed, complete assembly — frame, glass, and hardware together.",
 "fire-rated glass code compliance","../blog/fire-rated-glass-code-compliance.html"),
("ASCE 7-22","standards",
 "The American Society of Civil Engineers' minimum design loads standard, 2022 edition, which provides the wind-load methodology referenced by current building codes. ASCE 7 defines wind speeds, exposure categories, and the calculations that produce a project's required design pressures. Those pressures are what a glazing system's tested DP rating must meet or exceed.",
 "wind pressure calculator","../tools/wind-pressure-calculator/"),
("Florida Building Code (FBC)","standards",
 "The single statewide construction code adopted and updated on a multi-year cycle that governs commercial glazing across Florida, including structural wind loads, energy, and product-approval requirements. Local jurisdictions enforce the FBC as the Authority Having Jurisdiction and may add amendments. Every ACG scope is engineered to the FBC edition in force for the project's permit.",
 "Florida Building Code guide","../blog/florida-building-code-commercial-glazing-guide.html"),
("FBC HVHZ","standards",
 "The High-Velocity Hurricane Zone provisions of the Florida Building Code, which apply in Miami-Dade and Broward counties and impose the strictest impact, pressure, and product-approval requirements in the state. In HVHZ jurisdictions, glazing must carry a Miami-Dade Notice of Acceptance and pass the TAS protocols. ACG holds the licensing and product experience to deliver HVHZ-compliant glazing.",
 "Miami-Dade glazing guide","../blog/commercial-glazing-miami-dade-guide.html"),
("NOA (Notice of Acceptance)","standards",
 "A Miami-Dade County product approval document certifying that a building product passed the High-Velocity Hurricane Zone test protocols (the TAS standards) and may be used in HVHZ jurisdictions. An NOA lists the tested configurations, design pressures, and installation limitations. ACG specifies only glazing backed by a current, valid NOA when working in HVHZ counties.",
 "what is a product approval","../blog/what-is-a-product-approval-florida.html"),
("Miami-Dade Product Approval","standards",
 "The county-level approval program, anchored by the Notice of Acceptance, that governs which building products may be installed in Miami-Dade's High-Velocity Hurricane Zone. Many jurisdictions outside the HVHZ also accept Miami-Dade approvals as evidence of impact performance. It is the most stringent product-approval pathway in Florida and a benchmark for hurricane-rated glazing.",
 "HVHZ certified contractor","../blog/hvhz-certified-glazing-contractor-florida.html"),
("FL Product Approval (FPA)","standards",
 "The statewide Florida Product Approval system administered by the Florida Building Commission, which validates that a fenestration product meets FBC structural and impact requirements outside the HVHZ. An FPA number lets a product be used across most of Florida. Submittals list the FPA (or NOA in HVHZ counties) for every glazing assembly so reviewers can verify compliance.",
 "Florida product approval guide","../blog/florida-product-approval-glazing-guide.html"),
# ---- FIRE-RATED ----
("20-Minute Fire Rating","fire",
 "The lowest common fire rating for an opening protective, used where the code requires a limited level of fire resistance — often in corridor walls and certain smoke partitions. A 20-minute fire-rated door or glazing assembly resists fire passage for that interval under the listed test. The rating applies to the complete assembly, not the glass alone.",
 "fire-rated glass requirements Florida","../blog/fire-rated-glass-requirements-florida.html"),
("45-Minute Fire Rating","fire",
 "A fire-resistance rating commonly required for opening protectives in one-hour-rated interior walls and partitions. A 45-minute fire-rated glazing assembly is tested to resist fire for that duration; where larger glazed areas are needed, fire-protective products may give way to fire-resistive (wall-rated) glazing. ACG coordinates rated assemblies through Technical Glass Products.",
 "fire-rated glass systems","../fire-rated-glass-systems.html"),
("60-Minute Fire Rating","fire",
 "A one-hour fire rating for opening protectives, typical in one- and two-hour rated wall conditions. At 60 minutes, glass area limits tighten under fire-protective listings, and many projects move to fire-resistive ceramic or specialty glazing that blocks radiant heat. The required rating comes from the wall it protects and the building's occupancy and construction type.",
 None,None),
("90-Minute Fire Rating","fire",
 "A 90-minute fire rating is required for opening protectives in many two-hour-rated walls, such as certain stair and exit enclosures. At this level, glazing is usually fire-resistive — tested to block both flame and radiant heat transfer — rather than merely fire-protective. ACG specifies listed assemblies that match the wall rating and the code's glazing-area limits.",
 "fire-rated glass code compliance","../blog/fire-rated-glass-code-compliance.html"),
("Intumescent Glazing","fire",
 "Fire-resistive glass that contains clear interlayers which foam and turn opaque when heated, blocking both flame and radiant heat so the assembly can earn higher fire ratings and larger glazed areas. Intumescent products are used where occupants need protection from heat — not just flame — such as stair enclosures and high-rated walls. They are heavier and thicker than basic fire-protective glass.",
 None,None),
("Ceramic Glass (Fire-Rated)","fire",
 "A transparent fire-rated material made from glass-ceramic that withstands extreme thermal shock and high temperatures without breaking, used as fire-protective glazing in doors, sidelites, and windows. Ceramic glazing can carry ratings up to and beyond 90 minutes and is often filmed or laminated to meet impact-safety requirements. ACG sources fire-rated ceramic glazing through Technical Glass Products.",
 "fire-rated glass systems","../fire-rated-glass-systems.html"),
# ---- HURRICANE & IMPACT ----
("HVHZ (High-Velocity Hurricane Zone)","hurricane",
 "The Florida Building Code designation for Miami-Dade and Broward counties, where the strictest wind and windborne-debris requirements apply. Glazing in the HVHZ must carry a Miami-Dade Notice of Acceptance and pass the TAS impact and pressure protocols. The HVHZ sets the highest bar for hurricane glazing in the United States, and ACG is licensed and experienced for it.",
 "HVHZ glazing requirements","../hvhz-glazing-requirements.html"),
("Small Missile Impact","hurricane",
 "An impact-test category for windborne debris in regions above 30 feet or away from the most severe zones, where the test missile is a payload of small steel balls fired at the glazing. Passing small-missile testing qualifies a product for those areas. The other, more demanding category is large-missile impact, used at lower elevations near the ground.",
 "impact rated glass requirements","../blog/impact-rated-glass-requirements-florida-2026.html"),
("Large Missile Impact","hurricane",
 "The most demanding windborne-debris test category, in which a roughly nine-pound 2x4 timber is fired at the glazing at high speed to simulate flying debris near grade in a hurricane. Large-missile-rated laminated assemblies are required at lower building elevations in impact zones. A product earns the rating through ASTM E1886/E1996 or the Miami-Dade TAS 201 protocol.",
 "hurricane impact windows guide","../blog/hurricane-impact-windows-complete-guide-commercial-florida.html"),
("Design Pressure (DP) Rating","hurricane",
 "The positive and negative wind-load rating, in pounds per square foot, that a hurricane glazing system is tested to withstand. The required DP comes from the project's ASCE 7 wind-load calculation and exposure; the installed system's tested DP must meet or exceed it. In Florida, DP and impact rating together determine whether a product is approved for a given opening.",
 "impact windows and doors","../impact-windows-doors.html"),
("Impact-Resistant Glazing","hurricane",
 "A complete glazing assembly — laminated glass in a tested frame — engineered to resist penetration from windborne debris and to keep the building envelope sealed during a hurricane. Impact glazing replaces shutters with permanent protection and is required throughout Florida's windborne-debris regions. ACG supplies and installs impact-resistant systems from ESWindows, PGT, and other approved partners.",
 "impact vs hurricane shutters","../blog/impact-windows-vs-hurricane-shutters.html"),
# ---- PROCESS ----
("Shop Drawing","process",
 "Detailed fabrication and installation drawings the glazing subcontractor produces from the architect's design documents, showing exact dimensions, sections, anchorage, and glass make-ups for the specific project. Shop drawings are submitted for the architect's and engineer's review before fabrication begins. They translate the design intent into buildable detail and are the basis for ordering material.",
 "submittal process guide","../blog/commercial-glazing-submittal-process-guide.html"),
("RFI (Request for Information)","process",
 "A formal written question from the subcontractor or contractor to the design team asking for clarification, missing information, or a decision on a field condition. RFIs are tracked, numbered, and answered in writing so the project record is clear. ACG runs RFIs through Procore and targets fast turnaround so glazing scope never stalls the schedule.",
 "project delays and how to avoid","../blog/commercial-glazing-project-delays-how-to-avoid.html"),
("Submittal","process",
 "The package of product data, samples, shop drawings, and calculations the subcontractor sends to the design team for review and approval before fabrication and installation. Glazing submittals include product approvals (NOA/FPA), structural calcs, glass make-ups, and finish samples. An organized, complete submittal is one of the fastest ways to keep a glazing scope on schedule.",
 "submittal package guide","../glazing-submittal-package.html"),
("Value Engineering","process",
 "The structured process of finding lower-cost or faster ways to meet the project's performance and design requirements without sacrificing what the building actually needs — for glazing, that might mean an alternative system, frame depth, or glass make-up. ACG approaches value engineering on the merits of speed, reliability, and code compliance rather than simply cutting specification.",
 None,None),
("Mockup","process",
 "A full-scale sample of a glazing assembly built before mass fabrication to verify appearance, fit, and performance — sometimes a visual mockup on site and sometimes a performance mockup sent for water and structural testing. Mockups catch detailing and coordination issues early, when they cost little to fix, and set the quality benchmark for the production installation.",
 None,None),
("Punch List","process",
 "The list of remaining items — adjustments, touch-ups, missing pieces, or corrections — that a contractor must complete before a project area is accepted as substantially complete. A short, fast-closing glazing punch list is a sign of disciplined installation. ACG's field discipline and first-pass inspection focus are aimed at keeping punch lists minimal.",
 "how to know a glazier did quality work","../blog/how-to-know-glazier-did-quality-work.html"),
("Commissioning","process",
 "The systematic verification that installed building systems perform as designed before turnover. For the envelope, this can include water-infiltration testing of glazing assemblies and confirmation that operable systems, hardware, and operators work to specification. Commissioning gives the owner documented proof the installed glazing meets the project's performance requirements.",
 None,None),
("AAMA Testing","process",
 "Performance testing of fenestration to standards historically published by the American Architectural Manufacturers Association (now the Fenestration and Glazing Industry Alliance), covering air infiltration, water penetration, and structural load. AAMA/FGIA test results document a window or wall system's rated performance and frequently appear in glazing submittals as evidence the product meets project requirements.",
 None,None),
# ---- CONTRACT ----
("Division 08","contract",
 "The section of the CSI MasterFormat construction specifications that covers openings — doors, windows, storefronts, curtain wall, glazing, hardware, and louvers. When a project refers to the \u201CDivision 08 scope,\u201D it means the glazing and openings package. ACG is a commercial-only Division 08 subcontractor, bidding and self-performing the openings scope for general contractors.",
 "what is Division 08","../blog/what-is-division-08-construction.html"),
("AIA G702 / G703","contract",
 "The standard American Institute of Architects payment forms. G702 is the Application and Certificate for Payment — the cover sheet summarizing the amount due — and G703 is the Continuation Sheet that breaks the contract into a schedule of values line by line. Subcontractors bill progress against these forms, and they govern how draws, stored materials, and retainage are tracked.",
 None,None),
("Retainage","contract",
 "A percentage of each progress payment (commonly 5\u201310%) the owner or general contractor withholds until the work is substantially or finally complete, as security that the job will be finished and corrected. Retainage is released at agreed milestones. For subcontractors, managing retainage is a real cash-flow factor on long projects and is tracked through the G702/G703 billing.",
 None,None),
("Notice to Owner (NTO)","contract",
 "A statutory notice a subcontractor or supplier sends early in a Florida project to preserve its right to file a construction lien if it is not paid. Serving a timely Notice to Owner is a prerequisite to lien rights for parties not in direct contract with the owner. It is a routine, protective step in Florida construction administration.",
 None,None),
("Lien Rights","contract",
 "The legal right of a contractor, subcontractor, or supplier to file a claim against the improved property to secure payment for labor or materials furnished. In Florida, lien rights are governed by the Construction Lien Law and depend on steps such as the Notice to Owner and strict deadlines. They are a core payment-protection mechanism in commercial construction.",
 None,None),
("Change Order","contract",
 "A written, signed modification to the contract that adjusts the scope, price, or schedule — issued when conditions, design, or owner requests differ from the original agreement. Documented change orders keep added glazing work properly priced and authorized before it proceeds. Clear change-order discipline protects both the contractor and the owner from disputes at closeout.",
 None,None),
]

cat_label = {
 "systems":"Systems","glass-types":"Glass Types","performance":"Glass Performance",
 "frame":"Frame Materials","hardware":"Hardware","standards":"Standards & Codes",
 "fire":"Fire-Rated Glass","hurricane":"Hurricane & Impact","process":"Process","contract":"Contract",
}
order = ["systems","glass-types","performance","frame","hardware","standards","fire","hurricane","process","contract"]

# Build HTML
parts=[]
for cat in order:
    parts.append('        <h2 class="gl-cat" data-cat="%s">%s</h2>' % (cat, cat_label[cat]))
    for term,c,defn,ltext,lhref in T:
        if c!=cat: continue
        body=defn
        if ltext and lhref:
            body = defn + ' See ACG\u2019s <a href="%s">%s</a>.' % (lhref, ltext)
        parts.append('        <div class="gl-term" data-cat="%s"><h3>%s<span class="gl-tag">%s</span></h3><p>%s</p></div>' % (c, term, cat_label[c], body))
html_frag="\n".join(parts)

# Build DefinedTermSet JSON-LD
defined=[]
for term,c,defn,ltext,lhref in T:
    # strip the trailing "See ACG's ..." sentence from schema desc; use base defn only
    desc = defn
    defined.append({
        "@type":"DefinedTerm",
        "name":term,
        "description":desc,
        "inDefinedTermSet":"https://acglass.com/glossary/"
    })
termset={
    "@context":"https://schema.org",
    "@type":"DefinedTermSet",
    "@id":"https://acglass.com/glossary/#termset",
    "name":"Commercial Glazing & Division 08 Glossary",
    "url":"https://acglass.com/glossary/",
    "publisher":{"@id":"https://acglass.com/#organization"},
    "hasDefinedTerm":defined
}
jsonld='<script type="application/ld+json">\n'+json.dumps(termset, indent=2, ensure_ascii=False)+'\n</script>'

# word count of definitions
words=sum(len(d.split()) for _,_,d,_,_ in T)
print("TERMS:",len(T))
print("DEF WORDS:",words)
open("/home/user/workspace/glossary_frag.html","w").write(html_frag)
open("/home/user/workspace/glossary_jsonld.html","w").write(jsonld)
