/* ShopNow Kitchen — measurement layer.
 * Five defined events (canonical): page_view, outbound_click, guide_read, search, suggestion_rank.
 * Privacy-preserving by design: no cookies, no fingerprinting, no referrer capture,
 * no search strings, no IP handling on the client. Events either:
 *   (a) POST in batches to window.SITE_CONFIG.analyticsEndpoint (self-hosted, analytics/server.py), or
 *   (b) stay in this browser's localStorage until the reader exports or clears them.
 * Local click tallies feed the reader-facing counters and the CSV export.
 */
(function () {
  'use strict';
  try {
    var CFG = window.SITE_CONFIG || {};
    var EP = CFG.analyticsEndpoint || null;
    var KEY = 'sn_events', CKEY = 'sn_clicks', QUEUE = 'sn_queue';
    var path = location.pathname.replace(/^.*\/Affil2/, '') || '/';

    function readJSON(k, d) { try { return JSON.parse(localStorage.getItem(k) || 'null') || d; } catch (e) { return d; } }
    function writeJSON(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

    function log(name, props) {
      var ev = Object.assign({ e: name, p: path, t: Date.now() }, props || {});
      var evs = readJSON(KEY, []); evs.push(ev); writeJSON(KEY, evs.slice(-500));
      if (EP) {
        var q = readJSON(QUEUE, []); q.push(ev); writeJSON(QUEUE, q.slice(-200));
        flush();
      }
    }
    var flushing = false;
    function flush() {
      if (!EP || flushing) return;
      var q = readJSON(QUEUE, []); if (!q.length) return;
      flushing = true;
      writeJSON(QUEUE, []);
      var body = JSON.stringify({ events: q });
      var done = function () { flushing = false; };
      try {
        if (navigator.sendBeacon && navigator.sendBeacon(EP, new Blob([body], { type: 'application/json' }))) { done(); return; }
      } catch (e) {}
      fetch(EP, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, keepalive: true })
        .then(done).catch(function () { writeJSON(QUEUE, q.concat(readJSON(QUEUE, [])).slice(-200)); done(); });
    }

    /* 1. page_view — every page */
    log('page_view');

    /* 2. outbound_click — every marked product link (data-outbound) */
    document.querySelectorAll('[data-outbound]').forEach(function (a) {
      a.addEventListener('click', function () {
        var id = a.getAttribute('data-outbound');
        log('outbound_click', { product: id, slot: a.closest('section, article, main') ? 'body' : 'body' });
        var c = readJSON(CKEY, {}); c[id] = (c[id] || 0) + 1; writeJSON(CKEY, c);
        paintClicks();
      });
    });

    /* 3. guide_read — a guide was actually read (scrolled to 55% or 25s dwell) */
    if (/\/guides\//.test(path)) {
      var fired = false;
      var fire = function () { if (!fired) { fired = true; log('guide_read', { guide: path.split('/').pop() }); } };
      window.addEventListener('scroll', function () {
        var d = document.documentElement;
        if (d.scrollTop + d.clientHeight >= d.scrollHeight * 0.55) fire();
      }, { passive: true });
      setTimeout(fire, 25000);
    }

    /* 4. search — the reader searched; result count only, never the query string */
    if (/search\.html$/.test(path)) {
      var params = new URLSearchParams(location.search);
      var had = (params.get('q') || '').trim().length > 0;
      if (had) {
        setTimeout(function () {
          var n = document.querySelectorAll('[data-search-result]').length;
          log('search', { results: n });
        }, 300);
      }
    }

    /* 5. suggestion_rank — the reader ranked the direction register */
    function paintClicks() {
      var c = readJSON(CKEY, {}), el = document.getElementById('localClicks');
      if (el) el.textContent = Object.values(c).reduce(function (x, y) { return x + y; }, 0);
    }
    paintClicks();

    var exp = document.getElementById('exportClicks');
    if (exp) exp.addEventListener('click', function () {
      var c = readJSON(CKEY, {});
      download('clicks.csv', 'product,clicks\n' + Object.entries(c).map(function (x) { return x[0] + ',' + x[1]; }).join('\n'));
    });

    /* Suggestions ranking + decision worksheet (local-only, reader-owned) */
    var rank = readJSON('sn_rank', []);
    function renderRank() {
      document.querySelectorAll('#sugTable tbody tr').forEach(function (tr) {
        var s = tr.querySelector('.rank');
        if (s) s.textContent = rank.indexOf(tr.getAttribute('data-sug')) >= 0 ? ('#' + (rank.indexOf(tr.getAttribute('data-sug')) + 1)) : '';
      });
    }
    if (document.getElementById('sugTable')) {
      if (!rank.length) {
        rank = [].slice.call(document.querySelectorAll('#sugTable tbody tr')).map(function (tr) { return tr.getAttribute('data-sug'); });
      }
      document.querySelectorAll('[data-up],[data-down]').forEach(function (b) {
        b.addEventListener('click', function () {
          var id = b.getAttribute('data-up') || b.getAttribute('data-down');
          var i = rank.indexOf(id), j = b.hasAttribute('data-up') ? i - 1 : i + 1;
          if (j < 0 || j >= rank.length) return;
          var t = rank[i]; rank[i] = rank[j]; rank[j] = t;
          writeJSON('sn_rank', rank);
          log('suggestion_rank', { top: rank[0] });
          renderRank();
        });
      });
      renderRank();
      var er = document.getElementById('exportRank');
      if (er) er.addEventListener('click', function () {
        download('ranking.csv', 'rank,suggestion\n' + rank.map(function (s, i) { return (i + 1) + ',' + s; }).join('\n'));
      });
      var rr = document.getElementById('resetRank');
      if (rr) rr.addEventListener('click', function () { localStorage.removeItem('sn_rank'); location.reload(); });
      var f = document.getElementById('decisionForm');
      if (f) f.addEventListener('submit', function (e) {
        e.preventDefault();
        writeJSON('sn_decision', { chosen: f.chosen.value, why: f.why.value, measure: f.measure.value, t: Date.now() });
        document.getElementById('decisionSaved').textContent = 'Saved locally at ' + new Date().toISOString() + '. Export it with your ranking.';
      });
    }

    /* Reader capture (SG-30): honest gating — no endpoint, no fake signup */
    var cap = document.getElementById('captureForm');
    if (cap) {
      if (!CFG.readerCaptureEndpoint) {
        cap.addEventListener('submit', function (e) {
          e.preventDefault();
          document.getElementById('captureNote').textContent =
            'Mailing list is not connected yet (Q-09). Subscribe via RSS for now — this form will go live when a provider is chosen on the Suggestions page.';
        });
      } else {
        cap.action = CFG.readerCaptureEndpoint;
      }
    }

    function download(n, c) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([c], { type: 'text/csv' }));
      a.download = n; a.click();
    }
  } catch (e) {}
})();
