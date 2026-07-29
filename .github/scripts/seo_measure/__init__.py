"""SEO measurement layer for acglass.com.

Stdlib-only. Reads target definitions from .github/seo/seo-targets.json, ingests
Google Search Console metrics from CSV exports or API-shaped JSON, compares two
periods, and renders a weekly Markdown + CSV report.

No secrets are stored here and no SERP is ever fetched: every number originates
from a first-party export the site owner already has access to.
"""

__all__ = ["config", "ingest", "analyze", "report"]
