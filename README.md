# Affil2 — ShopNow Kitchen

A static, publication-style Amazon affiliate site covering five submitted products: three air
fryers and two meat thermometers. Specifications are read from the official Amazon listings, dated
and linked. Contradictions between listing fields are printed rather than smoothed over. Prices,
star ratings and review counts are deliberately excluded (Program Policies §2(b), §6(t)).

Live: https://karagemop466-tech.github.io/Affil2/

## Start here

| If you want | Read |
|---|---|
| The short version | `EXECUTIVE-SUMMARY.md` |
| What to decide next | `suggestions.html` — Decision Center, 30 proposals, rankable |
| The next build prompt | `design-brief.html` — design prompt, traffic plan, editorial standards (SG-17) |
| What is still unanswered | `questions.html` — Open Questions, 14 rows |
| What could not be verified | `flagged.html` — Flagged for Review, 36 flags |
| Where every fact came from | `sources.html` — source register |
| How measurement works | `measurement.html` — five events, collector contract, privacy |
| The machinery, stage by stage | `platform.html` — automation design, gated (SG-12) |
| How the site is built | `scripts/build_site.py` |

## Rebuild and check

    python3 scripts/build_site.py   # writes all pages, sitemap.xml, feed.xml, robots.txt
    python3 scripts/check_site.py   # compliance and integrity gate; exits 1 on any problem
    node tests/collector.test.js    # 13 checks: schema agreement and sanitisation rules
    python3 -m unittest discover -s tests -p "test_*.py" -v   # 22 site tests

Every HTML page is generated. Do not hand-edit a page: change `data/*.json` or the copy in
`scripts/build_site.py`, rebuild, and commit both. CI fails if the committed pages drift from the
generator output, and again if the gate fails.

## Layout

| Path | Holds |
|---|---|
| `data/products.json` | the shared product register: titles, field values, provenance, status |
| `data/editorial.json` | this site's voice: headlines, best-for, trade-offs, FAQ |
| `data/sources.json` | every source with what it supports and the date checked |
| `data/flags.json` | the flag register: severity, detail, resolution, source links |
| `data/events.json` | the five-event schema — the contract every collector implements |
| `data/reverification-2026-11-20.json` | attempt-by-attempt record of the short-link tests |
| `functions/api/collect.js` | collector, Cloudflare Pages Function (ships, not deployed) |
| `analytics/server.js` | collector, dependency-free Node server (ships, not deployed) |
| `analytics-endpoint/worker.js` | collector, aggregate-only Cloudflare Worker (ships, not deployed) |
| `assets/js/collect.js` | browser client: probes the collector once, inert while none answers |
| `assets/style.css` | storefront stylesheet (Fraunces + Inter) |
| `assets/app.js` | five measured events locally, search, ranking, CSV export |
| `tests/` | collector tests and site tests (unittest) |
| `scripts/` | generator and gate |

Cross-session rule: `data/products.json`, `data/sources.json` and `data/flags.json` are shared
records. Annotations are added to `data/editorial.json`; shared records are only edited when their
content is wrong.

## Rules the gate enforces

- The Amazon Associates statement appears twice on every page, the first time above `<main>`.
- Every Amazon product **buy link** carries the tracking ID and `rel="sponsored nofollow"`; every
  `link.amazon` short link carries `rel="sponsored nofollow"`. Labelled verification links to a
  listing (never a CTA) are marked sponsored but may be untagged — that is this site's published
  policy.
- No `$` amount, star rating or review count anywhere (patterns checked broadly).
- No broken internal links, no missing assets, no root-relative links, no Amazon-hosted imagery.
- Every page has one `<h1>`, a canonical matching its path, JSON-LD that parses, the brand font
  stylesheet, the collector client, and an entry in `sitemap.xml`; `feed.xml` parses and its items
  exist and cover every guide.
- A blank field must be marked `unverified`; a value must name where it was stated.
- Every flag referenced in HTML is defined, and every defined flag is published.
- `(paid link)` appears near every tagged buy link; the five event names are instrumented.

## Measurement

Five events — `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank` — counted in
the reader's own browser (localStorage only: clearable, exportable as CSV). The network half is
`assets/js/collect.js`: it probes `/api/collect` once per page and stays inert while no collector
answers, so the live site records nothing server-side today. Three deployable implementations ship
in the repository — `functions/api/collect.js` (Cloudflare Pages Function), `analytics/server.js`
(dependency-free Node server) and `analytics-endpoint/worker.js` (aggregate-only Worker, counters
only, 90-day expiry) — all implementing the schema in `data/events.json`. Search text is never
stored; search-term aggregation stays ungathered behind SG-18/Q-08. Deployment, host and retention
are owner decisions (FLG-036, Q-08). Details: `measurement.html`.

## CI

GitHub Pages publishes this repository with its own branch builder (`main`, `/`). It does not need a
deploy workflow, and `.github/workflows/pages.yml` deliberately does not try to run one; a second
deployer fighting the branch builder is how you get a half-published site.

The workflow is a gate, not a deployer. It regenerates every page and fails if the committed files
differ from the generator, then runs `scripts/check_site.py`, the collector tests and the site
tests. It runs on every push to `main` and on every pull request, so a change that breaks any step
is visible before it merges.
