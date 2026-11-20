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

P-04's certification is a seller-stated claim (NIST and NSF), not an independently verified certificate (FLG-035); its upper temperature is blank because the retrieved text did not confirm one (FLG-022).

## Corrections recorded this pass (not current conflicts)
- FLG-017 (P-03 wattage): an earlier register carried 1700 W; the current About this item excerpt states 120 V / 1000 W. Corrected; the 1700 W figure is not presented as a live same-page conflict.
- FLG-019 (P-05 warranty): an earlier register carried one year; the current About this item text states two-year assurance. Corrected.
- FLG-008 (P-05 battery): current About this item text states up to 50 hours per charge; an earlier capture recorded 70 hours that was not reproduced in review scope here. 50 hours is the only current statement kept; the earlier record is retained in the flag register for traceability.
- FLG-009 (P-02 model): variant numbers from an earlier capture were not re-confirmed and the field is blank.
- FLG-028 (legacy source IDs): S24 is now assigned (Search Console overview); S07 remains unused; no current claim depends on it.

## Hosting and measurement — open, not assumed
- GitHub Pages is configured (source `main`, `/`, HTTPS enforced) — configuration checked 2026-11-20 via the GitHub API. The public limits documentation states Pages is not intended or allowed as free hosting for sites primarily directed at commercial transactions; whether this affiliate publication fits is an unresolved policy question (FLG-036, SG-27), not a finding that a violation occurred. Owner should assess classification or migrate before directing purchase traffic.
- GitHub Pages documentation says visitor IP addresses are logged and stored for security purposes; the site disclosure distinguishes GitHub's host-side logs from the site's local browser events (FLG-037). The owner should review whether any additional privacy step is needed.
- Five events (`page_view`, `guide_read`, `outbound_click`, `search`, `suggestion_rank`) are counted in localStorage only; nothing is transmitted as the site ships. An optional, self-hosted collector (`scripts/analytics_server.py`) implements the same five events as daily aggregate counts without identifiers — it is not deployed and not wired to any page; if deployed, the disclosure must be updated first (SG-30).
- The campaign ledger is empty by design and stays empty until an authorized first-party report provides rows (SG-07, SG-29). No click, session, conversion or revenue figure is presented, and none may be inferred.
- Search Console verification would make query data available (SG-28); nothing about search demand is claimed yet.

## Not verified, and published as such
Intended ASINs for all five products (FLG-001) · whether the tracking ID is live and recorded (FLG-002) · short-link compliance status (FLG-003) · the one-per-product Special Link test (FLG-004, SG-29) · certification documents (FLG-035) · hands-on experience (FLG-032) · a named editor (FLG-033) · several model numbers/weights/temperatures not confirmed in retrieved listing text (FLG-022 and product blanks) · full live-page transcripts — listings are dynamic; this pass reviewed available excerpts (FLG-023).

## Decision Center additions this pass
SG-27 (hosting fit review before promotion), SG-28 (Search Console verification before expanding guides), SG-29 (confirm intent + test each Special Link in Associates Central), SG-30 (choose endpoint hosting/retention before any event leaves the device), SG-31 (re-read the five listings end to end). Each cites its evidence in the Decision Center table. Nothing self-applies.

## How the site is kept honest
`scripts/build_site.py` generates every page from `data/*.json`; `scripts/check_site.py` fails the build on missing disclosure, sponsorship/tag errors, prices, star ratings, review counts, broken links, sitemap/feed drift, unsourced spec rows, missing decision-table evidence, or intent/observed field removal. The CI workflow regenerates and gates on PRs to `main` (it is a verifier, not a deployer; Pages' own branch builder publishes `main`).

## Honest position on revenue
Zero, with no forecast. No commission rate, click, conversion or earnings figure can be obtained from an authorized first-party report yet. `campaign-ledger.html` is intentionally empty with its schema and provenance rule documented.
