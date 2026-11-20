/* Privacy-preserving event hook for Countertop Journal.
 * - No cookies, no local storage IDs, no fingerprinting.
 * - Sends only: event name, page path, and UTC day. No IP is read by this script.
 * - DISABLED while AFFIL_CONFIG.endpoint is empty (the current state, see data/site.json).
 * - Five events: page_view, product_view, outbound_click, guide_view, feed_open (proposed; see Suggestions S-07).
 */
(function () {
  var cfg = window.AFFIL_CONFIG || {};
  var endpoint = cfg.endpoint || "";

  function send(name, extra) {
    if (!endpoint || !navigator.sendBeacon) return; // disabled: nothing is sent
    var payload = {
      event: name,
      path: location.pathname,
      day: new Date().toISOString().slice(0, 10)
    };
    if (extra && extra.target) payload.target = String(extra.target).slice(0, 200);
    try { navigator.sendBeacon(endpoint, new Blob([JSON.stringify(payload)], { type: "application/json" })); } catch (e) { /* fail silently */ }
  }

  window.AffilTrack = { send: send, enabled: !!endpoint };

  var page = document.body && document.body.getAttribute("data-page");
  if (page === "product") send("product_view");
  else if (page === "guide") send("guide_view");
  else if (page === "feed") send("feed_open");
  send("page_view");

  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a[data-outbound], a[data-event]") : null;
    if (!a) return;
    if (a.hasAttribute("data-outbound")) send("outbound_click", { target: a.getAttribute("data-outbound") });
    else send(a.getAttribute("data-event"));
  }, true);
})();
