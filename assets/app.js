// Privacy-preserving measurement, search, mobile navigation, pair compare, ranking, and CSV export.
// Five events: page_view, outbound_click, guide_read, search, suggestion_rank.
// No cookies, no third-party requests, no fingerprinting, and no raw search text logged.
(function () {
  'use strict';
  try {
    var ALLOWED = { page_view: 1, outbound_click: 1, guide_read: 1, search: 1, suggestion_rank: 1 };
    var FORBIDDEN = {
      ip: 1, user_agent: 1, referrer: 1, cookie: 1, fingerprint: 1,
      query_text: 1, email: 1, session_id: 1
    };

    function getEndpoint() {
      if (typeof window !== 'undefined' && typeof window.SN_COLLECT_ENDPOINT === 'string' && window.SN_COLLECT_ENDPOINT) {
        return window.SN_COLLECT_ENDPOINT;
      }
      var m = document.querySelector('meta[name="sn-collect-endpoint"]');
      if (m && m.content) return m.content.trim();
      var stored = localStorage.getItem('sn_collect_url');
      return stored ? stored.trim() : '';
    }

    // Self-hosted collector transport (no-op unless an endpoint is configured; FLG-010).
    function send(payload) {
      var endpoint = getEndpoint();
      if (!endpoint) return false;
      if (!payload || !ALLOWED[payload.e]) return false;
      var clean = {};
      Object.keys(payload).forEach(function (k) {
        if (!FORBIDDEN[k]) clean[k] = payload[k];
      });
      clean.t = Math.floor((clean.t || Date.now()) / 60000) * 60000;
      var body = JSON.stringify(clean);
      if (typeof fetch === 'function') {
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: body,
          keepalive: true,
          credentials: 'omit'
        }).catch(function () {});
        return true;
      }
      return false;
    }

    var ev = [];
    try { ev = JSON.parse(localStorage.getItem('sn_events') || '[]'); } catch (_) { ev = []; }
    if (!Array.isArray(ev)) ev = [];

    function log(e, d) {
      if (!ALLOWED[e]) return;
      var entry = Object.assign({ e: e, t: Date.now(), page: location.pathname || '/' }, d || {});
      ev.push(entry);
      ev = ev.slice(-500);
      try { localStorage.setItem('sn_events', JSON.stringify(ev)); } catch (_) {}
      send(entry);
    }

    function recordOutbound(pid) {
      if (!pid) return;
      log('outbound_click', { product: pid });
      var c = {};
      try { c = JSON.parse(localStorage.getItem('sn_clicks') || '{}'); } catch (_) { c = {}; }
      c[pid] = (c[pid] || 0) + 1;
      try { localStorage.setItem('sn_clicks', JSON.stringify(c)); } catch (_) {}
      var el = document.getElementById('localClicks');
      if (el) {
        el.textContent = Object.values(c).reduce(function (x, y) { return x + y; }, 0);
      }
    }

    log('page_view');
    if (/\/guides\//.test(location.pathname)) log('guide_read');

    // Mobile nav toggle
    var navBtn = document.querySelector('.navtoggle');
    var navMenu = document.getElementById('primary-nav');
    if (navBtn && navMenu) {
      navBtn.addEventListener('click', function () {
        var open = navMenu.classList.toggle('open');
        navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      document.addEventListener('keydown', function (evt) {
        if (evt.key === 'Escape' && navMenu.classList.contains('open')) {
          navMenu.classList.remove('open');
          navBtn.setAttribute('aria-expanded', 'false');
          navBtn.focus();
        }
      });
    }

    // Outbound affiliate link clicks (supports static and dynamically rendered links)
    document.querySelectorAll('[data-outbound]').forEach(function (a) {
      a.addEventListener('click', function () {
        recordOutbound(a.getAttribute('data-outbound'));
      });
    });

    function csvCell(val) {
      var s = String(val == null ? '' : val);
      if (/[",\r\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
      return s;
    }

    function download(name, content) {
      var blob = new Blob([content], { type: 'text/csv;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }

    var ex = document.getElementById('exportClicks');
    if (ex) {
      ex.addEventListener('click', function () {
        var c = {};
        try { c = JSON.parse(localStorage.getItem('sn_clicks') || '{}'); } catch (_) { c = {}; }
        var lines = ['product,clicks'].concat(
          Object.entries(c).map(function (x) { return csvCell(x[0]) + ',' + csvCell(x[1]); })
        );
        download('clicks.csv', lines.join('\n'));
      });
    }

    var exEv = document.getElementById('exportEvents');
    if (exEv) {
      exEv.addEventListener('click', function () {
        var rows = ['event,timestamp_iso,page,detail'];
        ev.forEach(function (item) {
          var detail = {};
          Object.keys(item).forEach(function (k) {
            if (k !== 'e' && k !== 't' && k !== 'page') detail[k] = item[k];
          });
          rows.push([
            csvCell(item.e),
            csvCell(new Date(item.t).toISOString()),
            csvCell(item.page),
            csvCell(Object.keys(detail).length ? JSON.stringify(detail) : '')
          ].join(','));
        });
        download('events.csv', rows.join('\n'));
      });
    }

    // On-site search (search.html)
    var searchIdxEl = document.getElementById('searchIndex');
    var resultsEl = document.getElementById('results');
    var searchInput = document.getElementById('sq');
    var searchMeta = document.getElementById('searchMeta');
    if (searchIdxEl && resultsEl && searchInput) {
      var indexData = [];
      try { indexData = JSON.parse(searchIdxEl.textContent || '[]'); } catch (_) { indexData = []; }

      function runSearch(query, recordEvent) {
        var trimmed = (query || '').trim();
        searchInput.value = trimmed;
        var headerInput = document.getElementById('q');
        if (headerInput && !headerInput.value) headerInput.value = trimmed;
        while (resultsEl.firstChild) resultsEl.removeChild(resultsEl.firstChild);

        if (!trimmed) {
          if (searchMeta) {
            searchMeta.textContent = 'Searching across ' + indexData.length +
              ' pages on this site. Nothing is sent to a server — the index is embedded below and matched in your browser.';
          }
          return;
        }

        var terms = trimmed.toLowerCase().split(/\s+/).filter(Boolean);
        var scored = [];
        indexData.forEach(function (entry) {
          var t = (entry.t || '').toLowerCase();
          var d = (entry.d || '').toLowerCase();
          var k = (entry.k || '').toLowerCase();
          var combined = t + ' ' + k + ' ' + d;
          var allMatch = terms.every(function (term) { return combined.indexOf(term) !== -1; });
          if (!allMatch) return;
          var score = 0;
          terms.forEach(function (term) {
            if (t.indexOf(term) !== -1) score += 3;
            if (k.indexOf(term) !== -1) score += 2;
            if (d.indexOf(term) !== -1) score += 1;
          });
          scored.push({ entry: entry, score: score });
        });
        scored.sort(function (a, b) { return b.score - a.score; });

        if (searchMeta) {
          searchMeta.textContent = scored.length + ' result' + (scored.length === 1 ? '' : 's') +
            ' across ' + indexData.length + ' pages (matched locally in your browser).';
        }

        if (!scored.length) {
          var empty = document.createElement('p');
          empty.className = 'muted';
          empty.textContent = 'No matching pages found. Try broader terms like "basket", "450", "wireless", "capacity", or "warranty".';
          resultsEl.appendChild(empty);
        } else {
          scored.forEach(function (hit) {
            var box = document.createElement('article');
            box.className = 'hit';

            var where = document.createElement('div');
            where.className = 'where';
            where.textContent = hit.entry.k || 'page';
            box.appendChild(where);

            var h3 = document.createElement('h3');
            var a = document.createElement('a');
            a.href = hit.entry.u;
            a.textContent = hit.entry.t;
            h3.appendChild(a);
            box.appendChild(h3);

            var p = document.createElement('p');
            var snippet = hit.entry.d || '';
            p.textContent = snippet.length > 220 ? snippet.slice(0, 217) + '...' : snippet;
            box.appendChild(p);

            resultsEl.appendChild(box);
          });
        }

        if (recordEvent) {
          log('search', { q_len: trimmed.length, results: scored.length });
        }
      }

      var params = new URLSearchParams(location.search || '');
      var initialQ = params.get('q') || '';
      runSearch(initialQ, Boolean(initialQ.trim()));

      var searchForm = searchInput.closest('form');
      if (searchForm) {
        searchForm.addEventListener('submit', function (evt) {
          evt.preventDefault();
          var qVal = searchInput.value || '';
          var nextUrl = location.pathname + (qVal.trim() ? ('?q=' + encodeURIComponent(qVal.trim())) : '');
          if (window.history && window.history.replaceState) {
            window.history.replaceState(null, '', nextUrl);
          }
          runSearch(qVal, Boolean(qVal.trim()));
        });
      }
    }

    // Two-at-a-time head-to-head compare view (compare.html)
    var pairEl = document.getElementById('pairData');
    if (pairEl) {
      var pairData = {};
      try { pairData = JSON.parse(pairEl.textContent || '{}'); } catch (_) { pairData = {}; }
      var pairA = document.getElementById('pairA');
      var pairB = document.getElementById('pairB');
      var pairOut = document.getElementById('pairView');
      if (pairA && pairB && pairOut) {
        var renderPair = function () {
          var idA = pairA.value;
          var idB = pairB.value;
          var A = pairData[idA];
          var B = pairData[idB];
          if (!A || !B) return;
          if (idA === idB) {
            pairOut.innerHTML = '<p class="small">Pick two different products.</p>';
            return;
          }
          var rows = A.rows.map(function (r, i) {
            var other = B.rows[i] ? B.rows[i][1] : '';
            return '<tr><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td><td>' + other + '</td></tr>';
          }).join('');
          pairOut.innerHTML = '<table class="compare pair"><caption>Same rows, same sources, two columns. ' +
            'Blank-looking cells say why they are blank.</caption><thead><tr><th scope="col">Field</th>' +
            '<th scope="col"><a href="' + A.url + '">' + A.name + '</a></th>' +
            '<th scope="col"><a href="' + B.url + '">' + B.name + '</a></th></tr></thead><tbody>' + rows + '</tbody></table>' +
            '<p class="cta"><a class="btn" rel="sponsored nofollow" href="' + A.buy + '" data-outbound="' + idA + '">' +
            'Check the first on Amazon<span class="btn-sub">paid link</span></a>' +
            '<a class="btn ghost" rel="sponsored nofollow" href="' + B.buy + '" data-outbound="' + idB + '">' +
            'Check the second<span class="btn-sub">paid link</span></a></p>';
          pairOut.querySelectorAll('[data-outbound]').forEach(function (btn) {
            btn.addEventListener('click', function () {
              recordOutbound(btn.getAttribute('data-outbound'));
            });
          });
        };
        pairA.addEventListener('change', renderPair);
        pairB.addEventListener('change', renderPair);
        renderPair();
      }
    }

    // Decision Center suggestions ranking
    var sugTable = document.getElementById('sugTable');
    var rank = [];
    try { rank = JSON.parse(localStorage.getItem('sn_rank') || '[]'); } catch (_) { rank = []; }
    if (!Array.isArray(rank)) rank = [];

    function renderRank() {
      document.querySelectorAll('#sugTable tbody tr').forEach(function (tr) {
        var s = tr.querySelector('.rank');
        var id = tr.getAttribute('data-sug');
        if (s) s.textContent = rank.indexOf(id) >= 0 ? ('#' + (rank.indexOf(id) + 1)) : '';
      });
    }

    if (sugTable) {
      var allIds = [].slice.call(document.querySelectorAll('#sugTable tbody tr')).map(function (tr) {
        return tr.getAttribute('data-sug');
      });
      if (!rank.length) {
        rank = allIds.slice();
      } else {
        allIds.forEach(function (id) { if (rank.indexOf(id) === -1) rank.push(id); });
      }
      document.querySelectorAll('[data-up],[data-down]').forEach(function (b) {
        b.addEventListener('click', function () {
          var id = b.getAttribute('data-up') || b.getAttribute('data-down');
          var i = rank.indexOf(id);
          var j = b.hasAttribute('data-up') ? i - 1 : i + 1;
          if (i < 0 || j < 0 || j >= rank.length) return;
          var t = rank[i];
          rank[i] = rank[j];
          rank[j] = t;
          try { localStorage.setItem('sn_rank', JSON.stringify(rank)); } catch (_) {}
          log('suggestion_rank', { rank: rank.slice() });
          renderRank();
        });
      });
      renderRank();

      var er = document.getElementById('exportRank');
      if (er) {
        er.addEventListener('click', function () {
          download('ranking.csv', 'rank,suggestion\n' + rank.map(function (s, i) {
            return (i + 1) + ',' + csvCell(s);
          }).join('\n'));
        });
      }

      var rr = document.getElementById('resetRank');
      if (rr) {
        rr.addEventListener('click', function () {
          try { localStorage.removeItem('sn_rank'); } catch (_) {}
          location.reload();
        });
      }

      var f = document.getElementById('decisionForm');
      if (f) {
        try {
          var savedDecision = JSON.parse(localStorage.getItem('sn_decision') || 'null');
          if (savedDecision && f.chosen) {
            f.chosen.value = savedDecision.chosen || '';
            f.why.value = savedDecision.why || '';
            f.measure.value = savedDecision.measure || '';
          }
        } catch (_) {}
        f.addEventListener('submit', function (e) {
          e.preventDefault();
          try {
            localStorage.setItem('sn_decision', JSON.stringify({
              chosen: f.chosen.value,
              why: f.why.value,
              measure: f.measure.value,
              t: Date.now()
            }));
          } catch (_) {}
          var out = document.getElementById('decisionSaved');
          if (out) out.textContent = 'Saved locally at ' + new Date().toISOString() + '. Export it with your ranking.';
        });
      }
    }
  } catch (e) {}
})();
