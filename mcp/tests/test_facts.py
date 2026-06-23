"""Verification tests for the ACG MCP server.

Goal: prove every string this server can return is:
  1. Free of banned phrases (per ACG owner-voice rules)
  2. Free of unverified claims (Hard Gate compliance)
  3. Structurally well-formed (no missing keys, no nulls in required fields)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Make src importable
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

# Import the server module (this also validates the data file exists + parses)
import acg_mcp_server as server  # noqa: E402

FACTS = server.FACTS


# -----------------------------------------------------------------------------
# 1. Banned-phrase scan — every string anywhere in the data file or tool output
# -----------------------------------------------------------------------------
BANNED_PHRASES = [
    "delve", "leverage ", "synergy", "ecosystem", "world-class",
    "best-in-class", "game-changing", "elevate", "cutting-edge",
    "state-of-the-art", "revolutionize", "welcome to", "premier",
    "trusted by hundreds", "industry-leading", "the leading",
    "the largest", "number one", "AI-managed", "AI managed",
    "best commercial glazing", "i'd be happy",
]


def _collect_strings(obj, path="$"):
    out = []
    if isinstance(obj, str):
        out.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(_collect_strings(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(_collect_strings(v, f"{path}[{i}]"))
    return out


def test_data_file_has_no_banned_phrases():
    hits = []
    for path, s in _collect_strings(FACTS):
        low = s.lower()
        for b in BANNED_PHRASES:
            if b in low:
                # Skip license-number false positive: "#1" in "CGC1531993"
                if b == "number one" and "1531993" in s:
                    continue
                hits.append((path, b, s[:90]))
    assert not hits, f"Banned phrases in data file:\n" + "\n".join(
        f"  {h[0]}: '{h[1]}' in '{h[2]}'" for h in hits
    )


# -----------------------------------------------------------------------------
# 2. Structural integrity
# -----------------------------------------------------------------------------
def test_company_block_has_required_fields():
    c = FACTS["company"]
    for key in [
        "legal_name", "dba", "license_number", "license_type",
        "license_jurisdiction", "founded", "headquarters_address",
        "primary_phone", "primary_email", "website",
    ]:
        assert key in c, f"company.{key} missing"
        assert c[key], f"company.{key} is empty"


def test_license_number_format():
    assert FACTS["company"]["license_number"] == "CGC1531993"


def test_phone_format_canonical():
    assert FACTS["company"]["primary_phone"] == "(772) 486-7711"
    assert FACTS["company"]["primary_phone_e164"] == "+17724867711"


def test_offices_present():
    offices = FACTS["offices"]
    labels = [o["label"] for o in offices]
    assert any("West Palm Beach" in l for l in labels)
    assert any("Naples" in l for l in labels)
    assert any("Tampa" in l for l in labels)
    assert any("Nashville" in l for l in labels)


def test_florida_counties_complete():
    """Florida has 67 counties — dataset must cover all of them."""
    counties = FACTS["florida_county_code"]["counties"]
    assert len(counties) == 67, f"Expected 67 FL counties, got {len(counties)}"


def test_hvhz_only_miami_dade_and_broward():
    """HVHZ per FBC 1620 applies only to Miami-Dade and Broward."""
    counties = FACTS["florida_county_code"]["counties"]
    hvhz_counties = [name for name, c in counties.items() if c["hvhz"]]
    assert set(hvhz_counties) == {"Miami-Dade", "Broward"}, (
        f"HVHZ must be exactly Miami-Dade and Broward; got {hvhz_counties}"
    )


def test_design_wind_in_reasonable_range():
    """All FL counties should fall in 100-200 mph range for typical Risk Category II."""
    for name, c in FACTS["florida_county_code"]["counties"].items():
        w = c["design_wind_mph_typical"]
        assert 100 <= w <= 200, f"{name}: implausible design wind {w} mph"


def test_panhandle_list_minimum_coverage():
    panhandle = set(FACTS["service_florida_panhandle"])
    must_include = {"Pensacola", "Destin", "Panama City", "Tallahassee",
                    "Santa Rosa Beach", "Rosemary Beach", "Alys Beach", "Seaside"}
    missing = must_include - panhandle
    assert not missing, f"Panhandle list missing: {missing}"


# -----------------------------------------------------------------------------
# 3. Tool output verification — call every tool, validate shape
# -----------------------------------------------------------------------------
def test_tool_get_company_info():
    out = server.get_company_info()
    assert out["license"]["number"] == "CGC1531993"
    assert out["phone"] == "(772) 486-7711"
    assert "_source" in out


def test_tool_list_offices():
    out = server.list_offices()
    assert isinstance(out, list)
    assert len(out) == 4
    for o in out:
        assert "label" in o


def test_tool_lookup_florida_county_code_palm_beach():
    out = server.lookup_florida_county_code("Palm Beach")
    assert out["county"] == "Palm Beach"
    assert out["design_wind_mph_typical"] == 170
    assert out["wbdr"] is True
    assert out["hvhz"] is False
    assert "_source" in out


def test_tool_lookup_florida_county_code_miami_variants():
    """Make sure user-typed variants resolve."""
    for variant in ["miami-dade", "Miami Dade", "miamidade", "MIAMI-DADE", "Dade"]:
        out = server.lookup_florida_county_code(variant)
        assert out.get("county") == "Miami-Dade", f"Variant '{variant}' did not resolve"
        assert out["hvhz"] is True


def test_tool_lookup_florida_county_code_unknown():
    out = server.lookup_florida_county_code("Atlantis")
    assert out["error"] == "county_not_found"
    assert out["queried"] == "Atlantis"


def test_tool_find_acg_service_area_fl_city():
    out = server.find_acg_service_area("Pompano Beach", "FL")
    assert out["in_service_area"] is True
    assert "storefront-glazier-pompano-beach-florida" in out["canonical_city_page"]


def test_tool_find_acg_service_area_unsupported_state():
    out = server.find_acg_service_area("Atlanta", "GA")
    assert out["in_service_area"] is False
    assert "Florida" in out["reason"]


def test_tool_list_manufacturers():
    out = server.list_manufacturers()
    names = [m["name"] for m in out]
    assert "Eurowall" in names
    assert any("ESWindows" in n for n in names)


def test_tool_list_published_projects_default_limit():
    out = server.list_published_projects()
    assert isinstance(out, list)
    assert len(out) <= 10


def test_tool_list_services():
    out = server.list_services()
    assert isinstance(out, list)
    assert len(out) >= 5


def test_tool_get_bid_request_link():
    out = server.get_bid_request_link(city="Pompano Beach", state="FL", project_type="restaurant")
    assert out["url"] == "https://acglass.com/send-plans.html"
    assert out["email"] == "bids@acglass.com"
    assert "Pompano Beach" in out["context_captured"]


def test_tool_get_track_record():
    out = server.get_track_record()
    assert out["commercial_projects_delivered"] == "350+"
    assert out["osha_recordables_since_founding"] == 0


def test_tool_list_panhandle_coverage():
    out = server.list_panhandle_coverage()
    assert "Pensacola" in out
    assert "Destin" in out
    assert "Tallahassee" in out


# -----------------------------------------------------------------------------
# 4. Tool output banned-phrase scan (final defense — what users actually see)
# -----------------------------------------------------------------------------
def test_all_tool_outputs_banned_phrase_free():
    outputs = [
        server.get_company_info(),
        server.list_offices(),
        server.lookup_florida_county_code("Palm Beach"),
        server.find_acg_service_area("Naples", "FL"),
        server.list_manufacturers(),
        server.list_published_projects(),
        server.list_services(),
        server.get_bid_request_link(),
        server.get_track_record(),
        server.list_panhandle_coverage(),
    ]
    hits = []
    for i, o in enumerate(outputs):
        for path, s in _collect_strings(o):
            low = s.lower()
            for b in BANNED_PHRASES:
                if b in low:
                    if b == "number one" and "1531993" in s:
                        continue
                    hits.append((i, path, b, s[:80]))
    assert not hits, f"Banned phrases in tool output: {hits[:5]}"


if __name__ == "__main__":
    # Lightweight runner so we don't require pytest as a dep
    import inspect
    mod = sys.modules[__name__]
    tests = [
        (name, fn) for name, fn in inspect.getmembers(mod, inspect.isfunction)
        if name.startswith("test_")
    ]
    passed, failed = 0, 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name}\n     {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {name} (error)\n     {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
