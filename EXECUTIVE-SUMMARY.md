# Executive Summary — ShopNow Kitchen (Verified Update — Session arena/9f19fe6b-affil2)

Date 2026-11-20 · Tracking ID in use `shopnow047c-20` (issuance unverified, FLG-002)
Live site https://karagemop466-tech.github.io/Affil2/ · Full version with source links: `executive-summary.html`

## What this is
A static publication-style Amazon affiliate site covering five submitted products in two categories:
three air fryers and two meat thermometers across 38 generated HTML pages (including 13 buying guides). Every specification is read
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

## Sources (20 official sources in `data/sources.json`)
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
- `python3 -B scripts/build_site.py` built all 38 pages idempotently.
- `python3 -B scripts/check_site.py` passed (`checked 38 pages, 5 product records, 43 flags, 20 sources — ALL CHECKS PASS`).
- `python3 -B -m unittest discover -s tests -p "test_*.py" -v` passed (3 tests OK).
- `node tests/test_collector.js` passed (collector server, Cloudflare Pages Function, and client JS DOM/search/nav/CSV/telemetry tests).


## Shop-first polish pass (2026-11-20, session arena/93894704-affil2 · T-21)

What changed for a reader, and what the gate now refuses to publish:

- **Buyer-facing copy is no longer an audit.** Internal `FLG-` register codes were printed inside product
  card trade-offs, comparison cells, image captions, guide prose and the footer. The substance stays; the
  ticket number does not. Codes remain on `flagged.html`, `sources.html`, `verification.html`, the
  questions/suggestions registers and the product-intent record at the foot of each product page, which
  every card now links to ("why we say that"). `check_site.py` fails if a code reappears in the visible
  copy of the front page, shop, category, compare or guide pages.
- **Read times are measured, not asserted.** Guides previously claimed 4–7 minute reads over copy that
  runs 281–450 words. `guide_minutes()` now derives the figure from the guide's own word count (225 wpm,
  rounded up) at build time, and the gate re-derives it from each rendered page. Logged as FLG-041.
- **Pages are signed.** Every guide and product page carries a dated byline (The Kitchen Desk · verified
  against the official listing on 2026-11-20 · links to the authorship note). The byline is a role, not a
  person: Google's people-first guidance (new source **S25**) encourages accurate authorship and calls
  fabricated names, headshots and credentials deceptive, so a named editor of record stays an open item
  (FLG-033, Q-06) rather than a fiction.
- **Two new sourced guides.** `guides/thermometer-ice-test.html` walks USDA FSIS's own ice-water
  calibration test (stem ≥2 in, ≥30 s, should read 32 °F; "most food thermometers will give an accurate
  reading within 2 to 4 degrees F") and reads that baseline against the P-04 listing's ±0.5 °F and
  "calibration certificate" claims — recorded as FLG-043, still unverified, not restated as measured.
  `guides/read-an-air-fryer-listing.html` teaches title vs bullets vs the structured spec table using
  only contradictions already in the dated register. Both are in the sitemap, the feed and the on-site
  search index; neither makes a performance, popularity or volume claim.
- **The Decision Center now hands over the work.** Ticking proposals in `suggestions.html` assembles a
  copy-paste build prompt (chosen IDs, each one's what/why/cost/definition of done, the repo's standing
  constraints, and the unresolved owner questions). It is rendered server-side from the same JSON the
  browser uses, so `tests/test_collector.js` can and does assert the two agree. Five new proposals
  (SG-33…SG-38) record this pass with how to verify each one.
- **A markup leak found by reading the built pages, not the source.** Three guides escaped copy that had
  been authored with entities, so readers were shown the literal markup (`&mdash;`, a plusmn entity) where
  the sentence meant an em dash and ±0.5 °F. The generator now decodes named and numeric entities before
  escaping, every page rebuilt clean, and the gate fails on any visible entity sequence. Logged FLG-044.
- **Register state:** 44 flags (FLG-041/042/044 corrected, FLG-043 open), 20 sources (+S25), 13 guides,
  38 pages. Prices, ratings, review counts, sales ranks and commission figures remain absent by design
  (Program Policies §2(b), §6(t)); the analytics endpoint, Search Console verification, the one-per-product
  Special Link test, a custom domain and a named editor remain owner-gated and are published as such.
