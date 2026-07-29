"""Normalize GSC metrics from CSV exports or API-shaped JSON into one model.

Two supported inputs, both first-party:

  CSV  - what the GSC UI's "Export" button produces (Queries.csv, Pages.csv, or a
         combined query+page export from Looker Studio / the bulk export).
  JSON - the raw body of a searchanalytics.query response, or a snapshot written
         by seo-gsc-export.py.

Neither path takes credentials. Fetching from the API lives in seo-gsc-export.py
so that this module stays importable, offline, and testable.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from pathlib import Path

from .config import normalize_path, normalize_query


class IngestError(ValueError):
    """Raised when an input file cannot be interpreted as GSC metrics."""


# Header aliases seen across the GSC UI export, the bulk BigQuery export, and
# Looker Studio. Compared after lowercasing and stripping.
_QUERY_HEADERS = {"query", "queries", "top queries", "search query", "keyword"}
_PAGE_HEADERS = {"page", "pages", "top pages", "landing page", "url", "address"}
_CLICK_HEADERS = {"clicks", "url clicks", "click"}
_IMPRESSION_HEADERS = {"impressions", "impression"}
_CTR_HEADERS = {"ctr", "site ctr", "url ctr", "click through rate"}
_POSITION_HEADERS = {"position", "average position", "avg position", "avg. position"}


@dataclass(frozen=True)
class Row:
    """One GSC metric row. `query` and/or `page` may be None depending on dims."""

    query: str | None
    page: str | None
    clicks: int
    impressions: int
    ctr: float
    position: float | None

    @property
    def query_key(self) -> str | None:
        return normalize_query(self.query) if self.query else None

    @property
    def page_key(self) -> str | None:
        return normalize_path(self.page) if self.page else None


@dataclass
class Period:
    """A dated window of GSC rows."""

    label: str
    start: str | None = None
    end: str | None = None
    rows: list[Row] = field(default_factory=list)
    dimensions: tuple[str, ...] = ()
    source: str = "unknown"

    @property
    def has_page_dimension(self) -> bool:
        return "page" in self.dimensions

    @property
    def has_query_dimension(self) -> bool:
        return "query" in self.dimensions

    @property
    def date_range(self) -> str:
        if self.start and self.end:
            return f"{self.start} to {self.end}"
        return self.label

    def totals(self) -> dict[str, float]:
        return aggregate(self.rows)


def _looks_like_path(value) -> bool:
    """Distinguish a filename from inline document text.

    Inline CSV and JSON always span multiple lines, so a single-line string is a
    path. Without this a mistyped filename would be parsed as content and fail
    with a confusing header error instead of 'file not found'.
    """
    if isinstance(value, Path):
        return True
    if not isinstance(value, str):
        return False
    return "\n" not in value.strip()


def _num(value, default=0.0) -> float:
    """Parse a metric cell. Tolerates thousands separators and empty cells."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace(" ", "")
    if not text or text == "-":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def _pct(value) -> float:
    """Parse a CTR cell. '3.4%' -> 0.034; 0.034 -> 0.034; '3.4' -> 0.034.

    GSC's UI export writes a percent string while the API returns a ratio. A bare
    number above 1 can only be a percentage, since a ratio never exceeds 1.
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value) / 100.0 if value > 1 else float(value)
    text = str(value).strip()
    if not text:
        return 0.0
    if text.endswith("%"):
        return _num(text[:-1]) / 100.0
    n = _num(text)
    return n / 100.0 if n > 1 else n


def aggregate(rows) -> dict[str, float]:
    """Roll rows up to clicks/impressions/ctr/position.

    Average position is impression-weighted: GSC's own position figure is a
    per-impression average, so a plain mean across rows would over-weight
    low-volume long-tail rows.
    """
    clicks = sum(r.clicks for r in rows)
    impressions = sum(r.impressions for r in rows)
    weighted = sum(
        (r.position or 0.0) * r.impressions for r in rows if r.position is not None
    )
    weight = sum(r.impressions for r in rows if r.position is not None)
    return {
        "clicks": clicks,
        "impressions": impressions,
        "ctr": (clicks / impressions) if impressions else 0.0,
        "position": (weighted / weight) if weight else None,
    }


def _match_header(header: str, alias_set: set[str]) -> bool:
    return header.strip().strip('"').lower() in alias_set


def _resolve_columns(fieldnames) -> dict[str, str]:
    """Map canonical metric names onto this file's actual column names."""
    resolved: dict[str, str] = {}
    for name in fieldnames or []:
        if name is None:
            continue
        for canonical, aliases in (
            ("query", _QUERY_HEADERS),
            ("page", _PAGE_HEADERS),
            ("clicks", _CLICK_HEADERS),
            ("impressions", _IMPRESSION_HEADERS),
            ("ctr", _CTR_HEADERS),
            ("position", _POSITION_HEADERS),
        ):
            if canonical not in resolved and _match_header(name, aliases):
                resolved[canonical] = name
    return resolved


def load_csv(
    path_or_text, label: str, start: str | None = None, end: str | None = None
) -> Period:
    """Read a GSC CSV export into a Period.

    Accepts a path or raw CSV text. Dimensions are inferred from the headers, so
    the same function handles a query-only, page-only, or query+page export.
    """
    if _looks_like_path(path_or_text):
        p = Path(str(path_or_text))
        if not p.exists():
            raise IngestError(f"file not found: {p}")
        text = p.read_text(encoding="utf-8-sig")
        origin = str(p)
    else:
        text = str(path_or_text)
        origin = "inline-csv"

    reader = csv.DictReader(io.StringIO(text))
    cols = _resolve_columns(reader.fieldnames)
    if "query" not in cols and "page" not in cols:
        raise IngestError(
            f"{origin}: no query or page column found. "
            f"Saw headers: {reader.fieldnames}"
        )
    if "impressions" not in cols and "clicks" not in cols:
        raise IngestError(
            f"{origin}: no clicks or impressions column found. "
            f"Saw headers: {reader.fieldnames}"
        )

    rows: list[Row] = []
    for record in reader:
        query = record.get(cols["query"]) if "query" in cols else None
        page = record.get(cols["page"]) if "page" in cols else None
        if not (query or "").strip() and not (page or "").strip():
            continue
        position = (
            _num(record.get(cols["position"]), default=None)
            if "position" in cols
            else None
        )
        rows.append(
            Row(
                query=(query or "").strip() or None,
                page=(page or "").strip() or None,
                clicks=int(_num(record.get(cols.get("clicks")))),
                impressions=int(_num(record.get(cols.get("impressions")))),
                ctr=_pct(record.get(cols.get("ctr"))),
                position=position,
            )
        )

    dims = tuple(d for d in ("query", "page") if d in cols)
    return Period(
        label=label, start=start, end=end, rows=rows, dimensions=dims, source=origin
    )


def load_api_json(
    path_or_obj, label: str, start: str | None = None, end: str | None = None
) -> Period:
    """Read a searchanalytics.query response body, or a seo-gsc-export snapshot.

    API shape:      {"rows": [{"keys": [...], "clicks": n, ...}]}
    Snapshot shape: {"period": {...}, "dimensions": [...], "rows": [...]}

    The API returns dimension values positionally in `keys`, so the dimension
    list is required to interpret them. A snapshot carries its own; a bare API
    body is assumed to be ["query"] unless its keys look like URLs.
    """
    if _looks_like_path(path_or_obj):
        p = Path(str(path_or_obj))
        if not p.exists():
            raise IngestError(f"file not found: {p}")
        data = json.loads(p.read_text(encoding="utf-8"))
        origin = str(p)
    elif isinstance(path_or_obj, (str, bytes)):
        data = json.loads(path_or_obj)
        origin = "inline-json"
    else:
        data = path_or_obj
        origin = "in-memory"

    if not isinstance(data, dict):
        raise IngestError(f"{origin}: expected a JSON object at the top level")

    meta = data.get("period") or {}
    start = start or meta.get("start")
    end = end or meta.get("end")
    if label is None:
        label = meta.get("label", "period")

    raw_rows = data.get("rows")
    if raw_rows is None:
        raise IngestError(f"{origin}: no 'rows' key in payload")

    dims = data.get("dimensions")
    if dims:
        dims = [str(d).lower() for d in dims]
    else:
        dims = _infer_dimensions(raw_rows)

    rows: list[Row] = []
    for raw in raw_rows:
        query = page = None
        if "keys" in raw:
            keys = raw.get("keys") or []
            for i, dim in enumerate(dims):
                if i >= len(keys):
                    break
                if dim == "query":
                    query = keys[i]
                elif dim == "page":
                    page = keys[i]
        else:
            query = raw.get("query")
            page = raw.get("page")
        if not query and not page:
            continue
        rows.append(
            Row(
                query=query,
                page=page,
                clicks=int(_num(raw.get("clicks"))),
                impressions=int(_num(raw.get("impressions"))),
                ctr=_pct(raw.get("ctr")),
                position=_num(raw.get("position"), default=None),
            )
        )

    present = tuple(
        d for d in ("query", "page") if any(getattr(r, d) for r in rows)
    ) or tuple(d for d in dims if d in ("query", "page"))
    return Period(
        label=label,
        start=start,
        end=end,
        rows=rows,
        dimensions=present,
        source=data.get("source", origin),
    )


def _infer_dimensions(raw_rows) -> list[str]:
    """Guess dimension order for a bare API body that omitted it."""
    for raw in raw_rows:
        keys = raw.get("keys") or []
        if not keys:
            continue
        looks_url = [
            isinstance(k, str) and (k.startswith("http") or k.startswith("/"))
            for k in keys
        ]
        if len(keys) == 1:
            return ["page"] if looks_url[0] else ["query"]
        if len(keys) >= 2:
            return ["page", "query"] if looks_url[0] else ["query", "page"]
    return ["query"]


def load_period(
    path, label: str, start: str | None = None, end: str | None = None
) -> Period:
    """Dispatch on file extension."""
    suffix = Path(str(path)).suffix.lower()
    if suffix == ".csv":
        return load_csv(path, label, start, end)
    if suffix == ".json":
        return load_api_json(path, label, start, end)
    raise IngestError(f"{path}: unsupported extension {suffix!r} (expected .csv or .json)")


def write_snapshot(period: Period, path) -> Path:
    """Persist a Period as a portable JSON snapshot.

    This is the export half of the layer: it makes an API pull reproducible
    offline and diffable week over week, without re-querying.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "$schema_version": 1,
        "source": period.source,
        "dimensions": list(period.dimensions),
        "period": {
            "label": period.label,
            "start": period.start,
            "end": period.end,
        },
        "rows": [
            {
                "query": r.query,
                "page": r.page,
                "clicks": r.clicks,
                "impressions": r.impressions,
                "ctr": round(r.ctr, 6),
                "position": round(r.position, 2) if r.position is not None else None,
            }
            for r in period.rows
        ],
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out


def load_manual_metrics(path) -> dict:
    """Read manual-metrics.json, tolerating absence.

    A missing file is a normal state, not an error: the report renders every
    configured surface as 'not supplied' and lists it under Data Gaps.
    """
    p = Path(path)
    if not p.exists():
        return {"as_of": None, "sections": [], "_missing": str(p)}
    data = json.loads(p.read_text(encoding="utf-8"))
    if "sections" not in data:
        raise IngestError(f"{p}: manual metrics file has no 'sections' key")
    return data
