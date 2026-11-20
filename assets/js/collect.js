/*
 * ShopNow Kitchen - first-party event collector.
 *
 * This is the network half of the measurement layer. The reader-visible
 * counter in assets/app.js stays exactly as it is: local only, in the
 * reader's own browser. This file talks to a collector the site operator
 * runs, and only if one is deployed.
 *
 * Privacy rules, enforced here rather than promised in prose:
 *   - no cookies, no localStorage writes, no advertising identifiers
 *   - no IP address, no user agent, no device fingerprint is ever sent
 *   - a search is sent as a length and a result count, never as the query
 *   - the session id is random per page load and dies with the tab
 *   - the request is same-origin by default and best-effort; a failure is
 *     swallowed and the reader never notices
 *
 * If no collector is deployed at the endpoint, nothing here has any effect.
 */
(function () {
  "use strict";

  var DEFAULT_ENDPOINT = "/api/collect";
  var EVENTS = ["page_view", "outbound_click", "guide_read", "search", "suggestion_rank"];
  var enabled = false;
  var endpoint = DEFAULT_ENDPOINT;

  /*
   * The collector is same-origin by default. A deployment that keeps the
   * static site on one host and the collector on another points at it with
   * <meta name="x-collect-endpoint" content="https://collector.example/collect">.
   */
  function resolveEndpoint() {
    var meta = document.querySelector('meta[name="x-collect-endpoint"]');
    var value = meta && meta.getAttribute("content");
    if (value && /^https?:\/\//i.test(value)) return value.replace(/\/+$/, "");
    return DEFAULT_ENDPOINT;
  }

  function sessionId() {
    var bytes = new Uint8Array(9);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(bytes);
    } else {
      for (var i = 0; i < bytes.length; i++) bytes[i] = Math.floor(Math.random() * 256);
    }
    return Array.prototype.map
      .call(bytes, function (b) { return ("0" + b.toString(16)).slice(-2); })
      .join("");
  }

  var sid = sessionId();

  function referrerHost() {
    try {
      if (!document.referrer) return "";
      var url = new URL(document.referrer);
      return url.hostname === location.hostname ? "" : url.hostname;
    } catch (e) {
      return "";
    }
  }

  function send(name, payload) {
    if (!enabled) return;
    if (EVENTS.indexOf(name) === -1) return;
    var body = {
      event: name,
      path: location.pathname,
      session_id: sid,
      ts: new Date().toISOString()
    };
    for (var key in payload || {}) {
      if (Object.prototype.hasOwnProperty.call(payload, key)) body[key] = payload[key];
    }
    if (!body.referrer_host) body.referrer_host = referrerHost();

    try {
      var payloadJson = JSON.stringify(body);
      if (navigator.sendBeacon) {
        // text/plain is a simple content type, so a beacon needs no preflight
        // and still leaves the page immediately.
        navigator.sendBeacon(
          endpoint,
          new Blob([payloadJson], { type: "text/plain;charset=UTF-8" })
        );
      } else {
        fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payloadJson,
          keepalive: true,
          credentials: "omit"
        }).catch(function () {});
      }
    } catch (e) {
      /* measurement must never break a reader's click */
    }
  }

  function wireOutboundClicks() {
    document.addEventListener(
      "click",
      function (event) {
        var anchor = event.target && event.target.closest ? event.target.closest("a") : null;
        if (!anchor) return;
        var productId = anchor.getAttribute("data-outbound");
        if (!productId) return;
        send("outbound_click", {
          product_id: productId,
          link_position: anchor.getAttribute("data-position") || "unknown"
        });
      },
      true
    );
  }

  function wireGuideRead() {
    if (!/\/guides\//.test(location.pathname)) return;
    if (!("IntersectionObserver" in window)) return;
    var footer = document.querySelector("footer");
    if (!footer) return;
    var guideId = location.pathname.split("/").pop().replace(/\.html$/, "");
    var fired = false;
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          // The footer entering the viewport means the reader reached the end
          // of the guide. That is the honest definition of "read".
          if (entry.isIntersecting && !fired) {
            fired = true;
            send("guide_read", { guide_id: guideId });
            observer.disconnect();
          }
        });
      },
      { threshold: 0.6 }
    );
    observer.observe(footer);
  }

  function wireSearch() {
    if (!/search\.html$/.test(location.pathname)) return;
    var query = "";
    try {
      query = new URLSearchParams(location.search).get("q") || "";
    } catch (e) {
      query = "";
    }
    if (!query) return;
    var results = document.querySelectorAll("#results li").length;
    send("search", {
      query_length: String(query.length),
      result_count: String(results)
    });
  }

  function wireSuggestionRank() {
    var table = document.getElementById("sugTable");
    if (!table) return;
    document.addEventListener("click", function (event) {
      var button = event.target && event.target.closest ? event.target.closest("[data-up],[data-down]") : null;
      if (!button) return;
      var id = button.getAttribute("data-up") || button.getAttribute("data-down");
      var rows = table.querySelectorAll("tr[data-sug]");
      var position = 0;
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].getAttribute("data-sug") === id) {
          position = i + 1;
          break;
        }
      }
      // The re-order happens in assets/app.js; the position is recorded on the
      // next tick, once the new order is in place.
      window.setTimeout(function () {
        var updated = table.querySelectorAll("tr[data-sug]");
        var now = 0;
        for (var j = 0; j < updated.length; j++) {
          if (updated[j].getAttribute("data-sug") === id) {
            now = j + 1;
            break;
          }
        }
        send("suggestion_rank", { suggestion_id: id, position: String(now || position) });
      }, 0);
    });
  }

  function init() {
    endpoint = resolveEndpoint();
    // Probe the collector once. If it is not there, the whole module stays inert.
    try {
      fetch(endpoint, { method: "GET", credentials: "omit" })
        .then(function (response) {
          if (response && response.ok) {
            enabled = true;
            boot();
          }
        })
        .catch(function () {});
    } catch (e) {
      enabled = false;
    }
  }

  function boot() {
    send("page_view", {});
    wireOutboundClicks();
    wireGuideRead();
    wireSearch();
    wireSuggestionRank();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
