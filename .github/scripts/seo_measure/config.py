"""Load and validate .github/seo/seo-targets.json."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / ".github" / "seo" / "seo-targets.json"
DEFAULT_MANUAL_PATH = REPO_ROOT / ".github" / "seo" / "manual-metrics.json"


class ConfigError(ValueError):
    """Raised when seo-targets.json is missing required structure."""


def normalize_query(value: str) -> str:
    """Queries are compared case- and whitespace-insensitively.

    GSC lowercases queries already, but hand-edited config entries and CSV
    exports from other tools do not reliably agree on case or inner spacing.
    """
    return " ".join(value.lower().split())


def normalize_path(value: str) -> str:
    """Reduce a page URL to a site-root-relative path for cross-source joins.

    GSC reports full URLs, seo-targets.json lists paths, and CSV exports vary on
    trailing slash and index.html. All three must land on the same key.
    """
    if not value:
        return ""
    path = value.strip()
    for prefix in ("https://", "http://"):
        if path.lower().startswith(prefix):
            rest = path[len(prefix):]
            slash = rest.find("/")
            path = rest[slash:] if slash != -1 else "/"
            break
    path = path.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        path = "/" + path
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return path or "/"


@dataclass(frozen=True)
class TargetQuery:
    query: str
    group_id: str
    group_label: str
    market: str | None = None

    @property
    def key(self) -> str:
        return normalize_query(self.query)


@dataclass(frozen=True)
class Market:
    id: str
    label: str


@dataclass(frozen=True)
class TargetPage:
    path: str
    label: str
    role: str
    market: str | None = None

    @property
    def key(self) -> str:
        return normalize_path(self.path)


@dataclass
class Thresholds:
    page1_max_position: float = 10.0
    page2_max_position: float = 20.0
    page3_max_position: float = 30.0
    striking_min_position: float = 10.0
    striking_max_position: float = 30.0
    movement_min_impressions: int = 10
    material_position_delta: float = 1.0
    cann_min_urls: int = 2
    cann_min_impressions_per_url: int = 5
    cann_min_impression_share: float = 0.1
    cann_high_page1_urls: int = 2
    cann_high_min_share: float = 0.3

    def band(self, position: float | None) -> str:
        """Map an average position onto a SERP page band."""
        if position is None:
            return "unranked"
        if position <= self.page1_max_position:
            return "page1"
        if position <= self.page2_max_position:
            return "page2"
        if position <= self.page3_max_position:
            return "page3"
        return "beyond"

    def is_striking_distance(self, position: float | None) -> bool:
        if position is None:
            return False
        return self.striking_min_position < position <= self.striking_max_position


@dataclass
class ReportSettings:
    top_n_movers: int = 10
    top_n_pages: int = 20
    output_dir: str = ".github/seo/reports"


@dataclass
class TargetConfig:
    gsc_property: str
    thresholds: Thresholds
    report: ReportSettings
    queries: list[TargetQuery] = field(default_factory=list)
    markets: list[Market] = field(default_factory=list)
    pages: list[TargetPage] = field(default_factory=list)
    source_path: Path | None = None

    def query_by_key(self) -> dict[str, TargetQuery]:
        return {q.key: q for q in self.queries}

    @property
    def group_order(self) -> list[tuple[str, str]]:
        seen: dict[str, str] = {}
        for q in self.queries:
            seen.setdefault(q.group_id, q.group_label)
        return list(seen.items())


def _require(data: dict, key: str, ctx: str):
    if key not in data:
        raise ConfigError(f"{ctx}: missing required key '{key}'")
    return data[key]


def _parse_thresholds(raw: dict) -> Thresholds:
    striking = raw.get("striking_distance", {})
    movement = raw.get("movement", {})
    cann = raw.get("cannibalization", {})
    t = Thresholds(
        page1_max_position=float(raw.get("page1_max_position", 10.0)),
        page2_max_position=float(raw.get("page2_max_position", 20.0)),
        page3_max_position=float(raw.get("page3_max_position", 30.0)),
        striking_min_position=float(striking.get("min_position", 10.0)),
        striking_max_position=float(striking.get("max_position", 30.0)),
        movement_min_impressions=int(movement.get("min_impressions", 10)),
        material_position_delta=float(movement.get("material_position_delta", 1.0)),
        cann_min_urls=int(cann.get("min_urls", 2)),
        cann_min_impressions_per_url=int(cann.get("min_impressions_per_url", 5)),
        cann_min_impression_share=float(cann.get("min_impression_share_per_url", 0.1)),
        cann_high_page1_urls=int(cann.get("high_severity_page1_urls", 2)),
        cann_high_min_share=float(cann.get("high_severity_min_share", 0.3)),
    )
    if not t.page1_max_position < t.page2_max_position < t.page3_max_position:
        raise ConfigError(
            "thresholds: page1/page2/page3 max positions must be strictly increasing"
        )
    if t.cann_min_urls < 2:
        raise ConfigError("thresholds.cannibalization.min_urls must be >= 2")
    return t


def _parse_queries(groups: list) -> list[TargetQuery]:
    out: list[TargetQuery] = []
    seen: set[str] = set()
    for group in groups:
        gid = _require(group, "id", "query_groups[]")
        label = group.get("label", gid)
        for entry in group.get("queries", []):
            if isinstance(entry, str):
                text, market = entry, None
            elif isinstance(entry, dict):
                text = _require(entry, "query", f"query_groups[{gid}].queries[]")
                market = entry.get("market")
            else:
                raise ConfigError(
                    f"query_groups[{gid}]: query entries must be a string or an object"
                )
            tq = TargetQuery(text, gid, label, market)
            if tq.key in seen:
                raise ConfigError(f"duplicate target query across groups: {text!r}")
            seen.add(tq.key)
            out.append(tq)
    if not out:
        raise ConfigError("query_groups: no target queries defined")
    return out


def load_config(path: str | Path | None = None) -> TargetConfig:
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not cfg_path.exists():
        raise ConfigError(f"config not found: {cfg_path}")
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))

    prop = _require(raw, "property", "seo-targets.json")
    markets = [
        Market(
            id=_require(m, "id", "markets[]"),
            label=m.get("label", m.get("id", "")),
        )
        for m in raw.get("markets", [])
    ]
    pages = [
        TargetPage(
            path=_require(p, "path", "pages[]"),
            label=p.get("label", p.get("path", "")),
            role=p.get("role", "unclassified"),
            market=p.get("market"),
        )
        for p in raw.get("pages", [])
    ]
    queries = _parse_queries(_require(raw, "query_groups", "seo-targets.json"))

    known_markets = {m.id for m in markets}
    for q in queries:
        if q.market and q.market not in known_markets:
            raise ConfigError(f"query {q.query!r} references unknown market {q.market!r}")
    for p in pages:
        if p.market and p.market not in known_markets:
            raise ConfigError(f"page {p.path!r} references unknown market {p.market!r}")

    rep = raw.get("report", {})
    return TargetConfig(
        gsc_property=_require(prop, "gsc_property", "property"),
        thresholds=_parse_thresholds(raw.get("thresholds", {})),
        report=ReportSettings(
            top_n_movers=int(rep.get("top_n_movers", 10)),
            top_n_pages=int(rep.get("top_n_pages", 20)),
            output_dir=rep.get("output_dir", ".github/seo/reports"),
        ),
        queries=queries,
        markets=markets,
        pages=pages,
        source_path=cfg_path,
    )
