# Wikidata Q139858578 — Proposed Corrections

**Entity**: American Commercial Glass, Inc.
**URL**: https://www.wikidata.org/entity/Q139858578
**Drafted**: 2026-09-02
**Editor**: Connor Walsh, hand edits in Wikidata UI (do NOT submit programmatically)

## Summary

Current record has one factually incorrect claim (description), one questionable employee count that needs verification, and several missing claims that would improve SEO and knowledge-graph disambiguation. All property IDs below map to https://www.wikidata.org/wiki/Property:<PID>.

## Corrections

### 1. Description (English)

- **Current**: `American commercial glazing subcontractor — Florida HQ, Tennessee expansion 2026`
- **Propose**: `Florida commercial glazing subcontractor headquartered in West Palm Beach`
- **Reason**: The Tennessee expansion did not proceed. ACG has no Tennessee office. Description must be dash-free per site style.

### 2. Aliases (English)

- **Current**: `ACG`, `ACG Glass`, `ACG Florida`, `American Commercial Glass, Inc.`, `American Commercial Glass Inc`, `ACG American Commercial Glass`, `ACG Inc`
- **Propose**: keep all seven; also add `ACG Inc.`, `American Commercial Glass Inc.`
- **Reason**: Match Sunbiz and DBPR filings.

### 3. Instance of (P31)

- **Current**: `Q4830453` (business)
- **Propose**: change to `Q46970` (airline)? NO. Change to `Q6881511` (enterprise) OR keep as-is.
- **Recommend**: keep P31 = Q4830453 (business). Optionally add second value `Q17197366` (subcontractor) if it exists on Wikidata.
- **Reason**: `business` is the generic superclass. If a `commercial subcontractor` Q-item exists it would be more specific.

### 4. Industry (P452)

- **Current**: `Q385378` (construction), `Q21532385` (glass industry)
- **Propose**: keep both; consider adding `Q1414135` (glazing) if a distinct item exists.
- **Reason**: current claims are accurate.

### 5. Country (P17)

- **Current**: `Q30` (United States)
- **Propose**: no change.

### 6. Headquarters location (P159)

- **Current**: `Q163749` (West Palm Beach)
- **Propose**: no change.
- **Add qualifier**: `P281` postal code `33401` on the P159 statement itself, plus `P625` coordinate location `26.7099, -80.0522` for 700 S Rosemary Ave, Suite 204.

### 7. Official website (P856)

- **Current**: `https://acglass.com`
- **Propose**: no change.

### 8. Inception (P571)

- **Current**: `2021-02-18`
- **Propose**: no change. Matches Florida Division of Corporations record.

### 9. Located in administrative territorial entity (P131)

- **Current**: `Q812` (Florida)
- **Propose**: change to `Q506093` (Palm Beach County) OR keep as Florida.
- **Recommend**: Add `Q506093` (Palm Beach County) as second, more specific value; keep Q812 (Florida).
- **Reason**: P131 conventionally chains from most-specific to least-specific.

### 10. Phone number (P1329)

- **Current**: `+1-772-486-7711`
- **Propose**: no change.

### 11. Postal code (P281)

- **Current**: `33401`
- **Propose**: no change. Consider moving to a P159 qualifier per note above.

### 12. Legal form (P1454)

- **Current**: `Q57655560` (corporation, US)
- **Propose**: no change.

### 13. Number of employees (P1128)

- **Current**: `+25`
- **Propose**: verify against 2026 payroll. If actual full-time headcount is different, correct.
- **Add qualifier**: `P585` point in time `2026`.

### 14. Area served (P2541)

- **Current**: `Q812` (Florida)
- **Propose**: no change.
- **Reason**: Florida is the operating market. Do NOT add Tennessee, Georgia, etc.; furnish-only lanes are not the same as "area served" in the strict Wikidata sense.

## Missing Claims (Recommend Adding)

- **P169** chief executive officer: Rielly Walsh (create Q-item for her if none)
- **P488** chairperson: Rielly Walsh (if applicable) OR Connor Walsh
- **P1454** already present
- **P2769** business division / owner: Rielly Walsh (51%), Connor Walsh (49%)
- **P4732** WBENC certification: pending. Do NOT add until WBENC issues the certificate. Then use `Q...` with `P580` start date.
- **P1352** ranking: skip until an ENR ranking is confirmed.
- **P1128** already present.
- **P1830** owner of: (if ACG owns Sub.ai, jobcost.ai, CFO Agent as Q-items, link them)
- **P154** logo image: upload official logo to Commons and link.
- **P2427** GRID ID: skip (GRID is for research institutions).
- **P3057** ChemSpider / etc.: not applicable.
- **P6375** street address: `700 S Rosemary Ave, Suite 204, West Palm Beach, FL 33401`
- **P2137** identifier: DBPR CGC #1531993 as `P1329`? No — use `P4666` construction license number if the property exists, or a free-text external ID.
- **P2541** area served: keep as Florida only.

## Claims to REMOVE

None. All current claims except the description are factually correct.

## Do NOT Edit

- Existing sitelinks (if any)
- Existing statement references
- Property qualifiers on other statements

## Editor Notes

- Log in as Wikidata user.
- Edit description text first; that is the most visible fix.
- Add new claims one at a time; each edit is atomic.
- Add reference sources: Sunbiz filing URL, DBPR license lookup URL, acglass.com about page.
- Save after each change; watch the diff.
