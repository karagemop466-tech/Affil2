/*
 * Browser-local measurement for the static GitHub Pages publication.
 * Five named events are stored as aggregate counters only. No raw search text,
 * event timeline, page path, referrer, timestamp, IP address, or decision text is
 * included in the measurement record. Nothing is sent to a server.
 */
(function () {
  'use strict';

  var METRICS_KEY = 'sn_metrics_v1';
  var CLICKS_KEY = 'sn_clicks';
  var EVENTS = ['page_view', 'outbound_click', 'guide_read', 'search', 'suggestion_rank'];
  var PRODUCT_ID = /^P-\d{2}$/;
  var SUGGESTION_ID = /^SG-\d{2}$/;

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
  var firstRun = !storedMetrics || storedMetrics.version !== 1 || !storedMetrics.counts;
  var metrics = blankMetrics();
  if (!firstRun) {
    EVENTS.forEach(function (name) {
      var count = Number(storedMetrics.counts[name]);
      metrics.counts[name] = Number.isFinite(count) && count > 0 ? Math.floor(count) : 0;
    });
  }

  var clicks = cleanClicks(readJSON(CLICKS_KEY, {}));

  // Remove the earlier event-by-event log (which could contain a query or URL).
  // Only migrate event names to counts; never copy its event details forward.
  try {
    var legacyEvents = JSON.parse(localStorage.getItem('sn_events') || '[]');
    if (firstRun && Array.isArray(legacyEvents)) {
      legacyEvents.forEach(function (event) {
        if (event && EVENTS.indexOf(event.e) !== -1 && event.e !== 'outbound_click') {
          metrics.counts[event.e] += 1;
        }
      });
    }
  } catch (_) { /* old storage may be malformed */ }
  try { localStorage.removeItem('sn_events'); } catch (_) { /* optional storage */ }
  if (firstRun) metrics.counts.outbound_click = sumClicks(clicks);

  function saveMetrics() {
    try { localStorage.setItem(METRICS_KEY, JSON.stringify(metrics)); } catch (_) { /* optional storage */ }
  }

  function saveClicks() {
    try { localStorage.setItem(CLICKS_KEY, JSON.stringify(clicks)); } catch (_) { /* optional storage */ }
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

  function csv(rows) {
    return rows.map(function (row) {
      return row.map(csvCell).join(',');
    }).join('\n');
  }

  record('page_view');
  if (/\/guides\/[^/]+\.html$/.test(window.location.pathname)) record('guide_read');
  saveMetrics();
  updateLocalClickCount();

  // Product clicks are delegated so a click on nested button text is counted too.
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

  // Header searches pass a one-time fragment, which browsers do not send in the
  // HTTP request. The search page clears the fragment after reading it.
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

  // Client-side search: all untrusted strings are rendered with textContent.
  // No user query is interpolated into HTML or written to local storage.
  var searchForm = document.querySelector('form.searchpage');
  var searchInput = document.getElementById('sq');
  var searchIndexNode = document.getElementById('searchIndex');
  var results = document.getElementById('results');
  if (searchForm && searchInput && searchIndexNode && results) {
    var searchIndex = [];
    try {
      var parsedIndex = JSON.parse(searchIndexNode.textContent || '[]');
      if (Array.isArray(parsedIndex)) searchIndex = parsedIndex;
    } catch (_) { searchIndex = []; }

    function showMessage(text) {
      var message = document.createElement('p');
      message.textContent = text;
      results.replaceChildren(message);
    }

    function renderSearch(query) {
      results.replaceChildren();
      var terms = query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
      if (!terms.length) {
        showMessage('Enter a product, feature, or question to search this publication.');
        return 0;
      }

      var matches = searchIndex.filter(function (entry) {
        var searchable = [entry.t || '', entry.d || '', entry.k || ''].join(' ').toLocaleLowerCase();
        return terms.every(function (term) { return searchable.includes(term); });
      });
      if (!matches.length) {
        showMessage('No matches. Try a broader topic such as basket, capacity, or thermometer.');
        return 0;
      }

      var sitePath = new URL('.', window.location.href).pathname;
      var cards = [];
      matches.forEach(function (entry) {
        var destination;
        try { destination = new URL(entry.u, window.location.href); } catch (_) { return; }
        if (destination.origin !== window.location.origin || !destination.pathname.startsWith(sitePath)) return;
        var card = document.createElement('article');
        card.className = 'hit';
        var category = document.createElement('p');
        category.className = 'where';
        category.textContent = entry.k || 'ShopNow Kitchen';
        var heading = document.createElement('h3');
        var link = document.createElement('a');
        link.href = entry.u;
        link.textContent = entry.t || entry.u;
        heading.appendChild(link);
        card.appendChild(category);
        card.appendChild(heading);
        if (entry.d) {
          var summary = document.createElement('p');
          summary.textContent = String(entry.d)
            .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–')
            .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
            .replace(/&plusmn;/g, '±').replace(/&deg;/g, '°');
          card.appendChild(summary);
        }
        cards.push(card);
      });
      if (!cards.length) {
        showMessage('No matches. Try a broader topic such as basket, capacity, or thermometer.');
        return 0;
      }
      var count = cards.length;
      var summary = document.createElement('p');
      summary.className = 'small';
      summary.textContent = count === 1 ? 'One match.' : count + ' matches.';
      results.appendChild(summary);
      cards.forEach(function (card) { results.appendChild(card); });
      return count;
    }

    function cleanSearchUrl() {
      try { window.history.replaceState(null, '', window.location.pathname); } catch (_) { /* optional */ }
    }

    var fragment = new URLSearchParams(window.location.hash.slice(1));
    var legacyParams = new URLSearchParams(window.location.search);
    var queryFromUrl = fragment.get('q');
    var legacyQuery = legacyParams.get('q');
    var initialQuery = (queryFromUrl || legacyQuery || '').trim().slice(0, 120);
    if (initialQuery) {
      searchInput.value = initialQuery;
      renderSearch(initialQuery);
      record('search');
      cleanSearchUrl();
    } else {
      showMessage('Enter a product, feature, or question to search this publication.');
    }

    searchForm.addEventListener('submit', function (event) {
      event.preventDefault();
      var query = searchInput.value.trim().slice(0, 120);
      if (!query) {
        showMessage('Enter a product, feature, or question to search this publication.');
        return;
      }
      renderSearch(query);
      record('search');
      cleanSearchUrl();
    });
  }

  var exportClicks = document.getElementById('exportClicks');
  if (exportClicks) {
    exportClicks.addEventListener('click', function () {
      var rows = [['product', 'clicks']];
      Object.keys(clicks).sort().forEach(function (product) {
        rows.push([product, clicks[product]]);
      });
      download('clicks.csv', csv(rows));
    });
  }

  var exportEvents = document.getElementById('exportEvents');
  if (exportEvents) {
    exportEvents.addEventListener('click', function () {
      var rows = [['event', 'count']];
      EVENTS.forEach(function (name) { rows.push([name, metrics.counts[name]]); });
      download('event-counts.csv', csv(rows));
    });
  }

  // Suggestion order and the explicitly saved decision worksheet are local
  // reader choices, not part of the aggregate event record.
  var rank = readJSON('sn_rank', []);
  if (!Array.isArray(rank)) rank = [];
  var suggestionTable = document.getElementById('sugTable');
  if (suggestionTable) {
    var rows = Array.prototype.slice.call(document.querySelectorAll('#sugTable tbody tr[data-sug]'));
    var availableIds = rows.map(function (row) { return row.getAttribute('data-sug'); })
      .filter(function (id) { return SUGGESTION_ID.test(id); });
    rank = rank.filter(function (id, index, all) {
      return SUGGESTION_ID.test(id) && availableIds.indexOf(id) !== -1 && all.indexOf(id) === index;
    });
    availableIds.forEach(function (id) { if (rank.indexOf(id) === -1) rank.push(id); });

    function renderRank() {
      rows.forEach(function (row) {
        var label = row.querySelector('.rank');
        if (!label) return;
        var position = rank.indexOf(row.getAttribute('data-sug'));
        label.textContent = position >= 0 ? '#' + (position + 1) : '';
      });
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
        var csvRows = [['rank', 'suggestion']];
        rank.forEach(function (id, index) { csvRows.push([index + 1, id]); });
        download('ranking.csv', csv(csvRows));
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
        var decision = {};
        ['chosen', 'why', 'measure'].forEach(function (name) {
          var field = decisionForm.elements.namedItem(name);
          decision[name] = field ? field.value : '';
        });
        try { localStorage.setItem('sn_decision', JSON.stringify(decision)); } catch (_) { /* optional */ }
        var confirmation = document.getElementById('decisionSaved');
        if (confirmation) confirmation.textContent = 'Saved in this browser only. Export your decision to keep a copy.';
      });

      var exportDecision = document.getElementById('exportDecision');
      if (exportDecision) {
        exportDecision.addEventListener('click', function () {
          var csvRows = [['field', 'value']];
          ['chosen', 'why', 'measure'].forEach(function (name) {
            var field = decisionForm.elements.namedItem(name);
            csvRows.push([name, field ? field.value : '']);
          });
          download('decision.csv', csv(csvRows));
        });
      }
    }
  }
})();
