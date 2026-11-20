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
| T-09 | Final integration: build check, broken-link check, GitHub Pages, PR + merge | in progress | 6e40cecc | feed.xml, COORDINATION.md |

Status key: unclaimed / in progress / done / needs review (= published on Flagged for Review, does not block).

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

## T-09 completion (pending)
- PR: (to be created from arena/6e40cecc-affil2 to main)
- GitHub Pages: already enabled, source = main, live at https://karagemop466-tech.github.io/Affil2/ — re-deploy on main push after merge
- Flagged items FLG-001..FLG-010 published on flagged.html; do not block.

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
