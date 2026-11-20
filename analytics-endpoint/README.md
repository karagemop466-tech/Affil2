# Self-hosted analytics endpoint — contract & deployable references

Status: **spec + three reference implementations shipped; deployment is owner-gated**
(Q-08, FLG-010, FLG-036). GitHub Pages serves static files only, so nothing here runs
until the owner deploys one implementation and points the site at it. Until then the
browser client (`assets/js/collect.js`) probes once per page, gets no answer, and stays
inert: the live site collects nothing server-side.

The single source of truth for the schema is `data/events.json`; the reader-facing
description is `measurement.html`.

## The contract (identical for all three implementations)

- `GET /api/collect` → `200 {"status":"ok"}` — health probe, stores nothing. The client
  sends it once per page load and only enables measurement when it succeeds.
- `POST /api/collect` → `204` accepted, `400` for anything outside the schema,
  `413` for bodies over 4 KB.
- Same-origin by default. A deployment that separates site and collector points the
  site at it with `<meta name="x-collect-endpoint" content="https://collector.example/collect">`.

| Implementation | File | Storage | How to run it |
|---|---|---|---|
| Cloudflare Pages Function | `functions/api/collect.js` | Workers KV binding `EVENT_LOG` (optional) | Deploy the repo as a Cloudflare Pages project and bind the namespace; the route answers probe and sink. |
| Standalone Node server | `analytics/server.js` | newline-delimited JSON in a local file | `PORT=8787 LOG=./analytics/events.ndjson node analytics/server.js` — no npm install, no build step. |
| Cloudflare Worker, aggregate-only | `analytics-endpoint/worker.js` | daily counters in KV binding `SN_AGG`, 90-day expiry | `wrangler kv namespace create SN_AGG`, put the id into the binding, then `wrangler deploy analytics-endpoint/worker.js --name shopnow-analytics --compatibility-date 2026-11-20`. |

## The five defined events

| Event | Fired when | Payload fields (besides `event`, `path`, `session_id`, `ts`) |
|---|---|---|
| `page_view` | any page load | `referrer_host` (bare hostname of a different site, or empty) |
| `outbound_click` | a marked Amazon buy link is clicked | `product_id` (P-01…P-05), `link_position` |
| `guide_read` | the footer of a guide scrolls into view | — |
| `search` | a search results page has a query | `query_length`, `result_count` — never the words typed |
| `suggestion_rank` | a suggestion is moved up or down | `suggestion_id`, `position` |

## Privacy rules (hard requirements for any deployment)

1. **No cookies, no identifiers sent to the server.** The session id is random per page
   load and dies with the tab; it lets a server count sessions, not people.
2. **No IP logging, no user agent.** The references never read them; if your host logs
   IPs by default, disable it for this route.
3. **No third parties.** First-party only; no analytics vendors, no ad tags.
4. **Search text is never stored.** The reader-visible local counter may log a query in
   the reader's own browser (they can clear or export it), but no server in this
   repository accepts or keeps query text. Search-term aggregation stays ungathered
   until SG-18 is approved behind Q-08.
5. **Retention before collection.** The Worker's daily aggregates expire after 90 days;
   the Node file grows until rotated. Choose the retention period (FLG-036) before
   pointing the site at anything.

## Measurement-to-decision loop (what the data is for)

1. Baseline: `page_view` + `search` per guide → which questions bring people in.
2. `outbound_click` per product → which picks earn interest (NOT revenue — see below).
3. `suggestion_rank` + decision form exports → the change log for the next build.
4. **Orders/revenue come only from authorized first-party Associates reports** and go into
   the campaign ledger with dated provenance. No conversion score or revenue
   forecast is computed on this site, and none should be inferred from click counts.

## Tests

```bash
node tests/collector.test.js      # 13 checks: schema agreement and sanitisation
python3 -m unittest discover -s tests -p "test_*.py" -v
```
