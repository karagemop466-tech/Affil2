# Executive Summary — ShopNow Kitchen

Reviewed 2026-11-20 · Supplied tracking ID `shopnow047c-20` (issuance unverified, FLG-002)
Live site: https://karagemop466-tech.github.io/Affil2/ · Linked version: `executive-summary.html`

## What this is

A static, publication-style Amazon affiliate site covering five submitted products in two
categories: three air fryers and two meat thermometers. Published product facts are read from
official Amazon listing pages, dated, and linked. Where two parts of one listing disagree, both
figures are shown and the disagreement is flagged. No price, star rating, review count, or
best-seller rank is reproduced, consistent with Amazon's Program Policies (§2(b), §6(t); S02).

The pages compare seller-stated details. They are not hands-on tests, do not rank the market, and
do not forecast traffic, conversions, or revenue.

## The five records: observed redirects are not direct-listing references

| ID | Submitted link | Observed short-link target | Direct listing reference |
|----|----------------|---------------------------|--------------------------|
| P-01 | link.amazon/B04G1MEwY | B0CDY277D3 (snapshot, FLG-011) | https://www.amazon.com/dp/B0CDY277D3 |
| P-02 | link.amazon/B02NbDxp3 | B09B7SB46R (snapshot, FLG-011) | https://www.amazon.com/dp/B09B7SB46R |
| P-03 | link.amazon/B00hJ57DV | B08DKYBTPH (snapshot, FLG-011) | https://www.amazon.com/dp/B08DKYBTPH |
| P-04 | link.amazon/B0c8moW59 | — not confirmed; checkpoint page (FLG-012) | https://www.amazon.com/dp/B0DHZTCNR5 |
| P-05 | link.amazon/B0f3GKalj | B0DZFD6R9Z (snapshot, FLG-011) | https://www.amazon.com/dp/B0DZFD6R9Z |

The intended ASIN for every product stays blank until the owner confirms it (FLG-001). A direct
listing page being reachable does not prove a supplied short link resolves there, and no supplied
short link is claimed to be invalid; compliance status remains unresolved (FLG-003, FLG-015).
Redirect behavior varied between attempts (FLG-011), so each observed target is a dated snapshot.

## Sources

Official, dated rows live in `data/sources.json` / `sources.html`: Associates Operating Agreement
and Program Policies, FTC endorsement-disclosure guidance, Google outbound-link guidance, five
direct listing pages, five supplied short-link observations, Creators API eligibility and PA-API
deprecation notices, the USDA FSIS temperature chart, GitHub Pages host documentation, Google
Search Console ownership verification, and the GitHub Pages API response for the current host.
Food-safety temperatures are linked to the USDA chart rather than restated from memory.

## What was corrected in this pass

- Short-link observations and direct listing references are separate fields everywhere; P-04's
  unresolved redirect is no longer filled from its direct listing (FLG-012).
- Buyer-facing copy no longer presents unmeasured superlatives, popularity, or price-effect
  claims; guide titles remain question-shaped editorial hypotheses.
- Every comparison-table row and USDA table row now carries its own official source link.
- The header search no longer puts query text into page HTML: queries travel in a URL fragment,
  render via `textContent`, and are never written to local storage.
- Local measurement stores aggregate counts for the five events only; the old event-by-event log
  (which could contain a query or path) is erased on load.
- The build gate now regenerates in CI and fails on drift, and runs `assets/app.js` syntax plus
  privacy-behavior tests (`scripts/test_analytics.js`).
- FLG-006 corrected: the live GitHub Pages URL is the current canonical host (API: `cname` null,
  HTTPS enforced); a custom domain is optional, not an indexing prerequisite.

## Still open (published on `flagged.html` and `questions.html`)

Intended ASINs (FLG-001) · tracking-ID activity (FLG-002) · short-link compliance (FLG-003) ·
one-per-product Associates Special Link test (FLG-004) · listing conflicts (FLG-008, 009, 017,
018, 019, 021, 031, 034) · no hands-on testing (FLG-032) · no named author (FLG-033) ·
seller-stated certification wording (FLG-035) · browser-local-only counters (FLG-010) ·
Search Console and reader-capture choices (Q-09).

## Measurement and revenue position

Five events — `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank` — are
aggregate counters in each visitor's browser. They are not site-wide analytics and are not sent
anywhere. No conversion, order, or revenue figure appears because no authorized first-party report
exists; `campaign-ledger.html` is empty by design. An empty ledger means no report was entered —
not that visits or orders were zero.

## Owner-level setup before scaling

1. Confirm intended products/ASINs and the tracking ID in Associates Central (Q-01, Q-02).
2. Test one Special Link per product in the enrolled workflow; verify destination and tracking
   report before sending traffic (Q-04, SG-07).
3. Decide whether Search Console verification and any reader-capture channel are wanted (Q-09).
4. Decide on a separate analytics host and privacy policy only if site-wide counts are needed
   (Q-08); GitHub Pages cannot receive event writes.
