# Affil2 — ShopNow Kitchen

Publication-style Amazon affiliate site: **air fryers + meat thermometers** compared from official listings — a shop front, not an audit.

- Live site: GitHub Pages from `main` (`.github/workflows/pages.yml`)
- Start: `index.html` · Executive summary: `EXECUTIVE-SUMMARY.md` · Task board: `COORDINATION.md`
- Reference hub (every dashboard surface in one nav group): `reference.html`
- Registers: `verification.html` (line-by-line verification log), `sources.html`, `flagged.html`, `suggestions.html` (decision gate), `questions.html`, `campaign-ledger.html`
- Data of record: `data/products.json`, `data/sources.json`, `data/flags.json`, `data/verification.json`, `data/campaign-ledger.json`
- Analytics: `assets/app.js` (five defined events, privacy-preserving) + `assets/config.js` (endpoint switch) + `analytics/server.py` (self-hosted collector, see `analytics/README.md`)
- Gate: `python3 scripts/check_site.py` (disclosure, sponsored links, source rows, feed XML, JSON-LD, alt text, sitemap coverage)

**Disclosure on every page:** *As an Amazon Associate I earn from qualifying purchases.* Outbound product links are marked **(paid link)** and carry `rel="sponsored nofollow"`. Prices, ratings and commissions are deliberately not shown (Program Policies §2(b)).

Blank + flagged beats filled-in: if a value cannot be confirmed from an official source, it is left blank and published on [Flagged for Review](flagged.html) with its source links. Short-link (FLG-003) compliance status is **unresolved** — not claimed invalid.
