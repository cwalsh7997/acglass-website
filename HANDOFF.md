# Site Audit Handoff — `audit/dedupe-og-tags`

This branch carries **18 commits** of audit fixes for acglass.com. Nothing
has been pushed to GitHub or merged to `main` yet — production is unchanged.
This doc covers what's done, how to ship it, and what still needs your
input.

## Headline numbers

| Metric | Before | After |
|---|---|---|
| Duplicate `og:*` meta tags | 83 pages broken | 0 |
| Third-party font CDN requests per page | 3 (Google Fonts) | 0 (self-hosted woff2) |
| Broken internal links (HTML refs) | 437 | 0 |
| `<img>` tags with `width`/`height` (CLS) | ~2172 attrs (incomplete) | 1583/1592 imgs (99% coverage) |
| `<img>` tags with `decoding="async"` | 807 (50%) | 1591/1592 (99%) |
| `<img>` tags with `loading=*` | 1165 (73%) | 1590/1592 (99%) |
| Inline `onmouseover` event handlers | 6,763 | 777 (88% reduction) |
| Lead-capture forms that actually deliver | 0 (broken stub Formspree) | 2 (mailto fallback) |
| `<meta name="theme-color">` coverage | 0 pages | 444 pages |
| Service schema on system/product pages | 0 of 6 | 6 of 6 |
| `Florida\'s` literal-backslash in og:image:alt | 303 | 0 |
| Sitemap entries pointing at noindex'd pages | 9 | 0 |
| Pages without Privacy/Terms link in footer | 444 (orphan pages) | 4 (only minimal pages without footer) |
| Estimated HTML payload reduction | n/a | ~1.5–2 MB across the site |

## Commit log (oldest to newest on this branch)

```
4ab2221 fix: dedupe duplicate og:* meta tags on 83 pages
2b69212 perf: self-host Inter, JetBrains Mono, and Playfair Display
d3dd2fe fix: add canonical to press-release-tampa.html
2793ec6 fix(forms): mailto fallback so contact + send-plans actually deliver leads
a7a04e1 fix(links): repair 400 broken internal links + prune noindex'd pages from sitemap
6d92461 fix(links): repoint final 35 broken anchors to relevant index pages
7d18e38 fix: dedupe 404 robots meta + add partners.html to sitemap
ad7f276 perf(cls): add width+height to 1024+ <img> tags + repair broken image refs
cdc950c feat(seo): add Service schema to 6 product/system pages
bc44120 fix: remove stray backslash from "Florida's" in og:image:alt across 301 pages
82769a2 perf: add decoding="async" to 784 <img> tags that lacked it
888e636 perf: add loading="lazy" to 425 below-the-fold <img> tags
f432e93 docs: add HANDOFF.md summarizing the audit branch
4a3c4de fix: surface Privacy + Terms links from footer on 135 pages
b15a3cc fix: extend Privacy + Terms links to multi-line footer-bottom (304 more pages)
1b4365a fix: humans.txt founding year (2020 -> 2021)
9184c72 docs: note known minor issues in HANDOFF
ebfd8d8 perf: extract repeated city-pill inline styles + handlers to a CSS class
```

Each commit message has the full rationale + before/after numbers — read
those for context, not this doc.

## To ship: pick one

The branch needs to land somewhere. Three options:

### Option 1 — You merge to `main` and Pages auto-deploys

```sh
cd "C:/Users/cwals/Claude Code/acglass-website"
git checkout main
git merge audit/dedupe-og-tags
git push origin main
```

GitHub Pages picks it up in ~1 minute. **Reversible** with `git revert HEAD`
+ push if anything looks off. This is the fastest path but irreversible-ish.

### Option 2 — You push the branch first, then PR-review on GitHub

```sh
cd "C:/Users/cwals/Claude Code/acglass-website"
git push -u origin audit/dedupe-og-tags
# Open https://github.com/cwalsh7997/acglass-website/compare/main...audit/dedupe-og-tags
# Review the diff, merge via GitHub UI when ready
```

This needs a Personal Access Token or Git Credential Manager session. If
push hangs the way it did during this audit, run:

```sh
git config --global credential.helper manager
# Then push again — GCM will pop a browser auth window once
git push -u origin audit/dedupe-og-tags
```

### Option 3 — You discard everything

```sh
cd "C:/Users/cwals/Claude Code/acglass-website"
git checkout main
git branch -D audit/dedupe-og-tags
```

(I don't recommend this — you'd lose 12 commits of real fixes — but it's
your call.)

## Verify after deploy

Once main is live, run **Lighthouse mobile** on at least these three URLs:

- `https://acglass.com/` (homepage / LCP test)
- `https://acglass.com/commercial-glazing-miami.html` (city page / FAQ schema test)
- `https://acglass.com/blog/wild-blue-clubhouse-glazing.html` (Playfair font test)

Expectations:
- **Performance** should improve due to self-hosted fonts + img dimensions
  + decoding=async + lazy loading. Watch CLS specifically — should be ≤ 0.1.
- **SEO** should hit 100 — meta description, canonical, schema, viewport
  are all set on every page.
- **Accessibility** should improve from baseline because skip-link, alt
  text, theme-color, and ARIA-expanded on dropdowns are all present.

Also run **schema validator** on a city page: <https://validator.schema.org/>

Also run **mobile-friendly test**: <https://search.google.com/test/mobile-friendly>

## Things that still need YOU

These were either out of my scope (judgment / brand calls) or require
external accounts I don't have access to.

### 1. Real form backend (HIGHEST IMPACT)

Both `send-plans.html` and `contact.html` now have a `mailto:` fallback so
leads at least reach `connor@acglass.com` today. But mailto requires the
visitor to have an email client configured — desktop visitors without one
will see a "no app to handle this URL" prompt.

To fix properly, sign up at <https://formspree.io> (free for low volume),
create a form, get the form ID like `xnqyzlpv`, then either:

- I can swap it in for you when you give me the ID — just say "the
  Formspree ID is `xnqyzlpv`" and I'll wire both forms.
- Or do it yourself: in `send-plans.html` find `formspree-pending` and
  replace with the ID. For `contact.html` change the JS handler from
  mailto to a fetch() POST against `https://formspree.io/f/xnqyzlpv`.

Alternatives if you don't want Formspree:
- **Web3Forms** — no signup, free, just an API key from the website.
- **Netlify Forms** — but you'd have to move hosting from GitHub Pages.
- **Cloudflare Worker** writing to Google Sheets — most work, most flexible.

### 2. AI-managed branding (STRATEGIC)

The hero on every root page leads with **"Precision Glazing. AI-Managed.
Delivered."** This is woven into the schema, llms.txt, and the slogan.
I deliberately didn't touch it.

My honest opinion: GCs and architects buy on (1) submittal reliability, (2)
crews actually showing up, (3) FL CGC license, (4) project track record,
(5) bonding capacity. "AI-managed" is a differentiator but probably not
the primary lead trigger. Worth A/B testing a hero variant that leads
with **"350+ projects. 48-hour scope. Florida CGC #1531993"** and treats
AI-managed as a secondary frame. But that's a brand call, not mine.

### 3. The 23 "Adjacent Market" city pages

City pages like `commercial-glazing-parkland-fl.html` link to "nearby
city" cards (Coconut Creek, Cooper City, etc.) that don't exist as pages.
I redirected them to `/locations.html` so they don't 404 — but that's a
band-aid. To turn them into real ranking-page-each-city wins you'd
either build them out (with unique HVHZ / NOA / market color per city,
following the existing Miami/Tampa/Naples pattern) or remove the
"Adjacent Markets" section from city pages.

### 4. The 10 unwritten author blog posts

`author-connor-walsh.html` and `author-rielly-walsh.html` link to 10 blog
posts that don't exist (e.g., `division-08-scope-coordination-tips`,
`miami-dade-noa-compliance-checklist`). Currently redirected to
`blog.html`. To complete the E-E-A-T signal these author pages are trying
to build, those posts should actually exist. List of slugs in the commit
message of `6d92461`.

### 5. Heading hierarchy (~840 skips, mostly in footer)

Site has 839 places where heading levels skip non-sequentially (mostly
H2 → H4 / H5 in the footer because the footer uses `<h5>` for "Company /
Services / Trust / Contact" headings, but the previous heading on most
pages is an H2). Not a bug exactly — it's a stylistic choice that hurts
screen reader users who navigate by heading. Fix would require either:
- Restructuring the footer to use h3 with appropriate CSS
- Adding section landmarks with aria-labelledby instead of headings
- Or accepting the current pattern (the styling is keyed to `.footer h5`)

I didn't mass-fix because it's a CSS-coupled change.

### 6. Broken `<img>` references with no replacements (NONE — fixed)

Was 13 references to images that don't exist on disk. All redirected to
existing project hero images (mostly `wild-blue-clubhouse-hero.jpg`). If
you ever shoot photos for those projects (Boca Raton commercial, Daytona,
Hulett Port St Lucie, etc.), update the city pages' service-detail-visual
section to use the real photo.

## Known minor issues (browsers handle gracefully)

- **4 pages with unbalanced `<div>` tags** — fixable but risky to mass-edit
  without visual verification:
  - `commercial-glazing-naples.html` — 1 missing `</div>`
  - `eswindows-installer-miami.html` — 1 extra `</div>`
  - `portfolio.html` — 1 missing `</div>` (the `<div class="pf-grid-wrap">`
    on line 712 doesn't have a clearly matching close)
  - `location-template-snippet.html` — 2 missing `</div>` (it's a partial
    snippet so this is expected)
  Browsers auto-close at end of section / document so these don't visibly
  break, but they show up as warnings in HTML validators.

- **839 heading-level skips** (mostly H2 → H4 / H5 in footer) — flagged
  in #5 below.

- **Some JPGs declare og:image as 1200×630 but the actual file is bigger**
  (e.g., 1600×900). Facebook crops automatically; not a render bug. To fix
  perfectly you'd produce 1200×630 versions of the 30 or so most-used og
  images — image-processing work I couldn't do without ImageMagick.

## What I deliberately didn't touch

- Image compression / WebP encoding for PNGs (need ImageMagick).
- og:image dimensions (declared 1200×630 but actual files are usually
  1600×900 — Facebook crops automatically; not a bug per se).
- 133 `<picture>` blocks without a WebP `<source>` (mostly logo PNGs and
  one-off images where WebP doesn't help much).
- The "AI-Managed" brand voice (your call, see #2 above).

## Memory + tooling I left on disk

I created small awk helpers under `C:/Users/cwals/`:
- `fix-apos.awk` — replaces literal `\'` with `'` in HTML attributes
- `add-decoding.awk` — adds `decoding="async"` to `<img>` tags
- `add-lazy.awk` — adds `loading="lazy"` to non-LCP `<img>` tags

If you don't need them, just delete those files.

I also updated the project memory at
`C:/Users/cwals/.claude/projects/C--Users-cwals-Claude-Code/memory/`
so a future Claude session will know the state of this audit without
re-running discovery.
