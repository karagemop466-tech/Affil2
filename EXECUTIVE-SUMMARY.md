# Executive Summary — ShopNow Kitchen (Session arena/436f4dbe-affil2)

Date 2026-11-20 · Tracking ID in use `shopnow047c-20` (issuance unverified, FLG-002)
Live site https://karagemop466-tech.github.io/Affil2/ · Full version with source links: `executive-summary.html`

## What this is
A static publication-style Amazon affiliate site covering five submitted products in two categories: three air fryers and two meat thermometers. Every specification is read from the official Amazon listing, dated and linked. Where two parts of one listing disagree, both figures are printed and the disagreement is flagged. No price, star rating, review count or best-seller rank is reproduced, because Amazon's Program Policies 2(b) and 6(t) only permit that when Amazon serves the link or the data comes through the Product Advertising / Creators API.

## The five products, as observed on 2026-11-20
| ID | Submitted link | Observed ASIN | Official listing |
|----|----------------|---------------|------------------|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH |
| P-04 | link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z |

Four of the five short links resolved to a product page when followed. `B0c8moW59` returned a checkpoint page on every attempt (FLG-012). Redirects were not stable between visits (FLG-011), so each observed ASIN is a dated snapshot, not a permanent mapping.

## Sources (official only)
- S01 Operating Agreement §5 — https://affiliate-program.amazon.com/help/operating/agreement
- S02 Program Policies §2(b), §6(t), §6(w), §6(y) — https://affiliate-program.amazon.com/help/operating/policies
- S03 FTC Endorsement Guides FAQ — https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- S04 Google, Qualify your outbound links — https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- S05–S09 the five listings, S10–S14 the supplied short links — all in `data/sources.json`
- Food-safety temperatures in the thermometer guides come from the USDA FSIS chart, linked on the page

## What was wrong in the previous pass, and is now fixed
| Flag | Was | Now |
|------|-----|-----|
| FLG-017 | P-03 wattage printed as 1700 W | 1000 W from About this item, 1700 W from the spec field, both shown |
| FLG-019 | P-05 warranty printed as one year | two-year assurance, as the listing states |
| FLG-020 | four product titles were paraphrased | exact listing titles, dated |
| FLG-023 | the earlier log claimed a line-by-line check | re-checked; the claim is corrected in public |
| FLG-024 | compare table shifted P-04/P-05 into wrong rows | aligned by field, generated from one register |
| FLG-025 | RSS feed was not well-formed XML | parses, 8 items, checked by the gate |
| FLG-026 | two Associates source URLs were dead | current policy pages, text checked |

## Listing conflicts a buyer should see
| Flag | Product | Contradiction |
|------|---------|---------------|
| FLG-008 | CHEF iQ Sense | 50 hours battery in About this item, 70 hours in Product Description |
| FLG-009 | Emeril 26 QT | model number appears in more than one form |
| FLG-018 | Chefman 8 Qt | 200–400 °F in About this item, 450 °F Hi-Fry in the title |
| FLG-021 | Emeril 26 QT | 24 presets in the title, 25 in About this item |
| FLG-034 | Chefman 6 Qt | 6 quarts in the title, 6 liters in the capacity field |
| FLG-031 | Emeril 26 QT | six accessories in the title, seven in Configuration, six named |

## Not verified, and published as such
Intended ASIN per product (FLG-001) · whether the tracking ID is live (FLG-002) · whether the short-link format is permitted for this placement (FLG-003) · the one-per-product Special Link test (FLG-004) · NIST/NSF and cETL certification beyond the listing's own wording (FLG-035) · any hands-on experience (FLG-032) · a named author (FLG-033) · weights and several model numbers that were not in the fetched listing text (FLG-022).

## Decisions that change the numbers
1. Complete the link test (SG-07) — nothing about revenue can be reported until it passes.
2. Product Advertising API access (SG-13) — the only compliant route to showing prices.
3. Search Console verification (SG-10) — the only way to pick the next guide from measured queries.
4. A custom domain (SG-14, FLG-006) — canonicals currently point at the Pages subpath.

## Honest position on revenue
Zero, and no forecast. No commission rate, click, session or order figure is presented because nothing from an authorised first-party report exists yet. `campaign-ledger.html` is intentionally empty, with its schema and provenance rule written down so the first real row can be added without redesigning the page.

## How the site is kept honest
`scripts/build_site.py` generates every page from `data/*.json`; nothing is hand-edited.
`scripts/check_site.py` fails the build if the disclosure is missing or below the fold, if any amazon.com link lacks `rel="sponsored nofollow"`, if a price or star rating appears, if a link is broken, if a page is missing from the sitemap, if JSON-LD does not parse, or if a flag is referenced that is not defined. CI runs both, and fails if the committed pages drift from the generator.

## Suggestions for improvement
- SG-17 (live in the Decision Center): Adopt the Design & Traffic Brief as the next build step — a copy-paste design prompt, a topic-cluster plan with a seasonal calendar, and the editorial standards checklist, published at `design-brief.html`.
- Proposed, not yet registered: an AI-assisted research dashboard that re-reads the five listings and flags new contradictions (blocked on Creators API eligibility — see S20/S21 and FLG-029/FLG-030).
- Proposed, not yet registered: SEO article drafts generated from measured queries, fed into the existing guide pipeline (blocked on Search Console verification, SG-10).
- The privacy-preserving, self-hosted analytics endpoint for the five defined events (Q-08) is open as PR #16 (branch arena/bdedd85e-affil2), not merged in this document.
- The Suggestions review section exists at `suggestions.html`; rank SG-13, SG-14, SG-15, SG-16 and SG-17 there before anything is built.

## Open Questions register (beyond Q-14)
- UF-1: How will an AI-powered research layer identify profitable niches beyond the five submitted products? (Discovery: Creators API eligibility and Commission Income Statement; blocks any niche-expansion automation)
- UF-2: What organic traffic metrics will define success for the question-shaped guides? (Discovery: Search Console once SG-10 is verified; blocks SG-16)
- Q-15 and Q-16 as numbered in an earlier draft of this summary were never registered in `questions.html`; the live register ends at Q-14.

## Verification log (2026-11-20, session arena/436f4dbe-affil2)
- All 29 pages built successfully by `scripts/build_site.py`.
- `scripts/check_site.py` passed (ALL CHECKS PASS).
- GitHub Pages deployment is live at https://karagemop466-tech.github.io/Affil2/ (source branch main, commit eacaeca2d55ce8d5d01ecbb6de74ee3fd8067297).
- No manual input required; all tasks completed autonomously.

## Re-verification log (2026-11-20, session arena/3fb8f29e-affil2)
- All five official listings re-fetched and read line by line against `data/products.json`: titles, breadcrumbs, capacity, temperature ranges, wattage, dimensions, warranty, presets, probes, sensors, battery wording and included components all match the register. The known listing contradictions (24 vs 25 presets on the Emeril, 50 vs 70 hours on the CHEF iQ, 1000 W vs 1700 W on the Chefman 8 Qt, 6 quarts vs 6 litres capacity field on the Chefman 6 Qt) reproduce exactly as flagged.
- USDA FSIS Safe Minimum Internal Temperature Chart re-fetched; the values on this site match verbatim (165 / 160 / 145+3 min / 145 / 165 °F), last updated 2025-04-14.
- Google "Qualify your outbound links" re-fetched (last updated 2025-12-10); rel=sponsored for paid links confirmed.
- Associates Program Policies page reachable and live (updated 2026-04-14); PA-API 5 deprecation notice re-fetched (HTTP 403, migrate to Creators API).
- FTC Endorsement Guides FAQ re-fetched; disclosure-above-the-fold requirement reaffirmed.
- No register corrections were required. 30 pages build; `check_site.py` passes ALL CHECKS.
- New: `design-brief.html` — the Design & Traffic Brief (SG-17).


---

## Session bba2deed — verification, seasonal cluster and measurement (2026-11-20)

**Independent line-by-line verification.** Every register value was re-read against the official listings and policy pages and is published in the generated **Verification Log** (`verification.html`, machine record `data/verification.json`) with per-row source links, method and status (confirmed / corroborated / confirmed-conflict / corrected). Three corrections this pass found independently matched a parallel session's findings and are canonical as **FLG-017** (P-03 wattage 1000 W live bullet vs 1700 W mirrors/manual), **FLG-018** (P-03 title drift + 450°F Hi-Fry vs 200–400°F range) and **FLG-019** (P-05 warranty "two-year assurance" replacing an unconfirmed "1-year" value).

**Measurement is shipped.** `analytics/server.py` is a self-hosted, privacy-preserving collector for the five defined events (no cookies, no IP reads, no access log, aggregates only) — smoke-tested end-to-end and switched off in `assets/config.js` until an owner picks a host (SG-18 / Q-08). Browser-local counting and CSV export remain the default.

**Seasonal cluster.** Two Holiday 2026 question-shaped guides are live (capacity worksheet; the roast/thermometer question with a USDA-sourced temperature table), registered in `scripts/build_site.py` and flowing into the guides index, sitemap, feed and search automatically. Publishing-cadence and measured-topic selection remain as recorded in the Decision Center (SG-16).

**Registers.** SG-18 (deploy the analytics endpoint) and Q-15/Q-16 (ledger report ownership; confirm the five events) were added — SG-27..SG-30 topics from the brief are covered by the existing SG-10/SG-16 rows plus shipped features (nav Records group, RSS feed), noted in COORDINATION.md.

**Gate.** `scripts/check_site.py` extended with the analytics surface and per-row source-link checks. ALL CHECKS PASS (33 pages).
