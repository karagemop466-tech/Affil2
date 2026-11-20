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
| T-19 | Final integration: merge open PRs #16/#22/#27, resolve conflicts without discarding work, line-by-line re-verify combined data, build + broken-link gate, PR to main, merge, Pages deploy confirmation, completion record | in progress | de608df7 | COORDINATION.md, conflict resolutions in shared files as integration requires, EXECUTIVE-SUMMARY.md (append) |

Status key: unclaimed / in progress / done / needs review (= published on Flagged for Review, does not block).

> Session `de608df7` (branch `arena/de608df7-affil2`): first claimed T-12..T-14 from a stale base; renumbered to **T-19** after rebasing onto main — T-12 is taken (done, `4bbf49bb`), and the SG-27..SG-30/nav work (my old T-12) plus the analytics endpoint (my old T-13) are already in open PR #22 (`42617e35`) and PR #16 (`bdedd85e`) respectively. This session does not duplicate them; it integrates them as the final integration session (T-19).

## Verification log (2026-11-20, official sources only)

| Submitted link | Observed destination (separate field) | Official listing checked | Result |
|---|---|---|---|
| link.amazon/B04G1MEwY | B0CDY277D3 — CHEFMAN 6 Qt Dual Basket Air Fryer Oven (RJ38-SQPF-3TDB-2W) | https://www.amazon.com/dp/B0CDY277D3 | Title/model/specs match register; price/rating left blank per Program Policies §2(b) |
| link.amazon/B02NbDxp3 | B09B7SB46R — Emeril Lagasse 26 QT French Door Air Fryer Toaster Oven | https://www.amazon.com/dp/B09B7SB46R | Match; preset-count + model-number conflicts flagged (FLG-010/011) |
| link.amazon/B00hJ57DV | B08DKYBTPH — Chefman TurboFry Touch XL 8-Qt (RJ38-SQSS-8T) | https://www.amazon.com/dp/B08DKYBTPH | Match |
| link.amazon/B0c8moW59 | B0DHZTCNR5 — ThermoMaven Professional Digital Meat Thermometer, 1 Sec (HT07) | https://www.amazon.com/dp/B0DHZTCNR5 | Match |
| link.amazon/B0f3GKalj | B0DZFD6R9Z — CHEF iQ Sense [2025] Smart Wireless Meat Thermometer, Gen3 (CQ60-3C-Z1-E) | https://www.amazon.com/dp/B0DZFD6R9Z | Match; battery 50h vs 70h conflict flagged (FLG-012) |

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

## Integration note — T-19 (session de608df7, PR #22 merge, 2026-11-20)

- Merge of `arena/42617e35-affil2` (PR #22) into the integration branch: main's generated pages, `data/*.json` schema and `flags.json` ID meanings kept as authoritative (PR22 had identical ID sets on an older 3-field schema); no main work discarded.
- Session 42617e35's numbering in the block below (their T-10..T-17) is branch-local and predates main's board (whose T-10..T-18 belong to other sessions); their log is kept verbatim as their record. On main's board their content lands under T-19.
- Unique content ported into `scripts/build_site.py` (single source): SG-18..SG-30 decision rows (register now 30 rows; open ones SG-19/SG-20/SG-24 added to the shortlist), the Holiday Edit guide cluster (holiday-hosting, turkey-thermometer-plan, first-week-air-fryer added to GUIDES, sitemap, feed, both category lists and the design-brief cluster table), a front-page Holiday Edit section, original editorial art (`assets/img/*.jpg`) on the front page, categories and shop page, Fraunces/Inter brand fonts (SG-22), footer group renamed "Studio & records" (SG-27), and their gate rules (brand font link, (paid link) near every buy link, feed covers every guide, five instrumented events in app.js). 33 pages regenerate; `check_site.py` = ALL CHECKS PASS.
- Kept as new files: `analytics-endpoint/` (README + reference worker) and `scripts/update_chrome.py` (standalone tool, superseded by the generator but harmless).
- Flag-ID note: the verification log below says "FLG-011 (P-03 title vs body)" and "FLG-012 (Associates pages not re-fetchable)" — those meanings belong to their branch's older register; main's register (FLG-011 = unstable redirects, FLG-012 = B0c8moW59 not reproduced) is authoritative, and the P-03 wording finding is published under main's IDs. Their S01/S02 login-gate claim could not be reproduced: session T-19 fetched the Operating Agreement and Program Policies live the same day, so no flag was raised.
- Superseded (recorded, not silently dropped): their alternative front-page composition (main's published cover stays), and their hand-written chrome on the pre-existing pages (all regenerated by the generator so chrome is uniform).

---

# Session 2 — `42617e35`  Branch: `arena/42617e35-affil2`  Base: e1b6750 (main)
Started: 2026-11-20 (UTC). Scope: reader-facing polish pass ("reads like a shop, not an audit"), seasonal/trendy article clusters, decision-making registers (suggestions + questions), measurement layer (click counter + self-hosted analytics endpoint spec, five events), product-intent/link-test register fields, line-by-line re-verification against official sources.

> Claim note: no other session has an open claim (all T-01..T-09 done/owned by `530c2e6c`, inactive). Scopes below are claimed by `42617e35` on this branch. Shared outputs (sitemap, feed, nav) are edited by this session as the current integration session and re-verified before merge.

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-10 | Re-verify 5 Amazon listings + program sources (S01–S04) line by line | done | 42617e35 | data/sources.json, sources.html, COORDINATION.md |
| T-11 | Publication/shop redesign (imagery, brand, nav labels, front page leads with products) | done | 42617e35 | index.html, assets/style.css, assets/*, all .html (nav/footer) |
| T-12 | Seasonal/trendy article cluster (holiday hosting + evergreen questions) | done | 42617e35 | guides/*.html, guides.html |
| T-13 | Measurement layer: privacy-preserving outbound-click counter + self-hosted analytics endpoint spec, five defined events | done | 42617e35 | assets/app.js, analytics-endpoint/*, disclosure.html |
| T-14 | Product-intent confirmation record + per-product Special Link test register (separate fields) | done | 42617e35 | data/products.json, sources.html |
| T-15 | Decision registers: suggestions (SG-01..SG-30 incl. SG-27..SG-30) + open questions (known/unknown/how to close) | done | 42617e35 | suggestions.html, questions.html |
| T-16 | Executive summary refresh + flagged refresh | done | 42617e35 | EXECUTIVE-SUMMARY.md, executive-summary.html, flagged.html, data/flags.json |
| T-17 | Integration: sitemap/feed, check_site.py gate, PR to main + merge + Pages verify | in progress | 42617e35 | sitemap.xml, feed.xml, scripts/check_site.py, COORDINATION.md |

## Verification log — session 42617e35 (2026-11-20, official sources only)

| Item | Method | Result |
|---|---|---|
| P-01 B0CDY277D3 | live listing fetch | Title/identity match (long-form title incl. baskets/finish recorded in products.json) |
| P-02 B09B7SB46R | live listing fetch | Title/identity match; live title states **24** One-Touch Preset Options (FLG-009 evidence kept) |
| P-03 B08DKYBTPH | live listing fetch | Title/identity match; live title states TurboFry 4-in-1, **450 °F Hi-Fry** (FLG-011 — title vs body wording, both published) |
| P-04 B0DHZTCNR5 | live listing fetch | Title/identity match (HT07 family) |
| P-05 B0DZFD6R9Z | live listing fetch | Title/identity match (Gen3; live title drops "[2025 Model]" bracket — same ASIN) |
| S03 FTC Endorsement Guides FAQ | live fetch | Re-verified (affiliate-marketing section present) |
| S04 Google Qualify outbound links | live fetch | Re-verified (rel=sponsored; multiple rel values valid) |
| S15 USDA FSIS temperature chart | live fetch | Verified — poultry 165 °F, leftovers 165 °F, steaks 145 °F + 3-min rest (chart updated 2025-04-14). New source row. |
| S01/S02 Associates OA/Policies | live fetch FAILED (login-gated) | **MANUAL REVIEW** — links published on sources.html for hand-check (FLG-012). Wording basis carried from 530c2e6c log; not claimed as re-verified. |

Checks: `scripts/check_site.py` ALL CHECKS PASS (28 pages) — includes disclosure-before-`<main>`, sponsored marking on every Amazon link, (paid link) near every data-outbound, no price/star values, internal links + assets, sitemap coverage, feed coverage of all 9 guides, separate intended/observed fields in data registers, five instrumented events.

New flags this session: FLG-011 (P-03 title vs body wording), FLG-012 (Associates pages not re-fetchable). FLG-007/FLG-010 updated (AI-generated editorial imagery; measurement layer shipped, endpoint deploy pending).


---

## Session bdedd85e — integration note (T-19, 2026-11-20 UTC)

Their T-13/T-14 record is preserved verbatim below. Integration deltas, recorded rather
than silently rewritten:

- **FLG-033 renumbered → FLG-036.** `main` already uses FLG-033 for "no named author or
  editorial owner"; their collector flag is published as FLG-036 (detail expanded with the
  aggregate-only Worker as the third implementation) and their amended FLG-010 points at it.
  Their test assertion and `platform.html` were remapped in the same pass.
- **The collector now has a third deployable form:** `analytics-endpoint/worker.js` was
  adapted from PR #22's `/api/analytics` shape to this stack's `/api/collect` contract
  (GET probe → 200, POST → 204/400/413, aggregate-only KV, 90-day expiry, never stores
  search text). One contract, three implementations, one schema (`data/events.json`).
- **`analytics-endpoint/README.md` rewritten** to the `/api/collect` contract; PR #22's
  term-storage plan for search aggregation is recorded as gated behind SG-18/Q-08.
- **`scripts/build_content.py` supersession stands:** `main` builds with
  `scripts/build_site.py`; their generator edits were not carried over (their prose
  deltas were ported into the generator instead — disclosure, questions, SG-12, search,
  Measurement and Platform pages).
- **The workflow stays verify-only** (no deploy job): `main`'s CI runs rebuild → drift →
  gate → `node tests/collector.test.js` → `python3 -m unittest discover -s tests -p "test_*.py"`.
  Publication remains GitHub Pages' branch builder.
- **Tag rule scoped, not dropped:** the gate requires the tracking tag on every Amazon
  **buy link** (CTA) and `rel=sponsored` everywhere; labelled verification links may stay
  untagged per `how-we-choose.html`. Their blanket-tag test was adapted accordingly.
- **`assets/app.js` stays local-only.** Their client `assets/js/collect.js` is now the
  sole network half (probe → inert); app.js's duplicate beacon was never ported. Zero-result
  searches are counted (SG-18's signal) and guide events carry the slug.
- Branch-local T-13/T-14 numbering collided with `main`'s T-13/T-14 (already published);
  this record keeps their IDs as historical, per the same convention as their Session-2 block.

## Session bdedd85e — T-13 / T-14 claim (2026-11-20 UTC)

**Session ID:** `bdedd85e`  **Branch:** `arena/bdedd85e-affil2`
**Base when started:** `12d49cd` (the original `Initial commit`) — **stale**; `main` had already moved to `1c52f8a`.

### Conflict log — the parallel site was NOT merged

This session was started from a stale base and built a complete parallel site
(`tools/`, `content/`, `assets/`, `docs/`, `functions/`, `analytics/`, `tests/`,
plus its own `data/*.json` registers). That work is **not** merged.

Reason, recorded rather than quietly resolved:

- `main` already contains a complete, deployed publication from sessions
  `530c2e6c`, `6e40cecc`, `990af5de`, `937876a6`, `4bbf49bb` and `e9516a41`
  (PRs #1–#13). Merging a second site would discard all of it, including the
  re-verification records, FLG-017..030, the USDA and Creators API citations,
  the original illustrations and the decision tools.
- Two earlier sessions (`990af5de`, `e9516a41`) built parallel sites the same
  way; both were withdrawn for the same reason and logged above.
- The standing instruction for this repository is that a session must never
  overwrite another session's work, and that shared outputs belong to the
  final integration session. This session **is** the integration session, so it
  keeps `main`'s site and data and merges only what adds to them.

The parallel build is preserved out of tree at `/tmp/affil2-parallel/` for this
session's reference only. Nothing from it replaces a `main` file.

### What this session claims

| ID | Task | Status | Files (exclusive scope) |
|----|------|--------|-------------------------|
| T-13 | Self-hosted analytics endpoint + five-event privacy-preserving collector | in progress | `functions/api/collect.js`, `analytics/server.js`, `assets/js/collect.js`, `data/events.json`, `tests/collector.test.js` |
| T-14 | Measurement surface, gate hardening, tracking-tag compliance, CI in the publish workflow | in progress | `measurement.html`, `scripts/check_site.py`, `scripts/build_content.py`, `.github/workflows/pages.yml`, `sitemap.xml`, `feed.xml`, `disclosure.html`, `questions.html`, `data/flags.json` (append only), `tests/test_site.py`, `README.md`, `EXECUTIVE-SUMMARY.md` |

**Not claimed, not touched:** `data/products.json`, `data/sources.json`,
`data/reverification-2026-11-20.json`, `data/campaign-ledger.json`,
`scripts/build_content.py` product/spec rendering, `assets/style.css`,
`assets/illustrations/*`, and every existing page's editorial copy. Those stay
exactly as `main` has them.

### The gap this session is closing

`main`'s own records name the gap twice:

- `FLG-010` — "Analytics local-only: click counter runs in-browser until a
  self-hosted endpoint is deployed. See Q-08."
- `disclosure.html` — "A self-hosted endpoint (Q-08) will replace local storage
  when deployed; until then, server-side conversion data is blank by design."

GitHub Pages cannot host a server-side function, so the endpoint is shipped in
this repository in two deployable forms (a Cloudflare Pages Function and a
dependency-free Node server) and is **inert** until someone points the site at
one. The site keeps working, and keeps collecting nothing, until then.

### T-13 / T-14 completion (2026-11-20, session bdedd85e)

**What shipped**

| Area | File(s) | State |
|---|---|---|
| Collector, Cloudflare Pages Function | `functions/api/collect.js` | shipped, not deployed |
| Collector, standalone Node server | `analytics/server.js` | shipped, not deployed |
| Browser client | `assets/js/collect.js` | shipped, inert until a collector answers |
| Event schema | `data/events.json` | shipped, enforced in code by the collector |
| Measurement surface | `measurement.html` | published, linked from every page |
| Platform concept | `platform.html` | published, linked from every page |
| Gate hardening | `scripts/check_site.py` | 8 new rules |
| Generator changes | `scripts/build_content.py` | tracking tag on every Amazon product link, `rel="sponsored"` on every `link.amazon` link, collector script and dashboard links on every page |
| Publish workflow | `.github/workflows/pages.yml` | `verify` job: rebuild → drift check → gate → collector tests → site tests; `deploy` needs `verify` |
| Tests | `tests/collector.test.js`, `tests/test_site.py` | 13 + 22 checks |
| Registers | `data/flags.json` | FLG-033 appended, FLG-010 amended to point at it |

**Verification**

- `python3 scripts/build_content.py` — runs clean and is idempotent: a second run produces byte-identical pages.
- `python3 scripts/check_site.py` — **checked 27 pages, ALL CHECKS PASS**.
- `node tests/collector.test.js` — **13 checks passed**.
- `python3 -m unittest discover -s tests -p "test_*.py"` — **22 tests, OK**.
- Collector exercised end to end against a local server: `GET` → `200 {"status":"ok"}`, beacon-style `POST` → `204`, and a payload carrying `email`/`ip` stored neither. Against the static site `/api/collect` → `404`, so the client stays inert exactly as designed.
- HTML structure check over all 27 pages: 0 unclosed tags, 0 template artifacts.
- Local HTTP smoke test: every page and asset returns `200`.

**Rules added to the publishing gate**

1. Every Amazon **product** link carries the Associates tracking tag.
2. Every `link.amazon` short link carries `rel="sponsored"`.
3. No Amazon-hosted imagery.
4. Canonical link and meta description on every page.
5. Broader star-rating and review-count patterns.
6. The collector client is loaded on every page.
7. `data/events.json` and the collector agree on the event list.
8. `measurement.html` exists and is in the sitemap.

**Left open, on the board, not blocking**

- FLG-033 — the collector ships but is not deployed, because GitHub Pages cannot run a server-side function. Owner action: deploy one implementation, point the site at it, and choose a retention period.
- FLG-003 / FLG-004 — short-link compliance and the one-per-product Special Link test remain unresolved and are not claimed either way.
- FLG-001 / FLG-002 — intended ASINs and tracking-ID activity remain unconfirmed; the campaign ledger stays empty.

**Nothing from `main` was discarded.** `data/products.json`, `data/sources.json`, `data/reverification-2026-11-20.json`, `data/campaign-ledger.json`, `assets/style.css`, `assets/illustrations/*`, `scripts/build_content.py`'s product and spec rendering, and every page's editorial copy are as `main` had them. The only shared files this session changed are the ones listed in the claim: the workflow, the gate, the generator, the sitemap, the robots file, `data/flags.json` (append only), `disclosure.html`, `questions.html`, `suggestions.html`, `executive-summary.html`, `README.md` and `EXECUTIVE-SUMMARY.md` — all edited surgically, never rewritten.
