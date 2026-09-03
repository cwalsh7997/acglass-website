# Prune wave 2 (inventory only)

Decision aid. **No noindex, sitemap drop, or 301 was applied in this pass.** Do not delete pages.

Counted on branch `seo-auto`, 2026-09-03. Pattern counts only, plus five example URLs each. City service folders and the storefront-glazier set stay indexable until Connor picks a move.

## Pattern counts

| Pattern | Files on disk | In `sitemap.xml` | In `sitemap-cities.xml` | Notes |
| --- | --- | --- | --- | --- |
| `/{city}/commercial-storefronts/` | **77** | 77 | 77 | Self-canonical. No `robots` meta (indexable by default). |
| `/{city}/glass-railings/` | **77** | 77 | 77 | Same. Two extra statewide pages exist outside this pattern (`/glass-railing-systems-florida/`, `/balcony-glass-railings-florida/`) and are not in this count. |
| `/{city}/impact-windows-hurricane/` | **77** | 77 | 77 | Same. |
| `/storefront-glazier-{city}-florida/` | **101** | 101 | 101 | User brief said 102. **101** files match `storefront-glazier-*-florida/index.html`. [NEED: the 102nd URL if it uses another slug.] |

77 × 3 city-service folders = **231**. Plus 101 storefront-glazier URLs = **332** indexable template URLs in these four patterns.

Adjacent, not in this wave: `/{city}/all-glass-entrances/` is **77** city folders plus `/all-glass-entrances/`. Do not treat that set as approved for noindex here.

Do not noindex the 225 blog posts. Do not touch city **root** folders for the three offices or the six satellites in this memo's apply step (there is no apply step).

## Five examples per pattern

Thin/template evidence is the same shape on every sample: city-swapped title, a description from a small phrase bank, shared Haines EOC OG image, ~850–910 words on the city-service pages, geo tags for the city.

### `/{city}/commercial-storefronts/`

Title bank is almost one string. 54 of 77 are `Commercial Storefront Installation in {City}, FL | ACG`.

| URL | Title | Words (approx.) | Description bank |
| --- | --- | --- | --- |
| `/aventura/commercial-storefronts/` | Commercial Storefront Installation in Aventura, FL \| ACG | 864 | "ACG delivers commercial Storefront Installation in {City}, FL - owner-operated, licensed CGC #1531993, bids in 48 hours." |
| `/fort-pierce/commercial-storefronts/` | Commercial Storefront Installation in Fort Pierce, FL \| ACG | 887 | "Need commercial Storefront Installation in {City}? ACG runs the full Division 08 scope." |
| `/lighthouse-point/commercial-storefronts/` | Commercial Storefront Installation in Lighthouse Point \| ACG | 910 | "Licensed FL glazing sub (CGC #1531993). Commercial Storefront Installation in {City} - impact-rated, bonded, 48-hour scope letters." |
| `/parkland/commercial-storefronts/` | Commercial Storefront Installation in Parkland, FL \| ACG | 863 | "{City} commercial Storefront Installation by ACG - HVHZ impact experience, one Division 08 subcontract, 48-hour scoped bids." |
| `/winter-heaven/commercial-storefronts/` | Commercial Storefront Installation in Winter Haven, FL \| ACG | 904 | Folder slug is `winter-heaven` (typo); title says Winter Haven. "owner-operated, woman-owned, Miami-Dade NOA experience." |

### `/{city}/glass-railings/`

66 of 77 titles are `Glass Railing Installation in {City}, FL | ACG`.

| URL | Title | Words (approx.) | Description bank |
| --- | --- | --- | --- |
| `/aventura/glass-railings/` | Glass Railing Installation in Aventura, FL \| ACG | 856 | HVHZ / one Division 08 subcontract / 48-hour scoped bids |
| `/fort-pierce/glass-railings/` | Glass Railing Installation in Fort Pierce, FL \| ACG | 902 | Same HVHZ bank as Aventura |
| `/lighthouse-point/glass-railings/` | Glass Railing Installation in Lighthouse Point, FL \| ACG | 896 | "ACG delivers glass Railing Installation in {City}, FL - owner-operated, licensed CGC #1531993, bids in 48 hours." |
| `/parkland/glass-railings/` | Glass Railing Installation in Parkland, FL \| ACG | 854 | "Need glass Railing Installation in {City}? ACG runs the full Division 08 scope." |
| `/winter-heaven/glass-railings/` | Glass Railing Installation in Winter Haven, FL \| ACG | 916 | Same typo folder. woman-owned / NOA bank |

### `/{city}/impact-windows-hurricane/`

54 of 77 titles are `Hurricane Impact Windows and Doors in {City}, FL | ACG`.

| URL | Title | Words (approx.) | Description bank |
| --- | --- | --- | --- |
| `/aventura/impact-windows-hurricane/` | Hurricane Impact Windows and Doors in Aventura, FL \| ACG | 826 | "Commercial impact window and door installation in {City}, with Division 08 glazing scope information from American Commercial Glass." |
| `/fort-pierce/impact-windows-hurricane/` | Hurricane Impact Windows and Doors in Fort Pierce, FL \| ACG | 889 | HVHZ / one Division 08 subcontract bank |
| `/lighthouse-point/impact-windows-hurricane/` | Hurricane Impact Windows and Doors in Lighthouse Point \| ACG | 861 | "Licensed FL glazing sub… impact-rated, bonded, 48-hour scope letters." |
| `/parkland/impact-windows-hurricane/` | Hurricane Impact Windows and Doors in Parkland, FL \| ACG | 823 | woman-owned / NOA bank |
| `/winter-heaven/impact-windows-hurricane/` | Hurricane Impact Windows and Doors in Winter Haven, FL \| ACG | 895 | Typo folder. owner-operated / 48-hour bank |

### `/storefront-glazier-{city}-florida/`

Deeper than the city-service folders (~1,200–2,300 words) but still templated. 62 of 101 titles are `Storefront Glazier in {City}, FL | ACG - 48-Hr Bids`.

| URL | Title | Words (approx.) | Notes |
| --- | --- | --- | --- |
| `/storefront-glazier-alys-beach-florida/` | Commercial Storefront Glazier in Alys Beach, FL \| ACG | 1342 | 135 mph design-wind line in the description (not re-verified here). |
| `/storefront-glazier-fort-walton-beach-florida/` | Commercial Storefront Glazier in Fort Walton Beach, FL \| ACG | 1202 | Okaloosa County line; shorter of the set. |
| `/storefront-glazier-miami-beach-florida/` | Storefront Glazier in Miami Beach, FL \| ACG - 48-Hr Bids | 2209 | 48-Hr Bids title bank |
| `/storefront-glazier-port-saint-lucie-florida/` | Storefront Glazier in Port St. Lucie, FL \| ACG - 48-Hr Bids | 2290 | Same title bank |
| `/storefront-glazier-winter-haven-florida/` | Storefront Glazier in Winter Haven, FL \| ACG - 48-Hr Bids | 2277 | Correct "Haven" slug, unlike `winter-heaven/` city folder |

No `storefront-glazier-jacksonville-florida/` exists. Jacksonville's declared storefront primary is `/storefront-installer-jacksonville.html`.

## Recommendation (not applied)

**Prefer noindex + sitemap drop** for the 231 city-service URLs and for storefront-glazier URLs that are not one of the nine coverage targets. Do **not** 301 the 231 onto the three office metros plus six satellites.

Rationale, one line each:

- **City-service 77×3:** These are city+service clones (storefront / railing / impact). A 301 onto `/west-palm-beach/`, `/naples/`, `/tampa/`, `/miami/`, `/orlando/`, `/jacksonville/`, `/fort-lauderdale/`, `/fort-myers/`, or `/sarasota/` would send railing and impact URLs at storefront or city-root aliases. Several of those city roots still `rel=canonical` to a storefront-glazier URL. Wrong intent, and GitHub Pages cannot issue HTTP 301 without a Cloudflare rule.
- **Storefront-glazier 101:** Keep the pages that already serve as declared or de-facto primaries for the three staffed offices and the six satellites that 200. On disk that is eight of this pattern: `/storefront-glazier-west-palm-beach-florida/`, `/storefront-glazier-naples-florida/`, `/storefront-glazier-tampa-florida/`, `/storefront-glazier-miami-florida/`, `/storefront-glazier-orlando-florida/`, `/storefront-glazier-fort-lauderdale-florida/`, `/storefront-glazier-fort-myers-florida/`, `/storefront-glazier-sarasota-florida/`. Jacksonville is the ninth coverage city but is not in this filename pattern. noindex + sitemap drop the other **93**. A later 301 of those 93 onto the nearest of the eight (or onto `/commercial-glazing-jacksonville.html` for North Florida) needs Cloudflare and a GSC equity check. [NEED: GSC clicks/impressions on the 93.]
- **Why not apply now:** Original week-1 rule still holds: do not noindex the 77×3 or the storefront-glazier set in this PR. This file is the inventory.

If Connor later wants a single move, do city-service noindex+drop first (thinner, one title bank). Leave storefront-glazier until GSC is in hand. Do not delete directories.
