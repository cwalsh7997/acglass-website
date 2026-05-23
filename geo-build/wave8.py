#!/usr/bin/env python3
"""Wave 8: 10 more AIO FAQ + 10 vertical-city + 8 TN expansion + service-areas map + 4 blog."""
import os, json, sys, html as html_lib

OUT = "/home/user/workspace/acglass-website"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_sprint import build_aio
from wave5 import build_vc2

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">'''

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links">
<a href="/index.html">Home</a><a href="/case-studies/">Case Studies</a><a href="/tools/">Tools</a>
<a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]


def write_html(rel, html_str):
    full = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"  Wrote /{rel}")


# ============================================================
# 10 more AIO FAQ
# ============================================================

AIO6 = [
    {
        "slug": "what-is-tempered-laminated-glass",
        "title": "What Is Tempered Laminated Glass? (HVHZ Standard for Florida)",
        "description": "Tempered laminated glass combines two safety features: heat-treated tempering and laminated impact resistance. ACG explains where Florida code requires this combination.",
        "h1": "What Is Tempered Laminated Glass?",
        "summary": "Tempered laminated glass combines tempered safety glass (heat-treated for strength and safe break pattern) with laminated construction (two glass layers bonded to an interlayer). The result: maximum safety + impact resistance. Required in Florida HVHZ assemblies, glass railings, overhead glazing, and security applications.",
        "sections": [
            ("Why combine tempered AND laminated", "Tempered glass alone breaks safely (small granular pieces) but doesn't stay in place when broken. Laminated glass stays in place when broken but isn't strong enough on its own. Tempered laminated combines both: 4-5x annealed strength PLUS the laminated interlayer holding the assembly together. The standard for Florida HVHZ commercial work."),
            ("Standard tempered laminated assembly", "Typical Florida HVHZ tempered laminated lite: 1/4\" tempered glass + .090 PVB interlayer + 1/4\" tempered glass = 0.59\" nominal thickness. For higher performance: 1/4\" tempered + .090 SGP + 1/4\" tempered (SGP is 100x stiffer than PVB, used on the most demanding applications)."),
            ("Where Florida code requires tempered laminated", "HVHZ-rated openings (Miami-Dade, Broward, parts of Palm Beach east of Military Trail) require laminated assemblies. Many HVHZ NOAs specifically require tempered laminated. Glass railings require structural laminated glass (typically tempered laminated). Overhead glazing per IBC 2407 requires laminated."),
            ("Cost comparison", "Tempered alone: $25-$45/SF on 1/4\" thickness. Laminated tempered: $55-$95/SF on 1/2\" laminated thickness. Insulated tempered laminated impact (the full HVHZ commercial standard): $80-$140/SF as a complete IGU."),
            ("HVHZ approval considerations", "Each tempered laminated assembly is tested as a unit and approved via Miami-Dade NOA. You cannot substitute one manufacturer's tempered glass with another manufacturer's laminated interlayer and expect the NOA to apply. The full assembly (specific glass + specific interlayer + specific framing) must match the tested combination.")
        ],
        "faqs": [
            ("What is tempered laminated glass?", "Tempered laminated glass combines tempered safety glass (heat-treated for strength) with laminated construction (two glass layers bonded to an interlayer). Used in Florida HVHZ assemblies, glass railings, overhead glazing, and security applications."),
            ("Why is tempered laminated used in HVHZ?", "Florida HVHZ assemblies need both impact resistance (laminated holds the assembly together) AND safety break pattern (tempered breaks into safe granular pieces). Tempered laminated provides both in one product."),
            ("How thick is tempered laminated glass?", "Standard 1/4\" tempered + .090 interlayer + 1/4\" tempered = 0.59\" nominal thickness. Heavier applications use 3/8\" + .090 + 3/8\" = 0.84\". The interlayer can be PVB (standard) or SGP (premium, 100x stiffer)."),
            ("Is tempered laminated more expensive than just tempered?", "Yes \u2014 tempered laminated typically costs 2-3x more than equivalent tempered alone. The premium covers the additional glass lite, the interlayer material, and the laminated fabrication labor."),
            ("Can tempered laminated be cut or drilled?", "No. Like all tempered glass, it cannot be cut or drilled after fabrication. All openings, holes, and edge profiles must be specified before tempering.")
        ]
    },
    {
        "slug": "what-is-stick-built-curtain-wall",
        "title": "What Is Stick-Built Curtain Wall? (vs Unitized)",
        "description": "Stick-built curtain wall is assembled member-by-member on-site, vs unitized which is prefabricated in panels. ACG explains the trade-offs and when each is right.",
        "h1": "What Is Stick-Built Curtain Wall?",
        "summary": "Stick-built curtain wall is a multi-story aluminum-and-glass facade assembled member-by-member directly on the building's structure. Individual mullions are anchored to slab edges, then horizontals and glass are installed piece by piece. Distinct from unitized curtain wall, which is prefabricated in panels and craned into place. Stick-built is cheaper, more flexible, and better for projects up to 8 stories.",
        "sections": [
            ("How stick-built curtain wall is assembled", "Step 1: Anchors installed at slab edges per shop drawings. Step 2: Vertical mullions installed and anchored. Step 3: Horizontal members installed between mullions. Step 4: Spandrel panels installed at slab lines. Step 5: Vision glass installed (typically wet-glazed or pressure-equalized dry-glazed). Step 6: Sealants and weep system completed. Step 7: Final inspection and punch."),
            ("Stick-built vs unitized: when to choose each", "Stick-built: projects under 8 stories, complex geometries, budget-driven projects, jobs where field modifications are likely, smaller crew availability. Unitized: high-rise (8+ stories), tight schedules, complex assemblies (structural silicone, decorative coatings), better weather-tightness."),
            ("Cost comparison", "Stick-built curtain wall in Florida: $95-$175/SF installed. Unitized curtain wall: $135-$240/SF installed. Difference: 30-40% premium for unitized. The premium often pays back via faster schedule and tighter weather sealing."),
            ("Schedule comparison", "Stick-built install: typically 2,500-4,000 SF per crew per week (5 person crew). Unitized install: 5,000-8,000 SF per crew per week. Unitized is roughly 2x faster on the install phase, though shop fabrication is longer."),
            ("HVHZ stick-built considerations", "HVHZ stick-built curtain wall is fully approvable but requires careful field sealant application, anchorage QA, and proper weep detailing. NOAs reference complete assemblies; the field crew must maintain the tested configuration. Stick-built is more error-prone in HVHZ work \u2014 use experienced glaziers only."),
            ("When stick-built makes sense even on tall projects", "Some 10-15 story projects choose stick-built because: (1) complex curved or angled facades that don't unitize well, (2) tight site access (cranes can't easily land unitized panels), (3) phased construction with field-coordinated tolerances. Stick-built remains a valid choice on appropriate projects.")
        ],
        "faqs": [
            ("What's the difference between stick-built and unitized curtain wall?", "Stick-built is assembled member-by-member on-site. Unitized is prefabricated in shop-assembled panels and craned into place. Stick-built is cheaper but slower; unitized is faster but more expensive."),
            ("Is stick-built curtain wall HVHZ-rated?", "Yes \u2014 HVHZ-rated stick-built curtain wall is available with Miami-Dade NOAs. The full assembly (frame + glass + anchorage + sealants) is tested as a unit."),
            ("How tall can stick-built curtain wall go?", "Stick-built can technically go to high-rise heights but becomes cost-uncompetitive vs unitized above 8-10 stories. Most stick-built work is under 8 stories."),
            ("Which curtain wall type is more weather-tight?", "Unitized is more weather-tight because joints between factory-assembled panels are field-sealed (fewer field-sealed joints). Stick-built has more field-sealed joints, which means more potential leak points."),
            ("Which is faster to install?", "Unitized installs roughly 2x faster than stick-built in the field (5,000-8,000 SF/wk vs 2,500-4,000 SF/wk). However, unitized requires more shop fabrication time upfront.")
        ]
    },
    {
        "slug": "vinyl-vs-aluminum-storefront",
        "title": "Vinyl vs Aluminum Commercial Storefront: Why Aluminum Wins",
        "description": "Vinyl storefront is uncommon in commercial work \u2014 aluminum dominates. ACG explains why and where vinyl shows up.",
        "h1": "Vinyl vs Aluminum Commercial Storefront",
        "summary": "Commercial storefront is overwhelmingly aluminum, not vinyl. Aluminum supports larger openings, higher wind loads, more sophisticated hardware (continuous hinges, panic devices, automatic operators), and better long-term durability. Vinyl storefront exists but is limited to low-rise residential, small commercial, and budget-driven projects \u2014 it cannot match aluminum's commercial-grade structural and hardware capabilities.",
        "sections": [
            ("Why commercial defaults to aluminum", "Aluminum extrusions can be machined to virtually any cross-section, accept steel reinforcement for high wind loads, and support architectural finishes (anodize, PVDF paint, custom colors). Vinyl is a polymer with limited cross-sections, lower stiffness, and limited finish options."),
            ("Opening size limits", "Aluminum storefront supports openings up to 14 feet single-story and unlimited width. Vinyl storefront typically caps at 60-inch wide x 80-inch tall single-leaf maximum. For most commercial work, vinyl simply cannot handle the opening sizes."),
            ("Hardware capability", "Aluminum supports continuous hinges (essential for high-traffic commercial entries), panic hardware, automatic operators, electromagnetic locks, and architectural pulls of any size. Vinyl supports only basic residential hardware with limited weight capacity."),
            ("Wind load capability", "Aluminum thermally-broken commercial storefront with steel-reinforced mullions handles wind pressures up to 100+ PSF. Vinyl storefront caps at roughly 40-60 PSF \u2014 too low for many Florida commercial wall loads, especially on HVHZ work."),
            ("Where vinyl shows up", "Low-rise multi-family (3 stories or less), entry-level hospitality, ground-floor residential conversion, and very small commercial spaces (under 600 SF). Even in these markets, most Florida commercial GCs prefer aluminum because of consistency with the rest of the building's envelope."),
            ("Cost premium for aluminum", "Commercial aluminum storefront: $66-$142/SF installed. Vinyl storefront: $40-$85/SF installed. Aluminum is 50-80% more expensive, but the price premium is justified by opening flexibility, hardware quality, and long-term durability.")
        ],
        "faqs": [
            ("Why is commercial storefront aluminum instead of vinyl?", "Aluminum supports larger openings, higher wind loads, commercial-grade hardware (continuous hinges, panic, auto-operators), and longer service life. Vinyl is limited to small openings, residential hardware, and lower wind exposures."),
            ("Can vinyl storefront be used for commercial?", "Rarely. Vinyl storefront is limited to low-rise multi-family, entry-level hospitality, and very small commercial spaces. For most commercial work, vinyl can't handle the opening sizes or wind loads."),
            ("Is aluminum storefront more expensive than vinyl?", "Yes \u2014 aluminum commercial storefront costs 50-80% more than equivalent vinyl. $66-$142/SF aluminum vs $40-$85/SF vinyl. The premium covers structural capacity and hardware quality."),
            ("Are there HVHZ-rated vinyl storefronts?", "Yes, but with smaller approved opening sizes than aluminum equivalents. For most Florida commercial applications, aluminum HVHZ storefront is the practical answer."),
            ("Does aluminum storefront last longer than vinyl?", "Yes \u2014 commercial aluminum storefront has a documented service life of 30-50 years. Vinyl storefront typically lasts 15-25 years before UV degradation and frame issues require replacement.")
        ]
    },
    {
        "slug": "commercial-skylight-vs-translucent-panel",
        "title": "Commercial Skylight vs Translucent Panel: Cost, Daylight, Applications",
        "description": "Commercial skylights (glass) and translucent panels (Kalwall, Major Industries) offer different daylight qualities. ACG explains when each is the right choice.",
        "h1": "Commercial Skylight vs Translucent Panel",
        "summary": "Commercial overhead glazing comes in two main categories: clear or low-iron glass skylights (sharp views, focused daylight, higher cost), and translucent panel systems like Kalwall and Major Industries Guardian 275 (diffuse daylight, no view, lower cost). The right choice depends on whether you want view-through or pure ambient daylight.",
        "sections": [
            ("Glass skylights: sharp view, focused daylight", "Clear or low-iron glass skylights provide direct view of the sky and focused beams of sunlight. Used on residential, retail, and architectural-feature commercial spaces where view-through is desired. Standard laminated glass for IBC 2407 compliance."),
            ("Translucent panel systems: diffuse daylight, no view", "Kalwall and Major Industries Guardian 275 are fiberglass-reinforced sandwich panels with translucent insulating cores. They diffuse incoming daylight (no focused beams, no view-through), providing even ambient daylight across the space. Higher R-value than glass."),
            ("Best applications by panel type", "Glass skylights: retail spaces, residential, restaurant atriums, hotel lobbies, museum galleries. Translucent panels: warehouses, manufacturing, gymnasiums, recreation centers, athletic facilities, factory spaces \u2014 anywhere you want light but not direct sun."),
            ("Cost comparison", "Glass skylight (laminated insulated, 10x10 ft): $4,500-$9,500 installed. Translucent panel system (10x10 ft Kalwall): $3,200-$6,800 installed. Translucent panels are typically 25-35% cheaper than glass equivalents."),
            ("Energy and daylight performance", "Glass: U-factor 0.30-0.50, SHGC 0.20-0.50 (depends on coating), VLT 60-91%. Translucent panel: U-factor 0.10-0.30 (much better insulator), SHGC 0.10-0.40, diffuse VLT typically 20-50%. Translucent panels are far better insulators but provide less total daylight."),
            ("HVHZ overhead requirements", "Both glass skylights and translucent panels require HVHZ Miami-Dade NOAs for overhead use in HVHZ counties. Kalwall and Major Industries both carry current NOAs for their commercial overhead systems.")
        ],
        "faqs": [
            ("What's the difference between glass skylights and translucent panels?", "Glass skylights provide sharp view-through and focused daylight. Translucent panels (Kalwall, Major Industries) diffuse light into ambient daylight with no view. Each is suited to different applications."),
            ("Are translucent panels cheaper than glass skylights?", "Yes \u2014 translucent panels typically cost 25-35% less than equivalent glass skylight installations. They're also better insulators (lower U-factor)."),
            ("What's Kalwall used for?", "Kalwall is a translucent fiberglass-reinforced panel system used for diffuse daylight in warehouses, gymnasiums, manufacturing, athletic facilities, and similar spaces where ambient light without view-through is desired."),
            ("Can translucent panels be used in HVHZ Florida?", "Yes \u2014 Kalwall and Major Industries Guardian 275 both carry Miami-Dade NOAs for HVHZ overhead use. Confirm the specific NOA is current before specification."),
            ("Which has better R-value?", "Translucent panels have much better R-value (U-factor 0.10-0.30) than glass skylights (0.30-0.50). For energy-sensitive applications, translucent wins.")
        ]
    },
    {
        "slug": "what-is-pvb-vs-sgp-interlayer",
        "title": "PVB vs SGP Interlayer for Laminated Glass (Florida HVHZ)",
        "description": "Laminated glass uses PVB or SGP interlayers. PVB is standard; SGP is 100x stiffer for high-performance applications. ACG explains when to upgrade.",
        "h1": "PVB vs SGP Interlayer for Laminated Glass",
        "summary": "Laminated glass uses one of two interlayer types: PVB (polyvinyl butyral, standard) or SGP (SentryGlas Plus, premium). PVB is the standard interlayer for most HVHZ impact glass. SGP is 100 times stiffer than PVB, used for the most demanding applications: glass railings (post-breakage performance), high-rise overhead glazing, structural glass, security applications, and acoustic-enhanced assemblies.",
        "sections": [
            ("Polyvinyl butyral (PVB) \u2014 the standard interlayer", "PVB is a flexible plastic film commonly 0.030\", 0.060\", or 0.090\" thick. It bonds two glass lites together and holds the assembly intact when broken. Used in 90%+ of HVHZ laminated impact glass and standard safety glazing. Cost-effective and widely available."),
            ("SentryGlas Plus (SGP) \u2014 the premium ionoplast interlayer", "SGP (made by Kuraray) is a high-performance ionoplast interlayer 100x stiffer than PVB. It maintains structural rigidity after glass breakage, making it the standard for glass railings, structural glass beams, and overhead glazing where post-breakage performance matters."),
            ("When PVB is sufficient", "Standard HVHZ storefront and curtain wall laminated impact glass. Vision lites in commercial buildings. Safety glazing at doors and sidelights. Most commercial applications use PVB."),
            ("When SGP is required or recommended", "Glass railings (structural after breakage). Overhead glazing (per IBC 2407). Structural glass fins, beams, or columns. Security glass (jewelry retail, banking). Acoustic-enhanced assemblies (better STC than PVB)."),
            ("Cost comparison", "PVB interlayer adds roughly $5-$15/SF over annealed glass cost. SGP interlayer adds $15-$35/SF \u2014 typically 2-3x the PVB cost. For most commercial work, PVB is the cost-effective choice. SGP is reserved for applications where its performance is justified."),
            ("HVHZ NOA considerations", "Most HVHZ NOAs reference PVB interlayer specifically. Substituting SGP for PVB in an NOA-approved assembly may void the approval unless the NOA explicitly permits SGP. Confirm with the manufacturer and Miami-Dade Product Control before substitution.")
        ],
        "faqs": [
            ("What's the difference between PVB and SGP interlayers?", "PVB is the standard flexible plastic interlayer in most laminated glass. SGP (SentryGlas Plus) is a premium ionoplast interlayer 100x stiffer than PVB \u2014 used for structural and post-breakage-critical applications."),
            ("When should I use SGP interlayer instead of PVB?", "Use SGP for glass railings, overhead glazing, structural glass, security applications, and acoustic-enhanced assemblies. PVB is sufficient for standard HVHZ storefront, curtain wall, and safety glazing."),
            ("How much more expensive is SGP than PVB?", "SGP costs 2-3x more than PVB on the same nominal thickness. PVB adds $5-$15/SF; SGP adds $15-$35/SF over base annealed glass cost."),
            ("Is PVB sufficient for HVHZ impact glass?", "Yes \u2014 PVB is the standard interlayer for most HVHZ impact-rated assemblies. Specific Miami-Dade NOAs reference PVB by manufacturer and thickness."),
            ("Can I substitute SGP for PVB in an NOA assembly?", "Not without manufacturer confirmation. Most NOAs reference the specific interlayer used in testing. Substituting may void the approval. Confirm with the manufacturer before specifying.")
        ]
    },
    {
        "slug": "thermal-break-aluminum-explained",
        "title": "Thermal Break Aluminum Explained (Florida Energy Code)",
        "description": "Thermal break aluminum framing uses a polyamide isolator to reduce heat transfer. Required by Florida Energy Code for most commercial fenestration.",
        "h1": "Thermal Break Aluminum Framing Explained",
        "summary": "Thermal break aluminum framing uses a non-conductive polyamide isolator (typically 14-32mm wide) between the interior and exterior aluminum surfaces. This breaks the thermal bridge that otherwise allows heat to transfer directly through the metal, dramatically improving U-factor. Required by Florida Energy Code for most commercial fenestration in Climate Zones 1 and 2.",
        "sections": [
            ("How thermal break works", "Aluminum is a thermal conductor \u2014 heat transfers through it at 1,400 BTU\u00b7in/hr\u00b7ft\u00b2\u00b7\u00b0F. Without a break, the interior and exterior surfaces of an aluminum frame are at nearly the same temperature, defeating the purpose of insulated glass. The thermal break (polyamide) interrupts this conductivity, allowing the interior surface to stay closer to room temperature."),
            ("Thermal break widths and performance", "Standard thermal break widths: 14mm, 18mm, 24mm, 32mm. Wider = better U-factor. Common Florida commercial frames use 24mm or 32mm thermal breaks. The wider thermal break also reduces condensation risk on the interior frame surface during cold weather."),
            ("FL Energy Code requirements", "Florida Building Code Energy Conservation chapter (FBC EC) requires commercial vertical fenestration in Climate Zone 1 (South Florida) to meet U-factor \u2264 0.50. Climate Zone 2 (rest of FL) requires \u2264 0.55. Without thermal break, aluminum framing typically pushes total U-factor to 0.65-0.85 \u2014 fails code."),
            ("Common thermal-broken systems on Florida commercial", "Kawneer Series 501T, 601T, 701T (T = thermal break). YKK AP YHS 50 TU, YHS 60 TU. Tubelite T14651. EFCO 433. All offer current FL Product Approvals and Miami-Dade NOAs."),
            ("Cost premium for thermal break", "Thermal-broken aluminum frames cost 15-25% more than non-thermal-broken equivalents. The premium is required by code for most commercial work, so it's not really an optional cost \u2014 it's the baseline."),
            ("Coordination with glass spec", "Thermal-broken framing must pair with low-E insulated glass to achieve target U-factor. The framing alone is necessary but not sufficient. The complete assembly U-factor is calculated per NFRC 100 procedure.")
        ],
        "faqs": [
            ("What is thermal break aluminum?", "Thermal break aluminum framing uses a polyamide isolator between the interior and exterior aluminum surfaces. This breaks the thermal bridge that would otherwise allow heat to conduct directly through the metal, improving U-factor."),
            ("Is thermal break required by Florida code?", "Yes \u2014 Florida Energy Code requires commercial vertical fenestration to meet U-factor \u2264 0.50 (Climate Zone 1) or \u2264 0.55 (Climate Zone 2). Achieving this without thermal break is nearly impossible."),
            ("How much wider is thermal break aluminum?", "Standard thermal breaks are 14mm-32mm wide (about 0.55\"-1.26\"). Wider thermal breaks (24mm-32mm) achieve better U-factor."),
            ("Which manufacturers offer thermal-broken storefront?", "Kawneer (Series 501T, 601T, 701T), YKK AP (YHS 50 TU, YHS 60 TU), Tubelite (T14651), EFCO (433) all offer thermal-broken commercial storefront systems for Florida."),
            ("How much more does thermal break cost?", "Thermal-broken aluminum frames typically cost 15-25% more than non-thermal-broken equivalents. The premium is effectively required by Florida Energy Code, so it's part of the baseline cost.")
        ]
    },
    {
        "slug": "what-is-iru-insulating-glass-unit",
        "title": "What Is an Insulating Glass Unit (IGU)? Florida Commercial Standard",
        "description": "An insulating glass unit (IGU) is two glass lites separated by a sealed air or argon cavity. ACG explains construction, performance, and Florida code requirements.",
        "h1": "What Is an Insulating Glass Unit (IGU)?",
        "summary": "An insulating glass unit (IGU) is two or more glass lites separated by a sealed cavity, with the cavity filled with air or inert gas (argon, krypton). The sealed cavity dramatically reduces heat transfer, achieving U-factor 0.30-0.50 vs 1.10 for single-pane. Required by Florida Energy Code for all conditioned commercial space.",
        "sections": [
            ("IGU construction", "Two glass lites (typically 1/4\" each) separated by an aluminum or warm-edge spacer holding them 1/2\" apart. The perimeter is sealed with butyl primary sealant + polysulfide or polyurethane secondary sealant. Cavity filled with argon (most common) or air. Common nominal thickness: 1\" (1/4\" + 1/2\" + 1/4\")."),
            ("Performance metrics", "U-factor: 0.30-0.50 (vs 1.10 single pane). SHGC: 0.20-0.50 (depends on coating). VLT: 35-91% (depends on glass type). Sound transmission loss: STC 28-38 for standard IGUs; higher with laminated lites."),
            ("Argon vs air fill", "Argon-filled IGUs perform 5-10% better than air-filled on U-factor. Argon is heavier and more viscous, slowing convective heat transfer in the cavity. Most modern commercial IGUs are argon-filled at 90%+ concentration."),
            ("Warm-edge vs aluminum spacers", "Aluminum spacers conduct heat at the IGU edge, creating cold spots. Warm-edge spacers (stainless steel or polymer composite) reduce edge conductivity, improving overall U-factor by 5-15%. Most modern commercial IGUs use warm-edge spacers."),
            ("Low-E coating placement", "Low-E coating in an IGU goes on surface #2 (outboard glass, inside the cavity) for Florida hot climates. This reflects solar heat before it enters the building. Surface #3 (inboard glass, inside the cavity) is for cold climates."),
            ("HVHZ IGU configurations", "Standard Florida HVHZ commercial IGU: 1/4\" laminated impact tempered (outboard) + 1/2\" airspace + 1/4\" tempered (inboard) = 1\" nominal. This combines: impact rating + safety break + insulation + low-E coating in one assembly."),
            ("IGU service life", "Properly fabricated and installed commercial IGUs last 20-30 years. Failure mode is seal deterioration allowing moisture vapor into the cavity (visible as fogging or moisture droplets). Warranty typically 10 years against seal failure.")
        ],
        "faqs": [
            ("What is an insulating glass unit (IGU)?", "An IGU is two or more glass lites separated by a sealed cavity (typically 1/2\" filled with argon or air). The sealed cavity reduces heat transfer dramatically, achieving U-factor 0.30-0.50 vs 1.10 single-pane."),
            ("Is argon fill better than air fill?", "Yes \u2014 argon-filled IGUs perform 5-10% better on U-factor than air-filled equivalents. Argon is heavier and slows convective heat transfer in the cavity."),
            ("What's the lifespan of an insulating glass unit?", "Properly fabricated and installed commercial IGUs last 20-30 years. The failure mode is seal deterioration allowing moisture into the cavity. Warranties typically cover the first 10 years."),
            ("Which surface should low-E be on in Florida?", "Surface #2 (outboard glass, inside the cavity) for Florida hot climates. This reflects solar heat before it enters the building."),
            ("Are IGUs required for commercial buildings in Florida?", "Effectively yes. Florida Energy Code requires U-factor \u2264 0.50 (South FL) or \u2264 0.55 (rest of FL) for conditioned commercial space. Single-pane glass cannot meet this; IGUs are the standard solution.")
        ]
    },
    {
        "slug": "shop-drawings-glazing-explained",
        "title": "Shop Drawings for Commercial Glazing: What They Are and Why They Matter",
        "description": "Commercial glazing shop drawings convert architectural plans into fabrication-ready details. ACG explains what's in them and how to review them.",
        "h1": "Shop Drawings for Commercial Glazing",
        "summary": "Commercial glazing shop drawings are detailed fabrication documents produced by the glazier that translate architectural plans into manufacturing-ready details. They include exact mullion locations, glass sizes, hardware schedules, anchorage details, structural calculations, and product approval references. Shop drawing approval is a critical milestone before fabrication begins.",
        "sections": [
            ("What shop drawings include", "(1) Site plan and building elevation references. (2) Glass schedule \u2014 every lite identified by size, type, location. (3) Mullion layout drawings \u2014 every framing member located in plan and section. (4) Anchorage details \u2014 how the frame connects to the building structure. (5) Hardware schedule \u2014 closers, panic, hinges, locks, sweeps. (6) Section details \u2014 head, jamb, sill, mullion details. (7) Structural calculations showing wind load compliance. (8) NOA or FL Product Approval references."),
            ("Shop drawing approval process", "Step 1: Glazier produces shop drawings (typically 15-25 working days). Step 2: Architect and owner review and mark up. Step 3: Glazier revises and re-submits. Step 4: Architect approves. Step 5: Permit submittal package assembled. Step 6: AHJ permit review. Step 7: Fabrication begins after permit is issued."),
            ("What to look for as architect/owner reviewer", "(1) Glass spec matches your project requirements. (2) Mullion layout matches architectural intent. (3) Anchorage to structure is detailed for the actual building (not generic). (4) Hardware schedule is complete and matches finish hardware schedule. (5) NOA references are current and match the design pressure. (6) ADA compliance noted at accessible entries. (7) Sealant joint details show proper bedding and weep system."),
            ("Common shop drawing mistakes", "(1) Wind pressure on drawings doesn't match calculated DP. (2) Generic anchorage details instead of project-specific. (3) Hardware schedule missing or mismatched with arch schedule. (4) Expired or wrong NOA referenced. (5) Glass schedule confuses tempered vs heat-strengthened. (6) Missing acoustic or solar performance specifications when called for in arch spec."),
            ("Schedule impact of shop drawing delays", "Typical: 15-25 working days for first submittal, 5-10 days for revisions. Total: 4-6 weeks if revisions are minor. Add 2-3 weeks per major revision round. Submittal delays directly delay material ordering and field install."),
            ("ACG's shop drawing turnaround", "ACG produces commercial glazing shop drawings using AI-augmented workflows (documented at acglass.ai). Standard turnaround: 10-15 working days for storefront, 15-25 working days for curtain wall. Faster than the FL market average of 20-30 days.")
        ],
        "faqs": [
            ("What are shop drawings for commercial glazing?", "Shop drawings are detailed fabrication documents produced by the glazier that translate architectural plans into manufacturing-ready details. They include mullion locations, glass schedules, anchorage, hardware, and structural calcs."),
            ("Who produces shop drawings, the architect or glazier?", "The glazier produces shop drawings. The architect provides design intent in the architectural drawings, but the detailed fabrication-ready shop drawings are the glazier's responsibility."),
            ("How long do shop drawings take?", "First submittal: 15-25 working days for storefront, 15-30 for curtain wall. Revisions: 5-10 days each. Total cycle: 4-8 weeks depending on revision rounds."),
            ("Do I need to approve shop drawings before fabrication?", "Yes \u2014 architect and owner approval of shop drawings is required before the glazier can order materials and begin fabrication. Approval is the critical milestone in the project schedule."),
            ("What's the biggest shop drawing mistake to watch for?", "Design pressure mismatch \u2014 the wind load on the shop drawings must match (or exceed) the project's calculated wind pressure. NOA references must match the design pressure rating.")
        ]
    },
    {
        "slug": "what-is-noa-renewal-process",
        "title": "Miami-Dade NOA Renewal Process Explained",
        "description": "Miami-Dade NOAs expire every 5 years and must be renewed. ACG explains the renewal process and how to verify current approval status.",
        "h1": "Miami-Dade NOA Renewal Process",
        "summary": "Miami-Dade Notice of Acceptance (NOA) approvals are issued for 5-year terms and must be renewed by the manufacturer before expiration. Renewal requires re-submitting test data, paying renewal fees, and demonstrating product continuity. Expired NOAs cannot be used for new permits in HVHZ counties.",
        "sections": [
            ("How NOA terms work", "Miami-Dade County Product Control issues NOAs for 5-year terms. The expiration date is printed on the NOA document. Once expired, the NOA cannot be referenced in new permit submittals \u2014 even if the product is unchanged."),
            ("Renewal process", "Manufacturer submits a renewal application to Miami-Dade County Product Control 6-12 months before expiration. The renewal includes: (1) updated test reports (if testing has been redone), (2) statement of product continuity (confirming no design changes), (3) renewal fee payment, (4) any AHJ-required documentation. Review takes 4-12 weeks."),
            ("Common renewal complications", "(1) Manufacturer didn't anticipate renewal and missed the deadline. (2) Product design changed during the 5-year term \u2014 requires new full approval, not just renewal. (3) Testing requirements changed during the 5-year term \u2014 product needs new testing to meet current standards. (4) Manufacturer discontinued the product \u2014 NOA expires, no renewal."),
            ("Verifying NOA status before specification", "Always check the Miami-Dade County Product Control NOA database before specifying any product. Confirm: (1) the NOA is marked 'Approved' (not 'Pending Renewal' or 'Expired'). (2) The expiration date is at least 6 months in the future for permits that will take time to submit. (3) The approved configurations match your design pressure and assembly."),
            ("What happens if you specify with an expired NOA", "Permit submittal will be rejected. Project schedule delays 2-4 weeks while finding a replacement product with current approval. May require shop drawing revisions and re-engineering. Most importantly: glazier is on the hook to find a substitute that fits the design, often at additional cost."),
            ("Best practice: 'in good standing' verification at submittal", "Before submitting permit, run the NOA database search and document each NOA's current status with a screenshot. This protects the glazier and the project from renewal-related delays.")
        ],
        "faqs": [
            ("How long is a Miami-Dade NOA valid?", "Miami-Dade NOAs are issued for 5-year terms. They must be renewed by the manufacturer before expiration. Expired NOAs cannot be used in new permit submittals."),
            ("Who renews NOAs?", "The manufacturer is responsible for NOA renewal. Contractors and glaziers should verify the NOA is current before specifying or submitting for permit."),
            ("What happens if I use an expired NOA?", "Permit submittal will be rejected. The project must find a replacement product with current approval, causing 2-4 weeks of schedule delay and potentially requiring re-engineering."),
            ("How do I check NOA status?", "Search the Miami-Dade County Product Control NOA database online. Confirm the NOA is marked 'Approved' and the expiration date is in the future."),
            ("Can an NOA expire mid-project?", "Yes \u2014 if your project takes years to complete, an NOA used at permit submittal may expire before installation. This generally doesn't void the original approval for that specific permit, but it can complicate change orders and renewals.")
        ]
    },
    {
        "slug": "commercial-glazier-bid-process-florida",
        "title": "Commercial Glazier Bid Process in Florida: From Plans to Award",
        "description": "How Florida commercial glaziers bid commercial projects: from plan receipt through award. ACG explains the standard timeline and what GCs should expect.",
        "h1": "Commercial Glazier Bid Process in Florida",
        "summary": "Florida commercial glazing bids follow a standard 7-step process: (1) plans received, (2) takeoff and scope review, (3) quote development, (4) sealed bid submission, (5) bid leveling by GC, (6) qualification interview, (7) award. Standard FL market timeline: 7-15 business days. ACG benchmark: 48 hours on standard commercial plans.",
        "sections": [
            ("Step 1: Plans received", "GC or owner sends architectural drawings via email, Procore, BuildingConnected, or BidEngine. Standard package: architectural elevation drawings, glazing schedule, hardware schedule, spec section (CSI Division 08), and any addenda. Quality of plans dramatically affects bid quality \u2014 narrative-only bids carry 15-25% contingency."),
            ("Step 2: Takeoff and scope review", "Glazier reviews drawings and identifies all glazing scope: storefront, curtain wall, window wall, impact-rated openings, all-glass entrances, glass railings, and any decorative glass. Counts linear feet of mullion, square feet of glass, and counts of hardware items. ACG uses AI-augmented takeoff (documented at acglass.ai) to compress this from 2-3 days to 4-8 hours."),
            ("Step 3: Quote development", "Glazier prices: aluminum framing (per LF), glass (per SF), hardware (per item), sealants and accessories (per SF), shop drawings and engineering (lump sum), NOA/FL Product Approval submittal (lump sum), field installation labor (per SF), and project management. Add overhead and profit. Subtotal becomes the bid number."),
            ("Step 4: Sealed bid submission", "Glazier produces a written bid package: cover letter, scope of work, exclusions, qualifications, price, and validity period (typically 30 days). Submitted via email or platform. Most GCs require sealed bid by a specific deadline."),
            ("Step 5: Bid leveling by GC", "GC compares all bids side-by-side: price, scope inclusions/exclusions, qualifications, references, and bonding capacity. Bids more than 20% below or above the average get flagged. GC asks clarifying questions to align scope across bidders."),
            ("Step 6: Qualification interview", "Top 2-3 bidders interviewed by GC project manager. Topics: HVHZ submittal experience, similar project references, bonding letter, license verification, crew availability, schedule fit, and any value-engineering options. This stage filters out unqualified low bidders."),
            ("Step 7: Award", "GC issues a letter of intent (LOI) or signed subcontract to the winning glazier. Contract typically AIA A401-style subcontract with $3M/$6M bonding required. Award triggers shop drawing kickoff and material ordering."),
            ("ACG's 48-hour bid response benchmark", "ACG returns sealed bids on standard commercial plans in 48 hours \u2014 not the FL market average of 7-15 business days. We achieve this with AI-augmented takeoff, standardized pricing tables, and a streamlined bid review process. This speed wins us bids regularly.")
        ],
        "faqs": [
            ("How long does a commercial glazier bid take in Florida?", "Standard FL market: 7-15 business days from plans received to sealed bid. ACG benchmark: 48 hours on standard commercial plans. Bid speed correlates with operational discipline downstream."),
            ("What does a commercial glazing bid include?", "Aluminum framing, glass, hardware, sealants, shop drawings and engineering, NOA submittal, field installation, and project management. Standard exclusions: permit fees, rough opening prep, perimeter caulk by GC, and lifts/scaffolding."),
            ("How does a GC compare commercial glazing bids?", "GC compares price, scope inclusions/exclusions, qualifications, references, and bonding. Bids more than 20% below or above the average get scrutinized. The cheapest bid usually has missing scope."),
            ("What's the typical bid validity period?", "Standard FL commercial glazing bids are valid 30 days. Some longer projects accept 60-day validity, but most glaziers price-protect for 30 days to manage material cost exposure."),
            ("Should I bid commercial glazing to 3 or 5 glaziers?", "Three qualified bidders is the sweet spot. Five invites unqualified low bidders who don't have the operational discipline to execute. Pre-qualify by license, bonding, and portfolio before sending plans.")
        ]
    },
]


# ============================================================
# 10 more vertical x city
# ============================================================

VC5 = [
    ("restaurant-glazier-sarasota", "Restaurant", "Sarasota", "Sarasota", "sarasota", "sarasota-county", "restaurant-glazier-florida", 27.3364, -82.5404,
        "Sarasota restaurant construction is strong \u2014 downtown Main Street, St Armands Circle, Lakewood Ranch corridor. Chef-driven restaurants and brand-driven national rollouts. WBDR coastal.",
        "Sarasota is WBDR \u2014 ASTM E1996/E1886 impact assemblies required. City of Sarasota design review on downtown corridor."),
    ("hotel-glazing-contractor-jacksonville", "Hotel", "Jacksonville", "Duval", "jacksonville", "duval-county", "hotel-glazing-contractor-florida", 30.3322, -81.6557,
        "Jacksonville hotel construction is recovering with downtown waterfront, San Marco, and Town Center concentrations. Standard FBC inland; coastal WBDR for Beaches communities.",
        "Coastal Jacksonville (Beaches) is WBDR. Inland Duval is standard FBC. Multi-market AHJ structure consolidated under City of Jacksonville Building Inspection."),
    ("medical-office-glazier-fort-lauderdale", "Medical Office", "Fort Lauderdale", "Broward", "fort-lauderdale", "broward-county", "medical-office-glazier-florida", 26.1224, -80.1373,
        "Fort Lauderdale MOB construction is driven by Memorial Healthcare System, Broward Health, and Cleveland Clinic Florida Weston. Strong specialty clinic market across Broward.",
        "Broward MOB construction requires Miami-Dade NOA. ADA-compliant entrances with auto-operators standard."),
    ("retail-storefront-installer-jacksonville", "Retail", "Jacksonville", "Duval", "jacksonville", "duval-county", "retail-storefront-installer-florida", 30.3322, -81.6557,
        "Jacksonville retail concentrates on St. Johns Town Center, San Marco Square, Riverside Avondale, Avenues area. Strong national chain rollouts plus boutique retail.",
        "Coastal Jacksonville is WBDR. Inland Duval is standard FBC. Most Jacksonville retail is inland (standard FBC)."),
    ("retail-storefront-installer-sarasota", "Retail", "Sarasota", "Sarasota", "sarasota", "sarasota-county", "retail-storefront-installer-florida", 27.3364, -82.5404,
        "Sarasota retail is strong on St Armands Circle, downtown Main Street, and Westfield Sarasota Square. WBDR coastal exposure for all retail.",
        "Sarasota is WBDR \u2014 ASTM E1996/E1886 impact glass required."),
    ("office-building-glazier-sarasota", "Office Building", "Sarasota", "Sarasota", "sarasota", "sarasota-county", "office-building-glazier-florida", 27.3364, -82.5404,
        "Sarasota office construction is concentrated downtown and along Tamiami Trail. Medical office, professional services, and corporate satellite offices.",
        "Sarasota is WBDR. ASTM E1996/E1886 impact assemblies required for office facades."),
    ("school-glazier-naples", "School / Education", "Naples", "Collier", "naples", "collier-county", "school-glazier-florida", 26.1420, -81.7948,
        "Collier County Public Schools serves Naples, Marco Island, and Bonita Springs area. Strong K-12 construction and FGCU expansion driving education sector demand.",
        "Collier schools are WBDR coastal. ASTM E1996/E1886 impact-rated assemblies required. Post-Parkland security vestibule standards apply."),
    ("school-glazier-sarasota", "School / Education", "Sarasota", "Sarasota", "sarasota", "sarasota-county", "school-glazier-florida", 27.3364, -82.5404,
        "Sarasota County Schools has ongoing K-12 capital construction. Plus New College of Florida, Ringling College, and USF Sarasota-Manatee.",
        "Sarasota County is WBDR. Schools require ASTM E1996/E1886 impact assemblies. Post-Parkland security vestibule standards."),
    ("medical-office-glazier-orlando", "Medical Office", "Orlando", "Orange", "orlando", "orange-county", "medical-office-glazier-florida", 28.5384, -81.3789,
        "Orlando MOB construction is driven by AdventHealth Orlando, Orlando Health, and Nemours Children's Hospital. Strong specialty clinic and Lake Nona Medical City growth.",
        "Orlando is inland \u2014 standard FBC. Impact assemblies optional. ADA accessibility on all medical entries."),
    ("hotel-glazing-contractor-sarasota", "Hotel", "Sarasota", "Sarasota", "sarasota", "sarasota-county", "hotel-glazing-contractor-florida", 27.3364, -82.5404,
        "Sarasota hotel construction is strong on Lido Beach, St Armands Circle, downtown waterfront, and Lakewood Ranch corridor. Resort-driven tourism market.",
        "Sarasota is WBDR coastal. ASTM E1996/E1886 impact assemblies required for all hotel envelope work.")
]


# ============================================================
# 8 more Tennessee cities/neighborhoods
# ============================================================

TN_MORE = [
    # Brentwood neighborhoods
    ("brentwood-tn/maryland-farms-brentwood", "Maryland Farms", "brentwood-tn", "Brentwood", 36.0331, -86.7828, "Williamson",
        "Maryland Farms is Brentwood's primary Class-A office submarket. Corporate headquarters and professional services driving ongoing commercial construction."),
    # Franklin neighborhoods
    ("franklin-tn/cool-springs-franklin", "Cool Springs (Franklin)", "franklin-tn", "Franklin", 35.9678, -86.8133, "Williamson",
        "Cool Springs Franklin is the southern half of the Williamson County office and retail corridor \u2014 Mallory Lane, McEwen Drive, Tractor Supply Company HQ. Active commercial construction."),
    ("franklin-tn/downtown-franklin", "Downtown Franklin", "franklin-tn", "Franklin", 35.9251, -86.8688, "Williamson",
        "Downtown Franklin is the historic Main Street commercial corridor. Boutique retail, restaurant, and adaptive-reuse commercial. Strict Franklin Historic Zoning Commission review."),
    # Memphis neighborhoods
    ("memphis/downtown-memphis", "Downtown Memphis", "memphis", "Memphis", 35.1465, -90.0490, "Shelby",
        "Downtown Memphis includes Beale Street, FedExForum, AutoZone Park, and a rapidly redeveloping Pinch District. Commercial growth in entertainment, hospitality, and office."),
    ("memphis/east-memphis-poplar", "East Memphis (Poplar Corridor)", "memphis", "Memphis", 35.1257, -89.8765, "Shelby",
        "East Memphis along Poplar Avenue is the city's primary commercial spine \u2014 office, retail, healthcare, and restaurant concentrate here. Strong Class-A and Class-B office market."),
    # Knoxville neighborhoods
    ("knoxville/downtown-knoxville", "Downtown Knoxville", "knoxville", "Knoxville", 35.9606, -83.9207, "Knox",
        "Downtown Knoxville includes Market Square, Old City, and World's Fair Park area. Strong restaurant, brewery, retail, and office commercial market."),
    ("knoxville/turkey-creek-knoxville", "Turkey Creek", "knoxville", "Knoxville", 35.8995, -84.1623, "Knox",
        "Turkey Creek is West Knoxville's primary retail and restaurant corridor \u2014 Pinnacle at Turkey Creek shopping center and surrounding office. Strong national chain rollouts."),
    # Chattanooga neighborhoods
    ("chattanooga/downtown-chattanooga", "Downtown Chattanooga", "chattanooga", "Chattanooga", 35.0456, -85.3097, "Hamilton",
        "Downtown Chattanooga includes Riverfront, Bluff View Art District, Innovation District, and Tennessee Aquarium area. Strong commercial and tourism-driven construction.")
]


def schema_tn(canonical, name, lat, lng, area_name):
    return [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org",
         "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711",
         "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
         "address": {"@type": "PostalAddress", "addressLocality": "Nashville", "addressRegion": "TN", "addressCountry": "US"},
         "sameAs": ORG_SAMEAS,
         "areaServed": {"@type": "Place", "name": area_name, "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}},
        {"@context": "https://schema.org", "@type": "Service", "name": f"Commercial Storefront Glazier \u2014 {name}",
         "serviceType": "Commercial Glazing", "areaServed": area_name,
         "provider": {"@id": canonical + "#org"}}
    ]


def build_tn_submarket(slug, name, parent_slug, parent, lat, lng, county, blurb):
    canonical = f"https://acglass.com/{slug}/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Tennessee &middot; {html_lib.escape(parent)} Submarket</div>
<h1 style="color:#fff;font-size:clamp(32px,5vw,52px);line-height:1.1;margin:0 0 24px;">Storefront Glazier \u2014 {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Aluminum commercial storefront (Kawneer, YKK AP, Tubelite, EFCO)</li>
<li>Curtain wall and window wall</li>
<li>Restaurant folding glass walls and multi-slide doors</li>
<li>All-glass entrances</li>
<li>Glass railings</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>350+ commercial projects in Florida, applying the same operating playbook to Tennessee.</li>
<li>Nashville office opening Q3 2026 \u2014 bidding {html_lib.escape(name)} work now.</li>
<li>48-hour bid turnaround.</li>
<li>Parent city: <a href="/{parent_slug}/" style="color:#E11320;">{html_lib.escape(parent)} commercial storefront services</a>.</li>
</ul>
</div>
</section>'''
    schemas = schema_tn(canonical, name, lat, lng, f"{name}, {parent}, TN")
    bc = [("Home", "https://acglass.com/"), ("Tennessee", "https://acglass.com/tennessee/"), (parent, f"https://acglass.com/{parent_slug}/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name} \u2014 {parent}, TN | ACG"
    description = f"Commercial storefront glazing in {name}, {parent}, TN. ACG opens Nashville Q3 2026. 350+ FL projects."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(name)}, {html_lib.escape(parent)}, TN">
<meta name="geo.region" content="US-TN">
<meta name="ICBM" content="{lat}, {lng}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html(slug + "/index.html", html)


# ============================================================
# Service areas map
# ============================================================

def build_service_areas_map():
    canonical = "https://acglass.com/service-areas-map/"
    body = '''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Service Areas &middot; FL + TN</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">ACG Service Areas Map</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">ACG commercial glazing services across 25 Florida counties + Q3 2026 Tennessee expansion. Browse the map below by region, or jump directly to your market.</p>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1100px;">

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">South Florida (HVHZ)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/west-palm-beach/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">West Palm Beach</a>
<a href="/miami/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Miami</a>
<a href="/fort-lauderdale/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Fort Lauderdale</a>
<a href="/coral-gables/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Coral Gables</a>
<a href="/boca-raton/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Boca Raton</a>
<a href="/aventura/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Aventura</a>
<a href="/jupiter/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Jupiter</a>
<a href="/palm-beach/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Palm Beach</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Southwest Florida (WBDR)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/naples/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Naples</a>
<a href="/marco-island/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Marco Island</a>
<a href="/bonita-springs/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Bonita Springs</a>
<a href="/fort-myers/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Fort Myers</a>
<a href="/cape-coral/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Cape Coral</a>
<a href="/estero/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Estero</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Tampa Bay (WBDR)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/tampa/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Tampa</a>
<a href="/st-petersburg/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">St. Petersburg</a>
<a href="/clearwater/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Clearwater</a>
<a href="/sarasota/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Sarasota</a>
<a href="/bradenton/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Bradenton</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Treasure Coast (WBDR)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/vero-beach/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Vero Beach</a>
<a href="/stuart/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Stuart</a>
<a href="/port-saint-lucie/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Port St. Lucie</a>
<a href="/palm-city/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Palm City</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Central Florida (Standard FBC)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/orlando/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Orlando</a>
<a href="/winter-park/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Winter Park</a>
<a href="/kissimmee/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Kissimmee</a>
<a href="/sanford/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Sanford</a>
<a href="/lakeland/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Lakeland</a>
<a href="/ocala/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Ocala</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">North Florida + Panhandle</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/jacksonville/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Jacksonville</a>
<a href="/st-augustine/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">St. Augustine</a>
<a href="/ponte-vedra-beach/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Ponte Vedra Beach</a>
<a href="/tallahassee/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Tallahassee</a>
<a href="/gainesville/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Gainesville</a>
<a href="/pensacola/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Pensacola</a>
<a href="/daytona-beach/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Daytona Beach</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Florida Keys</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/key-west/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Key West</a>
<a href="/key-largo/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Key Largo</a>
<a href="/marathon/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Marathon</a>
</div>

<h2 style="color:#fff;font-size:28px;margin-bottom:24px;">Tennessee (Q3 2026)</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px;">
<a href="/nashville/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Nashville</a>
<a href="/brentwood-tn/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Brentwood</a>
<a href="/franklin-tn/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Franklin</a>
<a href="/murfreesboro-tn/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Murfreesboro</a>
<a href="/cool-springs-tn/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Cool Springs</a>
<a href="/memphis/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Memphis</a>
<a href="/knoxville/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Knoxville</a>
<a href="/chattanooga/" style="background:#0e284f;padding:16px 20px;border-radius:6px;text-decoration:none;color:#fff;border-left:3px solid #E11320;font-weight:600;">Chattanooga</a>
</div>

<div style="background:#0e284f;padding:32px;border-radius:8px;border-left:3px solid #E11320;text-align:center;">
<h3 style="color:#fff;font-size:22px;margin:0 0 10px;">Not seeing your market?</h3>
<p style="color:rgba(255,255,255,0.75);font-size:16px;margin:0 0 20px;">ACG bids commercial work across all 67 Florida counties plus Tennessee. Send plans to bids@acglass.com or call (772) 486-7711.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>

</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org",
         "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711",
         "sameAs": ORG_SAMEAS,
         "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"},
         "areaServed": [{"@type": "State", "name": "Florida"}, {"@type": "State", "name": "Tennessee"}]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
                              {"@type": "ListItem", "position": 2, "name": "Service Areas Map", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "ACG Service Areas \u2014 Florida Counties + Tennessee Coverage Map | ACG"
    description = "ACG commercial glazing service areas: 25 Florida counties + Tennessee Q3 2026 expansion. Browse coverage by region: South FL HVHZ, SW FL, Tampa Bay, Central FL, North FL, Keys, Tennessee."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html("service-areas-map/index.html", html)


if __name__ == "__main__":
    print("Building 10 more AIO FAQ...")
    for a in AIO6:
        build_aio(a)
    print("\nBuilding 10 more vertical x city...")
    for v in VC5:
        build_vc2(*v)
    print("\nBuilding 8 more TN submarkets...")
    for tn in TN_MORE:
        build_tn_submarket(*tn)
    print("\nBuilding /service-areas-map/...")
    build_service_areas_map()
    total = len(AIO6) + len(VC5) + len(TN_MORE) + 1
    print(f"\nTotal wave 8: {total}")
