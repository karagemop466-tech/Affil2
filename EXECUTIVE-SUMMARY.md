# Executive Summary — ShopNow Kitchen (Verified Update — Session arena/9f19fe6b-affil2)

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

---

# Session arena/0acc86ad-affil2 — shop voice, one indexable site, independent re-verification

Date 2026-11-20 · Tracking ID `shopnow047c-20` (issuance still unverified, FLG-002) ·
Live https://karagemop466-tech.github.io/Affil2/ · Branch `arena/0acc86ad-affil2`

## What was wrong with the site (and what changed)

The facts were right; the voice was a newsroom's. Buyer pages carried the project's filing
system: "chunk 7" crawl citations in 64 places, bare `FLG-0xx` ticket numbers on every product
card, a "Product-intent confirmation record" heading, and a "Specifications, line by line"
table that read like an audit workbook. That is the specific thing a reader experiences as
"an AI site".

| Was | Now |
|---|---|
| `Stated in: About this item & Product information — Features & Specs (chunks 4 & 7)` | `Read from the listing bullets on 2026-11-20` |
| `item weight unstated on listing (FLG-022)` | `the listing does not publish its weight` |
| `Product-intent confirmation record` | `Where this link actually goes` — the same five fields, in shopper language |
| `Best for` / `The catch` | `Buy it if` / `Skip it if` |
| No tags on cards | `Best for two cooks`, `Two baskets`, and a "Why we picked it" line per product |
| Zero flags cited on buyer pages | Every contradiction stated in words on the page, with a route to the full record |

Every published value is identical to before. Only the wording, and the amount of the project's
own machinery the reader is asked to look at, changed.

## What a buyer now gets that they did not before

1. **Cards that answer the question a shopper is actually asking.** Each card names the reason to
   pick it, the reason not to, and one paragraph on why this product is on the site at all.
2. **A "what comes with it" card** on every product page — box contents, care, warranty — quoted
   from the listing, with the listing's own contradictions left visible.
3. **A three-question shortlist** on `compare.html`: what you are shopping for, how many you cook
   for, how you cook, and how much counter depth you have. It scores only against specifications
   already published, and it filters by category before it scores, so an air-fryer question never
   returns a thermometer.
4. **A dated trust strip** above the fold on the homepage: what was checked, when, and why prices
   and star ratings are absent, stated as a reason rather than an apology.

## Findability: one site, with a stated reason to rank it

- `findability.txt` now publishes, at the site root: the canonical home, what the site is for,
  the editorial policy (authorship, review process, no hands-on testing, paid-link marking,
  corrections), the 24 reader-facing pages separately from the 12 project records, the sitemap,
  the feed, how to cite a page, and the known limits.
- `robots.txt` points to it. The sitemap still submits all 36 pages, because the site's own gate
  requires full coverage and a half-submitted site is worse than an honest one; the split lives
  in `findability.txt` instead, and `Q-22` puts the choice in front of the owner.

## Independent re-verification performed this session (T-22)

All five official listings were fetched live and re-read with no reuse of earlier notes.
33 field rows recorded in `data/verification-2026-11-20-live.json`, published in full on
`verification.html`.

| Product | Confirmed live this pass | Left marked unverified this pass |
|---|---|---|
| P-01 `B0CDY277D3` | 13.38×11.81×10.63 in, 200–450 °F, 120 V/1700 W, 1-yr, cETL, capacity 6 L vs 6 qt | item weight |
| P-02 `B09B7SB46R` | 16.9×15.8×14.8 in, 24 presets in title vs 25 in bullets, capacity 24.6 L vs 26 qt | weight (listing omits it), accessory count not re-counted |
| P-03 `B08DKYBTPH` | 12.75×13.5×10 in, 8 qt, 200–400 °F vs 450 °F Hi-Fry, 1000 W vs 1700 W, 4 presets, cETL, 1-yr | item weight |
| P-04 `B0DHZTCNR5` | ±0.5 °F, NIST/NSF as a listing field, 1 s, battery + calibration certificate included, wipe clean | model HT07, 572 °F upper rating |
| P-05 `B0DZFD6R9Z` | 50 h battery, 1000 °F, 3 probes + hub, Bluetooth/Wi-Fi, 2-yr vs 3-yr warranty | probe length |

Also re-read live: the USDA FSIS Safe Minimum Internal Temperature Chart (page states last
updated 2025-04-14) and the FTC Endorsement Guides FAQ. Both corroborate what the site already
cites (S22, S03).

**New findings, added as flags and published on Flagged for Review:** FLG-041 (a long
`Specification Met` list is a seller self-declaration, not tested certification), FLG-042 (P-03's
page points to a newer model than the one submitted), FLG-043 (buy-box offer state changes between
reads), FLG-044 (the five register values this pass did not reach, queued for next time).

**Not verified this session, and still not claimed:** short-link redirects, the Associates
agreement and program policy wording (login-gated), whether the tracking ID is issued, whether
`link.amazon` short links are permitted, the one-per-product Special Link test, Search Console,
and any hands-on performance.

## The decisions this leaves with the owner

| # | Decision | Why it is the one that matters | Where |
|---|---|---|---|
| 1 | Run the one-per-product Special Link test | Until a click is recorded in the tracking report, nothing about revenue is knowable | Q-04, FLG-004 |
| 2 | Verify Search Console and submit `sitemap.xml` | The only route to choosing the next guide from measured queries instead of instinct | Q-20, SG-29 |
| 3 | Read three rewritten pages and confirm nothing now reads as a test result | Rewording is the one change that can create a compliance problem | Q-21 |
| 4 | Decide whether the 12 project records stay in the sitemap | Dilution versus auditability; both are defensible | Q-22 |
| 5 | Decide whether to apply for Creators API access | The only compliant route to showing live price and product imagery | SG-13, SG-31 |

## Verification behind this summary

    python3 scripts/build_site.py        # 36 pages, idempotent
    python3 scripts/check_site.py        # 36 pages, 5 product records, 44 flags, 19 sources - ALL CHECKS PASS
    python3 -m unittest discover -s tests -p "test_*.py"     # 3 tests OK
    node tests/test_collector.js         # ALL JS COLLECTOR AND CLIENT TESTS PASS
    node --check assets/app.js           # syntax OK

The gate now also fails if a crawl-chunk citation or a bare flag ID appears on any of the 25
reader-facing pages, and if `findability.txt` omits a submitted page. The new rules were written
after the rewrite, and passing them is what makes the rewrite stay done.
