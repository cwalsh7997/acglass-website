# Components

The closed set of 18 from `rules/01` section 9. Source: `src/components/components.css`.
Every value is a token from `src/styles/tokens.css`. Building a 19th requires an
approval line in the PR.

| # | Component | Class | Notes |
|---|---|---|---|
| 1 | Header | `.c-header` | Sticky, 5 nav items max, hamburger below 900px |
| 2 | MobileNavSheet | `.c-navsheet` | Opaque, `--e-2`, Esc closes, focus-trapped |
| 3 | HeroSplit | `.c-hero` | 7/5. One real photo, 4:3, no overlay, no text over it |
| 4 | ProofBar | `.c-proofbar` | Text facts only. No logos, no icons, no counters |
| 5 | CapabilityList | `.c-capabilities` | Text list, not cards. Max 6. Zero icons |
| 6 | ProjectCard | `.c-project` | No hover zoom. Border darkens, link underlines |
| 7 | ProjectGrid | `.c-projectgrid` | 3/2/1. Never masonry |
| 8 | SpecTable | `.c-spectable` | The workhorse. Mono keys, sans values, `tnum` |
| 9 | ProcessSteps | `.c-steps` | Vertical. Never horizontal, never icons or arrows |
| 10 | DocumentList | `.c-doclist` | Name, format, size, updated date |
| 11 | CTABand | `.c-ctaband` | Max 2 per page |
| 12 | FormBlock | `.c-form__*` | See rules/03 |
| 13 | OfficeCard | `.c-office` | Exactly three exist |
| 14 | FAQList | `.c-faq__*` | Native `details`/`summary`, chevron rotates 90deg |
| 15 | Breadcrumb | `.c-breadcrumb` | Mono, `--fs-sm` |
| 16 | Footer | `.c-footer` | **No licence block.** D5, D9 |
| 17 | StickyActionBar | `.c-stickybar` | Mobile only |
| 18 | TypographicPlate | `.c-plate` | The no-photo fallback. Prevents invented imagery |

## Page composition caps

Max 6 sections per page, hero counting as one. Max 2 `CTABand`, max 1 `ProofBar`,
max 1 `ProjectGrid`. No page uses more than 8 of the 18. No component appears more
than twice, except `SpecTable`, `ProjectCard`, `OfficeCard` and `DocumentList` rows.

## Why the Footer has no licence slot

`rules/01` section 9 item 16 and D5/D9. If a licence number ever renders anywhere,
it renders with "Qualifying agent: Jeff Walsh." in the same block. The component
deliberately provides no slot, so the rule cannot be violated by filling one in.
