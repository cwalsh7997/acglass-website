#!/usr/bin/env python3
"""seo-report.py - Weekly SEO measurement report for acglass.com.

Compares two Search Console periods against the target set in
.github/seo/seo-targets.json and writes a Markdown report plus companion CSVs.

Inputs are files you already have: a CSV exported from the GSC UI, or a JSON
snapshot written by seo-gsc-export.py. No credentials are read and no SERP is
fetched.

Usage:
  # From two CSV exports (GSC UI > Export > CSV)
  python3 .github/scripts/seo-report.py \
      --current .github/seo/data/2026-07-20_2026-07-26.csv \
      --prior   .github/seo/data/2026-07-13_2026-07-19.csv \
      --current-range 2026-07-20:2026-07-26 \
      --prior-range   2026-07-13:2026-07-19

  # From API snapshots (dates are carried inside the snapshot)
  python3 .github/scripts/seo-report.py \
      --current .github/seo/data/current.json --prior .github/seo/data/prior.json

Exit codes: 0 ok, 1 bad input, 2 threshold breach under --fail-on-regression.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo_measure.analyze import build_analysis
from seo_measure.config import DEFAULT_CONFIG_PATH, DEFAULT_MANUAL_PATH, ConfigError, load_config
from seo_measure.ingest import IngestError, load_manual_metrics, load_period
from seo_measure.report import render_markdown, write_csvs

REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_range(value: str | None) -> tuple[str | None, str | None]:
    """Parse 'YYYY-MM-DD:YYYY-MM-DD'."""
    if not value:
        return None, None
    if ":" not in value:
        raise ValueError(f"date range must be START:END, got {value!r}")
    start, end = value.split(":", 1)
    return start.strip() or None, end.strip() or None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate the weekly ACG SEO report from GSC exports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--current", required=True, help="Current-period .csv or .json")
    p.add_argument("--prior", required=True, help="Prior-period .csv or .json")
    p.add_argument("--current-range", help="YYYY-MM-DD:YYYY-MM-DD for the current period")
    p.add_argument("--prior-range", help="YYYY-MM-DD:YYYY-MM-DD for the prior period")
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to seo-targets.json")
    p.add_argument(
        "--manual",
        default=str(DEFAULT_MANUAL_PATH),
        help="Path to manual-metrics.json (absent is fine; surfaces render as gaps)",
    )
    p.add_argument("--out-dir", help="Output directory (default: report.output_dir from config)")
    p.add_argument(
        "--no-csv", action="store_true", help="Write only the Markdown report"
    )
    p.add_argument(
        "--stdout", action="store_true", help="Also print the Markdown to stdout"
    )
    p.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit 2 if any target query dropped off page 1 or a HIGH cannibalization "
        "finding is present. For use as a CI gate.",
    )
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    try:
        cfg = load_config(args.config)
    except ConfigError as e:
        print(f"::error::invalid config: {e}", file=sys.stderr)
        return 1

    try:
        cur_start, cur_end = parse_range(args.current_range)
        pri_start, pri_end = parse_range(args.prior_range)
    except ValueError as e:
        print(f"::error::{e}", file=sys.stderr)
        return 1

    try:
        current = load_period(args.current, "current", cur_start, cur_end)
        prior = load_period(args.prior, "prior", pri_start, pri_end)
    except (IngestError, FileNotFoundError, ValueError) as e:
        print(f"::error::could not read input: {e}", file=sys.stderr)
        return 1

    if not current.rows:
        print(f"::error::{args.current} contained no usable rows", file=sys.stderr)
        return 1

    manual = load_manual_metrics(args.manual)
    analysis = build_analysis(current, prior, cfg, manual)

    out_dir = Path(args.out_dir) if args.out_dir else REPO_ROOT / cfg.report.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = current.end or current.label
    md_path = out_dir / f"seo-report-{stamp}.md"
    markdown = render_markdown(analysis)
    md_path.write_text(markdown, encoding="utf-8")

    written = [md_path]
    if not args.no_csv:
        written.extend(write_csvs(analysis, out_dir))

    movement = analysis["movement"]
    print(f"Report period : {current.date_range} vs {prior.date_range}")
    print(f"Target queries: {len(cfg.queries)}")
    print(
        f"Movement      : +{movement.counts['entered_page1']} onto page 1, "
        f"-{movement.counts['left_page1']} off page 1, "
        f"{movement.counts['striking_distance']} in striking distance"
    )
    print(f"Cannibalized  : {len(analysis['cannibalization'])} queries")
    print(f"Manual gaps   : {analysis['manual']['missing_count']}")
    for path in written:
        print(f"  wrote {path}")

    if args.stdout:
        print()
        print(markdown)

    if args.fail_on_regression:
        high = [f for f in analysis["cannibalization"] if f.severity == "high"]
        dropped = movement.left_page1
        if high or dropped:
            print(
                f"::error::regression gate: {len(dropped)} queries dropped off page 1, "
                f"{len(high)} HIGH cannibalization findings",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
