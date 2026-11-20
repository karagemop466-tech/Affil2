# Executive Summary — ShopNow Kitchen (Verified Update — Session arena/d95938bb-affil2)

Date 2026-11-20 · Tracking ID in use `shopnow047c-20` (issuance unverified, FLG-002)
Live site https://karagemop466-tech.github.io/Affil2/ · Full version with source links: `executive-summary.html`

## What this is
A static publication-style Amazon affiliate site covering five submitted products in two categories:
three air fryers and two meat thermometers across 36 generated HTML pages (including 11 buying guides). Every specification is read
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
`scripts/build_site.py` generates all 36 HTML pages from `data/*.json`; nothing is hand-edited.
`scripts/check_site.py` fails the build if the disclosure is missing or below the fold, if a double-escaped entity or an image without alt/intrinsic size/loading appears, if a product's distinguishing name is missing from the front page or the shop index, if `assets/config.js` stops being loaded before `assets/app.js`, if any
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

## Session `arena/d95938bb-affil2` — storefront polish pass (2026-11-20)

This pass audited the built site rather than the data register, and fixed what a reader would
actually see. Every change below is generated from `scripts/build_site.py` or `data/`, and new gate
rules were added so none of them can silently return.

**What was wrong, and what it is now**

| Flag | Defect | Reader-visible symptom | Fix |
|---|---|---|---|
| FLG-041 | Cards identified a product by its brand only | The front page, shop and category grids showed "Chefman" twice with no way to tell the 6-quart from the 8-quart | Each product carries a distinguishing name in `data/products.json` (`Chefman 6-Qt Dual Basket` vs `Chefman 8-Qt TurboFry`), printed on cards, the compare header, the product-page byline, breadcrumb and `<title>` |
| FLG-042 | Entities were escaped twice | "Seasonal guide &#183; Holiday 2026" and "&#8212;" printed as raw codes on three pages | Entities are decoded before escaping; gate fails on any double-escaped entity |
| FLG-043 | Guide images bypassed the photo system | No dimensions (layout shift), no loading attribute, no illustration caption | Both moved into `assets/photos/` and rendered through the captioned figure component; gate now requires alt, width/height and loading on every image |
| FLG-044 | Nine classes had no CSS rule | Unstyled text inside styled cards (safety table, badges, spec chips, hero facts) | Rules added; a class-vs-stylesheet audit reports zero unstyled classes |
| FLG-045 | Six unused images were committed | Dead weight, and imagery that looked gated but was not | Deleted; the images on the site are exactly the images that pass the gate |
| FLG-046 | Design brief counts were stale | "8 live guides" where 11 are live | Counts computed at build time from the guide list |
| FLG-047 | Compare implied prices/ratings were absent | A reader was told the data does not exist, when the listing prints it and this site excludes it by policy | Wording corrected on `compare.html` and every product page; no value is printed |
| FLG-048 | Spec citations name fetch chunk numbers | Citations that look precise but cannot be re-run | Kept, and explained: trust the table and field name, not the chunk number |
| FLG-049 | The analytics switch was inert | `assets/config.js` documented an endpoint no page loaded, so turning measurement on did nothing | The shell loads `config.js` before `app.js`, and `app.js` reads `window.SITE_CONFIG.analyticsEndpoint` |

**Re-verification performed in this pass (official listings only, 2026-11-20)**

Titles re-read and matched for all five ASINs, and the `Product information` block read row by row
for four of them. Confirmed directly: P-01 max 450 °F / 120 V / 1700 W / 13.38 × 11.81 × 10.63 in /
13.3 lb / "6 liters" against "6 Quart"; P-03 1700 W and Max 400 °F against "450 °F Hi-Fry" in the
title (FLG-017, FLG-018), 12.8 lb, 8 quarts, Part Number RJ38-SQSS-8T; P-05 upper temperature
1000 °F, immersion depth 4.75 in, 5 sensors, Wi-Fi + Bluetooth; P-02 title (24 presets, "Six Cooking
Accessories Included") against the 25-preset and seven-accessory fields already published as
conflicts (FLG-021, FLG-031). Full record, including what was *not* re-read and why, is in
`data/reverification-2026-11-20-session-d95938bb.json` and rendered on `verification.html`.

Prices, star ratings, review counts and best-seller ranks were visible on the listings in this pass
and are still not printed anywhere (Program Policies §2(b); FLG-005).

**Still blocked, unchanged, and not presented as done:** the one-Special-Link-per-product test
(FLG-004), tracking-ID activity (FLG-002), short-link compliance (FLG-003), Search Console
(FLG-028), a deployed collector (FLG-010), a custom domain (FLG-006), a named editor (FLG-033), and
any hands-on testing (FLG-032). All are owner actions; none can be completed from this environment.

**Gate status after this pass:** `python3 scripts/check_site.py` → 36 pages, 5 product records,
49 flags, 19 sources, ALL CHECKS PASS. Unit tests and the Node collector/client suite pass.

## Verification log (2026-11-20, session arena/9f19fe6b-affil2)
- Synced cleanly with `origin/main` (`21424ae`, preserving PRs #17–#36 including `design-brief.html`, storefront photos, `pairCompare`, `guides/first-week-air-fryer.html`, and dated `sources.html` changelog).
- Verified all 5 `link.amazon/*` short links, deep chunks across all 5 `/dp/` product pages, and official docs (`S01`–`S04`, `S20`–`S24`) live on 2026-11-20.
- `python3 -B scripts/build_site.py` built all 36 pages idempotently.
- `python3 -B scripts/check_site.py` passed (`checked 36 pages, 5 product records, 49 flags, 19 sources — ALL CHECKS PASS`).
- `python3 -B -m unittest discover -s tests -p "test_*.py" -v` passed (3 tests OK).
- `node tests/test_collector.js` passed (collector server, Cloudflare Pages Function, and client JS DOM/search/nav/CSV/telemetry tests).
