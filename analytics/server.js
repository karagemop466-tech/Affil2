/*
 * ShopNow Kitchen - standalone event collector.
 *
 * The same contract as functions/api/collect.js, but as a dependency-free
 * Node HTTP server for anyone who would rather run their own box than a
 * Cloudflare Pages project. No npm install, no build step.
 *
 *   node analytics/server.js
 *   PORT=8787 LOG=./analytics/events.ndjson node analytics/server.js
 *
 * Storage is newline-delimited JSON appended to a local file. Rotate it with
 * whatever you already use; the server only ever appends one line per event.
 *
 * To point the static site at a collector on another host, add this to the
 * <head> of every page:
 *
 *   <meta name="x-collect-endpoint" content="https://collector.example/collect">
 *
 * Privacy, enforced by the shared sanitize() rules:
 *   - no cookies, no IP address, no user agent, no device fingerprint
 *   - no query strings, hash fragments or referrer URLs are kept
 *   - a search is recorded as a length and a result count, never as text
 *   - a session id is random per page load and is not linked to anything else
 */

const http = require("http");
const fs = require("fs");
const path = require("path");

const ALLOWED_EVENTS = [
  "page_view",
  "outbound_click",
  "guide_read",
  "search",
  "suggestion_rank",
];

const ALLOWED_FIELDS = [
  "event",
  "path",
  "session_id",
  "ts",
  "referrer_host",
  "product_id",
  "link_position",
  "guide_id",
  "query_length",
  "result_count",
  "suggestion_id",
  "position",
];

const MAX_STRING = 300;
const MAX_BODY_BYTES = 4096;

function sanitize(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;

  const name = typeof raw.event === "string" ? raw.event : "";
  if (ALLOWED_EVENTS.indexOf(name) === -1) return null;

  const clean = { event: name };
  for (const key of ALLOWED_FIELDS) {
    if (key === "event") continue;
    const value = raw[key];
    if (typeof value !== "string") continue;
    clean[key] = value.slice(0, MAX_STRING);
  }

  if (clean.path) {
    clean.path = clean.path
      .replace(/^[a-z]+:\/\/[^/]*/i, "")
      .split("?")[0]
      .split("#")[0]
      .slice(0, MAX_STRING);
  }
  if (clean.session_id) {
    clean.session_id = clean.session_id.replace(/[^a-z0-9]/gi, "").slice(0, 32);
  }
  if (clean.referrer_host) {
    const host = clean.referrer_host
      .replace(/^[a-z]+:\/\//i, "")
      .split("/")[0]
      .split("?")[0]
      .split("#")[0]
      .replace(/^[^a-z0-9.-]+/i, "");
    clean.referrer_host = /^[a-z0-9.-]+\.[a-z]{2,}$/i.test(host) ? host.slice(0, 120) : "";
  }
  for (const key of ["product_id", "link_position", "guide_id", "suggestion_id"]) {
    if (clean[key]) clean[key] = clean[key].replace(/[^A-Za-z0-9._-]/g, "").slice(0, 64);
  }
  for (const key of ["query_length", "result_count", "position"]) {
    if (clean[key]) clean[key] = clean[key].replace(/[^0-9]/g, "").slice(0, 6);
  }

  clean.received_at = new Date().toISOString();
  return clean;
}

const PORT = Number(process.env.PORT || 8787);
const LOG = path.resolve(process.env.LOG || path.join(__dirname, "events.ndjson"));
const HOST = process.env.HOST || "0.0.0.0";

fs.mkdirSync(path.dirname(LOG), { recursive: true });

function appendEvent(event) {
  fs.appendFile(LOG, JSON.stringify(event) + "\n", function (err) {
    if (err) {
      // Storage failures are logged, never surfaced to the reader.
      console.error("[collect] write failed:", err.message);
    }
  });
}

function send(res, status, body, headers) {
  res.writeHead(status, Object.assign({ "cache-control": "no-store" }, headers || {}));
  res.end(body === undefined ? "" : body);
}

const server = http.createServer(function (req, res) {
  const cors = {
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type",
  };

  if (req.method === "OPTIONS") {
    send(res, 204, "", cors);
    return;
  }

  if (req.method === "GET") {
    send(res, 200, JSON.stringify({ status: "ok", service: "shopnow-kitchen-collect" }), {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
    });
    return;
  }

  if (req.method !== "POST") {
    send(res, 405, "", cors);
    return;
  }

  let size = 0;
  let body = "";
  let aborted = false;

  req.on("data", function (chunk) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) {
      aborted = true;
      send(res, 413, "", cors);
      req.destroy();
      return;
    }
    body += chunk;
  });

  req.on("end", function () {
    if (aborted) return;
    let raw;
    try {
      raw = JSON.parse(body);
    } catch (err) {
      send(res, 400, "", cors);
      return;
    }
    const event = sanitize(raw);
    if (!event) {
      send(res, 400, "", cors);
      return;
    }
    appendEvent(event);
    send(res, 204, "", cors);
  });

  req.on("error", function () {
    /* a dropped reader must never produce a stack trace in the log */
  });
});

if (require.main === module) {
  server.listen(PORT, HOST, function () {
    console.log("[collect] listening on http://" + HOST + ":" + PORT);
    console.log("[collect] writing events to " + LOG);
  });
}

module.exports = { sanitize, ALLOWED_EVENTS, ALLOWED_FIELDS, server };
