# Executive Summary — ShopNow Kitchen (Affil2)

Last updated: 2026-11-20 · Tracking ID supplied: `shopnow047c-20` (UNVERIFIED — FLG-002) · Sessions: 530c2e6c (build), bba2deed (verification + publication passes)

## What this is
A publication-style Amazon affiliate site (static HTML on GitHub Pages) covering 5 submitted links in 2 categories: 3 air fryers (P-01…P-03) and 2 meat thermometers (P-04…P-05). The landing page leads with products and buyer questions ("shop, not audit"); every dashboard surface lives behind one Reference group + the footer. Disclosure sits above the fold on every page and repeats in the footer; every outbound product link is marked **(paid link)** with `rel="sponsored nofollow"`.

## Verified against official sources (2026-11-20, line-by-line)
Full ledger: `verification.html` / `data/verification.json`. Method legend and per-value status are on those pages.

- All five titles, capacities, dimensions and headline specs re-read from the official Amazon listings (S10–S14).
- S01 (Operating Agreement §5 disclosure wording), S03 (FTC endorsement guidance) and S04 (Google `rel="sponsored"`) confirmed from the official pages; S02 (Program Policies §2(b) price rule) corroborated with the official URL left for manual review.
- Confirmed conflicts re-verified live: P-02 preset count 24 vs 25 and model variants (FLG-009); P-05 battery 50 h vs 70 h (FLG-008).

## New findings this pass (all published on Flagged for Review)
- **FLG-011** — P-03 wattage conflict: live listing bullet says "1000 Watts/120 Volts – RJ38-SQSS-8T"; product-info mirrors and the Chefman manual say 1700 W. Both published; neither chosen.
- **FLG-012** — P-03 title drift ("TurboFry Touch" → "TurboFry 4-in-1 with 450°F Hi-Fry Option") + title's 450°F Hi-Fry vs bullet's 200–400°F range. Both published.
- **FLG-013** — P-05 warranty corrected: register's "1-year" claim was unconfirmed; the listing states a "two-year assurance" (corroborated). Prior value recorded as unconfirmed.

## Corrections made (C-01…C-07, see verification.html)
P-03 power display, P-05 warranty, three title normalizations, feed.xml malformed `<language>` tag (now valid XML), missing JSON-LD (now shipped), and stale flag cross-references in COORDINATION.md.

## Shipped this pass
- **Publication polish**: image hero, editorial imagery (original artwork — FLG-007), seasonal band + Holiday 2026 cluster, bylines, Reference navigation group, reader-capture module (RSS-first).
- **Two seasonal question-shaped guides** (`guides/holiday-capacity.html`, `guides/holiday-roast-thermometer.html`), added to sitemap + RSS feed. Publishing cadence documented: 2 guides/month + seasonal clusters.
- **Measurement**: five defined events (`page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank`), privacy-preserving client (no cookies/PII/search strings), self-hosted endpoint shipped in `analytics/` and tested end-to-end (whitelist, aggregates, no-IP design). Production deployment is gated on Q-08; the switch is one line in `assets/config.js`.
- **Registers**: SG-27…SG-30 rows (nav labels, RSS, Search Console prep, reader capture), Q-13…Q-16 (five-events confirmation, imagery rights, ledger report access, conflicted-spec policy).
- **Machine gate**: `scripts/check_site.py` now also verifies feed XML well-formedness, JSON-LD, per-row source links in every data table, image alt text, SG-27..30 presence, and the analytics surface. All 29 pages pass.

## Not verified / gated (do not block)
Intended ASINs (FLG-001), tracking-ID issuance (FLG-002), short-link compliance (FLG-003 — unresolved, **not** claimed invalid), Special Link one-per-product tests (FLG-004, needs the enrolled Associates account), prices/ratings/commissions (FLG-005, deliberately blank per S02), canonical host (FLG-006), licensed product photos (FLG-007), the listing conflicts above (FLG-008/009/011/012/013), analytics endpoint host (FLG-010, Q-08), Search Console + email provider (Q-09).

## Next decisions for the owner
Answer Q-01…Q-04 (intent, tracking ID, short links, link tests), rank SG-01…SG-30 on `suggestions.html`, choose the analytics host (Q-08) and reader-capture provider (Q-09), then test one Special Link per product before scaling.
