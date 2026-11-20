# Affil2 — ShopNow Kitchen

A static, publication-style Amazon affiliate site covering five submitted products: three air
fryers and two meat thermometers. Specifications are read from the official Amazon listings (including
deep `Product information` tables), dated and linked. Contradictions between listing fields are
printed rather than smoothed over. Prices, star ratings and review counts are deliberately excluded
(Program Policies §2(b), §6(t)).

Live: https://karagemop466-tech.github.io/Affil2/

## Start here

| If you want | Read |
|---|---|
| The short version | `EXECUTIVE-SUMMARY.md` |
| What to decide next | `suggestions.html` — Decision Center, 32 proposals, rankable |
| The next build prompt | `design-brief.html` — design prompt, traffic plan, editorial standards (SG-17) |
| What is still unanswered | `questions.html` — Open Questions, current count on the page |
| What could not be verified | `flagged.html` — Flagged for Review, 51 flags, every one sourced |
| Why crawlers should rank this | `findability.txt` — canonical home, editorial policy, indexable pages, citation form |
| What is still unanswered | `questions.html` — Open Questions, 20 rows |
| What could not be verified | `flagged.html` — Flagged for Review, 47 flags, every one sourced |
| Where every fact came from | `sources.html` — Source Register, 19 official sources + dated changelog |
| AI platform blueprint & gates | `platform.html` — 7-module architecture & Creators API / ML policy limits (SG-31) |
| Telemetry & collector guide | `measurement.html` — 5-event privacy schema & Search Console checklist (SG-25) |
| How the site is built | `scripts/build_site.py` |

## Rebuild and check

    python3 scripts/build_site.py                          # writes 36 pages, sitemap.xml, feed.xml, robots.txt, findability.txt
    python3 scripts/build_site.py                          # writes every page, sitemap.xml, feed.xml, robots.txt
    python3 scripts/check_site.py                          # compliance and integrity gate; exits 1 on any problem
    python3 -m unittest discover -s tests -p "test_*.py" -v
    node tests/test_collector.js                           # collector server, Cloudflare function & client DOM tests

Every HTML page is generated. Do not hand-edit a page: change `data/*.json` or the copy in
`scripts/build_site.py`, rebuild, and commit both. CI fails if the committed pages drift from the
generator output, if the gate fails, or if the unit/collector tests fail.

## Layout

| Path | Holds |
|---|---|
| `data/products.json` | the shared product register: titles, field values, provenance, status |
| `data/editorial.json` | this site's voice: headlines, best-for, trade-offs, FAQ |
| `data/sources.json` | 19 official sources (`S01`–`S04`, `S10`–`S24`) with what each supports and date checked |
| `data/flags.json` | 51 flags (`FLG-001`–`FLG-051`): severity, detail, owner status, source links |
| `data/events.json` | canonical 5-event privacy-preserving measurement schema and forbidden fields |
| `data/reverification-2026-11-20.json` | attempt-by-attempt record of the short-link and deep-table tests |
| `assets/style.css` | storefront stylesheet, including photo-card and diagram styles |
| `assets/photos/` | generated illustrative storefront scenes, captioned on every page that uses them (FLG-036) |
| `assets/illustrations/` | 3 original editorial SVG schematics (`air-fryer.svg`, `air-fryer-oven.svg`, `thermometer.svg`) |
| `assets/app.js` | five measured events, client search (`search.html`), pair compare and the three-question shortlist (`compare.html`), mobile nav toggle, ranking, CSV export, gated `send()` |
| `findability.txt` | generated site profile: canonical home, editorial policy, reader pages vs records, sitemap, feed, citation form, known limits |
| `data/verification-2026-11-20-live.json` | the independent live re-read of all five listings: 33 field rows, each marked verified / conflict / unverified for that pass |
| `analytics/server.js` | zero-dependency Node.js self-hosted collector (`GET`/`POST /api/collect`) |
| `functions/api/collect.js` | drop-in Cloudflare Pages Function collector matching `data/events.json` |
| `scripts/` | single-source generator (`build_site.py`) and compliance gate (`check_site.py`) |
| `tests/` | Python integration tests (`test_site.py`) and Node.js collector/client tests (`test_collector.js`) |

Cross-session rule: `data/products.json`, `data/sources.json` and `data/flags.json` are shared
records. Annotations are added to `data/editorial.json`; shared records are only edited when live
verification shows an inaccuracy or newly confirmed value.

## What this pass changed, and what it did not verify

The storefront pass added a front-page router (four ways in, stated as the reader's situation),
a product line at the end of every guide with one tagged button, and styling for the hero and
guide markup that had been shipping without CSS rules. It also stopped marking FTC, Google, USDA
and Amazon policy citations as `rel="sponsored"` — that attribute belongs on the listings we earn
on, not on the documents a claim is checked against — and removed six image files that nothing
referenced.

**It verified nothing against a live source.** The environment this pass ran in could reach
GitHub and the two package registries only; `amazon.com`, `affiliate-program.amazon.com`,
`ftc.gov`, `developers.google.com` and `fsis.usda.gov` all failed at TLS. Every register value
therefore still rests on the dated reads recorded against S01–S24 by earlier sessions. That limit
is itself published as FLG-045 rather than left implicit, and no `verified` status was added
anywhere on the strength of this pass.

## Rules the gate enforces

- The Amazon Associates statement appears twice on every page, the first time above `<main>`.
- Every `amazon.com` link carries `rel="sponsored nofollow"`; every outbound product link carries the
  tracking ID (`shopnow047c-20`).
- No `$` amount, star rating, review count, cross-row placeholder, or unverified `26.5 lb` claim anywhere.
- No broken internal links, no missing assets, no orphaned SVG illustrations, no root-relative links.
- Every generated photo (`assets/photos/`) has an explicit editorial illustration caption, alt text, and intrinsic dimensions.
- Every `<table>` with `<thead>` matches column counts across all `<tbody>` rows.
- Every page has one `<h1>`, canonical & `og:url` matching its path, valid JSON-LD, and an entry in
  `sitemap.xml`; `feed.xml` parses and its items exist.
- A blank field must be marked `unverified`; a value must name where it was stated.
- Every flag referenced in HTML or `editorial.json` is defined, and every defined flag is published.
- **Reader voice.** No crawl-chunk citation (`chunk 7`) and no bare flag ID (`FLG-0xx`) may appear on
  any reader-facing page — product pages, category pages, guides, `index`, `shop`, `compare`,
  `how-we-choose`, `about`, `disclosure`, `search`. Flags belong on `flagged.html`, where they are
  published in full with their sources. A contradiction a shopper should know about is stated in
  words on the page instead.
- **Findability.** `findability.txt` exists, names the canonical home, and lists every page in
  `sitemap.xml`.
- `assets/style.css` parses (balanced braces, closed `@media` blocks) and every class the generator
  emits has a rule, so a page cannot ship unstyled.
- No image file under `assets/` ships without a page or a generator script referencing it.
- `rel="sponsored"` appears only on `amazon.com/dp/` listings; policy and government citations
  must not claim to be paid placements.
- Every guide ends on a product line with a tagged link, the feed item count matches the guide
  count, and the front page still offers the router.

## Measurement & Collector

Five events — `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank` — are defined
in `data/events.json` and logged in `localStorage` by default. No cookies, no third-party requests,
no fingerprinting, and no raw search text logged (`search` logs query length and hit count only).
Readers can export both click counts and their full event log as CSV on `disclosure.html`.

When deployed outside static GitHub Pages (or configured via `<meta name="sn-collect-endpoint">` or
`localStorage.sn_collect_url`), `send()` in `assets/app.js` transmits schema-validated cookieless
events to either:

    HOST=0.0.0.0 PORT=8787 node analytics/server.js

or `functions/api/collect.js` on Cloudflare Pages (`measurement.html`, `FLG-010`, `Q-08`).

## CI

GitHub Pages publishes this repository with its own branch builder (`main`, `/`). It does not need a
deploy workflow, and `.github/workflows/pages.yml` deliberately does not try to run one; a second
deployer fighting the branch builder is how you get a half-published site.

The workflow is a gate, not a deployer. It regenerates every page and fails if the committed files
differ from the generator, runs `scripts/check_site.py`, and executes both the Python and Node.js
test suites on every push to `main` and every pull request.
