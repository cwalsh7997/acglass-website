# Prune wave 2

Inventory counted on branch `seo-auto`, 2026-09-03. **Applied 2026-09-03** on `cursor/seo-auto-wave2-6d6c`: `noindex,follow` + self-canonical + sitemap drop. HTML files were not deleted. No 301.

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

Thin/template evidence is the same shape on every sample: city-swapped title, a description from a small phrase bank, shared Haines EOC OG image, ~850-910 words on the city-service pages, geo tags for the city.

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

Deeper than the city-service folders (~1,200-2,300 words) but still templated. 62 of 101 titles are `Storefront Glazier in {City}, FL | ACG - 48-Hr Bids`.

| URL | Title | Words (approx.) | Notes |
| --- | --- | --- | --- |
| `/storefront-glazier-alys-beach-florida/` | Commercial Storefront Glazier in Alys Beach, FL \| ACG | 1342 | 135 mph design-wind line in the description (not re-verified here). |
| `/storefront-glazier-fort-walton-beach-florida/` | Commercial Storefront Glazier in Fort Walton Beach, FL \| ACG | 1202 | Okaloosa County line; shorter of the set. |
| `/storefront-glazier-miami-beach-florida/` | Storefront Glazier in Miami Beach, FL \| ACG - 48-Hr Bids | 2209 | 48-Hr Bids title bank |
| `/storefront-glazier-port-saint-lucie-florida/` | Storefront Glazier in Port St. Lucie, FL \| ACG - 48-Hr Bids | 2290 | Same title bank |
| `/storefront-glazier-winter-haven-florida/` | Storefront Glazier in Winter Haven, FL \| ACG - 48-Hr Bids | 2277 | Correct "Haven" slug, unlike `winter-heaven/` city folder |

No `storefront-glazier-jacksonville-florida/` exists. Jacksonville's declared storefront primary is `/storefront-installer-jacksonville.html`.

## Applied 2026-09-03

**noindex,follow + self-canonical + sitemap drop.** HTML files were not deleted. No 301. GitHub Pages cannot HTTP 301 without Cloudflare, and Cloudflare is out of scope.

| Set | Noindexed | Kept indexable |
| --- | --- | --- |
| `/{city}/commercial-storefronts/` | 77 | 0 |
| `/{city}/glass-railings/` | 77 | 0 |
| `/{city}/impact-windows-hurricane/` | 77 | 0 (no sibling impact folder exists) |
| `/storefront-glazier-{city}-florida/` | 93 | 8 keepers below |

**Total URLs noindexed: 324.**

Keepers (staffed offices + satellites that exist in this filename pattern): `/storefront-glazier-west-palm-beach-florida/`, `/storefront-glazier-naples-florida/`, `/storefront-glazier-tampa-florida/`, `/storefront-glazier-miami-florida/`, `/storefront-glazier-orlando-florida/`, `/storefront-glazier-fort-lauderdale-florida/`, `/storefront-glazier-fort-myers-florida/`, `/storefront-glazier-sarasota-florida/`. Jacksonville has no `storefront-glazier-jacksonville-florida` file; none was created.

Left indexable, not in the city-slug count of 101: `/storefront-glazier-florida/` (statewide GC guide). That is the 102nd `storefront-glazier-*-florida` glob match.

`/boca-raton/` city root is now self-canonical and listed in `sitemap.xml` + `sitemap-cities.xml` so crawl-check still has a Boca market in a sitemap after `/storefront-glazier-boca-raton-florida/` was noindexed and dropped. Boca is a gsc-gated storefront primary in `url-primaries.json`; that registry row was not flipped.

A later 301 of the 93 onto the nearest keeper (or onto `/commercial-glazing-jacksonville.html` for North Florida) needs Cloudflare and a GSC equity check. [NEED: GSC clicks/impressions on the 93.] Do not delete directories.
