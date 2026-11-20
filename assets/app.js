/*
 * First-party, browser-local measurement for the static GitHub Pages site.
 * The five defined events are aggregate counters only; no query text, URL,
 * timestamp, referrer, IP, or event-by-event trail is saved here.
 * A remote endpoint is intentionally not configured: GitHub Pages cannot
 * receive event writes. Amazon orders remain report-only in the campaign ledger.
 */
(function () {
  'use strict';

  var METRICS_KEY = 'sn_metrics_v1';
  var CLICKS_KEY = 'sn_clicks';
  var EVENTS = ['page_view', 'outbound_click', 'guide_read', 'search', 'suggestion_rank'];
  var PRODUCT_ID = /^P-\d{2}$/;

  function blankMetrics() {
    var counts = {};
    EVENTS.forEach(function (name) { counts[name] = 0; });
    return { version: 1, counts: counts };
  }

  function readJSON(key, fallback) {
    try {
      var value = JSON.parse(localStorage.getItem(key) || 'null');
      return value && typeof value === 'object' ? value : fallback;
    } catch (_) {
      return fallback;
    }
  }

  function cleanClicks(value) {
    var clean = {};
    Object.keys(value || {}).forEach(function (key) {
      var number = Number(value[key]);
      if (PRODUCT_ID.test(key) && Number.isFinite(number) && number > 0) {
        clean[key] = Math.floor(number);
      }
    });
    return clean;
  }

  function sumClicks(value) {
    return Object.keys(value).reduce(function (total, key) {
      return total + value[key];
    }, 0);
  }

  var storedMetrics = readJSON(METRICS_KEY, null);
  var isFirstRun = !storedMetrics || storedMetrics.version !== 1 || !storedMetrics.counts;
  var metrics = blankMetrics();
  if (!isFirstRun) {
    EVENTS.forEach(function (name) {
      var count = Number(storedMetrics.counts[name]);
      metrics.counts[name] = Number.isFinite(count) && count > 0 ? Math.floor(count) : 0;
    });
  }

  var clicks = cleanClicks(readJSON(CLICKS_KEY, {}));

  // Migrate only aggregate counts from the older event log, then erase its
  // per-event timestamps, paths and search text. Product clicks are counted
  // from the existing aggregate key to avoid duplicating old click events.
  try {
    var legacyEvents = JSON.parse(localStorage.getItem('sn_events') || '[]');
    if (isFirstRun && Array.isArray(legacyEvents)) {
      legacyEvents.forEach(function (event) {
        if (event && EVENTS.indexOf(event.e) !== -1 && event.e !== 'outbound_click') {
          metrics.counts[event.e] += 1;
        }
      });
    }
    localStorage.removeItem('sn_events');
  } catch (_) { /* local storage may be unavailable */ }
  if (isFirstRun) metrics.counts.outbound_click = sumClicks(clicks);

  function saveMetrics() {
    try { localStorage.setItem(METRICS_KEY, JSON.stringify(metrics)); } catch (_) { /* optional */ }
  }

  function saveClicks() {
    try { localStorage.setItem(CLICKS_KEY, JSON.stringify(clicks)); } catch (_) { /* optional */ }
  }

  function record(name) {
    if (EVENTS.indexOf(name) === -1) return;
    metrics.counts[name] += 1;
    saveMetrics();
  }

  function updateLocalClickCount() {
    var counter = document.getElementById('localClicks');
    if (counter) counter.textContent = String(sumClicks(clicks));
  }

  record('page_view');
  if (/\/guides\/[^/]+\.html$/.test(window.location.pathname)) record('guide_read');
  if (/\/search\.html$/.test(window.location.pathname)) {
    var directSearch = document.documentElement.hasAttribute('data-search-request');
    var searchQuery = new URLSearchParams(window.location.search).get('q');
    if (directSearch || (searchQuery && searchQuery.trim())) record('search');
  }
  window.ShopNowMetrics = {
    recordSearch: function () { record('search'); }
  };

  // Keep header searches on the static page itself. The one-time query is
  // passed in a URL fragment (not sent to the host) and removed on arrival.
  document.querySelectorAll('header form[role="search"]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      var input = form.querySelector('input[name="q"]');
      var query = input ? input.value.trim().slice(0, 120) : '';
      if (!query) return;
      event.preventDefault();
      var destination = new URL(form.getAttribute('action') || 'search.html', window.location.href);
      destination.search = '';
      destination.hash = 'q=' + encodeURIComponent(query);
      window.location.assign(destination.href);
    });
  });

  saveMetrics();
  updateLocalClickCount();

  document.addEventListener('click', function (event) {
    var target = event.target;
    var anchor = target && target.closest ? target.closest('[data-outbound]') : null;
    if (!anchor) return;
    var product = anchor.getAttribute('data-outbound') || '';
    if (!PRODUCT_ID.test(product)) return;

    record('outbound_click');
    clicks[product] = (clicks[product] || 0) + 1;
    saveClicks();
    updateLocalClickCount();
  });

  var exportButton = document.getElementById('exportClicks');
  if (exportButton) {
    exportButton.addEventListener('click', function () {
      var rows = ['product,clicks'];
      Object.keys(clicks).sort().forEach(function (product) {
        rows.push(product + ',' + clicks[product]);
      });
      download('clicks.csv', rows.join('\n'));
    });
  }

  var rank = readJSON('sn_rank', []);
  if (!Array.isArray(rank)) rank = [];

  function renderRank() {
    document.querySelectorAll('#sugTable tbody tr').forEach(function (row) {
      var label = row.querySelector('.rank');
      if (!label) return;
      var position = rank.indexOf(row.getAttribute('data-sug'));
      label.textContent = position >= 0 ? '#' + (position + 1) : '';
    });
  }

  var suggestionTable = document.getElementById('sugTable');
  if (suggestionTable) {
    var suggestionRows = Array.prototype.slice.call(
      suggestionTable.querySelectorAll('tbody tr[data-sug]')
    );
    if (!rank.length) {
      rank = suggestionRows.map(function (row) { return row.getAttribute('data-sug'); });
    }

    document.querySelectorAll('[data-up],[data-down]').forEach(function (button) {
      button.addEventListener('click', function () {
        var id = button.getAttribute('data-up') || button.getAttribute('data-down');
        var from = rank.indexOf(id);
        var to = button.hasAttribute('data-up') ? from - 1 : from + 1;
        if (from < 0 || to < 0 || to >= rank.length) return;
        var moved = rank[from];
        rank[from] = rank[to];
        rank[to] = moved;
        try { localStorage.setItem('sn_rank', JSON.stringify(rank)); } catch (_) { /* optional */ }
        record('suggestion_rank');
        renderRank();
      });
    });

    renderRank();

    var exportRank = document.getElementById('exportRank');
    if (exportRank) {
      exportRank.addEventListener('click', function () {
        var rows = ['rank,suggestion'];
        rank.forEach(function (suggestion, index) {
          rows.push((index + 1) + ',' + suggestion);
        });
        download('ranking.csv', rows.join('\n'));
      });
    }

    var resetRank = document.getElementById('resetRank');
    if (resetRank) {
      resetRank.addEventListener('click', function () {
        try {
          localStorage.removeItem('sn_rank');
          localStorage.removeItem('sn_decision');
        } catch (_) { /* optional */ }
        window.location.reload();
      });
    }

    var decisionForm = document.getElementById('decisionForm');
    if (decisionForm) {
      var savedDecision = readJSON('sn_decision', null);
      if (savedDecision && typeof savedDecision === 'object') {
        ['chosen', 'why', 'measure'].forEach(function (name) {
          var field = decisionForm.elements.namedItem(name);
          if (field && typeof savedDecision[name] === 'string') field.value = savedDecision[name];
        });
        var savedNote = document.getElementById('decisionSaved');
        if (savedNote) savedNote.textContent = 'A decision saved in this browser is loaded below.';
      }

      decisionForm.addEventListener('submit', function (event) {
        event.preventDefault();
        var chosen = decisionForm.elements.namedItem('chosen');
        var why = decisionForm.elements.namedItem('why');
        var measure = decisionForm.elements.namedItem('measure');
        var decision = {
          chosen: chosen ? chosen.value : '',
          why: why ? why.value : '',
          measure: measure ? measure.value : '',
          savedAt: new Date().toISOString()
        };
        try { localStorage.setItem('sn_decision', JSON.stringify(decision)); } catch (_) { /* optional */ }
        var confirmation = document.getElementById('decisionSaved');
        if (confirmation) confirmation.textContent = 'Saved in this browser only. Export the decision CSV to keep a separate copy.';
      });

      var exportDecision = document.getElementById('exportDecision');
      if (exportDecision) {
        exportDecision.addEventListener('click', function () {
          var fields = [
            ['field', 'value'],
            ['chosen', decisionForm.elements.namedItem('chosen').value],
            ['why', decisionForm.elements.namedItem('why').value],
            ['measure', decisionForm.elements.namedItem('measure').value]
          ];
          var csv = fields.map(function (row) {
            return row.map(csvCell).join(',');
          }).join('\n');
          download('decision.csv', csv);
        });
      }
    }
  }

  function csvCell(value) {
    var text = String(value == null ? '' : value);
    if (/^[\s]*[=+\-@]/.test(text)) text = "'" + text;
    return '"' + text.replace(/"/g, '""') + '"';
  }

  function download(filename, content) {
    var url = URL.createObjectURL(new Blob([content], { type: 'text/csv;charset=utf-8' }));
    var link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 0);
  }
})();
