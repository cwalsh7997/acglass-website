#!/usr/bin/env python3
"""Wave 2 AIO-bait FAQ pages — next batch of high-search questions for Florida commercial glazing.
8 new pages with full FAQPage + Article schema."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_sprint import build_aio, AIO_PAGES

WAVE2 = [
    {
        "slug": "curtain-wall-cost-florida",
        "title": "How Much Does Curtain Wall Cost in Florida? (2026 Per Sq Ft)",
        "description": "Florida curtain wall costs $95 to $240 per square foot installed in 2026. ACG breaks down stick-built vs unitized, glass type, finish, and what drives the price spread.",
        "h1": "How Much Does Curtain Wall Cost in Florida?",
        "summary": "Curtain wall in Florida costs $95 to $240 per square foot installed in 2026. Stick-built curtain wall is the lower end ($95-$175/SF). Unitized curtain wall — fabricated in panels off-site — is the upper end ($135-$240/SF). HVHZ-rated, structural silicone, or custom-frit assemblies push past $260/SF.",
        "sections": [
            ("What's included in the curtain wall cost number", "Aluminum mullions and rails (4-8 inch face dimensions), structural anchors at slab edges, insulated glass infill, spandrel glass at slab lines, weep and pressure-equalization system, sealants, shop drawings, structural engineering, and field installation including crane time for unitized assemblies. Excludes building permit, slab edge tolerance correction, and architectural feature back-up structure."),
            ("Stick-built vs unitized: when each makes sense", "Stick-built curtain wall is assembled member-by-member on-site. It's cheaper, easier to fix at install, and works on small-to-medium projects (under 8 stories typically). Unitized curtain wall is prefabricated in panels at a fabrication shop and hoisted into place by crane. Costs more but installs faster (one panel covers an entire floor bay), gives better weather-tightness, and is the standard above 8 stories."),
            ("The five biggest cost drivers", "1) HVHZ rating — Miami-Dade NOA assemblies add 20-35%. 2) Glass spec — clear vision low-E vs. ceramic-frit vs. structural-silicone laminated impact, each is a step-change. 3) Mullion depth — 4\" face profile is base, 8\" face for high-wind exposure adds significantly. 4) Finish — class I anodize is the baseline, PVDF paint is +15-25%, custom anodize is +30-50%. 5) Project height — slab-edge access, crane requirements, and rigging add cost above 8 stories."),
            ("Typical real-world Florida curtain wall projects", "5-story office, 12,000 SF curtain wall, stick-built, clear low-E IG, anodized: $1.4M-$2.1M complete. 12-story hotel, 30,000 SF curtain wall, unitized, laminated impact IG (HVHZ), PVDF finish: $5.5M-$7.2M complete. 3-story medical office, 8,000 SF curtain wall, stick-built, frit glass + clear IG: $920K-$1.4M complete."),
            ("How to compress curtain wall cost without value-engineering away performance", "Choose stick-built where feasible — saves 15-25% over unitized. Use stock mullion sections rather than custom extrusions. Limit color count to 1-2 in the same building. Lock the design package before shop drawings — re-engineering after pricing is the #1 cost overrun. Issue full architectural drawings, not narratives — narrative-bid pricing carries 15-25% contingency.")
        ],
        "faqs": [
            ("How much does curtain wall cost in Florida in 2026?", "Florida curtain wall costs $95 to $240 per square foot installed in 2026. Stick-built is $95-$175/SF. Unitized is $135-$240/SF. HVHZ rating, premium glass, and custom finishes push individual projects above $260/SF."),
            ("Is curtain wall cheaper than storefront?", "No — curtain wall is significantly more expensive per square foot than storefront. Curtain wall is engineered to span multiple floors and resist higher wind loads, with deeper mullions, more anchor engineering, and larger shop drawings. Storefront is single-story and substantially less complex."),
            ("Which is better, stick-built or unitized curtain wall?", "Stick-built is cheaper, simpler, and works for projects under 8 stories or with simple geometry. Unitized is faster to install (saving schedule), more weather-tight, and is the standard for high-rise. The right choice depends on project size, schedule, and budget."),
            ("Do curtain wall costs include the glass?", "Yes — curtain wall pricing typically includes the insulated glass unit infill. Glass spec (clear, low-E, laminated, frit, ceramic-coated, structural silicone) significantly affects the total."),
            ("Can curtain wall be value-engineered?", "Yes, but most value-engineering on curtain wall hurts performance: thinner mullions reduce wind capacity, cheaper glass reduces solar performance, single-source manufacturer products lose owner negotiating leverage. Better to optimize the design package upfront than VE after pricing.")
        ]
    },
    {
        "slug": "structural-silicone-glazing-explained",
        "title": "Structural Silicone Glazing Explained (Cost, Code, Use Cases)",
        "description": "Structural silicone glazing bonds glass to aluminum framing with high-performance silicone — no exterior cap. ACG explains where it makes sense and where it doesn't.",
        "h1": "Structural Silicone Glazing Explained",
        "summary": "Structural silicone glazing (SSG) is a curtain wall or storefront technique where glass is bonded directly to the aluminum framing with high-performance structural silicone — eliminating the exterior aluminum cap and producing a flush, all-glass exterior appearance. SSG is used on Class-A office, luxury hotel, and architecturally-driven commercial projects. It costs 20-40% more than traditional pressure-equalized glazing and requires factory-bonded units for HVHZ jurisdictions.",
        "sections": [
            ("What structural silicone actually does", "In traditional curtain wall, glass is held to the framing by an exterior aluminum pressure plate or cap. The cap creates a visible aluminum grid on the building exterior. Structural silicone replaces the cap with high-strength silicone adhesive — the glass is bonded directly to the aluminum mullion. The result: a flush all-glass exterior with no visible aluminum cap, only the visible grid of where mullions are behind the glass."),
            ("Two- vs four-sided SSG", "Two-sided SSG keeps aluminum caps on the horizontal joints and uses silicone on the vertical joints (or vice versa). Four-sided SSG uses silicone on all four edges of the glass lite. Four-sided is the higher-performance, more dramatic appearance — and the more expensive."),
            ("HVHZ and SSG: factory-bonded units required", "Miami-Dade and HVHZ jurisdictions require structural silicone joints to be factory-bonded — the glass and aluminum sub-frame are bonded in a controlled fabrication environment, not on-site. The bonded assembly then ships to site and installs as a single panel. This is more expensive than stick-built SSG but ensures consistent silicone cure quality."),
            ("Cost premium for SSG", "Structural silicone glazing typically costs 20-40% more than traditional pressure-equalized curtain wall on the same project. The premium covers: higher-grade silicone material (Dow 995 or equivalent), engineering certification of the bond, factory bonding labor for HVHZ work, and longer shop drawing timelines."),
            ("When SSG is the right call", "Class-A office where the architect specified a flush all-glass exterior. Luxury hotel where finish matters. Award-targeting architectural projects (AIA awards, USGBC LEED Platinum). High-end mixed-use where ground-floor commercial wants a continuous glass look. Skip SSG on basic commercial, retail TI, restaurant TI, and budget-driven projects.")
        ],
        "faqs": [
            ("What is structural silicone glazing?", "Structural silicone glazing (SSG) is a curtain wall technique where glass is bonded to aluminum framing with high-performance silicone adhesive instead of an exterior aluminum pressure cap. It produces a flush, all-glass exterior appearance."),
            ("Is structural silicone glazing allowed in HVHZ?", "Yes, with one major caveat: HVHZ jurisdictions (Miami-Dade, Broward, parts of Palm Beach) require structural silicone joints to be factory-bonded, not field-bonded. The bonded panels then install on-site as pre-assembled units."),
            ("How much does structural silicone glazing cost?", "Structural silicone glazing typically costs 20-40% more than traditional pressure-equalized curtain wall on the same project. The premium covers higher-grade silicone, engineering certification, and factory bonding labor."),
            ("Is structural silicone glazing reliable long-term?", "Yes, when properly designed and installed with documented silicone products (Dow 995 or equivalent) and qualified installation. The technique has been used on commercial buildings since the 1970s with documented long-term performance."),
            ("When should I NOT use structural silicone glazing?", "Skip SSG on basic retail TI, restaurant TI, budget commercial, and projects where the architect did not specifically request the flush all-glass appearance. The cost premium is hard to justify on standard commercial work.")
        ]
    },
    {
        "slug": "what-is-spandrel-glass",
        "title": "What Is Spandrel Glass? (Where It's Used, How It Differs from Vision Glass)",
        "description": "Spandrel glass is opaque glass installed at slab lines in curtain wall to conceal interior structure. ACG explains shadow box vs ceramic frit and where each is used.",
        "h1": "What Is Spandrel Glass?",
        "summary": "Spandrel glass is opaque architectural glass installed in curtain walls and window walls at slab lines, between floor levels, to conceal interior structure (slab edges, ceiling cavities, mechanical chases) from the building exterior. It comes in two main types: ceramic-frit spandrel (color baked onto the back surface of glass) and shadow box spandrel (a vision lite with an opaque panel behind it).",
        "sections": [
            ("Where spandrel glass is used in a building", "In a multi-story curtain wall, the vision area of each floor (where occupants look out) is separated from the next floor's vision area by a spandrel zone. The spandrel zone covers the slab edge, perimeter mechanical, ceiling cavity, and any architectural feature you don't want visible from the building exterior. Typical spandrel zone height: 24-48 inches."),
            ("Ceramic-frit spandrel — the standard solution", "Ceramic-frit spandrel is a single lite of glass with opaque ceramic ink fired onto the back (interior-facing) surface. The frit pattern is typically solid (100% coverage) on spandrel — though dot-pattern and gradient frit are used for special applications. Frit colors are typically warm-neutral, dark-neutral, or color-matched to the architectural design intent."),
            ("Shadow box spandrel — the deeper appearance", "Shadow box spandrel uses a vision lite (clear or low-E) with an opaque insulated panel (typically painted aluminum or color-matched material) installed behind the glass at a 6-12 inch setback. The result: a deeper, dimensional appearance with shadow lines visible inside the spandrel. More expensive than frit but offers a higher-end architectural look."),
            ("Heat-treatment requirements", "Spandrel glass typically must be heat-strengthened or fully tempered because the spandrel zone experiences thermal stress (sun heats the opaque back surface, glass tries to expand). Heat-strengthened is standard for most spandrel; fully tempered is required where building code specifies safety glazing or where the spandrel is at hazardous-location height."),
            ("Cost vs vision glass", "Ceramic-frit spandrel costs roughly 30-50% more than equivalent clear vision glass. Shadow box spandrel costs roughly 60-100% more. The cost driver is mostly fabrication (frit firing or panel installation) rather than glass cost itself."),
            ("Color and pattern selection", "Frit color selection is best done with physical samples in actual daylight. Computer renderings consistently misrepresent how frit colors read on the building. Get 12x12 inch field samples and view them at the actual building site at noon and at 4pm before committing to a color.")
        ],
        "faqs": [
            ("What is spandrel glass?", "Spandrel glass is opaque architectural glass installed in curtain walls and window walls at slab lines to conceal interior structure (slab edges, ceiling cavities, mechanical) from the exterior. It's used between floor levels to separate vision-glass zones."),
            ("What's the difference between spandrel and vision glass?", "Vision glass is transparent and used at floor-occupied levels for daylight and view. Spandrel glass is opaque and used at slab lines and floor-line zones to conceal the building structure. Both are part of the same curtain wall assembly."),
            ("Does spandrel glass need to be tempered?", "Spandrel glass typically must be heat-strengthened (or fully tempered) because the opaque back surface heats up in direct sun and creates thermal stress. Heat-strengthened is standard; full tempering is required in safety-glazing locations."),
            ("What's the difference between ceramic-frit and shadow box spandrel?", "Ceramic-frit spandrel uses opaque ceramic ink fired onto the back of a single glass lite. Shadow box spandrel uses a vision lite with an opaque panel installed 6-12 inches behind it, creating dimensional depth. Shadow box costs more but offers a higher-end appearance."),
            ("Can spandrel glass be specified in any color?", "Yes — ceramic-frit can be matched to virtually any architectural color, including custom RAL or Pantone-equivalent specs. Solid frit, dot-pattern, and gradient frit are all available. Always review physical samples in daylight before committing."),
        ]
    },
    {
        "slug": "ada-storefront-door-requirements-florida",
        "title": "ADA Storefront Door Requirements in Florida (2026 Compliance Guide)",
        "description": "ADA-compliant commercial storefront doors in Florida require 32-inch minimum clear width, 5-pound max opening force, level landings, and proper hardware. ACG breaks down compliance.",
        "h1": "ADA Storefront Door Requirements in Florida",
        "summary": "Florida ADA-compliant commercial storefront doors must meet five requirements per FBC Accessibility chapter (which adopts the 2010 ADA Standards): (1) minimum 32 inches clear width when door is open 90 degrees, (2) maximum 5 pounds opening force on interior doors / 8.5 pounds on exterior fire doors, (3) level landings on both sides, (4) compliant hardware (lever, panic, or auto-operator), and (5) accessible clear floor space at door approach.",
        "sections": [
            ("The 32-inch clear width rule", "ADA requires 32 inches minimum clear width when the door is open 90 degrees. This is measured from the door face (when open) to the opposite stop or jamb. Standard 36-inch wide doors easily meet this; 32-inch wide doors do not (you lose 1.5-2 inches to door thickness at 90 degrees). For pairs of doors, one leaf must independently provide 32 inches clear width."),
            ("The 5-pound opening force rule", "Interior doors must require 5 pounds or less to open. Exterior doors are not directly regulated by ADA on opening force, but most Florida AHJs apply the same standard to exterior storefront entries. This is achieved with proper closer adjustment, low-resistance hardware, and (where needed) automatic operators."),
            ("Level landing requirement", "Both sides of the door must have a level landing — typically 60 inches deep on the swing side and 48 inches on the pull side. Maximum slope: 1:48. This is where many Florida storefronts fail at substantial completion — the sidewalk has settled and the landing is no longer level. Coordinate with the GC on subgrade prep BEFORE concrete pour."),
            ("Hardware compliance", "Door hardware must be operable with one hand without tight grasping or twisting. Lever handles, panic hardware, push-pull paddle, and auto-operators all comply. Round knobs do NOT comply. Push-button auto-operators must be located 36-48 inches above the floor, 60 inches from the door swing arc."),
            ("Vestibule and pair-door considerations", "Vestibules require both sets of doors to comply independently. If automated operators are used, both interior and exterior doors must have operators with synchronized activation. Pair doors (two doors hinged together) must have one leaf independently provide 32 inches clear width — typically the active leaf."),
            ("Common ADA violations on Florida storefronts", "1) Door swing landing not level due to sidewalk settlement. 2) Closer adjustment too tight (>5 lb force). 3) Wrong hardware (knobs instead of levers). 4) Auto-operator activation button outside reach range. 5) Vestibule clear floor space inadequate. 6) Threshold height exceeds 1/2 inch.")
        ],
        "faqs": [
            ("What are ADA requirements for storefront doors in Florida?", "ADA requires storefront doors in Florida to have 32-inch minimum clear width, 5-pound maximum opening force on interior doors, level landings on both sides, accessible hardware (lever, panic, or auto-operator), and adequate clear floor space."),
            ("Do all commercial storefront doors in Florida need ADA compliance?", "All primary entrances and all required-egress doors must comply. Service entries used only by employees may have reduced requirements. Existing buildings undergoing alterations trigger ADA compliance on the altered portions."),
            ("What hardware is ADA-compliant for storefront doors?", "Lever handles, panic hardware, push-pull paddles, and automatic operators all comply. Round knobs do not comply. All compliant hardware must be operable with one hand without tight grasping or twisting."),
            ("How do I know if my storefront landing is ADA-compliant?", "Use a 4-foot level on both sides of the door, in both directions. Slope cannot exceed 1:48 (about 1/4 inch per foot). The landing must be at least 60 inches deep on the swing side and 48 inches on the pull side."),
            ("Are automatic door operators required for ADA?", "Not required on most commercial storefronts, but they're often the most reliable way to meet the 5-pound opening force requirement on heavy exterior doors. Many Florida owners install auto-operators as a practical compliance solution.")
        ]
    },
    {
        "slug": "fire-rated-glazing-explained",
        "title": "Fire-Rated Glazing Explained (20, 45, 60, 90, 120 Minute Ratings)",
        "description": "Fire-rated glazing in commercial buildings comes in 20, 45, 60, 90, and 120-minute ratings. ACG explains where each is required, common products, and code compliance.",
        "h1": "Fire-Rated Glazing Explained",
        "summary": "Fire-rated glazing is glass tested to maintain integrity during a fire for a specific duration — 20, 45, 60, 90, or 120 minutes. Required at fire-rated walls, exit stairs, occupancy separations, and openings in rated assemblies. Common products: SuperLite II XL, FireLite (Pilkington), Pyrostop, and Pyran by SCHOTT. The required rating depends on the wall's fire rating per IBC and FBC.",
        "sections": [
            ("How fire-rated glazing actually works", "Fire-rated glass is engineered to survive direct flame contact and high temperatures for a specific duration. Products use different technologies: wired glass (legacy, declining use), ceramic glass (high temperature resistance), intumescent interlayer (expands when heated to block flame transmission), and tempered with gel layer (water-cooled glass technology). The rating measures both integrity (no flame passage) and, in higher ratings, insulation (limits heat transfer to the unexposed side)."),
            ("The 5 standard ratings", "20-minute: smoke and draft control doors, corridor walls. 45-minute: shaft walls, vertical exits in low-rise. 60-minute: fire barriers, exit stair enclosures in high-rise. 90-minute: occupancy separations between certain occupancy types. 120-minute: most demanding rating, typically used in high-rise exit stair enclosures and area separation walls."),
            ("Integrity-only (E rating) vs integrity-plus-insulation (EI rating)", "Integrity-only glazing prevents flame and smoke passage but allows heat to transmit through. This is acceptable for many applications. Insulation-rated glazing (EI) limits heat transfer on the unexposed side — required where occupants must use the space adjacent to the rated assembly during fire (exit stairs, vestibules)."),
            ("Common products on Florida commercial projects", "FireLite Plus (Pilkington): 20-90 min, integrity-only. SuperLite II-XL (SAFTI FIRST): 20-120 min, integrity-only and EI options. Pyrostop (Pilkington): 60-120 min, EI rating, intumescent. Pyran (SCHOTT): 20-180 min, ceramic, integrity-only. Each has different size limitations and cost."),
            ("Code requirements: what triggers fire-rated glazing", "Fire-rated walls (rated per IBC Table 716.1(2)) require fire-rated glazing in openings. Exit stair enclosures, area separation walls, occupancy separations, and corridor walls all may require rated glazing depending on the building's construction type and occupancy classification. Always verify with project code official before specification."),
            ("Cost impact", "Fire-rated glazing is significantly more expensive than standard tempered or laminated commercial glass. 20-min rated glass: 4-8x clear tempered cost. 60-min: 8-15x. 90-120 min EI: 15-30x. Limit fire-rated glazing to where actually required by code.")
        ],
        "faqs": [
            ("What is fire-rated glazing?", "Fire-rated glazing is glass tested to maintain integrity during a fire for a specific duration — typically 20, 45, 60, 90, or 120 minutes. It's required in commercial buildings at fire-rated walls, exit stair enclosures, and occupancy separations per IBC and FBC."),
            ("What ratings are commercially available?", "20, 45, 60, 90, and 120 minute ratings are commercially standard. Each has integrity-only (E rating) and integrity-plus-insulation (EI rating) variants. EI is required where heat transfer to the unexposed side must be limited."),
            ("How much does fire-rated glass cost?", "Fire-rated glazing is significantly more expensive than standard commercial glass. 20-minute rated: 4-8x clear tempered cost. 60-minute: 8-15x. 90-120 minute EI: 15-30x. Limit to where code actually requires."),
            ("Is wired glass still allowed in fire-rated assemblies?", "Wired glass is still allowed by IBC and FBC for some applications but is restricted near doors and in safety-glazing locations because it doesn't meet impact safety standards. Modern fire-rated alternatives have largely replaced wired glass on commercial work."),
            ("What's the difference between fire-rated and impact-rated glass?", "Fire-rated glazing is tested for fire resistance. Impact-rated glazing is tested for windborne debris resistance. They're different code requirements addressing different hazards. Some products meet both (fire + impact), but the testing is separate.")
        ]
    },
    {
        "slug": "commercial-glass-replacement-vs-repair",
        "title": "Commercial Glass Replacement vs Repair: Which Do You Need?",
        "description": "Should you replace or repair commercial glass? ACG explains when glass can be repaired vs when full replacement is required, cost, and insurance considerations.",
        "h1": "Commercial Glass Replacement vs Repair",
        "summary": "Most commercial glass damage requires replacement, not repair. Glass cannot be welded or patched. Chips, cracks, seal failures, and impact damage all require lite replacement. Surface scratches under 1/16 inch can sometimes be polished out; deeper scratches require replacement. Insurance typically covers vandalism, accidental breakage, and storm damage but not gradual seal failure.",
        "sections": [
            ("What can be repaired (limited list)", "Surface scratches under 1/16 inch deep: sometimes polished out with cerium oxide. Surface stains (mineral deposits, light hard water): cleaned with specialty chemicals. Hardware adjustment: closers, hinges, locks, sweeps. Sealant joint failure (wet glazing): can be re-caulked. Setting blocks: can be replaced if dropped or settled."),
            ("What requires replacement (most issues)", "Any crack or chip in the glass itself. Insulated glass unit (IGU) seal failure — moisture or fog inside the cavity. Laminated glass delamination. Impact damage (even if the glass is still in place). Tempered glass that has shattered into pieces. Frit damage or coating delamination. Frame damage that has compromised glass anchorage."),
            ("Why most glass damage requires replacement", "Glass is a brittle ceramic material — you can't weld it, you can't patch it. Cracks propagate over time and can lead to full failure. Cracked tempered glass is unsafe (it can shatter without warning). IGU seal failure cannot be repaired in the field; the unit must be replaced."),
            ("Typical replacement cost (per lite)", "Storefront vision lite (3-6 SF, clear tempered): $400-$900 installed. Storefront vision lite (impact-rated): $800-$1,800 installed. Curtain wall vision lite (medium size): $1,500-$4,000 installed. Curtain wall corner unit or oversized: $3,000-$12,000 installed. Glass railing panel: $600-$2,200 installed. Custom-frit or specialty glass: 2-4x standard cost."),
            ("Insurance: what's typically covered", "Vandalism: usually covered, deductible applies. Accidental breakage by occupants/contractors: usually covered. Storm damage: covered under the wind/hurricane portion of commercial policy. Theft/break-in damage: covered under property policy. Gradual seal failure: typically NOT covered (considered wear and tear). Building movement damage: usually NOT covered."),
            ("How to minimize replacement delays", "Document the failure immediately with photos and a written incident note. Notify the original glazier first (warranty coordination). For non-warranty replacements, get a written quote from 2-3 qualified glaziers. Order replacement glass early — fabrication can take 2-4 weeks even for stock IG. Plan temporary boarding if the opening is exposed.")
        ],
        "faqs": [
            ("Can commercial glass be repaired or does it need replacement?", "Most commercial glass damage requires replacement, not repair. Glass cannot be welded or patched. Surface scratches under 1/16 inch can sometimes be polished out, but cracks, chips, seal failures, and impact damage all require lite replacement."),
            ("How much does commercial glass replacement cost?", "Storefront vision lite (clear tempered): $400-$900 installed. Impact-rated storefront lite: $800-$1,800. Curtain wall vision lite: $1,500-$4,000. Oversized or custom-frit glass: 2-4x standard cost."),
            ("Does insurance cover commercial glass replacement?", "Insurance typically covers vandalism, accidental breakage, and storm damage. Gradual seal failure (foggy IG units) is usually NOT covered. Always check your specific commercial policy and deductible."),
            ("How long does commercial glass replacement take?", "Stock-size storefront glass: 1-3 weeks from order to installation. Insulated glass units: 2-4 weeks. Custom or impact-rated glass: 4-10 weeks. Plan temporary boarding if the opening is exposed."),
            ("Should I use the original glazier for replacement?", "Yes if the original install is under warranty — the original glazier handles warranty coordination at no charge. For out-of-warranty work, choose any qualified glazier with documented experience in your project type.")
        ]
    },
    {
        "slug": "kawneer-vs-ykk-ap-storefront",
        "title": "Kawneer vs YKK AP Storefront Systems (Side-by-Side Comparison)",
        "description": "Kawneer and YKK AP are the two most-installed commercial aluminum storefront brands in Florida. ACG compares Series 451T vs YHS 50 TU, cost, availability, and HVHZ approvals.",
        "h1": "Kawneer vs YKK AP: Aluminum Storefront Compared",
        "summary": "Kawneer (a Howmet subsidiary) and YKK AP are the two dominant aluminum commercial storefront manufacturers in Florida. Both offer comparable performance — the choice usually comes down to architect specification, distributor relationships, lead time, and finish availability. Kawneer typically has broader stock color availability; YKK AP often wins on lead time and price point.",
        "sections": [
            ("Kawneer overview", "Kawneer (a Howmet Aerospace subsidiary) is the largest commercial aluminum storefront manufacturer in North America. Florida architect specifications default to Kawneer roughly 60% of the time. Common Florida systems: Series 451T (1-3/4\" face, basic), Series 501T (2\" face, thermal break), Series 601T (2-1/4\" face), Series 701T (2-1/2\" face, heavy duty). Class I anodize and PVDF finishes broadly available."),
            ("YKK AP overview", "YKK AP USA is the U.S. arm of YKK Corporation (Japan). Strong in commercial storefront, window wall, and unitized curtain wall. Common Florida systems: YHS 50 TU (1-3/4\" face), YHS 60 TU (2-1/4\" face). Aggressive pricing and competitive lead times. Class I anodize and PVDF finishes available."),
            ("Side-by-side equivalents", "Kawneer Series 451T ≈ YKK YHS 50 TU (entry-level thermally-broken storefront). Kawneer Series 501T ≈ YKK YHS 60 TU (mid-range thermally-broken). Both manufacturers offer HVHZ-rated assemblies with Miami-Dade NOAs. Both ship from Florida warehouses for faster delivery on Florida projects."),
            ("Cost comparison", "On equivalent specs, YKK AP is typically 8-15% less expensive than Kawneer on the storefront line item. The premium for Kawneer comes from broader distribution network and stronger long-term brand recognition with architects. For most Florida commercial projects, the cost difference is decisive only on large jobs."),
            ("Lead time comparison", "YKK AP often delivers 1-2 weeks faster than Kawneer on standard stock colors. Custom anodize and custom PVDF lead times are similar (8-12 weeks). For tight schedule projects, YKK is often the safer choice."),
            ("Architect preference", "Florida architects default to Kawneer in spec because it's the longer-established Florida brand. Many specs explicitly say 'Kawneer Series 451T or approved equal.' YKK AP routinely qualifies as an approved equal on these specs.")
        ],
        "faqs": [
            ("Is Kawneer or YKK AP better for Florida commercial storefront?", "Both are excellent. Kawneer is the larger, more widely-specified brand. YKK AP is typically 8-15% less expensive and often faster on lead time. The right choice depends on project budget, schedule, and architect spec."),
            ("What's the difference between Kawneer Series 451T and YKK YHS 50 TU?", "Both are entry-level thermally-broken aluminum storefront systems with 1-3/4 inch face dimension. Performance ratings are comparable. Kawneer is more widely specified; YKK is typically less expensive and faster lead time."),
            ("Do both Kawneer and YKK have HVHZ-rated systems?", "Yes — both manufacturers offer Miami-Dade NOA-approved storefront assemblies for HVHZ work. Pre-permit submittal, verify the specific NOA is current and that the design pressure matches the project requirements."),
            ("Which has faster lead time, Kawneer or YKK?", "YKK AP typically delivers 1-2 weeks faster than Kawneer on standard stock colors. Custom finishes (anodize, PVDF) have similar 8-12 week lead times on both."),
            ("Can YKK AP qualify as 'approved equal' on a Kawneer-spec'd project?", "Yes, in most cases. Most Florida storefront specs read 'Kawneer Series X or approved equal,' and YKK AP routinely qualifies on functional equivalence. Confirm with the architect of record before substituting.")
        ]
    },
    {
        "slug": "florida-product-approval-vs-noa",
        "title": "Florida Product Approval vs Miami-Dade NOA: What's the Difference?",
        "description": "Florida Product Approval (FL #) and Miami-Dade NOA both certify glazing assemblies for Florida code compliance. ACG explains when each applies and how to use them.",
        "h1": "Florida Product Approval vs Miami-Dade NOA",
        "summary": "Florida Product Approval (FL #) and Miami-Dade Notice of Acceptance (NOA) are two parallel approval systems for commercial glazing assemblies in Florida. NOAs are issued by Miami-Dade County Product Control and required in HVHZ counties. Florida Product Approvals are issued by the Florida Department of Business and Professional Regulation (DBPR) and accepted statewide outside HVHZ. Many products carry both.",
        "sections": [
            ("How Florida Product Approval works", "Florida Product Approval is a statewide approval system administered by Florida DBPR. Manufacturers submit test data to a state-approved validation entity, which reviews and issues an FL # (e.g., FL27543-R8). The approval is valid statewide for the specific product configuration. Required for any building component used in Florida outside HVHZ counties — including doors, windows, shutters, roofing, and structural components."),
            ("How Miami-Dade NOA works", "Miami-Dade Notice of Acceptance (NOA) is issued by Miami-Dade County Product Control. NOAs reference Miami-Dade TAS 201 (large missile impact), TAS 202 (static pressure), and TAS 203 (cyclic pressure) testing — the strictest in Florida. Required in HVHZ counties (Miami-Dade, Broward, parts of Palm Beach east of Military Trail)."),
            ("When NOA is required vs FL # is sufficient", "NOA required: any commercial glazing in Miami-Dade County or Broward County. NOA required in HVHZ portion of Palm Beach (east of Military Trail). FL # is sufficient: rest of Florida — including non-HVHZ Palm Beach, Treasure Coast, Tampa Bay, Naples, and Panhandle. Many AHJs outside HVHZ will still accept Miami-Dade NOAs as the higher-strict approval."),
            ("How to verify each", "Florida Product Approval: search the Florida Building Code Online portal (floridabuilding.org/pr) by FL # or manufacturer. Miami-Dade NOA: search the Miami-Dade County Product Control Section's online NOA database. For both, confirm the expiration date is in the future."),
            ("Common mistakes that cause permit rejection", "1) Submitting an FL # when the AHJ requires an NOA (HVHZ rejection). 2) Using an expired approval. 3) Specifying components from different manufacturers that don't share a tested assembly. 4) Design pressure on drawings exceeds the approval's rated DP. 5) Wrong anchorage detail referenced. 6) Approved equal submitted without the proper substitution documentation."),
            ("Typical timeline for new approvals", "Florida Product Approval: 4-8 weeks for new approvals once test data is submitted. Miami-Dade NOA: 8-16 weeks for new approvals (more stringent review). Both must be renewed every 5 years.")
        ],
        "faqs": [
            ("What's the difference between Florida Product Approval and Miami-Dade NOA?", "Florida Product Approval (FL #) is a statewide approval issued by Florida DBPR. Miami-Dade NOA is issued by Miami-Dade County Product Control and references stricter HVHZ testing (TAS 201/202/203). Both are valid in their respective jurisdictions."),
            ("Where is a Miami-Dade NOA required?", "Miami-Dade NOAs are required in all of Miami-Dade County, all of Broward County, and the HVHZ portion of Palm Beach County (east of Military Trail). Outside these areas, Florida Product Approval is sufficient."),
            ("Can a Florida Product Approval be used in Miami-Dade?", "Generally no — Miami-Dade and other HVHZ AHJs require Miami-Dade NOAs for HVHZ-rated components. Some products carry both an FL # and an NOA, in which case the NOA is the relevant approval for HVHZ submittal."),
            ("How long are these approvals valid?", "Both Florida Product Approvals and Miami-Dade NOAs are issued for 5-year terms. Manufacturers must renew them before expiration. Always verify the current status at the relevant agency before submittal."),
            ("Where do I look up these approvals?", "Florida Product Approval: floridabuilding.org/pr (search by FL # or manufacturer). Miami-Dade NOA: Miami-Dade County Product Control NOA database (search by NOA number or manufacturer).")
        ]
    }
]

if __name__ == "__main__":
    for p in WAVE2:
        build_aio(p)
    print(f"\n{len(WAVE2)} wave 2 AIO pages built.")
