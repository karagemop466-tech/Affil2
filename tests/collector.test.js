/*
 * Tests for the self-hosted event collector.
 *
 * Run with:  node tests/collector.test.js
 * No test framework, no npm install.
 */

const assert = require("assert");
const path = require("path");

const collector = require(path.join(__dirname, "..", "functions", "api", "collect.js"));
const server = require(path.join(__dirname, "..", "analytics", "server.js"));

const sanitize = collector.sanitize;
const ALLOWED_EVENTS = collector.ALLOWED_EVENTS;

let passed = 0;
function test(name, fn) {
  try {
    fn();
    passed++;
    console.log("  ok  - " + name);
  } catch (err) {
    console.error("  FAIL- " + name);
    console.error("        " + err.message);
    process.exitCode = 1;
  }
}

console.log("collector");

test("accepts exactly the five documented events", function () {
  assert.deepStrictEqual(ALLOWED_EVENTS, [
    "page_view",
    "outbound_click",
    "guide_read",
    "search",
    "suggestion_rank",
  ]);
});

test("rejects an event that is not in the schema", function () {
  assert.strictEqual(sanitize({ event: "secret_event" }), null);
  assert.strictEqual(sanitize({ event: "purchase" }), null);
  assert.strictEqual(sanitize({ event: "conversion" }), null);
  assert.strictEqual(sanitize({}), null);
  assert.strictEqual(sanitize(null), null);
  assert.strictEqual(sanitize([{ event: "page_view" }]), null);
});

test("keeps only the documented fields", function () {
  const clean = sanitize({
    event: "page_view",
    path: "/guides/",
    session_id: "abc123",
    email: "reader@example.com",
    name: "A Reader",
    ip: "203.0.113.9",
    user_agent: "Mozilla/5.0",
    fingerprint: "abc",
  });
  assert.strictEqual(clean.email, undefined);
  assert.strictEqual(clean.name, undefined);
  assert.strictEqual(clean.ip, undefined);
  assert.strictEqual(clean.user_agent, undefined);
  assert.strictEqual(clean.fingerprint, undefined);
  assert.strictEqual(clean.path, "/guides/");
});

test("strips the query string and the host from a path", function () {
  const clean = sanitize({
    event: "page_view",
    path: "https://site.example/guides/?utm_source=x&id=9#top",
  });
  assert.strictEqual(clean.path, "/guides/");
});

test("keeps a bare referrer host and drops anything else", function () {
  assert.strictEqual(sanitize({ event: "page_view", referrer_host: "news.example" }).referrer_host, "news.example");
  assert.strictEqual(sanitize({ event: "page_view", referrer_host: "https://news.example/a?b=1" }).referrer_host, "news.example");
  assert.strictEqual(sanitize({ event: "page_view", referrer_host: "javascript:alert(1)" }).referrer_host, "");
  assert.strictEqual(sanitize({ event: "page_view", referrer_host: "localhost" }).referrer_host, "");
});

test("reduces a session id to a safe alphabet", function () {
  const clean = sanitize({ event: "page_view", session_id: "ab-12_cd<script>" });
  assert.strictEqual(clean.session_id, "ab12cdscript");
});

test("reduces identifiers to a safe shape", function () {
  const clean = sanitize({ event: "outbound_click", product_id: "P-01", link_position: "hero; drop" });
  assert.strictEqual(clean.product_id, "P-01");
  assert.strictEqual(clean.link_position, "herodrop");
});

test("keeps only digits for counts", function () {
  const clean = sanitize({ event: "search", query_length: "12 chars", result_count: "3;drop" });
  assert.strictEqual(clean.query_length, "12");
  assert.strictEqual(clean.result_count, "3");
});

test("never stores the text of a search query", function () {
  const clean = sanitize({ event: "search", q: "my email is reader@example.com", query: "reader@example.com" });
  assert.strictEqual(clean.q, undefined);
  assert.strictEqual(clean.query, undefined);
});

test("caps a long string", function () {
  const clean = sanitize({ event: "page_view", path: "/" + "a".repeat(5000) });
  assert.ok(clean.path.length <= 300);
});

test("stamps a received_at time", function () {
  const clean = sanitize({ event: "page_view" });
  assert.ok(/^\d{4}-\d{2}-\d{2}T/.test(clean.received_at));
});

test("the node server and the pages function share one sanitize rule", function () {
  const raw = { event: "page_view", path: "/x/", session_id: "s1", cookie: "a=b" };
  const a = sanitize(raw);
  const b = server.sanitize(raw);
  assert.strictEqual(a.cookie, undefined);
  assert.strictEqual(b.cookie, undefined);
  assert.strictEqual(a.path, b.path);
  assert.strictEqual(a.session_id, b.session_id);
});

test("the event schema file matches the collector", function () {
  const fs = require("fs");
  const schema = JSON.parse(
    fs.readFileSync(path.join(__dirname, "..", "data", "events.json"), "utf8")
  );
  const declared = schema.events.map(function (e) { return e.name; });
  assert.deepStrictEqual(declared, ALLOWED_EVENTS);
  assert.deepStrictEqual(server.ALLOWED_EVENTS, ALLOWED_EVENTS);
});

console.log("");
console.log(passed + " checks passed");
if (process.exitCode) {
  console.error("collector tests FAILED");
} else {
  console.log("collector tests OK");
}
