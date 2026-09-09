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

## The other number

`(561) 800-4221` is a real ACG line. It appears 112 times in ACG's own records,
including bid templates, and it is what `downtobid.com` publishes. It is **not**
the number for public citations. It never appeared on acglass.com.

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
4. **BBB, Procore, Facebook**: confirm each shows 772-486-7711 and acglass.com.

## Gap: no Google Business Profile in sameAs

The Organization node lists Wikidata, LinkedIn, Facebook, Instagram, Procore and
BBB. There is no Google Business Profile. The only Google Maps URLs on the site
are generic city embeds, not a business listing. A verified GBP per office is one
of the strongest signals available for both local pack and AI answers, and ACG
has three addresses that would each support one.
