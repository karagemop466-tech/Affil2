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

# Session 2 — `42617e35`  Branch: `arena/42617e35-affil2`  Base: e1b6750 (main)
Started: 2026-11-20 (UTC). Scope: reader-facing polish pass ("reads like a shop, not an audit"), seasonal/trendy article clusters, decision-making registers (suggestions + questions), measurement layer (click counter + self-hosted analytics endpoint spec, five events), product-intent/link-test register fields, line-by-line re-verification against official sources.

> Claim note: no other session has an open claim (all T-01..T-09 done/owned by `530c2e6c`, inactive). Scopes below are claimed by `42617e35` on this branch. Shared outputs (sitemap, feed, nav) are edited by this session as the current integration session and re-verified before merge.

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| T-10 | Re-verify 5 Amazon listings + program sources (S01–S04) line by line | in progress | 42617e35 | data/sources.json, sources.html, COORDINATION.md |
| T-11 | Publication/shop redesign (imagery, brand, nav labels, front page leads with products) | in progress | 42617e35 | index.html, assets/style.css, assets/*, all .html (nav/footer) |
| T-12 | Seasonal/trendy article cluster (holiday hosting + evergreen questions) | in progress | 42617e35 | guides/*.html, guides.html |
| T-13 | Measurement layer: privacy-preserving outbound-click counter + self-hosted analytics endpoint spec, five defined events | in progress | 42617e35 | assets/app.js, analytics-endpoint/*, disclosure.html |
| T-14 | Product-intent confirmation record + per-product Special Link test register (separate fields) | in progress | 42617e35 | data/products.json, sources.html |
| T-15 | Decision registers: suggestions (SG-01..SG-30 incl. SG-27..SG-30) + open questions (known/unknown/how to close) | in progress | 42617e35 | suggestions.html, questions.html |
| T-16 | Executive summary refresh + flagged refresh | in progress | 42617e35 | EXECUTIVE-SUMMARY.md, executive-summary.html, flagged.html, data/flags.json |
| T-17 | Integration: sitemap/feed, check_site.py gate, PR to main + merge + Pages verify | unclaimed | 42617e35 | sitemap.xml, feed.xml, scripts/check_site.py, COORDINATION.md |
