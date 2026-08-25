# Sample output

**Everything in this directory is synthetic.** The numbers come from the test
fixtures in `.github/scripts/tests/fixtures/` and are invented to exercise the
analyzers. They are not ACG performance data and must not be quoted, reported,
or compared against real figures.

They are committed so the report's shape can be reviewed without needing
Search Console access.

| File | Shows |
| --- | --- |
| `seo-report-2026-07-26.md` | The full weekly report, all seven sections. |
| `queries.csv` | One row per target query with both periods and deltas. |
| `pages.csv` | One row per priority page. |
| `cannibalization.csv` | One row per competing URL per flagged query. |
| `movement.csv` | One row per query per movement bucket. |
| `manual-metrics.csv` | Flattened manual values, including the unsupplied ones. |

Regenerate with:

```bash
python3 .github/scripts/seo-report.py \
  --current .github/scripts/tests/fixtures/gsc-combined-current.csv \
  --prior   .github/scripts/tests/fixtures/gsc-combined-prior.csv \
  --current-range 2026-07-20:2026-07-26 \
  --prior-range   2026-07-13:2026-07-19 \
  --manual  .github/scripts/tests/fixtures/manual-metrics-partial.json \
  --out-dir .github/seo/samples
```

The synthetic-data banner at the top of the Markdown file is added by hand after
generating; re-add it if you regenerate.

The fixtures deliberately contain the cannibalization patterns the strategy
research identified as real standing issues - the duplicate West Palm Beach
pages and the three-way Nashville split - so the detector's output can be
sanity-checked against a known-shape input.
