# acglass.com

Static site, GitHub Pages + Cloudflare. Repo root = deploy root - everything tracked here is publicly served.

Rules for all agents:
- Full build/claims/style rules live in `_internal/CLAUDE.md` (git-ignored, local only). Read it before content work.
- Never add quantitative claims, certifications, or manufacturer relationships that are not verified in `_internal/CLAUDE.md`.
- Never commit internal docs, scripts, or QA artifacts outside `_internal/`.
- One exception, deliberate: CI scripts live in `.github/scripts/`. GitHub Pages
  does not serve `.github/` (verified - `acglass.com/.github/workflows/pulse.yml`
  returns 404 while `/.gitignore` returns 200), and Actions cannot read
  `_internal/` because it is git-ignored. Do not "clean these up" - deleting
  `scripts/` in bd0515fa is what broke SEO Verify for 22 days.
