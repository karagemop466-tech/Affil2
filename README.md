# Affil2 — Countertop Journal (working title)

A static affiliate buyer-guide site for the supplied Amazon links (air fryers and multi-function kitchen appliances). Hosted with GitHub Pages from `docs/`.

Live site (after deploy): https://karagemop466-tech.github.io/Affil2/

## What is here

| Path | What it is |
|---|---|
| `docs/` | Generated site. This is the GitHub Pages source. Do not edit by hand. |
| `data/*.json`, `data/campaign-ledger.csv` | All content and verification data. Edit these, then rebuild. |
| `tools/build_site.py` | Builds `docs/` from `data/` (no dependencies; Python 3). |
| `tools/check_site.py` | Integration checks: disclosure on every page, no broken links, `rel="sponsored"` on affiliate links, source link on every product row, intent fields not merged or guessed, sitemap/feed valid. |
| `COORDINATION.md` | Shared task board, claims, log, and handoffs. |

## Rebuild and check

```bash
python3 tools/build_site.py
python3 tools/check_site.py
```

## Rules this site follows

- Associates identification statement, verbatim, under the masthead and in the footer of every page (Operating Agreement §5).
- Affiliate links carry `rel="sponsored"` (Google guidance).
- Intended product fields (ASIN, listing URL, confirmation date/source) stay blank until confirmed. Observed redirect targets are kept in separate fields.
- Blank data is shown blank and marked unverified. Nothing is inferred.
- No click, conversion, revenue, or commission figures are shown. The campaign ledger is empty by design.

## Not live yet

- Outbound click and conversion events: the hook exists (`docs/assets/track.js`) but is disabled. GitHub Pages cannot store events. See Suggestions S-01.
- Associates Special Link test, tracking-ID validation, and Search Console verification need owner accounts. See Flagged for Review.

## Sources

Official sources, with the date checked and what was verified, are on the site's Sources page (`docs/sources/`) and in `data/sources.json`.
