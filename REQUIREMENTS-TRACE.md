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
| 1 | Landing page leads with products, not verification copy | Partial | `index.html`: H1 is a buying question ("One basket, two baskets, or an oven?"); the product section `#the-picks` follows. | — | Shop-first rebuild claimed by `59ada9df` (T-13..T-20, PR #28, DIRTY). |
| 2 | Category subpages | Done | `air-fryers.html`, `meat-thermometers.html`, `shop.html`. | — | — |
| 3 | Every dashboard surface reachable from the footer, under one navigation group | Done | Primary nav has one "Records" group. Footer nav links 18 record pages (`about`, `campaign-ledger`, `design-brief`, `disclosure`, `executive-summary`, `flagged`, `measurement`, `platform`, `questions`, `sources`, `suggestions`, `verification` and others). | — | — |
| 4 | Associates disclosure above the fold on every page, repeated in the footer | Done | `index.html`: disclosure at line 37, `<main>` at line 39, footer copy at line 231. The gate requires the first occurrence above `<main>` on every page. The sentence matches Operating Agreement §5 word for word (see section 4). | Operating Agreement §5: https://affiliate-program.amazon.com/help/operating/agreement · FTC FAQ: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | — |
| 5 | Every `amazon.com` link marked `rel="sponsored nofollow"` | Done | `scripts/check_site.py` (`sponsored` check, around line 114–117) fails the build if any `amazon.com` link lacks it. | Google, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | — |
| 6 | Every outbound product link carries the tracking ID `shopnow047c-20` | Done (format) · Blocked (activity) | All five product links in `index.html` carry `tag=shopnow047c-20`. Whether the ID is active is not confirmed (FLG-002). | — | Owner: Associates Central check (FLG-002). |

### 1b. Product-intent record and link validation

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 7 | Store the intended ASIN, official listing URL, confirmation date and source for each submitted link | Partial · Irregular | `data/products.json`: `listing` is set for P-01..P-05 (`https://www.amazon.com/dp/<ASIN>`); the confirmation date sits in `observed_status` as prose; each field has a `src`. The `asin` field is filled with the observed value (see I-1). | Listing URL form that carries the ASIN, e.g. https://www.amazon.com/dp/B0CDY277D3 (checked live 2026-11-20). The formal ASIN definition is not yet linked to an official page (I-7). | `36170d15` (T-17, PR #35, DIRTY) owns the identity fields. Request logged. |
| 8 | Keep observed redirect targets in a separate field; do not merge the two | Partial · Irregular | `observed` is separate from `submitted` and `listing`. But `asin` duplicates `observed` for all five products (I-1). | — | `36170d15`. |
| 9 | Submitted short links are recorded and not called invalid | Done | `executive-summary.html` and `flagged.html` (FLG-003) say the status is unresolved. The only two uses of "invalid" are negations. | Operating Agreement §1 defines Special Links (checked 2026-11-20). | — |
| 10 | One Special Link per product tested in the enrolled Associates workflow, with destination and tracking report confirmed | Blocked | Not performed. No test is recorded. Product pages publish tagged `/dp/` links, and the open flag is FLG-004 ("Special Links pending test"). SG-07 proposes the test. No Associates Central access in this sandbox. | Special Links definition: Operating Agreement §1, https://affiliate-program.amazon.com/help/operating/agreement | Owner. Needs Associates Central access. |

### 1c. Guides, cadence and measurement

| # | Requirement | Status | Evidence on `main` | Official source (checked) | Owner action / claim |
|---|---|---|---|---|---|
| 11 | Question-shaped guides from the four supplied working titles | Done | H1s match the brief verbatim: `guides/basket-vs-oven.html` ("Basket or oven-style air fryer: what should you compare?"), `guides/capacity-checklist.html` ("A no-hype checklist for comparing air fryer capacity"), `guides/cleanup-counter-space.html` ("How to assess cleanup and counter-space trade-offs"), `guides/multi-function-questions.html` ("Questions to ask before buying a multi-function kitchen appliance"). The brief calls these working titles; the site makes no popularity claim. | — | — |
| 12 | Each new guide added to the sitemap and the feed | Done | `sitemap.xml` has 11 guide entries; `feed.xml` has 11 items; `guides/` holds 11 files. | — | — |
| 13 | A publishing cadence is set | Proposed | Weekly cadence is SG-16 and Q-07. `design-brief.html` says "Weekly cadence chosen from queries: blocked on Search Console." It is not adopted. | — | Owner decision (SG-16). |
| 14 | Seasons | Partial · Irregular | `design-brief.html` seasonal calendar. Thanksgiving 2026-11-26 is confirmed by OPM. Black Friday 2026-11-27 is the computed day after and has no cited source (I-2). | OPM federal holidays, 2026 table: "Thursday, November 26 — Thanksgiving Day": https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | Owner: cite a source for Black Friday or label it as computed. |
| 15 | Topic clusters | Proposed | A 15-topic cluster plan, labelled as hypotheses, in `design-brief.html`. | — | Owner decision. |
| 16 | Five measured events defined | Done (schema) | `data/events.json`: `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank`. `assets/app.js` logs them to `localStorage`. | — | — |
| 17 | Privacy-preserving outbound-click counter | Done (local only) | `outbound_click` writes the product ID to `localStorage`. No cookies, no third-party requests. | — | — |
| 18 | Self-hosted analytics endpoint | Code present · not deployed | `analytics/server.js`, `analytics/server.py`, `functions/api/collect.js`. `assets/config.js`: `analyticsEndpoint: null`. | — | `bdedd85e` (PR #16, DIRTY). Hosting needs the owner (FLG-010, Q-08). |
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
| 26 | Clear list of open questions and missing information | Done | `questions.html`: 20 questions (Q-01..Q-20). | — | — |
| 27 | Flagged for Review page with sources | Done | `flagged.html`: 40 flags (FLG-001..FLG-040), each with a source. The gate checks that defined and published flags match. | — | — |
| 28 | Source register, each row with an official link | Partial · Irregular | `sources.html` and `data/sources.json`: 19 sources, all `https`. The gate does not check that each URL is on an official domain (I-4). | — | Owner: spot-check. |
| 29 | Every spec table row has a source link | Partial | The gate requires a source link on spec rows (`scripts/check_site.py`, around line 243). It does not check every table row on every page (I-3). | — | Gate extension requested (I-3). |
| 30 | Named author and byline | Blocked | `about.html` states that no named human author stands behind the copy yet (FLG-033). Nothing was invented. | FTC guidance on endorsements (S03). | Owner: real name and credentials. |
| 31 | Brand and imagery | Partial | Generated illustrative photos in `assets/photos/`, each captioned as illustrative. No Amazon imagery (FLG-007). | — | Owner: licensed imagery, if wanted. |
| 32 | Nav labels, RSS feed, Search Console, reader capture (SG-27..SG-30) | Partial | Nav labels: done. RSS: `feed.xml`, done. Search Console: no property verified (SG-29). Reader capture: `readerCaptureEndpoint: null` in `assets/config.js` (Q-09, SG-30). | — | Owner: Search Console property (SG-29); capture provider (SG-30). |
| 33 | Compliance gate runs in the publishing workflow | Done | `.github/workflows/pages.yml`, job "Verify site": regeneration drift check plus `scripts/check_site.py`. Run for `2de7bdd` completed `success` at 2026-11-20 06:23:34Z. | — | — |
| 34 | GitHub Pages live from `main` | Done | Pages API: status `built`, source `main /`. `pages build and deployment` for `2de7bdd` completed `success` at 06:23:33Z. Live: https://karagemop466-tech.github.io/Affil2/ | — | — |
| 35 | Parallel sessions coordinated on one board | Partial | `COORDINATION.md` is maintained. Open PRs #16, #28, #34, #35 and #41 report DIRTY (merge conflicts with `main`). | — | Final integration session, once all claims are done. |
| 36 | Line-by-line verification from official sources, links for manual review | Partial | Earlier sessions re-read the five listings (`58c6ca4a`, PR #39, merged). This session re-read Operating Agreement §5 and the OPM 2026 holiday table (section 4). Listing-level conflicts remain flagged (FLG-008, 017, 018, 021, 034, 038). | — | — |

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

## 3. Irregularities found in this pass

These do not block publication. Each is listed for review.

- **I-1 — intended and observed ASIN are the same value.** In `data/products.json`, `asin` equals `observed` for P-01 (`B0CDY277D3`), P-02 (`B09B7SB46R`), P-03 (`B08DKYBTPH`), P-04 (`B0DHZTCNR5`) and P-05 (`B0DZFD6R9Z`). FLG-001 says the intended field stays blank and the observed field stays separate. The brief says do not merge the two. Logged to `36170d15` on `COORDINATION.md`. Not edited here.
- **I-2 — Black Friday date has no source.** `design-brief.html` lists "Black Friday 2026-11-27". It is the day after Thanksgiving (2026-11-26, confirmed by OPM). Either cite a source or label it as computed.
- **I-3 — table-row sourcing is only partly enforced.** `check_site.py` checks a source link on spec rows. The brief asks for a source link on every table row. Requested as a gate extension, logged to `59ada9df` (T-19).
- **I-4 — official-domain check missing.** The gate checks that source URLs use `https`. It does not check that each URL is on an official domain. Logged to `59ada9df`.
- **I-5 — source date not recorded.** The Operating Agreement page reads "Updated: October 15, 2025" (fetched 2026-11-20). `data/sources.json` records the date checked but not the page's own date. Logged to `59ada9df`.
- **I-7 — formal ASIN definition not yet sourced.** The brief says Amazon's ASIN definition gives a checkable identifier. No official Amazon page with that definition was located in this pass. Third-party glossaries were not used as a source. Owner or next pass: find the official Amazon help page, or cite the listing's Product information table.
- **I-8 — stale flag numbers in COORDINATION.md.** Earlier entries cite "FLG-019 commission schedule", "FLG-028 Search Console" and "FLG-032 research data". In `data/flags.json` those numbers now mean: FLG-019 is the P-05 warranty record, FLG-028 is a missing source (S07), FLG-032 is "no hands-on testing". No flag covers Search Console or the commission schedule. Those items are tracked in SG-29 and the site copy instead. Logged for the integration session; not edited here.
- **I-6 — open PRs conflict with `main`.** PRs #16, #28, #34, #35 and #41 report DIRTY. Left to their owners and the final integration session.

## 4. Checked in this pass (2026-11-20)

| Item | Official page | Result |
|---|---|---|
| Associates disclosure wording, §5 | https://affiliate-program.amazon.com/help/operating/agreement | §5 reads: "As an Amazon Associate I earn from qualifying purchases." The site uses the same sentence verbatim (`index.html` line 37). |
| Thanksgiving 2026 date | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 2026 table: "Thursday, November 26 — Thanksgiving Day." Matches `design-brief.html`. |
| Black Friday 2026 date | — | Not checked against an official source (I-2). |
| Live site | https://karagemop466-tech.github.io/Affil2/ | Pages API `built`; deploy for `2de7bdd` succeeded. |
| Local gate | `python3 scripts/build_site.py`, `python3 scripts/check_site.py` | `checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS`. Build is idempotent. |
