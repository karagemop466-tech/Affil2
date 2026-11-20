# Executive Summary — ShopNow Kitchen

**Updated:** 2026-11-20
**Live:** https://karagemop466-tech.github.io/Affil2/
**Selected tracking ID:** `shopnow047c-20` (issuance/activity unconfirmed; see FLG-002)

## What is published

ShopNow Kitchen is a static Amazon affiliate publication for five submitted product links: three air fryers and two meat thermometers. The publication includes category shelves, product pages, comparison and shortlist tools, question-shaped buying guides, a suggestions/decision center, an open-questions register, an empty campaign ledger, and a clearly labeled Flagged for Review page.

The site prioritizes useful purchase questions and official-listing facts. No hands-on testing is represented. Prices, ratings, review counts, sales ranks, commission estimates, forecasts, and conversion scores are omitted. Unconfirmed fields remain blank and are identified as unverified. Product links carry `rel="sponsored nofollow"`; the disclosure sits below the masthead and repeats in every footer.

## Submitted links and observed destinations

| Product | Submitted URL | Observed ASIN | Official listing |
|---|---|---|---|
| P-01 | https://link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 |
| P-02 | https://link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R |
| P-03 | https://link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH |
| P-04 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 |
| P-05 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z |

Observed destinations are recorded separately from owner-confirmed intent. The owner has not confirmed intended ASINs. The short-link format's status is unresolved; this summary does not characterize the supplied URLs as invalid. Before scaling, test one compliant Special Link per product in the enrolled Associates workflow and check its destination and account report (FLG-001, FLG-003, FLG-004).

## Evidence and open gates

The product facts and their provenance are in `data/products.json`; official sources are catalogued in `data/sources.json`. Listing contradictions and other unresolved matters are published on `flagged.html`. The 51-item review register is generated from `data/flags.json`; 19 official source records are listed in `sources.html`. Dates refer to evidence capture, not an assurance that a listing never changes.

Key owner-gated items: confirm intended products, confirm tracking-ID access/activity, perform the enrolled Special Link test, provide first-party reporting before entering campaign results, configure analytics hosting if cross-visitor measurement is wanted, and verify Search Console before using query data to select future articles. The campaign ledger remains empty by design. No revenue or conversion rate is claimed.

Amazon Associates' official agreement and policies, the FTC Endorsement Guides FAQ, Google's outbound-link guidance, and USDA FSIS food-safety guidance are linked from `sources.html` and `README.md` for manual review. The current policies must be reread before operational scaling; this publication is not legal advice.

## Build and publication status

The static site generator is `scripts/build_site.py`; `scripts/check_site.py` enforces disclosure, affiliate-link marking, sourced data, completeness of review flags, and page integrity. Python integration tests and Node collector/client tests are in `tests/`. GitHub Pages currently reports a successful build on `main` at https://karagemop466-tech.github.io/Affil2/.

To rebuild and validate locally:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
node tests/test_collector.js
```

## Practical next decisions

1. In the enrolled Associates account, validate a Special Link for each intended product before promoting it.
2. Verify tracking ID issuance and inspect first-party reports; keep the campaign ledger empty until eligible sessions, clicks, orders, and revenue are available with provenance.
3. Decide whether to host the prepared collector and verify Search Console. Do not describe either as active until independently confirmed.
4. Review article topics and publication cadence in `suggestions.html`; use real query data once available rather than asserting trend or conversion potential without evidence.
5. Recheck listing claims and policy sources whenever products or operational practices change.

## Reader-surface pass (2026-11-20, session `93894704` · T-30)

Buyer-facing pages no longer carry the project's filing system: register codes and crawl citations were
stripped from shop, category, comparison, search and guide copy, while `flagged.html` (58 flags),
`sources.html` (22 sources) and `verification.html` still publish every one in full. Guide read times are
computed from the page's own words, and all 13 guides and 5 product pages are signed by a dated role
byline that links to the authorship note — no person was named, because the owner has not (FLG-033) and
presenting an invented author would be deceptive. Two new sourced how-to guides were added (the USDA
ice-water calibration test, and how to read a listing's contradictory fields). The Decision Center
shortlist now assembles the next build prompt from one shared payload, identical server-side and in the
browser. One defect of this pass's own making was found by reading the built pages — escaped copy that had
been authored with entities printed its markup to readers — and is fixed plus gated (FLG-057).

Gate and tests at integration: `checked 38 pages, 5 product records, 58 flags, 22 sources — ALL CHECKS
PASS`; 7 Python tests OK; the Node collector/client suite passes. No price, rating, commission figure,
conversion score or revenue forecast was added, and the campaign ledger stays empty.
