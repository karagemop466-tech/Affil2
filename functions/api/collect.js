/**
 * Cloudflare Pages Function — privacy-preserving analytics collector (/api/collect).
 * Mirrors analytics/server.js validation rules with zero cookies, zero IP logging,
 * and strict field whitelisting. Bind optional KV namespace SN_EVENTS to store summaries.
 */

const ALLOWED_EVENTS = {
  page_view: ['e', 't', 'page'],
  outbound_click: ['e', 't', 'page', 'product'],
  guide_read: ['e', 't', 'page'],
  search: ['e', 't', 'page', 'q_len', 'results'],
  suggestion_rank: ['e', 't', 'page', 'rank']
};

const FORBIDDEN = new Set([
  'ip', 'user_agent', 'referrer', 'cookie', 'fingerprint', 'query_text', 'email', 'session_id'
]);

function validate(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
    return { ok: false, error: 'Payload must be a JSON object' };
  }
  for (const k of Object.keys(raw)) {
    if (FORBIDDEN.has(k)) return { ok: false, error: `Forbidden privacy field: ${k}` };
  }
  const e = raw.e;
  if (typeof e !== 'string' || !Object.prototype.hasOwnProperty.call(ALLOWED_EVENTS, e)) {
    return { ok: false, error: 'Unknown or missing event name' };
  }
  const allowed = new Set(ALLOWED_EVENTS[e]);
  for (const k of Object.keys(raw)) {
    if (!allowed.has(k)) return { ok: false, error: `Unexpected field: ${k}` };
  }
  if (typeof raw.page !== 'string' || !raw.page.startsWith('/') || raw.page.length > 200) {
    return { ok: false, error: 'Invalid page path' };
  }
  const clean = {
    e,
    t: Math.floor((typeof raw.t === 'number' && Number.isFinite(raw.t) ? raw.t : Date.now()) / 60000) * 60000,
    page: raw.page.split('?')[0].split('#')[0]
  };
  if (e === 'outbound_click') {
    if (typeof raw.product !== 'string' || !/^P-0[1-5]$/.test(raw.product)) {
      return { ok: false, error: 'Invalid product ID' };
    }
    clean.product = raw.product;
  } else if (e === 'search') {
    if (!Number.isInteger(raw.q_len) || raw.q_len < 1 || raw.q_len > 200 ||
        !Number.isInteger(raw.results) || raw.results < 0 || raw.results > 500) {
      return { ok: false, error: 'Invalid search counts' };
    }
    clean.q_len = raw.q_len;
    clean.results = raw.results;
  } else if (e === 'suggestion_rank') {
    if (!Array.isArray(raw.rank) || raw.rank.length > 30 ||
        !raw.rank.every((s) => typeof s === 'string' && /^SG-\d{2}$/.test(s))) {
      return { ok: false, error: 'Invalid rank array' };
    }
    clean.rank = raw.rank.slice();
  }
  return { ok: true, value: clean };
}

function jsonResponse(status, data) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    }
  });
}

export async function onRequestGet() {
  return jsonResponse(200, {
    ok: true,
    mode: 'cloudflare-pages-function',
    schema_version: '1.0',
    events: Object.keys(ALLOWED_EVENTS),
    cookies: false
  });
}

export async function onRequestPost(context) {
  let rawText;
  try {
    rawText = await context.request.text();
  } catch (_) {
    return jsonResponse(400, { ok: false, error: 'Unable to read request body' });
  }
  if (rawText.length > 4096) {
    return jsonResponse(413, { ok: false, error: 'Payload too large' });
  }
  let parsed;
  try {
    parsed = JSON.parse(rawText);
  } catch (_) {
    return jsonResponse(400, { ok: false, error: 'Malformed JSON body' });
  }
  const verdict = validate(parsed);
  if (!verdict.ok) {
    return jsonResponse(400, { ok: false, error: verdict.error });
  }
  if (context.env && context.env.SN_EVENTS && typeof context.env.SN_EVENTS.put === 'function') {
    const key = `${verdict.value.t}:${verdict.value.e}:${crypto.randomUUID()}`;
    await context.env.SN_EVENTS.put(key, JSON.stringify(verdict.value));
  }
  return jsonResponse(202, { ok: true, recorded: verdict.value.e });
}
