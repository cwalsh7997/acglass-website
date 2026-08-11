#!/usr/bin/env python3
"""Fail closed when the local NOA source ledger is missing or stale.

This checker is intentionally offline. It never contacts a government portal
and never changes public product data. A human must review the cited source and
update noa/data.json through the governed publishing workflow.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "noa" / "data.json"
REQUIRED_FIELDS = {
    "fl_pa",
    "status",
    "source_url",
    "last_verified",
}


@dataclass(frozen=True)
class Finding:
    partner: str
    system: str
    reason: str


def parse_day(value: str) -> date:
    return datetime.fromisoformat(value).date()


def audit(data: dict, today: date, max_age_days: int) -> tuple[int, list[Finding]]:
    total = 0
    findings: list[Finding] = []
    partners = data.get("partners")
    if not isinstance(partners, dict):
        return 0, [Finding("data.json", "partners", "missing partner map")]
    if not partners:
        return 0, [Finding("data.json", "partners", "partner map is empty")]

    for partner in partners.values():
        label = str(partner.get("label", "unlabeled partner"))
        systems = partner.get("systems")
        if not isinstance(systems, list):
            findings.append(Finding(label, "systems", "missing system list"))
            continue
        if not systems:
            findings.append(Finding(label, "systems", "system list is empty"))
            continue
        for row in systems:
            total += 1
            system = str(row.get("fl_pa", "unidentified system"))
            missing = sorted(REQUIRED_FIELDS - set(row))
            if missing:
                findings.append(
                    Finding(label, system, f"missing fields: {', '.join(missing)}")
                )
                continue
            source = str(row.get("source_url", "")).strip()
            if not source.startswith("https://"):
                findings.append(Finding(label, system, "source URL is not HTTPS"))
            try:
                verified = parse_day(str(row["last_verified"]))
            except ValueError:
                findings.append(Finding(label, system, "invalid last_verified date"))
                continue
            age = (today - verified).days
            if age < 0:
                findings.append(Finding(label, system, "last_verified is in the future"))
            elif age > max_age_days:
                findings.append(
                    Finding(label, system, f"source review is {age} days old")
                )
    if total == 0:
        findings.append(Finding("data.json", "systems", "no systems tracked"))
    return total, findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-age-days", type=int, default=90)
    parser.add_argument("--today", help="test override in YYYY-MM-DD format")
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    args = parser.parse_args()

    if args.max_age_days < 1:
        parser.error("--max-age-days must be positive")

    try:
        today = parse_day(args.today) if args.today else date.today()
        data = json.loads(args.data.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"NOA source ledger could not be read: {exc}")
        return 2

    total, findings = audit(data, today, args.max_age_days)
    print(f"NOA source ledger status: {today.isoformat()}")
    print(f"Systems tracked: {total}")
    print(f"Maximum source age: {args.max_age_days} days")
    print(f"Review findings: {len(findings)}")
    for finding in findings:
        print(f"  {finding.partner} | {finding.system} | {finding.reason}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
