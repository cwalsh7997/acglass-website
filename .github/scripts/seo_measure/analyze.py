"""Period comparison, cannibalization detection, and page-band movement."""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import TargetConfig, Thresholds
from .ingest import Period, Row, aggregate


@dataclass
class Stat:
    """Rolled-up metrics for one entity (a query or a page) in one period."""

    clicks: int = 0
    impressions: int = 0
    ctr: float = 0.0
    position: float | None = None
    present: bool = False

    @classmethod
    def from_rows(cls, rows) -> "Stat":
        if not rows:
            return cls()
        agg = aggregate(rows)
        return cls(
            clicks=int(agg["clicks"]),
            impressions=int(agg["impressions"]),
            ctr=agg["ctr"],
            position=agg["position"],
            present=True,
        )


@dataclass
class Comparison:
    """One entity's current-vs-prior movement."""

    key: str
    display: str
    current: Stat
    prior: Stat
    group_id: str = ""
    group_label: str = ""
    market: str | None = None
    band_current: str = "unranked"
    band_prior: str = "unranked"
    transition: str = "flat"

    @property
    def clicks_delta(self) -> int:
        return self.current.clicks - self.prior.clicks

    @property
    def impressions_delta(self) -> int:
        return self.current.impressions - self.prior.impressions

    @property
    def clicks_pct(self) -> float | None:
        return pct_change(self.current.clicks, self.prior.clicks)

    @property
    def impressions_pct(self) -> float | None:
        return pct_change(self.current.impressions, self.prior.impressions)

    @property
    def position_gain(self) -> float | None:
        """Positive means the average position improved (moved toward 1)."""
        if self.current.position is None or self.prior.position is None:
            return None
        return self.prior.position - self.current.position

    @property
    def is_tracked(self) -> bool:
        return self.current.present or self.prior.present


@dataclass
class CannibalFinding:
    query: str
    total_impressions: int
    total_clicks: int
    urls: list[dict] = field(default_factory=list)
    severity: str = "low"

    @property
    def url_count(self) -> int:
        return len(self.urls)

    @property
    def primary(self) -> dict | None:
        return self.urls[0] if self.urls else None


@dataclass
class MovementSummary:
    """Counts and named examples for every band transition worth acting on."""

    counts: dict[str, int] = field(default_factory=dict)
    entered_page1: list[Comparison] = field(default_factory=list)
    left_page1: list[Comparison] = field(default_factory=list)
    entered_top30: list[Comparison] = field(default_factory=list)
    left_top30: list[Comparison] = field(default_factory=list)
    striking_distance: list[Comparison] = field(default_factory=list)
    improved: list[Comparison] = field(default_factory=list)
    declined: list[Comparison] = field(default_factory=list)
    band_current: dict[str, int] = field(default_factory=dict)
    band_prior: dict[str, int] = field(default_factory=dict)
    suppressed_low_volume: int = 0


def pct_change(current: float, prior: float) -> float | None:
    """None when there is no prior baseline to divide by."""
    if not prior:
        return None
    return (current - prior) / prior * 100.0


def _rows_by_query(period: Period) -> dict[str, list[Row]]:
    out: dict[str, list[Row]] = {}
    for r in period.rows:
        if r.query_key:
            out.setdefault(r.query_key, []).append(r)
    return out


def _rows_by_page(period: Period) -> dict[str, list[Row]]:
    out: dict[str, list[Row]] = {}
    for r in period.rows:
        if r.page_key:
            out.setdefault(r.page_key, []).append(r)
    return out


def _classify(prior_band: str, current_band: str) -> str:
    if prior_band == current_band:
        return "flat"
    order = {"page1": 0, "page2": 1, "page3": 2, "beyond": 3, "unranked": 4}
    return "improved" if order[current_band] < order[prior_band] else "declined"


def compare_queries(
    current: Period,
    prior: Period,
    cfg: TargetConfig,
    targets_only: bool = True,
) -> list[Comparison]:
    """Compare per-query metrics across two periods.

    With targets_only, the result covers exactly the configured target set -
    including queries absent from both exports, which is itself a finding (a
    target with zero impressions is not ranking at all).
    """
    t = cfg.thresholds
    cur_rows = _rows_by_query(current)
    pri_rows = _rows_by_query(prior)
    targets = cfg.query_by_key()

    keys = set(targets) if targets_only else set(cur_rows) | set(pri_rows)
    comparisons: list[Comparison] = []
    for key in sorted(keys):
        target = targets.get(key)
        cur = Stat.from_rows(cur_rows.get(key, []))
        pri = Stat.from_rows(pri_rows.get(key, []))
        c = Comparison(
            key=key,
            display=target.query if target else key,
            current=cur,
            prior=pri,
            group_id=target.group_id if target else "untracked",
            group_label=target.group_label if target else "Untracked",
            market=target.market if target else None,
            band_current=t.band(cur.position),
            band_prior=t.band(pri.position),
        )
        c.transition = _classify(c.band_prior, c.band_current)
        comparisons.append(c)
    return comparisons


def compare_pages(current: Period, prior: Period, cfg: TargetConfig) -> list[Comparison]:
    """Compare per-page metrics for the configured priority pages."""
    t = cfg.thresholds
    cur_rows = _rows_by_page(current)
    pri_rows = _rows_by_page(prior)
    out: list[Comparison] = []
    for page in cfg.pages:
        cur = Stat.from_rows(cur_rows.get(page.key, []))
        pri = Stat.from_rows(pri_rows.get(page.key, []))
        c = Comparison(
            key=page.key,
            display=page.label,
            current=cur,
            prior=pri,
            group_id=page.role,
            group_label=page.role,
            market=page.market,
            band_current=t.band(cur.position),
            band_prior=t.band(pri.position),
        )
        c.transition = _classify(c.band_prior, c.band_current)
        out.append(c)
    out.sort(key=lambda c: (-c.current.impressions, c.display))
    return out


def summarize_movement(
    comparisons: list[Comparison], thresholds: Thresholds
) -> MovementSummary:
    """Bucket comparisons into page-1 / page-3 transitions.

    Queries below the impression floor in both periods are excluded from the
    movement lists - an average position computed off 2 impressions swings
    wildly and would dominate the report with noise.
    """
    s = MovementSummary()
    for c in comparisons:
        s.band_current[c.band_current] = s.band_current.get(c.band_current, 0) + 1
        s.band_prior[c.band_prior] = s.band_prior.get(c.band_prior, 0) + 1

        volume = max(c.current.impressions, c.prior.impressions)
        if volume < thresholds.movement_min_impressions:
            if c.is_tracked:
                s.suppressed_low_volume += 1
            continue

        cur_p1 = c.band_current == "page1"
        pri_p1 = c.band_prior == "page1"
        cur_top30 = c.band_current in ("page1", "page2", "page3")
        pri_top30 = c.band_prior in ("page1", "page2", "page3")

        if cur_p1 and not pri_p1:
            s.entered_page1.append(c)
        if pri_p1 and not cur_p1:
            s.left_page1.append(c)
        if cur_top30 and not pri_top30:
            s.entered_top30.append(c)
        if pri_top30 and not cur_top30:
            s.left_top30.append(c)
        if thresholds.is_striking_distance(c.current.position):
            s.striking_distance.append(c)

        gain = c.position_gain
        if gain is not None and abs(gain) >= thresholds.material_position_delta:
            (s.improved if gain > 0 else s.declined).append(c)

    s.striking_distance.sort(key=lambda c: -c.current.impressions)
    s.improved.sort(key=lambda c: -(c.position_gain or 0))
    s.declined.sort(key=lambda c: (c.position_gain or 0))
    s.counts = {
        "entered_page1": len(s.entered_page1),
        "left_page1": len(s.left_page1),
        "entered_top30": len(s.entered_top30),
        "left_top30": len(s.left_top30),
        "striking_distance": len(s.striking_distance),
        "improved": len(s.improved),
        "declined": len(s.declined),
    }
    return s


def _cannibal_severity(urls: list[dict], t) -> str:
    """Grade a finding by how much traffic the split is actually costing.

    Rank is weighted, not just share. An even 50/50 split between two URLs at
    positions 45 and 55 wins nothing if it is consolidated, while a 60/40 split
    across page 2 is a page-1 placement being given away. Grading on share alone
    inverts those two, which matters because --fail-on-regression gates on HIGH.
    """
    page1_count = sum(1 for u in urls if u["band"] == "page1")
    if page1_count >= t.cann_high_page1_urls:
        return "high"

    runner_up = urls[1]
    even_split = runner_up["share"] >= t.cann_high_min_share
    runner_up_reachable = (
        runner_up["position"] is not None
        and runner_up["position"] <= t.page2_max_position
    )
    if even_split and runner_up_reachable:
        return "high"

    contested = any(
        u["position"] is not None and u["position"] <= t.page3_max_position
        for u in urls
    )
    if contested and (len(urls) > 2 or even_split):
        return "medium"
    return "low"


def detect_cannibalization(
    period: Period, cfg: TargetConfig, targets_only: bool = False
) -> list[CannibalFinding]:
    """Find queries where two or more ACG URLs both draw impressions.

    Requires a query+page dimensioned export - a query-only or page-only export
    physically cannot show which URL served which query. Returns [] in that case
    rather than guessing; the report states the gap explicitly.
    """
    if not (period.has_query_dimension and period.has_page_dimension):
        return []

    t = cfg.thresholds
    targets = cfg.query_by_key()
    grouped: dict[str, dict[str, list[Row]]] = {}
    for r in period.rows:
        if not (r.query_key and r.page_key):
            continue
        if targets_only and r.query_key not in targets:
            continue
        grouped.setdefault(r.query_key, {}).setdefault(r.page_key, []).append(r)

    findings: list[CannibalFinding] = []
    for query_key, by_page in grouped.items():
        stats = {page_key: Stat.from_rows(rows) for page_key, rows in by_page.items()}

        # Share is always a share of the whole query, including the long-tail URLs
        # that fall below the floors. Dividing by the qualifying subset instead
        # would inflate every share and understate the query's real volume.
        query_impr = sum(s.impressions for s in stats.values())
        query_clicks = sum(s.clicks for s in stats.values())
        if not query_impr:
            continue

        qualifying = [
            (page_key, s)
            for page_key, s in stats.items()
            if s.impressions >= t.cann_min_impressions_per_url
            and s.impressions / query_impr >= t.cann_min_impression_share
        ]
        if len(qualifying) < t.cann_min_urls:
            continue

        qualifying.sort(key=lambda item: -item[1].impressions)
        urls = [
            {
                "page": page_key,
                "clicks": s.clicks,
                "impressions": s.impressions,
                "position": s.position,
                "share": s.impressions / query_impr,
                "band": t.band(s.position),
            }
            for page_key, s in qualifying
        ]

        findings.append(
            CannibalFinding(
                query=targets[query_key].query if query_key in targets else query_key,
                total_impressions=query_impr,
                total_clicks=query_clicks,
                urls=urls,
                severity=_cannibal_severity(urls, t),
            )
        )

    rank = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (rank[f.severity], -f.total_impressions))
    return findings


def summarize_groups(comparisons: list[Comparison], cfg: TargetConfig) -> list[dict]:
    """Roll query comparisons up to their configured groups.

    Emitted in the order the groups appear in the config, not the order the
    comparisons happen to be sorted in, so week-over-week reports line up.
    """
    buckets: dict[str, dict] = {}
    for c in comparisons:
        if c.group_id not in buckets:
            buckets[c.group_id] = {
                "group_id": c.group_id,
                "label": c.group_label,
                "queries": 0,
                "ranking": 0,
                "clicks": 0,
                "prior_clicks": 0,
                "impressions": 0,
                "prior_impressions": 0,
                "page1": 0,
                "_pos_weight": 0.0,
                "_pos_sum": 0.0,
            }
        b = buckets[c.group_id]
        b["queries"] += 1
        b["clicks"] += c.current.clicks
        b["prior_clicks"] += c.prior.clicks
        b["impressions"] += c.current.impressions
        b["prior_impressions"] += c.prior.impressions
        if c.current.present:
            b["ranking"] += 1
        if c.band_current == "page1":
            b["page1"] += 1
        if c.current.position is not None and c.current.impressions:
            b["_pos_sum"] += c.current.position * c.current.impressions
            b["_pos_weight"] += c.current.impressions

    ordered = [gid for gid, _ in cfg.group_order if gid in buckets]
    ordered += [gid for gid in buckets if gid not in set(ordered)]

    out = []
    for gid in ordered:
        b = buckets[gid]
        b["avg_position"] = (
            b["_pos_sum"] / b["_pos_weight"] if b["_pos_weight"] else None
        )
        b["clicks_pct"] = pct_change(b["clicks"], b["prior_clicks"])
        b["impressions_pct"] = pct_change(b["impressions"], b["prior_impressions"])
        del b["_pos_sum"], b["_pos_weight"]
        out.append(b)
    return out


def summarize_manual(manual: dict, current_period: Period) -> dict:
    """Flatten manual-metrics.json and mark every unsupplied or stale value.

    Nothing here is estimated. A metric with a null value is reported as a gap
    so the weekly report distinguishes 'zero' from 'nobody pulled the number'.
    """
    as_of = manual.get("as_of")
    stale = bool(as_of and current_period.end and as_of < current_period.end)
    sections = []
    gaps = []
    supplied = missing = 0

    for raw in manual.get("sections", []):
        section_method = raw.get("input_method", "manual-export")
        metrics = []
        for m in raw.get("metrics", []):
            method = m.get("input_method", section_method)
            has_value = m.get("value") is not None
            if has_value:
                supplied += 1
            else:
                missing += 1
                gaps.append(
                    {
                        "section": raw.get("label", raw.get("id", "")),
                        "metric": m.get("label", m.get("id", "")),
                        "scope": m.get("market") or m.get("engine") or "",
                        "input_method": method,
                        "runbook": raw.get("runbook", ""),
                    }
                )
            metrics.append(
                {
                    "id": m.get("id", ""),
                    "label": m.get("label", m.get("id", "")),
                    "scope": m.get("market") or m.get("engine") or "",
                    "value": m.get("value"),
                    "unit": m.get("unit", ""),
                    "target": m.get("target"),
                    "input_method": method,
                    "connector_id": m.get("connector_id") or raw.get("connector_id"),
                    "supplied": has_value,
                }
            )
        sections.append(
            {
                "id": raw.get("id", ""),
                "label": raw.get("label", raw.get("id", "")),
                "source": raw.get("source", ""),
                "input_method": section_method,
                "connector_id": raw.get("connector_id"),
                "runbook": raw.get("runbook", ""),
                "metrics": metrics,
            }
        )

    return {
        "as_of": as_of,
        "stale": stale,
        "sections": sections,
        "gaps": gaps,
        "supplied_count": supplied,
        "missing_count": missing,
        "file_missing": manual.get("_missing"),
    }


def build_analysis(
    current: Period,
    prior: Period,
    cfg: TargetConfig,
    manual: dict | None = None,
) -> dict:
    """Run every analysis and return the payload the report renders."""
    query_cmp = compare_queries(current, prior, cfg, targets_only=True)
    page_cmp = compare_pages(current, prior, cfg)
    movement = summarize_movement(query_cmp, cfg.thresholds)
    cannibal = detect_cannibalization(current, cfg)

    notes = []
    if not current.has_page_dimension:
        notes.append(
            "Current export has no page dimension: page performance and "
            "cannibalization could not be computed. Re-export with query+page "
            "dimensions to enable them."
        )
    if not current.has_query_dimension:
        notes.append(
            "Current export has no query dimension: query movement could not be "
            "computed."
        )
    if current.has_query_dimension and current.has_page_dimension and not cannibal:
        notes.append(
            "No cannibalization above threshold in this period."
        )
    if prior.rows and set(current.dimensions) != set(prior.dimensions):
        # A query-only prior against a query+page current compares a query's
        # total against one URL's slice of it, which reads as a collapse.
        notes.append(
            f"Period dimensions differ - current is "
            f"[{', '.join(current.dimensions) or 'none'}], prior is "
            f"[{', '.join(prior.dimensions) or 'none'}]. Deltas are not "
            f"comparable; re-export both periods with the same dimensions."
        )

    return {
        "config": cfg,
        "current": current,
        "prior": prior,
        "totals_current": current.totals(),
        "totals_prior": prior.totals(),
        "queries": query_cmp,
        "pages": page_cmp,
        "movement": movement,
        "cannibalization": cannibal,
        "groups": summarize_groups(query_cmp, cfg),
        "manual": summarize_manual(manual or {"sections": []}, current),
        "notes": notes,
    }
