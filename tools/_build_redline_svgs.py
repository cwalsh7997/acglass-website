#!/usr/bin/env python3
"""Generate invented-typical shop-drawing SVGs for the redline clinic.

These figures are teaching diagrams for one typical 5 ft x 7 ft SF-1 lite.
They are not a project drawing. Paper #fbf7f0. Redline #b42318.
"""

from __future__ import annotations

from pathlib import Path

PAPER = "#fbf7f0"
RED = "#b42318"
INK = "#1c1916"
NAVY = "#0e284f"
MUTED = "#6b6258"
GRID = "#d8cfc2"
GLASS = "#c5d8e6"
LAM = "#7ea8c4"
MONO = "#d7e4ee"
ALUM = "#b8b2a8"
OUT = Path(__file__).resolve().parents[1] / "blog" / "images" / "redline-clinic"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg(w: int, h: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img">\n'
        f'<rect width="{w}" height="{h}" fill="{PAPER}"/>\n'
        f"{body}\n</svg>\n"
    )


def title_block(w: int, h: int, sheet: str, title: str) -> str:
    y = h - 46
    return f"""
<rect x="16" y="12" width="{w - 32}" height="28" fill="none" stroke="{NAVY}" stroke-width="1.2"/>
<text x="28" y="31" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{NAVY}">{esc(sheet)}</text>
<text x="{w - 28}" y="31" text-anchor="end" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{RED}">TYPICAL 5x7 SF-1 · NOT A PROJECT DRAWING</text>
<rect x="16" y="{y}" width="{w - 32}" height="30" fill="none" stroke="{NAVY}" stroke-width="1.2"/>
<text x="28" y="{y + 20}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{NAVY}">ACG REDLINE CLINIC</text>
<text x="{w / 2}" y="{y + 20}" text-anchor="middle" font-family="Georgia, Times, serif" font-size="13" fill="{INK}">{esc(title)}</text>
<text x="{w - 28}" y="{y + 20}" text-anchor="end" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{MUTED}">INVENTED TYPICAL LITE</text>
"""


def cloud(cx: float, cy: float, rw: float, rh: float, label: str) -> str:
    return f"""
<ellipse cx="{cx}" cy="{cy}" rx="{rw}" ry="{rh}" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 3"/>
<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="10" fill="{RED}">{esc(label)}</text>
"""


def panel_box(x: float, y: float, w: float, h: float, n: str, title: str, body: str) -> str:
    return f"""
<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fffdf8" stroke="{NAVY}" stroke-width="1"/>
<rect x="{x}" y="{y}" width="28" height="22" fill="{RED}"/>
<text x="{x + 14}" y="{y + 16}" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="#fff">{esc(n)}</text>
<text x="{x + 38}" y="{y + 16}" font-family="Georgia, Times, serif" font-size="13" fill="{NAVY}">{esc(title)}</text>
<text x="{x + 14}" y="{y + 48}" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="12" fill="{INK}">{esc(body)}</text>
"""


def fig_00() -> str:
    cards = [
        ("01", "IGU makeup", "Florida impact often laminates outboard. UFC 5-11.1 laminates the inboard lite."),
        ("02", "Bite", "Silicone: larger of 3/8 in or glass thickness. Tape: 2x laminated-glass thickness."),
        ("03", "Vestibule", "UFC 5-11.2 pulls vestibules and stairs into the same fragment-reduction rule."),
        ("04", "Replacement", "UFC 5-1.1.2.1: window replacement on an inhabited DoD building still triggers 5-11."),
    ]
    parts = [title_block(1200, 420, "FIG 00", "Four redlines on one typical 5x7 storefront lite")]
    for i, (n, title, body) in enumerate(cards):
        x = 24 + i * 292
        parts.append(panel_box(x, 56, 280, 300, n, title, ""))
        # wrap body manually
        words = body.split()
        line = ""
        y = 96
        for word in words:
            trial = (line + " " + word).strip()
            if len(trial) > 28:
                parts.append(
                    f'<text x="{x + 16}" y="{y}" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{INK}">{esc(line)}</text>'
                )
                line = word
                y += 20
            else:
                line = trial
        if line:
            parts.append(
                f'<text x="{x + 16}" y="{y}" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{INK}">{esc(line)}</text>'
            )
        parts.append(
            f'<rect x="{x + 16}" y="250" width="248" height="88" fill="{PAPER}" stroke="{GRID}"/>'
        )
        if n == "01":
            parts.append(f'<rect x="{x + 36}" y="262" width="18" height="64" fill="{LAM}"/>')
            parts.append(f'<rect x="{x + 58}" y="262" width="10" height="64" fill="#e8f2f8"/>')
            parts.append(f'<rect x="{x + 72}" y="262" width="18" height="64" fill="{MONO}"/>')
            parts.append(
                f'<text x="{x + 100}" y="288" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{RED}">WRONG: outboard lam</text>'
            )
            parts.append(
                f'<text x="{x + 100}" y="308" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{NAVY}">UFC wants inboard lam</text>'
            )
        elif n == "02":
            parts.append(f'<rect x="{x + 36}" y="268" width="70" height="52" fill="{ALUM}"/>')
            parts.append(f'<rect x="{x + 56}" y="278" width="36" height="32" fill="{GLASS}"/>')
            parts.append(
                f'<path d="M{x + 56} 294 H{x + 40}" stroke="{RED}" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{x + 116}" y="292" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{RED}">bite + bead</text>'
            )
            parts.append(
                f'<text x="{x + 116}" y="312" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{NAVY}">tape = 2x thickness</text>'
            )
        elif n == "03":
            parts.append(f'<rect x="{x + 40}" y="266" width="50" height="56" fill="none" stroke="{NAVY}"/>')
            parts.append(f'<rect x="{x + 90}" y="278" width="36" height="32" fill="none" stroke="{NAVY}"/>')
            parts.append(cloud(x + 65, 294, 42, 28, "5-11.2"))
        else:
            parts.append(
                f'<text x="{x + 28}" y="284" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">inhabited DoD</text>'
            )
            parts.append(
                f'<text x="{x + 28}" y="304" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">+ replace windows</text>'
            )
            parts.append(
                f'<text x="{x + 28}" y="324" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{RED}">= 5-11, not 50% reno</text>'
            )
    return svg(1200, 420, "\n".join(parts))


def fig_01() -> str:
    parts = [title_block(820, 1040, "FIG 01", "Opening elevation · typical SF-1")]
    # frame
    parts.append(f'<rect x="210" y="90" width="360" height="504" fill="{ALUM}" stroke="{NAVY}" stroke-width="2"/>')
    parts.append(f'<rect x="232" y="112" width="316" height="460" fill="{GLASS}" stroke="{NAVY}" stroke-width="1.2"/>')
    # dims
    parts.append(f'<path d="M210 80 H570" stroke="{INK}" stroke-width="1"/>')
    parts.append(f'<text x="390" y="74" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">5\'-0"</text>')
    parts.append(f'<path d="M190 90 V594" stroke="{INK}" stroke-width="1"/>')
    parts.append(f'<text x="178" y="360" text-anchor="end" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">7\'-0"</text>')
    parts.append(
        f'<text x="390" y="350" text-anchor="middle" font-family="Georgia, Times, serif" font-size="20" fill="{NAVY}">SF-1</text>'
    )
    parts.append(
        f'<text x="390" y="372" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{MUTED}">TYP. STOREFRONT LITE</text>'
    )
    # redline clouds
    parts.append(cloud(390, 170, 118, 36, "1  IGU MAKEUP"))
    parts.append(cloud(560, 320, 92, 34, "2  BITE"))
    parts.append(cloud(300, 480, 110, 34, "3  VESTIBULE?"))
    parts.append(cloud(500, 560, 118, 32, "4  REPLACEMENT"))
    # notes
    notes = [
        "REDLINE SET (INVENTED TYPICAL, NOT A JOB)",
        "1  Confirm inboard lite is laminated or PC. A Florida",
        "   impact IGU that laminates outboard is not 5-11.1.",
        "2  Show silicone bite (larger of 3/8 in or glass",
        "   thickness) or tape bite = 2x laminated thickness.",
        "3  If this lite sits in a vestibule or stair, 5-11.2",
        "   still applies. Do not mark it interior-unprotected.",
        "4  Window replacement on an inhabited DoD building",
        "   triggers 5-11 under 5-1.1.2.1. Not a 50% trigger.",
        "Do not invent an NOA ID, design pressure, U-factor,",
        "or SHGC on this sheet. Those stay project-specific.",
    ]
    y = 640
    for line in notes:
        fill = RED if line.startswith("REDLINE") else INK
        parts.append(
            f'<text x="40" y="{y}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="{fill}">{esc(line)}</text>'
        )
        y += 20
    return svg(820, 1040, "\n".join(parts))


def igu_stack(x: float, y: float, out_fill: str, in_fill: str, out_lab: str, in_lab: str) -> str:
    return f"""
<rect x="{x}" y="{y}" width="70" height="220" fill="{ALUM}" stroke="{NAVY}"/>
<rect x="{x + 10}" y="{y + 10}" width="18" height="200" fill="{out_fill}" stroke="{INK}"/>
<rect x="{x + 30}" y="{y + 10}" width="10" height="200" fill="#eef6fb" stroke="{GRID}"/>
<rect x="{x + 42}" y="{y + 10}" width="18" height="200" fill="{in_fill}" stroke="{INK}"/>
<text x="{x + 19}" y="{y + 248}" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{INK}">{esc(out_lab)}</text>
<text x="{x + 51}" y="{y + 248}" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{INK}">{esc(in_lab)}</text>
<text x="{x - 8}" y="{y + 20}" text-anchor="end" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="10" fill="{MUTED}">WEATHER</text>
<text x="{x + 86}" y="{y + 20}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="10" fill="{MUTED}">ROOM</text>
"""


def fig_02() -> str:
    parts = [title_block(1100, 620, "FIG 02", "Outboard NOA laminate vs UFC 5-11.1 inboard laminate")]
    parts.append(
        f'<text x="80" y="78" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">Florida wind / impact makeup (typical pattern)</text>'
    )
    parts.append(
        f'<text x="600" y="78" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">UFC 4-010-01 Section 5-11.1 floor</text>'
    )
    parts.append(igu_stack(160, 110, LAM, MONO, "LAM", "MONO"))
    parts.append(igu_stack(700, 110, MONO, LAM, "MONO", "LAM / PC"))
    parts.append(cloud(195, 200, 70, 40, "OUTBOARD"))
    parts.append(cloud(751, 220, 70, 40, "INBOARD"))
    parts.append(
        f'<text x="80" y="400" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="14" fill="{INK}">A Miami-Dade NOA or Florida Product Approval is wind and impact. It does not prove the inboard lite is laminated.</text>'
    )
    parts.append(
        f'<text x="80" y="424" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="14" fill="{INK}">UFC 5-11.1: min. 1/4 in laminated or polycarbonate, or two 1/8 in plies with 0.030 in PVB. On an IGU the innermost lite must be laminated or PC.</text>'
    )
    parts.append(
        f'<text x="80" y="456" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="{RED}">REDLINE: do not shop an outboard-laminate impact IGU and call the UFC side done.</text>'
    )
    parts.append(
        f'<text x="80" y="488" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{MUTED}">No NOA ID, psi, U-factor, or SHGC on this figure. Those values stay on the project schedule.</text>'
    )
    return svg(1100, 620, "\n".join(parts))


def fig_03() -> str:
    parts = [title_block(1100, 640, "FIG 03", "Silicone bite vs structural tape bite")]
    # silicone
    parts.append(f'<rect x="90" y="80" width="420" height="360" fill="#fffdf8" stroke="{NAVY}"/>')
    parts.append(
        f'<text x="110" y="108" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">Silicone (5-11.1)</text>'
    )
    parts.append(f'<rect x="140" y="140" width="80" height="220" fill="{ALUM}" stroke="{NAVY}"/>')
    parts.append(f'<rect x="220" y="160" width="36" height="180" fill="{LAM}" stroke="{INK}"/>')
    parts.append(f'<rect x="208" y="160" width="12" height="180" fill="{RED}" opacity="0.35"/>')
    parts.append(
        f'<path d="M208 250 H170" stroke="{RED}" stroke-width="1.4"/>'
    )
    parts.append(
        f'<text x="250" y="200" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">bite = larger of</text>'
    )
    parts.append(
        f'<text x="250" y="220" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{RED}">3/8 in or glass thk</text>'
    )
    parts.append(
        f'<text x="250" y="248" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">bead 3/16 in min.</text>'
    )
    parts.append(
        f'<text x="110" y="400" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{INK}">On a 1/4 in laminated lite the silicone bite floor is 3/8 in.</text>'
    )
    # tape
    parts.append(f'<rect x="560" y="80" width="460" height="360" fill="#fffdf8" stroke="{NAVY}"/>')
    parts.append(
        f'<text x="580" y="108" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">Structural tape (5-11.1)</text>'
    )
    parts.append(f'<rect x="610" y="140" width="80" height="220" fill="{ALUM}" stroke="{NAVY}"/>')
    parts.append(f'<rect x="690" y="160" width="36" height="180" fill="{LAM}" stroke="{INK}"/>')
    parts.append(f'<rect x="678" y="160" width="12" height="180" fill="{RED}"/>')
    parts.append(
        f'<text x="740" y="200" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">tape bite =</text>'
    )
    parts.append(
        f'<text x="740" y="220" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{RED}">2x laminated-glass thk</text>'
    )
    parts.append(
        f'<text x="740" y="248" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{INK}">UFC 4-010-01 §5-11.1</text>'
    )
    parts.append(
        f'<text x="580" y="400" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{INK}">On a 1/4 in laminated lite the tape bite floor is 1/2 in.</text>'
    )
    parts.append(
        f'<text x="90" y="480" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="14" fill="{INK}">Bite applies on both sides of a single pane and on the inboard lite only of an IGU. A laminate without the specified bite is incomplete.</text>'
    )
    parts.append(
        f'<text x="90" y="508" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="{RED}">REDLINE: shops that omit bite fail 5-11.1 even if the word laminated appears.</text>'
    )
    return svg(1100, 640, "\n".join(parts))


def fig_04() -> str:
    parts = [title_block(1100, 700, "FIG 04", "Vestibule and stair · UFC 4-010-01 §5-11.2")]
    # plan
    parts.append(f'<rect x="60" y="70" width="480" height="420" fill="#fffdf8" stroke="{NAVY}"/>')
    parts.append(
        f'<text x="80" y="96" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">Typical vestibule plan (invented)</text>'
    )
    parts.append(f'<rect x="120" y="140" width="360" height="280" fill="none" stroke="{NAVY}" stroke-width="2"/>')
    parts.append(f'<rect x="200" y="140" width="200" height="12" fill="{GLASS}" stroke="{NAVY}"/>')
    parts.append(f'<rect x="200" y="408" width="200" height="12" fill="{GLASS}" stroke="{NAVY}"/>')
    parts.append(f'<rect x="120" y="220" width="12" height="120" fill="{GLASS}" stroke="{NAVY}"/>')
    parts.append(f'<rect x="468" y="220" width="12" height="120" fill="{GLASS}" stroke="{NAVY}"/>')
    parts.append(cloud(300, 146, 90, 28, "ENTRY LITE"))
    parts.append(cloud(474, 280, 70, 28, "SIDE LITE"))
    parts.append(
        f'<text x="300" y="300" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{MUTED}">VESTIBULE</text>'
    )
    # stair
    parts.append(f'<rect x="580" y="70" width="460" height="420" fill="#fffdf8" stroke="{NAVY}"/>')
    parts.append(
        f'<text x="600" y="96" font-family="Georgia, Times, serif" font-size="16" fill="{NAVY}">Typical stair borrowed lite</text>'
    )
    for i in range(6):
        y = 160 + i * 36
        parts.append(f'<rect x="640" y="{y}" width="220" height="28" fill="none" stroke="{NAVY}"/>')
    parts.append(f'<rect x="880" y="160" width="18" height="216" fill="{GLASS}" stroke="{NAVY}"/>')
    parts.append(cloud(889, 250, 56, 40, "STAIR"))
    parts.append(
        f'<text x="80" y="530" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="14" fill="{INK}">Section 5-11.2 pulls vestibules and stairs into the same fragment-reduction rule as 5-11.1. Do not price those openings as unprotected interior glass.</text>'
    )
    parts.append(
        f'<text x="80" y="556" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13" fill="{RED}">REDLINE: calling a vestibule or stair lite "interior" does not drop 5-11.</text>'
    )
    parts.append(
        f'<text x="80" y="580" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{MUTED}">Doors are 5-12.1. Confirm opening type before you exclude it.</text>'
    )
    return svg(1100, 700, "\n".join(parts))


def fig_05() -> str:
    parts = [title_block(1100, 640, "FIG 05", "Replacement trigger · UFC 4-010-01 §5-1.1.2.1")]
    boxes = [
        (80, 90, "INHABITED DoD BUILDING", "Occupancy, not county. On-post is UFC."),
        (420, 90, "WINDOW REPLACEMENT", "Any replacement package. Six openings is enough."),
        (760, 90, "SECTION 5-11 APPLIES", "Laminated inboard glass and specified bite."),
    ]
    for i, (x, y, t, s) in enumerate(boxes):
        parts.append(f'<rect x="{x}" y="{y}" width="260" height="150" fill="#fffdf8" stroke="{NAVY}"/>')
        parts.append(
            f'<text x="{x + 16}" y="{y + 36}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="{RED}">{esc(t)}</text>'
        )
        parts.append(
            f'<text x="{x + 16}" y="{y + 70}" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="13" fill="{INK}">{esc(s)}</text>'
        )
        if i < 2:
            parts.append(
                f'<path d="{x + 260} {y + 75} L{x + 332} {y + 75}" stroke="{RED}" stroke-width="2" marker-end="url(#arr)"/>'
            )
    parts.append(
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L8,3 L0,6 Z" fill="{RED}"/></marker></defs>'
    )
    parts.append(f'<rect x="80" y="280" width="940" height="220" fill="#fffdf8" stroke="{RED}" stroke-width="1.4"/>')
    lines = [
        "Not the 50 percent renovation trigger. A small package on an occupied admin building is enough.",
        "Supplemental interior windows and new openings are included. A borrowed lite or a new punched opening is 5-11 work.",
        "Film is not a substitute (5-11.4). ASTM F1642 / F2912 / F2248 apply only when the spec cites them.",
        "Florida path still sits next to this: NOA in HVHZ, Florida Product Approval elsewhere. Two proofs, one assembly.",
    ]
    y = 314
    for line in lines:
        parts.append(
            f'<text x="100" y="{y}" font-family="ui-sans-serif, Helvetica, Arial, sans-serif" font-size="14" fill="{INK}">{esc(line)}</text>'
        )
        y += 42
    return svg(1100, 640, "\n".join(parts))


FIGURES = {
    "fig-00-redline-sequence.svg": fig_00,
    "fig-01-opening-elevation.svg": fig_01,
    "fig-02-igu-outboard-vs-inboard.svg": fig_02,
    "fig-03-bite-silicone-vs-tape.svg": fig_03,
    "fig-04-vestibule-stair.svg": fig_04,
    "fig-05-replacement-trigger.svg": fig_05,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        path = OUT / name
        path.write_text(fn(), encoding="utf-8")
        print(f"wrote {path.relative_to(OUT.parent.parent.parent)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
