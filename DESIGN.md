# Design

The system is fixed. `src/styles/tokens.css` is the single source of every value and
is the only file permitted to contain a raw one. `scripts/check-design-lint.sh` fails
the build on any violation and is wired into `scripts/verify.sh`.

Adjectives are not design direction. If a rule conflicts with a judgment about what
looks premium, the rule wins.

## Type

Eight tokens on a 1.25 ratio at a 16px base, clamped between the 390px and 1440px
sizes. **Six sizes maximum render on any one page.** Weights 400, 500, 600, 700 only.
No 300: Inter 300 at 17px is illegible on Windows. No 800 or 900.

`--measure: 68ch` on every prose block. The researched readability band is 45 to 75
characters; 68ch sits mid-band at `--fs-body`.

Uppercase is permitted **only** on mono labels at `0.06em` tracking. Sentence case
everywhere else. Never Title Case, never ALL CAPS on a heading or a sentence.

## Color

**Navy is the brand. Red is the pointer.** Red appears at most twice in any single
viewport, typically one primary button plus one accent rule.

Red is never body text, a prose link, an icon fill, a heading color, a card hover
fill, or a background taller than 200px. `--red-500` on `--navy-800` measures 3.01:1
and **fails AA**: on navy the only permitted red is `--red-300` at 5.30:1. Red *text*
on white is always `--red-600` at 6.11:1, never `--red-500` at 4.87:1.

Contrast minimums are 4.5:1 for text and 3:1 for all non-text UI including borders,
icons and focus rings. The ratios in `tokens.css` are measured, not estimated. Any
new pair gets measured and recorded before it ships.

No color exists outside that list. No greens or ambers except the two form-state
tokens, and those are text only.

## Space and layout

The 8pt scale is a closed set. `padding: 18px` does not exist. Nothing exceeds 128px
of vertical padding anywhere.

**Asymmetry is required.** A page where every section is a centered 1200px stack is a
failed page. Section headers occupy columns 1 to 5 and body columns 6 to 12, or the
reverse, on at least three sections per page.

## Surface

**Borders, not shadows.** The default card is `1px solid var(--line-200)` with no
shadow. The two elevation tokens exist only for genuinely floating layers.

Radius maxes at 4px. `border-radius: 999px` is banned. Glazing is a square-edged,
mullion-and-frame product; 12px-plus radii read consumer SaaS.

## Motion

See `MOTION.md`. Four behaviors site-wide, nothing longer than 260ms, `transform` and
`opacity` only.

## Fonts

Two families, self-hosted, latin subset, `font-display: swap`.

| File | Size |
|---|---:|
| `inter-variable-latin.woff2` | 47 KB |
| `jetbrains-mono-variable-latin.woff2` | 39 KB |
| **Total** | **87 KB** against a 120 KB cap |

Archivo (176 KB) and Playfair Display (75 KB across two files) were removed in phase 2.
The payload went from 348 KB to 87 KB, a 75% reduction. Archivo's stacks already listed
Inter as the next fallback, so removing it degraded cleanly. Playfair backed a `--serif`
token that the two-family spec does not permit; that token now points at the sans stack.

## Dark surface mode, 2026-09-09

The library was built light: `.u-section` defaulted to `--paper` with `--ink-900`
text. It was applied to three pages, and then the rest of the site was measured.

    alachua-county/    rgb(5, 10, 18)
    aventura/          rgb(5, 10, 18)
    all-glass-entrances/ rgb(5, 10, 18)
    index.html         rgb(5, 7, 12)
    about.html         rgb(10, 14, 22)
    portfolio.html     rgb(5, 7, 12)
    blog/              rgb(5, 10, 18)

Every page type is dark. The three converted pages were the only light ones on a
1,527-page site, which means the design system was making acglass.com **less**
uniform, not more. That is the opposite of the point.

Dark is the brand. The components moved to it.

### Surfaces are named, not hard-coded

`tokens.css` section 3b defines `--surface`, `--surface-raised`, `--surface-alt`,
`--on-surface`, `--on-surface-muted` and `--surface-rule`. Components reference
those rather than `--paper` and `--ink-900` directly, so the theme is one block
rather than a sweep. Measured against `--surface`:

    --on-surface        16.7:1
    --on-surface-muted   9.3:1
    --red-300            7.2:1

### The red that was wrong everywhere

`tokens.css` already documented `--red-600` as "6.11:1 on white" and `--red-300`
as "the only red permitted on a navy section". Every red text colour in the
component library pointed at `--red-600` because the library was written light.
On `--surface` that measures 3.07:1 and fails at body size. Seven components were
repointed, including three that are not on any page yet, so the defect cannot
arrive later with a new page.

### Scope

Loading the system is opt-in per page: three pages link `tokens.css` today. The
other 1,594 are untouched by any of this, which is why a theme reversal of this
size was safe to make in one commit.
