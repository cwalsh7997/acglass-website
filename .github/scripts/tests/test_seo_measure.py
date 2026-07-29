#!/usr/bin/env python3
"""Tests for the SEO measurement layer.

Run:  python3 -m unittest discover -s .github/scripts/tests -v
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from seo_measure.analyze import (  # noqa: E402
    build_analysis,
    compare_pages,
    compare_queries,
    detect_cannibalization,
    summarize_groups,
    summarize_manual,
    summarize_movement,
)
from seo_measure.config import (  # noqa: E402
    ConfigError,
    DEFAULT_CONFIG_PATH,
    DEFAULT_MANUAL_PATH,
    load_config,
    normalize_path,
    normalize_query,
)
from seo_measure.ingest import (  # noqa: E402
    IngestError,
    Period,
    Row,
    aggregate,
    load_api_json,
    load_csv,
    load_manual_metrics,
    write_snapshot,
)
from seo_measure.report import render_markdown, write_csvs  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _tracked_files() -> set[str]:
    """Files git knows about.

    Consulted instead of the working tree so the page-existence check still
    works in a sparse checkout, where directory-style pages are in the index
    but not on disk.
    """
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files"],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def load_script(filename: str):
    """Import a hyphenated CLI script, which a normal import statement cannot."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        filename.replace("-", "_").removesuffix(".py"), SCRIPTS_DIR / filename
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows_period(rows, dims=("query", "page"), **kw):
    return Period(
        label=kw.pop("label", "p"),
        start=kw.pop("start", "2026-07-20"),
        end=kw.pop("end", "2026-07-26"),
        rows=rows,
        dimensions=tuple(dims),
        source="test",
    )


class TestNormalization(unittest.TestCase):
    def test_query_normalization_is_case_and_space_insensitive(self):
        self.assertEqual(
            normalize_query("  Commercial   Glazing Contractor  "),
            "commercial glazing contractor",
        )

    def test_path_normalization_strips_origin_query_and_fragment(self):
        for raw in (
            "https://acglass.com/nashville/",
            "http://acglass.com/nashville/?utm_source=x",
            "/nashville/#top",
            "https://acglass.com/nashville/index.html",
        ):
            self.assertEqual(normalize_path(raw), "/nashville/", raw)

    def test_path_normalization_handles_root_and_empty(self):
        self.assertEqual(normalize_path("https://acglass.com"), "/")
        self.assertEqual(normalize_path("https://acglass.com/"), "/")
        self.assertEqual(normalize_path(""), "")

    def test_path_normalization_adds_leading_slash(self):
        self.assertEqual(normalize_path("about.html"), "/about.html")


class TestConfig(unittest.TestCase):
    def test_repo_config_loads_and_validates(self):
        cfg = load_config(DEFAULT_CONFIG_PATH)
        self.assertTrue(cfg.gsc_property.startswith("sc-domain:"))
        self.assertGreater(len(cfg.queries), 20)
        self.assertGreater(len(cfg.pages), 10)
        self.assertGreater(len(cfg.markets), 5)

    def test_repo_config_page_paths_exist_in_repo(self):
        """Every priority page must be a real URL, or the report tracks a ghost."""
        cfg = load_config(DEFAULT_CONFIG_PATH)
        tracked = _tracked_files()
        missing = []
        for page in cfg.pages:
            path = page.key.lstrip("/")
            candidates = {path or "index.html", f"{path}index.html" if path.endswith("/") else f"{path}/index.html"}
            on_disk = any((REPO_ROOT / c).is_file() for c in candidates)
            in_git = bool(tracked) and bool(candidates & tracked)
            if not (on_disk or in_git):
                missing.append(page.path)
        self.assertEqual(missing, [], f"config lists pages absent from the repo: {missing}")

    def test_band_boundaries_are_inclusive_at_the_top(self):
        cfg = load_config(DEFAULT_CONFIG_PATH)
        t = cfg.thresholds
        self.assertEqual(t.band(1.0), "page1")
        self.assertEqual(t.band(10.0), "page1")
        self.assertEqual(t.band(10.1), "page2")
        self.assertEqual(t.band(20.0), "page2")
        self.assertEqual(t.band(30.0), "page3")
        self.assertEqual(t.band(30.1), "beyond")
        self.assertEqual(t.band(None), "unranked")

    def test_striking_distance_excludes_page1(self):
        t = load_config(DEFAULT_CONFIG_PATH).thresholds
        self.assertFalse(t.is_striking_distance(9.0))
        self.assertFalse(t.is_striking_distance(10.0))
        self.assertTrue(t.is_striking_distance(10.5))
        self.assertTrue(t.is_striking_distance(30.0))
        self.assertFalse(t.is_striking_distance(31.0))

    def test_duplicate_query_across_groups_is_rejected(self):
        bad = {
            "property": {"gsc_property": "sc-domain:example.com"},
            "query_groups": [
                {"id": "a", "queries": ["same query"]},
                {"id": "b", "queries": ["Same Query"]},
            ],
        }
        with self._temp_config(bad) as path:
            with self.assertRaises(ConfigError) as ctx:
                load_config(path)
            self.assertIn("duplicate", str(ctx.exception))

    def test_unknown_market_reference_is_rejected(self):
        bad = {
            "property": {"gsc_property": "sc-domain:example.com"},
            "markets": [{"id": "tampa"}],
            "query_groups": [
                {"id": "a", "queries": [{"query": "x", "market": "atlantis"}]}
            ],
        }
        with self._temp_config(bad) as path:
            with self.assertRaises(ConfigError):
                load_config(path)

    def test_non_increasing_bands_are_rejected(self):
        bad = {
            "property": {"gsc_property": "sc-domain:example.com"},
            "thresholds": {"page1_max_position": 30, "page3_max_position": 10},
            "query_groups": [{"id": "a", "queries": ["x"]}],
        }
        with self._temp_config(bad) as path:
            with self.assertRaises(ConfigError):
                load_config(path)

    def test_missing_property_is_rejected(self):
        with self._temp_config({"query_groups": []}) as path:
            with self.assertRaises(ConfigError):
                load_config(path)

    def _temp_config(self, payload):
        class _Ctx:
            def __enter__(self_inner):
                self_inner.dir = tempfile.TemporaryDirectory()
                p = Path(self_inner.dir.name) / "cfg.json"
                p.write_text(json.dumps(payload), encoding="utf-8")
                return p

            def __exit__(self_inner, *a):
                self_inner.dir.cleanup()

        return _Ctx()


class TestCsvIngest(unittest.TestCase):
    def test_gsc_ui_query_export(self):
        period = load_csv(FIXTURES / "gsc-queries-current.csv", "current")
        self.assertEqual(period.dimensions, ("query",))
        self.assertTrue(period.has_query_dimension)
        self.assertFalse(period.has_page_dimension)
        self.assertGreater(len(period.rows), 5)

    def test_percent_ctr_is_parsed_to_a_ratio(self):
        period = load_csv(
            "Top queries,Clicks,Impressions,CTR,Position\nfoo,5,100,5%,3.2\n", "p"
        )
        self.assertAlmostEqual(period.rows[0].ctr, 0.05)

    def test_ratio_ctr_is_passed_through(self):
        period = load_csv("query,clicks,impressions,ctr,position\nfoo,5,100,0.05,3.2\n", "p")
        self.assertAlmostEqual(period.rows[0].ctr, 0.05)

    def test_thousands_separators_are_parsed(self):
        period = load_csv(
            'query,clicks,impressions,ctr,position\nfoo,"1,234","56,789",2.2%,4.5\n', "p"
        )
        self.assertEqual(period.rows[0].clicks, 1234)
        self.assertEqual(period.rows[0].impressions, 56789)

    def test_header_aliases_are_accepted(self):
        period = load_csv(
            "Landing Page,URL Clicks,Impressions,Avg. Position\n"
            "https://acglass.com/nashville/,3,40,12.5\n",
            "p",
        )
        self.assertEqual(period.dimensions, ("page",))
        self.assertEqual(period.rows[0].page_key, "/nashville/")
        self.assertEqual(period.rows[0].clicks, 3)
        self.assertAlmostEqual(period.rows[0].position, 12.5)

    def test_blank_and_dash_cells_do_not_crash(self):
        period = load_csv("query,clicks,impressions,ctr,position\nfoo,,-,,\n", "p")
        self.assertEqual(period.rows[0].clicks, 0)
        self.assertEqual(period.rows[0].impressions, 0)
        self.assertIsNone(period.rows[0].position)

    def test_rows_with_no_dimension_value_are_skipped(self):
        period = load_csv("query,clicks,impressions\nfoo,1,2\n,3,4\n", "p")
        self.assertEqual(len(period.rows), 1)

    def test_missing_dimension_column_raises(self):
        with self.assertRaises(IngestError):
            load_csv("clicks,impressions\n1,2\n", "p")

    def test_missing_metric_columns_raise(self):
        with self.assertRaises(IngestError):
            load_csv("query,something\nfoo,bar\n", "p")

    def test_mistyped_path_reports_file_not_found_not_a_header_error(self):
        """A typo'd filename must not be parsed as if it were inline CSV text."""
        with self.assertRaises(IngestError) as ctx:
            load_csv("/tmp/definitely-not-here.csv", "p")
        self.assertIn("file not found", str(ctx.exception))

    def test_utf8_bom_export_is_readable(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bom.csv"
            p.write_text(
                "Top queries,Clicks,Impressions,CTR,Position\nfoo,1,10,10%,5\n",
                encoding="utf-8-sig",
            )
            period = load_csv(p, "p")
            self.assertEqual(period.rows[0].query, "foo")


class TestJsonIngest(unittest.TestCase):
    def test_raw_api_body_with_keys_and_explicit_dimensions(self):
        payload = {
            "dimensions": ["query", "page"],
            "rows": [
                {
                    "keys": ["commercial glazing contractor miami", "https://acglass.com/x.html"],
                    "clicks": 4,
                    "impressions": 90,
                    "ctr": 0.0444,
                    "position": 8.1,
                }
            ],
        }
        period = load_api_json(payload, "current")
        self.assertEqual(period.rows[0].query_key, "commercial glazing contractor miami")
        self.assertEqual(period.rows[0].page_key, "/x.html")
        self.assertEqual(set(period.dimensions), {"query", "page"})

    def test_dimensions_are_inferred_when_absent(self):
        period = load_api_json(
            {"rows": [{"keys": ["https://acglass.com/a.html"], "clicks": 1, "impressions": 2}]},
            "p",
        )
        self.assertEqual(period.rows[0].page_key, "/a.html")
        self.assertIsNone(period.rows[0].query)

    def test_flat_row_shape_is_accepted(self):
        period = load_api_json(
            {"rows": [{"query": "foo", "page": "/a.html", "clicks": 1, "impressions": 2}]},
            "p",
        )
        self.assertEqual(period.rows[0].query, "foo")

    def test_snapshot_carries_its_own_period(self):
        period = load_api_json(FIXTURES / "gsc-snapshot-current.json", None)
        self.assertEqual(period.start, "2026-07-20")
        self.assertEqual(period.end, "2026-07-26")

    def test_missing_rows_key_raises(self):
        with self.assertRaises(IngestError):
            load_api_json({"nope": []}, "p")

    def test_mistyped_json_path_reports_file_not_found(self):
        with self.assertRaises(IngestError) as ctx:
            load_api_json("/tmp/definitely-not-here.json", "p")
        self.assertIn("file not found", str(ctx.exception))

    def test_snapshot_roundtrip_preserves_metrics(self):
        original = load_csv(FIXTURES / "gsc-combined-current.csv", "current",
                            "2026-07-20", "2026-07-26")
        with tempfile.TemporaryDirectory() as d:
            out = write_snapshot(original, Path(d) / "snap.json")
            restored = load_api_json(out, None)
        self.assertEqual(len(original.rows), len(restored.rows))
        self.assertEqual(original.totals()["clicks"], restored.totals()["clicks"])
        self.assertEqual(
            original.totals()["impressions"], restored.totals()["impressions"]
        )
        self.assertEqual(set(original.dimensions), set(restored.dimensions))


class TestAggregate(unittest.TestCase):
    def test_position_is_impression_weighted_not_a_plain_mean(self):
        rows = [
            Row("a", None, 0, 1000, 0.0, 2.0),
            Row("b", None, 0, 1, 0.0, 90.0),
        ]
        agg = aggregate(rows)
        # A plain mean would be 46.0; impression weighting keeps it near 2.
        self.assertLess(agg["position"], 3.0)

    def test_ctr_is_recomputed_from_totals(self):
        rows = [Row("a", None, 5, 50, 0.9, 3.0), Row("b", None, 5, 50, 0.9, 3.0)]
        self.assertAlmostEqual(aggregate(rows)["ctr"], 0.1)

    def test_empty_rows_yield_none_position(self):
        self.assertIsNone(aggregate([])["position"])


class TestComparison(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(DEFAULT_CONFIG_PATH)

    def test_every_target_query_appears_even_with_no_data(self):
        comparisons = compare_queries(rows_period([]), rows_period([]), self.cfg)
        self.assertEqual(len(comparisons), len(self.cfg.queries))
        self.assertTrue(all(c.band_current == "unranked" for c in comparisons))

    def test_position_gain_is_positive_when_rank_improves(self):
        q = "commercial glazing contractor miami"
        cur = rows_period([Row(q, "/a.html", 10, 100, 0.1, 4.0)])
        pri = rows_period([Row(q, "/a.html", 5, 100, 0.05, 12.0)])
        c = next(x for x in compare_queries(cur, pri, self.cfg) if x.key == q)
        self.assertAlmostEqual(c.position_gain, 8.0)
        self.assertEqual(c.transition, "improved")
        self.assertEqual(c.band_prior, "page2")
        self.assertEqual(c.band_current, "page1")

    def test_pct_change_is_none_without_a_baseline(self):
        q = "commercial glazing contractor miami"
        cur = rows_period([Row(q, "/a.html", 10, 100, 0.1, 4.0)])
        c = next(x for x in compare_queries(cur, rows_period([]), self.cfg) if x.key == q)
        self.assertIsNone(c.clicks_pct)
        self.assertIsNone(c.position_gain)
        self.assertEqual(c.clicks_delta, 10)

    def test_query_metrics_sum_across_pages(self):
        q = "commercial glazing contractor miami"
        cur = rows_period(
            [
                Row(q, "/a.html", 3, 60, 0.05, 5.0),
                Row(q, "/b.html", 2, 40, 0.05, 15.0),
            ]
        )
        c = next(x for x in compare_queries(cur, rows_period([]), self.cfg) if x.key == q)
        self.assertEqual(c.current.clicks, 5)
        self.assertEqual(c.current.impressions, 100)

    def test_page_comparison_matches_config_paths_to_full_urls(self):
        cur = rows_period(
            [Row(None, "https://acglass.com/nashville/index.html", 7, 70, 0.1, 6.0)],
            dims=("page",),
        )
        pages = compare_pages(cur, rows_period([], dims=("page",)), self.cfg)
        nashville = next(p for p in pages if p.key == "/nashville/")
        self.assertEqual(nashville.current.clicks, 7)


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(DEFAULT_CONFIG_PATH)
        self.t = self.cfg.thresholds

    def _cmp(self, cur_pos, pri_pos, impressions=500):
        q = "commercial glazing contractor miami"
        cur = rows_period(
            [Row(q, "/a.html", 1, impressions, 0.01, cur_pos)] if cur_pos else []
        )
        pri = rows_period(
            [Row(q, "/a.html", 1, impressions, 0.01, pri_pos)] if pri_pos else []
        )
        return [c for c in compare_queries(cur, pri, self.cfg) if c.key == q]

    def test_entering_page1_is_detected(self):
        s = summarize_movement(self._cmp(5.0, 14.0), self.t)
        self.assertEqual(s.counts["entered_page1"], 1)
        self.assertEqual(s.counts["left_page1"], 0)

    def test_dropping_off_page1_is_detected(self):
        s = summarize_movement(self._cmp(16.0, 6.0), self.t)
        self.assertEqual(s.counts["left_page1"], 1)
        self.assertEqual(s.counts["entered_page1"], 0)

    def test_entering_top30_is_detected(self):
        s = summarize_movement(self._cmp(25.0, 45.0), self.t)
        self.assertEqual(s.counts["entered_top30"], 1)

    def test_leaving_top30_is_detected(self):
        s = summarize_movement(self._cmp(48.0, 22.0), self.t)
        self.assertEqual(s.counts["left_top30"], 1)

    def test_striking_distance_captures_page2_and_page3(self):
        s = summarize_movement(self._cmp(18.0, 18.0), self.t)
        self.assertEqual(s.counts["striking_distance"], 1)

    def test_low_volume_queries_are_suppressed_from_movement(self):
        s = summarize_movement(self._cmp(5.0, 25.0, impressions=2), self.t)
        self.assertEqual(s.counts["entered_page1"], 0)
        self.assertEqual(s.suppressed_low_volume, 1)

    def test_sub_threshold_position_drift_is_not_reported(self):
        s = summarize_movement(self._cmp(5.0, 5.4), self.t)
        self.assertEqual(s.counts["improved"], 0)
        self.assertEqual(s.counts["declined"], 0)

    def test_band_distribution_counts_all_targets(self):
        s = summarize_movement(compare_queries(rows_period([]), rows_period([]), self.cfg), self.t)
        self.assertEqual(s.band_current["unranked"], len(self.cfg.queries))

    def test_movement_floor_is_inclusive_at_the_configured_minimum(self):
        """min_impressions is a minimum, so exactly that many qualifies."""
        floor = self.t.movement_min_impressions
        self.assertEqual(
            summarize_movement(self._cmp(5.0, 14.0, impressions=floor), self.t)
            .counts["entered_page1"],
            1,
        )
        below = summarize_movement(self._cmp(5.0, 14.0, impressions=floor - 1), self.t)
        self.assertEqual(below.counts["entered_page1"], 0)
        self.assertEqual(below.suppressed_low_volume, 1)


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(DEFAULT_CONFIG_PATH)

    def test_every_configured_group_is_represented_once(self):
        groups = summarize_groups(
            compare_queries(rows_period([]), rows_period([]), self.cfg, targets_only=True),
            self.cfg,
        )
        self.assertEqual([g["group_id"] for g in groups], [gid for gid, _ in self.cfg.group_order])
        self.assertEqual(sum(g["queries"] for g in groups), len(self.cfg.queries))
        self.assertTrue(all(g["ranking"] == 0 for g in groups))
        self.assertTrue(all(g["avg_position"] is None for g in groups))

    def test_group_rollup_totals_and_average_position(self):
        q1 = "commercial glazing contractor miami"
        q2 = "storefront glazing contractor florida"
        cur = rows_period(
            [
                Row(q1, "/a.html", 10, 1000, 0.01, 4.0),
                Row(q2, "/b.html", 2, 100, 0.02, 24.0),
            ]
        )
        pri = rows_period([Row(q1, "/a.html", 5, 500, 0.01, 6.0)])
        groups = summarize_groups(
            compare_queries(cur, pri, self.cfg, targets_only=True), self.cfg
        )
        g = next(g for g in groups if g["clicks"])
        self.assertEqual(g["clicks"], 12)
        self.assertEqual(g["prior_clicks"], 5)
        self.assertEqual(g["impressions"], 1100)
        self.assertEqual(g["ranking"], 2)
        self.assertEqual(g["page1"], 1)
        self.assertAlmostEqual(g["clicks_pct"], 140.0, places=6)
        # Impression-weighted, so the 100-impression page-3 row barely moves it.
        self.assertAlmostEqual(
            g["avg_position"], (4.0 * 1000 + 24.0 * 100) / 1100, places=6
        )


class TestCannibalization(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(DEFAULT_CONFIG_PATH)

    def test_two_page1_urls_on_one_query_is_high_severity(self):
        q = "commercial glazing contractor west palm beach"
        period = rows_period(
            [
                Row(q, "/west-palm-beach/", 10, 500, 0.02, 4.0),
                Row(q, "/commercial-glazing-west-palm-beach.html", 6, 400, 0.015, 7.0),
            ]
        )
        findings = detect_cannibalization(period, self.cfg)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "high")
        self.assertEqual(findings[0].url_count, 2)
        self.assertEqual(findings[0].primary["page"], "/west-palm-beach/")
        self.assertAlmostEqual(sum(u["share"] for u in findings[0].urls), 1.0, places=6)

    def test_share_is_of_the_whole_query_not_the_qualifying_subset(self):
        """A below-floor third URL still counts toward the query's impressions."""
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 10, 1000, 0.01, 4.0),
                Row(q, "/b.html", 3, 300, 0.01, 7.0),
                Row(q, "/c.html", 0, 80, 0.0, 41.0),
            ]
        )
        finding = detect_cannibalization(period, self.cfg)[0]
        self.assertEqual(finding.url_count, 2)
        self.assertEqual(finding.total_impressions, 1380)
        self.assertEqual(finding.total_clicks, 13)
        self.assertAlmostEqual(finding.urls[0]["share"], 1000 / 1380, places=6)
        self.assertAlmostEqual(finding.urls[1]["share"], 300 / 1380, places=6)
        self.assertLess(sum(u["share"] for u in finding.urls), 1.0)

    def test_single_url_query_is_not_flagged(self):
        period = rows_period(
            [Row("commercial glazing contractor miami", "/a.html", 10, 500, 0.02, 4.0)]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg), [])

    def test_url_below_impression_floor_is_ignored(self):
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 10, 500, 0.02, 4.0),
                Row(q, "/b.html", 0, 1, 0.0, 60.0),
            ]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg), [])

    def test_url_below_share_floor_is_ignored(self):
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 10, 1000, 0.01, 4.0),
                Row(q, "/b.html", 0, 20, 0.0, 60.0),
            ]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg), [])

    def test_three_competing_urls_off_page1_is_medium(self):
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 1, 100, 0.01, 22.0),
                Row(q, "/b.html", 1, 90, 0.01, 25.0),
                Row(q, "/c.html", 1, 85, 0.01, 28.0),
            ]
        )
        findings = detect_cannibalization(period, self.cfg)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "medium")
        self.assertEqual(findings[0].url_count, 3)

    def test_even_split_off_page3_is_low_severity(self):
        """Consolidating two position-50 URLs wins nothing, so it is not urgent."""
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 0, 110, 0.0, 45.0),
                Row(q, "/b.html", 0, 100, 0.0, 55.0),
            ]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg)[0].severity, "low")

    def test_even_split_on_page2_is_high_severity(self):
        """A page-2 split is a page-1 placement being given away."""
        q = "commercial glazing contractor miami"
        period = rows_period(
            [
                Row(q, "/a.html", 2, 300, 0.007, 12.4),
                Row(q, "/b.html", 1, 200, 0.005, 18.9),
            ]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg)[0].severity, "high")

    def test_query_only_export_cannot_detect_cannibalization(self):
        period = rows_period(
            [Row("commercial glazing contractor miami", None, 10, 500, 0.02, 4.0)],
            dims=("query",),
        )
        self.assertEqual(detect_cannibalization(period, self.cfg), [])

    def test_untracked_queries_are_flagged_too(self):
        """Cannibalization is a site-health problem, not only a target-set problem."""
        period = rows_period(
            [
                Row("some long tail phrase", "/a.html", 1, 100, 0.01, 8.0),
                Row("some long tail phrase", "/b.html", 1, 90, 0.01, 9.0),
            ]
        )
        self.assertEqual(len(detect_cannibalization(period, self.cfg)), 1)

    def test_targets_only_mode_restricts_to_the_target_set(self):
        period = rows_period(
            [
                Row("some long tail phrase", "/a.html", 1, 100, 0.01, 8.0),
                Row("some long tail phrase", "/b.html", 1, 90, 0.01, 9.0),
            ]
        )
        self.assertEqual(detect_cannibalization(period, self.cfg, targets_only=True), [])

    def test_findings_are_ordered_high_severity_first(self):
        period = rows_period(
            [
                Row("q high", "/a.html", 1, 100, 0.01, 3.0),
                Row("q high", "/b.html", 1, 95, 0.01, 5.0),
                Row("q low", "/c.html", 1, 900, 0.01, 40.0),
                Row("q low", "/d.html", 1, 110, 0.01, 55.0),
            ]
        )
        findings = detect_cannibalization(period, self.cfg)
        self.assertEqual(findings[0].query, "q high")
        self.assertEqual(findings[0].severity, "high")


class TestManualMetrics(unittest.TestCase):
    def test_repo_manual_template_parses(self):
        manual = load_manual_metrics(DEFAULT_MANUAL_PATH)
        self.assertIn("sections", manual)
        ids = {s["id"] for s in manual["sections"]}
        self.assertTrue({"local_map", "ai_visibility", "bing"} <= ids)

    def test_missing_file_is_not_an_error(self):
        manual = load_manual_metrics(Path("/nonexistent/manual.json"))
        self.assertEqual(manual["sections"], [])
        self.assertTrue(manual["_missing"])

    def test_null_values_are_counted_as_gaps_not_zeros(self):
        manual = {
            "as_of": "2026-07-26",
            "sections": [
                {
                    "id": "s",
                    "label": "S",
                    "input_method": "manual-export",
                    "metrics": [
                        {"id": "a", "label": "A", "value": None},
                        {"id": "b", "label": "B", "value": 0},
                    ],
                }
            ],
        }
        summary = summarize_manual(manual, rows_period([]))
        self.assertEqual(summary["missing_count"], 1)
        self.assertEqual(summary["supplied_count"], 1)
        self.assertEqual(summary["gaps"][0]["metric"], "A")

    def test_metric_level_input_method_overrides_the_section(self):
        manual = {
            "sections": [
                {
                    "id": "s",
                    "label": "S",
                    "input_method": "manual-export",
                    "metrics": [
                        {"id": "a", "label": "A", "value": 1, "input_method": "unavailable-no-api"}
                    ],
                }
            ]
        }
        summary = summarize_manual(manual, rows_period([]))
        self.assertEqual(
            summary["sections"][0]["metrics"][0]["input_method"], "unavailable-no-api"
        )

    def test_values_older_than_the_period_are_marked_stale(self):
        manual = {"as_of": "2026-07-01", "sections": []}
        self.assertTrue(summarize_manual(manual, rows_period([]))["stale"])

    def test_current_values_are_not_stale(self):
        manual = {"as_of": "2026-07-26", "sections": []}
        self.assertFalse(summarize_manual(manual, rows_period([]))["stale"])


class TestReport(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(DEFAULT_CONFIG_PATH)
        self.current = load_csv(
            FIXTURES / "gsc-combined-current.csv", "current", "2026-07-20", "2026-07-26"
        )
        self.prior = load_csv(
            FIXTURES / "gsc-combined-prior.csv", "prior", "2026-07-13", "2026-07-19"
        )
        self.manual = load_manual_metrics(FIXTURES / "manual-metrics-partial.json")
        self.analysis = build_analysis(self.current, self.prior, self.cfg, self.manual)

    def test_markdown_contains_every_section(self):
        md = render_markdown(self.analysis, generated_on="2026-07-29")
        for heading in (
            "## 1. Totals",
            "## 2. Page-1 / page-3 movement",
            "## 3. Target query groups",
            "## 4. Cannibalization",
            "## 5. Priority pages",
            "## 6. Local, map, AI and Bing surfaces",
            "## 7. Data gaps",
        ):
            self.assertIn(heading, md)

    def test_markdown_is_deterministic(self):
        a = render_markdown(self.analysis, generated_on="2026-07-29")
        b = render_markdown(
            build_analysis(self.current, self.prior, self.cfg, self.manual),
            generated_on="2026-07-29",
        )
        self.assertEqual(a, b)

    def test_unsupplied_metrics_render_as_not_supplied_never_zero(self):
        md = render_markdown(self.analysis, generated_on="2026-07-29")
        self.assertIn("_not supplied_", md)

    def test_known_cannibalized_query_surfaces_in_the_report(self):
        md = render_markdown(self.analysis, generated_on="2026-07-29")
        self.assertIn("commercial glazing contractor west palm beach", md)
        self.assertGreater(len(self.analysis["cannibalization"]), 0)

    def test_csvs_are_written_with_headers(self):
        with tempfile.TemporaryDirectory() as d:
            written = write_csvs(self.analysis, d)
            names = {p.name for p in written}
            self.assertEqual(
                names,
                {
                    "queries.csv",
                    "pages.csv",
                    "cannibalization.csv",
                    "movement.csv",
                    "manual-metrics.csv",
                },
            )
            for p in written:
                lines = p.read_text(encoding="utf-8").splitlines()
                self.assertGreaterEqual(len(lines), 1, p.name)

    def test_queries_csv_has_one_row_per_target(self):
        with tempfile.TemporaryDirectory() as d:
            write_csvs(self.analysis, d)
            lines = (Path(d) / "queries.csv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines) - 1, len(self.cfg.queries))

    def test_report_notes_missing_page_dimension(self):
        query_only = load_csv(FIXTURES / "gsc-queries-current.csv", "current")
        analysis = build_analysis(query_only, self.prior, self.cfg, self.manual)
        md = render_markdown(analysis, generated_on="2026-07-29")
        self.assertIn("Not computable", md)

    def test_report_warns_when_the_two_periods_have_different_dimensions(self):
        query_only = load_csv(FIXTURES / "gsc-queries-current.csv", "prior")
        analysis = build_analysis(self.current, query_only, self.cfg, self.manual)
        self.assertTrue(
            any("dimensions differ" in n for n in analysis["notes"]), analysis["notes"]
        )
        self.assertIn("dimensions differ", render_markdown(analysis, generated_on="x"))

    def test_matched_dimensions_produce_no_warning(self):
        analysis = build_analysis(self.current, self.prior, self.cfg, self.manual)
        self.assertFalse(any("dimensions differ" in n for n in analysis["notes"]))


class TestCli(unittest.TestCase):
    def test_end_to_end_run_writes_report_and_csvs(self):
        module = load_script("seo-report.py")

        with tempfile.TemporaryDirectory() as d:
            code = module.main(
                [
                    "--current", str(FIXTURES / "gsc-combined-current.csv"),
                    "--prior", str(FIXTURES / "gsc-combined-prior.csv"),
                    "--current-range", "2026-07-20:2026-07-26",
                    "--prior-range", "2026-07-13:2026-07-19",
                    "--manual", str(FIXTURES / "manual-metrics-partial.json"),
                    "--out-dir", d,
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue((Path(d) / "seo-report-2026-07-26.md").is_file())
            self.assertTrue((Path(d) / "queries.csv").is_file())

    def test_bad_date_range_is_rejected(self):
        module = load_script("seo-report.py")
        with tempfile.TemporaryDirectory() as d:
            code = module.main(
                [
                    "--current", str(FIXTURES / "gsc-combined-current.csv"),
                    "--prior", str(FIXTURES / "gsc-combined-prior.csv"),
                    "--current-range", "nonsense",
                    "--out-dir", d,
                ]
            )
        self.assertEqual(code, 1)

    def test_missing_input_file_is_reported_as_missing(self):
        module = load_script("seo-report.py")
        with tempfile.TemporaryDirectory() as d:
            code = module.main(
                [
                    "--current", str(Path(d) / "nope.csv"),
                    "--prior", str(FIXTURES / "gsc-combined-prior.csv"),
                    "--out-dir", d,
                ]
            )
        self.assertEqual(code, 1)

    def _run_gate(self, out_dir, current, prior):
        return load_script("seo-report.py").main(
            [
                "--current", str(current),
                "--prior", str(prior),
                "--current-range", "2026-07-20:2026-07-26",
                "--prior-range", "2026-07-13:2026-07-19",
                "--out-dir", out_dir,
                "--fail-on-regression",
            ]
        )

    def test_regression_gate_exits_2_when_a_target_drops_off_page1(self):
        with tempfile.TemporaryDirectory() as d:
            code = self._run_gate(
                d,
                FIXTURES / "gsc-combined-current.csv",
                FIXTURES / "gsc-combined-prior.csv",
            )
        self.assertEqual(code, 2)

    def test_regression_gate_exits_0_on_a_clean_period(self):
        """Same data both periods: nothing moved and nothing is cannibalized."""
        clean = (
            "Query,Page,Clicks,Impressions,CTR,Position\n"
            "commercial glazing contractor miami,https://acglass.com/miami/,10,500,2%,4.1\n"
        )
        with tempfile.TemporaryDirectory() as d:
            cur = Path(d) / "cur.csv"
            cur.write_text(clean, encoding="utf-8")
            code = self._run_gate(d, cur, cur)
        self.assertEqual(code, 0)

    def test_report_renders_with_a_config_outside_the_repo(self):
        """--config may point anywhere; the footer must not crash on it."""
        cfg_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            external = Path(d) / "cfg.json"
            external.write_text(json.dumps(cfg_payload), encoding="utf-8")
            code = load_script("seo-report.py").main(
                [
                    "--current", str(FIXTURES / "gsc-combined-current.csv"),
                    "--prior", str(FIXTURES / "gsc-combined-prior.csv"),
                    "--current-range", "2026-07-20:2026-07-26",
                    "--prior-range", "2026-07-13:2026-07-19",
                    "--config", str(external),
                    "--out-dir", d,
                    "--no-csv",
                ]
            )
            self.assertEqual(code, 0)
            md = (Path(d) / "seo-report-2026-07-26.md").read_text(encoding="utf-8")
        self.assertIn(str(external), md)


class TestExportWindows(unittest.TestCase):
    def test_weekly_windows_respect_the_gsc_lag_and_do_not_overlap(self):
        module = load_script("seo-gsc-export.py")

        from datetime import date

        (cs, ce), (ps, pe) = module.weekly_windows(date(2026, 7, 29))
        self.assertEqual(ce, date(2026, 7, 26))
        self.assertEqual(cs, date(2026, 7, 20))
        self.assertEqual(pe, date(2026, 7, 19))
        self.assertEqual(ps, date(2026, 7, 13))
        self.assertLess(pe, cs)
        self.assertEqual((ce - cs).days, 6)


class TestNoSecrets(unittest.TestCase):
    """The repo root is the deploy root, so a leaked key would be world-readable."""

    SECRET_MARKERS = [
        "-----BEGIN PRIVATE KEY-----",
        "-----BEGIN RSA PRIVATE KEY-----",
        '"private_key"',
        "AIza",
        "sk-",
        "pplx-",
        "hooks.slack.com/services/",
    ]

    def test_no_credential_material_in_the_measurement_layer(self):
        targets = [
            SCRIPTS_DIR / "seo-report.py",
            SCRIPTS_DIR / "seo-gsc-export.py",
            REPO_ROOT / ".github" / "seo" / "seo-targets.json",
            REPO_ROOT / ".github" / "seo" / "manual-metrics.json",
        ]
        targets.extend((SCRIPTS_DIR / "seo_measure").glob("*.py"))
        for path in targets:
            text = path.read_text(encoding="utf-8")
            for marker in self.SECRET_MARKERS:
                self.assertNotIn(marker, text, f"{path.name} contains {marker!r}")

    def test_config_files_carry_no_metric_values(self):
        """seo-targets.json defines targets only; values arrive at runtime."""
        raw = json.loads(
            (REPO_ROOT / ".github" / "seo" / "seo-targets.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("rows", raw)
        self.assertNotIn("metrics", raw)


if __name__ == "__main__":
    unittest.main(verbosity=2)
