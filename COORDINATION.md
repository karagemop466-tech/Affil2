# COORDINATION — Affil2 shared task board

Session ID (this turn): `6e40cecc`  Branch: `arena/6e40cecc-affil2`  Base: `e1b6750e92adaae69e95872700db578f499870ca` (main)
Prior session: `530c2e6c` (branch `arena/530c2e6c-affil2`, merged into main at `e1b6750e`). Started: 2026-11-20 (UTC)  Tracking ID supplied: `shopnow047c-20` (UNVERIFIED — see FLG-002)

> All task scopes were completed by `530c2e6c` and merged to main. This session (`6e40cecc`) took over the stale T-09 claim (>60 minutes old, no new commits) per the handoff rule and edits only files in its own scope: feed.xml fix and COORDINATION.md integration record. No file owned by another session was edited.

## Task board

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-01 | Repo audit + COORDINATION claim | done | 530c2e6c | COORDINATION.md |
| T-02 | Product-intent register + line-by-line verification vs official Amazon listings | done | 530c2e6c | data/products.json, data/sources.json, data/flags.json, products/*.html |
| T-03 | Compliance gate (disclosure, sponsored, no-price, no-ratings) + check script | done | 530c2e6c | scripts/check_site.py, disclosure.html, assets/* |
| T-04 | Publication front page + category pages + product pages | done | 530c2e6c | index.html, air-fryers.html, meat-thermometers.html, products/*.html |
| T-05 | Question-shaped guides (4 supplied hypotheses + 2 thermometer guides) | done | 530c2e6c | guides/*.html |
| T-06 | Suggestions / Direction section + Open Questions register + Executive Summary | done | 530c2e6c | suggestions.html, questions.html, executive-summary.html, EXECUTIVE-SUMMARY.md |
| T-07 | SEO/findability (sitemap, robots, RSS, JSON-LD, search) + click/analytics layer | done | 530c2e6c | sitemap.xml, robots.txt, feed.xml, assets/app.js |
| T-08 | Flagged for Review page + campaign ledger (empty, provenance) | done | 530c2e6c | flagged.html, campaign-ledger.html, data/campaign-ledger.json |
| T-09 | Final integration: build check, broken-link check, GitHub Pages, PR + merge | done | 6e40cecc | feed.xml, COORDINATION.md |
| T-10 | Rebuild product data from verified listings; add scripts/build_content.py (generated tables); fix compare column shift; remove unverified 'Verified' labels; fix S01/S02 URLs; extend check_site.py to catch stale values; re-check P-03 specs; reconcile flags (new IDs FLG-017+) | done | 937876a6 | data/products.json, data/sources.json, data/flags.json (appends only), scripts/build_content.py, scripts/check_site.py, generated HTML (products/*, compare, index, category, guides, sources, flagged, executive-summary), EXECUTIVE-SUMMARY.md, feed.xml |
| T-11 | Publication styling + decision-support improvements | done | 4bbf49bb | assets/style.css, assets/illustrations/*.svg, suggestions.html, questions.html, search.html, COORDINATION.md |
| T-12 | Final integrate original illustrations in generated product cards | done | 4bbf49bb | scripts/build_content.py, generated product-card pages (index, categories, guides), compare.html, COORDINATION.md |
| T-23 | Newsroom voice pass: remove internal audit tokens (chunk numbers, flag IDs, intent-record jargon) from buyer-facing pages while keeping every fact and source; add reader-native provenance blocks | done | 0acc86ad | scripts/build_site.py, scripts/check_site.py, data/editorial.json, generated pages |
| T-24 | Findability file: machine-readable site profile at /findability.txt plus verification of robots/sitemap/feed | done | 0acc86ad | findability.txt, robots.txt, sitemap.xml, feed.xml, scripts/build_site.py |
| T-25 | Live re-verification of the five listings' published specs + policy sources; dated record | done | 0acc86ad | data/verification-2026-11-20-live.json, data/sources.json, COORDINATION.md |
| T-27 | Reconcile open PRs (#47, #51, #53) and record dispositions | done | a150712 | COORDINATION.md only |
| T-30 | Final integration: documentation reconciliation, official-source pass, gates, PR and Pages verification | in progress | 57fc3be0 | COORDINATION.md, README.md, EXECUTIVE-SUMMARY.md, data/verification-2026-11-20-pass3.json |

> **Session `57fc3be0` claim (2026-11-20).** Branch `arena/57fc3be0-affil2`, base `4ddede5` (main).
> This session takes the **final-integration** role described in the brief: it re-verifies the combined
> data line by line against official sources, reconciles the open PRs left by earlier sessions, makes
> the published counts self-generating so they cannot drift, confirms the site builds with no broken
> links, and publishes to GitHub Pages.
> **Scope claimed:** `COORDINATION.md`, `README.md`, `EXECUTIVE-SUMMARY.md`,
> `data/verification-2026-11-20-pass3.json` (new), and the verification section of
> `scripts/build_site.py` + `scripts/check_site.py`.
> **Scope NOT claimed (not edited by this session):** `data/products.json`, `data/sources.json`,
> `data/editorial.json`, `data/events.json`, `analytics/`, `functions/`, `assets/app.js`,
> `assets/style.css` — shared records owned by other sessions. Requests against them are logged here.
> Shared outputs (data tables, index, navigation) are changed by this integration session **only
> after** the other tasks above are done, per the brief.
> Live-source note: `curl` cannot reach `amazon.com` / `ftc.gov` / `developers.google.com` /
> `affiliate-program.amazon.com` from this sandbox (TLS blocked on every request), but the
> `fetch_page` tool **can**. Verification therefore uses `fetch_page` against the official URLs.

Status key: unclaimed / in progress / done / needs review (= published on Flagged for Review, does not block).

## Verification log (2026-11-20, official sources only)

| Submitted link | Observed destination (separate field) | Official listing checked | Result |
|---|---|---|---|
| link.amazon/B04G1MEwY | B0CDY277D3 — CHEFMAN 6 Qt Dual Basket Air Fryer Oven (RJ38-SQPF-3TDB-2W) | https://www.amazon.com/dp/B0CDY277D3 | Title/model/specs match register; price/rating left blank per Program Policies §2(b) |
| link.amazon/B02NbDxp3 | B09B7SB46R — Emeril Lagasse 26 QT French Door Air Fryer Toaster Oven | https://www.amazon.com/dp/B09B7SB46R | Match; preset-count + model-number conflicts flagged (FLG-009; canonical numbering in data/flags.json) |
| link.amazon/B00hJ57DV | B08DKYBTPH — Chefman TurboFry Touch XL 8-Qt (RJ38-SQSS-8T) | https://www.amazon.com/dp/B08DKYBTPH | Match |
| link.amazon/B0c8moW59 | B0DHZTCNR5 — ThermoMaven Professional Digital Meat Thermometer, 1 Sec (HT07) | https://www.amazon.com/dp/B0DHZTCNR5 | Match |
| link.amazon/B0f3GKalj | B0DZFD6R9Z — CHEF iQ Sense [2025] Smart Wireless Meat Thermometer, Gen3 (CQ60-3C-Z1-E) | https://www.amazon.com/dp/B0DZFD6R9Z | Match; battery 50h vs 70h conflict flagged (FLG-008; canonical numbering in data/flags.json) |

Program sources: Amazon Associates Operating Agreement + Program Policies (affiliate-program.amazon.com), FTC Endorsement Guides FAQ (ftc.gov), Google "Qualify outbound links" (developers.google.com). Full register: `sources.html` / `data/sources.json`.

## Irregularities (do not block merge; all on flagged.html)
FLG-001 Intended ASINs unconfirmed by owner — intended field left blank, observed field separate.
FLG-002 Tracking ID shopnow047c-20 shape matches published pattern but issuance/activity cannot be confirmed publicly.
FLG-003 Short-link (link.amazon) compliance status unresolved — do NOT claim invalid.
FLG-004 Special Links not yet tested in enrolled Associates workflow — PENDING TEST, one per product.
FLG-005 No prices/ratings/BSR/commission shown — unverified fields blank per §2(b).
FLG-006 No custom domain / canonical host chosen — placeholder canonical flagged.
FLG-007 No product photography licensed — no Amazon images used.
FLG-008 CHEF iQ battery conflict 50h vs 70h on same listing.
FLG-009 Emeril preset count 24 vs 25 + model number variants on same listing.
FLG-010 Analytics is local-only until a self-hosted endpoint is deployed (Q-08).

## Verification log additions (2026-11-20, session 6e40cecc, official sources re-fetched)
| Item | Official source checked | Result |
|------|------------------------|--------|
| P-01 B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Title matches register: "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff..."; breadcrumb Home & Kitchen > ... > Air Fryers |
| P-05 B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Title matches register: "CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | ... Gen3"; breadcrumb ... > Meat Thermometers |
| S03 FTC Endorsement Guides FAQ | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Disclosure must be clear and conspicuous; connection to marketer must be disclosed |
| S04 Google qualify outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | rel="sponsored" for paid/affiliate links; multiple values allowed |
| feed.xml | W3C-expat well-formedness check | Fixed `<language>en-us>` → `<language>en-us</language>`, now valid |
| check_site.py | 25 pages | ALL CHECKS PASS |

## Handoff / conflict log

- 2026-11-20 505e685a (current session, branch arena/505e685a-affil2, base 4ddede54 = main): claimed T-28 and T-29. Added scripts/research_engine.py (product research from first-party events) and scripts/campaign_optimizer.py (campaign optimization from first-party clicks). Verified: python3 scripts/build_site.py builds 36 pages, python3 scripts/check_site.py ALL CHECKS PASS (36 pages, 5 product records, 50 flags, 19 sources), Python and JS test suites pass. GitHub Pages already live at https://karagemop466-tech.github.io/Affil2/ (status: built, source=main, https enforced). No conflicts — edits are limited to new files in own scope; no shared records modified.

## Handoff / conflict log (original)
- 2026-11-20 530c2e6c: claimed all tasks, repo empty, no conflicts; all tasks merged to main at e1b6750e.
- 2026-11-20 6e40cecc: took over stale T-09 claim (>60 min old, no new commits); feed.xml language tag fixed; re-verified P-01/P-05 vs official Amazon listings; re-fetched S03/S04; check_site 25 pages ALL CHECKS PASS.
- PR link + merge result: (to be recorded at T-09 completion)
- 2026-11-20 937876a6: claimed T-10 (see task board). Rebase onto main 373d1c2 conflicted in data/flags.json and flagged.html: both sessions used FLG-011..FLG-016 for different findings. Resolution: main's FLG-001..FLG-016 kept unchanged; this session's new findings appended as FLG-017..FLG-028; references remapped. No work from 990af5de or 6e40cecc discarded.

## T-09 completion (2026-11-20, session 6e40cecc)
- PR: https://github.com/karagemop466-tech/Affil2/pull/4 — merged via `gh pr merge 4 --merge`, merge commit 59181b84827c13e7e752de492875655f49aa5c49, state MERGED
- Merge brought session 990af5de's PR #3 (re-verification addendum, FLG-011..FLG-016, data/reverification-2026-11-20.json) onto main ahead of this PR; no main work was discarded. Parallel duplicate site from 990af5de was withdrawn by that session — not merged.
- GitHub Pages: deploy workflow for 59181b8 concluded success (run 44679837573). Live: https://karagemop466-tech.github.io/Affil2/ (source = main, https enforced)
- Final gate: scripts/check_site.py ALL CHECKS PASS (25 pages); feed.xml and sitemap.xml valid XML
- Flagged items FLG-001..FLG-016 published on flagged.html; do not block. See questions.html Q-01..Q-12 and suggestions.html SG-01..SG-12 for the open decision register.
- T-09 marked done.

---

## Session 990af5de — handoff and re-verification addendum (2026-11-20)

Branch: `arena/990af5de-affil2`. Work is PR #3 (https://github.com/karagemop466-tech/Affil2/pull/3).

**What happened (conflict log).**
- This session claimed T-01..T-10 on its own branch (commit `41b0c77`) and built a second, parallel site (`docs/`, `tools/`).
- When it tried to open the PR, `main` already contained session `530c2e6c`'s merged work (PR #1 `fdb5d79`, PR #2 `e1b6750`, live on Pages). The two sets of work overlapped on `COORDINATION.md`, `README.md`, `data/products.json`, `data/sources.json`, and the site.
- Resolution: the parallel site was **not merged**. It was removed from this branch before the merge. `main`'s versions of every shared file were kept (`COORDINATION.md`, `README.md`, `data/products.json`, `data/sources.json`, `data/flags.json`, all HTML pages, workflow). No `main` work was discarded.
- The claims T-01..T-10 from `41b0c77` are withdrawn. This session's only contribution is the re-verification below.

**What this addendum adds.**
- `data/reverification-2026-11-20.json`: attempt-by-attempt record for the five short links and the five ASIN pages, with the official sources re-checked.
- Flags FLG-011..FLG-016 added to `data/flags.json` and to the `flagged.html` table. Each has a source link (see the detail text).
  - FLG-011 short-link redirects change between attempts.
  - FLG-012 `B0c8moW59` not reproduced (4 attempts; checkpoint each time).
  - FLG-013 record titles differ from live page titles (P-02, P-03, P-05).
  - FLG-014 tokens are 9 characters (ASIN length rule unverified officially).
  - FLG-015 Program Policies §2(e)/(g) bear on link status.
  - FLG-016 Program Policies §2(d) bears on search-referred purchases.

**Verification performed (2026-11-20, this session).**
- Re-opened all five short links (2–4 attempts where the first failed).
- Opened `/dp/B0CDY277D3`, `/dp/B09B7SB46R`, `/dp/B08DKYBTPH`, `/dp/B0DHZTCNR5`, `/dp/B0DZFD6R9Z`. All exist; ASINs match the record.
- Re-read Operating Agreement §5 (identification statement; matches the site), Program Policies §2(d)/(e)/(g), Google `rel="sponsored"`, and 16 CFR 255.5 excerpt.
- `python3 scripts/check_site.py`: ALL CHECKS PASS (25 pages).

**Not verified in this pass.** Prices, ratings, model numbers, preset counts, FTC FAQ text, Associates account / Special Link test, tracking-ID activity. These stay with the existing flags (FLG-002, FLG-004, FLG-005, FLG-008, FLG-009).

**Merge.** PR #3 merges this addendum into `main`. Pages redeploys from `main` through `.github/workflows/pages.yml`. The merge result is recorded in the PR.


## Session 4bbf49bb — T-11 completion and coordination (2026-11-20)

- Completed non-overlapping publication styling, original category illustrations, decision-path guidance, clearly labeled topic hypotheses, and safer search rendering/input targeting. Site data and product facts were not altered.
- The subsequent upstream T-10 claim (`937876a6`) owned the generated landing page. Its updated `index.html` was preserved intact during rebase. T-12 later integrated the three generic editorial illustrations into the card generator; they are not product photos.
- Other rebase conflicts were resolved by retaining upstream T-10 work and adding only T-11's decision panel in `questions.html`; no upstream product or source data was discarded.
- Verification: `python3 scripts/check_site.py` passed (25 pages); all illustrations parsed as XML; changed-page assets exist; local HTTP smoke checks returned 200 for homepage, decision pages, search, and illustrations; `git diff --check` passed.
- Self-hosted analytics, Search Console, Associates account access, and Special Link tests remain pending and are not represented as live.
- PR #7: https://github.com/karagemop466-tech/Affil2/pull/7 — merged (merge commit 466be4d0c5bab85c3026a2c15a9671e23ffc8af2).
- Pages run 44680289362 for PR #7's merge was cancelled by GitHub because a higher-priority Pages deployment was queued. The subsequent run 44680310672 for newer main commit a14339c succeeded and included PR #7. Pages API reports status `built` and live URL https://karagemop466-tech.github.io/Affil2/.

## T-10 completion (2026-11-20, session 937876a6)
- PR: https://github.com/karagemop466-tech/Affil2/pull/6 — merged via `gh pr merge 6 --merge`, merge commit df6c8e178901c89f4fb850783c4ad5fffb87887b, state MERGED.
- GitHub Pages: build for df6c8e1 status `built`; deploy run 44680124134 success. Live https://karagemop466-tech.github.io/Affil2/flagged.html shows FLG-017..028 (verified after cache refresh).
- Gate: scripts/check_site.py ALL CHECKS PASS (25 pages), now includes XML well-formedness (feed.xml, sitemap.xml) and stale-value checks.
- Re-check of P-03 (B08DKYBTPH): chunks 3 and 5 contain no product specs (protection plans, recommendations); model, capacity, presets remain from chunk 4 as recorded.
- Still open (flagged, do not block): intended ASINs (FLG-001), tracking ID (FLG-002), short-link compliance (FLG-003), Special Link test (FLG-004), P-04 short-link destination (FLG-012), CHEF iQ battery (FLG-008), Emeril model/presets (FLG-009, FLG-021).

---

## Session e9516a41 — claim, conflict, withdrawal, and handoff (2026-11-20 UTC)

**Claim (withdrawn).** Session `e9516a41` claimed R-01..R-07 on `arena/e9516a41-affil2`. Those claims overlapped T-10 (`937876a6`, in progress: data/products.json, data/sources.json, data/flags.json, scripts/check_site.py, generated HTML, feed.xml) and T-11 (`4bbf49bb`, done: style, illustrations, decision panels). The claim was not merged into `main`.

**Conflict (logged, not resolved by overwrite).** A rebase onto `main` at `466be4d` conflicted in COORDINATION.md. The session's own rebuild (replacing root HTML, data files, and the deploy workflow with a `dist/` build) would have overwritten T-10 and T-11 outputs. Per the protocol, the rebase was aborted and nothing was pushed to `main`. No upstream work was discarded. The rebuild is kept as an untracked patch in the workspace (`handoff-e9516a41/`, not committed), so T-10 can cherry-pick ideas from it if wanted.

**Verified this run (official Amazon pages read in this session):**
- P-03 B08DKYBTPH: title "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option…" confirmed. Buy-box: New, $69.99, Amazon.com. Spec table not reached in chunks 0–3, so the "200–400 °F" range is **not confirmed and remains an open conflict** (FLG-012).
- P-01 B0CDY277D3: title confirmed. Buy-box state differs between reads: earlier "Used – Like New" (Amazon Resale); this run "Buy New $79.93, sold by Amazon.com". Treat the offer state as unstable (FLG-018).
- P-02 B09B7SB46R, P-05 B0DZFD6R9Z: titles and breadcrumbs confirmed against the main records.
- B0DHZTCNR5: listing exists (ThermoMaven). Not confirmed as P-04's target (FLG-014).
- Short links this run: P-01, P-02, P-05 resolved; P-03 inconsistent (checkpoint once, product page once); P-04 never reached a product page (homepage, sign-in, "Continue shopping" checkpoint, each once) — FLG-013, FLG-014.

**Findings for the T-10 owner (not applied here, because T-10 owns these files):**
1. Main still states spec values this run could not reproduce from the listing text it read: P-01 "200–450 °F" and "120 V / 1700 W"; P-03 "120 V / 1000 W" and "200–400 °F (listing)"; P-02 "16.9 inches of depth"; P-04 "±0.5 °F", "NIST and NSF", "1 AAA battery"; P-05 "Up to 50 hours" battery. Some may be correct from pages read by 530c2e6c or 937876a6. Each needs a spec-table citation with the chunk number, or removal.
2. Main's `index.html` P-03 card and `products/p03-chefman-8qt-turbrofry.html` keep the slug typo "turbrofry". Consider renaming in the T-10 integration.
3. The buy-box state for P-01 changes between reads (see above). Consider a FLG entry with the date-stamped observations.
4. `scripts/check_site.py` on main passes (25 pages). Consider adding a rule that spec-like values must be quoted from an observed title or a cited table row.
5. Pages source must be the GitHub Actions workflow if the `dist/` approach is used; main currently deploys root via the workflow at `.github/workflows/pages.yml`. Keep as is unless T-10 changes it.

**Remaining open (owner action, unchanged):** FLG-001 intended ASINs; FLG-002 tracking ID; FLG-004 Special Link test; FLG-019 commission schedule; FLG-028 Search Console; FLG-032 research data.

**Status:** session `e9516a41` makes no further changes to shared outputs. It holds no active claim. Re-claim only after T-10 is marked done.


## Session 4bbf49bb — T-12 claim (2026-11-20)

- T-10 and T-11 are complete. This final integration connects existing original, generic SVG artwork to the data-driven card generator and its generated pages.
- Scope: scripts/build_content.py, generated product cards in index/category/guide pages, compare.html generated comparison block, and this coordination record. No product facts, source data, policy claims, or outbound links will change.
- The latest rebase preserved upstream main's T-10 completion and the e9516a41 conflict/handoff record in COORDINATION.md; no upstream files were discarded.


## Session 4bbf49bb — T-12 completion (2026-11-20)

- Integrated the original generic SVG illustrations into the data-driven product-card generator. All generated cards carry descriptive alt text explicitly saying the art is not a product photo.
- Fixed a generator non-idempotence issue: the compare page's “Air fryers” heading accumulated on repeat builds. The generator now replaces the entire generated comparison block.
- Verification: `python3 scripts/build_content.py` run twice with identical second-run output; `python3 scripts/check_site.py` passed (25 pages); all SVG/feed/sitemap XML parsed; generated asset paths, five homepage card images, and single compare headings verified; `git diff --check` passed.
- No product data, sourced values, links, or compliance claims changed. Existing unknowns remain flagged.
- PR #11: https://github.com/karagemop466-tech/Affil2/pull/11 — merged (merge commit d51c04ac301c0c8dc9b9d34142d9391afb9e6c1b).
- GitHub Pages deploy run 44680641868 for that merge succeeded; Pages API status is `built` at https://karagemop466-tech.github.io/Affil2/.

---

## Session `arena/9397cc0c-affil2` — additive pass (2026-11-20)

**Branch:** `arena/9397cc0c-affil2` (platform-bound; cannot create per-task branches)
**Base:** `981db91` (main, after PR #9)

### What this session did first, and got wrong

It built a **second, parallel site** (`docs/`, `build.js`, `content/`, `assets/`) before reading the
board closely enough to notice that `main` already contained a merged, live site from sessions
`530c2e6c`, `6e40cecc`, `937876a6` and `4bbf49bb`. It then opened PR #10.

**Resolution:** PR #10 was **closed unmerged** (https://github.com/karagemop466-tech/Affil2/pull/10).
The parallel site was not merged and no `main` work was discarded. This is recorded rather than
quietly deleted, because the coordination rule exists precisely to prevent this and it was broken.

What the duplicate did produce that was genuinely new — and which `main` did not contain — is below.

### What was added (append-only; no existing row edited or removed)

| Added | Where | Why it was missing |
|-------|-------|--------------------|
| `S20` Creators API registration/eligibility | `data/sources.json` | The site described a research/automation capability but no source documented the gate on it. |
| `S21` PA-API 5 deprecation notice | `data/sources.json` | PA-API 5 is the API most affiliate tooling assumes exists. It now returns HTTP 403. Not previously cited anywhere. |
| `S22` USDA FSIS Safe Minimum Internal Temperature Chart | `data/sources.json` | Thermometer pages discuss doneness with no food-safety authority cited. |
| `FLG-029` Automation blocked until final acceptance | `data/flags.json` | Follows from S20 + S21. |
| `FLG-030` No food-safety source cited until now | `data/flags.json` | Follows from S22. |
| USDA doneness table on both thermometer product pages | `scripts/build_content.py` (`usda_doneness_block()`) | Added in the generator, not by hand-editing generated HTML; scoped to `cat == 'Meat Thermometers'`; verified idempotent across three consecutive generator runs. |

### Verification performed this session (2026-11-20)

| Item | Official source | Result |
|------|-----------------|--------|
| Creators API eligibility | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api | "before you register … you must have an Amazon Associates account that has been reviewed and received final acceptance"; "available only to associates who have referred qualified sales"; "Only the primary account owner … can sign up" |
| Creators API introduction | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction | Prerequisite list states "at least 10 qualifying sales within the past 30 days to access the PA API through the Creators API" |
| PA-API 5 status | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation | "has been deprecated"; callers receive HTTP `403 Forbidden` / `AccessDeniedException`; migrate to Creators API |
| USDA temperatures | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart | 165 / 160 / 145+3min / 145 / 165 °F, quoted verbatim |
| Store ID suffix | https://www.amazon.com/b?node=51812349011 | Amazon: "our software automatically adds "-20" to the end of all Store IDs" — corroborates FLG-002 (format only; issuance still unverified) |

### Independent corroboration of existing flags

This session's own link testing agrees with `main` rather than contradicting it:

- `link.amazon/B0c8moW59` resolved to `B0DHZTCNR5` once and to the Amazon homepage on a second attempt — consistent with `main`'s FLG-012 and FLG-011.
- All five supplied tokens are 9 characters while the observed ASINs are 10 — matches `main`'s FLG-014.

Both observations were reached separately, which raises confidence in them.

### Gate status after this change

- `python3 scripts/build_content.py` — runs clean, idempotent
- `python3 scripts/check_site.py` — **checked 25 pages, ALL CHECKS PASS**
- `sitemap.xml` and `feed.xml` — parse as valid XML
- No new pages added, so the sitemap requires no new entry

### PR and merge record — session `arena/9397cc0c-affil2`

| Field | Value |
|-------|-------|
| PR opened | https://github.com/karagemop466-tech/Affil2/pull/13 |
| PR #10 (duplicate site) | **Closed unmerged** — https://github.com/karagemop466-tech/Affil2/pull/10 |
| Merge | `gh pr merge 13 --merge` — state **MERGED** |
| Merge commit | `1c52f8a985b83816bd02a1691adc4bde6b38fa45` |
| Pages deploy | `pages build and deployment` for `1c52f8a` — **completed / success** |
| Live URL | https://karagemop466-tech.github.io/Affil2/ |
| Post-deploy verification | `sources.html` serves S20, S21, S22. `products/p04-thermomaven-1sec.html` and `products/p05-chefiq-sense-gen3.html` serve the USDA doneness table. `flagged.html` and `data/flags.json` on `main` carry 30 flags through FLG-030. |

**Conflicts encountered and how they were resolved.** Rebasing onto current `main` conflicted in `compare.html` and `COORDINATION.md`. Neither side's work was discarded. `compare.html` is generated output, so it was restored from `main` and reproduced byte-identical by re-running the generator (this PR contributes no change to it). `COORDINATION.md` was resolved by keeping both session records, `main`'s first and this session's appended.

**Mistake recorded.** This session hand-edited the generated product pages to add the USDA block on its first attempt. `scripts/build_content.py` regenerated those files and silently wiped the edit. The block was then moved into the generator itself, scoped to the thermometer category, and verified idempotent over three consecutive runs. Generated files must never be hand-edited.

### Still not done, and why

- **Analytics endpoint.** Unchanged. `assets/app.js` still logs the five events to `localStorage` only. Deploying a self-hosted endpoint needs hosting that GitHub Pages cannot provide (existing FLG-010 / Q-08).
- **Capture form.** No email provider exists, so none was added.
- **Associates test.** Cannot be performed without access to Associates Central (existing FLG-004).

---

## Session `5506d56a` — one generator over the shared register

Branch `arena/5506d56a-affil2`. Base `e1b6750`, merged forward from `15aee5c` before opening the PR.
Task board: this session claimed T-10..T-16 and built the single-generator front end. Nothing below
rewrites another session's records.

### What changed, and what deliberately did not

| File | Change |
|---|---|
| `data/products.json`, `data/sources.json`, `data/reverification-2026-11-20.json` | **read-only.** Consumed as the record of truth. `git diff` against `main` on these three files is empty |
| `data/editorial.json` | **new.** This site's voice — headline, best-for, trade-off, FAQ per product — so annotations live outside the shared register |
| `data/usda-temperatures.json` | **new.** The FSIS table (S22) as data, so the numbers are rendered, not typed into prose. Ported from the block `9397cc0c` added to the thermometer pages, which this generator would otherwise have overwritten |
| `data/flags.json` | **appended only.** Added FLG-031 (P-02 accessory count), FLG-032 (no hands-on testing), FLG-033 (no named author), FLG-034 (P-01 quarts vs litres), FLG-035 (certification is a seller statement). Added `severity`, `links` and `owner_status` to every record so each row can cite a source. No existing `title` or `detail` was modified — checked field by field against `main` |
| `scripts/build_site.py` | **new.** Generates all 29 pages, `sitemap.xml`, `feed.xml`, `robots.txt` |
| `scripts/build_content.py` | **superseded.** Left on disk, unreferenced by CI. `build_site.py` is now the only generator. Removing it is safe but was not done here, to avoid deleting another session's file |
| `scripts/check_site.py` | rewritten (below) |
| `assets/style.css`, `assets/app.js` | rebuilt for the generated markup. The illustrations from `4bbf49bb` are kept and used |
| `.github/workflows/pages.yml` | regenerate → fail on drift → gate → deploy; also runs on pull requests |
| `.nojekyll` | added so `assets/` is served as-is |

### Conflict resolution, stated plainly

`main` advanced from `e1b6750` to `15aee5c` (through PR #14) while this session worked. Three of the
defects this session set out to fix — listing title drift, P-03 wattage, the malformed feed — had
already been found and fixed there. `main`'s register was therefore adopted rather than duplicated.

Two numeric collisions were resolved in `main`'s favour:

- My FLG-029 (P-01 quarts vs litres) clashed with `main`'s FLG-029 (product-data automation blocked).
  Mine was renumbered **FLG-034**.
- My FLG-030 (certification) clashed with `main`'s FLG-030 (food-safety source). Mine became
  **FLG-035**.

Every `FLG-nnn` written into page copy was then re-checked against the register's `title`, and the
hardcoded numbers that assumed an older numbering were corrected. A gate rule now fails the build if
a page cites a flag that is not defined, or if a defined flag is never published.

### The gate, as it now stands

Page level: doctype, `lang`, canonical matching the page's own path, one `<h1>`, the Associates
statement twice with the first occurrence above `<main>`, nav and footer completeness, no
root-relative links, no broken internal link or asset, JSON-LD that parses, no template debris.

Compliance level: every `amazon.com` link carries `rel="sponsored nofollow"`; every outbound product
link carries `tag=shopnow047c-20`; no `$` amount, star rating or review count anywhere.

Data level: a blank field must be marked `unverified`; every flag needs a source that exists in
`sources.json`; every defined flag must be published and every published flag must be defined;
thermometer pages must carry the USDA block and air-fryer pages must not.

Build level: every page in `sitemap.xml` and every sitemap entry backed by a file; `feed.xml` parses
and its items exist; `robots.txt` points at the canonical sitemap; the embedded search index parses
and its URLs exist. CI additionally regenerates and fails if the committed pages differ from the
generator output.

### Run

    python3 scripts/build_site.py
    python3 scripts/check_site.py
    → checked 29 pages, 5 product records, 35 flags, 17 sources — ALL CHECKS PASS

### PR and deploy

| Field | Value |
|-------|-------|
| PR | https://github.com/karagemop466-tech/Affil2/pull/15 |
| Merge | merged into `main`; Pages deploy result recorded below in the next commit |
| Open items | FLG-001 to FLG-035 published on `flagged.html`; none blocks publication |

### Still not done

- **Analytics endpoint.** Unchanged: `assets/app.js` logs five events to `localStorage` and its
  `send()` is a no-op. Needs hosting GitHub Pages cannot provide (FLG-010, Q-08).
- **Associates link test.** Needs Associates Central (FLG-004). Every product page says `PENDING TEST`.
- **Intended ASINs.** Owner-only (FLG-001).
- **`scripts/build_content.py`.** Unreferenced now. Delete deliberately, not by accident.

### Corrective follow-up — the workflow was reverted, not shipped

Found on the post-merge check: `main` still carried the old single-job `Deploy GitHub Pages`
workflow. Cause: an early `git checkout origin/main -- .github/workflows/pages.yml` in this session's
first integration attempt restored the upstream copy over the hardened one, and the later force-push
of the rebased branch kept that reverted file. Consequence: PR #15 merged and Pages deployed
successfully, but the generator-drift check and `check_site.py` never ran in CI. The site itself is
correct — the gate passes locally — but the enforcement this PR promised was absent.

Fixed in a follow-up PR: the workflow is now a single `verify` job (regenerate → fail on drift →
`check_site.py`) that runs on pull requests and on pushes to `main`.

It does not deploy, on purpose. This repository's Pages site is configured as **legacy**
(`build_type: legacy`, `main` /), so GitHub's own branch builder publishes every push. Adding
`actions/deploy-pages` on top of that would fail against a legacy site and duplicate the deployer.
Given that the branch builder publishes whatever lands on `main`, the gate cannot block a merge by
itself; it makes a breakage loud and immediate instead, which is what a repository without branch
protection can actually support.

---

## Session `82c875a9` — storefront front end (T-17)

Branch `arena/82c875a9-affil2`, base `1a19c24`. Claiming one task with a file scope that no other
session holds; nothing in `main` is being rewritten.

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-17 | Storefront rebuild: editorial photography, front page that leads with products, store-style cards, CSS refresh | in progress | 82c875a9 | `assets/photos/*`, `assets/style.css`, `scripts/build_site.py`, `scripts/check_site.py`, `data/editorial.json` (annotations only), generated HTML, `COORDINATION.md` |

Scope note: `data/products.json`, `data/sources.json` and `data/flags.json` are **read-only** for this
session. Any new flag is appended to `data/flags.json` only if an existing one does not already cover
the finding; no existing title or detail is modified. `data/editorial.json` gets image/season
annotations only. Baseline before this session: `build_site.py` + `check_site.py` both clean,
29 pages, ALL CHECKS PASS.

### T-17 result — storefront rebuild (session `82c875a9`)

| Field | Value |
|---|---|
| Pages rebuilt | 29 (all generated) |
| Gate | `build_site.py` clean, `check_site.py` **ALL CHECKS PASS** — 29 pages, 5 products, 37 flags, 17 sources |
| New gate rule | every generated photo must be captioned as illustration, carry alt text and intrinsic dimensions |
| New flag | FLG-037 — on-site search was inert on `main`; the index existed but nothing read the query. Fixed and published. |
| New proposal IDs | SG-17..SG-22 (front-page rotation, intent landing pages, change log, head-to-head view, editor decision, hands-on policy) |
| New question IDs | Q-15..Q-18 (imagery approval, basis for the picks, one-sentence purpose, jurisdictional disclosure) |

**Verification performed this session.** Re-fetched and re-read: the Amazon Associates Program Policies
page (S02, "Updated: April 14, 2026"), FTC *Disclosures 101* (S03 supporting document — disclosure must
be hard to miss, not buried at the end of a page or behind a click), Google *Qualify your outbound
links* (S04, `rel="sponsored"`, multiple values allowed, last updated 2025-12-10), the USDA FSIS safe
temperature chart (S22, last updated Apr 14 2025 — all ten rows still match `data/usda-temperatures.json`),
and listings B0CDY277D3 and B08DKYBTPH, both of which still serve the titles recorded in the register.
No register value was changed on the strength of this pass; nothing needed correcting.

**Irregularity found, then resolved the other way round.** `guides/instant-vs-wireless.html` quoted the
ThermoMaven's upper range as 572 °F while `data/products.json` marked that field `unverified`. Rather than
delete the prose, the listing was re-read: the product-information table states `Upper Temperature Range
572 °F`, so the guide was right and the register was stale. See the re-read below.

**Files not touched.** `data/products.json`, `data/sources.json` read-only. `data/flags.json` appended only
(FLG-036, FLG-037). No other session's work was modified or reverted.

### Live-listing re-read (2026-11-20) — seven blanks filled, one prose claim withdrawn

Triggered by the 572 °F question above, every product page was re-read in full rather than from a partial
excerpt. The product-information tables carry values an earlier pass had never reached.

| Product | Field | Value now published | Section named as source |
|---|---|---|---|
| P-02 Emeril 26QT | Model | 4-00675-02X-VN | Item details: Model Number / Part Number |
| P-02 Emeril 26QT | Temperature | 75–500 °F | Features & Specs: Min 75 °F, Max 500 °F |
| P-02 Emeril 26QT | Power | 120 V / 1700 W | Features & Specs: Output Wattage, Wattage, Voltage |
| P-04 ThermoMaven | Model | HT07 | Item details: Model Name / Model / Part Number |
| P-04 ThermoMaven | Upper temperature | 572 °F | Features & Specs: Upper Temperature Range |
| P-05 CHEF iQ Sense | Model | CQ60-3C-Z1-E | Item details: Model / Part Number |
| P-05 CHEF iQ Sense | Probe length | 4.75 in | Immersion Depth; Measurements: Item Length |

Two adverse findings came out of the same pass and are published, not smoothed over:

- **FLG-039.** Three guides stated weights — 26.5 lb, 12.8 lb, "around 13 pounds" — that no listing
  carries. The prose contradicted the register, which had weight correctly marked unverified. Every
  weight figure was removed from the guide copy and the register's blank now prints on the compare page
  with its reason.
- **FLG-038.** The CHEF iQ listing states a two-year assurance in About this item and a `Warranty
  Description` of `3 Year` in Item details. Both are now printed as a conflict; the earlier register
  record held only the two-year figure.

Nothing was inferred. Weight stays blank for all five products because no listing states it, and the
model numbers moved from blank to stated only because the section naming them was read directly.

### Shipped in the same pass, so the Decision Center stays honest

- **SG-20 (was: recommended).** A dated, reader-facing change log now sits on `sources.html`, generated
  from every flag whose severity is `corrected`.
- **SG-21 (was: recommended).** The compare page has a working two-at-a-time head-to-head: two selectors,
  17 aligned rows, rendered from an embedded view of the same register, with both buy links tagged. The
  gate now checks that data parses, that each of the five products is present, that every linked page
  exists and that every buy link carries the Associates tag.
- **SG-18 (partially).** The front page prints a dated issue line; the picks themselves are still static,
  so rotation remains open (Q-16).
- **S23 added.** FTC *Disclosures 101* is now in the source register and cited for disclosure placement.
  It was fetched and quoted this session; it is official FTC material, not a third-party summary.

### Link and build audit this session

- `scripts/check_site.py`: 29 pages, 5 products, 40 flags, 18 sources — **ALL CHECKS PASS**.
- Independent audit across all 29 pages: 0 broken internal links, 0 missing assets, 0 un-sponsored
  amazon.com anchors.
- `node --check assets/app.js`: clean. Search and pair-view scripts syntax-checked.
- Every generated photograph is captioned, has alt text and intrinsic dimensions; the gate fails
  otherwise.

---

## Session 5ecbe089 — measurement and publication integration
T-17 | in progress | 5ecbe089 | COORDINATION.md, measurement/, assets/app.js, scripts/build_site.py and generated publication outputs, assets/feature.webp, analytics documentation. Integrate current main first; preserve existing verification records.
Coordination append conflict resolved by retaining both session entries.
Scope adjustment: PR #16 already owns the collector and platform proposal; do not duplicate or overwrite that work. This integration covers the publication shell, search and local event wiring, generated pages, assets/style.css and original illustrative scenes (feature.jpg, basket.jpg, probe.jpg).
T-17 | done (publication integration); server-side analytics remains needs review (FLG-010, parallel PR #16). New front-page artwork illustrates cooking situations, not specific SKUs. No new specifications, trend claims, orders or ASIN confirmations. Search renders text nodes from the generated index; search event contains only result count. Reviewed Amazon's Special Link requirement at https://affiliate-program.amazon.com/help/operating/agreement (section 1); no account-level reporting access. Inherited listing evidence was preserved, not newly certified. Local generator + integrity gate: 29 pages, five products, 35 published flags, 17 registered sources; passed.
Rebase integration: preserved concurrent buyer-facing copy from #19 under the new featured section heading; regenerated index rather than hand-editing it.

Release: [PR #20](https://github.com/karagemop466-tech/Affil2/pull/20) merged to main as abc753d. GitHub Pages reported built for descendant 64a35e5; [deployment succeeded](https://github.com/karagemop466-tech/Affil2/actions/runs/44682594233). Confirmed the new cover is present in the deployed revision.

### PRs opened and merged by this session

| PR | Title | Result | Commit / deploy |
|----|-------|--------|-----------------|
| [#15](https://github.com/karagemop466-tech/Affil2/pull/15) | One generator over the merged register, plus a stricter compliance gate | merged | `eacaeca`, Pages built |
| [#17](https://github.com/karagemop466-tech/Affil2/pull/17) | CI: a verify gate that regenerates and checks every page | merged, `Verify site` green | `1a19c24`, Pages built |
| [#19](https://github.com/karagemop466-tech/Affil2/pull/19) | Copy: stop explaining the brief to shoppers | merged, green | `829398c`, Pages built |
| [#21](https://github.com/karagemop466-tech/Affil2/pull/21) | Compare table: category-aware rows, and a gate rule against cross-row placeholders | merged, green | `64a35e5`, Pages built |
| [#24](https://github.com/karagemop466-tech/Affil2/pull/24) | Fix a page that quoted 572 °F and called the same field unverified | merged, green | `2a4ffa8`, Pages built |

Live: https://karagemop466-tech.github.io/Affil2/ — `pages build and deployment` reported
`completed/success` for every one of these commits, and `Verify site` reported `completed/success`
on the same SHA each time.

### Three defects found by reading the live pages, not the local build

Each of these passed the gate at the time it was published, which is why they are recorded here
rather than quietly fixed.

1. **A page contradicted itself.** `products/p04-thermomaven-1sec.html` left upper temperature blank
   in the spec table and answered the same question in the FAQ with "572 °F". Fixed in PR #24, and
   the gate now fails when a FAQ states a figure the register calls unverified or conflicting.
2. **Placeholders leaked between categories.** The comparison table printed
   "n/a, not a capacity appliance" in the weight and dimensions rows and "see battery row" in the
   power row, pointing at a row that does not exist. Fixed in PR #21, with a gate rule against that
   class of text.
3. **The gate was not running in CI at all.** Recorded above, fixed in PR #17.

Lesson for the next session: `python3 scripts/check_site.py` proves the markup is compliant, not that
it reads correctly. Read at least one product page and `compare.html` on the live URL after deploying,
with a cache-busting query string, because GitHub Pages will serve a cached older build for a while
and it is easy to mistake that for your own bug.

## Session `3fb8f29e` — claim

> NOTE (renumbered): another session used T-17 for its measurement/publication integration (merged in PR #20). This session's task is therefore T-18.

Branch `arena/3fb8f29e-affil2`. Base `1a19c24` (main, after PR #17). Task: independent re-verification pass over the five official listings and the policy sources, plus one new deliverable the owner asked for — a generated `design-brief.html` (design prompt pack + organic-traffic plan + editorial standards) wired into the Decision Center as proposal SG-17. Then: build, gate, PR, merge, Pages confirmation, and the record here.

Scope: `scripts/build_site.py`, `scripts/check_site.py` (only if a new gate rule is needed), new generated page `design-brief.html`, `sitemap.xml`, `feed.xml`, `robots.txt`, `COORDINATION.md`, `README.md` (one row), generated HTML. No other session's open PR (#16, branch `arena/bdedd85e-affil2`) is touched. Shared register `data/products.json`, `data/sources.json` are read-only unless verification proves a value wrong; `data/flags.json` is append-only.

T-18 | Re-verification + design & traffic brief + PR/merge/Pages record | in progress | 3fb8f29e | scripts/build_site.py, design-brief.html, sitemap.xml, feed.xml, robots.txt, COORDINATION.md, README.md

## Session `3fb8f29e` — T-18 completion record

T-18 (renumbered from T-17; session 5ecbe089 used T-17 for its measurement/publication integration, merged as PR #20). Base `1a19c24`; rebased through `2a4ffa8` (PRs #19–#24 landed mid-flight).

What shipped in [PR #26](https://github.com/karagemop466-tech/Affil2/pull/26):

- New generated page `design-brief.html` — the Design & Traffic Brief: a copy-paste design prompt (brand, front-page anatomy, components, type and tone, illustration, accessibility, SEO/structured data, compliance, forbidden patterns); a 15-topic cluster plan labelled as hypotheses; a 2026-11-26 → 2027-02-14 seasonal calendar; a ten-point "not AI slop" editorial standards checklist; an explicit "what this brief does not claim" section; a brief-element-to-live-state mapping table.
- SG-17 added to the Decision Center as "Adopt the Design & Traffic Brief as the next build step" (status: Not started — recommended for approval). It is linked from the footer dashboard group on all 30 pages, from the sitemap and from the on-site search index.
- Docs reconciled: README start-here table (17 proposals, 35 flags); `EXECUTIVE-SUMMARY.md` gained a dated re-verification log and its never-registered SG-17..SG-20 / Q-15..Q-16 IDs were renumbered (live SG-17 = the brief; UF-1/UF-2 hold the leftover ideas).

Independent re-verification (2026-11-20, all fetched live this session; full table in the PR body): all five official listings re-read line by line — titles, breadcrumbs, capacity, temperature ranges, wattage, dimensions, warranty, presets, probes, sensors, battery wording, included components — **all match the register**; the known listing contradictions (FLG-008, FLG-017, FLG-018, FLG-021, FLG-034) reproduce exactly as flagged. USDA FSIS chart, Google qualify-outbound-links, Associates Program Policies (updated 2026-04-14), PA-API 5 deprecation notice and the FTC Endorsement Guides FAQ were all re-fetched and match what the site cites. **No register corrections were required.**

Merge: `gh pr merge 26 --merge` → merge commit `c021fb0`. GitHub Pages deploy run `44683183551` → **success** (site serves design-brief.html, confirmed live). "Verify site" run on the merge commit `44683184399` → **success**.

Process notes: two rebases onto a fast-moving main; conflicts in COORDINATION.md, assets/style.css and generated pages resolved by keeping both sides and regenerating from the merged generator — no hand-edited HTML; committed pages re-verified byte-identical to generator output before push. One `git push --force-with-lease` (this branch only; lease checked). Open and untouched: PR #16 (analytics collector, needs review/owner decision), FLG-001..FLG-035 (all published, none blocks).

---

## Session 42617e35 — independent re-verification, polish pass, and merge reconciliation

Branch `arena/42617e35-affil2` (base e1b6750). Claimed T-10..T-17 at start; the claim block is preserved in this session's history (commit 6f9f056). By the time this branch integrated, sessions 436f4dbe / 937876a6 / 9397cc0c / 4bbf49bb / 5506d56a / 5ecbe089 / bdedd85e had advanced `main` through PRs #2–#23, including the generator (`scripts/build_site.py`), the expanded gate, the 35-flag register and the magazine shell.

### Independent verification (2026-11-20, live fetches, official sources only)

| Item | Result |
|---|---|
| B0CDY277D3 · B09B7SB46R · B08DKYBTPH · B0DHZTCNR5 · B0DZFD6R9Z | Live listing titles fetched and matched line by line against the register — corroborates the existing observed-target records (S10–S19). Live title drift noted on P-02 (title states 24 presets) and P-03 (title states 450 °F Hi-Fry) — both already published as FLG-021 / FLG-018. |
| FTC Endorsement Guides FAQ (S03) | Re-verified live. |
| Google Qualify outbound links (S04) | Re-verified live (rel=sponsored; multiple rel values valid). |
| USDA FSIS temperature chart (S22) | Verified live: poultry 165 °F, leftovers 165 °F, steaks 145 °F + 3-min rest (chart dated 2025-04-14). Corroborates S22. |
| S01/S02 Associates OA + Program Policies | Fetch blocked (login-gated). URLs left for manual review; no wording claimed as re-verified. Existing FLG-026 already covers source-URL health. |

### Merge conflict log (2026-11-20)

`gh pr merge 22` refused: `main` had moved (PRs #3..#23). Per protocol the merge was stopped and resolved **without discarding any other session's work**:

1. Session artifacts superseded by `main` were **deleted before merging** (kept out of the combined tree): hand-written guides (holiday-hosting, turkey-thermometer-plan, first-week), hand-written page chrome, a parallel `analytics-endpoint/` collector spec, and local imagery. Rationale: guides and page outputs are generator-owned on `main` (CI fails on drift), and the analytics collector scope belongs to **open PR #16** ("do not duplicate or overwrite that work"). The first-week topic survives as a generator-native guide (below).
2. `git merge origin/main` auto-merged `data/products.json` and `assets/app.js` into invalid/duplicated hybrids; both were **restored to main's versions** (`git checkout origin/main -- data/products.json assets/app.js`). Main's schema (per-field `st: verified/unverified`) is authoritative and its gate depends on it. Nothing from main was lost.
3. This file: main's copy won the conflict; this entry re-appends session 42617e35's log rather than replacing anyone's.

### Unique contributions merged in this pass (generator-level, regenerated)

- **SG-17…SG-30** rows in the Decision Center (`scripts/build_site.py` → `suggestions.html`), including the required parallel-pass rows: SG-27 nav labels, SG-28 the shipped RSS feed, SG-29 Search Console, SG-30 reader capture.
- **`guides/first-week-air-fryer.html`** — evergreen getting-started guide added to the generator's guide list (in sitemap + feed automatically).

Gate after regeneration: `python3 scripts/build_site.py` (30 pages) + `python3 scripts/check_site.py` → **checked 30 pages, 5 product records, 35 flags, 17 sources — ALL CHECKS PASS**.

### Second conflict round (same day)

`gh pr merge 22` refused again: `main` moved through PRs #24–#27 (including the Design & Traffic
Brief and an SG ID-collision fix). Resolved the same way — main's versions kept, this session's
additions re-applied on top of the merged generator, generated outputs regenerated. Renumbering note:
this session's register rows are **SG-18…SG-30**; its original SG-17 slot is occupied on main by the
Design & Traffic Brief row (SG-17), and its re-verification content is covered by the 5d81a8f log.

### Third conflict round (same day, storefront pass)

`main` moved again (PRs #28–#30, session 82c875a9 storefront rebuild; proposals renumbered
SG-18…SG-23). Resolved the same way: main's versions kept, this session's additions re-applied on
the merged generator. Final register placement for this session: **SG-24…SG-30** (SG-24 first-week
guide shipped; SG-25 collector deploy; SG-26 ledger feed; **SG-27 nav labels · SG-28 the shipped RSS
feed · SG-29 Search Console · SG-30 reader capture** — the required parallel-pass rows).

### PR / deploy result
- PR: https://github.com/karagemop466-tech/Affil2/pull/22 (this branch → main). Merge result and Pages verification are recorded in the follow-up record commit after the merge.
- Superseded/owned-elsewhere work, for the record: analytics collector + measurement surface = PR #16 (open, session bdedd85e); hand-written polish artifacts dropped in favor of generator outputs = see merge log above.

## Session 42617e35 — independent re-verification, polish pass, and merge reconciliation

Branch `arena/42617e35-affil2` (base e1b6750). Claimed T-10..T-17 at start; the claim block is preserved in this session's history (commit 6f9f056). By the time this branch integrated, sessions 436f4dbe / 937876a6 / 9397cc0c / 4bbf49bb / 5506d56a / 5ecbe089 / bdedd85e had advanced `main` through PRs #2–#23, including the generator (`scripts/build_site.py`), the expanded gate, the 35-flag register and the magazine shell.

### Independent verification (2026-11-20, live fetches, official sources only)

| Item | Result |
|---|---|
| B0CDY277D3 · B09B7SB46R · B08DKYBTPH · B0DHZTCNR5 · B0DZFD6R9Z | Live listing titles fetched and matched line by line against the register — corroborates the existing observed-target records (S10–S19). Live title drift noted on P-02 (title states 24 presets) and P-03 (title states 450 °F Hi-Fry) — both already published as FLG-021 / FLG-018. |
| FTC Endorsement Guides FAQ (S03) | Re-verified live. |
| Google Qualify outbound links (S04) | Re-verified live (rel=sponsored; multiple rel values valid). |
| USDA FSIS temperature chart (S22) | Verified live: poultry 165 °F, leftovers 165 °F, steaks 145 °F + 3-min rest (chart dated 2025-04-14). Corroborates S22. |
| S01/S02 Associates OA + Program Policies | Fetch blocked (login-gated). URLs left for manual review; no wording claimed as re-verified. Existing FLG-026 already covers source-URL health. |

### Merge conflict log (2026-11-20)

`gh pr merge 22` refused: `main` had moved (PRs #3..#23). Per protocol the merge was stopped and resolved **without discarding any other session's work**:

1. Session artifacts superseded by `main` were **deleted before merging** (kept out of the combined tree): hand-written guides (holiday-hosting, turkey-thermometer-plan, first-week), hand-written page chrome, a parallel `analytics-endpoint/` collector spec, and local imagery. Rationale: guides and page outputs are generator-owned on `main` (CI fails on drift), and the analytics collector scope belongs to **open PR #16** ("do not duplicate or overwrite that work"). The first-week topic survives as a generator-native guide (below).
2. `git merge origin/main` auto-merged `data/products.json` and `assets/app.js` into invalid/duplicated hybrids; both were **restored to main's versions** (`git checkout origin/main -- data/products.json assets/app.js`). Main's schema (per-field `st: verified/unverified`) is authoritative and its gate depends on it. Nothing from main was lost.
3. This file: main's copy won the conflict; this entry re-appends session 42617e35's log rather than replacing anyone's.

### Unique contributions merged in this pass (generator-level, regenerated)

- **SG-17…SG-30** rows in the Decision Center (`scripts/build_site.py` → `suggestions.html`), including the required parallel-pass rows: SG-27 nav labels, SG-28 the shipped RSS feed, SG-29 Search Console, SG-30 reader capture.
- **`guides/first-week-air-fryer.html`** — evergreen getting-started guide added to the generator's guide list (in sitemap + feed automatically).

Gate after regeneration: `python3 scripts/build_site.py` (30 pages) + `python3 scripts/check_site.py` → **checked 30 pages, 5 product records, 35 flags, 17 sources — ALL CHECKS PASS**.

### Second conflict round (same day)

`gh pr merge 22` refused again: `main` moved through PRs #24–#27 (including the Design & Traffic
Brief and an SG ID-collision fix). Resolved the same way — main's versions kept, this session's
additions re-applied on top of the merged generator, generated outputs regenerated. Renumbering note:
this session's register rows are **SG-18…SG-30**; its original SG-17 slot is occupied on main by the
Design & Traffic Brief row (SG-17), and its re-verification content is covered by the 5d81a8f log.

### Third conflict round (same day, storefront pass)

`main` moved again (PRs #28–#30, session 82c875a9 storefront rebuild; proposals renumbered
SG-18…SG-23). Resolved the same way: main's versions kept, this session's additions re-applied on
the merged generator. Final register placement for this session: **SG-24…SG-30** (SG-24 first-week
guide shipped; SG-25 collector deploy; SG-26 ledger feed; **SG-27 nav labels · SG-28 the shipped RSS
feed · SG-29 Search Console · SG-30 reader capture** — the required parallel-pass rows).

### Fourth conflict round (same day)

`main` moved again (PR #32: weight-figure gate). Single-file conflict (search.html, generator
output) resolved by regeneration; the merged generator kept both sessions' edits. Register rows for
this session: SG-24…SG-30.

### PR / deploy result
- PR: https://github.com/karagemop466-tech/Affil2/pull/22 (this branch → main). Merge result and Pages verification are recorded in the follow-up record commit after the merge.
- Superseded/owned-elsewhere work, for the record: analytics collector + measurement surface = PR #16 (open, session bdedd85e); hand-written polish artifacts dropped in favor of generator outputs = see merge log above.

## Session 42617e35 — independent re-verification, polish pass, and merge reconciliation

Branch `arena/42617e35-affil2` (base e1b6750). Claimed T-10..T-17 at start; the claim block is preserved in this session's history (commit 6f9f056). By the time this branch integrated, sessions 436f4dbe / 937876a6 / 9397cc0c / 4bbf49bb / 5506d56a / 5ecbe089 / bdedd85e had advanced `main` through PRs #2–#23, including the generator (`scripts/build_site.py`), the expanded gate, the 35-flag register and the magazine shell.

### Independent verification (2026-11-20, live fetches, official sources only)

| Item | Result |
|---|---|
| B0CDY277D3 · B09B7SB46R · B08DKYBTPH · B0DHZTCNR5 · B0DZFD6R9Z | Live listing titles fetched and matched line by line against the register — corroborates the existing observed-target records (S10–S19). Live title drift noted on P-02 (title states 24 presets) and P-03 (title states 450 °F Hi-Fry) — both already published as FLG-021 / FLG-018. |
| FTC Endorsement Guides FAQ (S03) | Re-verified live. |
| Google Qualify outbound links (S04) | Re-verified live (rel=sponsored; multiple rel values valid). |
| USDA FSIS temperature chart (S22) | Verified live: poultry 165 °F, leftovers 165 °F, steaks 145 °F + 3-min rest (chart dated 2025-04-14). Corroborates S22. |
| S01/S02 Associates OA + Program Policies | Fetch blocked (login-gated). URLs left for manual review; no wording claimed as re-verified. Existing FLG-026 already covers source-URL health. |

### Merge conflict log (2026-11-20)

`gh pr merge 22` refused: `main` had moved (PRs #3..#23). Per protocol the merge was stopped and resolved **without discarding any other session's work**:

1. Session artifacts superseded by `main` were **deleted before merging** (kept out of the combined tree): hand-written guides (holiday-hosting, turkey-thermometer-plan, first-week), hand-written page chrome, a parallel `analytics-endpoint/` collector spec, and local imagery. Rationale: guides and page outputs are generator-owned on `main` (CI fails on drift), and the analytics collector scope belongs to **open PR #16** ("do not duplicate or overwrite that work"). The first-week topic survives as a generator-native guide (below).
2. `git merge origin/main` auto-merged `data/products.json` and `assets/app.js` into invalid/duplicated hybrids; both were **restored to main's versions** (`git checkout origin/main -- data/products.json assets/app.js`). Main's schema (per-field `st: verified/unverified`) is authoritative and its gate depends on it. Nothing from main was lost.
3. This file: main's copy won the conflict; this entry re-appends session 42617e35's log rather than replacing anyone's.

### Unique contributions merged in this pass (generator-level, regenerated)

- **SG-17…SG-30** rows in the Decision Center (`scripts/build_site.py` → `suggestions.html`), including the required parallel-pass rows: SG-27 nav labels, SG-28 the shipped RSS feed, SG-29 Search Console, SG-30 reader capture.
- **`guides/first-week-air-fryer.html`** — evergreen getting-started guide added to the generator's guide list (in sitemap + feed automatically).

Gate after regeneration: `python3 scripts/build_site.py` (30 pages) + `python3 scripts/check_site.py` → **checked 30 pages, 5 product records, 35 flags, 17 sources — ALL CHECKS PASS**.

### Second conflict round (same day)

`gh pr merge 22` refused again: `main` moved through PRs #24–#27 (including the Design & Traffic
Brief and an SG ID-collision fix). Resolved the same way — main's versions kept, this session's
additions re-applied on top of the merged generator, generated outputs regenerated. Renumbering note:
this session's register rows are **SG-18…SG-30**; its original SG-17 slot is occupied on main by the
Design & Traffic Brief row (SG-17), and its re-verification content is covered by the 5d81a8f log.

### Third conflict round (same day, storefront pass)

`main` moved again (PRs #28–#30, session 82c875a9 storefront rebuild; proposals renumbered
SG-18…SG-23). Resolved the same way: main's versions kept, this session's additions re-applied on
the merged generator. Final register placement for this session: **SG-24…SG-30** (SG-24 first-week
guide shipped; SG-25 collector deploy; SG-26 ledger feed; **SG-27 nav labels · SG-28 the shipped RSS
feed · SG-29 Search Console · SG-30 reader capture** — the required parallel-pass rows).

### Fifth reconcile (same day, PR #33 copy/gate widening)

Auto-merged without conflict; outputs regenerated. Register rows for this session: SG-24…SG-30.

### PR / deploy result
- PR: https://github.com/karagemop466-tech/Affil2/pull/22 (this branch → main). Merge result and Pages verification are recorded in the follow-up record commit after the merge.
- Superseded/owned-elsewhere work, for the record: analytics collector + measurement surface = PR #16 (open, session bdedd85e); hand-written polish artifacts dropped in favor of generator outputs = see merge log above.

## Session 42617e35 — independent re-verification, polish pass, and merge reconciliation

Branch `arena/42617e35-affil2` (base e1b6750). Claimed T-10..T-17 at start; the claim block is preserved in this session's history (commit 6f9f056). By the time this branch integrated, sessions 436f4dbe / 937876a6 / 9397cc0c / 4bbf49bb / 5506d56a / 5ecbe089 / bdedd85e had advanced `main` through PRs #2–#23, including the generator (`scripts/build_site.py`), the expanded gate, the 35-flag register and the magazine shell.

### Independent verification (2026-11-20, live fetches, official sources only)

| Item | Result |
|---|---|
| B0CDY277D3 · B09B7SB46R · B08DKYBTPH · B0DHZTCNR5 · B0DZFD6R9Z | Live listing titles fetched and matched line by line against the register — corroborates the existing observed-target records (S10–S19). Live title drift noted on P-02 (title states 24 presets) and P-03 (title states 450 °F Hi-Fry) — both already published as FLG-021 / FLG-018. |
| FTC Endorsement Guides FAQ (S03) | Re-verified live. |
| Google Qualify outbound links (S04) | Re-verified live (rel=sponsored; multiple rel values valid). |
| USDA FSIS temperature chart (S22) | Verified live: poultry 165 °F, leftovers 165 °F, steaks 145 °F + 3-min rest (chart dated 2025-04-14). Corroborates S22. |
| S01/S02 Associates OA + Program Policies | Fetch blocked (login-gated). URLs left for manual review; no wording claimed as re-verified. Existing FLG-026 already covers source-URL health. |

### Merge conflict log (2026-11-20)

`gh pr merge 22` refused: `main` had moved (PRs #3..#23). Per protocol the merge was stopped and resolved **without discarding any other session's work**:

1. Session artifacts superseded by `main` were **deleted before merging** (kept out of the combined tree): hand-written guides (holiday-hosting, turkey-thermometer-plan, first-week), hand-written page chrome, a parallel `analytics-endpoint/` collector spec, and local imagery. Rationale: guides and page outputs are generator-owned on `main` (CI fails on drift), and the analytics collector scope belongs to **open PR #16** ("do not duplicate or overwrite that work"). The first-week topic survives as a generator-native guide (below).
2. `git merge origin/main` auto-merged `data/products.json` and `assets/app.js` into invalid/duplicated hybrids; both were **restored to main's versions** (`git checkout origin/main -- data/products.json assets/app.js`). Main's schema (per-field `st: verified/unverified`) is authoritative and its gate depends on it. Nothing from main was lost.
3. This file: main's copy won the conflict; this entry re-appends session 42617e35's log rather than replacing anyone's.

### Unique contributions merged in this pass (generator-level, regenerated)

- **SG-17…SG-30** rows in the Decision Center (`scripts/build_site.py` → `suggestions.html`), including the required parallel-pass rows: SG-27 nav labels, SG-28 the shipped RSS feed, SG-29 Search Console, SG-30 reader capture.
- **`guides/first-week-air-fryer.html`** — evergreen getting-started guide added to the generator's guide list (in sitemap + feed automatically).

Gate after regeneration: `python3 scripts/build_site.py` (30 pages) + `python3 scripts/check_site.py` → **checked 30 pages, 5 product records, 35 flags, 17 sources — ALL CHECKS PASS**.

### Second conflict round (same day)

`gh pr merge 22` refused again: `main` moved through PRs #24–#27 (including the Design & Traffic
Brief and an SG ID-collision fix). Resolved the same way — main's versions kept, this session's
additions re-applied on top of the merged generator, generated outputs regenerated. Renumbering note:
this session's register rows are **SG-18…SG-30**; its original SG-17 slot is occupied on main by the
Design & Traffic Brief row (SG-17), and its re-verification content is covered by the 5d81a8f log.

### Third conflict round (same day, storefront pass)

`main` moved again (PRs #28–#30, session 82c875a9 storefront rebuild; proposals renumbered
SG-18…SG-23). Resolved the same way: main's versions kept, this session's additions re-applied on
the merged generator. Final register placement for this session: **SG-24…SG-30** (SG-24 first-week
guide shipped; SG-25 collector deploy; SG-26 ledger feed; **SG-27 nav labels · SG-28 the shipped RSS
feed · SG-29 Search Console · SG-30 reader capture** — the required parallel-pass rows).

### Fourth conflict round (same day)

`main` moved again (PR #32: weight-figure gate). Single-file conflict (search.html, generator
output) resolved by regeneration; the merged generator kept both sessions' edits. Register rows for
this session: SG-24…SG-30.

### Fifth reconcile (same day, PR #33 copy/gate widening)

Auto-merged without conflict; outputs regenerated. Register rows for this session: SG-24…SG-30.

### PR / deploy result
- PR: https://github.com/karagemop466-tech/Affil2/pull/22 (this branch → main). Merge result and Pages verification are recorded in the follow-up record commit after the merge.
- Superseded/owned-elsewhere work, for the record: analytics collector + measurement surface = PR #16 (open, session bdedd85e); hand-written polish artifacts dropped in favor of generator outputs = see merge log above.

## Session 42617e35 — integration result (recorded after merge)

| Field | Value |
|-------|-------|
| PR | https://github.com/karagemop466-tech/Affil2/pull/22 |
| Merge | merged into `main` 2026-11-20T06:00:14Z as merge commit `175375fa37938143f9c2c945f14c45799310eb55` |
| Pages | Deployed and serving the merged revision — live check of https://karagemop466-tech.github.io/Affil2/guides/first-week-air-fryer.html returns the new guide with disclosure above the fold and sourced product links |
| Gate at merge | `python3 scripts/check_site.py` → ALL CHECKS PASS (31 pages, 5 product records, 40 flags, 18 sources) |
| Register rows shipped | SG-24…SG-30 (incl. required SG-27 nav labels · SG-28 shipped RSS feed · SG-29 Search Console · SG-30 reader capture) |
| Guide shipped | guides/first-week-air-fryer.html (in sitemap + feed) |
| Flagged / open | FLG-001…FLG-040 as published on flagged.html; analytics collector still owned by open PR #16 (not duplicated here) |

### Claim (2026-11-20, `active`)

- Claiming the local-search privacy defect: built-in search terms are currently serialized into request URLs (`?q=`), and `search.html` / `disclosure.html` claim "nothing is sent to a server" while search query text nonetheless reaches the host in the request URL. Fix (T-19, renumbered to avoid clashing with session `3fb8f29e`'s T-18 in PR #26): generated search forms will stop serializing `q`, a session-storage handoff will feed the local results page, and the site copy will state exactly what happens to search words and what measurement does. Scope is `scripts/build_site.py`, `assets/app.js`, `scripts/check_site.py` gate rules and regenerated pages only; register rows and product facts are out of scope. Owner-gated open items (FLG-001/002/003/004/010/028/033) remain untouched. (Earlier T-10 doc pass duplicated work already merged upstream via `main`; those commits were dropped during this rebase.)

### T-19 completion (2026-11-20, session 5ff64069)

- **Fixed:** generated search inputs no longer carry a `name` attribute, so a no-JS GET cannot serialize `q`. `assets/app.js` intercepts `role="search"` submissions, carries the trimmed query in `sessionStorage` (`sn_search_query`, cleared on use), and navigates to the local search page without a query string. The `search` event still records a result count only; query words never enter localStorage events.
- **Copy corrected in the generator:** `search.html` and `disclosure.html` no longer claim "nothing is sent to a server"; the disclosure now states that search words ride session storage, ordinary page requests still reach the GitHub Pages host, and no measured event leaves the device. The `search` event row reads "result count only", and the unsupported "Popular starting points" heading is now "Three places to start".
- **Gate added:** `check_site.py` fails on named inputs inside `role="search"` forms, on `URLSearchParams(location.search)` or `get('q')` query reading in `assets/app.js`, on a missing session-storage handoff or disclosure wording, and on the stale no-server claim. Upstream image-caption, no-invented-weight and pair-view gates are retained alongside these rules.
- **Verification (after rebasing through PRs #22/#33/#36):** generator idempotent across consecutive runs; `python3 scripts/check_site.py` -> `checked 31 pages, 5 product records, 40 flags, 18 sources / ALL CHECKS PASS`; `node --check assets/app.js`; feed.xml and sitemap.xml parse; `git diff --check`. Node VM smoke: built-in search stores whitespace-normalized words in session storage, navigates with an unparameterized URL, hostile query strings render only through value/textContent, matching searches log a numeric result count with no query field, and the one-session handoff clears. No external source pages fetched; no product/source/flag facts changed. Scope stayed inside T-19: the collector proposal (#16) is untouched; the merged polish/content work (#22/#36) is preserved and regenerated on top of.

---

## Session `arena/9f19fe6b-affil2` — deep live verification, collector stack, and platform blueprint (2026-11-20)

Branch `arena/9f19fe6b-affil2`, merged cleanly with `origin/main` (`0b509ab`, preserving PRs #17–#37 including `design-brief.html`, storefront photo cards, two-at-a-time compare, `guides/first-week-air-fryer.html`, privacy-preserving `sessionStorage` search handoff, `SG-17..SG-30`, `Q-15..Q-18`, `FLG-036..FLG-040`, and `S23`).

### Live verification performed

- Re-fetched all five `link.amazon/*` short links: all five resolved cleanly on attempt 1 (`B04G1MEwY -> B0CDY277D3`, `B02NbDxp3 -> B09B7SB46R`, `B00hJ57DV -> B08DKYBTPH`, `B0c8moW59 -> B0DHZTCNR5`, `B0f3GKalj -> B0DZFD6R9Z`). Intermittent redirect instability stays tracked under `FLG-011` and `FLG-012` records the checkpoint-then-reproduced history.
- Audited deep `Product information` tables (`Features & Specs`, `Measurements`, `Item details`, `Warranty & Support`) across all five live `/dp/` listings:
  - Verified P-01 weight `13.3 pounds` and P-03 weight `12.8 pounds` directly from their `Measurements` tables; confirmed P-02, P-04, and P-05 omit item weight (`FLG-022`, `FLG-039`).
  - Confirmed P-02 model `4-00675-02X-VN` (conflict vs earlier `4-00675-02`, `FLG-009`), temperature `75–500 °F`, power `120 volts / 1700 watts`, P-03 power conflict (`1700 W` in Features & Specs vs `1000 W` in About this item, `FLG-017`), P-04 model `HT07` / `572 °F` / `6.5 in` / `Wipe Clean`, and P-05 model `CQ60-3C-Z1-E` / `4.75 in` / warranty conflict (`two-year` vs `3 Year`, `FLG-038`, `FLG-019`).
- Read Amazon Operating Agreement §5, Program Policies (chunks 0–9: Commission Income §2(d)/(e)/(g), Participation Requirements §2(a)/(b), §5 ML restriction, §6(t)/(v)/(w)/(y), IP License §1, §2(e)/(h)/(i)/(k), and §4 Agent Terms), Creators API onboarding (`S20`), PA-API 5 deprecation (`S21`), FTC guidance (`S03`, `S23`), Google outbound links (`S04`), and USDA FSIS temperature/calibration guides (`S22`, `S24`).

### Code, data, and gate additions

- Merged and extended `scripts/build_site.py`: kept `origin/main`'s storefront (`design-brief.html`, captioned `assets/photos/`, `pairCompare`, `guides/first-week-air-fryer.html`, `sources.html` changelog) alongside `platform.html` (`SG-31`), `measurement.html` (`SG-25`), `build_sources()` 4-column table alignment, `normalise()` separation of `observed` vs `intended`, vector schematic gallery in `about.html` (`assets/illustrations/*.svg`), and reconciled `SG-01..SG-32` + `Q-01..Q-20`.
- Hardened `assets/app.js` and added self-hosted collector endpoints: unified DOM-safe `search.html` engine, mobile `.navtoggle` + `Escape`, two-at-a-time `pairCompare` with real product-ID click tracking, `#exportEvents` + RFC-4180 CSV escaping, and schema-validated `send()` transport backed by `data/events.json`, `analytics/server.js`, and `functions/api/collect.js`.
- Hardened `scripts/check_site.py` (added table `thead`/`tbody` column symmetry, verified-weight guard against `data/products.json`, non-orphaned valid SVGs, `og:url` verification, editorial flag checks, `events.json` & `app.js` contract checks alongside `origin/main`'s photo caption & `pairData` checks) and added `tests/test_site.py` + `tests/test_collector.js` wired into `.github/workflows/pages.yml`.

### Gate and tests

- `python3 -B scripts/build_site.py`: `built 33 pages` (idempotent across consecutive runs).
- `python3 -B scripts/check_site.py`: `checked 33 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS`.
- `python3 -B -m unittest discover -s tests -p "test_*.py" -v`: 3 tests OK.
- `node tests/test_collector.js`: `ALL JS COLLECTOR AND CLIENT TESTS PASS`.


## PR + merge result (session bba2deed)

- PR: https://github.com/karagemop466-tech/Affil2/pull/29 — merged via `gh pr merge 29 --merge`, merge commit `1d2ed6e` on `main`, state MERGED.
- Gate at merge: `python3 scripts/check_site.py` ALL CHECKS PASS (36 pages, 5 product records, 40 flags, 19 sources); `python3 tests/test_site.py` OK (page-count expectation updated 33 → 36 for the three added pages: two Holiday 2026 guides + the Verification Log).
- GitHub Pages: `pages-build-deployment` run 44687038495 for merge commit `1d2ed6e` — build 8s ✓, deploy 11s ✓, report ✓. Live: https://karagemop466-tech.github.io/Affil2/ (source = main).
- Flagged items FLG-001..FLG-040 published on https://karagemop466-tech.github.io/Affil2/flagged.html — none block; short-link compliance (FLG-003) remains unresolved and is not claimed invalid.
- Notes: `analytics/server.py` (session bba2deed, Python) and `analytics/server.js` (parallel collector stack with tests) both ship; the live site continues to use whichever the owner deploys, switched in `assets/config.js`. `analytics/data/` is git-ignored (event data must not enter git).

---

## Session `58c6ca4a` — live re-verification pass and status record (2026-11-20 UTC)

**Branch:** `arena/58c6ca4a-affil2` · **Base:** `4025ecc` (main, after PR #38) · **Task:** T-20 (re-verify live listings, reconcile open items, record state). Scope: `COORDINATION.md` only. No product, source, flag or generated-page value was changed.

### Live listing re-read (official Amazon.com pages, fetched 2026-11-20)

| Record | Official listing URL | Title read this session | Matches register title? |
|---|---|---|---|
| P-01 | https://www.amazon.com/dp/B0CDY277D3 | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | Yes |
| P-02 | https://www.amazon.com/dp/B09B7SB46R | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … 24 One-Touch Preset Options … : Home & Kitchen" | Yes (preset count 24 in title; see FLG-021) |
| P-03 | https://www.amazon.com/dp/B08DKYBTPH | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option … : Home & Kitchen" | Yes (450 °F Hi-Fry in title; see FLG-018) |
| P-04 | https://www.amazon.com/dp/B0DHZTCNR5 | "Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy … : Home & Kitchen" | Yes |
| P-05 | https://www.amazon.com/dp/B0DZFD6R9Z | "Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes … Gen3 : Home & Kitchen" | Yes |

Observed on these pages in this read, not written into the register: the buy-box price on each page varies with the page state (for example the P-04 page showed $16.99 and the P-05 page showed a 3-year protection-plan add-on). Prices stay blank per Program Policies §2(b) and FLG-005. The P-01 page also showed a "Sponsored Ad" block for other products; no sponsored item was added to the site.

### Short-link and status checks

- Short links were not re-resolved from this sandbox in this pass; the earlier 2026-11-20 resolution record (above, "Live verification performed") stands unchanged. Intermittent redirect behavior remains under FLG-011 / FLG-012 / FLG-013 / FLG-014.
- `python3 -B scripts/check_site.py` → ALL CHECKS PASS (36 pages, 5 product records, 40 flags, 19 sources).
- `python3 -B -m unittest discover -s tests -p "test_*.py"` → 3 tests OK.
- `node tests/test_collector.js` → ALL JS COLLECTOR AND CLIENT TESTS PASS.
- The GitHub Pages URL is not reachable from this sandbox (outbound is limited to github.com, api.github.com, codeload, npm, PyPI). Live Pages status is therefore not re-confirmed here; the last recorded deploy is run 44687038495 for merge `1d2ed6e`.

### Open PRs from other sessions (not touched by this session)

| PR | Branch | Opened | Note |
|---|---|---|---|
| #16 | `arena/bdedd85e-affil2` | 2026-11-20 05:32Z | Self-hosted analytics endpoint and platform proposal; owner decision pending (FLG-010). |
| #28 | `arena/59ada9df-affil2` | 2026-11-20 05:47Z | Overlapping T-13..T-20 scope. Not merged here. |
| #34 | `arena/82c875a9-affil2` | 2026-11-20 06:00Z | Coordination record for storefront work. Not merged here. |
| #35 | `arena/36170d15-affil2` | 2026-11-20 06:00Z | T-17 title overlaps the already-merged T-17 (PR #20). Not merged here. |

GitHub reported `mergeable: UNKNOWN` for all four. Each belongs to another session; merging any of them would overwrite that session's claim, so this session leaves them for their owners or for the final integration session.

### Still owner-gated (cannot be completed from this sandbox)

- FLG-001 intended ASIN confirmation by the owner.
- FLG-002 tracking-ID activity; FLG-003 short-link compliance status; FLG-004 one Special Link test in the enrolled Associates workflow. These require the owner's Associates account. No account-level access exists in this session.
- FLG-010 / FLG-028 / FLG-033 analytics endpoint deployment and Search Console verification (requires owner accounts).
- FLG-019 commission schedule and FLG-032 research data (require owner-supplied first-party reports).

### Irregularities noted in this pass

- No new listing contradictions beyond those already published (FLG-008, FLG-017, FLG-018, FLG-021, FLG-034).
- The sandbox cannot reach amazon.com directly for scripted checks; the titles above were read through the page-fetch tool and should be re-checked by a human in a browser: https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z

### Task status

T-20 | Live re-verification of the five listings + status reconciliation | done | 58c6ca4a | COORDINATION.md

### T-20 release record (session 58c6ca4a)

- PR: https://github.com/karagemop466-tech/Affil2/pull/39 — merged via `gh pr merge --merge`, merge commit `66ccda9`, state MERGED.
- `Verify site` run on `66ccda9` → success. Pages deploy for `66ccda9` ran as `pages build and deployment`; see the Actions run list for its final conclusion.

---

## Session `cb967199` — open-PR reconciliation and independent publication review

### Claim (2026-11-20, active)

- Claiming a documentation-only integration review: reconcile open PRs against the current `main`, record whether each contains unique work or is superseded, and log a concrete line-by-line publication finding if one is found. Scope: `COORDINATION.md` only. Do not edit generator/data/site outputs in this pass unless the review identifies a release-blocking defect; if so, record the request and keep scope isolated until safely claimed. Existing account-gated items remain unresolved and are not to be guessed.

### Scope amendment (2026-11-20, session `cb967199`)

Line-by-line review of the deployed pages found two publication defects, both verified against the live site before touching any file:

1. `index.html` main content carries a third dashboard surface — a "Working on this site?" panel linking Decision Center / Open Questions / Flagged / Sources — beyond the masthead Records group and the footer Records line. That violates the shipped rule: lead with the products; every dashboard surface reachable from the footer and a single navigation group.
2. The P-03 front-page card prints the item weight inside the Capacity chip ("Capacity: 8 quarts (12.8 lb)"). The 12.8 lb figure is verified (S12 Measurements table), but a weight belongs in the product spec table, which already carries it; the chip mixes two fields.

Scope expanded to fix both: `scripts/build_site.py` (front-page panel section only), `data/products.json` (P-03 `card` chip wording only), regenerated pages, gate + tests rerun. No product fact, source, or flag changes; account-gated items (FLG-001/002/003/004/010/028/033) remain untouched. Also claiming the port of open PR #34's documentation block into this file (see next commit) since that branch has no merge base with the shallow clone and cannot be git-merged locally.

### Port of open PR #34 (2026-11-20, session `cb967199`)

PR #34 (`arena/82c875a9-affil2`, commit `d9bba276`) is a documentation-only record whose branch has no
merge base with this shallow clone, so it cannot be git-merged locally; its block is ported verbatim
below instead. The three merge-commit hashes it cites were verified to exist on `main` via the GitHub
API before porting: `63cb1fb` → PR #30, `c916fce` → PR #32, `e948aae` → PR #33. PR #34 is closed as
integrated once this lands.

### Publication record (session `82c875a9`)

| PR | Title | Result |
|----|-------|--------|
| [#30](https://github.com/karagemop466-tech/Affil2/pull/30) | Storefront rebuild, working search and pair compare, register re-verified against live listings | merged → `63cb1fb`; Pages **success**, Verify site **success** on that SHA |
| [#32](https://github.com/karagemop466-tech/Affil2/pull/32) | Remove the last unsupported weight claim, gate against any lb figure in prose | merged → `c916fce`; live page confirmed |
| [#33](https://github.com/karagemop466-tech/Affil2/pull/33) | P-02 lede stops promising weight content the register cannot supply | merged → `e948aae`; live page confirmed |

Live: https://karagemop466-tech.github.io/Affil2/ — all 30 pages, plus `compare.html` with the working
pair view, checked on the deployed URL rather than the local build.

**Lesson repeated, and worth writing down.** PR #30 passed the gate, deployed green, and still shipped
one wrong number: `data/editorial.json` carried "26.5 lb" for the Emeril, and that string is rendered
into the compare table's catch column and into a product FAQ. I found it by reading the deployed
`compare.html`, not by running `check_site.py` twice. The gate now fails on any `N lb/lbs/pound` figure
in page prose, and on any promise of weight information, but the general point stands: the gate proves
markup and sourcing rules, not that the sentence is true. Read the live page after every deploy.

**Renumbering note for the next session.** `main` gained the Design & Traffic Brief at SG-17 while this
branch was open. This branch's six proposals are therefore SG-18 to SG-23, and its two shipped items are
SG-20 (change log) and SG-21 (pair compare). Do not re-use SG-17.

### Review result, fixes, and open-PR dispositions (2026-11-20, session `cb967199`)

Gate truth on the final base (`origin/main` `4025ecc` = PR #29 + #38 merged, plus this session's commits):
`python3 scripts/build_site.py` → 36 pages, idempotent across consecutive runs; `python3 scripts/check_site.py`
→ checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS; `python3 -m unittest discover`
→ 3 tests OK; `node tests/test_collector.js` → ALL JS COLLECTOR AND CLIENT TESTS PASS.

Review method: fetched the deployed landing page and the P-01 product page live, read the PR bodies and
changed-file lists of every open PR against what is actually on `main`, and re-ran the gate. Sources this
session: the deployed pages themselves, the live Amazon listing B0CDY277D3 (title corroborates S10), and
the GitHub API for PR/merge-commit facts. No product fact, source, or flag changed.

Fixes shipped (each verified against the deployed site first, then fixed at generator/data level, rebuilt, gated):

1. **Front page led with a dashboard panel.** `index.html` main content carried a third dashboard surface
   ("Working on this site?") beyond the masthead Records group and the footer Records line. Removed in
   `scripts/build_site.py`; dashboard surfaces remain reachable from the masthead Records group (the single
   navigation group) and the footer — matches shipped proposal SG-01.
2. **P-03 capacity chip mixed two fields.** The front-page card printed "Capacity: 8 quarts (12.8 lb)".
   The 12.8 lb figure is verified (S12, Measurements table) but belongs in the spec table, which already
   carries it. Chip now reads "8 quarts (single basket)" (`data/products.json`). No fact changed; the
   verified weight stays on the P-03 specification table and QA row.

Open-PR reconciliation (closes executed after this PR merges):

| PR | Disposition | Rationale |
|---|---|---|
| #16 | close as superseded | Collector endpoints (`analytics/server.js`, `functions/api/collect.js`), the five-event schema, `measurement.html`, the platform concept and collector tests all shipped on `main` in integrated form via PR #31. Unique leftovers (`assets/js/collect.js`, `tests/collector.test.js`) are replaced by `assets/app.js` `send()` and `tests/test_collector.js`. The owner decision stays open (SG-25, FLG-010, Q-08) and is untouched. |
| #28 | close as superseded | Shop-first front page, verified specs, review workflow, flag-reference and weight gates all shipped on `main` in later integrated form (PRs #30/#32/#33/#31). Unique content not on `main`: four guide topics — counter-depth, quarts-vs-litres, usda-temperature-chart, wattage-and-circuits — recorded here as the guide backlog for the next content session, to be regenerated natively in `build_site.py` GUIDES so index/sitemap/feed/search stay in sync. |
| #34 | ported; close as integrated | Block ported verbatim above; branch not locally mergeable (no merge base in this shallow clone). |
| #35 | close as superseded | Identity separation (intended/observed fields on every product page), source-linked spec rows, SG-27..SG-31, five-event coverage and the strengthened gate are all verified present on `main` this session by reading the deployed product page and the gate output. Unique leftover (`scripts/analytics_server.py`) duplicates `analytics/server.js`/`server.py`. |

Account-gated open items (FLG-001/002/003/004/010/028/033, SG-07/SG-25/SG-29/SG-31, Q-01..Q-04) remain
untouched and unguessed.

### Integration result (2026-11-20, session `cb967199`)

| Field | Value |
|-------|-------|
| PR | https://github.com/karagemop466-tech/Affil2/pull/41 |
| Merge | merged into `main` as merge commit `4dd7cdd` (no approval wait, per standing instruction) |
| Verify site | run 44687657922 on `4dd7cdd` → success |
| GitHub Pages | `pages build and deployment` run 44687657657 → success; site live at https://karagemop466-tech.github.io/Affil2/ |
| Live verification | deployed landing page re-fetched with a cache-buster after deploy: "Working on this site?" panel absent from main content (dashboard surfaces only in the masthead Records group + footer), P-03 chip reads "Capacity: 8 quarts (single basket)", hero facts show 11 buying guides, disclosure strip above the fold, sponsored labels intact. A first uncached fetch minutes after deploy served the pre-deploy copy from CDN cache — noted so future sessions use a cache-buster when checking a just-deployed page. |
| Merge conflicts during the pass | three rounds of `git pull --rebase origin main` while parallel sessions merged PRs #29/#38/#39/#40; all resolved in COORDINATION.md by keeping every session's record block once (nothing discarded). |
| PR dispositions executed | #16 closed superseded; #28 closed superseded (four guide topics preserved as backlog); #34 closed integrated (block ported verbatim); #35 closed superseded. PR #29 was merged by its own session during this pass. Each close comment states where the work lives on main. |
| Gate at merge | 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS; 3 Python tests OK; JS collector tests pass; generator idempotent. |
| Not touched | account-gated items FLG-001/002/003/004/010/028/033, SG-07/SG-25/SG-29/SG-31, Q-01..Q-04; no product fact, source, or flag changed. |

---

## Session `c449a2ad` — T-21 claim (2026-11-20 UTC)

Branch `arena/c449a2ad-affil2`, base `4025ecc` (main, after PR #38). Scope is deliberately read-only with respect to shared outputs.

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-21 | Requirements traceability register: every requirement in the current brief mapped to status, evidence, owning claim and the owner action it needs; plus a read-only log of intent/observed field irregularities | in progress | c449a2ad | `REQUIREMENTS-TRACE.md` (new), `COORDINATION.md` (append only) |

Not claimed here, and not edited: the open PRs #28 (59ada9df: T-13..T-20), #34 (82c875a9), #35 (36170d15: T-17 identity fields), #16 (bdedd85e: analytics T-13/T-14). Their file scopes are left alone. Requests for those owners are logged below rather than applied.

Requests logged for owners (not applied in this session):
- For `36170d15` (identity fields): `data/products.json` sets `asin` equal to the observed redirect target for P-01..P-05 (for example P-01 `asin: B0CDY277D3`, `observed: B0CDY277D3`). FLG-001 says the intended field stays blank and the observed field stays separate. The two should not hold the same value.
- For `59ada9df` (verification pass T-18): the re-fetch should cover the S01/S02 "Updated" dates. The Operating Agreement page currently reads "Updated: October 15, 2025" at https://affiliate-program.amazon.com/help/operating/agreement (checked 2026-11-20 by c449a2ad). Compare with the date in `data/sources.json`.
- Mergeability: PRs #16, #28, #34 and #35 all report `DIRTY` (merge conflicts with main at 4025ecc). The final integration session needs to rebase them in order or retire the duplicates.

### T-21 completion (session `c449a2ad`, 2026-11-20 UTC)

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-21 | Requirements traceability register + read-only irregularity log | done | c449a2ad | `REQUIREMENTS-TRACE.md` (new), `COORDINATION.md` (append only) |

- **Register:** `REQUIREMENTS-TRACE.md` maps 36 requirements from the current brief to status, evidence on `main`, official source, and owner action. Owner-only items are listed separately (section 2).
- **Live official sources read this pass:** Associates Operating Agreement §4 and §5 (https://affiliate-program.amazon.com/help/operating/agreement). §5 wording matches the site's disclosure sentence verbatim. OPM Federal Holidays 2026 (https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/): Thanksgiving Day is Thursday, November 26, 2026. Amazon listing B0CDY277D3 (https://www.amazon.com/dp/B0CDY277D3): page loads; title matches the register.
- **Local verification:** `python3 scripts/build_site.py` leaves every tracked file unchanged (idempotent). `python3 scripts/check_site.py` → `checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS`. Python and Node test suites pass.
- **Corrections made while verifying:** three flag references in the first draft pointed at the wrong flags. They now point at SG-29 (Search Console), SG-26 (ledger) and FLG-004 (Special Link test). One source link was not verified and was removed; that gap is logged as I-7.
- **Irregularities (not blocking; detail in `REQUIREMENTS-TRACE.md` §3):** I-1 `asin` equals `observed` for P-01..P-05; I-2 Black Friday date unsourced; I-3 gate checks source links on spec rows only; I-4 gate checks `https` only, not official domains; I-5 Operating Agreement "Updated" date not recorded in `sources.json`; I-6 open PRs #16, #28, #34, #35 report DIRTY; I-7 formal ASIN definition not yet linked to an official page; I-8 stale flag numbers in older COORDINATION entries.
- **Requests to owners (logged, not applied):**
  - `36170d15` (identity fields): I-1.
  - `59ada9df` (gate and sources, T-19/T-18): I-3, I-4, I-5.
  - Final integration session: I-2 (cite or label Black Friday), I-6 (rebase or retire DIRTY PRs), I-7 (locate the official ASIN definition), I-8 (refresh stale flag references).
- **Not done here, and why:** no listing re-read (done by `58c6ca4a`, PR #39). No change to shared data, generator, nav, or site pages; those are claimed by other sessions. No Associates, Search Console or analytics access exists in this sandbox.

### T-21 release record (session `c449a2ad`)

- PR: https://github.com/karagemop466-tech/Affil2/pull/43. Merged with `gh pr merge 43 --merge` at 2026-11-20T06:28:23Z as merge commit `22dcda1`, state MERGED.
- Checks on the PR: "Regenerate and gate" passed. On `22dcda1`, "Verify site" completed `success`, and "pages build and deployment" completed `success`. Pages status: `built`.
- Live: https://karagemop466-tech.github.io/Affil2/REQUIREMENTS-TRACE.md serves the register. Owner items and irregularities I-1..I-8 are as recorded above.
- Nothing from another session was overwritten. COORDINATION.md was merged from `main`, and this record was appended to it.
- Conflict log (`c449a2ad`): `main` moved three times during T-21 (PRs #39–#42). COORDINATION.md conflicted on each rebase or merge. Each time, main's full file was kept and only this session's block was re-appended. Nothing from another session was discarded. The session's own branch was force-pushed once, with a lease, after a rebase rewrote its unmerged claim commit. Records: PR #43 (`22dcda1`) and PR #44 (`6e4077b`).

---

## Claim — session `35973829` (2026-11-20, `active`)

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-26 | Final integration: land PR #46 (T-22 re-verification addendum) on top of current main, re-run all gates + broken-link check, PR → main, merge, Pages confirmation, record (renumbered twice: c449a2ad took T-21, 578ca10d took T-22, b6b809da took T-23, 0acc86ad took T-24/T-25 — see collision log) | in progress | 35973829 | `COORDINATION.md`, and via merge only the PR #46 scope (`data/verification.json` additive, `scripts/build_site.py`, `verification.html` regenerated) |

- Branch `arena/35973829-affil2`, base `c8b8926` (main, after PR #31), integrating forward through `f1e84b6` (main, after PR #45).
- Baseline at claim time: `build_site.py` + `check_site.py` pass on 33 pages; Python (3) and Node collector tests pass; feed/sitemap XML parse; Pages `main` built with green Verify site + deploy runs.
- Open-PR state at claim time: #16/#28/#34/#35 closed as superseded/integrated (session cb967199, PR #41); #29 merged (PR #38); **#46 open but CONFLICTING** (session 578ca10d, T-22) — this session lands it.
- No other session's claim is taken over; PR #46's branch content is merged, not rewritten.
## Session `578ca10d` — final integration pass: line-by-line re-verification, verification-log addendum, PR + Pages

Branch `arena/578ca10d-affil2`, rebased onto `origin/main` (`2de7bdd`, after PRs #38–#40) before opening the PR. This session is the **final integration pass**: it re-verifies the combined data line by line, confirms the site builds with no broken links, and publishes the result.

### Claim (2026-11-20, `active`)

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-22 | Final integration: line-by-line re-verification + verification-log addendum + PR/merge/Pages record (renumbered from T-21 after c449a2ad claimed T-21 for a requirements-traceability register; see conflict log below) | done | 578ca10d | `data/verification.json` (additive), `scripts/build_site.py` (generator), `verification.html` (regenerated), `COORDINATION.md` |

Scope note: `data/products.json`, `data/sources.json`, `data/flags.json` and `data/editorial.json` are **read-only** for this session. No product value, source record or flag was changed — the re-verification found no inaccuracies, so the register stands. Open PRs #16 / #28 / #34 / #35 (other sessions) were not touched or duplicated.

### Task-ID collision and conflict resolution (logged per protocol)

- 2026-11-20 `578ca10d`: chose T-21 for this final-integration pass before checking the board for
  later numbers. While this session worked, session `c449a2ad` claimed T-21 for a requirements-
  traceability register (`REQUIREMENTS-TRACE.md`) and merged it via PRs #42/#43. The two T-21
  definitions do not touch the same files: c449a2ad edited `REQUIREMENTS-TRACE.md` + `COORDINATION.md`
  only; this session edits `data/verification.json`, `scripts/build_site.py`, `verification.html`
  and `COORDINATION.md`.
- Resolution: c449a2ad's record and work are kept intact; this session's task was renumbered to
  **T-22**. The `git pull --rebase` conflict in `COORDINATION.md` was resolved by taking main's
  version of the file (preserving the cb967199 and c449a2ad records) and re-appending this session's
  record unchanged except for the renumbering. No other session's work was discarded.

### Independent line-by-line re-verification (2026-11-20, official sources only)

| Item | Official source checked | Result |
|------|------------------------|--------|
| P-01 B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Page title matches the register exactly; breadcrumb Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers. |
| P-02 B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Title matches the register exactly, incl. 24 One-Touch Preset Options (FLG-021 as published). |
| P-03 B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Title matches the register exactly, incl. 450 °F Hi-Fry Option (FLG-018 as published). |
| P-04 B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Title matches the register exactly; breadcrumb … › Thermometers & Timers › Meat. |
| P-05 B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Title matches the register exactly (reached via short-link resolution); breadcrumb … › Thermometers & Timers › Meat. |
| Short link B04G1MEwY (P-01) | https://link.amazon/B04G1MEwY | 2 attempts → Amazon homepage both times. Intermittent redirect instability (FLG-011); confirmed target B0CDY277D3 stands. Not claimed invalid (FLG-003). |
| Short link B02NbDxp3 (P-02) | https://link.amazon/B02NbDxp3 | 2 attempts → homepage both times. FLG-011; target B09B7SB46R stands. Not claimed invalid. |
| Short link B00hJ57DV (P-03) | https://link.amazon/B00hJ57DV | 2 attempts → homepage both times. FLG-011; target B08DKYBTPH stands. Not claimed invalid. |
| Short link B0c8moW59 (P-04) | https://link.amazon/B0c8moW59 | 2 attempts → homepage both times. Consistent with FLG-011 / FLG-012; the earlier resolving fetch (B0DHZTCNR5) stands. Not claimed invalid. |
| Short link B0f3GKalj (P-05) | https://link.amazon/B0f3GKalj | Resolved cleanly to /dp/B0DZFD6R9Z on the first attempt — confirms the observed target. |
| S03 FTC Endorsement Guides FAQ | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | Live; material connection must be disclosed clearly and conspicuously. |
| S04 Google qualify outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Live (last updated 2025-12-10); rel="sponsored" for paid links; multiple rel values allowed. |
| S22 USDA FSIS safe temperature chart | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart | Live (last updated Apr 14, 2025); all values match `data/usda-temperatures.json`. |
| S01 Associates Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Live; "Updated: October 15, 2025". §5 is the basis of the site's disclosure statement. |
| S02 Associates Program Policies | https://affiliate-program.amazon.com/help/operating/policies | Live; "Updated: April 14, 2026". Basis of the no-price / no-ratings gate rules. |
| Live deployed pages | https://karagemop466-tech.github.io/Affil2/ | index.html, a product page and feed.xml fetched live — disclosure above the fold, sponsored tagged links, full 11-item feed. No broken links found on the checked pages. |

**No register corrections were required** — every title and policy claim matched the published register. The only behavioral observation is the short-link redirect instability, which corroborates (does not contradict) the existing FLG-011 / FLG-012 records; no claim that the short links are invalid (FLG-003 stands).

### What changed (additive only)

- `data/verification.json`: new top-level `rechecks` array (R-01…R-16), one row per check above, each with its official source link; new `recheck_session` / `recheck_date` / `recheck_note` fields. **No existing row, value or status was modified** — checked field by field against the pre-edit file.
- `scripts/build_site.py`: `build_verification()` now renders a "Re-verification addendum" table (ID / what was checked / official source / result) below the corrections table, and the page kicker lists this session. The addendum block is skipped if `rechecks` is absent, so the generator remains backward-compatible.
- `verification.html`: regenerated by the generator (no hand-editing).
- `COORDINATION.md`: this record.

### Gate and tests

- `python3 -B scripts/build_site.py` → `built 36 pages`, idempotent across consecutive runs.
- `python3 -B scripts/check_site.py` → `checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS`.
- `python3 -B -m unittest discover -s tests -p "test_*.py"` → 3 tests OK.
- `node tests/test_collector.js` → ALL JS COLLECTOR AND CLIENT TESTS PASS.
- `git diff --check` → clean.

### Still owner-gated (unchanged; none blocks publication)

FLG-001 intended ASINs · FLG-002 tracking-ID activity · FLG-003 short-link compliance status · FLG-004 Special Link test · FLG-010 analytics endpoint · FLG-019 commission schedule · FLG-028 Search Console · FLG-032 research data · FLG-033 named author. All are published on `flagged.html` with their source links.

### T-22 release record (session 578ca10d)

- PR: (recorded after merge below)
- GitHub Pages: (recorded after merge below)

### T-26 verification record (session `35973829`, 2026-11-20 UTC)

Scope executed: merged `origin/main` (`f1e84b6`, after PR #45) and PR #46's branch (`arena/578ca10d-affil2`, T-22 re-verification addendum) into `arena/35973829-affil2`. Two COORDINATION.md conflicts resolved by keeping every session's record block once (nothing discarded). No product, source, flag or editorial value was authored or altered by this session.

| Check | Result |
|---|---|
| `python3 -B scripts/build_site.py` ×2 | `built 36 pages`, idempotent, working tree clean after both runs |
| `python3 -B scripts/check_site.py` | `checked 36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS` |
| `python3 -B -m unittest discover -s tests -p "test_*.py"` | 3 tests OK |
| `node tests/test_collector.js` | ALL JS COLLECTOR AND CLIENT TESTS PASS |
| `node --check assets/app.js` | clean |
| feed.xml / sitemap.xml | parse as valid XML; sitemap lists 36 pages; feed carries 11 items |
| Independent internal-link audit (all 36 pages, 2,268 hrefs) | 0 broken internal links, 0 missing assets |
| Independent disclosure audit | disclosure strip present above `<main>` on all 36 pages (plus footer copy) |
| Independent `rel="sponsored"` audit | 0 amazon.com anchors missing `sponsored` |
| Spec-table source-link audit (5 product pages) | every `Field / Value / Source` row carries a source link; blanks marked `unverified`/`not stated` |
| USDA doneness tables (P-04, P-05) | each cites https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart (S22) |
| PR #46 addendum rendered | `verification.html` carries "Re-verification addendum" with R-01…R-16; `data/verification.json` rechecks = 16, every row has an `https://` source URL |

Sources fetched live by this session (official only):

| Source | Result |
|---|---|
| https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links (S04) | Live; `rel="sponsored"` for paid links; multiple rel values allowed; last updated 2025-12-10 — matches register |
| https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking (S03) | Live; endorser–marketer connection "should be disclosed clearly and conspicuously" — matches register |
| https://www.amazon.com/dp/B0CDY277D3 (P-01) | Page title matches `data/products.json` verbatim; breadcrumb Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers |
| https://www.amazon.com/dp/B0DHZTCNR5 (P-04) | Page title matches `data/products.json` verbatim; breadcrumb … › Thermometers & Timers › Meat |

Irregularities: none new found by this pass. Owner-gated items unchanged (FLG-001/002/003/004/010/019/028/032/033); all 40 flags remain published on `flagged.html` and none blocks merge. Minor observation, not flagged: `REQUIREMENTS-TRACE.md` (T-21 doc) is served on Pages but is not an HTML page and is not listed in `sitemap.xml` — consistent with the gate's page definition.

### T-26 status

in progress → PR opened and merged; Pages confirmation and PR link recorded in the follow-up block below.
---

## Session `arena/b6b809da-affil2` — T-23 claim: storefront conversion, asset hygiene, and a decision-path section (2026-11-20)

**Branch:** `arena/b6b809da-affil2` (platform-bound; this is the only branch this session may write to).
**Base:** rebased onto `origin/main` `4dd7cdd` (PR #41) at the start of this session; gate green before any edit
(`36 pages, 5 product records, 40 flags, 19 sources — ALL CHECKS PASS`, 3 Python tests OK, Node collector tests PASS).

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-23 | Storefront conversion + asset hygiene + decision-path section (renumbered from T-21: that number was claimed by c449a2ad for the requirements-traceability register while this session worked) | in progress | b6b809da | `scripts/build_site.py`, `scripts/check_site.py`, `scripts/seasonal_guides.py`, `assets/style.css`, `data/flags.json` (append only), `data/editorial.json` (annotations only), regenerated HTML/`sitemap.xml`/`feed.xml`, `COORDINATION.md`, removal of unreferenced duplicate image files under `assets/` |

Scope note: `data/products.json`, `data/sources.json` are **read-only** for this session — no product
fact, listing value or source is changed, and no new claim about Amazon, FTC, Google or USDA policy is
made. `data/flags.json` is appended to only. The workflow file, `analytics/`, `functions/` and the
tests are not touched. Open owner-gated items (FLG-001/002/003/004/010/028/033) stay untouched.

**Constraint on verification this session, stated up front.** This sandbox can only reach
`github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org` and
`files.pythonhosted.org`. Every other host — `amazon.com`, `affiliate-program.amazon.com`, `ftc.gov`,
`developers.google.com`, `fsis.usda.gov` — fails TLS from here. **No live source was re-fetched in this
session.** Consequently this session asserts **no new product, listing or policy fact**, does not
re-verify any register value, and records no "verified" status for anything it did not read. Work is
limited to markup, styling, generated navigation, gate rules, and the removal of duplication that can
be proved from the repository itself. Register values stand on the earlier sessions' dated reads
(S10–S19, S01–S04, S20–S24); that their text was not re-read today is itself recorded below.

### T-23 completion (session `b6b809da`, 2026-11-20)

Renumbered from T-21: session `c449a2ad` claimed T-21 (requirements traceability, `REQUIREMENTS-TRACE.md`)
and session `578ca10d` then used T-22 for the final-integration addendum, both while this session worked.
Those numbers were taken; this session's task is T-23. No other session's work was edited.

**What shipped**

| Area | Change |
|---|---|
| Stylesheet integrity | `assets/style.css` line 601 opened `.pdp-art img{` and never closed it, so the `@media(max-width:1000px)` rule after it was parsed as declarations and dropped. Fixed, and the gate now fails on an unbalanced stylesheet or an unclosed `@media` block. |
| Missing styles | The generator emits `.hero`, `.hero-photo`, `.hero-copy`, `.hero-facts`, `.aisle-photo`, `.pdp-photo`; the November layer renamed the hero to `.cover` and shipped no rule for any of them. Rules added (dark-green cover card with cream type), and the gate now fails on any class the generator emits that has no rule. |
| Front page | A four-way "start where you actually are" router sits directly under the hero and above the category directory. It answers "which of these am I?" before asking the reader to browse. Gated. |
| Guides | Every guide now ends on *If this guide decided it for you*: one line per relevant product (choose-it-if + the caveat) and one tagged button. Section headings carry generated step markers; the hand-typed "1." prefixes were removed so the number is not printed twice. |
| Product pages | Each product page links to the guides that discuss it (previously there was no product→guide link at all). Gated in both directions. |
| Link semantics | FTC, Google, USDA and Amazon policy/creators-API citations were carrying `rel="sponsored nofollow"`, which marks them as paid placements. Only `amazon.com/dp/` listings are now sponsored; citations use `rel="noopener noreferrer"`. Gated. |
| Dead files | Six unreferenced images removed (`assets/feature.jpg`, `basket.jpg`, `probe.jpg`, `assets/img/cat-air-fryers.jpg`, `cat-thermometers.jpg`, `hero-kitchen.jpg` — the last three duplicated a file of the same name under `assets/photos/` at a different size). Gated: an image file nothing references now fails the build. |
| Stale counts | SG-02 said "ten guides … include all ten" against eleven published; the count is now derived from `GUIDES`. README and the executive summary were refreshed to 46 flags / current page count. |

**What was verified, and what could not be**

Reached from this sandbox: GitHub API and the repository itself. Not reached: `amazon.com`,
`affiliate-program.amazon.com`, `ftc.gov`, `developers.google.com`, `fsis.usda.gov` — all failed at TLS.
So **no listing, policy page or temperature chart was re-read in this session**, no register value was
changed, and no value is newly marked verified. Every fact on the site still rests on the dated reads
recorded against S01–S24 by earlier sessions. Published as **FLG-045** with the same wording on
`flagged.html`.

Verified by execution instead: `scripts/build_site.py` → 36 pages, idempotent across consecutive runs;
`scripts/check_site.py` → `checked 36 pages, 5 product records, 46 flags, 19 sources — ALL CHECKS PASS`
(including the 8 new rules); `python3 -m unittest discover` → 3 tests OK; `node tests/test_collector.js`
→ ALL JS COLLECTOR AND CLIENT TESTS PASS; a full internal link crawl of all 36 pages → 0 broken links;
HTTP 200 for home, shop, compare, guides, a guide, a product page, flagged, suggestions, questions,
sources, every dashboard page, the stylesheet and the images; disclosure confirmed above `<main>` on the
served homepage; `git diff --check` clean.

**New flags published (append-only; FLG-001–FLG-040 untouched, verified field by field)**

FLG-041 unclosed CSS rule · FLG-042 policy citations mislabelled `rel=sponsored` · FLG-043 six dead image
files · FLG-044 stale "ten guides" count · FLG-045 no source re-read in this pass (the honest limit) ·
FLG-046 the masthead name and volume line are editorial devices, not an owned brand.

**Conflict log.** `git pull --rebase` conflicted in `COORDINATION.md` (main gained three session records
and a `REQUIREMENTS-TRACE.md` while this session worked). Resolved by keeping main's entire file and
re-appending only this session's block — no other session's record was discarded. The branch was force-pushed
once with `--force-with-lease` after that rebase, on this branch only.


### T-23 release record

| Field | Value |
|---|---|
| PR | https://github.com/karagemop466-tech/Affil2/pull/48 |
| CI before merge | `Verify site` run 44688719463 on `arena/b6b809da-affil2` — **success** |
| Merge | `gh pr merge 48 --merge` — state **MERGED**, 2026-11-20T06:34:38Z, merge commit `4faab7903c73adee7cac51a1df07948f56ac0e34` |
| Post-merge gate | `Verify site` run 44688784940 on `main` — **success** |
| Pages | `pages build and deployment` run 44688783949 — **success**; GitHub API reports `status: built`, `build_type: legacy`, `html_url: https://karagemop466-tech.github.io/Affil2/` |
| Live page check | **Not performed from this sandbox.** `karagemop466-tech.github.io` is not on this environment's reachable-host list and the fetch failed at TLS (`SSL_ERROR_SYSCALL`). Deployment success and the Pages `built` status are confirmed through the GitHub API; the rendered-page read the board's own lesson asks for must be done from a browser. |

Honest limit, repeated: the deploy is confirmed by the GitHub API, not by fetching the deployed HTML from
here. The next session with network access should open the live homepage, one guide and `flagged.html`
with a cache-busting query string and confirm the router, the guide product line and FLG-041…FLG-046 render.

## Session `arena/0acc86ad-affil2` — claim (2026-11-20; T-IDs renumbered T-23..T-25 upstream)

Branch `arena/0acc86ad-affil2`, base `66ccda9` (main, after PR #39). Session ID `0acc86ad`.

**Why.** The owner's brief for this session is a *voice* brief, not a data brief: "Make it read like a shop, not an audit." The site's factual spine is already verified and gated; what remains is that buyer-facing pages leak production artifacts into the copy — "chunk 7", inline `FLG-0xx` IDs, "Product-intent confirmation record", "Specifications, line by line". A shopper should never see the newsroom.

**Claimed (non-overlapping).**
- T-23 — voice pass inside `scripts/build_site.py` render functions + `assets/style.css` additions + `data/editorial.json` copy; regenerated HTML. Every published fact, source link, disclosure placement, sponsored marking and gate rule is preserved; only the reader-facing wording and layout change.
- T-24 — `findability.txt` at the repo root and the generator/check rules that keep robots, sitemap and feed consistent with it.
- T-25 — a dated live re-verification record of the five listings' *published* spec values and the policy sources, appended as new evidence; no existing flag is deleted or downgraded.

**Not claimed / untouched.** `data/flags.json` numbering and existing entries, `data/products.json` field values (unless live verification contradicts them, in which case the conflict is logged as a new flag and the value is left as published with both figures), the open collector work in PR #16, and every owner-gated item (FLG-001/002/003/004/010/028/033). Anything another session claimed first is theirs; I will log a request instead of editing.

**Test plan.** `python3 scripts/build_site.py` (idempotent), `python3 scripts/check_site.py`, `python3 -m unittest discover -s tests`, `node tests/test_collector.js`, plus a browser-level read of the three highest-traffic pages (home, a category page, a product page) to confirm no internal token reaches a reader.

## Session `arena/0acc86ad-affil2` — completion record (2026-11-20)

Branch `arena/0acc86ad-affil2`, based on `66ccda9`. Three tasks claimed at the start of the session (originally claimed as T-20..T-22; renumbered to T-23..T-25 because session 58c6ca4a already used T-20 for its own verification pass — the IDs, not the work, collided):
each committed and pushed separately; scope stayed inside the claim.

### T-23 — shop voice on every buyer page (done)

**Problem found.** The facts were right; the voice was a newsroom's. Measured before the change:
64 crawl-chunk citations ("chunk 7"), 305 occurrences of bare `FLG-0xx` ticket numbers across 36
files, a "Product-intent confirmation record" heading on all five product pages, and a
"Specifications, line by line" table heading.

**What changed (generator, not hand-edited HTML).**
- `go_clean()` in `scripts/build_site.py` strips crawl-chunk citations and flag IDs from every
  string that passes through `esc()`. Internal records are untouched; `flagged.html` is generated
  from `data/flags.json` and never passes through it, so every flag is still published in full.
- `source_note()` turns "Stated in: About this item & Product information — Features & Specs
  (chunks 4 & 7)" into "Read from the listing bullets on 2026-11-20", with a link to the source
  register. No value changed.
- `ledger_block()` replaces the intent record with a shopper-facing table that keeps all five
  required fields visible and separate: intended ASIN, observed redirect target, Special Link,
  confirmation date, Associates test status.
- `deals_block()` adds a "What comes with it" card (box contents, care, warranty) quoted from the
  listing's own fields.
- `card()` gains shop tags (`Best for two cooks`, `Two baskets`) and a "Why we picked it" line per
  product; "Best for"/"The catch" became "Buy it if"/"Skip it if".
- Reader-facing language in `data/products.json` and `data/editorial.json` rewritten where it
  carried citations. Two FAQ answers were rewritten after the citation strip exposed that they no
  longer named their own conflict — the gate caught this, which is the gate working.
- `how-we-choose`, `about`, `disclosure` and the search index were swept too.

**Verification.** `build_site.py` idempotent (36 pages); `check_site.py` ALL CHECKS PASS (36 pages,
5 product records, 44 flags, 19 sources); 3 Python tests OK; `node tests/test_collector.js` PASS;
`node --check assets/app.js` OK. Zero `chunk` citations and zero bare flag IDs remain on all 25
reader-facing pages (`grep` verified, and now enforced by the gate).

### T-24 — one indexable site with a stated reason to rank (done)

- `findability.txt` generated at the site root: canonical home, purpose, editorial policy
  (authorship, review process, no hands-on testing, paid-link marking, corrections), the 24
  reader-facing pages separately from the 12 project records, sitemap, feed, citation form, and
  known limits. `robots.txt` points at it.
- Sitemap deliberately still submits all 36 pages: the gate and an existing test require full
  coverage, and a half-submitted site is worse than an honest single site. The split lives in
  `findability.txt` and the choice is recorded as **Q-22** for the owner.
- Gate additions: all pages in `sitemap.xml` must appear in `findability.txt`; reader pages may not
  contain a chunk citation or a flag ID. CI now also fails on drift in `findability.txt`.

### T-25 — independent live re-verification (done)

All five official listings fetched live this session and re-read without reusing earlier notes.
33 field rows recorded in `data/verification-2026-11-20-live.json` and published as an
"Independent live pass" section on `verification.html`.

| Source | Result |
|---|---|
| `/dp/B0CDY277D3` | dimensions, 200–450 °F, 120 V/1700 W, 1-yr, cETL, capacity 6 L vs 6 qt — confirmed |
| `/dp/B09B7SB46R` | 16.9×15.8×14.8 in, 24 vs 25 presets, 24.6 L vs 26 qt — confirmed |
| `/dp/B08DKYBTPH` | 12.75×13.5×10 in, 8 qt, 200–400 °F vs 450 °F Hi-Fry, 1000 W vs 1700 W, 4 presets — confirmed |
| `/dp/B0DHZTCNR5` | ±0.5 °F, NIST/NSF as a listing field, 1 s, battery + calibration certificate, wipe clean — confirmed |
| `/dp/B0DZFD6R9Z` | 50 h, 1000 °F, 3 probes + hub, Bluetooth/Wi-Fi, 2-yr vs 3-yr — confirmed |
| USDA FSIS temperature chart | re-read; page states last updated 2025-04-14; 145 °F + 3-min rest, 160 °F, 165 °F, 165 °F, 145 °F confirmed |
| FTC Endorsement Guides FAQ | re-read; material connection must be disclosed clearly and conspicuously |

Values this pass did **not** reach are recorded as `unverified this pass` rather than copied from
the register: P-01/P-03 item weight, P-04 model HT07 and 572 °F, P-05 probe length.

**New flags (appended, nothing deleted or downgraded):** FLG-041 (a long `Specification Met` list is
a seller self-declaration), FLG-042 (P-03 points to a newer model than the submitted one), FLG-043
(buy-box offer state changes between reads), FLG-044 (the five values not re-reached).

**Not re-verified, still not claimed:** short-link redirects, Associates agreement / program policy
wording (login-gated), tracking-ID issuance, `link.amazon` compliance, the one-per-product Special
Link test, Search Console, and any hands-on performance.

### Decision-register additions (same session, non-overlapping)

- **SG-33** shop voice on buyer pages (Shipped) · **SG-34** `findability.txt` (Shipped) ·
  **SG-35** three-question shortlist (Shipped).
- **Q-21** does the rewrite change what the site may claim? (needs a human read of three pages)
- **Q-22** should the 12 project records stay in the sitemap? (owner)
- **Q-23** which three questions should the shortlist ask? (waiting on measured data)

### Handoff / conflict log

- Rebased onto `origin/main` at `66ccda9` (PR #39) cleanly before claiming. No other session held a
  live claim on `scripts/build_site.py`, `scripts/check_site.py`, `assets/style.css` or `assets/app.js`
  during this session, so no request had to be logged against another owner.
- Open PRs #16, #28, #34, #35 were left untouched. #16 owns the collector; nothing in this session
  edits `analytics/`, `functions/` or `data/events.json`.
- No file owned by another session was modified. `data/flags.json` was appended to only
  (FLG-041..044); `data/sources.json` was not edited.

### Merge resolution vs origin/main (this branch)

`origin/main` advanced to `3ceebb0` (PRs #40–#46) while this branch was in progress. `git merge
origin/main` conflicted in six files. Resolution, without discarding upstream work:

- `scripts/build_site.py` auto-merged and carries both sides (this session's `go_clean`,
  `findability.txt`, picker, shop cards, reading estimate; upstream's verification-addendum block).
- The five conflicted generated pages (`index.html`, `shop.html`, `verification.html`,
  `products/p01…`, `products/p02…`) were resolved by taking upstream's committed output and
  **re-running the merged generator**, which reproduces upstream's addendum rows (R-01…, from
  `data/verification.json`) and this session's reader-voice output in one pass. Generated files are
  never hand-merged.
- This file keeps upstream's records and appends this session's claim and completion records.
- Re-ran the gate after regeneration: 36 pages, 5 product records, 44 flags, 19 sources — ALL CHECKS PASS.

### Merge resolution vs origin/main at 4faab79

Upstream advanced again (PRs #47–#48, session b6b809da, which also claimed an ID called T-23 and
added its own FLG-041…045). Resolution, keeping both sides:

- `scripts/build_site.py`, `scripts/check_site.py` auto-merged; upstream's CSS/class gate and
  bidirectional product-link work are intact alongside this session's reader-voice helpers.
- `data/flags.json`: merged by ID as a union (upstream 46, this session 4) — and because upstream
  had already used FLG-041…045, **this session's four findings were renumbered to FLG-047…050**
  rather than overwriting anyone's IDs. 50 flags total.
- `assets/style.css`: both sides' additions kept. Upstream's new "every emitted class needs a rule"
  gate immediately caught four status tokens this session emits (`.ok`, `.warn`, `.muted`,
  `.needs`); rules were added rather than the gate loosened.
- All conflicted generated pages were resolved by re-running the merged generator.
- Gate after regeneration: 36 pages, 5 product records, 50 flags, 19 sources — ALL CHECKS PASS.

**ID collision log:** T-20, T-21 and T-23 are all now used by more than one session for different
work (this session's claim originally used T-20..T-22; this session's work is recorded as T-23..T-25).
Flag IDs are unique and monotonic; task IDs are not. Future sessions should claim from the current
maximum, not from the last ID seen in a prompt.

## Session `arena/0acc86ad-affil2` — PR, merge and deploy result

| Field | Value |
|-------|-------|
| PR | https://github.com/karagemop466-tech/Affil2/pull/49 |
| Merge | merged into `main` 2026-11-20T06:37:58Z as merge commit `c50a7fa761dca963a2952ca169ae6ccfc79cdb76` |
| CI before merge | "Regenerate and gate" — **pass** (run 44689101755) |
| Pages | `status=built`, https://karagemop466-tech.github.io/Affil2/ |
| Live verification | `findability.txt` fetched live and complete; product page fetched live and confirmed serving the reader-voice version ("Buy it if", "The specs that decide it", "Where this link actually goes", "Read from the listing bullets on 2026-11-20") with zero chunk citations or flag IDs |
| Gate at merge | 36 pages, 5 product records, 50 flags, 19 sources — ALL CHECKS PASS |
| Tests at merge | 3 Python tests OK; ALL JS COLLECTOR AND CLIENT TESTS PASS |

### Merge rounds required (main moved four times during this session)

1. `66ccda9` — clean rebase at claim time.
2. `3ceebb0` (PRs #40–#46) — six-file conflict; merged generator kept both sides, generated pages
   regenerated, upstream verification addendum R-01… preserved.
3. `4faab79` (PRs #47–#48, session b6b809da) — 17-file conflict; upstream had also used
   FLG-041…045, so **this session's four findings were renumbered to FLG-047…050**; upstream's new
   CSS/class gate caught four missing status-token rules, which were added rather than the gate
   being loosened.
4. `9af864b` (PR #50) — COORDINATION.md only; both sides kept.

No other session's work was discarded at any point. Every resolution was re-verified with the full
gate and both test suites before pushing.

## Session `arena/0acc86ad-affil2` — closing record

| Item | Result |
|------|--------|
| PR #49 (the work) | MERGED 2026-11-20T06:37:58Z — `c50a7fa` |
| PR #52 (the record) | MERGED — `4ddede5` |
| CI on final main commit | `Verify site` success, `pages build and deployment` success |
| Pages API | `status = built` |
| Live | https://karagemop466-tech.github.io/Affil2/ |

Everything this session claimed is published and reachable: reader-voice product and category
pages, `findability.txt` at the site root, the independent live pass on `verification.html`,
FLG-047…050 on `flagged.html`, SG-33…SG-35 on the Decision Center, and Q-21…Q-23 on Open
Questions. No task from this session remains open, and no other session's work was discarded.

**For the next session:** claim task IDs from the current maximum in the task board, not from the
last ID mentioned in a prompt — T-20, T-21 and T-23 each ended up used twice during this session
because parallel sessions read the same stale prompt. Flag IDs are safe (monotonic to FLG-050).
## Session `arena/614b9fe7-affil2` (T-26) — short-link re-check

- **Claimed:** T-26, files: data/verification-2026-11-20-shortlinks.json, data/flags.json (append only), COORDINATION.md, regenerated pages.
- **Sources fetched:** the five submitted links (S15–S19 in data/sources.json), each via fetch on 2026-11-20.
- **Result:** all five final URLs were `https://www.amazon.com/` (homepage), not the product pages recorded in the observed-destination field. Not reproduced. Recorded observed values were **not** changed; causes unconfirmed. Logged as **FLG-051** (needs review). Does not mean the short links are invalid (FLG-003 remains).
- **Gate:** `scripts/check_site.py` — 36 pages, 5 product records, 51 flags, 19 sources — ALL CHECKS PASS. `tests/test_site.py` OK; `tests/test_collector.js` PASS.
- **Not re-verified this session:** Associates agreement wording, tracking-ID issuance, the one-per-product Special Link test (requires the owner's Associates account; FLG-004), analytics endpoint, Search Console.
- **Conflict log:** none. Branch `arena/614b9fe7-affil2` at `main` 4ddede5 when claimed; no other session's claims touched.


### Session `arena/614b9fe7-affil2` (T-26) — PR, merge and deploy result

| Field | Value |
|-------|-------|
| PR | https://github.com/karagemop466-tech/Affil2/pull/55 |
| Merge | merged into `main` as `cac85d126bb920b3ebb48fbab7791ffb21f0c2a0` |
| CI before merge | "Regenerate and gate" — pass; "Verify site" — success |
| Pages | latest build `built` at `b1362ba4…`, https://karagemop466-tech.github.io/Affil2/ |
| Gate at merge | 36 pages, 5 product records, 51 flags, 19 sources — ALL CHECKS PASS |

## Session `57fc3be0` integration update (2026-11-20)

**T-26 — limited independent live pass:** fetched all five official Amazon `/dp/` pages and recorded only the observed page titles and ASINs in `data/verification-2026-11-20-pass3.json`. Fetched S01/S02 Amazon policy pages (publicly reachable; S02 page says updated 2026-04-14), S03 FTC Endorsement Guides FAQ, and S04 Google Search Central outbound-link guidance. The exact scope and limitations are recorded in that JSON; this was not a full spec re-verification and does not confirm seller claims, intended ASINs, short-link compliance, Associates enrollment, tracking ID, or report data. The FTC page says endorsements must be honest/not misleading and material connections should be disclosed clearly/conspicuously. Google says use `rel="sponsored"` for ads/paid placements and supports multiple values. Amazon OA displayed update date 2025-10-15; no account-only facts asserted.

**T-28 — documentation reconciled:** replaced README duplicate rows and stale counts/claims; rewrote EXECUTIVE-SUMMARY.md to reflect the present five products, 51 review flags, 19 sources, owner-gated items, and the empty campaign ledger. Generator and compliance/test gates pass; documentation changes are not generated HTML.

**PR reconciliation:** PR #53 is already merged (confirmed with `gh pr view`); its docs work is included in main history. PR #47 and PR #51 were closed after review but its branch is based on an unrelated, divergent snapshot and its tree diff would remove substantial current functionality (including analytics, findability, compliance checks, and shared records); it is not safe to merge wholesale. Its seasonal spotlight/guide-cluster additions were reviewed, but not applied as a risky broad patch. PR #51 is a coordination-only verification narrative on another unrelated branch; the current session recorded its own narrower live pass and the product inventory's existing field-level verification remains unchanged. Neither conflicting PR is a safe merge candidate into this shallow checkout. The closure rationale and the narrower live pass are retained here; no verification data was removed.

**Local validation (2026-11-20):** `python3 scripts/build_site.py` → built 36 pages; `python3 scripts/check_site.py` → 36 pages, 5 products, 51 flags, 19 sources, ALL CHECKS PASS; Python unittest → 3 tests OK; `node tests/test_collector.js` → ALL JS COLLECTOR AND CLIENT TESTS PASS. Additional internal href/src scan found zero missing local targets. GitHub Pages API previously reported `built`, source `main`, URL `https://karagemop466-tech.github.io/Affil2/`.
