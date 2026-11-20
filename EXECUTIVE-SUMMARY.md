# Executive Summary — ShopNow Kitchen (Verified Update — Session arena/9f19fe6b-affil2)

Date 2026-11-20 · Tracking ID in use `shopnow047c-20` (issuance unverified, FLG-002)
Live site https://karagemop466-tech.github.io/Affil2/ · Full version with source links: `executive-summary.html`

## What this is
A static publication-style Amazon affiliate site covering five submitted products in two categories:
three air fryers and two meat thermometers across 31 generated HTML pages. Every specification is read
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

## Sources (18 official sources in `data/sources.json`)
- S01 Operating Agreement §5 — https://affiliate-program.amazon.com/help/operating/agreement
- S02 Program Policies (Commission Income §2(d)/(e)/(g), Participation §2(a)/(b), §5 ML restriction, §6(t)/(v)/(w)/(y), IP License §1, §2(e)/(h)/(i)/(k), §4 Agent Terms) — https://affiliate-program.amazon.com/help/operating/policies
- S03 FTC Endorsement Guides FAQ — https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- S04 Google, Qualify your outbound links — https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- S10–S14 the five `/dp/` Amazon product listings; S15–S19 the five supplied `link.amazon` short links
- S20 Amazon Creators API onboarding — https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api
- S21 PA-API 5 deprecation notice — https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation
- S22 & S23 USDA FSIS Safe Minimum Internal Temperature Chart and Food Thermometers calibration guide

## What deep verification fixed and surfaced on 2026-11-20
| Area / Flag | Previous state | Now |
|------|-----|-----|
| Deep spec tables (FLG-022) | Weights (P-01/P-03), P-02 temp/power/model, P-04 model/upper temp, P-05 model/probe length left blank; editorial prose contained unverified `26.5 lb` for P-02 | Verified P-01 `13.3 lb`, P-02 `4-00675-02X-VN` / `75–500 °F` / `1700 W`, P-03 `12.8 lb`, P-04 `HT07` / `572 °F` / `6.5 in`, P-05 `CQ60-3C-Z1-E` / `4.75 in`; removed unverified `26.5 lb` prose and kept P-02 weight/warranty blank |
| FLG-017 | P-03 wattage switched from `1700 W` to `1000 W` | Features & Specs states `1700 W` while About this item states `1000 W`; marked `conflict` and both printed |
| FLG-019 | P-05 warranty changed to `two-year assurance` | Live listing states `two-year assurance` in About this item vs `3 Year` in Item details (prior register `1-year`); marked `conflict` and both printed |
| FLG-012 | `B0c8moW59` blocked by checkpoint (0/4); `P-04.observed` was `null` | Follow-up fetch resolved `B0c8moW59 -> B0DHZTCNR5`; intermittent stability remains tracked under `FLG-011` |
| Client JS & tables | `assets/app.js` lacked search, mobile nav toggle, `exportEvents`, and `send()`; `sources.html` had a 5-header vs 4-cell table mismatch | Implemented working search, nav toggle, CSV `exportEvents`, configurable `send()` + self-hosted collectors (`analytics/server.js`, `functions/api/collect.js`), and fixed `sources.html` 4-column symmetry |
| Stale flag IDs & counts | `editorial.json` & `questions.html` cited outdated flag IDs (`FLG-014`/`015`/`016`/`018` old numbers; `Q-02 -> FLG-010`) | Remapped every flag reference accurately and added `check_site.py` enforcement |

## Eight active listing conflicts published to buyers
| Flag | Product | Contradiction |
|------|---------|---------------|
| FLG-008 | CHEF iQ Sense | 50 hours battery in About this item vs 70 hours in an earlier Product Description capture |
| FLG-009 | Emeril 26 QT | `4-00675-02X-VN` in live Item details vs `4-00675-02` in an earlier capture |
| FLG-017 | Chefman 8 Qt | `1700 W` in Features & Specs vs `1000 W` in About this item |
| FLG-018 | Chefman 8 Qt | `400 °F` max in About this item & spec field vs `450 °F Hi-Fry` in title |
| FLG-019 | CHEF iQ Sense | `two-year assurance` in About this item vs `3 Year` in Item details (prior register: 1-year) |
| FLG-021 | Emeril 26 QT | 24 presets in title, Configuration & Description vs 25 in About this item |
| FLG-031 | Emeril 26 QT | Six accessories in title & Included Components vs 7 in Configuration & Description |
| FLG-034 | Chefman 6 Qt | 6 quarts in title & bullets vs 6 liters in Measurements field |

## Not verified, and published as such
Intended ASIN per product (FLG-001) · whether the tracking ID is live (FLG-002) · whether the
short-link format is permitted for this placement (FLG-003) · the one-per-product Special Link test
(FLG-004) · P-02 item weight & written warranty terms (FLG-022) · NIST/NSF and cETL certification
beyond listing statements (FLG-035) · any hands-on experience (FLG-032) · a named author (FLG-033).

## Decisions that change the numbers
1. Complete the link test (SG-07, Q-04) — nothing about revenue can be reported until it passes.
2. Amazon Creators API access (SG-13, SG-17, Q-15) — the only compliant route to showing prices, product images, and automated catalog data (with ML training barred under Program Policies §5 / IP §1 & §2(e)).
3. Search Console verification (SG-10, SG-18, Q-16) — the only way to pick future guides from measured organic queries.
4. Self-hosted analytics hosting (SG-20, Q-08) — deploy `analytics/server.js` or `functions/api/collect.js` beyond static GitHub Pages.
5. A custom domain (SG-14, FLG-006, Q-05) — canonicals currently point at the Pages subpath.

## Honest position on revenue
Zero, and no forecast. No commission rate, click, session or order figure is presented because nothing
from an authorised first-party report exists yet. `campaign-ledger.html` is intentionally empty, with
its schema and provenance rule written down so the first real row can be added without redesigning
the page.

## How the site is kept honest
`scripts/build_site.py` generates all 31 HTML pages from `data/*.json`; nothing is hand-edited.
`scripts/check_site.py` fails the build if the disclosure is missing or below the fold, if any
`amazon.com` link lacks `rel="sponsored nofollow"`, if a price, star rating, or unverified `26.5 lb`
claim appears, if a link or asset is broken, if any SVG illustration is orphaned, if any table has
mismatched `<thead>`/`<tbody>` column counts, if a page is missing from the sitemap, if JSON-LD does
not parse, or if an undefined or unpublished flag exists. CI runs regeneration, drift detection,
`check_site.py`, Python unit tests (`tests/test_site.py`), and Node.js collector/client tests
(`tests/test_collector.js`).

## Suggestions & Open Questions added across sessions (`SG-17..SG-20`, `Q-15..Q-16`)
- `SG-17` / `platform.html`: AI affiliate platform blueprint and compliance matrix shipped; automated catalog ingestion remains blocked until Creators API acceptance (`S20`, `S21`, `FLG-029`, `Q-15`).
- `SG-18` / `Q-16`: Question-shaped article generation from Search Console queries (blocked until SG-10 verification).
- `SG-19`: Suggestions Review ranking & decision worksheet shipped on `suggestions.html`.
- `SG-20` / `measurement.html`: Zero-dependency `analytics/server.js`, Cloudflare Pages `functions/api/collect.js`, `data/events.json`, and `assets/app.js` `send()` shipped in repo; hosting outside GitHub Pages remains pending (`FLG-010`, `Q-08`).

## Verification log (2026-11-20, session arena/9f19fe6b-affil2)
- Synced branch cleanly with `origin/main` (`829398c`, preserving PR #17, PR #18, and PR #19).
- Verified all 5 `link.amazon/*` short links, deep chunks across all 5 `/dp/` product pages, and official docs (`S01`–`S04`, `S20`–`S23`) live on 2026-11-20.
- `python3 scripts/build_site.py` built all 31 pages idempotently.
- `python3 scripts/check_site.py` passed (`checked 31 pages, 5 product records, 35 flags, 18 sources — ALL CHECKS PASS`).
- `python3 -m unittest discover -s tests -p "test_*.py" -v` passed (3 tests OK).
- `node tests/test_collector.js` passed (collector server, Cloudflare Pages Function, and client JS DOM/search/nav/CSV/telemetry tests).
