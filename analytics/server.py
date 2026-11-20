#!/usr/bin/env python3
"""ShopNow Kitchen — self-hosted, privacy-preserving analytics endpoint.

Design constraints (see analytics/README.md and disclosure.html):
  * No cookies, no fingerprinting, no user identifiers.
  * The client IP address is NEVER read, logged, or stored (the request handler
    discards it; no access log is written).
  * No referrer capture, no query strings, no free text — event payloads are
    name + page path + coarse props only (the five defined events).
  * Stores raw events as JSONL per month, plus rolling aggregates.
  * CORS is restricted to one site origin (ALLOWED_ORIGIN env var).

Run:   python3 analytics/server.py --port 8787
Stop:  Ctrl-C
Test:  curl -s -X POST http://127.0.0.1:8787/v1/events \
         -H 'Content-Type: application/json' \
         -d '{"events":[{"e":"page_view","p":"/","t":0}]}'
       curl -s http://127.0.0.1:8787/v1/stats
"""
import argparse
import json
import os
import re
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ALLOWED_ORIGIN = os.environ.get(
    "ALLOWED_ORIGIN", "https://karagemop466-tech.github.io"
)
DATA_DIR = os.environ.get("ANALYTICS_DATA", os.path.join(os.path.dirname(__file__), "data"))
VALID_EVENTS = {"page_view", "outbound_click", "guide_read", "search", "suggestion_rank"}
MAX_BATCH = 100
PATH_RE = re.compile(r"^/[A-Za-z0-9._\-/]*$")
_lock = threading.Lock()

def _month_file():
    return os.path.join(DATA_DIR, "events-%s.jsonl" % datetime.now(timezone.utc).strftime("%Y-%m"))

def store(batch):
    """Append events to JSONL. Never records source IP or headers."""
    rows = []
    for ev in batch[:MAX_BATCH]:
        if not isinstance(ev, dict):
            continue
        name = ev.get("e")
        if name not in VALID_EVENTS:
            continue
        path = ev.get("p", "/")
        if not isinstance(path, str) or not PATH_RE.match(path[:200]):
            path = "/"
        row = {"e": name, "p": path[:200], "t": int(ev.get("t") or time.time() * 1000)}
        for k in ("product", "guide", "results", "top", "slot"):
            if k in ev and isinstance(ev[k], (str, int)):
                row[k] = str(ev[k])[:64]
        rows.append(row)
    if rows:
        os.makedirs(DATA_DIR, exist_ok=True)
        with _lock:
            with open(_month_file(), "a", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)

def stats():
    """Aggregate counts only — no timelines, no identifiers."""
    counts = Counter()
    pages = Counter()
    products = Counter()
    days = set()
    if os.path.isdir(DATA_DIR):
        with _lock:
            for name in sorted(os.listdir(DATA_DIR)):
                if not name.endswith(".jsonl"):
                    continue
                with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
                    for line in f:
                        try:
                            r = json.loads(line)
                        except ValueError:
                            continue
                        counts[r.get("e", "?")] += 1
                        pages[r.get("p", "?")] += 1
                        if r.get("product"):
                            products[r["product"]] += 1
                        days.add(datetime.fromtimestamp(r.get("t", 0) / 1000, timezone.utc).strftime("%Y-%m-%d"))
    return {
        "events": dict(counts),
        "pages": dict(pages.most_common(50)),
        "outbound_clicks_by_product": dict(products),
        "days_with_data": sorted(days),
        "privacy": "aggregate only; no cookies, no IPs, no identifiers",
    }

class Handler(BaseHTTPRequestHandler):
    server_version = "SNKAnalytics/1.0"

    def log_message(self, *args):
        """No access logging — deliberately silent (privacy)."""
        return

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path.rstrip("/") != "/v1/events":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            if n > 32_000:
                self.send_error(413)
                return
            body = json.loads(self.rfile.read(n) or b"{}")
            stored = store(body.get("events", []) if isinstance(body, dict) else [])
        except (ValueError, TypeError):
            self.send_error(400)
            return
        self.send_response(204)
        self._cors()
        self.send_header("X-Stored-Events", str(stored))
        self.end_headers()

    def do_GET(self):
        if self.path.rstrip("/") != "/v1/stats":
            self.send_error(404)
            return
        payload = json.dumps(stats()).encode("utf-8")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--host", default="0.0.0.0")
    args = ap.parse_args()
    print("ShopNow Kitchen analytics endpoint on %s:%d (origin: %s)" % (args.host, args.port, ALLOWED_ORIGIN))
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
