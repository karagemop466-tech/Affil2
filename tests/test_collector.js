#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');

const { createCollectorServer, validatePayload } = require('../analytics/server');

function requestJson(port, method, reqPath, bodyText) {
  return new Promise((resolve, reject) => {
    const headers = {};
    if (bodyText !== undefined) {
      headers['Content-Type'] = 'application/json';
      headers['Content-Length'] = Buffer.byteLength(bodyText);
    }
    const req = http.request({ host: '127.0.0.1', port, method, path: reqPath, headers }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const text = Buffer.concat(chunks).toString('utf8');
        let json = null;
        try { json = JSON.parse(text); } catch (_) {}
        resolve({ status: res.statusCode, headers: res.headers, text, json });
      });
    });
    req.on('error', reject);
    if (bodyText !== undefined) req.write(bodyText);
    req.end();
  });
}

async function testCollectorValidationAndServer() {
  // Unit validation checks
  assert.equal(validatePayload(null).ok, false);
  assert.equal(validatePayload([]).ok, false);
  assert.equal(validatePayload({ e: 'page_view', page: '/index.html', ip: '1.2.3.4' }).ok, false);
  assert.equal(validatePayload({ e: 'search', page: '/search.html', q_len: 5, results: 2, query_text: 'air fryer' }).ok, false);
  assert.equal(validatePayload({ e: 'outbound_click', page: '/shop.html', product: 'BAD' }).ok, false);
  assert.equal(validatePayload({ e: 'unknown_evt', page: '/' }).ok, false);

  const goodSearch = validatePayload({ e: 'search', page: '/search.html?q=secret', q_len: 6, results: 3, t: 1700000123456 });
  assert.equal(goodSearch.ok, true);
  assert.equal(goodSearch.value.page, '/search.html'); // query stripped
  assert.equal(goodSearch.value.t % 60000, 0); // coarsened to minute

  // Live HTTP server checks on ephemeral port
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'shopnow-test-'));
  const logFile = path.join(tmpDir, 'events.ndjson');
  const server = createCollectorServer({ logFile });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const { port } = server.address();

  try {
    const health = await requestJson(port, 'GET', '/api/collect');
    assert.equal(health.status, 200);
    assert.equal(health.json.ok, true);
    assert.equal(health.json.cookies, false);
    assert.equal(health.headers['set-cookie'], undefined);

    const validPayloads = [
      { e: 'page_view', page: '/index.html' },
      { e: 'guide_read', page: '/guides/basket-vs-oven.html' },
      { e: 'outbound_click', page: '/products/p01-chefman-6qt-dual-basket.html', product: 'P-01' },
      { e: 'search', page: '/search.html', q_len: 11, results: 2 },
      { e: 'suggestion_rank', page: '/suggestions.html', rank: ['SG-07', 'SG-13'] }
    ];
    for (const payload of validPayloads) {
      const res = await requestJson(port, 'POST', '/api/collect', JSON.stringify(payload));
      assert.equal(res.status, 202);
      assert.equal(res.json.recorded, payload.e);
      assert.equal(res.headers['set-cookie'], undefined);
    }

    const lines = fs.readFileSync(logFile, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
    assert.equal(lines.length, 5);
    assert.deepEqual(lines.map((l) => l.e), ['page_view', 'guide_read', 'outbound_click', 'search', 'suggestion_rank']);

    // Rejections
    const forbiddenRes = await requestJson(port, 'POST', '/api/collect', JSON.stringify({
      e: 'page_view', page: '/index.html', cookie: 'abc'
    }));
    assert.equal(forbiddenRes.status, 400);

    const badJsonRes = await requestJson(port, 'POST', '/api/collect', '{broken');
    assert.equal(badJsonRes.status, 400);

    const hugeRes = await requestJson(port, 'POST', '/api/collect', JSON.stringify({
      e: 'page_view', page: '/' + 'a'.repeat(5000)
    }));
    assert.equal(hugeRes.status, 413);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

async function testCloudflareFunctionModule() {
  const fnUrl = require('node:url').pathToFileURL(path.resolve(__dirname, '..', 'functions', 'api', 'collect.js')).href;
  const mod = await import(fnUrl);
  const getResp = await mod.onRequestGet();
  assert.equal(getResp.status, 200);
  const getBody = await getResp.json();
  assert.equal(getBody.ok, true);
  assert.equal(getBody.cookies, false);

  const stored = [];
  const fakePost = (obj) => mod.onRequestPost({
    request: new Request('https://example.invalid/api/collect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(obj)
    }),
    env: { SN_EVENTS: { put: async (k, v) => stored.push({ k, v: JSON.parse(v) }) } }
  });

  const okResp = await fakePost({ e: 'outbound_click', page: '/shop.html', product: 'P-04' });
  assert.equal(okResp.status, 202);
  assert.equal(stored.length, 1);
  assert.equal(stored[0].v.product, 'P-04');

  const badResp = await fakePost({ e: 'page_view', page: '/shop.html', fingerprint: 'xyz' });
  assert.equal(badResp.status, 400);
}

function makeFakeElement(tag, id, attrs = {}) {
  const el = {
    tagName: tag.toUpperCase(),
    id: id || '',
    attrs: Object.assign({}, attrs),
    children: [],
    listeners: {},
    classList: {
      _set: new Set(),
      toggle(cls) {
        if (this._set.has(cls)) { this._set.delete(cls); return false; }
        this._set.add(cls); return true;
      },
      contains(cls) { return this._set.has(cls); },
      remove(cls) { this._set.delete(cls); }
    },
    value: attrs.value || '',
    textContent: '',
    content: attrs.content || '',
    href: attrs.href || '',
    get firstChild() { return this.children[0] || null; },
    appendChild(child) { this.children.push(child); return child; },
    removeChild(child) {
      const idx = this.children.indexOf(child);
      if (idx >= 0) this.children.splice(idx, 1);
      return child;
    },
    addEventListener(type, fn) {
      (this.listeners[type] = this.listeners[type] || []).push(fn);
    },
    dispatch(type, evt = {}) {
      (this.listeners[type] || []).forEach((fn) => fn(Object.assign({ preventDefault() {} }, evt)));
    },
    getAttribute(k) { return this.attrs[k] ?? null; },
    setAttribute(k, v) { this.attrs[k] = String(v); },
    hasAttribute(k) { return Object.prototype.hasOwnProperty.call(this.attrs, k); },
    querySelector() { return null; },
    closest() { return null; },
    click() { this.clicked = true; },
    focus() { this.focused = true; }
  };
  return el;
}

function testAppJsClientBehavior() {
  const appCode = fs.readFileSync(path.resolve(__dirname, '..', 'assets', 'app.js'), 'utf8');
  const searchHtml = fs.readFileSync(path.resolve(__dirname, '..', 'search.html'), 'utf8');
  const idxMatch = searchHtml.match(/<script type="application\/json" id="searchIndex">([\s\S]*?)<\/script>/);
  assert.ok(idxMatch, 'search.html must embed searchIndex');

  const store = {};
  const localStorage = {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; }
  };
  const sStore = { sn_search_query: 'two baskets' };
  const sessionStorage = {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(sStore, k) ? sStore[k] : null),
    setItem: (k, v) => { sStore[k] = String(v); },
    removeItem: (k) => { delete sStore[k]; }
  };

  const navBtn = makeFakeElement('button', '');
  const navMenu = makeFakeElement('nav', 'primary-nav');
  const searchInput = makeFakeElement('input', 'sq');
  const headerInput = makeFakeElement('input', 'q');
  const searchForm = makeFakeElement('form', '');
  searchForm.querySelector = () => searchInput;
  searchInput.closest = () => searchForm;
  const searchMeta = makeFakeElement('p', 'searchMeta');
  const resultsEl = makeFakeElement('div', 'results');
  const searchIdxEl = makeFakeElement('script', 'searchIndex');
  searchIdxEl.textContent = idxMatch[1];
  const exportEventsBtn = makeFakeElement('button', 'exportEvents');
  const outboundBtn = makeFakeElement('a', '', { 'data-outbound': 'P-01' });
  const metaCollector = makeFakeElement('meta', '', { content: '' });

  const byId = {
    'primary-nav': navMenu,
    sq: searchInput,
    q: headerInput,
    searchMeta,
    results: resultsEl,
    searchIndex: searchIdxEl,
    exportEvents: exportEventsBtn
  };

  const fetchCalls = [];
  const docListeners = {};
  const blobsCreated = [];
  const navigatedUrls = [];

  const sandbox = {
    window: {},
    location: {
      pathname: '/guides/basket-vs-oven.html',
      search: '',
      assign: (u) => navigatedUrls.push(u)
    },
    localStorage,
    sessionStorage,
    Blob: function FakeBlob(parts) { blobsCreated.push(parts.join('')); this.parts = parts; },
    URL: { createObjectURL: () => 'blob:mock', revokeObjectURL: () => {} },
    Date,
    Object,
    Array,
    JSON,
    Math,
    String,
    Number,
    Boolean,
    setTimeout: () => {},
    fetch: (url, opts) => {
      fetchCalls.push({ url, opts });
      return Promise.resolve({ ok: true });
    },
    document: {
      body: makeFakeElement('body', ''),
      createElement: (tag) => makeFakeElement(tag, ''),
      getElementById: (id) => byId[id] || null,
      querySelector: (sel) => {
        if (sel === '.navtoggle') return navBtn;
        if (sel === 'meta[name="sn-collect-endpoint"]') return metaCollector;
        return null;
      },
      querySelectorAll: (sel) => {
        if (sel === '[data-outbound]') return [outboundBtn];
        if (sel === 'form[role="search"]') return [searchForm];
        return [];
      },
      addEventListener: (t, fn) => { (docListeners[t] = docListeners[t] || []).push(fn); }
    }
  };
  sandbox.window.history = { replaceState() {} };

  // Run 1: default static mode -> 0 fetch requests even with events firing
  vm.runInNewContext(appCode, sandbox);
  assert.equal(fetchCalls.length, 0, 'Static mode must send zero analytics requests');
  assert.equal(sessionStorage.getItem('sn_search_query'), null, 'sn_search_query must clear after handoff');

  const loggedEvents = JSON.parse(localStorage.getItem('sn_events'));
  assert.ok(loggedEvents.some((e) => e.e === 'page_view'));
  assert.ok(loggedEvents.some((e) => e.e === 'guide_read'));
  const searchEv = loggedEvents.find((e) => e.e === 'search');
  assert.ok(searchEv, 'search event must fire for ?q=two+baskets');
  assert.equal(searchEv.q_len, 11);
  assert.ok(searchEv.results >= 1);
  assert.equal(searchEv.query_text, undefined, 'raw search text must not be recorded');
  assert.ok(resultsEl.children.length >= 1, 'search.html must render matching .hit cards');

  // Mobile nav toggle
  navBtn.dispatch('click');
  assert.equal(navMenu.classList.contains('open'), true);
  assert.equal(navBtn.getAttribute('aria-expanded'), 'true');
  docListeners.keydown.forEach((fn) => fn({ key: 'Escape' }));
  assert.equal(navMenu.classList.contains('open'), false);
  assert.equal(navBtn.getAttribute('aria-expanded'), 'false');

  // Outbound click & exportEvents CSV
  outboundBtn.dispatch('click');
  const clicks = JSON.parse(localStorage.getItem('sn_clicks'));
  assert.equal(clicks['P-01'], 1);
  exportEventsBtn.dispatch('click');
  assert.ok(blobsCreated.some((csv) => csv.startsWith('event,timestamp_iso,page,detail') && csv.includes('outbound_click')));

  // Run 2: configured collector endpoint -> sends cookieless POST without forbidden fields
  metaCollector.content = 'https://collector.example/api/collect';
  vm.runInNewContext(appCode, sandbox);
  assert.ok(fetchCalls.length >= 2);
  const posted = JSON.parse(fetchCalls[0].opts.body);
  assert.equal(fetchCalls[0].opts.credentials, 'omit');
  assert.equal(posted.e, 'page_view');
  assert.equal(posted.t % 60000, 0);
}

(async () => {
  await testCollectorValidationAndServer();
  await testCloudflareFunctionModule();
  testAppJsClientBehavior();
  console.log('ALL JS COLLECTOR AND CLIENT TESTS PASS');
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
