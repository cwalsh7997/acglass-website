# STATUS

## Open PR queue
_None yet. No phase branch cut: see Blockers._

## Baseline
`.agent/evidence/p0-remediation/verify-baseline.txt`, captured before any content edit.
`ACG_FEDERAL_WARN_ONLY=1 bash scripts/verify.sh` → exit 1, 32s.

| check | result |
|---|---|
| license-attribution | CONFIG (number unconfirmed) |
| safety-claims | **FAIL** |
| placeholders | **FAIL** |
| volume-claims | PASS |
| bonding | **FAIL** |
| geography | CONFIG (county list empty) |
| federal-status | CONFIG (warn-only until phase 6) |
| deny-list | CONFIG (not generated) |
| image-rights | CONFIG (csv empty) |

PASS 1 · FAIL 3 · CONFIG 5. Config is not a pass.

## Done this session
- Kit installed to `_internal/kit-staging/` (git-ignored). `/CLAUDE.md` added to
  `.gitignore` so the root copy can never be committed.
- Built `scripts/verify.sh` + 9 checks + `.agent/config/`. Rewrote them with `git grep`
  after the first version took over 2 minutes; now 32s.
- Shipped `44d9a7e0a` and `48dfa14c9`: nine internal docs off the public deploy.

## Blockers
- **Classifier is blocking repo file moves** (`cp -R`, `mv`) inside the working tree.
  The root `CLAUDE.md` could not be placed. The `.gitignore` rule is in place ahead of it.
  Commands for Connor are in the session report.
