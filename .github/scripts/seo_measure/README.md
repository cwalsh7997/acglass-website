# ACG SEO measurement layer

Turns Search Console exports into a weekly report scored against a maintained
target set: which priority queries moved on and off page 1, which queries have
more than one ACG URL competing for them, how the money pages performed, and
which non-API surfaces (map pack, AI assistants, Bing) nobody has filled in yet.

Stdlib-only Python 3.11+. No secrets are stored in the repo, and no SERP is ever
fetched - every number originates from a first-party export the site owner
already has access to.

## Why it lives in `.github/`

The repo root is the deploy root: anything tracked outside `.github/` is served
publicly at `acglass.com/...`. GitHub Pages does not serve `.github/`, and
Actions cannot read `_internal/` because it is git-ignored. So `.github/` is the
only place CI-readable tooling can live. This is the deliberate exception
documented in the root `CLAUDE.md` - do not "clean it up" into the root.

## Layout

```
.github/seo/
  seo-targets.json      target queries, markets, pages, thresholds  <- edit this
  manual-metrics.json   values for surfaces with no API             <- edit weekly
  data/                 your GSC exports (git-ignored)
  reports/              generated output (git-ignored)
  samples/              a committed example report

.github/scripts/
  seo-report.py         CLI: exports -> Markdown + CSV report
  seo-gsc-export.py     CLI: GSC API -> JSON snapshots (optional)
  seo_measure/
    config.py           loads and validates seo-targets.json
    ingest.py           CSV + API JSON -> one row model
    analyze.py          period comparison, cannibalization, band movement
    report.py           Markdown + CSV rendering
  tests/                unittest suite + synthetic fixtures
```

## Weekly runbook

### 1. Get the data

Either path works. The CSV path needs no credentials at all.

**Option A - CSV from the Search Console UI (no setup).**

1. Search Console → Performance → Search results.
2. Set the date range to the last complete week. Search Console finalizes data
   on a 2-3 day lag, so end the window at least 3 days before today.
3. Add the **Pages** dimension alongside **Queries** if you want cannibalization
   detection - a queries-only export physically cannot show which URL served
   which query, and the report will say so rather than guess.
4. Export → CSV. Save into `.github/seo/data/` as
   `YYYY-MM-DD_YYYY-MM-DD.csv`.
5. Repeat for the prior week.

Header names are matched loosely, so the UI export (`Top queries`, `Clicks`,
`Impressions`, `CTR`, `Position`), the bulk export, and Looker Studio exports
all work. CTR is accepted as either `3.4%` or `0.034`.

**Option B - API snapshots (needs the existing `GSC_SA_JSON` secret).**

```bash
pip install google-api-python-client google-auth
export GSC_SA_JSON="$(cat /path/to/service-account.json)"   # never commit this
python3 .github/scripts/seo-gsc-export.py --weekly --out-dir .github/seo/data
```

Writes `current.json` and `prior.json` for the last two complete weeks. The
service account needs read access to the property in Search Console; it is the
same secret `seo-pulse.py` already uses. Credentials are read from the
environment only - `GSC_SA_JSON` inline, or `GOOGLE_APPLICATION_CREDENTIALS`
pointing at a file.

### 2. Fill in what the APIs cannot give you

Open `.github/seo/manual-metrics.json`, set `as_of` to the last day of the
reporting window, and fill in the values you have. Leave the rest `null`.

A `null` renders as *not supplied* and is listed under **Data gaps** - it is
never estimated, interpolated, or carried over from a previous week. That
distinction matters: `0` means "we measured zero", `null` means "nobody pulled
the number". If `as_of` predates the end of the reporting period, the report
prints a staleness warning.

Each metric declares how it is sourced:

| `input_method` | Meaning |
| --- | --- |
| `manual-export` | A human downloads it from the vendor UI and types it in. |
| `connector` | A script owns it; `connector_id` names which one. |
| `unavailable-no-api` | UI-only, no API published. Manual entry is the only option - do not build a scraper for it. |

Current sources:

- **Local / map pack** - GBP → Performance → per location → Download. The GBP
  Performance API can automate this later; until then it is a manual export.
- **Map-pack rank / Share of Local Voice** - from a licensed geo-grid vendor's
  export, quarterly. Never by querying Google directly.
- **AI assistant visibility** - run the existing monthly *AI Visibility*
  workflow (`.github/scripts/ai-visibility.py`) and copy the per-engine cite
  rate from its Slack summary. No engine offers first-party citation reporting,
  so that prompt panel is the measurement.
- **Bing** - Search Performance is API-accessible via the `BING_API_KEY` that
  `seo-pulse.py` already uses. The **AI Performance** report is preview-only
  with no API; export it by hand monthly.
- **Google AI surfaces** - the GSC generative-AI report is impressions-only,
  capped at 1,000 rows, and not exposed by the Search Analytics API.

### 3. Generate the report

```bash
python3 .github/scripts/seo-report.py \
  --current .github/seo/data/2026-07-20_2026-07-26.csv \
  --prior   .github/seo/data/2026-07-13_2026-07-19.csv \
  --current-range 2026-07-20:2026-07-26 \
  --prior-range   2026-07-13:2026-07-19
```

With snapshots the dates are already inside the files:

```bash
python3 .github/scripts/seo-report.py \
  --current .github/seo/data/current.json \
  --prior   .github/seo/data/prior.json
```

Output lands in `.github/seo/reports/`:

| File | Contents |
| --- | --- |
| `seo-report-<end-date>.md` | The readable weekly report. |
| `queries.csv` | One row per target query, both periods, with deltas and bands. |
| `pages.csv` | One row per priority page. |
| `cannibalization.csv` | One row per competing URL per flagged query. |
| `movement.csv` | One row per query per movement bucket. |
| `manual-metrics.csv` | Flattened manual values, including the unsupplied ones. |

Useful flags: `--stdout` to print the Markdown, `--no-csv` for Markdown only,
`--out-dir` to redirect output, and `--fail-on-regression` to exit 2 when a
target query drops off page 1 or a HIGH cannibalization finding appears (for
use as a CI gate - off by default).

### 4. Act on it

Read the report in this order:

1. **Dropped off page 1** - regressions on money queries, most urgent.
2. **Cannibalization, HIGH first** - two ACG URLs splitting one query's
   impressions. Pick one canonical page per intent-city pair and 301 the rest.
   The duplicate West Palm Beach and three-way Nashville splits are the known
   standing cases.
3. **Striking distance** - page 2-3 with real impression volume. Cheapest
   page-1 wins available.
4. **Data gaps** - anything unmeasured is unmanaged.

## Editing the target set

`.github/seo/seo-targets.json` is the single source of truth. It holds targets
and thresholds only - never metric values.

- **`query_groups[]`** - a query is either a bare string or
  `{"query": "...", "market": "<market id>"}`. Duplicates across groups are
  rejected at load time, since one query rolling up into two groups would
  double-count it.
- **`markets[]`** - every `market` referenced by a query or page must exist here
  or the config fails to load.
- **`pages[]`** - priority pages, matched to GSC URLs after normalizing away the
  origin, query string, fragment, and `/index.html`. A test asserts every listed
  page actually exists in the repo, so a renamed page fails CI instead of
  silently reporting zeros forever.
- **`thresholds`** - position bands and the noise floors described below.

### How the numbers are defined

**Position bands.** Page 1 is position ≤ 10, page 2 is ≤ 20, page 3 is ≤ 30,
everything beyond is "Page 4+". A query with no impressions is "No impressions",
which is distinct from ranking badly.

**Average position** is impression-weighted, matching how Search Console
computes it. A plain mean would let a long-tail row with 1 impression drag the
figure as hard as a head term with 1,000.

**Query figures from a query+page export are re-aggregated, so they will not
tie out exactly against the GSC UI's query view.** A query+page export splits
one query across its URLs; rolling those rows back up recovers the impression
count but only approximates the position, because Google computes the
query-level average over impressions this report cannot see individually. The
difference is small - around 0.05 positions in the sample data - and it is
consistent week over week, so deltas remain sound even though the absolute
number is a hair off the UI. Export query-only if you need figures that match
the UI exactly, and accept that cannibalization detection is then unavailable.

**Position gain** is signed so `+` always means movement toward position 1, even
though the underlying number goes down.

**Movement floor.** A query must clear `movement.min_impressions` (default 10)
in at least one period before any position delta is reported. An average
position computed off 2 impressions swings wildly; without the floor those rows
dominate the movement lists. Suppressed queries are counted in the report so the
holdout is visible.

Because of that floor, **the band distribution and the transition counts do not
reconcile.** The distribution counts every target query, while the transition
counts only cover queries above the floor. A query can therefore move from Page
2 to Page 1 in the distribution without appearing in "Entered page 1". This is
deliberate: the distribution answers "where does the target set stand", the
transitions answer "what moved enough to be worth acting on".

**Cannibalization.** Flagged when 2+ ACG URLs each hold at least
`min_impressions_per_url` (5) impressions *and* at least
`min_impression_share_per_url` (10%) of that query's impressions. Share is
measured against the query's *whole* impression count, including the URLs that
fall below those floors - so the shares of the flagged URLs sum to less than
100% whenever a long tail exists, and the reported impression total is the
query's real total rather than the qualifying subset's.

Severity weights rank, not just share, because consolidating two URLs sitting at
positions 45 and 55 wins nothing while a 60/40 split across page 2 is a page-1
placement being given away:

| Severity | Condition |
| --- | --- |
| HIGH | 2+ competing URLs on page 1, or the runner-up holds ≥30% share *and* ranks within page 2. |
| MEDIUM | At least one URL within the top 30, and either 3+ competing URLs or a ≥30% runner-up. |
| LOW | Everything else - including even splits that are all beyond page 3. |

This matters beyond triage order: `--fail-on-regression` gates CI on HIGH, so
grading on share alone would fail the build on page-4 noise while passing real
page-2 cannibalization.

Detection needs a query+page dimensioned export and returns nothing -
explicitly, in the report - without one.

## Tests

```bash
python3 -m unittest discover -s .github/scripts/tests -t .github/scripts/tests -v
```

No network, no credentials, runs in well under a second. The suite covers
CSV/JSON ingest quirks (percent vs ratio CTR, thousands separators, header
aliases, BOM, blank cells, mistyped paths), band boundaries, movement classification,
cannibalization severity and every threshold that suppresses a finding, manual
metric gap handling, report determinism, and the CLI end-to-end.

Two act as guardrails rather than unit tests: one asserts no credential material
appears anywhere in the layer, and one asserts every page in `seo-targets.json`
still exists in the repo.

The fixtures in `tests/fixtures/` are **synthetic**. They are shaped to exercise
the analyzers - a two-URL page-1 split, a three-way Nashville split, one query
entering page 1 and one leaving - and are not ACG performance data.

## Constraints

Deliberate, and worth preserving:

- **No secrets in the repo.** Credentials come from the environment only, reusing
  the `GSC_SA_JSON` and `BING_API_KEY` secrets the existing workflows already
  define. A test enforces this.
- **No SERP scraping.** Rank data comes from Search Console. Map-pack position
  comes from a licensed geo-grid vendor's export. Nothing here queries Google
  directly.
- **No invented numbers.** Unmeasured is reported as unmeasured. A surface with
  no API stays a manual input rather than becoming a scraper or an estimate.
- **No new API integrations** beyond the Search Console read scope that
  `seo-pulse.py` already uses.

## Relationship to the existing scripts

Complementary, not a replacement:

| Script | Cadence | Role |
| --- | --- | --- |
| `seo-pulse.py` | nightly | Site-wide totals and bucket clicks → Google Sheet + Slack. |
| `ai-visibility.py` | monthly | Runs a fixed prompt panel through 3 AI engines. Feeds the AI section here. |
| `seo-verify.py` | on push | Asserts on-page facts (titles, canonicals) on the live site. |
| `seo-report.py` | weekly | Scores the target set, and is the only one that does per-query movement and cannibalization. |
