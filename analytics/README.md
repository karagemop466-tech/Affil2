# Self-hosted analytics endpoint (T-12)

A tiny, dependency-free collector for the site's **five defined events**:
`page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank`.

## Privacy design (what makes it privacy-preserving)

| Rule | How |
|---|---|
| No cookies / no identifiers | The client never sets or sends an ID; payloads are event + path + coarse props only |
| No IP collection | The server never reads the request address and writes **no access log** |
| No referrers / search strings / free text | `search` events carry a result count, never the query; paths are whitelisted by regex |
| Minimal retention | JSONL by month, aggregates only in `/v1/stats`; delete the folder to erase everything |
| One origin | `ALLOWED_ORIGIN` restricts CORS to the site's own origin |

This is the endpoint referred to as Q-08 / FLG-010. GitHub Pages cannot host it
(static hosting only), so it is deployed separately and its URL is switched on in
`assets/config.js` (`analyticsEndpoint`). Until then the client keeps events in the
visitor's own browser (localStorage) with a CSV export — no data leaves the device.

## Run it

```bash
python3 analytics/server.py --port 8787
# ALLOWED_ORIGIN=https://your-host python3 analytics/server.py   # for production
```

## Test it

```bash
curl -s -X POST http://127.0.0.1:8787/v1/events \
  -H 'Content-Type: application/json' \
  -d '{"events":[{"e":"page_view","p":"/","t":0},{"e":"outbound_click","p":"/","product":"P-01"}]}'
curl -s http://127.0.0.1:8787/v1/stats
```

## Production deployment checklist (gated — Q-08)

1. Pick a host you control (a $0–5 VPS, Fly.io, Cloudflare Workers + KV, etc.).
2. Set `ALLOWED_ORIGIN` to the site origin; serve behind HTTPS.
3. Set `analyticsEndpoint` in `assets/config.js` to `https://<host>/v1/events`.
4. Confirm in `/v1/stats` that events arrive and that **no** IP/referrer fields exist in the JSONL.
5. Update `disclosure.html` ("analytics status") and close FLG-010 in `data/flags.json`.
6. Decide retention (default: keep 3 months of JSONL) and put it in the privacy note.

The `data/` folder inside `analytics/` is generated at runtime and is git-ignored.
