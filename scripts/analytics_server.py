#!/usr/bin/env python3
"""
Optional, self-hosted, privacy-preserving event collector for ShopNow Kitchen.

This collector is NOT deployed and NOT referenced by any page. It exists so the five
site events can be counted server-side later, without changing the event names and
without collecting anything you would not want printed in a public audit.

What it stores: per-day aggregate counts only, e.g. {"2026-11-20": {"page_view": 12}}.
What it never stores or logs: IP addresses, cookies, user agents, fingerprints,
account identifiers, raw search terms, individual click histories, referrer URLs.
Request headers are read solely to decide nothing; they are never written anywhere.

Security notes (read before deploying):
  * Deploy behind HTTPS at a same-origin route (e.g. nginx/caddy reverse proxy). This
    file speaks plain HTTP and must not be exposed directly to the internet.
  * /stats requires the ANALYTICS_TOKEN bearer token. Without the env var set, /stats
    is disabled entirely. /healthz is unauthenticated and returns only "ok".
  * Run it as an unprivileged user with a writable ANALYTICS_STATE file path outside
    any public web root. Set ANALYTICS_RETENTION_DAYS (default 90) to cap history.

Environment:
  ANALYTICS_STATE          path of the JSON aggregate store (default: analytics-state.json next to this file)
  ANALYTICS_TOKEN          bearer token for /stats (if unset, /stats returns 404)
  ANALYTICS_RETENTION_DAYS integer, entries older than this many days are dropped on write (default 90)
  ANALYTICS_PORT           listen port (default 8791); binds 127.0.0.1, put a TLS proxy in front
"""
import datetime
import json
import os
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ALLOWED_EVENTS = ("page_view", "guide_read", "outbound_click", "search", "suggestion_rank")
STATE = pathlib.Path(os.environ.get("ANALYTICS_STATE", str(pathlib.Path(__file__).with_name("analytics-state.json"))))
TOKEN = os.environ.get("ANALYTICS_TOKEN")
try:
    RETENTION_DAYS = int(os.environ.get("ANALYTICS_RETENTION_DAYS", "90"))
except ValueError:
    RETENTION_DAYS = 90
PORT = int(os.environ.get("ANALYTICS_PORT", "8791"))


def load_state():
    try:
        return json.loads(STATE.read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Never silently overwrite a corrupt store.
        sys.exit(f"refusing to start: {STATE} is not valid JSON; fix or move it first")


def prune(state):
    cutoff = (datetime.date.today() - datetime.timedelta(days=RETENTION_DAYS)).isoformat()
    return {day: counts for day, counts in state.items() if day >= cutoff}


def bump(event):
    state = prune(load_state())
    today = datetime.date.today().isoformat()
    day = state.setdefault(today, {})
    day[event] = int(day.get(event, 0)) + 1
    tmp = STATE.with_suffix(STATE.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, STATE)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body=b"", content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Deliberately silent: never write request lines (they contain the client IP).
        return

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, b"ok\n", "text/plain; charset=utf-8")
        elif self.path == "/stats":
            if not TOKEN:
                self._send(404, b"{}")
                return
            auth = self.headers.get("Authorization", "")
            if auth != f"Bearer {TOKEN}":
                self._send(401, b'{"error":"unauthorized"}')
                return
            body = json.dumps(load_state(), sort_keys=True).encode()
            self._send(200, body)
        else:
            self._send(404, b"{}")

    def do_POST(self):
        if self.path != "/event":
            self._send(404, b"{}")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(411, b"{}")
            return
        if length <= 0 or length > 512:
            self._send(413, b"{}")
            return
        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send(400, b'{"error":"bad json"}')
            return
        if not isinstance(payload, dict):
            self._send(400, b'{"error":"bad shape"}')
            return
        event = payload.get("e")
        if event not in ALLOWED_EVENTS:
            self._send(422, b'{"error":"unknown event"}')
            return
        # Any extra keys (identifiers, paths, terms) are ignored by construction.
        bump(event)
        self._send(204)


if __name__ == "__main__":
    if "--check" in sys.argv:
        print("analytics_server.py OK; allow-list:", ", ".join(ALLOWED_EVENTS))
        sys.exit(0)
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"listening on 127.0.0.1:{PORT}; state at {STATE}; retention {RETENTION_DAYS}d")
    httpd.serve_forever()
