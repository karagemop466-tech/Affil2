# Executive Summary — ShopNow Kitchen

Date 2026-11-20 · Branch `arena/36170d15-affil2` · Tracking ID in use `shopnow047c-20` (issuance and activity unverified — FLG-002)
Reference live site: https://karagemop466-tech.github.io/Affil2/ — publication is served by GitHub Pages from `main`; the work in this branch is not on `main` until merged.
Full on-site version with source links: `executive-summary.html`

## What this is
A static, publication-style Amazon affiliate publication covering five submitted products in two categories: three air fryers and two meat thermometers. Specifications are tied to dated official sources; contradictions between listing statements are printed, not smoothed over; unsupported values are left blank. No price, star rating, review count or best-seller rank is reproduced — Program Policies §2(b) and §6(t) permit those only when Amazon serves the link or the data arrives through an approved API, and this site has neither.

## The five products: three separate identities, kept separate
The submitted short-link token, any redirect actually observed, and the official listing used for the product record are stored as separate fields. Intended ASINs remain blank until the owner confirms them (FLG-001). Official listing ≠ confirmed intent; an observed redirect ≠ intended destination.

| ID | Submitted token | Intended ASIN | Observed redirect target | Official listing |
|----|-----------------|---------------|--------------------------|------------------|
| P-01 | link.amazon/B04G1MEwY | blank (FLG-001) | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 |
| P-02 | link.amazon/B02NbDxp3 | blank (FLG-001) | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R |
| P-03 | link.amazon/B00hJ57DV | blank (FLG-001) | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH |
| P-04 | link.amazon/B0c8moW59 | blank (FLG-001) | none observed — checkpoint page on every attempt (FLG-012) | https://www.amazon.com/dp/B0DHZTCNR5 |
| P-05 | link.amazon/B0f3GKalj | blank (FLG-001) | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z |

Redirect observations are dated snapshots, not permanent mappings (FLG-011). The official listing ASIN is shown because it is the page used to source the product data; it is not evidence of the owner's intent.

## Current listing conflicts (both statements kept, source-linked)
| Flag | Product | Field | Statements captured 2026-11-20 |
|------|---------|-------|-------------------------------|
| FLG-034 | Chefman 6 Qt (P-01) | Capacity | 6 quarts / 2×3-qt baskets (About this item) vs 6 liters (Product Details) |
| FLG-021 | Emeril 26 QT (P-02) | Presets | 24 one-touch presets (page title) vs 25 cooking pre-sets (About this item) |
| FLG-031 | Emeril 26 QT (P-02) | Included accessories | six (page title / Included Components names six) vs seven (Configuration) |
| FLG-018 | Chefman 8 Qt (P-03) | Top temperature | 200–400 °F (About this item) vs 450 °F Hi-Fry option (page title) |
| FLG-008 | CHEF iQ Sense (P-05) | Battery | 50 hours (About this item, current) vs 70 hours (earlier capture retained for review) |
| FLG-038 | CHEF iQ Sense (P-05) | Warranty | two-year assurance (About this item) vs 3 Year (Warranty Description, Item details) |

P-04's certification is a seller-stated listing statement (NIST and NSF, FLG-035), not an independently reviewed certificate; its 572 °F upper range is stated in the Features & Specs table (FLG-040).

## Decision Center additions this pass (merged tree)
- **SG-31** — Review GitHub Pages suitability before directing purchase traffic (FLG-041). Blocking for promotion; not a finding of a violation.
- **SG-32** — Re-read the five listings end to end and refresh review scope (extends the 2026-11-20 re-read recorded under FLG-040).
- **SG-25** — Deploy the optional self-hosted collector in this repository (counts five events as daily aggregates, no identifiers; not deployed today).
- **SG-29** — Search Console property and sitemap submission (owner account needed).
- **SG-26** — Feed the campaign ledger from authorized first-party reports only; the ledger stays empty until one exists.
- All 31 proposals carry their official evidence source(s) in the Decision Center; nothing self-applies.

## How the site is kept honest
`scripts/build_site.py` generates every page from `data/*.json`; `scripts/check_site.py` fails the build on missing disclosure, sponsorship/tag errors, prices, star ratings, review counts, broken links, sitemap/feed drift, unsourced spec rows, missing decision-table evidence, or intent/observed field removal. The CI workflow regenerates and gates on PRs to `main` (it is a verifier, not a deployer; Pages' own branch builder publishes `main`).

## Honest position on revenue
Zero, with no forecast. No commission rate, click, conversion or earnings figure can be obtained from an authorized first-party report yet. `campaign-ledger.html` is intentionally empty with its schema and provenance rule documented.

## Tools and open items (current)
- SG-17 / `design-brief.html` — the Design & Traffic Brief is published and linked.
- The self-hosted analytics collector is in this repository (`scripts/analytics_server.py`, aggregate counts only, five events) and is not deployed; deploying it is SG-25.
- Suggestions review lives at `suggestions.html`; rank SG-13, SG-14, SG-15, SG-16, SG-17, SG-25 and SG-31 there before anything is built.
- Open Questions register now runs to Q-18 (imagery policy, front-page evidence, one-sentence purpose, governing jurisdiction) plus UF-1/UF-2 (niche expansion, success metrics) awaiting account access.
- Q-15 to Q-18 are registered in `questions.html`.
- Pages hosting suitability is an open pre-promotion question (SG-31, FLG-041), and GitHub's host-side IP logging must be surfaced in the privacy notice (SG-25 context, FLG-042); see the disclosure page.

## Verification log (2026-11-20, session arena/436f4dbe-affil2)
- All 29 pages built successfully by `scripts/build_site.py`; `check_site.py` passed (superseded by later passes).
- Bracket note: the line "No manual input required; all tasks completed autonomously" in that log should not be read as closing the owner-action items; those remain open and are listed throughout this document.

## Re-verification log (2026-11-20, session arena/3fb8f29e-affil2)
- All five official listings re-fetched and read line by line against `data/products.json`: titles, breadcrumbs, capacity, temperature ranges, wattage, dimensions, warranty, presets, probes, sensors, battery wording and included components all match the register. The known listing contradictions (24 vs 25 presets on the Emeril, 50 vs 70 hours on the CHEF iQ, 1000 W vs 1700 W on the Chefman 8 Qt as an About-vs-spec-field difference, 6 quarts vs 6 litres capacity field on the Chefman 6 Qt) reproduce as flagged.
- USDA FSIS chart re-fetched; values on this site match verbatim (165 / 160 / 145+3 min / 145 / 165 °F).
- Google "Qualify your outbound links" re-fetched; rel=sponsored for paid links confirmed.
- Associates Program Policies and the PA-API 5 deprecation notice re-fetched; migrate to the Creators API.
- FTC Endorsement Guides FAQ re-fetched; disclosure-above-the-fold requirement reaffirmed.
- `design-brief.html` published (SG-17).

## Merge integration log (2026-11-20, session arena/36170d15-affil2)
- Merged `origin/main` (which carries the re-read register, the storefront build, the design brief and 40 flags) with this branch's identity separation and measurement work.
- Register fields now publish the 2026-11-20 re-read values (FLG-040); P-02 model 4-00675-02X-VN / 75–500 °F / 1700 W, P-04 model HT07 / 572 °F upper range, P-05 model CQ60-3C-Z1-E / 4.75 in probe, P-05 warranty conflict (FLG-038), weights blank everywhere (FLG-022, no listing states them).
- New-schema product records: intended ASIN blank (FLG-001); observed redirect and official listing stored as separate dated records; every field carries `source_id`.
- Decision Center proposals renumbered to append cleanly after main (SG-31 hosting suitability, SG-32 listing re-read); all 25 rows cite official evidence.
- Flag register extended to 42 with FLG-041 (Pages hosting suitability — open question, not a violation finding) and FLG-042 (host-side IP logging — disclosure updated).
- Source register extended to 28 (S24 Pages limits, S25–S27 Search Console, S28 Pages custom domains, S29 RSS 2.0, S30 CAN-SPAM, S31 helpful content, S32 Pages overview/host-side IP logs, S33 SEO Starter Guide). Main's S23 (FTC Disclosures 101) is unchanged.
- Optional self-hosted collector added (`scripts/analytics_server.py`): five events only, daily aggregate counts, no identifiers; not deployed and not referenced by any page; disclosure says so.
- Gate union: main's image-caption, no-`lb`-in-prose, pair-view and FAQ rules, plus source-linked spec rows, source-linked compare cells, decision-table evidence, identity-record fields, plain-text submitted links, five-events-in-`app.js`, collector allow-list, README flag count.
- P-04's short link remains unresolved (checkpoint page, FLG-012). Nothing about the Associate account, tracking or conversion is claimed.

