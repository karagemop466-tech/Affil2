# Affil2 — ShopNow Kitchen

Publication-style Amazon affiliate site: air fryers + meat thermometers compared from official listings.

- Live site: GitHub Pages from `main` (see `.github/workflows/pages.yml`)
- Start: `index.html` · Executive summary: `EXECUTIVE-SUMMARY.md` · Task board: `COORDINATION.md`
- Data: `data/products.json`, `data/sources.json`, `data/flags.json`, `data/events.json`
- Rebuild generated pages: `python3 scripts/build_content.py`
- Check: `python3 scripts/check_site.py`
- Tests: `python3 -m unittest discover -s tests -p "test_*.py"` and `node tests/collector.test.js`

Disclosure on every page: As an Amazon Associate I earn from qualifying purchases.

## Measurement

Five first-party events (`page_view`, `outbound_click`, `guide_read`, `search`,
`suggestion_rank`). The reader-visible counter stays in the reader's own
browser. The server-side collector is self-hosted and ships in two forms:

| Form | File | Run it |
|---|---|---|
| Cloudflare Pages Function | `functions/api/collect.js` | deploy the repo as a Pages project, bind a KV namespace named `EVENT_LOG` |
| Standalone Node server | `analytics/server.js` | `node analytics/server.js` — no npm install, no build step |

Point the site at a collector on another host with
`<meta name="x-collect-endpoint" content="https://collector.example/collect">`.
Until a collector answers the health probe, the client is inert and nothing is
collected. See `measurement.html` and FLG-033.
