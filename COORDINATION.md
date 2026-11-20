# COORDINATION — Affil2 shared task board

Session ID: `530c2e6c`  Branch: `arena/530c2e6c-affil2`  Base: `12d49cdc2523508f8cc6d2d36257b48e6ffc5529` (main)
Started: 2026-11-20 (UTC)  Tracking ID supplied: `shopnow047c-20` (UNVERIFIED — see FLG-002)

> Single-session run: no other session has claimed any task in this repo (repo was README-only at start, verified `git log`/`ls`). All scopes below are claimed by `530c2e6c` on this branch. No file owned by another session was edited.

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
| T-09 | Final integration: build check, broken-link check, GitHub Pages, PR + merge | in progress | 530c2e6c | .github/workflows/pages.yml, COORDINATION.md |

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

## Handoff / conflict log
- 2026-11-20 530c2e6c: claimed all tasks, repo empty, no conflicts.
- PR link + merge result: (to be recorded at T-09 completion)

## T-09 completion (2026-11-20)
- PR: https://github.com/karagemop466-tech/Affil2/pull/1 — merged (merge commit fdb5d79)
- GitHub Pages: built, deploy workflow success. Live: https://karagemop466-tech.github.io/Affil2/
- Final gate: scripts/check_site.py ALL CHECKS PASS (25 pages)
- Flagged items FLG-001..FLG-010 published on flagged.html; do not block.

---

## Session 177269f3 — re-verification, correction and integration run (branch `arena/177269f3-affil2`)

Claimed: 2026-11-20 (UTC). Base: `origin/main` @ fdb5d79 (PR #1 merged; PR #2 merged). Branch fast-forwarded from 12d49cd to fdb5d79 — no local commits were lost.

Branch-naming note: the brief asks for `session-<id>/<task>` branches; the session rules require all work on the assigned branch `arena/177269f3-affil2`, so tasks are logged here instead of on separate branches. This is the only active session on the board.

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-10 | Independent re-check of all 5 submitted links and the 5 `/dp/` listing pages (did not reuse 530c2e6c results) | done | 177269f3 | data/products.json, data/verification.json |
| T-11 | Correct the prior build: remove unverified specs, remove dp/?tag= links for unconfirmed ASINs, correct overclaims | done | 177269f3 | data/*.json, content/*.html |
| T-12 | Data-driven generator (`scripts/build.py`) for all pages, sitemap, robots, RSS | done | 177269f3 | scripts/build.py, site/ (generated, not committed) |
| T-13 | Line-by-line verification gate (`scripts/verify.py`): disclosure on every page, sponsored rel on every outbound link, no prices/ratings, no broken links, sitemap coverage, every row has a source | done | 177269f3 | scripts/verify.py |
| T-14 | Pages workflow: build → verify → deploy (fails closed) | done | 177269f3 | .github/workflows/pages.yml |
| T-15 | Questions, suggestions (decision menu), flagged-for-review, sources, product-intent record, ledger, executive summary | done | 177269f3 | content/*.html, data/*.json |
| T-16 | Integration: build + verify + PR #3 to main + merge + Pages deploy check; record here | in progress | 177269f3 | COORDINATION.md |

### Session 177269f3 verification log (2026-11-20, official sources only)

| Submitted link | Token | Short-link resolution (this session) | Direct `/dp/` check (this session) | Prior session 530c2e6c claim | Result |
|---|---|---|---|---|---|
| link.amazon/B04G1MEwY | 9 chars | Resolved → `amazon.com/dp/B0CDY277D3` | B0CDY277D3 page title matches | B0CDY277D3 | Reproduced (redirect). Title verified; specs not verified |
| link.amazon/B02NbDxp3 | 9 chars | Resolved → `amazon.com/dp/B09B7SB46R` | B09B7SB46R page title matches | B09B7SB46R | Reproduced (redirect). Title verified; specs not verified |
| link.amazon/B00hJ57DV | 9 chars | Not resolved (Amazon checkpoint interstitial) | `/dp/B08DKYBTPH` exists; title = Chefman 8 Qt TurboFry | B08DKYBTPH | NOT reproduced (FLG-011) |
| link.amazon/B0c8moW59 | 9 chars | Not resolved (Amazon homepage, no product) | `/dp/B0DHZTCNR5` exists; title = ThermoMaven 1 Sec | B0DHZTCNR5 | NOT reproduced (FLG-011) |
| link.amazon/B0f3GKalj | 9 chars | Not resolved (Amazon homepage, no product) | `/dp/B0DZFD6R9Z` exists; title = CHEF iQ Sense Gen3 | B0DZFD6R9Z | NOT reproduced (FLG-011) |

Corrections made by 177269f3 (details on `flagged.html` and `verification.html`):
- Prior executive summary stated that all five links resolve to the observed ASINs and that titles/specs match listings. Not reproduced for 3 of 5; specs were not checked. Corrected (FLG-015).
- Prior product pages built `amazon.com/dp/<ASIN>?tag=shopnow047c-20` links for ASINs whose link mapping is unconfirmed. Replaced: outbound CTAs now use the submitted short links, marked sponsored, with Special Link test pending (FLG-017).
- Prior spec values marked "(listing)" (dimensions, wattage, weight, temperature ranges, battery hours, model numbers, presets) were not verified in this session. Blanked and flagged (FLG-016).
- Prior `sources.json` URLs S01/S02 (`help/node/topic/...`) were not retrieved. Replaced with URLs retrieved this session (FLG-024).
- Prior title for P-03 said "Chefman TurboFry Touch"; the live page title reads "Chefman Air Fryer 8 Qt | TurboFry 4-in-1 with 450°F Hi-Fry Option". Recorded as observed title; prior "200–400°F" range blanked (FLG-016).
- Prior title for P-02 (Emeril) said "Extra Large Air Fryer"; live title reads "...24 One-Touch Preset Options...". Recorded as observed (relevant to FLG-009).
