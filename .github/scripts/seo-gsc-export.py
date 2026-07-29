#!/usr/bin/env python3
"""seo-gsc-export.py - Export Search Console metrics to JSON snapshots.

Optional companion to seo-report.py. If you already export CSVs from the GSC UI,
you do not need this script at all - seo-report.py reads those directly.

Credentials come from the environment only, using the same GSC_SA_JSON secret
that .github/scripts/seo-pulse.py already relies on. Nothing is written to disk
except the metric snapshots, and no credential is ever echoed.

  GSC_SA_JSON                     inline service-account JSON, or
  GOOGLE_APPLICATION_CREDENTIALS  path to a service-account JSON file

The service account needs read access to the property in Search Console.

Usage:
  # Last complete week plus the week before it, both dimensioned query+page
  python3 .github/scripts/seo-gsc-export.py --weekly --out-dir .github/seo/data

  # An explicit window
  python3 .github/scripts/seo-gsc-export.py \
      --start 2026-07-20 --end 2026-07-26 --out .github/seo/data/current.json

Exit codes: 0 ok, 1 missing credentials or bad arguments, 3 API/dependency error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo_measure.config import ConfigError, DEFAULT_CONFIG_PATH, load_config
from seo_measure.ingest import load_api_json, write_snapshot

# Search Console finalizes data on a 2-3 day lag; anything newer is incomplete.
GSC_LAG_DAYS = 3
API_ROW_LIMIT = 25000


def load_credentials():
    """Build read-only Search Console credentials from the environment."""
    inline = os.environ.get("GSC_SA_JSON")
    cred_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    # Checked before importing, so a missing secret reports the missing secret
    # rather than a missing library.
    if not inline and not (cred_file and Path(cred_file).exists()):
        print(
            "::error::no credentials. Set GSC_SA_JSON (inline service-account JSON) or "
            "GOOGLE_APPLICATION_CREDENTIALS (path to one). Never commit either.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        from google.oauth2 import service_account
    except ImportError:
        print(
            "::error::missing dependency. pip install google-api-python-client google-auth",
            file=sys.stderr,
        )
        raise SystemExit(3)

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    if inline:
        try:
            info = json.loads(inline)
        except json.JSONDecodeError:
            print(
                "::error::GSC_SA_JSON is set but is not valid JSON.", file=sys.stderr
            )
            raise SystemExit(1)
        return service_account.Credentials.from_service_account_info(info, scopes=scopes)

    return service_account.Credentials.from_service_account_file(cred_file, scopes=scopes)


def build_service(credentials):
    try:
        from googleapiclient.discovery import build
    except ImportError:
        print(
            "::error::missing dependency. pip install google-api-python-client google-auth",
            file=sys.stderr,
        )
        raise SystemExit(3)
    return build("searchconsole", "v1", credentials=credentials, cache_discovery=False)


def fetch(service, prop: str, start: date, end: date, dimensions: list[str]) -> dict:
    """Page through searchanalytics.query until the API stops returning rows."""
    rows: list[dict] = []
    offset = 0
    while True:
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": dimensions,
            "rowLimit": API_ROW_LIMIT,
            "startRow": offset,
        }
        resp = service.searchanalytics().query(siteUrl=prop, body=body).execute()
        batch = resp.get("rows", [])
        rows.extend(batch)
        if len(batch) < API_ROW_LIMIT:
            break
        offset += len(batch)
    return {"rows": rows, "dimensions": dimensions, "source": f"gsc-api:{prop}"}


def weekly_windows(anchor: date) -> tuple[tuple[date, date], tuple[date, date]]:
    """The last complete 7-day window ending before the GSC lag, and the one prior."""
    end = anchor - timedelta(days=GSC_LAG_DAYS)
    start = end - timedelta(days=6)
    prior_end = start - timedelta(days=1)
    prior_start = prior_end - timedelta(days=6)
    return (start, end), (prior_start, prior_end)


def export_window(service, prop, start, end, dimensions, out_path, label) -> Path:
    payload = fetch(service, prop, start, end, dimensions)
    payload["period"] = {
        "label": label,
        "start": start.isoformat(),
        "end": end.isoformat(),
    }
    period = load_api_json(payload, label, start.isoformat(), end.isoformat())
    written = write_snapshot(period, out_path)
    print(f"  {label}: {start} to {end} - {len(period.rows):,} rows -> {written}")
    return written


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Export GSC Search Analytics to JSON snapshots.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    p.add_argument("--property", help="Override the gsc_property from the config")
    p.add_argument(
        "--dimensions",
        default="query,page",
        help="Comma-separated GSC dimensions. query+page is required for "
        "cannibalization detection (default: query,page)",
    )
    p.add_argument(
        "--weekly",
        action="store_true",
        help="Export the last complete week and the week before it as current.json "
        "and prior.json",
    )
    p.add_argument("--start", help="YYYY-MM-DD (single-window mode)")
    p.add_argument("--end", help="YYYY-MM-DD (single-window mode)")
    p.add_argument("--out", help="Output path (single-window mode)")
    p.add_argument("--out-dir", default=".github/seo/data", help="Output dir (--weekly)")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    try:
        cfg = load_config(args.config)
    except ConfigError as e:
        print(f"::error::invalid config: {e}", file=sys.stderr)
        return 1

    prop = args.property or cfg.gsc_property
    dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    if not dimensions:
        print("::error::--dimensions must name at least one dimension", file=sys.stderr)
        return 1

    if not args.weekly and not (args.start and args.end and args.out):
        print(
            "::error::use --weekly, or supply all of --start --end --out",
            file=sys.stderr,
        )
        return 1

    service = build_service(load_credentials())
    print(f"Property  : {prop}")
    print(f"Dimensions: {', '.join(dimensions)}")

    try:
        if args.weekly:
            out_dir = Path(args.out_dir)
            (cur_start, cur_end), (pri_start, pri_end) = weekly_windows(date.today())
            export_window(
                service, prop, cur_start, cur_end, dimensions,
                out_dir / "current.json", "current",
            )
            export_window(
                service, prop, pri_start, pri_end, dimensions,
                out_dir / "prior.json", "prior",
            )
        else:
            start = date.fromisoformat(args.start)
            end = date.fromisoformat(args.end)
            if start > end:
                print("::error::--start is after --end", file=sys.stderr)
                return 1
            export_window(service, prop, start, end, dimensions, Path(args.out), "window")
    except ValueError as e:
        print(f"::error::bad date: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"::error::Search Console API call failed: {e}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
