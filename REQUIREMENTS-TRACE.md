# Requirements trace — ShopNow Kitchen

Task **T-21** · session `c449a2ad` · checked 2026-11-20 (UTC) against `main` at `2de7bdd`.

This file maps each requirement in the current brief to its status on `main`, the file that
shows it, the official source where one applies, and the owner action it still needs. It adds no
product facts. "Done" means the repository contains the item and `scripts/check_site.py` covers it.
It does not mean an outside service (Associates Central, Search Console, an analytics host) has
been configured. Those are marked Blocked.

Status key: **Done** · **Partial** · **Blocked** (needs owner account or access) · **Proposed**
(needs an owner decision) · **Not done by design** · **Irregular** (see section 3).

Open pull requests from other sessions are listed where they claim a row. Their file scopes were
not edited here.

## 1. Requirement trace

### 1a. Shop, navigation and disclosure

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 1 | Landing page leads with products, not verification copy | Done (main `7f67912`) | `index.html`: hero, then "Shop by category" (`section.dept`), then "The three we'd start with" (`#the-picks`). The spec strip ("How this site works") comes between them. The H1 is a buying question. | — | Front-page work from `59ada9df` (PR #28, DIRTY) may still conflict; `cb967199` (PR #41) landed a front-page change on main. |
| 2 | Category subpages | Done | `air-fryers.html`, `meat-thermometers.html`, `shop.html`. | — | — |
| 3 | Every dashboard surface reachable from the footer, under one navigation group | Done | Primary nav has one "Records" group. Footer nav links 18 record pages (`about`, `campaign-ledger`, `design-brief`, `disclosure`, `executive-summary`, `flagged`, `measurement`, `platform`, `questions`, `sources`, `suggestions`, `verification` and others). | — | — |
| 4 | Associates disclosure above the fold on every page, repeated in the footer | Done | `index.html`: disclosure at line 37, `<main>` at line 39, footer copy at line 231. The gate requires the first occurrence above `<main>` on every page. The sentence matches Operating Agreement §5 word for word (see section 4). | Operating Agreement §5: https://affiliate-program.amazon.com/help/operating/agreement · FTC FAQ: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | — |
| 5 | Every `amazon.com` link marked `rel="sponsored nofollow"` | Done | `scripts/check_site.py` (`sponsored` check, around line 114–117) fails the build if any `amazon.com` link lacks it. | Google, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | — |
| 6 | Every outbound product link carries the tracking ID `shopnow047c-20` | Done (format) · Blocked (activity) | All five product links in `index.html` carry `tag=shopnow047c-20`. Whether the ID is active is not confirmed (FLG-002). | — | Owner: Associates Central check (FLG-002). |

### 1b. Product-intent record and link validation

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 7 | Store the intended ASIN, official listing URL, confirmation date and source for each submitted link | Done | `data/products.json` gives every record `intended_asin` (blank, with `intended_status` explaining why), `observed`, `observed_status`, `observed_source`, `confirmed` (YYYY-MM-DD), `listing` and `listing_source`. The product page prints all of it in the intent table, with the date and both source ids. | Amazon's own definition — "a unique 10-character alphanumeric code assigned to every product listed in the Amazon store": https://sell.amazon.com/blog/what-is-an-asin (read 2026-11-20, page dated Jun 4, 2025). Registered as S27, which closes the search recorded as FLG-053. | None. The gate fails if `intended_asin` is ever filled, if it ever equals `observed`, or if a source id is missing from `sources.json`. |
| 8 | Keep observed redirect targets in a separate field; do not merge the two | Done | The ambiguous legacy `asin` key is gone; I-1 is closed. `observed` holds the confirmed redirect target, `intended_asin` holds the owner's intent (blank), and both generators build affiliate and plain URLs from `observed` only. | S27 | `tests/test_site.py::test_intent_and_observed_never_merge` fails if the legacy key returns. |
| 9 | Submitted short links are recorded and not called invalid | Done · Irregular (FLG-051) | `executive-summary.html` and `flagged.html` (FLG-003) say the status is unresolved. The only two uses of "invalid" are negations. T-31 re-check on 2026-11-20: five of five submitted links ended on the amazon.com home page in the fetch, which does not reproduce the earlier records (S15–S19). Recorded as an observation in `data/link-resolution-2026-11-20.json`, not as a finding that the links are invalid. | Operating Agreement §1 defines Special Links (checked 2026-11-20). | — |
| 10 | One Special Link per product tested in the enrolled Associates workflow, with destination and tracking report confirmed | Blocked | Not performed. No test is recorded. Product pages publish tagged `/dp/` links, and the open flag is FLG-004 ("Special Links pending test"). SG-07 proposes the test. No Associates Central access in this sandbox. | Special Links definition: Operating Agreement §1, https://affiliate-program.amazon.com/help/operating/agreement | Owner. Needs Associates Central access. |

### 1c. Guides, cadence and measurement

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 11 | Question-shaped guides from the four supplied working titles | Done | H1s match the brief verbatim: `guides/basket-vs-oven.html` ("Basket or oven-style air fryer: what should you compare?"), `guides/capacity-checklist.html` ("A no-hype checklist for comparing air fryer capacity"), `guides/cleanup-counter-space.html` ("How to assess cleanup and counter-space trade-offs"), `guides/multi-function-questions.html` ("Questions to ask before buying a multi-function kitchen appliance"). The brief calls these working titles; the site makes no popularity claim. | — | — |
| 12 | Each new guide added to the sitemap and the feed | Done | `sitemap.xml` has 11 guide entries; `feed.xml` has 11 items; `guides/` holds 11 files. | — | — |
| 13 | A publishing cadence is set | Done | `guides.html` publishes the policy: one guide a week, a ship-only-if-it-earns-it rule, and the five conditions a guide must meet (one question, dated sources, a verdict, listed in sitemap + feed in the same build, a sponsored-marked exit). The published-guide table is generated from the guide register, so a claimed cadence cannot drift from the real one. | — | Owner: confirm the rate holds after one measured cycle (Q-25). |
| 14 | Seasons | Done | `design-brief.html` seasonal calendar keeps the T-31 date corrections and now labels every row by kind: three `official holiday` rows link to OPM, four `retail moment` / `cultural marker` rows say plainly that they have no official publisher. I-2 is closed. | OPM federal holidays, 2026 and 2027 tables (S26): https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | Owner: register a commercial calendar publisher only if retail dates must be cited (Q-27). |
| 15 | Topic clusters | Done | The 15-topic plan in `design-brief.html` now names, on every row, the listing or published chart the topic would be built from, and links a live guide to its own page. Titles stay labelled as working hypotheses, not popularity claims. | Listing pages and the USDA FSIS chart (S22) as cited per row. | Owner: Search Console data decides which proposed title is written first (Q-20). |
| 16 | Five measured events defined | Done (schema) | `data/events.json`: `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank`. `assets/app.js` logs them to `localStorage`. | — | — |
| 17 | Privacy-preserving outbound-click counter | Done (local only) | `outbound_click` writes the product ID to `localStorage`. No cookies, no third-party requests. | — | — |
| 18 | Self-hosted analytics endpoint | Code present · switch now wired, host still missing | `analytics/server.js`, `analytics/server.py`, `functions/api/collect.js`. `assets/config.js`: `analyticsEndpoint: null`. The client now actually reads that key: `assets/app.js` resolves the endpoint from `window.SN_COLLECT_ENDPOINT`, then the `sn-collect-endpoint` meta tag, then `SITE_CONFIG.analyticsEndpoint`, and every page loads `assets/config.js` before `app.js` (gate-enforced). Before this pass the config file was never loaded by any page, so the documented switch was dead code. | — | Owner: host the collector and set the URL (FLG-010, Q-08). |
| 19 | Real analytics turned on, so the next topic comes from measured queries | Blocked | Nothing is transmitted; the endpoint is null. | — | Owner hosting (FLG-010). |
| 20 | Campaign ledger starts empty, with a defined schema and a provenance rule | Done | `data/campaign-ledger.json` has `rows: []`. `campaign-ledger.html` columns: Date (UTC), Source report, Channel, Eligible sessions, Outbound clicks, Reported orders, Provenance note. | — | — |
| 21 | No conversion score and no revenue forecast | Done | Excluded by rule. `executive-summary.html` and `campaign-ledger.html` say so. | Operating Agreement §4: no representation about traffic or commission income (checked live 2026-11-20): https://affiliate-program.amazon.com/help/operating/agreement | — |

### 1d. Research, pricing and competition

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 22 | Trend, price, review, competition and commission analysis | Not done by design | Prices, star ratings and review counts are excluded (FLG-005; Program Policies §2(b), §6(t), as recorded in the S02 register; not re-checked in this pass). Site copy says commission schedules need sign-in to Associates Central, so the schedule is not reproduced. No research data was supplied (SG-26 requires first-party reports). | Creators API registration (final acceptance and qualifying sales): https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api · PA-API 5 deprecation: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation | Owner: first-party reports. Nothing is estimated. |
| 23 | Platform architecture, including the compliance gate on automation | Done (document) | `platform.html` (SG-31): seven modules, with Creators API and ML-use limits. | Same as row 22; Program Policies §5 (S02 register; not re-checked in this pass). | Owner decision before any automation. |

### 1e. Records, verification and publication

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 24 | Executive summary | Done | `executive-summary.html` and `EXECUTIVE-SUMMARY.md`. | — | Keep counts in sync. |
| 25 | Suggestions section to review and rank before any change | Done | `suggestions.html`: 32 proposals (SG-01..SG-32). | — | — |
| 26 | Clear list of open questions and missing information | Done | `questions.html`: 27 questions (Q-01..Q-27). Q-24..Q-27 were added this session; each row states what is known, what is missing, how to discover it, what it blocks, who can answer and a status. | — | The answers need owner access; the register itself is complete. |
| 27 | Flagged for Review page with sources | Done | `flagged.html`: 58 published flags (FLG-001..FLG-058), each with at least one source id and an owner status. FLG-050 and FLG-053 are now `corrected`; FLG-054..FLG-058 were opened or resolved this session. | — | Owner reviews the `needs review` rows. |
| 28 | Source register, each row with an official link | Done | `sources.html` and `data/sources.json`: 22 sources, all `https`, every one on the official-host allowlist. T-31 added the allowlist; this session made the check two-way (every external link on every page must be on it) and added a reason to each allowlist entry. Each source carries its read date, and the three policy pages carry their own published revision date. | Operating Agreement (Updated: October 15, 2025), Program Policies (Updated: April 14, 2026), Google outbound links (Last updated 2025-12-10 UTC) | Owner: re-read the three policy pages before each cycle (FLG-058). |
| 29 | Every table row has a source link | Done | The gate walks every table body on every page. A row passes if it carries a hyperlink, a source button or a register citation (S01, FLG-017). A table with unsourced rows fails unless it declares itself a first-party record with `data-own` **and** its caption says what it records and where the record lives. Comparison, cluster, corrections, intent, specification and seasonal rows all gained explicit source controls; I-3 is closed. | — | — |
| 30 | Named author and byline | Blocked | `about.html` states that no named human author stands behind the copy yet (FLG-033). Nothing was invented. | FTC guidance on endorsements (S03). | Owner: real name and credentials. |
| 31 | Brand and imagery | Partial | Generated illustrative photos in `assets/photos/`, each captioned as illustrative. No Amazon imagery (FLG-007). | — | Owner: licensed imagery, if wanted. |
| 32 | Nav labels, RSS feed, Search Console, reader capture (SG-27..SG-30) | Partial | Nav labels: done. RSS: `feed.xml` plus a named "Follow new guides" block on `guides.html` that explains the feed and says why no email capture exists. Search Console: still no verified property (SG-29). Reader capture: no provider, and the site says so rather than shipping an empty form (`readerCaptureEndpoint: null`, Q-09). | — | Owner: Search Console property (SG-29). Email capture only with a stated privacy policy (Q-09). |
| 33 | Compliance gate runs in the publishing workflow | Done | `.github/workflows/pages.yml`, job "Verify site": regeneration drift check plus `scripts/check_site.py`. Run for `2de7bdd` completed `success` at 2026-11-20 06:23:34Z. | — | — |
| 34 | GitHub Pages live from `main` | Done | Pages API: status `built`, source `main /`. `pages build and deployment` for `2de7bdd` completed `success` at 06:23:33Z. Live: https://karagemop466-tech.github.io/Affil2/ | — | — |
| 35 | Parallel sessions coordinated on one board | Done | `COORDINATION.md` carries this session's claim and completion record with its file scope, committed and pushed before work started. On rebase, `main` had already used task IDs T-27, T-30 and T-31, flag IDs FLG-051-053 and source id S25 for other sessions' work, so this session's tasks are recorded as T-32..T-37, its findings as FLG-054..FLG-058, and its ASIN definition as S27 rather than overwriting any of those rows. No other session's work was discarded at any merge point. | — | — |
| 36 | Line-by-line verification from official sources, links for manual review | Done | T-31 re-read the five `/dp/` listings and the policy pages (sections 4-5). This session re-read all five listings again at field level and every policy page, and recorded it in `data/verification-independent-2026-11-20.json` — value as printed, where it was read, and whether the pass actually reached it. FLG-050's five previously unconfirmed values were all re-read. Listing-level contradictions stay published (FLG-008, 017, 018, 021, FLG-055). | Five listing URLs in section 6; S01, S02, S03, S04, S26, S27. | — |

## 2. Owner-only items

These cannot be finished from the sandbox. Each one needs an account, a hosting decision or a
person.

- **Associates Central:** Special Link test (FLG-004, SG-07); tracking-ID activity (FLG-002); short-link compliance (FLG-003); intended ASINs (FLG-001); commission schedule (not reproduced; no dedicated flag).
- **Analytics hosting:** deploy one collector and set `analyticsEndpoint` (FLG-010, Q-08).
- **Search Console:** verify a property (SG-29).
- **Author:** supply a real name and credentials, or keep the site unsigned (FLG-033).
- **Reader capture:** choose an email provider (Q-09, SG-30).
- **Measured data:** first-party reports for the campaign ledger (SG-26).
- **Decisions:** publishing cadence (SG-16, Q-07); topic clusters (section 1c, row 15).

## 3. Irregularities: current state

Each item the earlier passes raised is now closed, or carries the flag that tracks it. Nothing here
blocks publication; all of it is published on `flagged.html` with its sources.

| ID | Raised | State now | Evidence |
|---|---|---|---|
| I-1 | `asin` duplicated `observed`, merging the two fields | **Closed.** The legacy key is gone. | `data/products.json`; gate rule; `test_intent_and_observed_never_merge` |
| I-2 | Black Friday had no source | **Closed.** Every seasonal row now states its kind and its source. Official holidays link to OPM; retail moments say they have no official publisher. | `design-brief.html`; S26; Q-27 |
| I-3 | Table-row sourcing only partly enforced | **Closed.** Every table body is walked; exemptions must declare themselves in the markup and explain themselves in the caption. | `scripts/check_site.py` T-34 rules |
| I-4 | No official-domain check | **Closed.** Any host not on the allowlist fails the build; the check now runs against every external link on every page, not just the register. | `scripts/check_site.py`; `OFFICIAL_SOURCE_HOSTS` |
| I-5 | Source page revision date not recorded | **Closed.** `page_date` is recorded for every source that publishes one. | `data/sources.json`; FLG-058 |
| I-7 | No official ASIN definition | **Closed.** Amazon's own definition was located and registered as S27, and is cited wherever the intended-ASIN blank is explained. | https://sell.amazon.com/blog/what-is-an-asin |
| I-6 / I-8 | Open PRs conflicting; stale flag numbers quoted | **Superseded.** The PR set quoted by T-21 was resolved when its successors merged. This session's flag IDs continue from FLG-054, after `main`'s FLG-053. | `COORDINATION.md` |

New items opened or resolved this session, all published on `flagged.html`:

- **FLG-054 — the supplied tokens are 9 characters, not 10-character ASINs.** Anchored to S27.
- **FLG-055 — P-05 is a variation family.** The published specs belong to the 3-probe variant.
- **FLG-056 — provenance cites a page section, never a chunk.** Chunk indices were removed from the register.
- **FLG-057 — three listings print a second, vaguer warranty sentence** in the Warranty & Support block.
- **FLG-058 — the policy pages carry their own revision dates**, now recorded beside the date they were read.

## 4. Checked in this pass (2026-11-20)

| Item | Official page | Result |
|---|---|---|
| Associates disclosure wording, §5 | https://affiliate-program.amazon.com/help/operating/agreement | §5 reads: "As an Amazon Associate I earn from qualifying purchases." The site uses the same sentence verbatim (`index.html` line 37). |
| Thanksgiving 2026 date | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 2026 table: "Thursday, November 26 — Thanksgiving Day." Matches `design-brief.html`. |
| Black Friday 2026 date | — | Not checked against an official source (I-2). |
| Live site | https://karagemop466-tech.github.io/Affil2/ | Pages API `built`; deploy for `2de7bdd` succeeded. |
| Local gate | `python3 scripts/build_site.py`, `python3 scripts/check_site.py` | `checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS` (2026-11-20 earlier pass). Build is idempotent. |

## 5. T-31 pass (session `7481731c`, 2026-11-20 UTC)

What was re-read, and where each item is recorded. Every row cites the official page or the record file.

| Item | Official page or record | Result |
|---|---|---|
| Five `/dp/` listings (ASIN and product title) | https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z | Each URL resolves to a product page whose title contains the register title. Recorded in `data/link-resolution-2026-11-20.json` (rows S10–S14). Prices and ratings were seen and deliberately not recorded. |
| Five submitted short links | https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV · https://link.amazon/B0c8moW59 · https://link.amazon/B0f3GKalj | Final URL was the amazon.com home page on every attempt (P-01 and P-04 twice). Does not reproduce the earlier records. FLG-051. Not called invalid. |
| OPM federal holidays | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 2026: Thursday, November 26, Thanksgiving Day. 2027: Friday, January 01, New Year's Day. S26. |
| Associates Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | "Updated: October 15, 2025". §1 defines Special Links. S01. |
| Seller Central, add one product (G1471) | https://sellercentral.amazon.com/help/hub/reference/external/G1471 | Lists UPC, EAN, ISBN or ASIN as accepted identifiers. Does not define ASIN. S25. FLG-053. |

Gate additions (all fail the build when broken, checked with a deliberately bad copy): official-host allowlist for sources (I-4); link-resolution record consistency (submitted link matches the register, listing titles contain the register title, no price, a home-page result cannot be marked as reproduced).

## 6. Independent live pass (session `c6fa1006`, 2026-11-20 UTC)

A second field-level read of all five listings, plus every policy source, recorded in
`data/verification-independent-2026-11-20.json`. Each field records the value as the page printed it,
the section it was read from, and whether this pass actually reached it. A field this pass did not
reach says so rather than copying the earlier answer.

| Item | Official page | Result |
|---|---|---|
| P-01 listing | https://www.amazon.com/dp/B0CDY277D3 | 1700 W, 120 V, 93 °C/450 °F, 6 L vs 6 qt, 13.38 × 11.81 × 10.63 in, 13.3 lb. Capacity and warranty self-conflict; both printed. |
| P-02 listing | https://www.amazon.com/dp/B09B7SB46R | 24.6 L vs a "26-quart" bullet, "25 COOKING PRE-SETS" vs "24 One-Touch Preset" in the title, 16.9 × 15.8 × 14.8 in. |
| P-03 listing | https://www.amazon.com/dp/B08DKYBTPH | 1700 W in Features & Specs vs 1000 W in a bullet; 400 °F maximum vs the 450 °F Hi-Fry title; 12.8 lb; `RJ38-SQSS-8T`; "1-Year Limited Warranty". |
| P-04 listing | https://www.amazon.com/dp/B0DHZTCNR5 | Model `HT07` in all three model fields; upper range 572 °F; 6.5 in; NIST/NSF listed as a seller spec claim; no warranty duration printed. |
| P-05 listing | https://www.amazon.com/dp/B0DZFD6R9Z | Three probes plus hub, five sensors, 1000 °F, 4.75 in, `CQ60-3C-Z1-E`, "3 Year" in Item details vs a "two-year assurance" bullet. |
| Associates disclosure wording | https://affiliate-program.amazon.com/help/operating/agreement | §5: "As an Amazon Associate I earn from qualifying purchases." The site uses that sentence verbatim. Page reads "Updated: October 15, 2025". |
| Special Links, prices, claims | https://affiliate-program.amazon.com/help/operating/policies | §2(a)/(b): Special Links must carry the Associates ID; prices and availability only when Amazon serves them or via Creators API / PA API. No price or rating appears here. Page reads "Updated: April 14, 2026". |
| `rel="sponsored"` | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Advertisements and paid placements should carry `sponsored`. Every product link does. Page reads "Last updated 2025-12-10 UTC". |
| FTC material connection | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Affiliate compensation is a material connection and must be disclosed clearly and conspicuously. The strip sits under the masthead on every page. |
| ASIN definition | https://sell.amazon.com/blog/what-is-an-asin | "A unique 10-character alphanumeric code assigned to every product listed in the Amazon store." Registered as S27; closes I-7 / FLG-053. |
| US federal holidays | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 2026: Nov 26 Thanksgiving, Dec 25 Christmas. 2027: Jan 1 New Year's Day. |
| Local gate | `python3 scripts/build_site.py` then `python3 scripts/check_site.py` | `checked 36 pages, 5 product records, 58 flags, 22 sources — ALL CHECKS PASS`. Build is idempotent. |
| Tests | `python3 -m unittest discover -s tests -p "test_*.py"` and `node tests/test_collector.js` | 7 Python tests pass; all JS collector and client tests pass. |

Tooling defects found and fixed while doing this pass, each of which had been weakening verification:

1. The gate printed its verdict **before** its last two rule blocks, so rules added after the
   report could never fail the build. Moving the report to the end surfaced five real failures.
2. The findability check compared an absolute path against a relative URL, so it failed on every page.
3. `src_ids` was used before definition — a latent `NameError`.
4. `assets/config.js` was loaded by no page, so `analyticsEndpoint` and `readerCaptureEndpoint` were
   documentation rather than switches (now loaded on every page, before `app.js`, gate-enforced).
5. Four guide strings carried HTML entities through `esc()`, printing "&mdash;" literally. A gate rule
   now fails on any double-escaped named entity.

## 7. What this trace does not claim

It does not claim the site will rank, will earn, or has been reviewed by a human editor. It does not
claim any product was tested. It does not claim the Associates account is active, that the supplied
short links are compliant, or that a Special Link test has passed — those are owner-only items in
section 2, and they are published on the site rather than hidden.
