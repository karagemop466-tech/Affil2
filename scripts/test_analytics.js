#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync(require('node:path').join(__dirname, '..', 'assets', 'app.js'), 'utf8');

function boot(pathname, hasSearchRequest) {
  const values = new Map();
  const handlers = {};
  const documentElement = {
    hasAttribute(name) { return name === 'data-search-request' && hasSearchRequest; }
  };
  const document = {
    documentElement,
    addEventListener(name, callback) { handlers[name] = callback; },
    querySelectorAll() { return []; },
    getElementById() { return null; }
  };
  const window = {
    location: { pathname, search: '' },
    setTimeout(callback) { callback(); }
  };
  const localStorage = {
    getItem(key) { return values.has(key) ? values.get(key) : null; },
    setItem(key, value) { values.set(key, String(value)); },
    removeItem(key) { values.delete(key); }
  };
  vm.runInNewContext(source, { document, window, localStorage, URLSearchParams, URL, Blob, JSON, Number, Object, Array, String, Math });
  return { values, handlers, window };
}

const home = boot('/Affil2/index.html', false);
let metrics = JSON.parse(home.values.get('sn_metrics_v1'));
assert.equal(metrics.version, 1);
assert.equal(metrics.counts.page_view, 1);
assert.deepEqual(Object.keys(metrics.counts).sort(), [
  'guide_read', 'outbound_click', 'page_view', 'search', 'suggestion_rank'
]);
assert.equal(home.values.has('sn_events'), false, 'legacy event-level history is removed');

home.window.ShopNowMetrics.recordSearch();
metrics = JSON.parse(home.values.get('sn_metrics_v1'));
assert.equal(metrics.counts.search, 1);
assert.equal(JSON.stringify(metrics).includes('query'), false, 'raw query data is not recorded');

const anchor = { getAttribute(name) { return name === 'data-outbound' ? 'P-02' : ''; } };
home.handlers.click({ target: { closest(selector) { return selector === '[data-outbound]' ? anchor : null; } } });
metrics = JSON.parse(home.values.get('sn_metrics_v1'));
assert.equal(metrics.counts.outbound_click, 1);
assert.deepEqual(JSON.parse(home.values.get('sn_clicks')), { 'P-02': 1 });

const searchPage = boot('/Affil2/search.html', true);
metrics = JSON.parse(searchPage.values.get('sn_metrics_v1'));
assert.equal(metrics.counts.page_view, 1);
assert.equal(metrics.counts.search, 1, 'a submitted search is counted without storing its text');

console.log('analytics event and privacy checks passed');
