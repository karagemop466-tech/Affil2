# Executive Summary — ShopNow Kitchen (Verified Update — through session arena/ca4af934-affil2, T-24)

Date 2026-11-20 · Tracking ID in use `shopnow047c-20` (issuance unverified, FLG-002)
Live site https://karagemop466-tech.github.io/Affil2/ · Full version with source links: `executive-summary.html`

## What this is
A static publication-style Amazon affiliate site covering five submitted products in two categories:
three air fryers and two meat thermometers across 33 generated HTML pages (including 9 buying guides). Every specification is read
from the official Amazon listing (including deep `Product information` tables), dated and linked.
Where two parts of one listing disagree, both figures are printed and the disagreement is flagged.
No price, star rating, review count or best-seller rank is reproduced, because Amazon's Program
Policies Participation Requirements §2(b) and §6(t) only permit that when Amazon serves the link or
the data comes through the Product Advertising / Creators API.

## The five products, as observed on 2026-11-20
| ID | Submitted link | Observed ASIN | Official listing |
|----|----------------|---------------|------------------|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH |
| P-04 | link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z |

Earlier attempts on 2026-11-20 resolved four short links while `link.amazon/B0c8moW59` hit
Amazon checkpoint/HTTP 500 pages four times (FLG-012). On follow-up re-test (`arena/9f19fe6b-affil2`,
2026-11-20), all five short links resolved cleanly to their respective `/dp/<ASIN>` pages, including
`B0c8moW59 -> B0DHZTCNR5`. Redirects can still behave inconsistently between visits (FLG-011), so each
observed ASIN remains a dated snapshot rather than owner-confirmed intent (FLG-001).

## Sources (19 official sources in `data/sources.json`)
- S01 Operating Agreement §5 — https://affiliate-program.amazon.com/help/operating/agreement
- S02 Program Policies (Commission Income §2(d)/(e)/(g), Participation §2(a)/(b), §5 ML restriction, §6(t)/(v)/(w)/(y), IP License §1, §2(e)/(h)/(i)/(k), §4 Agent Terms) — https://affiliate-program.amazon.com/help/operating/policies
- S03 FTC Endorsement Guides FAQ — https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- S04 Google, Qualify your outbound links — https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- S10–S14 the five `/dp/` Amazon product listings; S15–S19 the five supplied `link.amazon` short links
- S20 Amazon Creators API onboarding — https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api
- S21 PA-API 5 deprecation notice — https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation
- S22 USDA FSIS Safe Minimum Internal Temperature Chart; S23 FTC Disclosures 101; S24 USDA FSIS Food Thermometers calibration guide

## Register fields verified from deep Product information tables on 2026-11-20
| Product | Field | Value now published | Where on the listing |
|---|---|---|---|
| P-01 Chefman 6 Qt | Item Weight | 13.3 pounds | Product information — Measurements table |
| P-02 Emeril 26QT | Model | 4-00675-02X-VN | Item details: Model Number / Part Number (conflict vs earlier `4-00675-02`, FLG-009) |
| P-02 Emeril 26QT | Temperature | 75–500 °F | Features & Specs: Min 75 °F, Max 500 °F |
| P-02 Emeril 26QT | Power | 120 V / 1700 W | Features & Specs: Output Wattage, Wattage, Voltage |
| P-03 Chefman 8 Qt | Item Weight | 12.8 pounds | Product information — Measurements table |
| P-03 Chefman 8 Qt | Power | 1700 W vs 1000 W | Features & Specs (`1700 W`) vs About this item (`1000 W`, FLG-017) |
| P-04 ThermoMaven | Model | HT07 | Item details: Model Name / Model / Part Number |
| P-04 ThermoMaven | Upper temperature | 572 °F | Features & Specs: Upper Temperature Rating (also `6.5 in` depth, `Wipe Clean`) |
| P-05 CHEF iQ Sense | Model | CQ60-3C-Z1-E | Item details: Model / Part Number |
| P-05 CHEF iQ Sense | Probe length | 4.75 in | Immersion Depth; Measurements: Item Length |
| P-05 CHEF iQ Sense | Warranty | 2-yr vs 3 Year | About this item (`two-year`) vs Item details (`3 Year`, FLG-038 / FLG-019) |

An unverified Emeril (P-02) weight figure (`26.5 lb`) previously in three guides was purged because
`B09B7SB46R` omits item weight (FLG-022, FLG-039), while `P-01` (`13.3 lb`) and `P-03` (`12.8 lb`)
were confirmed directly in their `Measurements` tables.

## Active listing conflicts published to buyers
| Flag | Product | Contradiction |
|------|---------|---------------|
| FLG-008 | CHEF iQ Sense | 50 hours battery in About this item vs 70 hours in an earlier Product Description capture |
| FLG-009 | Emeril 26 QT | `4-00675-02X-VN` in live Item details vs `4-00675-02` in an earlier capture |
| FLG-017 | Chefman 8 Qt | `1700 W` in Features & Specs vs `1000 W` in About this item |
| FLG-018 | Chefman 8 Qt | `400 °F` max in About this item & spec field vs `450 °F Hi-Fry` in title |
| FLG-038 | CHEF iQ Sense | `two-year assurance` in About this item vs `3 Year` in Item details (prior register FLG-019) |
| FLG-021 | Emeril 26 QT | 24 presets in title, Configuration & Description vs 25 in About this item |
| FLG-031 | Emeril 26 QT | Six accessories in title & Included Components vs 7 in Configuration & Description |
| FLG-034 | Chefman 6 Qt | 6 quarts in title & bullets vs 6 liters in Measurements field |

## Not verified, and published as such
Intended ASIN per product (FLG-001) · whether the tracking ID is live (FLG-002) · whether the
short-link format is permitted for this placement (FLG-003) · the one-per-product Special Link test
(FLG-004) · P-02 item weight & HTML warranty terms (FLG-022) · NIST/NSF and cETL certification
beyond listing statements (FLG-035) · any hands-on experience (FLG-032) · a named author (FLG-033).

## Decisions that change the numbers
1. Complete the link test (SG-07, Q-04) — nothing about revenue can be reported until it passes.
2. Amazon Creators API access (SG-13, SG-31, Q-19) — the only compliant route to showing prices, product images, and automated catalog data (with ML training barred under Program Policies §5 / IP §1 & §2(e)).
3. Search Console verification (SG-10, SG-29, SG-32, Q-20) — the only way to pick future guides from measured organic queries.
4. Self-hosted analytics hosting (SG-25, Q-08) — deploy `analytics/server.js` or `functions/api/collect.js` beyond static GitHub Pages.
5. A custom domain (SG-14, FLG-006, Q-05) — canonicals currently point at the Pages subpath.

## Honest position on revenue
Zero, and no forecast. No commission rate, click, session or order figure is presented because nothing
from an authorised first-party report exists yet. `campaign-ledger.html` is intentionally empty, with
its schema and provenance rule written down so the first real row can be added without redesigning
the page.

## How the site is kept honest
`scripts/build_site.py` generates all 33 HTML pages from `data/*.json`; nothing is hand-edited.
`scripts/check_site.py` fails the build if the disclosure is missing or below the fold, if any
`amazon.com` link lacks `rel="sponsored nofollow"`, if a price, star rating, cross-row placeholder, or
unverified weight claim appears, if a link or asset is broken, if any SVG schematic is orphaned, if
any generated photo lacks a caption/alt/dimensions, if any table has mismatched `<thead>`/`<tbody>`
column counts, if a page is missing from the sitemap, if JSON-LD does not parse, or if an undefined
or unpublished flag exists. CI runs regeneration, drift detection, `check_site.py`, Python unit tests
(`tests/test_site.py`), and Node.js collector/client tests (`tests/test_collector.js`).

## Suggestions & Open Questions across sessions (`SG-17..SG-32`, `Q-15..Q-20`)
- `SG-17` (`design-brief.html`): Publication design prompt, 4-cluster topic plan, seasonal calendar, and 10 editorial standards — shipped.
- `SG-18`–`SG-24`, `SG-26`–`SG-30`, `Q-15`–`Q-18`: Storefront issue calendar, intent pages, dated reader change log (`sources.html`), 2-product compare (`compare.html`), first-week air fryer guide (`guides/first-week-air-fryer.html`), editor decision, hands-on policy, RSS/Search Console tracking, imagery & jurisdiction questions — shipped/tracked cleanly.
- `SG-25` (`measurement.html`): Zero-dependency `analytics/server.js`, Cloudflare Pages `functions/api/collect.js`, `data/events.json`, RFC-4180 CSV export, and `assets/app.js` `send()` shipped in repo; external hosting remains pending (`FLG-010`, `Q-08`).
- `SG-31` (`platform.html`) / `Q-19`: AI affiliate platform blueprint and compliance matrix shipped; automated catalog ingestion remains blocked until Creators API acceptance (`S20`, `S21`, `FLG-029`).
- `SG-32` / `Q-20`: Question-shaped article generation from Search Console queries (blocked until SG-10 / SG-29 verification).

## Verification log (2026-11-20, session arena/9f19fe6b-affil2)
- Synced cleanly with `origin/main` (`21424ae`, preserving PRs #17–#36 including `design-brief.html`, storefront photos, `pairCompare`, `guides/first-week-air-fryer.html`, and dated `sources.html` changelog).
- Verified all 5 `link.amazon/*` short links, deep chunks across all 5 `/dp/` product pages, and official docs (`S01`–`S04`, `S20`–`S24`) live on 2026-11-20.
- `python3 -B scripts/build_site.py` built all 33 pages idempotently.
- `python3 -B scripts/check_site.py` passed (`checked 36 pages, 5 product records, 46 flags, 19 sources — ALL CHECKS PASS`).
- `python3 -B -m unittest discover -s tests -p "test_*.py" -v` passed (3 tests OK).
- `node tests/test_collector.js` passed (collector server, Cloudflare Pages Function, and client JS DOM/search/nav/CSV/telemetry tests).

## Verification log (2026-11-20, session arena/ca4af934-affil2 — T-24 independent pass (claimed as T-21 pre-merge; renumbered twice after ID collisions with parallel sessions))
Independent line-by-line re-verification against live official pages (this session's own fetches,
not inherited):

| Check | Source | Result |
|---|---|---|
| P-01..P-05 listing titles | https://www.amazon.com/dp/B0CDY277D3 · /dp/B09B7SB46R · /dp/B08DKYBTPH · /dp/B0DHZTCNR5 · /dp/B0DZFD6R9Z | All five live titles match the register strings exactly |
| P-03 Product information tables | https://www.amazon.com/dp/B08DKYBTPH | Line-by-line match: Item Weight 12.8 pounds; Dimensions 12.75"D x 13.5"W x 10"H; Capacity 8 quarts; Output Wattage/Wattage 1700 watts; Voltage 120 volts; Max Temperature Setting 400 °F; Part Number RJ38-SQSS-8T; Warranty Description 1-Year Limited Warranty; the 1700 W vs 1000 W conflict (FLG-017) and the 400/450 °F conflict (FLG-018) remain as published |
| P-05 Features & Specs | https://www.amazon.com/dp/B0DZFD6R9Z | Line-by-line match: Upper Temperature Range 1000 °F; Immersion Depth 4.75 inches; 5 Sensors; Bluetooth + Wi Fi; Dishwasher Safe |
| FTC Endorsement Guides FAQ (S03) | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Live; disclosure wording relied on ("connection … disclosed clearly and conspicuously") confirmed |
| Google qualify outbound links (S04) | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Live; rel="sponsored" for paid links and multiple rel values confirmed |
| USDA FSIS temperature chart (S22) | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart | Live; 145 °F + 3-min rest (steaks), 160 °F (ground meats), 165 °F (poultry, leftovers) match the site's USDA table; chart dated 2025-04-14 |

**Not re-reached in this pass (inherited from same-day passes by sessions 530c2e6c / 937876a6 / 9f19fe6b, citations already in `data/products.json`):** the P-01, P-02 and P-04 deep spec tables (this session's chunk fetches landed on ad modules due to pagination drift; the earlier cited captures stand, and nothing was re-marked as verified on their behalf). Prices, ratings and buy-box state remain deliberately unrecorded (FLG-005).

## Table audit (2026-11-20, T-24)
333 table rows across 33 pages audited: 174 rows carry direct external source links; 84 carry an explicit blank/flag/policy marker (blank values, `PENDING`, "not shown, by policy", FLG- references); the remaining 75 are planning, decision, question, event-schema or ledger rows (internal records with explicit statuses, not product claims) or data rows whose table caption and headers carry the official links (compare view: 4 rows; USDA doneness tables: 8 rows, USDA chart linked in each caption). Every data value row on product pages (spec tables, intent record) now carries a row-level link to the official listing or the supplied short link. Row-level exemptions, all documented: compare-view data rows (traceable via column headers → product pages → row-level sources, plus the five listing links now in the caption), USDA doneness rows (single-source table, USDA chart linked in the caption), the five-event schema tables (the site's own contract, `data/events.json`), and the decision/question/ledger registers (internal records with explicit statuses, not product claims).

## Defects found and fixed by this pass (session arena/ca4af934-affil2)
1. Double-escaped HTML entities (`&plusmn;`, `&mdash;`, `&nbsp;`, `&deg;`) rendered literally in four guide `sub`/`intro` strings on `guides.html` and guide pages — replaced with real characters (confirmed fixed in generated output).
2. Product-intent confirmation record rows for the observed redirect target, model provenance, confirmation date, token and observation note lacked row-level links — now each links the official listing or the supplied link (intended vs observed fields remain separate; intended stays blank per FLG-001).
3. Compare-table caption now carries the five official listing links and states the traceability path per column.
4. New flag **FLG-047** (cosmetic; raised as FLG-041 before the ID collision with main's FLG-041..046 was visible, then renumbered): the P-03 URL slug `p03-chefman-8qt-turbrofry` misspells the listing's "TurboFry" name. Rename would change a published URL, so it is left to the owner's decision; no data affected.

## Manual review links (all official)
- Product listings: https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z
- Supplied short links: https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV · https://link.amazon/B0c8moW59 · https://link.amazon/B0f3GKalj
- Amazon Associates Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement (S01) · Program Policies: https://affiliate-program.amazon.com/help/operating/policies (S02) — both login-gated; wording left for manual review (FLG-026 covers URL health)
- FTC Endorsement Guides FAQ: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking (S03) · FTC Disclosures 101: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers (S23)
- Google qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links (S04)
- Creators API onboarding: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api (S20) · PA-API 5 deprecation: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation (S21)
- USDA FSIS temperature chart: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart (S22) · thermometer calibration: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers (S24)

## Open parallel pull requests (owner review; untouched by this session)
PRs #28 (`59ada9df`), #29 (`bba2deed`), #34 (`82c875a9`) and #35 (`36170d15`) were opened by earlier parallel sessions and left open. Per the coordination protocol this session neither merged nor closed another session's claimed work; several of their themes are already covered on `main` (collector stack in PR #31, storefront in PR #30). Review links: https://github.com/karagemop466-tech/Affil2/pulls
