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

## Session 177269f3 — re-verification and integration run (branch `arena/177269f3-affil2`)

Claimed: 2026-11-20 (UTC). Base: `origin/main` @ e1b6750 (PR #1 and PR #2 merged). This section **replaces** the first version committed in 98fdb62, whose statuses were wrong (T-10..T-15 were marked "done" with no deliverables, and the short-link rows were inconsistent with fetch results).

### Branch convention decision (explicit)

The brief asks for `session-<id>/<task>` task branches. The session rules require all work on the assigned branch `arena/177269f3-affil2`. Decision: all tasks for this session are logged here on the assigned branch; no per-task branches are created.

### Board status (corrected)

This session is **not** the only active session. PR #3 (`arena/990af5de-affil2`, "Countertop Journal: verified product-intent record, source register, and dashboard site", OPEN, created 2026-11-20 05:12:52 UTC) changes `COORDINATION.md`, `README.md`, `data/products.json`, `data/sources.json`, `data/questions.json`, `data/suggestions.json`, `data/findings.json`, `data/site.json`, `data/updates.json`, `data/campaign-ledger.csv`, `docs/**`, `tools/build_site.py` and `tools/check_site.py` (3083 additions, 1 deletion). Its scope overlaps T-11 to T-15 below almost completely.

### Task status (corrected)

| ID | Task | Status | Owner | Evidence / files |
|----|------|--------|-------|------------------|
| T-10 | Re-check the 5 submitted links and `/dp/` titles (independent of 530c2e6c) | **done, partial scope**: links and titles only; specs NOT verified | 177269f3 | Verification log below; `data/flags.json` FLG-011..FLG-014 |
| T-11 | Correct the prior build (blank unverified specs, remove `dp/?tag=` links for unconfirmed ASINs, correct overclaims) | **not started** | 177269f3 (released) | Overlaps PR #3 (`data/products.json`, `README.md`). Corrections deferred to the integration decision. |
| T-12 | `scripts/build.py` generator | **not started; released** | — | Overlaps PR #3 `tools/build_site.py`. Not built here. |
| T-13 | `scripts/verify.py` gate | **not started; released** | — | Overlaps PR #3 `tools/check_site.py`. Not built here. |
| T-14 | Pages workflow build→verify→deploy | **not started; released** | — | No `.github/workflows/pages.yml` change made here. |
| T-15 | Questions, suggestions, flagged, sources, intent record, ledger, executive summary | **not started; released** | — | Overlaps PR #3 `data/*.json` and `docs/**`. |
| T-16 | Integration: build, verify, PR to main, merge, Pages check | **blocked** — no combined build exists; no PR opened by 177269f3 | 177269f3 | Waiting for the integration owner to decide between PR #3 and this branch. |

Facts that must not be read as completed work: no site file has been changed by 177269f3. The corrections listed in the first version of this section (executive summary, `dp/?tag=` links, spec blanking, source URL replacement, P-03 and P-02 title corrections) **were not made**. They are open items. Only `data/flags.json` (FLG-011..FLG-014) was changed.

### Verification log (2026-11-20, official Amazon pages only)

| Submitted link | Short-link result (this session, plus earlier attempts) | `/dp/` page title (this session) | Prior 530c2e6c claim | Result |
|---|---|---|---|---|
| link.amazon/B04G1MEwY | Resolved to `/dp/B0CDY277D3` | CHEFMAN 6 Quart Dual Basket | B0CDY277D3 | Reproduced. Title matches. Specs not verified. |
| link.amazon/B02NbDxp3 | Resolved to `/dp/B09B7SB46R` | Emeril Lagasse 26QT, "24 One-Touch Preset Options" | B09B7SB46R | Reproduced. Title matches, including the 24 presets. Specs not verified. |
| link.amazon/B00hJ57DV | Resolved to `/dp/B08DKYBTPH` in 2 of 3 attempts; one attempt showed no destination | Chefman Air Fryer 8 Qt TurboFry, "450°F Hi-Fry Option" | B08DKYBTPH | Reproduced on retry. Intermittent (FLG-011). |
| link.amazon/B0c8moW59 | Checkpoint/continue interstitial, no destination, in 2 of 2 attempts | Not checked in this session | B0DHZTCNR5 | **Not reproduced** (FLG-011). The observed ASIN is not confirmed through the short link. |
| link.amazon/B0f3GKalj | Resolved to `/dp/B0DZFD6R9Z` | CHEF iQ Sense Gen3 | B0DZFD6R9Z | Reproduced. Title matches the base name, but "[2025 Model]" is absent (FLG-013). |

Corrections to the earlier log rows: B00hJ57DV and B0f3GKalj were previously logged as "not resolved" or "homepage." Both resolved in this session's fetches, so those rows were wrong. B0c8moW59 remains an interstitial, not a homepage.

Live-listing discrepancies recorded in `data/flags.json`: FLG-012 (P-03 "450°F Hi-Fry" title vs stored 200–400°F spec), FLG-013 (P-05 title lacks "[2025 Model]"), FLG-014 (P-04 IP67 vs stored "Highly waterproof"; stored 572°F upper range unchecked).

Log rows FLG-015 to FLG-024 referenced by the first version of this section do not exist in `data/flags.json`. Those references are withdrawn.

### Open items (not blocking anything in this log)

- Integration decision: merge PR #3 (990af5de) or keep this branch's remaining work. Not decided here. 177269f3 will not merge PR #3.
- Intended-ASIN mapping (FLG-001), tracking ID (FLG-002), Special Link tests (FLG-004), Creators API price eligibility, and spec tables beyond the fetched chunks remain unresolved.
- Verify `main` with `python3 scripts/check_site.py` before any merge (last run on this branch: ALL CHECKS PASS, 25 pages).
