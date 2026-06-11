#!/usr/bin/env python3
"""Build the 7th spec page: Section 08 51 13 Aluminum Windows.

Modeled on the existing spec pages; uses real CSI 3-part structure.
"""
import json
from pathlib import Path
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/t13-spec-augment.py').read().split('# Process each existing')[0])

ROOT = Path('/home/user/workspace/acglass-website')
SPECS = ROOT / 'architect-specs'

new_path = SPECS / 'section-08-51-13-aluminum-windows.html'

spec_body = """PART 1 GENERAL

1.1 SUMMARY
A. Section includes commercial aluminum windows: fixed, single-hung, horizontal slider, casement, awning, projected, and double-hung configurations for commercial occupancies in Florida.

1.2 REFERENCES
A. AAMA/WDMA/CSA 101/I.S.2/A440 — North American Fenestration Standard (NAFS).
B. ASTM E283 — Standard Test Method for Determining Rate of Air Leakage.
C. ASTM E330 — Standard Test Method for Structural Performance of Exterior Windows.
D. ASTM E331 — Standard Test Method for Water Penetration of Exterior Windows.
E. ASTM E1886 / E1996 — Impact Resistance (HVHZ).
F. ANSI Z97.1 / 16 CFR 1201 — Safety Glazing.
G. Florida Building Code 8th Edition; Miami-Dade NOA for HVHZ projects; Florida Building Code Energy Conservation (FBC-EC).

1.3 PERFORMANCE REQUIREMENTS
A. Wind Load: Per ASCE 7-22 for project location and exposure category.
B. Air Infiltration: ≤ 0.30 cfm/sf per ASTM E283 at 6.24 psf.
C. Water Infiltration Resistance: No leakage at 15% of design pressure per ASTM E331, minimum 8 psf.
D. Forced Entry Resistance: AAMA 1304 Grade 10 minimum.
E. Impact Resistance (HVHZ): Large- and small-missile per ASTM E1886/E1996.
F. Thermal Performance: U-factor and SHGC values per FBC-EC compliance method (prescriptive, performance, or energy modeling).
G. Cycle Performance (operable): 4,000-cycle minimum life test per AAMA 920 (or equivalent) for hinged/sliding operating sash.

1.4 SUBMITTALS
A. Product Data — manufacturer cut sheets for each window type, including profile dimensions, glass make-up, frame finish, and hardware.
B. Shop Drawings — sealed by a Florida-licensed PE, showing window types, locations, glazing schedule, anchor patterns, and perimeter conditions.
C. Florida Product Approval (FL PA) — current approval for each proposed window type and configuration.
D. Miami-Dade NOA — for HVHZ projects, current Notice of Acceptance covering the specific tested configuration.
E. Structural Calculations — project-specific anchor and member calculations sealed by a Florida-licensed PE.
F. Thermal Performance Data — NFRC-certified U-factor, SHGC, VT, and condensation resistance.
G. Glazing Schedule — full make-up by elevation including low-E coating type and surface position.
H. Samples — frame corner section and operating hardware sample.
I. Warranty — manufacturer's standard warranty plus installer warranty document.

1.5 QUALITY ASSURANCE
A. Manufacturer: Holding current Florida Product Approval for proposed windows.
B. Installer: Manufacturer-authorized, demonstrated minimum 5 commercial window installations of comparable scope.
C. Mock-Up: For projects exceeding 50 commercial windows, provide a project-specific mock-up unit for performance verification prior to mass fabrication.

PART 2 PRODUCTS

2.1 MANUFACTURERS
A. Acceptable Manufacturers (basis of design):
1. ESWindows (Tecnoglass) — single-hung, horizontal slider, casement, projected, fixed.
2. PGT Industries — WinGuard Aluminum impact line.
3. Aldora Aluminum and Glass — architectural fixed, casement, awning, single-hung, mullions.
B. Substitutions: Permitted only with prior approval; substituted product must carry current FL PA and (HVHZ) NOA documentation equivalent to basis of design.

2.2 SYSTEM
A. Frame: Aluminum 6063-T5 or T6 extrusion with thermal break where required by FBC-EC.
B. Glass: 1-inch insulating glass minimum. Laminated interlayer (0.090 in PVB or SGP) on the exterior lite for impact-rated assemblies. Heat-strengthened or tempered as required by code.
C. Hardware: Stainless steel where exposed to coastal exposure; AAMA 901 forced-entry compliant.
D. Sealants: Low-modulus silicone, AAMA 850 / 853 compliant; bond-compatible with adjacent substrates.
E. Anchors: Stainless steel, sized per project-specific structural calculation.
F. Finish: PVDF (Kynar 500) 2-coat or 3-coat, AAMA 2605 compliant; anodized class I per AAMA 611 acceptable as alternate.

PART 3 EXECUTION

3.1 INSTALLATION
A. Install per approved shop drawings, manufacturer instructions, and AAMA InstallationMasters guidelines.
B. Verify rough opening is plumb, level, and square within manufacturer's tolerance prior to setting frame.
C. Anchor per project-specific structural calculation. Do not deviate from approved anchor pattern.
D. Install pan flashing and perimeter membrane per project water-management details.
E. Seal perimeter with low-modulus silicone tooled to a concave joint profile."""

# Build the head (copy from existing storefront spec, swap CSI numbers + h1 + summary)
existing_storefront = (SPECS / 'section-08-41-13-aluminum-storefront.html').read_text()
# Find through the first </p> after csi-num in spec-hero
# Then continue through copy button section to <pre class="spec-body"
head_end_idx = existing_storefront.find('<pre class="spec-body"')
if head_end_idx < 0:
    raise SystemExit("template head end not found")
head = existing_storefront[:head_end_idx]

# Replace the CSI number, title, and summary
head = head.replace('Section 08 41 13 - Aluminum Storefront Framing', 'Section 08 51 13 - Aluminum Windows')
head = head.replace('section-08-41-13-aluminum-storefront', 'section-08-51-13-aluminum-windows')
head = head.replace('"SECTION 08 41 13"', '"SECTION 08 51 13"')
head = head.replace('SECTION 08 41 13', 'SECTION 08 51 13')
head = head.replace('Aluminum Storefront Framing', 'Aluminum Windows')
head = head.replace('Commercial storefront aluminum framing systems including stick-built and pre-glazed configurations, with Florida Product Approval and Miami-Dade NOA references.',
                     'Commercial aluminum window systems for fixed, single-hung, slider, casement, awning, and projected configurations, with Florida Product Approval and Miami-Dade NOA references.')

# Augment block — built below after constants are defined


# Footer
footer = '''
    <p class="spec-footer-note">Prepared by American Commercial Glass (ACG), Florida CGC #1531993, for use by architects and specification writers. This spec section is provided as a starting point — modify per project, code edition, and AHJ requirements. Always verify Florida Product Approval / Miami-Dade NOA documentation matches the specified system. For questions or system-specific guidance, contact <a href="mailto:specs@acglass.com" style="color:rgba(255,255,255,0.85);">specs@acglass.com</a>.</p>

    <script>
      function copySpec() {
        const text = document.getElementById('specBody').innerText;
        navigator.clipboard.writeText(text).then(() => {
          document.getElementById('copyStatus').classList.add('show');
          setTimeout(() => document.getElementById('copyStatus').classList.remove('show'), 2000);
        });
      }
    </script>
  </main>
</body>
</html>
'''

# Constants we imported don't include COMMON_PART_1_ADDITIONS; load from spec-expansions.py
from importlib import util
spec = util.spec_from_file_location("spec_exp", "/tmp/spec-expansions.py")
# Just inline a strip-down expansion since the imported file expects a different path 
# Use the constants directly:
COMMON_PART_1_ADDITIONS = """
1.6 DELIVERY, STORAGE, AND HANDLING
A. Deliver materials in manufacturer's original, unopened, undamaged containers with identification labels intact.
B. Store materials in a dry, ventilated location, off the ground, protected from weather, moisture, dust, and contact with dissimilar materials. Maintain factory-applied protective coverings until immediately prior to installation.
C. Handle glass per GANA Glazing Manual Section 13. Reject and replace any unit with cracked, chipped, or scratched glass. Do not store glass in direct sunlight; cover with non-staining, opaque material if outdoor storage is unavoidable.
D. Field-measure all openings prior to fabrication. Do not begin fabrication until field measurements are reconciled against shop drawings and recorded on the project Owner-Architect-Contractor (OAC) meeting log.

1.7 PROJECT CONDITIONS
A. Field Measurements: Verify dimensions of structural openings and tolerances at perimeter conditions before fabrication.
B. Existing Conditions: Coordinate with adjacent trades — concrete, masonry, framing, sheathing, water-resistive barriers, flashings.
C. Coordination: Verify that openings, anchors, embeds, sealant joints, and water-resistive barrier terminations are installed and inspected before window installation begins.
"""

COMMON_PART_3_ADDITIONS = """
3.4 EXAMINATION
A. Examine openings, substrates, and structural support for compliance with manufacturer's requirements. Verify rough openings are plumb, square, and within manufacturer's tolerances.
B. Verify continuity of water-resistive barrier (WRB) and air barrier at the rough opening.
C. Proceed only after unsatisfactory conditions have been corrected.

3.5 PREPARATION
A. Clean opening surfaces immediately before installation. Remove dust, debris, and loose particles.
B. Apply primers and sealant tapes per manufacturer instructions where required.

3.6 ADJUSTING
A. Adjust operating sashes, hardware, and accessories for smooth, leak-proof operation.
B. Replace defective work that cannot be successfully repaired.

3.7 CLEANING AND PROTECTION
A. Remove labels, dirt, and excess sealant from finished surfaces using methods recommended by manufacturers.
B. Provide temporary protection against staining, scratching, and construction damage. Remove at Substantial Completion.

3.8 DEFICIENCY PROCEDURES
A. Document deficiencies in the project OAC log. Coordinate with General Contractor on corrective action.
B. Investigate any water infiltration following AAMA 511 forensic procedures.
"""

pre_section = f'    <pre class="spec-body" id="specBody">{spec_body}\n\n{COMMON_PART_1_ADDITIONS.strip()}\n\n{COMMON_PART_3_ADDITIONS.strip()}\n\nEND OF SECTION</pre>\n'

# Now build augment
augment = build_augment_block('section-08-51-13-aluminum-windows.html')

# ACG Spec Writing Notes sidebar
notes_sidebar = '''
    <aside class="spec-notes" style="max-width:880px;margin:40px auto 60px;padding:24px 28px;background:rgba(255,255,255,0.03);border-left:3px solid #e11320;border-radius:6px;color:rgba(255,255,255,0.85);">
      <h2 style="color:#e11320;font-size:14px;letter-spacing:0.08em;text-transform:uppercase;margin:0 0 16px;">ACG Spec Writing Notes</h2>
      <p style="margin:0 0 12px;line-height:1.7;">Commercial aluminum windows in Florida sit at the intersection of FBC wind code, FBC energy code, and accessibility/egress requirements. The spec writer&rsquo;s job is to constrain enough to get apples-to-apples bids on a known-compliant product list — without locking the project to a single source.</p>
      <h3 style="font-size:14px;color:#fff;margin:20px 0 8px;">Florida-specific considerations</h3>
      <ul style="margin:0 0 12px;padding-left:20px;line-height:1.7;">
        <li>HVHZ (Miami-Dade, Broward, parts of Palm Beach): Both a Florida Product Approval AND a Miami-Dade NOA are required. FPA alone is insufficient for HVHZ permit submission.</li>
        <li>FBC-EC compliance method: The chosen compliance method (prescriptive, performance, or energy model) drives the U-factor / SHGC / VT requirements. Confirm with the design team before specifying glass make-up.</li>
        <li>Egress: Operable windows on egress paths must comply with FBC Chapter 10 minimum sill height, clear opening dimensions, and operating force criteria. Spec the egress-compliant configuration where applicable.</li>
        <li>Cycle life: AAMA 920 is the baseline cycle-life test for operable sash. Multifamily and hospitality occupancies frequently exceed typical residential cycle counts within 3 years &mdash; specify the manufacturer&rsquo;s commercial cycle-test data.</li>
      </ul>
      <h3 style="font-size:14px;color:#fff;margin:20px 0 8px;">Common pitfalls we see</h3>
      <ul style="margin:0 0 12px;padding-left:20px;line-height:1.7;">
        <li>Specifying a window series without specifying the FL PA configuration. Manufacturers&rsquo; FL PA numbers cover specific frame depth, glass make-up, and anchor pattern combinations &mdash; not the entire series.</li>
        <li>Glass make-up under-specified: &lsquo;1-inch insulating with low-E&rsquo; is ambiguous. Specify glass thickness, low-E coating type and surface position, gas fill, spacer type, and laminated interlayer where required.</li>
        <li>Anchor calculation: many bidders submit generic anchor schedules. Require project-specific calculations sealed by a Florida-licensed PE.</li>
        <li>Weep system: aluminum windows are pressure-equalized. Blocked or painted-over weeps trap water; specify weep inspection at substantial completion.</li>
      </ul>
      <h3 style="font-size:14px;color:#fff;margin:20px 0 8px;">Submittal review checklist</h3>
      <ul style="margin:0 0 12px;padding-left:20px;line-height:1.7;">
        <li>Confirm window types, sizes, and quantities match the approved schedule.</li>
        <li>Verify FL PA / NOA configuration matches the project glass make-up and anchor pattern.</li>
        <li>Confirm thermal performance package includes NFRC-certified U-factor, SHGC, VT, and condensation resistance.</li>
        <li>Confirm structural calculation is sealed by a Florida-licensed engineer.</li>
        <li>Confirm operable sash hardware is commercial-grade with documented cycle-life data.</li>
      </ul>
      <p style="margin:20px 0 0;font-size:13px;color:rgba(255,255,255,0.6);">Questions on system selection? Email <a href="mailto:specs@acglass.com" style="color:#e11320;">specs@acglass.com</a>.</p>
    </aside>
'''

final_html = head + pre_section + augment + notes_sidebar + footer
new_path.write_text(final_html)
print(f"WROTE: {new_path}")

# Word count audit
import re
c2 = re.sub(r'<script[^>]*>.*?</script>', '', final_html, flags=re.DOTALL)
c2 = re.sub(r'<style[^>]*>.*?</style>', '', c2, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', c2)
text = re.sub(r'\s+', ' ', text).strip()
print(f"Words: {len(text.split())}")
