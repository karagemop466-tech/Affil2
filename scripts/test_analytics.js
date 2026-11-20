#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'assets', 'app.js'), 'utf8');

function makeNode(tagName, attributes = {}) {
  const listeners = {};
  const attrs = { ...attributes };
  let text = '';
  const node = {
    tagName: tagName.toUpperCase(),
    attributes: attrs,
    children: [],
    className: '',
    value: '',
    href: '',
    download: '',
    listeners,
    addEventListener(name, callback) { (listeners[name] ||= []).push(callback); },
    emit(name, event = {}) { (listeners[name] || []).forEach((callback) => callback(event)); },
    appendChild(child) { this.children.push(child); return child; },
    prepend(child) { this.children.unshift(child); return child; },
    replaceChildren(...children) { this.children = children; },
    remove() {},
    click() {},
    getAttribute(name) { return attrs[name] || ''; },
    hasAttribute(name) { return Object.hasOwn(attrs, name); },
    querySelector(selector) {
      if (selector === 'input[name="q"]') return this.searchInput || null;
      if (selector === '.rank') return this.rankNode || null;
      return null;
    },
    closest() { return null; }
  };
  Object.defineProperty(node, 'textContent', {
    get() { return text + this.children.map((child) => child.textContent || '').join(''); },
    set(value) { text = String(value); this.children = []; }
  });
  Object.defineProperty(node, 'innerHTML', {
    get() { return ''; },
    set() { throw new Error('innerHTML must not be used for untrusted search content'); }
  });
  return node;
}

function boot(options = {}) {
  const values = new Map(Object.entries(options.storage || {}));
  const documentListeners = {};
  const nodes = {};
  const location = {
    pathname: options.pathname || '/Affil2/index.html',
    origin: 'https://example.test',
    search: options.search || '',
    hash: options.hash || '',
    href: 'https://example.test' + (options.pathname || '/Affil2/index.html') +
      (options.search || '') + (options.hash || ''),
    assigned: '',
    assign(url) { this.assigned = String(url); }
  };
  const window = {
    location,
    history: {
      replacements: [],
      replaceState(_state, _title, url) {
        this.replacements.push(url);
        location.search = '';
        location.hash = '';
        location.href = 'https://example.test' + url;
      }
    },
    setTimeout(callback) { callback(); }
  };
  const storage = {
    getItem(key) { return values.has(key) ? String(values.get(key)) : null; },
    setItem(key, value) { values.set(key, String(value)); },
    removeItem(key) { values.delete(key); }
  };

  const outboundClickAnchor = options.outbound ? makeNode('a', { 'data-outbound': 'P-02' }) : null;
  const headerForms = [];
  if (options.headerSearch) {
    const input = makeNode('input', { name: 'q' });
    input.value = options.headerSearch;
    const form = makeNode('form', { action: 'search.html' });
    form.searchInput = input;
    headerForms.push(form);
  }

  if (options.searchPage) {
    const form = makeNode('form');
    const input = makeNode('input');
    const results = makeNode('div');
    const index = makeNode('script');
    index.textContent = JSON.stringify(options.searchIndex || []);
    form.searchInput = input;
    form.querySelector = (selector) => selector === 'input[name="q"]' ? input : null;
    nodes.searchForm = form;
    nodes.sq = input;
    nodes.results = results;
    nodes.searchIndex = index;
  }

  let suggestionRows = [];
  let suggestionButtons = [];
  if (options.suggestions) {
    const table = makeNode('table');
    nodes.sugTable = table;
    suggestionRows = ['SG-01', 'SG-02'].map((id) => {
      const row = makeNode('tr', { 'data-sug': id });
      row.rankNode = makeNode('span');
      row.querySelector = (selector) => selector === '.rank' ? row.rankNode : null;
      return row;
    });
    const up = makeNode('button', { 'data-up': 'SG-02' });
    const down = makeNode('button', { 'data-down': 'SG-01' });
    up.hasAttribute = (name) => name === 'data-up';
    down.hasAttribute = (name) => name === 'data-down';
    suggestionButtons = [up, down];
    nodes.upButton = up;
  }

  const document = {
    body: makeNode('body'),
    addEventListener(name, callback) { documentListeners[name] = callback; },
    querySelector(selector) { return selector === 'form.searchpage' ? nodes.searchForm || null : null; },
    querySelectorAll(selector) {
      if (selector === 'header form[role="search"]') return headerForms;
      if (selector === '[data-up],[data-down]') return suggestionButtons;
      if (selector === '#sugTable tbody tr[data-sug]') return suggestionRows;
      return [];
    },
    getElementById(id) { return nodes[id] || null; },
    createElement(tagName) { return makeNode(tagName); }
  };
  if (options.outbound) {
    documentListeners.click = null;
  }

  const context = {
    document,
    window,
    localStorage: storage,
    URL,
    URLSearchParams,
    Blob,
    console
  };
  vm.runInNewContext(source, context, { filename: 'assets/app.js' });

  return { values, document, documentListeners, headerForms, location, window, nodes, suggestionRows };
}

function getMetrics(result) {
  return JSON.parse(result.values.get('sn_metrics_v1'));
}

const home = boot();
let metrics = getMetrics(home);
assert.equal(metrics.version, 1);
assert.equal(metrics.counts.page_view, 1);
assert.deepEqual(Object.keys(metrics.counts).sort(), [
  'guide_read', 'outbound_click', 'page_view', 'search', 'suggestion_rank'
]);
assert.equal(home.values.has('sn_events'), false, 'legacy event-level history is erased');
assert.equal(JSON.stringify(metrics).includes('pathname'), false, 'no page path in counters');

const legacy = boot({
  storage: {
    sn_events: JSON.stringify([
      { e: 'search', q: 'private query text', t: 123, page: '/search.html' },
      { e: 'page_view', t: 124, page: '/index.html' }
    ]),
    sn_clicks: JSON.stringify({ 'P-01': 2, unknown: 99 })
  }
});
metrics = getMetrics(legacy);
assert.equal(metrics.counts.search, 1, 'legacy event names may migrate as aggregate counts');
assert.equal(metrics.counts.page_view, 2, 'legacy page count plus current page view');
assert.equal(metrics.counts.outbound_click, 2, 'only valid aggregate product clicks migrate');
assert.equal(legacy.values.has('sn_events'), false);
assert.equal(JSON.stringify(legacy.values.get('sn_metrics_v1')).includes('private query'), false);

const payload = '<img src=x onerror=alert(1)>';
const search = boot({
  pathname: '/Affil2/search.html',
  hash: '#q=' + encodeURIComponent(payload),
  searchPage: true,
  searchIndex: [{ t: payload, u: 'products/p01-example.html', d: 'A safe summary' }]
});
metrics = getMetrics(search);
assert.equal(metrics.counts.search, 1, 'a submitted search is counted');
assert.equal(search.nodes.sq.value, payload, 'query is held in the input only');
const card = search.nodes.results.children.find((child) => child.tagName === 'ARTICLE');
assert.ok(card, 'matching results render as a result card');
const anchor = card.children[1].children[0];
assert.equal(anchor.textContent, payload, 'untrusted title is inserted as text');
assert.equal(anchor.href, 'products/p01-example.html');
assert.ok(search.window.history.replacements.includes('/Affil2/search.html'), 'query fragment is removed from the address bar');
assert.equal(JSON.stringify([...search.values.entries()]).includes(payload), false, 'raw query is never persisted');

const header = boot({ pathname: '/Affil2/index.html', headerSearch: 'counter space' });
let prevented = false;
header.headerForms[0].emit('submit', { preventDefault() { prevented = true; } });
assert.equal(prevented, true);
assert.ok(header.location.assigned.endsWith('/Affil2/search.html#q=counter%20space'));
assert.equal(header.location.search, '', 'header search does not add a query string to the HTTP request');
assert.equal(header.values.has('sn_metrics_v1'), true);
assert.equal(JSON.stringify([...header.values.entries()]).includes('counter space'), false);

const guide = boot({ pathname: '/Affil2/guides/basket-vs-oven.html' });
assert.equal(getMetrics(guide).counts.guide_read, 1, 'guide_read means a guide page was loaded');

const outbound = boot({ outbound: true });
const outboundAnchor = makeNode('a', { 'data-outbound': 'P-02' });
outboundAnchor.getAttribute = (name) => name === 'data-outbound' ? 'P-02' : '';
outbound.documentListeners.click({ target: { closest(selector) {
  return selector === '[data-outbound]' ? outboundAnchor : null;
} } });
assert.equal(getMetrics(outbound).counts.outbound_click, 1);
assert.deepEqual(JSON.parse(outbound.values.get('sn_clicks')), { 'P-02': 1 });

const suggestions = boot({ suggestions: true });
suggestions.nodes.upButton.emit('click');
assert.equal(getMetrics(suggestions).counts.suggestion_rank, 1);
assert.deepEqual(JSON.parse(suggestions.values.get('sn_rank')), ['SG-02', 'SG-01']);

console.log('analytics, local search, and privacy checks passed');
