// ShopNow Kitchen — reference analytics endpoint (Cloudflare Worker, aggregate-only).
//
// Implements the same contract as functions/api/collect.js and analytics/server.js:
//   GET  /api/collect -> 200 {"status":"ok"}   (health probe, stores nothing)
//   POST /api/collect -> 204 accepted, 400 outside the schema, 413 over 4 KB
// The authoritative schema is data/events.json; measurement.html documents it.
//
// Privacy rules enforced here rather than promised in prose:
//   - no IP address or user-agent reads, no raw-event storage, aggregate-only KV
//   - stores daily counters per event, per product, per guide — counters only
//   - never stores a session id (distinct-session counting without identifiers
//     is deliberately not attempted in KV)
//   - never stores the text of a search query: search terms stay ungathered
//     until SG-18 is approved behind Q-08
//   - daily buckets expire after 90 days (documented default; owner may change
//     before deploying — FLG-036 requires the retention decision first)
//
// Binding required: SN_AGG (Workers KV namespace). See README.md in this folder.

const ALLOWED = new Set([
  "page_view",
  "outbound_click",
  "guide_read",
  "search",
  "suggestion_rank",
]);

const NINETY_DAYS = 7776000; // seconds

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/collect") {
      return new Response(null, { status: 404 });
    }
    const cors = {
      "Access-Control-Allow-Origin": url.origin,
      "Cache-Control": "no-store",
    };

    if (request.method === "GET") {
      // Health probe: the browser client sends this once per page load and only
      // switches measurement on when it succeeds.
      return new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== "POST") {
      return new Response(null, { status: 405, headers: cors });
    }

    let body;
    try {
      const text = await request.text();
      if (text.length > 4096) return new Response(null, { status: 413, headers: cors });
      body = JSON.parse(text);
    } catch {
      return new Response(null, { status: 400, headers: cors });
    }
    if (!body || typeof body.event !== "string" || !ALLOWED.has(body.event)) {
      return new Response(null, { status: 400, headers: cors });
    }

    const day =
      typeof body.ts === "string" && /^\d{4}-\d{2}-\d{2}/.test(body.ts)
        ? body.ts.slice(0, 10)
        : new Date().toISOString().slice(0, 10);
    const key = `agg:${day}`;

    const agg = JSON.parse(
      (await env.SN_AGG.get(key)) || '{"events":{},"products":{},"guides":{}}'
    );
    agg.events[body.event] = (agg.events[body.event] || 0) + 1;
    if (typeof body.product_id === "string" && /^P-\d{2}$/.test(body.product_id)) {
      agg.products[body.product_id] = (agg.products[body.product_id] || 0) + 1;
    }
    if (typeof body.path === "string" && /^\/guides\/[\w.-]{1,80}\.html$/.test(body.path)) {
      const slug = body.path.split("/").pop();
      agg.guides[slug] = (agg.guides[slug] || 0) + 1;
    }
    // search: counted as an event only. No term, no length, no result count is
    // written to KV — the counters above are the whole record.

    await env.SN_AGG.put(key, JSON.stringify(agg), { expirationTtl: NINETY_DAYS });
    return new Response(null, { status: 204, headers: cors });
  },
};
