# Affil2 — ShopNow Kitchen

A static, publication-style Amazon affiliate site covering five submitted products: three air
fryers and two meat thermometers. Specifications are read from the official Amazon listings (including
the deep `Product information` tables), dated and linked. Contradictions between listing fields are
printed rather than smoothed over. Prices, star ratings and review counts are deliberately excluded
(Program Policies §2(b), §6(t)).

Live: https://karagemop466-tech.github.io/Affil2/

## Start here

| If you want | Read |
|---|---|
| The short version | `EXECUTIVE-SUMMARY.md` |
| What to decide next | `suggestions.html` — Decision Center, 20 proposals, rankable |
| What is still unanswered | `questions.html` — Open Questions, 16 rows |
| What could not be verified | `flagged.html` — Flagged for Review, 35 items |
| Where every fact came from | `sources.html` — Source Register, 18 official sources |
| AI platform blueprint & gates | `platform.html` — 7-module architecture & Creators API / ML policy limits |
| Telemetry & collector guide | `measurement.html` — 5-event privacy schema & Search Console checklist |
| How the site is built | `scripts/build_site.py` |

## Rebuild and check

    python3 scripts/build_site.py                          # writes 31 pages, sitemap.xml, feed.xml, robots.txt
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
| `data/sources.json` | 18 official sources with what each supports and the date checked |
| `data/flags.json` | 35 flags: severity, detail, owner status, source links |
| `data/events.json` | canonical 5-event privacy-preserving measurement schema and forbidden fields |
| `data/reverification-2026-11-20.json` | attempt-by-attempt record of the short-link and deep-table tests |
| `assets/style.css` | storefront stylesheet |
| `assets/app.js` | five measured events, client search (`search.html`), mobile nav toggle, ranking, CSV export, `send()` transport |
| `assets/illustrations/` | 3 original editorial SVG illustrations (not product photography) |
| `analytics/server.js` | zero-dependency Node.js self-hosted collector (`GET`/`POST /api/collect`) |
| `functions/api/collect.js` | drop-in Cloudflare Pages Function collector matching `data/events.json` |
| `scripts/` | single-source generator (`build_site.py`) and compliance gate (`check_site.py`) |
| `tests/` | Python integration tests (`test_site.py`) and Node.js collector/client tests (`test_collector.js`) |

Cross-session rule: `data/products.json`, `data/sources.json` and `data/flags.json` are shared
records. Annotations are added to `data/editorial.json`; shared records are only edited when live
verification shows an inaccuracy or newly confirmed value.

## Rules the gate enforces

- The Amazon Associates statement appears twice on every page, the first time above `<main>`.
- Every `amazon.com` link carries `rel="sponsored nofollow"`; every outbound product link carries the
  tracking ID (`shopnow047c-20`).
- No `$` amount, star rating, review count, or unverified `26.5 lb` claim anywhere.
- No broken internal links, no missing assets, no orphaned SVG illustrations, no root-relative links.
- Every `<table>` with `<thead>` matches column counts across all `<tbody>` rows.
- Every page has one `<h1>`, canonical & `og:url` matching its path, valid JSON-LD, and an entry in
  `sitemap.xml`; `feed.xml` parses and its items exist.
- A blank field must be marked `unverified`; a value must name where it was stated.
- Every flag referenced in HTML or `editorial.json` is defined, and every defined flag is published.

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
