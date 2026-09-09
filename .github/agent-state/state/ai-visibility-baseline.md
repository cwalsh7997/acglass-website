# AI / LLM search visibility: first recorded baseline

Measured 2026-09-09 by running each query through a live web-search engine and
reading the answer and the cited URLs. This is a proxy for a search-grounded
model, not a replacement for the real thing.

**The automated audit has never produced a number.** `.github/workflows/ai-visibility.yml`
runs 10 prompts across Perplexity, Gemini and OpenAI monthly, and has failed on
2026-07-01, 2026-08-01 and 2026-09-01 with `Missing required secret 'PPLX_API_KEY'`.
Until `PPLX_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `SHEETS_SA_JSON`,
`SHEETS_ID` and `SLACK_WEBHOOK` are set, there is no trend, only this snapshot.

## Where ACG stands

| query | ACG in the answer | ACG URLs cited | who owns it otherwise |
|---|---|---|---|
| commercial glazing contractor West Palm Beach | **1st** | west-palm-beach-commercial-glazing.html | Miller Glass, RAD Glass, AP Glazing, Avery Glass |
| commercial glazing Naples storefront curtain wall | **1st** | acglass.com, /miami/, /palm-beach/ | Florida Engineered Glass, Collier Custom Glass, Luxurious Glass |
| impact storefront glazing installer Miami | **1st** | /miami/, storefront-installer-miami.html, commercial-storefront-systems.html | Impact Glass Services, Ultimate Pros, ASP Windows |
| best commercial glazing contractor Florida | 4th, filed under "South Florida" | none | downtobid directory pages sweep the SERP |
| best commercial glazing contractor in Tampa | **absent** | none | JEM Glass, Ashe Glass, All Phase Glass |
| who is American Commercial Glass | present but contaminated | acglass.com pages | see below |

The pattern is consistent: **where ACG has a city page that ranks, the model puts
ACG first and quotes ACG's own numbers back verbatim** ("350+ projects, Florida
CGC #1531993, bonded $3M/$6M"). Where ACG has no ranking page, competitors own
the answer completely.

## Entity contamination on the brand query

Asked who ACG is, the answer returns a second, contradictory history:

> "Founded in 2001 by Jeffrey Walsh, Liberty Home Builders Inc. ... American
> Commercial Glass, a division of Liberty Home Builders"

against the site's and Wikidata's `foundingDate 2021-02-18`. The source is the
legacy domain. That domain is clean now (`acommercialglass.com` 301s at the root
and 404s every path), so this is stale index and model memory, not live content.
It decays on its own; a Search Console removal request speeds it up.

## Citations that disagree with each other

| signal | acglass.com | Wikidata Q139858578 | downtobid West Palm Beach |
|---|---|---|---|
| phone | 772-486-7711 (62 uses) | +1-772-486-7711 | **(561) 800-4221** |
| website | acglass.com | https://acglass.com | **acommercialglass.com** |

The 561 number is real: it appears 112 times in ACG's own records including bid
templates. Two live numbers split across citations weakens entity resolution.
Which one is canonical for public listings is Connor's call.

## Directory coverage, on the sites that own these SERPs

`downtobid.com/contractors/glazing/{city}` outranks almost everything for
"best commercial glazing contractors {city}".

| city | ACG listed |
|---|---|
| West Palm Beach | **#1 of 15**, but wrong domain and the other phone number |
| Tampa | **absent** |
| Miami | **absent** |
| Naples | page returns 404, no listing exists |

## Named competitors surfaced by these queries

JEM Glass (Tampa) · Southern Glass Products (Lakeland) · Dash Door & Glass ·
Ashe Glass & Mirror · All Phase Glass & Mirror · Miller Glass & Glazing ·
RAD Glass · AP Glazing · Avery Glass & Mirror · Florida Engineered Glass ·
Collier Custom Glass · Luxurious Glass · Impact Glass Services · Aluminate Glass ·
LMG Glass & Mirror

ACG publishes `acg-vs-*` comparison pages for Giroux, Harmon and Permasteelisa,
which are national curtainwall firms. None of the Florida names above, which are
the ones actually returned for these searches, has one.
