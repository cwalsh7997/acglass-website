"""Match owner-approved public copy by metric, path and exact source hash."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


REGISTRY = ".github/seo/public-metrics-2026-10-24.json"


def load_registry(root):
    path = Path(root) / REGISTRY
    if not path.is_file():
        return []
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("public metric approval registry must be an object")
    if data.get("approval", {}).get("answer_exact") != "All three are current and cleared":
        raise ValueError("public metric approval record is incomplete")
    rows = data.get("approved_source_surfaces")
    if not isinstance(rows, list):
        raise ValueError("approved metric surfaces are missing")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("approved metric surface must be an object")
        if not all(isinstance(row.get(k), str) and row[k] for k in ("kind", "path", "sha256")):
            raise ValueError("approved metric surface has an invalid identity")
        if row.get("max_occurrences") != 1:
            raise ValueError("approved metric surface must have one bounded occurrence")
        if hashlib.sha256(row.get("source_text", "").encode()).hexdigest() != row["sha256"]:
            raise ValueError("approved metric surface does not match its source hash")
    return rows


def approved(rows, kind, path, source_text, used):
    digest = hashlib.sha256(source_text.encode()).hexdigest()
    identity = (kind, path, digest)
    match = next((r for r in rows if (r["kind"], r["path"], r["sha256"]) == identity), None)
    if not match or used.get(identity, 0) >= match["max_occurrences"]:
        return False
    used[identity] = used.get(identity, 0) + 1
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("kind")
    args = parser.parse_args()
    try:
        rows = load_registry(args.root)
    except (ValueError, OSError) as exc:
        # Emit a finding rather than silently converting a damaged registry
        # into a successful empty grep stream.
        print("approval-registry:0:" + str(exc))
        return 1
    used = {}
    for line in sys.stdin:
        line = line.rstrip("\r\n")
        if not line:
            continue
        parts = line.split(":", 2)
        if len(parts) != 3 or not approved(rows, args.kind, parts[0], parts[2], used):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
