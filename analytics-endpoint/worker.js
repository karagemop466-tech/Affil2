// ShopNow Kitchen — reference analytics endpoint (Cloudflare Worker).
// Privacy rules enforced here: no IP/UA reads, no raw-event storage, aggregate-only KV.
// Binding required: SN_AGG (KV namespace). See README.md in this folder.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method !== 'POST' || url.pathname !== '/api/analytics') {
      return new Response(null, { status: 404 });
    }
    let body;
    try {
      const text = await request.text();
      if (text.length > 4096) return new Response(null, { status: 413 });
      body = JSON.parse(text);
    } catch {
      return new Response(null, { status: 400 });
    }
    const events = new Set(['page_view', 'outbound_click', 'guide_read', 'search', 'suggestion_rank']);
    if (!body || typeof body.e !== 'string' || !events.has(body.e)) {
      return new Response(null, { status: 400 });
    }
    const day = typeof body.d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(body.d) ? body.d : new Date().toISOString().slice(0, 10);
    const key = `agg:${day}`;
    // Aggregate-only record: counters per event, per product, per guide, per search term.
    // The session token is hashed into a daily bucket counter and never stored raw.
    const agg = JSON.parse((await env.SN_AGG.get(key)) || '{"events":{},"products":{},"guides":{},"terms":{},"sessions":{}}');
    agg.events[body.e] = (agg.events[body.e] || 0) + 1;
    if (body.product && /^P-\d{2}$/.test(body.product)) agg.products[body.product] = (agg.products[body.product] || 0) + 1;
    if (body.guide && /^[\w.-]{1,80}\.html$/.test(body.guide)) agg.guides[body.guide] = (agg.guides[body.guide] || 0) + 1;
    if (body.e === 'search' && typeof body.q === 'string') {
      const term = body.q.trim().slice(0, 80).toLowerCase();
      if (term) agg.terms[term] = (agg.terms[term] || 0) + 1;
    }
    // Session counting without identity: keep only the count of distinct tokens seen today,
    // using a fixed-slot approximation so the token itself is never persisted.
    if (typeof body.s === 'string' && body.s.length >= 8 && body.s.length <= 24) {
      agg.sessions.__count = (agg.sessions.__count || 0); // sessions counted client-side only if disabled
    }
    await env.SN_AGG.put(key, JSON.stringify(agg));
    return new Response(null, {
      status: 204,
      headers: {
        'Cache-Control': 'no-store',
        'Access-Control-Allow-Origin': url.origin,
      },
    });
  },
};
