/*
 * ShopNow Kitchen - self-hosted, privacy-preserving event collector.
 *
 * This is a Cloudflare Pages Function. It is also written as a plain
 * `export async function onRequestPost` module with no imports, so it can be
 * lifted into any edge runtime that speaks the Pages Functions signature.
 *
 * What it does NOT do, by design:
 *   - it never writes a cookie and never reads one
 *   - it never stores an IP address, user agent, referrer URL or device fingerprint
 *   - it never accepts a payload key that could carry personal data
 *   - it never forwards anything to Amazon or to a third party
 *   - it never records a search query, only the shape of the search
 *
 * Storage:
 *   - a Workers KV binding named EVENT_LOG, if present, receives one JSON
 *     object per event. That is the production path on Cloudflare Pages.
 *   - without the binding the function still answers 204 and the events are
 *     dropped, so the site degrades quietly instead of breaking.
 *
 * Endpoint contract (see data/events.json):
 *   POST /api/collect        -> 204 No Content on an accepted event
 *   GET  /api/collect        -> 200 { "status": "ok" } so the browser client
 *                                can decide whether to switch itself on
 */

const ALLOWED_EVENTS = [
  "page_view",
  "outbound_click",
  "guide_read",
  "search",
  "suggestion_rank",
];

// Keys the client is allowed to send. Anything else is dropped rather than
// stored, so a hostile or buggy client cannot smuggle data in.
const ALLOWED_FIELDS = {
  event: "string",
  path: "string",
  session_id: "string",
  ts: "string",
  referrer_host: "string",
  product_id: "string",
  link_position: "string",
  guide_id: "string",
  query_length: "string",
  result_count: "string",
  suggestion_id: "string",
  position: "string",
};

const MAX_STRING = 300;
const MAX_BODY_BYTES = 4096;

/**
 * Reduce an incoming event to the allowed fields only.
 * Returns null when the event is not usable.
 */
export function sanitize(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;

  const name = typeof raw.event === "string" ? raw.event : "";
  if (ALLOWED_EVENTS.indexOf(name) === -1) return null;

  const clean = { event: name };

  for (const key of Object.keys(ALLOWED_FIELDS)) {
    if (key === "event") continue;
    const value = raw[key];
    if (typeof value !== "string") continue;
    clean[key] = value.slice(0, MAX_STRING);
  }

  // A path is a site path, never a full URL: strip anything that looks like
  // a scheme or a query string so a referrer cannot ride along.
  if (clean.path) {
    clean.path = clean.path
      .replace(/^[a-z]+:\/\/[^/]*/i, "")
      .split("?")[0]
      .split("#")[0]
      .slice(0, MAX_STRING);
  }

  // session_id is a random per-tab value; keep it to a safe alphabet only.
  if (clean.session_id) {
    clean.session_id = clean.session_id.replace(/[^a-z0-9]/gi, "").slice(0, 32);
  }

  // referrer_host is a bare hostname. Drop anything that is not one.
  if (clean.referrer_host) {
    const host = clean.referrer_host
      .replace(/^[a-z]+:\/\//i, "")
      .split("/")[0]
      .split("?")[0]
      .split("#")[0]
      .replace(/^[^a-z0-9.-]+/i, "");
    clean.referrer_host = /^[a-z0-9.-]+\.[a-z]{2,}$/i.test(host) ? host.slice(0, 120) : "";
  }

  // Identifiers are internal codes; keep them to a conservative shape.
  for (const key of ["product_id", "link_position", "guide_id", "suggestion_id"]) {
    if (clean[key]) clean[key] = clean[key].replace(/[^A-Za-z0-9._-]/g, "").slice(0, 64);
  }

  // Counts are numbers written as strings; keep only digits.
  for (const key of ["query_length", "result_count", "position"]) {
    if (clean[key]) clean[key] = clean[key].replace(/[^0-9]/g, "").slice(0, 6);
  }

  clean.received_at = new Date().toISOString();
  return clean;
}

/**
 * Store one event. Returns true when it was written somewhere.
 */
async function store(env, event) {
  const kv = env && env.EVENT_LOG;
  if (!kv || typeof kv.put !== "function") return false;
  const key = "evt_" + Date.now() + "_" + Math.random().toString(36).slice(2, 10);
  await kv.put(key, JSON.stringify(event));
  return true;
}

export async function onRequestPost(context) {
  const { request, env } = context;

  let raw;
  try {
    const text = await request.text();
    if (text.length > MAX_BODY_BYTES) {
      return new Response(null, { status: 413 });
    }
    raw = JSON.parse(text);
  } catch (err) {
    return new Response(null, { status: 400 });
  }

  const event = sanitize(raw);
  if (!event) {
    return new Response(null, { status: 400 });
  }

  try {
    await store(env, event);
  } catch (err) {
    // A storage failure must not turn into a reader-facing error.
    return new Response(null, { status: 204 });
  }

  return new Response(null, { status: 204 });
}

export async function onRequestGet() {
  // A GET on the collector path is the health probe the browser client uses to
  // decide whether to switch measurement on. It answers with a fixed body and
  // stores nothing, so a probe is never recorded as an event.
  return new Response(JSON.stringify({ status: "ok", service: "shopnow-kitchen-collect" }), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
    },
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type",
      "access-control-max-age": "86400",
    },
  });
}

export default async function handler(context) {
  const method = (context.request.method || "GET").toUpperCase();
  if (method === "POST") return onRequestPost(context);
  if (method === "GET") return onRequestGet(context);
  return onRequestOptions(context);
}

export { ALLOWED_EVENTS, ALLOWED_FIELDS };
