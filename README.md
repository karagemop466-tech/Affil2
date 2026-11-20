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
| What to decide next | `suggestions.html` — Decision Center, 31 proposals, rankable (each cites its evidence) |
| The next build prompt | `design-brief.html` — design prompt, traffic plan, editorial standards |
| What is still unanswered | `questions.html` — Open Questions, 18 rows |
| What could not be verified | `flagged.html` — Flagged for Review, 42 flags, every one sourced |
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
| `assets/style.css` | storefront stylesheet, including the photo-card layer |
| `assets/photos/` | generated illustrative imagery, captioned on every page that uses it (FLG-036) |
| `scripts/analytics_server.py` | optional, self-hosted collector for the five events (not deployed) |
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
- Every nonblank product-intent field stays separate: intended ASIN, observed redirect target and
  official listing are distinct fields and the gate fails if they are merged or the intended ASIN is
  filled in.
- Every comparison-table product cell links to its source; every Decision Center row cites an
  evidence source; the submitted short link is never rendered as a clickable URL.
- `README.md`'s flag count must equal `data/flags.json`.
- The optional collector must contain the same five events and nothing else.
- Every flag referenced in HTML is defined, and every defined flag is published.

## Measurement

Five events — `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank` — are counted
in localStorage only. No cookies, no third-party requests, no analytics script ships with the site.
The `search` event records that a search ran and how many results it returned, never the query
words. Readers can export their own event log (Disclosure page) and click counts as CSV.

`scripts/analytics_server.py` is an optional, self-hosted collector for the same five events. It
stores per-day aggregate counts only — no identifier, cookie, IP address, user agent or raw search
term — and it is not deployed or wired to any page. If it is ever deployed behind HTTPS at a
same-origin route, the disclosure must be updated before any event is sent (SG-25).

Hosting note: this site is served by GitHub Pages, which documents IP-address logging for security
purposes; the disclosure distinguishes that from the site's local browser events. Whether Pages is
the right host for a commercial-affiliate publication is an open question tracked as FLG-041/SG-31.

## Deprecated

`scripts/build_content.py` is a deprecated shim that delegates to `scripts/build_site.py`; it does
nothing else and should not be extended.

## CI

GitHub Pages publishes this repository with its own branch builder (`main`, `/`). It does not need a
deploy workflow, and `.github/workflows/pages.yml` deliberately does not try to run one; a second
deployer fighting the branch builder is how you get a half-published site.

The workflow is a gate, not a deployer. It regenerates every page and fails if the committed files
differ from the generator, then runs `scripts/check_site.py`. It runs on every push to `main` and on
every pull request, so a change that breaks either step is visible before it merges.
