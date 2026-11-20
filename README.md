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
| What to decide next | `suggestions.html` — Decision Center, 16 proposals, rankable |
| What is still unanswered | `questions.html` — Open Questions, 14 rows |
| What could not be verified | `flagged.html` — Flagged for Review, 33 items |
| Where every fact came from | `sources.html` — source register |
| How the site is built | `scripts/build_site.py` |

## Rebuild and check

    python3 scripts/build_site.py   # writes all pages, sitemap.xml, feed.xml, robots.txt
    python3 scripts/check_site.py   # compliance and integrity gate; exits 1 on any problem

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
| `data/reverification-2026-11-20.json` | attempt-by-attempt record of the short-link tests |
| `assets/style.css` | storefront stylesheet |
| `assets/app.js` | five measured events, search, ranking, CSV export |
| `scripts/` | generator and gate |

Cross-session rule: `data/products.json`, `data/sources.json` and `data/flags.json` are shared
records. Annotations are added to `data/editorial.json`; shared records are only edited when their
content is wrong.

## Rules the gate enforces

- The Amazon Associates statement appears twice on every page, the first time above `<main>`.
- Every amazon.com link carries `rel="sponsored nofollow"`; every outbound product link carries the
  tracking ID.
- No `$` amount, star rating or review count anywhere.
- No broken internal links, no missing assets, no root-relative links.
- Every page has one `<h1>`, a canonical matching its path, JSON-LD that parses, and an entry in
  `sitemap.xml`; `feed.xml` parses and its items exist.
- A blank field must be marked `unverified`; a value must name where it was stated.
- Every flag referenced in HTML is defined, and every defined flag is published.

## Measurement

Five events — `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank` — counted in
localStorage only. No cookies, no third-party requests, no analytics script. Readers can export
their own event log and click counts as CSV. A self-hosted collector is one function away in
`assets/app.js` (`send()`), and the privacy statement that must ship with it is drafted in
`disclosure.html` (FLG-010).

## CI

`.github/workflows/pages.yml` has two jobs. `verify` regenerates every page and fails if the
committed files differ from the generator, then runs `scripts/check_site.py`. `deploy` runs only on
`main` and only if `verify` passed. The workflow also runs on pull requests, so a change that breaks
the gate is caught before merge.
