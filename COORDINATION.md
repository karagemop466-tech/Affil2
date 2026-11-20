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
| T-10 | Independent line-by-line re-verification of register values vs official sources + verification log | done | bba2deed | data/verification.json, sources.html, COORDINATION.md |
| T-11 | Publication polish pass: brand, typography, imagery, seasons, clusters, authorship, nav labels (SG-27) | done | bba2deed | index.html, guides.html, guides/*.html, products/*.html, about.html, assets/style.css, assets/img/*, all *.html (nav/footer) |
| T-12 | Analytics on: five defined events, privacy-preserving outbound-click counter, self-hosted endpoint shipped + tested | done | bba2deed | assets/app.js, assets/config.js, analytics/*, disclosure.html |
| T-13 | Seasonal/question-shaped guides + publishing cadence + sitemap/feed sync (SG-28) | done | bba2deed | guides/*.html, guides.html, feed.xml, sitemap.xml |
| T-14 | Registers: SG-27..SG-30 rows, decision-gate UX, questions completeness (SG-29, SG-30) | done | bba2deed | suggestions.html, questions.html |
| T-15 | Integration: check script extension, JSON-LD fix, PR + merge + Pages confirm, record | in progress | bba2deed | scripts/check_site.py, .github/workflows/*, COORDINATION.md, EXECUTIVE-SUMMARY.md, README.md |

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

Session `bba2deed` scope note: branched from `12d49cd`, rebased onto `main` @ `e1b6750` before claiming. Tasks T-01..T-09 recorded done by `530c2e6c` (no longer active); T-10..T-15 claimed by `bba2deed` on branch `arena/bba2deed-affil2`. File scope above is exclusive for this claim; shared-board edits to COORDINATION.md are expected by every session. Branches `arena/177269f3-affil2`, `arena/9397cc0c-affil2`, `arena/990af5de-affil2` exist but carry no commits and no claims as of this entry.

## Handoff / conflict log
- 2026-11-20 530c2e6c: claimed all tasks, repo empty, no conflicts.
- PR link + merge result: (to be recorded at T-09 completion)
- 2026-11-20 bba2deed: claimed T-10..T-15 after rebasing onto main @ e1b6750. No conflicts observed.

## T-10..T-15 completion (2026-11-20, session bba2deed)

Sources used (all official, links for manual review): amazon.com listings S10-S14 (fetched 2026-11-20), Amazon Associates Operating Agreement (affiliate-program.amazon.com/help/operating/agreement), Program Policies (affiliate-program.amazon.com/help/node/topic/202131110), FTC Endorsement Guides FAQ (ftc.gov), Google Qualify-outbound-links (developers.google.com), USDA FSIS safe-temperature chart (fsis.usda.gov, used in the holiday roast guide).

Verification performed: every register value re-read row by row (titles, capacities, temperatures, power, dimensions, weights, models, features, warranty, box contents) against the official listings; policy claims checked against the official policy pages; per-value status (confirmed / corroborated / confirmed-conflict / corrected) published in `verification.html` + `data/verification.json`; per-row source links enforced by `scripts/check_site.py` (ALL CHECKS PASS, 29 pages).

Irregularities found by this pass (published on flagged.html; do not block):
- FLG-011 P-03 wattage conflict: live About-this-item bullet "1000 Watts/120 Volts - RJ38-SQSS-8T" vs product-info mirrors + Chefman manual "1700 watts". Both published; neither chosen.
- FLG-012 P-03 title drift (TurboFry Touch -> TurboFry 4-in-1 with 450F Hi-Fry Option) + 450F Hi-Fry title claim vs 200-400F bullet range.
- FLG-013 P-05 warranty: register's "1-year" unconfirmed; listing states "two-year assurance" (corroborated). Corrected with provenance.
- C-05 feed.xml malformed (<language> unclosed; XML parse error) - fixed; gate now parses the feed as XML.
- C-06 SG-08 claimed JSON-LD shipped but none existed - JSON-LD added (WebSite/Organization/Article/BreadcrumbList).
- C-07 stale flag cross-references in the session-530c2e6c log above (FLG-010/011/012 -> canonical FLG-008/009/010) - corrected in place.

Notes: "corroborated" values were read from product-information mirrors of the listing's own spec table (listing Product-details blocks were not reliably extractable in fetch); official listing links provided in every table row for manual review. Short links (FLG-003) remain unresolved and are NOT claimed invalid. Special Link one-per-product tests (FLG-004) still require the enrolled Associates workflow.

## T-09 completion (2026-11-20)
- PR: https://github.com/karagemop466-tech/Affil2/pull/1 — merged (merge commit fdb5d79)
- GitHub Pages: built, deploy workflow success. Live: https://karagemop466-tech.github.io/Affil2/
- Final gate: scripts/check_site.py ALL CHECKS PASS (25 pages)
- Flagged items FLG-001..FLG-010 published on flagged.html; do not block.
