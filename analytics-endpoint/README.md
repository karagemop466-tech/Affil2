# Self-hosted analytics endpoint — contract & deployable reference

Status: **spec + reference implementation shipped; deployment is owner-gated** (Q-08, FLG-010).
Until an endpoint is live at `https://<your-host>/api/analytics`, the site's measurement layer
works entirely in the visitor's browser (localStorage) and every beacon fails silently.

## The five defined events

| Event | Fired when | Payload fields |
|---|---|---|
| `page_view` | any page load | `p` (path) |
| `guide_read` | a `guides/*.html` page load | `p`, `guide` (slug) |
| `outbound_click` | a marked Amazon link click | `p`, `product` (P-01…P-05) |
| `search` | search page load with `?q=` or search submit | `p`, `q` (query, truncated to 80 chars) |
| `suggestion_rank` | a suggestions ranking change | `p`, `top` (top-5 suggestion ids) |

Every beacon also carries: `s` (random session token, regenerated per tab, never persisted
client-side), `d` (UTC date, YYYY-MM-DD).

## Privacy rules (hard requirements for any deployment)

1. **No cookies, no localStorage/IDB identifiers sent to the server.** The session token is
   random, memory-only, and rotated per tab session. It supports counting sessions per day —
   it cannot identify a person.
2. **No IP logging.** The reference worker below does not read or store IP addresses or
   user-agent strings. If your host logs IPs by default, disable it for this route.
3. **No third parties.** The endpoint is first-party only; no analytics vendors, no ad tags.
4. **Retention 90 days** for raw events; daily aggregates may be kept indefinitely
   (counts only — no strings beyond `guide` slugs and `product` ids).
5. **Search queries** are kept only as daily aggregate terms (no session binding) so editorial
   topics can be chosen from measured queries. Purge terms on request.

## Request contract

`POST /api/analytics` — `Content-Type: application/json`, body = one event object (above).
Respond `204` on success, `400` on malformed body, `413` over 4 KB. CORS: same-origin only.

## Reference implementation (`worker.js`)

A dependency-free Cloudflare Worker that stores **daily aggregate counts** in KV
(`sn_agg` key per day). It deliberately does not store raw events. Deploying it is one
candidate path for Q-08 — any host that can expose `POST /api/analytics` under the same
rules is equally valid.

```bash
# Cloudflare wrangler example (owner-run; requires a Cloudflare account)
wrangler kv namespace create SN_AGG
# put the id into worker.js bindings, then:
wrangler deploy analytics-endpoint/worker.js --name shopnow-analytics --compatibility-date 2026-11-20
```

Then point the site at it: the client posts to the **relative** path `api/analytics`, so a
reverse-proxy route from the site host to the worker keeps everything first-party.

## Measurement-to-decision loop (what the data is for)

1. Baseline: `page_view` + `search` per guide → which questions bring people in.
2. `outbound_click` per product → which picks earn interest (NOT revenue — see below).
3. `suggestion_rank` + decision form exports → the change log for the next build.
4. **Orders/revenue come only from authorized first-party Associates reports** and go into
   `data/campaign-ledger.json` with dated provenance. No conversion score or revenue
   forecast is computed on this site, and none should be inferred from click counts.
