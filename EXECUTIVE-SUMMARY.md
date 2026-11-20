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
stripped from shop, category, comparison, search and guide copy, while `flagged.html` (66 flags),
`sources.html` (22 sources) and `verification.html` still publish every one in full. Guide read times are
computed from the page's own words, and all 18 guides and 5 product pages are signed by a dated role
byline that links to the authorship note — no person was named, because the owner has not (FLG-033) and
presenting an invented author would be deceptive. Two new sourced how-to guides were added (the USDA
ice-water calibration test, and how to read a listing's contradictory fields). The Decision Center
shortlist now assembles the next build prompt from one shared payload, identical server-side and in the
browser. One defect of this pass's own making was found by reading the built pages — escaped copy that had
been authored with entities printed its markup to readers — and is fixed plus gated (FLG-057).

Gate and tests at integration: `checked 43 pages, 5 product records, 66 flags, 22 sources —
ALL CHECKS PASS`; 22 Python tests OK; the Node collector/client suite passes. No price, rating, commission figure,
conversion score or revenue forecast was added, and the campaign ledger stays empty.

## Traffic wave, per-product imagery, and the gate that was not running (2026-11-20, session `19dbf5e2` · T-31…T-34)

**Editorial.** Five new question-shaped guides went live for the six weeks of demand that follow
publication — whether a dual basket is worth it, the 165 °F leftover rule, what a certification line on
a spec sheet actually promises, the five checks before gifting an appliance in December, and a
seven-day dry run for a leave-in probe. Guide count: 18. Two further topics this session drafted were
**retired rather than published**, because a parallel session shipped the same topics in the meantime;
their unique substance was folded into the live pages instead of competing with them. Every figure in
the new copy is read from `data/products.json` or the USDA FSIS records in the source register: no
price, no rating, no review count, no cook time, and no claim that anybody here cooked in these units.

**Storefront.** The five products shared two image files across 43 pages. Each now has its own original
rendering on its card, its shop box, its category box and its product page, with matching `og:image`
and `twitter:image`, so a shared page looks like the product rather than like the homepage. No Amazon
photography is used anywhere: the site holds no licence for it, and every image is captioned as an
illustration made for this site.

**Decisions made reviewable.** The Decision Center now opens with three coherent paths — finish the
storefront, grow the traffic, build the machine — each naming what it needs, what it must not do, and
how the owner would know it worked, instead of leaving 46 proposals to be ranked one row at a time.
Six new open questions (Q-24…Q-29) record what only the owner can decide: the masthead and byline,
whether labelled renderings are acceptable, the publishing cadence, the next products, whether cook
times are ever allowed, and whether `osha.gov` may be admitted to the official-source allowlist.

**The significant finding.** `scripts/check_site.py` printed its verdict and exited in the middle of the
file, so the reader-voice, verification-link and findability rules appended below that line ran *after*
the result and could never fail a build — three sessions had cited them as enforcement while they were
unread. Running them honestly produced 97 real defects, all fixed in the generator rather than by
loosening a rule: 44 register rows with no source link (the page promised one in every row), the audit
copy of the product-intent record still printed on all five product pages above the shop-voice version,
and a coverage check that compared an absolute path against a URL prefix so it could never match
(FLG-064, FLG-065, FLG-066). Two of this session's own findings were dropped as duplicates of work a
parallel session had already merged.

Still owner-gated, unchanged, and now recorded in the same place as everything else that is unknown:
the Special Link test (Q-04/FLG-004), Associate ID activity (Q-02/FLG-002), the `link.amazon` short-link
compliance question (Q-03/FLG-003 — not asserted invalid), the short-link re-check that landed on the
Amazon homepage rather than the listings (FLG-051), the domain and brand decision (Q-05/Q-24), Creators
API acceptance (Q-19), Search Console verification (Q-20) and the analytics collector host (SG-25). The
campaign ledger remains empty by design: it is fed only from authorised first-party reports.

Gate and tests after this session: `checked 43 pages, 5 product records, 66 flags, 22 sources —
ALL CHECKS PASS`, every rule reachable; 22 Python tests OK; the Node collector and client suite passes;
two consecutive builds are byte-identical. Deployed to GitHub Pages (`status = built`) and verified on
the live product and guide pages, not only in the repository.
