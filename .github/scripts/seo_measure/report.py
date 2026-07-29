"""Render the analysis payload as Markdown plus companion CSVs."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .analyze import pct_change

BAND_LABELS = {
    "page1": "Page 1",
    "page2": "Page 2",
    "page3": "Page 3",
    "beyond": "Page 4+",
    "unranked": "No impressions",
}


def fmt_int(value) -> str:
    return "-" if value is None else f"{int(value):,}"


def fmt_pct(value, digits: int = 1) -> str:
    """Format a ratio (0.034) as a percentage string."""
    return "-" if value is None else f"{value * 100:.{digits}f}%"


def fmt_delta_pct(value, digits: int = 1) -> str:
    """Format an already-percentage delta with an explicit sign."""
    return "n/a" if value is None else f"{value:+.{digits}f}%"


def fmt_pos(value) -> str:
    return "-" if value is None else f"{value:.1f}"


def fmt_gain(value) -> str:
    """Position gain, signed so that + always means 'moved toward #1'."""
    if value is None:
        return "n/a"
    return f"{value:+.1f}"


def fmt_signed(value) -> str:
    return "n/a" if value is None else f"{value:+,}"


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["_No rows._", ""]
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(r) + " |" for r in rows)
    out.append("")
    return out


def _movement_rows(comparisons, limit: int) -> list[list[str]]:
    return [
        [
            c.display,
            c.group_label,
            BAND_LABELS[c.band_prior],
            BAND_LABELS[c.band_current],
            fmt_pos(c.prior.position),
            fmt_pos(c.current.position),
            fmt_gain(c.position_gain),
            fmt_int(c.current.impressions),
            fmt_signed(c.clicks_delta),
        ]
        for c in comparisons[:limit]
    ]


_MOVEMENT_HEADERS = [
    "Query",
    "Group",
    "Prior band",
    "Current band",
    "Prior pos",
    "Current pos",
    "Pos gain",
    "Impr",
    "Clicks delta",
]


def render_markdown(analysis: dict, generated_on: str | None = None) -> str:
    cfg = analysis["config"]
    cur = analysis["current"]
    pri = analysis["prior"]
    tc = analysis["totals_current"]
    tp = analysis["totals_prior"]
    movement = analysis["movement"]
    manual = analysis["manual"]
    top_n = cfg.report.top_n_movers
    generated_on = generated_on or date.today().isoformat()

    L: list[str] = []
    L.append(f"# ACG SEO Weekly Report - {cur.date_range}")
    L.append("")
    L.append(f"- **Property:** `{cfg.gsc_property}`")
    L.append(f"- **Current period:** {cur.date_range} ({len(cur.rows):,} rows)")
    L.append(f"- **Prior period:** {pri.date_range} ({len(pri.rows):,} rows)")
    L.append(f"- **Dimensions:** {', '.join(cur.dimensions) or 'none'}")
    L.append(f"- **Generated:** {generated_on}")
    L.append(
        f"- **Targets tracked:** {len(cfg.queries)} queries, "
        f"{len(cfg.pages)} pages, {len(cfg.markets)} markets"
    )
    L.append("")
    L.append(
        "_All figures come from first-party Search Console exports. Surfaces "
        "without an API are listed under Data Gaps and are never estimated._"
    )
    L.append("")

    L.append("## 1. Totals")
    L.append("")
    L.extend(
        _table(
            ["Metric", "Current", "Prior", "Change"],
            [
                [
                    "Clicks",
                    fmt_int(tc["clicks"]),
                    fmt_int(tp["clicks"]),
                    fmt_delta_pct(pct_change(tc["clicks"], tp["clicks"])),
                ],
                [
                    "Impressions",
                    fmt_int(tc["impressions"]),
                    fmt_int(tp["impressions"]),
                    fmt_delta_pct(pct_change(tc["impressions"], tp["impressions"])),
                ],
                [
                    "CTR",
                    fmt_pct(tc["ctr"], 2),
                    fmt_pct(tp["ctr"], 2),
                    fmt_delta_pct(pct_change(tc["ctr"], tp["ctr"])),
                ],
                [
                    "Avg position",
                    fmt_pos(tc["position"]),
                    fmt_pos(tp["position"]),
                    fmt_gain(
                        (tp["position"] - tc["position"])
                        if tc["position"] is not None and tp["position"] is not None
                        else None
                    ),
                ],
            ],
        )
    )
    L.append(
        f"_Avg position is impression-weighted. A positive change means movement "
        f"toward position 1._"
    )
    L.append("")

    L.append("## 2. Page-1 / page-3 movement")
    L.append("")
    counts = movement.counts
    L.extend(
        _table(
            ["Transition", "Queries"],
            [
                ["Entered page 1", str(counts["entered_page1"])],
                ["Dropped off page 1", str(counts["left_page1"])],
                ["Entered top 30 (page 1-3)", str(counts["entered_top30"])],
                ["Dropped out of top 30", str(counts["left_top30"])],
                ["Improved >= threshold", str(counts["improved"])],
                ["Declined >= threshold", str(counts["declined"])],
                ["In striking distance (page 2-3)", str(counts["striking_distance"])],
            ],
        )
    )
    L.append("**Band distribution**")
    L.append("")
    L.extend(
        _table(
            ["Band", "Current", "Prior"],
            [
                [
                    BAND_LABELS[band],
                    str(movement.band_current.get(band, 0)),
                    str(movement.band_prior.get(band, 0)),
                ]
                for band in ("page1", "page2", "page3", "beyond", "unranked")
            ],
        )
    )
    if movement.suppressed_low_volume:
        L.append(
            f"_{movement.suppressed_low_volume} target queries were held out of the "
            f"movement lists for falling under the "
            f"{cfg.thresholds.movement_min_impressions}-impression floor in both "
            f"periods._"
        )
        L.append("")

    L.append("### 2a. Entered page 1")
    L.append("")
    L.extend(_table(_MOVEMENT_HEADERS, _movement_rows(movement.entered_page1, top_n)))
    L.append("### 2b. Dropped off page 1")
    L.append("")
    L.extend(_table(_MOVEMENT_HEADERS, _movement_rows(movement.left_page1, top_n)))
    L.append("### 2c. Striking distance (page 2-3, best page-1 candidates)")
    L.append("")
    L.extend(
        _table(_MOVEMENT_HEADERS, _movement_rows(movement.striking_distance, top_n))
    )
    L.append("### 2d. Largest declines")
    L.append("")
    L.extend(_table(_MOVEMENT_HEADERS, _movement_rows(movement.declined, top_n)))

    L.append("## 3. Target query groups")
    L.append("")
    L.extend(
        _table(
            [
                "Group",
                "Queries",
                "With impressions",
                "On page 1",
                "Clicks",
                "Clicks change",
                "Impressions",
                "Impr change",
                "Avg pos",
            ],
            [
                [
                    g["label"],
                    str(g["queries"]),
                    str(g["ranking"]),
                    str(g["page1"]),
                    fmt_int(g["clicks"]),
                    fmt_delta_pct(g["clicks_pct"]),
                    fmt_int(g["impressions"]),
                    fmt_delta_pct(g["impressions_pct"]),
                    fmt_pos(g["avg_position"]),
                ]
                for g in analysis["groups"]
            ],
        )
    )

    L.append("## 4. Cannibalization")
    L.append("")
    cannibal = analysis["cannibalization"]
    t = cfg.thresholds
    L.append(
        f"_A query is flagged when {t.cann_min_urls}+ ACG URLs each hold at least "
        f"{t.cann_min_impressions_per_url} impressions and at least "
        f"{t.cann_min_impression_share:.0%} of that query's impressions. Shares are "
        f"of the whole query, so they sum to under 100% when other URLs draw "
        f"impressions below those floors._"
    )
    L.append("")
    L.append(
        f"_Severity weights rank: HIGH is {t.cann_high_page1_urls}+ URLs on page 1, "
        f"or a runner-up holding {t.cann_high_min_share:.0%}+ share while still "
        f"within position {t.page2_max_position:.0f}. An even split beyond position "
        f"{t.page3_max_position:.0f} is LOW - consolidating it wins nothing._"
    )
    L.append("")
    if not cannibal:
        L.append(
            "_No queries above threshold._"
            if cur.has_page_dimension and cur.has_query_dimension
            else "_Not computable: the current export lacks a query+page dimension pair._"
        )
        L.append("")
    else:
        L.extend(
            _table(
                ["Severity", "Query", "URLs", "Impressions", "Clicks", "Top URL", "Top share"],
                [
                    [
                        f.severity.upper(),
                        f.query,
                        str(f.url_count),
                        fmt_int(f.total_impressions),
                        fmt_int(f.total_clicks),
                        f"`{f.primary['page']}`" if f.primary else "-",
                        fmt_pct(f.primary["share"]) if f.primary else "-",
                    ]
                    for f in cannibal
                ],
            )
        )
        L.append("**Competing URLs by query**")
        L.append("")
        for f in cannibal:
            L.append(f"- **{f.query}** ({f.severity})")
            for u in f.urls:
                L.append(
                    f"  - `{u['page']}` - {fmt_int(u['impressions'])} impr "
                    f"({fmt_pct(u['share'])}), {fmt_int(u['clicks'])} clicks, "
                    f"pos {fmt_pos(u['position'])} ({BAND_LABELS[u['band']]})"
                )
        L.append("")

    L.append("## 5. Priority pages")
    L.append("")
    L.extend(
        _table(
            [
                "Page",
                "Path",
                "Role",
                "Clicks",
                "Clicks change",
                "Impressions",
                "Impr change",
                "Avg pos",
                "Pos gain",
            ],
            [
                [
                    c.display,
                    f"`{c.key}`",
                    c.group_label,
                    fmt_int(c.current.clicks),
                    fmt_delta_pct(c.clicks_pct),
                    fmt_int(c.current.impressions),
                    fmt_delta_pct(c.impressions_pct),
                    fmt_pos(c.current.position),
                    fmt_gain(c.position_gain),
                ]
                for c in analysis["pages"][: cfg.report.top_n_pages]
            ],
        )
    )

    L.append("## 6. Local, map, AI and Bing surfaces")
    L.append("")
    if manual["file_missing"]:
        L.append(
            f"_No manual metrics file at `{manual['file_missing']}`. "
            f"Every surface below is unreported._"
        )
        L.append("")
    else:
        L.append(
            f"_As of {manual['as_of'] or 'never'}. "
            f"{manual['supplied_count']} supplied, {manual['missing_count']} not supplied._"
        )
        if manual["stale"]:
            L.append("")
            L.append(
                f"> **Stale:** manual metrics were last refreshed {manual['as_of']}, "
                f"before the end of the reporting period ({cur.end}). Refresh before "
                f"acting on this section."
            )
        L.append("")
    for section in manual["sections"]:
        L.append(f"### {section['label']}")
        L.append("")
        L.append(f"- Source: {section['source']}")
        L.append(f"- Input: `{section['input_method']}`" + (
            f" via `{section['connector_id']}`" if section["connector_id"] else ""
        ))
        L.append("")
        L.extend(
            _table(
                ["Metric", "Scope", "Value", "Unit", "Target", "Input"],
                [
                    [
                        m["label"],
                        m["scope"] or "-",
                        str(m["value"]) if m["supplied"] else "_not supplied_",
                        m["unit"] or "-",
                        m["target"] or "-",
                        f"`{m['input_method']}`",
                    ]
                    for m in section["metrics"]
                ],
            )
        )

    L.append("## 7. Data gaps")
    L.append("")
    for note in analysis["notes"]:
        L.append(f"- {note}")
    if manual["gaps"]:
        L.append(
            f"- {len(manual['gaps'])} manual/connector metrics were not supplied "
            f"for this period:"
        )
        by_section: dict[str, list[str]] = {}
        for g in manual["gaps"]:
            label = f"{g['metric']}" + (f" ({g['scope']})" if g["scope"] else "")
            by_section.setdefault(g["section"], []).append(label)
        for section_label, items in by_section.items():
            L.append(f"  - **{section_label}**: {', '.join(items)}")
    if not analysis["notes"] and not manual["gaps"]:
        L.append("- None.")
    L.append("")
    L.append("---")
    L.append("")
    L.append(
        f"Targets: `{_display_path(cfg.source_path)}` "
        f"· Runbook: `.github/scripts/seo_measure/README.md`"
    )
    L.append("")
    return "\n".join(L)


def _display_path(path: Path | None) -> str:
    """Repo-relative when possible, absolute otherwise.

    --config may legitimately point outside the repo, and relative_to() raises
    rather than returning the absolute path in that case.
    """
    if path is None:
        return "seo-targets.json"
    root = Path(__file__).resolve().parents[3]
    try:
        return str(Path(path).resolve().relative_to(root))
    except ValueError:
        return str(path)


def _write_csv(path: Path, headers: list[str], rows: list[list]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)
    return path


def write_csvs(analysis: dict, out_dir) -> list[Path]:
    """Emit the machine-readable companions to the Markdown report."""
    out_dir = Path(out_dir)
    written = []

    written.append(
        _write_csv(
            out_dir / "queries.csv",
            [
                "query", "group", "market",
                "clicks", "prior_clicks", "clicks_delta", "clicks_pct",
                "impressions", "prior_impressions", "impressions_delta", "impressions_pct",
                "ctr", "prior_ctr",
                "position", "prior_position", "position_gain",
                "band", "prior_band", "transition",
            ],
            [
                [
                    c.display, c.group_id, c.market or "",
                    c.current.clicks, c.prior.clicks, c.clicks_delta,
                    _round(c.clicks_pct),
                    c.current.impressions, c.prior.impressions, c.impressions_delta,
                    _round(c.impressions_pct),
                    _round(c.current.ctr, 6), _round(c.prior.ctr, 6),
                    _round(c.current.position), _round(c.prior.position),
                    _round(c.position_gain),
                    c.band_current, c.band_prior, c.transition,
                ]
                for c in analysis["queries"]
            ],
        )
    )

    written.append(
        _write_csv(
            out_dir / "pages.csv",
            [
                "page", "label", "role", "market",
                "clicks", "prior_clicks", "clicks_pct",
                "impressions", "prior_impressions", "impressions_pct",
                "position", "prior_position", "position_gain", "band",
            ],
            [
                [
                    c.key, c.display, c.group_id, c.market or "",
                    c.current.clicks, c.prior.clicks, _round(c.clicks_pct),
                    c.current.impressions, c.prior.impressions, _round(c.impressions_pct),
                    _round(c.current.position), _round(c.prior.position),
                    _round(c.position_gain), c.band_current,
                ]
                for c in analysis["pages"]
            ],
        )
    )

    written.append(
        _write_csv(
            out_dir / "cannibalization.csv",
            [
                "query", "severity", "url_count", "page",
                "impressions", "clicks", "impression_share", "position", "band",
            ],
            [
                [
                    f.query, f.severity, f.url_count, u["page"],
                    u["impressions"], u["clicks"], _round(u["share"], 4),
                    _round(u["position"]), u["band"],
                ]
                for f in analysis["cannibalization"]
                for u in f.urls
            ],
        )
    )

    movement = analysis["movement"]
    movement_rows = []
    for bucket, items in (
        ("entered_page1", movement.entered_page1),
        ("left_page1", movement.left_page1),
        ("entered_top30", movement.entered_top30),
        ("left_top30", movement.left_top30),
        ("striking_distance", movement.striking_distance),
        ("improved", movement.improved),
        ("declined", movement.declined),
    ):
        for c in items:
            movement_rows.append(
                [
                    bucket, c.display, c.group_id,
                    c.band_prior, c.band_current,
                    _round(c.prior.position), _round(c.current.position),
                    _round(c.position_gain),
                    c.current.impressions, c.clicks_delta,
                ]
            )
    written.append(
        _write_csv(
            out_dir / "movement.csv",
            [
                "bucket", "query", "group", "prior_band", "current_band",
                "prior_position", "current_position", "position_gain",
                "impressions", "clicks_delta",
            ],
            movement_rows,
        )
    )

    manual = analysis["manual"]
    written.append(
        _write_csv(
            out_dir / "manual-metrics.csv",
            ["section", "metric", "scope", "value", "unit", "input_method", "supplied"],
            [
                [
                    s["label"], m["label"], m["scope"],
                    "" if m["value"] is None else m["value"],
                    m["unit"], m["input_method"], "yes" if m["supplied"] else "no",
                ]
                for s in manual["sections"]
                for m in s["metrics"]
            ],
        )
    )
    return written


def _round(value, digits: int = 2):
    return "" if value is None else round(value, digits)
