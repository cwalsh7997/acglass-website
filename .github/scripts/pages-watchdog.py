#!/usr/bin/env python3
"""GitHub Pages deploy watchdog.

Why this exists
---------------
acglass.com is served by GitHub Pages (legacy build type, source branch `main`,
path `/`) behind Cloudflare. Vercel is not the live host; vercel.json is dead
config, so a green Vercel check says nothing about what visitors see.

On 2026-08-26 the Pages build for commit 002721322 entered status "building" at
15:08:11Z and never left it. Normal builds finish in 43-120 seconds. That one
sat for about 14 hours with no alert of any kind. A merged SEO fix looked
shipped and was not live. It was found by hand, and a manual rebuild then
published in 42 seconds.

Nothing in the repo watched the deploy surface itself, so this script does. It
runs on a schedule and fails loudly on the four states that mean "main is not
what the edge is serving".

Failure conditions (exit 1)
---------------------------
1. latest Pages build status is `errored`.
2. latest Pages build status is `building` and its created_at is older than
   HUNG_BUILD_MINUTES (15). This is the exact hang signature from 2026-08-26.
3. latest Pages build status is `built` but its commit sha is not the current
   `main` HEAD sha. main advanced and Pages never rebuilt.
4. the API or the live origin could not be read at all (unknown state is not a
   healthy state).
5. any `Sitemap:` URL declared in live robots.txt returns a non-200 status or
   does not parse as XML. This catches the 2026-09-03 report where
   https://acglass.com/sitemap.xml briefly returned HTTP 500 during a Pages
   deploy window while sitemap-blog.xml still looked fine.

Warning condition (exit 0, loud text)
-------------------------------------
The live `last-modified` header on https://acglass.com/ is more than
STALE_EDGE_MINUTES (30) older than the newest successful build. That is a
cache/propagation smell rather than a build failure, so it warns instead of
failing.

Stdlib only, by design: no pip step, no third-party imports, and no network
beyond api.github.com and acglass.com.

Run locally:  python3 .github/scripts/pages-watchdog.py
Tests:        cd .github/scripts && python3 -m unittest tests.test_pages_watchdog
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

REPO = os.environ.get("GITHUB_REPOSITORY", "cwalsh7997/acglass-website")
# GITHUB_API_URL is set for us inside Actions and is api.github.com there. It
# is honoured here so the script can also be run by hand through an API host
# that is not api.github.com without editing code.
API_ROOT = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
LIVE_URL = "https://acglass.com/"
ROBOTS_URL = LIVE_URL + "robots.txt"
MASTER_SITEMAP_URL = LIVE_URL + "sitemap.xml"
USER_AGENT = "acglass-pages-watchdog"

# A build that has not finished in this long is hung, not slow. Normal builds
# take 43-120 seconds, so 15 minutes is roughly 7x the worst normal case: late
# enough to never fire on a merely slow build, early enough that a hang is
# caught within one or two watchdog runs instead of 14 hours later.
HUNG_BUILD_MINUTES = 15

# How far behind the newest successful build the edge may lag before we say so.
STALE_EDGE_MINUTES = 30

TIMEOUT_SECONDS = 30


class Decision(object):
    """Outcome of one watchdog evaluation."""

    def __init__(self):
        self.failures = []
        self.warnings = []
        self.summary = []

    @property
    def ok(self):
        return not self.failures

    @property
    def exit_code(self):
        return 0 if self.ok else 1

    def render(self):
        lines = ["GitHub Pages deploy watchdog", "=" * 30]
        lines.extend(self.summary)
        lines.append("")
        if self.failures:
            lines.append("FAIL (%d):" % len(self.failures))
            for item in self.failures:
                lines.append("  - " + item)
        if self.warnings:
            lines.append("WARN (%d):" % len(self.warnings))
            for item in self.warnings:
                lines.append("  - " + item)
        if not self.failures and not self.warnings:
            lines.append("OK: Pages is published and the edge is current.")
        elif not self.failures:
            lines.append("OK: no failure conditions met (warnings above).")
        return "\n".join(lines)


def parse_iso8601(value):
    """Parse a GitHub API timestamp such as 2026-08-27T05:12:50Z.

    Returns an aware UTC datetime, or None when the value is missing or is not
    a shape we recognise. Callers treat None as "unknown", never as "fine".
    """
    if not value:
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_http_date(value):
    """Parse an RFC 1123 HTTP date such as Thu, 27 Aug 2026 05:13:31 GMT."""
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S"):
        try:
            parsed = datetime.strptime(text, fmt)
        except ValueError:
            continue
        return parsed.replace(tzinfo=timezone.utc)
    return None


def _short(sha):
    if not sha:
        return "unknown"
    return str(sha)[:9]


def _minutes(delta):
    return delta.total_seconds() / 60.0


def _fmt_ts(moment):
    if moment is None:
        return "unknown"
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def decide(latest_build, head_sha, live_last_modified,
           latest_success=None, now=None,
           hung_minutes=HUNG_BUILD_MINUTES,
           stale_edge_minutes=STALE_EDGE_MINUTES,
           errors=None):
    """Pure decision function. No network, no clock unless `now` is omitted.

    latest_build        dict from /repos/{owner}/{repo}/pages/builds/latest,
                        or None when the call failed.
    head_sha            current `main` HEAD sha, or None when unknown.
    live_last_modified  the `last-modified` header value from LIVE_URL as a
                        string, a datetime, or None.
    latest_success      newest build dict whose status is `built`. Defaults to
                        latest_build when that build is itself `built`.
    errors              list of fetch error strings to fold into failures.
    """
    result = Decision()
    now = now or datetime.now(timezone.utc)

    if isinstance(live_last_modified, datetime):
        live_dt = live_last_modified
        if live_dt.tzinfo is None:
            live_dt = live_dt.replace(tzinfo=timezone.utc)
        live_dt = live_dt.astimezone(timezone.utc)
    else:
        live_dt = parse_http_date(live_last_modified)

    status = (latest_build or {}).get("status")
    build_sha = (latest_build or {}).get("commit")
    created = parse_iso8601((latest_build or {}).get("created_at"))
    updated = parse_iso8601((latest_build or {}).get("updated_at"))
    duration_ms = (latest_build or {}).get("duration")
    build_error = ((latest_build or {}).get("error") or {}).get("message")

    if latest_success is None and status == "built":
        latest_success = latest_build
    success_at = parse_iso8601((latest_success or {}).get("updated_at")
                               or (latest_success or {}).get("created_at"))

    # Diagnostics print in every case, pass or fail. The 2026-08-26 hang was
    # only diagnosable because someone read these fields by hand.
    result.summary.append("checked at:         %s" % _fmt_ts(now))
    result.summary.append("repository:         %s" % REPO)
    result.summary.append("latest build status: %s" % (status or "unknown"))
    result.summary.append("latest build sha:    %s" % _short(build_sha))
    result.summary.append("latest build created: %s" % _fmt_ts(created))
    result.summary.append("latest build updated: %s" % _fmt_ts(updated))
    if isinstance(duration_ms, (int, float)):
        result.summary.append("latest build duration: %.1fs" % (duration_ms / 1000.0))
    else:
        result.summary.append("latest build duration: unknown")
    if created is not None:
        result.summary.append("build age:           %.1f min" % _minutes(now - created))
    result.summary.append("main HEAD sha:       %s" % _short(head_sha))
    result.summary.append("newest successful build: %s" % _fmt_ts(success_at))
    result.summary.append("live last-modified:  %s" % _fmt_ts(live_dt))
    if build_error:
        result.summary.append("build error message: %s" % build_error)

    for message in (errors or []):
        result.failures.append(message)

    if latest_build is None:
        if not (errors or []):
            result.failures.append(
                "no Pages build payload available; deploy state is unknown")
        return result

    if status == "errored":
        result.failures.append(
            "Pages build %s for %s ERRORED (created %s): %s"
            % ((latest_build.get("url") or "unknown"), _short(build_sha),
               _fmt_ts(created), build_error or "no message from the API"))
    elif status == "building":
        if created is None:
            result.failures.append(
                "Pages build for %s is 'building' with no parsable created_at; "
                "treating unknown age as a hang" % _short(build_sha))
        else:
            age = _minutes(now - created)
            if age > hung_minutes:
                result.failures.append(
                    "Pages build for %s HUNG in 'building' for %.1f min "
                    "(threshold %d min, normal builds finish in 43-120s). "
                    "This is the 2026-08-26 signature: re-run the Pages build "
                    "from the Pages settings page or push an empty commit."
                    % (_short(build_sha), age, hung_minutes))
            else:
                result.summary.append(
                    "note: build in progress for %.1f min, under the %d min "
                    "hang threshold" % (age, hung_minutes))
    elif status == "built":
        if not head_sha:
            result.failures.append(
                "cannot compare published sha to main HEAD: HEAD sha unknown")
        elif str(build_sha) != str(head_sha):
            result.failures.append(
                "Pages published %s but main HEAD is %s. main advanced and "
                "Pages never rebuilt, so merged work is not live."
                % (_short(build_sha), _short(head_sha)))
    else:
        result.failures.append(
            "unrecognised Pages build status %r; treating as unhealthy"
            % (status,))

    # Edge freshness. Only meaningful once we know when a build last succeeded.
    if success_at is None:
        result.warnings.append(
            "no successful Pages build timestamp available, so edge freshness "
            "could not be checked")
    elif live_dt is None:
        result.warnings.append(
            "no parsable last-modified header from %s, so edge freshness "
            "could not be checked" % LIVE_URL)
    else:
        lag = _minutes(success_at - live_dt)
        result.summary.append("edge lag behind newest build: %.1f min" % lag)
        if lag > stale_edge_minutes:
            result.warnings.append(
                "live edge at %s is serving content last modified %s, %.1f min "
                "older than the newest successful build (%s). Threshold is "
                "%d min. Suspect a stale Cloudflare cache: purge it and "
                "re-check." % (LIVE_URL, _fmt_ts(live_dt), lag,
                               _fmt_ts(success_at), stale_edge_minutes))

    return result


def _request(url, headers=None, method="GET"):
    request = urllib.request.Request(url, method=method)
    request.add_header("User-Agent", USER_AGENT)
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    return urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)


def _api_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = (os.environ.get("GITHUB_TOKEN")
             or os.environ.get("GH_TOKEN")
             or os.environ.get("GH_ENTERPRISE_TOKEN"))
    if token:
        headers["Authorization"] = "Bearer " + token
    return headers


def fetch_api(path, errors, label):
    url = API_ROOT + path
    try:
        with _request(url, _api_headers()) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        errors.append("%s: HTTP %s from %s" % (label, exc.code, url))
    except Exception as exc:  # noqa: BLE001 - any failure is an unknown state
        errors.append("%s: %s from %s" % (label, exc, url))
    return None


def fetch_live_last_modified(errors):
    """HEAD the live origin and return its last-modified header value."""
    try:
        with _request(LIVE_URL, method="HEAD") as response:
            return response.headers.get("last-modified")
    except Exception as exc:  # noqa: BLE001
        errors.append("live fetch: %s from %s" % (exc, LIVE_URL))
    return None


def parse_robots_sitemaps(text):
    """Return Sitemap: URLs from a robots.txt body."""
    if not text:
        return []
    return re.findall(r"^\s*Sitemap:\s*(\S+)", text, re.IGNORECASE | re.MULTILINE)


def evaluate_sitemap_response(url, status, body):
    """Pure check for one live sitemap response. Returns a failure string or None."""
    if status != 200:
        return "sitemap %s HTTP %s (search engines use this as a primary entry point)" % (
            url, status)
    if not body or not body.strip():
        return "sitemap %s HTTP 200 but empty body" % (url,)
    try:
        ET.fromstring(body)
    except ET.ParseError as exc:
        return "sitemap %s HTTP 200 but XML parse failed: %s" % (url, exc)
    return None


def check_live_sitemaps(errors):
    """Fetch robots.txt and every declared sitemap. Returns (failures, url_count)."""
    failures = []
    try:
        with _request(ROBOTS_URL) as response:
            robots = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        errors.append("robots.txt: HTTP %s from %s" % (exc.code, ROBOTS_URL))
        return failures, 0
    except Exception as exc:  # noqa: BLE001
        errors.append("robots.txt: %s from %s" % (exc, ROBOTS_URL))
        return failures, 0

    sitemap_urls = parse_robots_sitemaps(robots)
    if not sitemap_urls:
        failures.append("robots.txt declares no Sitemap: URLs")
        return failures, 0

    if MASTER_SITEMAP_URL not in sitemap_urls:
        failures.append("robots.txt omits the master sitemap %s" % MASTER_SITEMAP_URL)

    for url in sitemap_urls:
        try:
            with _request(url) as response:
                body = response.read()
                failure = evaluate_sitemap_response(url, response.status, body)
        except urllib.error.HTTPError as exc:
            failure = evaluate_sitemap_response(url, exc.code, b"")
        except Exception as exc:  # noqa: BLE001
            failures.append("sitemap fetch: %s from %s" % (exc, url))
            continue
        if failure:
            failures.append(failure)

    return failures, len(sitemap_urls)


def newest_successful_build(builds):
    """Pick the newest build with status `built` from a builds list payload."""
    if not isinstance(builds, list):
        return None
    best = None
    best_at = None
    for build in builds:
        if not isinstance(build, dict) or build.get("status") != "built":
            continue
        moment = parse_iso8601(build.get("updated_at") or build.get("created_at"))
        if moment is None:
            continue
        if best_at is None or moment > best_at:
            best, best_at = build, moment
    return best


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    errors = []

    latest = fetch_api("/repos/%s/pages/builds/latest" % REPO, errors,
                       "pages/builds/latest")
    head = fetch_api("/repos/%s/commits/main" % REPO, errors, "commits/main")
    head_sha = (head or {}).get("sha")

    latest_success = None
    if not latest or latest.get("status") != "built":
        # Only spend the extra call when the latest build is not itself the
        # newest success, since edge freshness needs a success timestamp.
        builds = fetch_api("/repos/%s/pages/builds?per_page=20" % REPO, [],
                           "pages/builds")
        latest_success = newest_successful_build(builds)

    live_last_modified = fetch_live_last_modified(errors)
    sitemap_failures, sitemap_count = check_live_sitemaps(errors)

    result = decide(latest, head_sha, live_last_modified,
                    latest_success=latest_success, errors=errors)
    result.failures.extend(sitemap_failures)
    if sitemap_failures:
        result.summary.append("live sitemap checks: FAIL (%d)" % len(sitemap_failures))
    else:
        result.summary.append("live sitemap checks: OK (%d URLs from robots.txt)"
                              % sitemap_count)
    print(result.render())

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            with open(summary_path, "a", encoding="utf-8") as handle:
                handle.write("```\n" + result.render() + "\n```\n")
        except OSError:
            pass

    if "--never-fail" in argv:
        return 0
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
