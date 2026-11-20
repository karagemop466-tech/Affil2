#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const SCHEMA_PATH = path.resolve(__dirname, '..', 'data', 'events.json');
let schema;
try {
  schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
} catch (_) {
  schema = {
    schema_version: '1.0',
    events: {
      page_view: { allowed_fields: ['e', 't', 'page'] },
      outbound_click: { allowed_fields: ['e', 't', 'page', 'product'] },
      guide_read: { allowed_fields: ['e', 't', 'page'] },
      search: { allowed_fields: ['e', 't', 'page', 'q_len', 'results'] },
      suggestion_rank: { allowed_fields: ['e', 't', 'page', 'rank'] }
    },
    forbidden_fields: ['ip', 'user_agent', 'referrer', 'cookie', 'fingerprint', 'query_text', 'email', 'session_id']
  };
}

const ALLOWED_EVENTS = schema.events;
const FORBIDDEN_FIELDS = new Set(schema.forbidden_fields || []);
const MAX_BODY_BYTES = 4096;

function validatePayload(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
    return { ok: false, error: 'Payload must be a JSON object' };
  }
  for (const key of Object.keys(raw)) {
    if (FORBIDDEN_FIELDS.has(key)) {
      return { ok: false, error: `Forbidden privacy field: ${key}` };
    }
  }
  const eventName = raw.e;
  if (typeof eventName !== 'string' || !Object.prototype.hasOwnProperty.call(ALLOWED_EVENTS, eventName)) {
    return { ok: false, error: 'Unknown or missing event name' };
  }
  const spec = ALLOWED_EVENTS[eventName];
  const allowedKeys = new Set(spec.allowed_fields || []);
  for (const key of Object.keys(raw)) {
    if (!allowedKeys.has(key)) {
      return { ok: false, error: `Unexpected field for ${eventName}: ${key}` };
    }
  }
  if (typeof raw.page !== 'string' || !raw.page.startsWith('/') || raw.page.length > 200) {
    return { ok: false, error: 'Invalid page path' };
  }
  const cleanPage = raw.page.split('?')[0].split('#')[0];
  const clean = {
    e: eventName,
    t: Math.floor((typeof raw.t === 'number' && Number.isFinite(raw.t) ? raw.t : Date.now()) / 60000) * 60000,
    page: cleanPage
  };

  if (eventName === 'outbound_click') {
    if (typeof raw.product !== 'string' || !/^P-0[1-5]$/.test(raw.product)) {
      return { ok: false, error: 'Invalid product ID for outbound_click' };
    }
    clean.product = raw.product;
  } else if (eventName === 'search') {
    if (!Number.isInteger(raw.q_len) || raw.q_len < 1 || raw.q_len > 200) {
      return { ok: false, error: 'Invalid q_len for search' };
    }
    if (!Number.isInteger(raw.results) || raw.results < 0 || raw.results > 500) {
      return { ok: false, error: 'Invalid results count for search' };
    }
    clean.q_len = raw.q_len;
    clean.results = raw.results;
  } else if (eventName === 'suggestion_rank') {
    if (!Array.isArray(raw.rank) || raw.rank.length > 30 ||
        !raw.rank.every((id) => typeof id === 'string' && /^SG-\d{2}$/.test(id))) {
      return { ok: false, error: 'Invalid rank array for suggestion_rank' };
    }
    clean.rank = raw.rank.slice();
  }

  return { ok: true, value: clean };
}

function createCollectorServer(options = {}) {
  const logFile = options.logFile || process.env.COLLECT_LOG_FILE || '/tmp/shopnow-events.ndjson';
  const allowOrigin = options.allowOrigin ?? process.env.COLLECT_ALLOW_ORIGIN ?? '';

  function sendJson(res, status, body) {
    const headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    };
    if (allowOrigin) {
      headers['Access-Control-Allow-Origin'] = allowOrigin;
      headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS';
      headers['Access-Control-Allow-Headers'] = 'Content-Type';
    }
    res.writeHead(status, headers);
    res.end(JSON.stringify(body));
  }

  return http.createServer((req, res) => {
    const reqPath = (req.url || '/').split('?')[0];

    if (req.method === 'OPTIONS' && reqPath === '/api/collect') {
      return sendJson(res, 204, {});
    }

    if (req.method === 'GET' && (reqPath === '/health' || reqPath === '/api/collect')) {
      return sendJson(res, 200, {
        ok: true,
        mode: 'self-hosted',
        schema_version: schema.schema_version || '1.0',
        events: Object.keys(ALLOWED_EVENTS),
        cookies: false
      });
    }

    if (req.method === 'POST' && reqPath === '/api/collect') {
      const contentLen = Number(req.headers['content-length'] || 0);
      if (Number.isFinite(contentLen) && contentLen > MAX_BODY_BYTES) {
        res.writeHead(413, {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'no-store',
          'Connection': 'close'
        });
        res.end(JSON.stringify({ ok: false, error: 'Payload too large' }));
        req.resume();
        return;
      }
      let size = 0;
      let tooLarge = false;
      const chunks = [];
      req.on('data', (chunk) => {
        if (tooLarge) return;
        size += chunk.length;
        if (size > MAX_BODY_BYTES) {
          tooLarge = true;
          chunks.length = 0;
          if (!res.writableEnded) {
            res.writeHead(413, {
              'Content-Type': 'application/json; charset=utf-8',
              'Cache-Control': 'no-store',
              'Connection': 'close'
            });
            res.end(JSON.stringify({ ok: false, error: 'Payload too large' }));
          }
          return;
        }
        chunks.push(chunk);
      });
      req.on('end', () => {
        if (tooLarge) return;
        let parsed;
        try {
          parsed = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        } catch (_) {
          return sendJson(res, 400, { ok: false, error: 'Malformed JSON body' });
        }
        const verdict = validatePayload(parsed);
        if (!verdict.ok) {
          return sendJson(res, 400, { ok: false, error: verdict.error });
        }
        try {
          fs.mkdirSync(path.dirname(logFile), { recursive: true });
          fs.appendFileSync(logFile, JSON.stringify(verdict.value) + '\n', 'utf8');
        } catch (err) {
          return sendJson(res, 500, { ok: false, error: 'Failed to persist event' });
        }
        return sendJson(res, 202, { ok: true, recorded: verdict.value.e });
      });
      return;
    }

    return sendJson(res, 404, { ok: false, error: 'Not found' });
  });
}

if (require.main === module) {
  const host = process.env.HOST || '0.0.0.0';
  const port = Number(process.env.PORT || 8787);
  const server = createCollectorServer();
  server.listen(port, host, () => {
    console.log(`ShopNow collector listening on http://${host}:${port}/api/collect`);
  });
}

module.exports = {
  ALLOWED_EVENTS,
  FORBIDDEN_FIELDS,
  MAX_BODY_BYTES,
  createCollectorServer,
  validatePayload
};
