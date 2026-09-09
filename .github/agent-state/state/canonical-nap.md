# Canonical NAP for every ACG citation

**Decided by Connor, 2026-09-09.** Any listing, profile, or citation ACG controls
uses exactly this. Where a directory shows something else, the directory is wrong.

```
Name      American Commercial Glass
Phone     (772) 486-7711          <- canonical, decided 2026-09-09
Website   https://acglass.com     <- canonical, not acommercialglass.com
Address   700 S Rosemary Ave Suite 204, West Palm Beach, FL 33401
License   FL CGC #1531993
```

Offices, all reachable on the same number:

| office | address |
|---|---|
| West Palm Beach (HQ) | 700 S Rosemary Ave Suite 204, West Palm Beach, FL 33401 |
| Naples | 4850 Tamiami Trail N Ste 301, Naples, FL 34103 |
| Tampa | 3031 N Rocky Point Dr W Ste 600, Tampa, FL 33607 |

## Google Business Profiles, per Connor 2026-09-09

| location | GMB | on acglass.com | DBPR / SunBiz |
|---|---|---|---|
| West Palm Beach | **verified** | published as HQ | SunBiz principal address |
| Stuart | **verified** | **not mentioned anywhere** | DBPR license address, SunBiz registered agent |
| Naples | not verified | published as an office | not listed |
| Tampa | not verified | published as an office | not listed |

Two things are inverted here and both are worth Connor's attention.

**Stuart is ACG's strongest verified local signal and the site is silent about
it.** A verified profile, the DBPR license address, and the SunBiz registered
agent address all say Stuart, 257 SE Monterey Road, 34994. The website says
West Palm Beach, Naples and Tampa, and never says Stuart. A general contractor
who follows the instruction on
florida-commercial-glazing-contractors-compared.html, "type the number" into
DBPR, lands on a Stuart address against a page claiming a West Palm Beach HQ.
Nothing here is false. It is unexplained, which is a different problem and a
fixable one.

**The two offices the site does claim are the two without a verified profile.**
Naples and Tampa carry no GMB verification, so the two locations doing the most
work in the site's local SEO have the least external corroboration.

Whether Stuart should appear on the site is a location claim and therefore
Connor's decision, not an agent's. It is not recorded here as an office.

## The other numbers

There are **three** real ACG numbers in circulation, not two. None of the other
two has ever appeared on acglass.com, and both are published by third parties.

| number | occurrences in ACG's own records | published by |
|---|---|---|
| **(772) 486-7711** | canonical, 12,740 on acglass.com | acglass.com, Wikidata |
| (561) 800-4221 | 112, including bid templates | downtobid.com |
| (561) 283-8030 | 687, including live email correspondence | Yelp, Yahoo Local |

All three are real. Only 772-486-7711 is for public citation. Three numbers
across citations is a materially weaker entity signal than the two originally
recorded here, because each one anchors a separate cluster of listings.

## State of every citation, checked 2026-09-09

| surface | phone | website | status |
|---|---|---|---|
| acglass.com | 772-486-7711, 12,740 uses across 4 formats | acglass.com | correct, no change needed |
| Wikidata Q139858578 | +1-772-486-7711 | https://acglass.com | correct |
| downtobid.com West Palm Beach | **(561) 800-4221** | **acommercialglass.com** | **both wrong** |
| BBB profile | not checked | not checked | in sameAs |
| Procore network | not checked | not checked | in sameAs |
| Facebook | not checked | not checked | in sameAs, handle is acommercialglass |

## Off-site actions, in impact order

1. **downtobid.com** West Palm Beach entry: change phone to (772) 486-7711 and
   website to acglass.com. ACG is #1 of 15 there and it is the page that outranks
   almost everything for "best commercial glazing contractors west palm beach".
2. **downtobid.com** Tampa and Miami: ACG is absent from both. Naples has no page.
3. **Google Search Console**: removal request for stale `acommercialglass.com`
   URLs. The brand query still returns "founded in 2001, a division of Liberty
   Home Builders" against ACG's actual 2021-02-18 founding.
4. **BBB, Procore, Facebook, Yelp, Yahoo Local**: confirm each shows 772-486-7711
   and acglass.com. Yelp currently publishes (561) 283-8030.
5. **Add the verified West Palm Beach profile to the Organization sameAs.** It is
   the single strongest local signal ACG holds and the schema does not reference it.

## Gap: the verified profiles are not in sameAs

The Organization node lists Wikidata, LinkedIn, Facebook, Instagram, Procore and
BBB. It references no Google Business Profile, although two are verified. The
only Google Maps URLs on the site are generic city embeds, not business
listings. Wiring the verified West Palm Beach profile into sameAs needs its
Maps URL, which has to come from the account. It cannot be derived from a search
result without guessing, and a guessed identifier is worse than none.
