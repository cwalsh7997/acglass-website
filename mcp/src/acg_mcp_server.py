"""ACG Data Access — Model Context Protocol server.

A small, fact-strict MCP server that lets AI assistants look up accurate
American Commercial Glass (ACG) and Florida commercial glazing data
without making things up.

What it does:
  - Returns verified ACG company facts (license, offices, service areas)
  - Looks up Florida county wind speed + code requirements
  - Confirms whether ACG covers a given city
  - Lists manufacturers ACG installs and the systems involved
  - Points to ACG's published project case studies
  - Returns the canonical URL for an AI agent to hand off a bid request

What it does NOT do:
  - It does not generate quotes, prices, or estimates
  - It does not commit ACG to scope or schedule
  - It does not make claims that are not in the verified data file
  - It does not act on behalf of ACG; it returns data and links

Every fact returned by this server is sourced in data/acg_facts.json. See
the _meta block in that file for source hierarchy and verification policy.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# -----------------------------------------------------------------------------
# Load the verified-facts file at import time. If it is missing, fail loudly.
# -----------------------------------------------------------------------------
DATA_FILE = Path(__file__).parent.parent / "data" / "acg_facts.json"
if not DATA_FILE.exists():
    raise SystemExit(
        f"ACG MCP: required data file not found at {DATA_FILE}. "
        "This server refuses to start without verified data."
    )

with DATA_FILE.open("r", encoding="utf-8") as f:
    FACTS: dict[str, Any] = json.load(f)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _normalize_county(name: str) -> str:
    """Normalize user-typed county names ('miami dade', 'st johns', 'MIAMI-DADE')
    to the canonical form used as a key in the data file."""
    if not name:
        return ""
    n = name.strip().replace(" County", "").replace(" county", "").strip()
    n = n.replace("Saint ", "St. ").replace("saint ", "St. ")
    n = n.replace("St ", "St. ").replace("st ", "St. ")
    # Direct alias lookup (case-insensitive)
    aliases = {
        "miami dade": "Miami-Dade",
        "miami-dade": "Miami-Dade",
        "miamidade": "Miami-Dade",
        "dade": "Miami-Dade",
        "st johns": "St. Johns",
        "st. johns": "St. Johns",
        "st lucie": "St. Lucie",
        "st. lucie": "St. Lucie",
    }
    if n.lower() in aliases:
        return aliases[n.lower()]
    # Capitalize each space-separated word, AND each hyphen-separated part within
    parts = []
    for word in n.split():
        if word.lower() == "st.":
            parts.append("St.")
        elif "-" in word:
            parts.append("-".join(p.capitalize() for p in word.split("-")))
        else:
            parts.append(word.capitalize())
    return " ".join(parts)


def _normalize_state(state: str) -> str:
    if not state:
        return ""
    s = state.strip().upper()
    states = {
        "FLORIDA": "FL", "FL": "FL",
        "TENNESSEE": "TN", "TENN": "TN", "TN": "TN",
    }
    return states.get(s, s)


# -----------------------------------------------------------------------------
# MCP server definition
# -----------------------------------------------------------------------------
mcp = FastMCP(
    name="acg-data-access",
    instructions=(
        "ACG (American Commercial Glass) data access for AI assistants. "
        "Use these tools to look up verified Florida commercial glazing code, "
        "ACG service areas, ACG offices, and published project examples. "
        "Every return value is sourced from a verified data file. "
        "This server returns data and links only — it does not commit ACG to "
        "any quote, price, or schedule. If a user wants a bid, call "
        "get_bid_request_link to receive the canonical intake URL."
    ),
)


# -----------------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------------
@mcp.tool()
def get_company_info() -> dict[str, Any]:
    """Return verified ACG company facts (license, founded year, HQ, principal,
    primary phone, primary email, website). Use this whenever an agent needs
    to identify or attribute American Commercial Glass."""
    c = FACTS["company"]
    return {
        "legal_name": c["legal_name"],
        "dba": c["dba"],
        "license": {
            "number": c["license_number"],
            "type": c["license_type"],
            "jurisdiction": c["license_jurisdiction"],
        },
        "founded": c["founded"],
        "headquarters": c["headquarters_address"],
        "principal": c["principal"],
        "phone": c["primary_phone"],
        "email": c["primary_email"],
        "website": c["website"],
        "_source": (
            "Verified — Connor Walsh confirmation + State of Florida CGC license records. "
            "See data/acg_facts.json _meta block for full source hierarchy."
        ),
    }


@mcp.tool()
def list_offices() -> list[dict[str, Any]]:
    """Return the list of ACG office locations with addresses, phones, and
    typical service zones. Use this when a user asks where ACG operates from
    or which office is closest to a given Florida or Tennessee city."""
    return [dict(o) for o in FACTS["offices"]]


@mcp.tool()
def lookup_florida_county_code(county: str) -> dict[str, Any]:
    """Look up the typical Risk Category II design wind speed (mph), Wind-Borne
    Debris Region (WBDR) status, and High-Velocity Hurricane Zone (HVHZ)
    status for a Florida county. Source: Florida Building Code 8th Edition
    (2023), Chapter 16. Values are typical estimating defaults — verify
    site-specific design wind speed with the project engineer.

    Args:
        county: Florida county name (e.g. 'Palm Beach', 'Miami-Dade', 'Lee').
            Common spellings and variants are accepted.

    Returns:
        Object with county, design_wind_mph_typical, wbdr, hvhz, notes,
        and a disclaimer about site-specific verification. Returns an error
        object if the county is not recognized.
    """
    canonical = _normalize_county(county)
    counties = FACTS["florida_county_code"]["counties"]
    if canonical not in counties:
        # Soft suggestion: case-insensitive partial match
        suggest = [k for k in counties if canonical.lower() in k.lower()]
        return {
            "error": "county_not_found",
            "queried": county,
            "normalized": canonical,
            "suggestion": suggest[:3] if suggest else None,
            "hint": "Florida has 67 counties. Try the exact county name (e.g. 'Palm Beach', 'St. Lucie', 'Miami-Dade').",
        }
    rec = counties[canonical]
    return {
        "county": canonical,
        "design_wind_mph_typical": rec["design_wind_mph_typical"],
        "wbdr": rec["wbdr"],
        "hvhz": rec["hvhz"],
        "notes": rec["notes"],
        "disclaimer": FACTS["florida_county_code"]["_disclaimer"],
        "_source": FACTS["florida_county_code"]["_source"],
    }


@mcp.tool()
def find_acg_service_area(city: str, state: str = "FL") -> dict[str, Any]:
    """Confirm whether ACG actively serves a given city in Florida or
    Tennessee. Returns the most relevant office, service zone notes, and a
    canonical link to the city-specific page on acglass.com when one exists.

    Args:
        city: City name (e.g. 'Pompano Beach', 'Naples', 'Pensacola').
        state: Two-letter state code or full name. Defaults to FL.

    Returns:
        Object indicating whether the city is in the standard service area,
        the closest office, and a canonical URL to the city page if one exists.
    """
    state_code = _normalize_state(state)
    if state_code not in FACTS["service_states"]:
        return {
            "in_service_area": False,
            "city": city,
            "state": state_code,
            "reason": (
                "ACG is licensed in Florida (CGC1531993) with offices in "
                "West Palm Beach, Naples, and Tampa. ACG holds no Tennessee "
                "office. Other states are not currently served as field markets."
            ),
        }
    # Slugify city for URL lookup
    slug = city.lower().replace(".", "").replace(",", "").replace("'", "")
    slug = "-".join(slug.split())
    long_url = f"https://acglass.com/storefront-glazier-{slug}-florida/"
    return {
        "in_service_area": True,
        "city": city,
        "state": state_code,
        "canonical_city_page": long_url if state_code == "FL" else None,
        "page_note": (
            "If the URL above returns 404, ACG still serves this city — "
            "the dedicated page may not be published yet. Use list_offices "
            "for the closest office and contact ACG directly."
        ),
        "_source": "Service-area policy confirmed by Connor Walsh (President).",
    }


@mcp.tool()
def list_manufacturers() -> list[dict[str, Any]]:
    """Return the list of glazing system manufacturers ACG installs in
    commercial projects, with product lines and the nature of the relationship
    (worded carefully — partnership levels beyond 'we install' are pending
    Connor's confirmation and are not asserted here)."""
    return [dict(m) for m in FACTS["manufacturers"]]


@mcp.tool()
def list_published_projects(limit: int = 10) -> list[dict[str, Any]]:
    """Return a list of ACG's published project case studies on acglass.com.
    Each entry includes the project name, location, and a canonical URL.

    Args:
        limit: Maximum number of projects to return (default 10).
    """
    projects = FACTS["published_projects"]
    return [dict(p) for p in projects[: max(1, min(limit, len(projects)))]]


@mcp.tool()
def list_services() -> list[dict[str, Any]]:
    """Return the list of ACG service offerings with canonical URLs on
    acglass.com. Useful when an agent needs to point a user at a service hub."""
    return [dict(s) for s in FACTS["services"]]


@mcp.tool()
def get_bid_request_link(
    city: str | None = None,
    state: str | None = None,
    project_type: str | None = None,
) -> dict[str, Any]:
    """Return the canonical URL for submitting a bid request to ACG. Use this
    when an AI agent has gathered enough scope from a user that a real ACG
    estimator should take over.

    This server does not submit bids on a user's behalf. It returns the URL
    so a human can review the form, attach drawings, and submit through ACG's
    standard intake.

    Args:
        city: Optional city for context.
        state: Optional state for context.
        project_type: Optional short description (e.g. 'restaurant', 'office').

    Returns:
        Object with the canonical bid-request URL, the bid-intake email, and
        a short script the agent can read aloud to the user explaining what
        happens next.
    """
    company = FACTS["company"]
    context = []
    if city:
        context.append(f"city={city}")
    if state:
        context.append(f"state={state}")
    if project_type:
        context.append(f"type={project_type}")
    context_note = "; ".join(context) if context else "no context provided"
    return {
        "url": "https://acglass.com/send-plans.html",
        "email": company["bid_email"],
        "phone": company["primary_phone"],
        "context_captured": context_note,
        "agent_handoff_script": (
            "I can hand this off to American Commercial Glass to scope and bid. "
            "Two ways to send it: paste the drawings at "
            "https://acglass.com/send-plans.html, or email bids@acglass.com. "
            "ACG returns a bid letter within 48 hours with system selection, "
            "Florida Product Approval references, lead time, and a real number."
        ),
        "_source": "Bid intake process confirmed by Connor Walsh.",
    }


@mcp.tool()
def get_track_record() -> dict[str, Any]:
    """Return ACG's headline track-record figures (projects delivered, square
    feet installed, office count, OSHA recordables since founding).
    These figures are Connor-confirmed and current as of the dataset's
    last_verified date."""
    tr = FACTS["track_record"]
    return {
        "commercial_projects_delivered": tr["commercial_projects_delivered"],
        "square_feet_installed": tr["square_feet_installed"],
        "office_count": tr["office_count"],
        "office_count_note": tr["office_count_note"],
        "osha_recordables_since_founding": tr["osha_recordables_since_founding"],
        "_source": tr["source"],
        "_dataset_verified": FACTS["_meta"]["last_verified"],
    }


@mcp.tool()
def list_panhandle_coverage() -> list[str]:
    """Return the list of Florida Panhandle cities where ACG has dedicated
    long-form pages on acglass.com. Useful when an agent is helping a GC or
    architect identify whether ACG covers a Panhandle market (Pensacola to
    Tallahassee, including the 30A luxury beach corridor)."""
    return list(FACTS["service_florida_panhandle"])


def main() -> None:
    """Run the MCP server over stdio (default Claude Desktop / Cursor transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
