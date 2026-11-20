/* Shared JS for ShopNow Reviews.
   Two small jobs: (1) privacy-preserving event counters, (2) nothing else.
   No cookies, no fingerprinting, no third-party requests except the configured endpoint. */
(function () {
  'use strict';

  var CFG = window.SHOPNOW_CONFIG || {};
  var ENDPOINT = CFG.analyticsEndpoint || '';
  var DNT = navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.msDoNotTrack === '1';

  function bucketViewport() {
    var w = window.innerWidth || 0;
    if (w < 500) return 'xs';
    if (w < 800) return 's';
    if (w < 1100) return 'm';
    return 'l';
  }

  function send(eventName, payload) {
    if (DNT) return;
    var body = JSON.stringify(Object.assign({
      event: eventName,
      path: location.pathname,
      ts: new Date().toISOString(),
      viewport: bucketViewport(),
      ref: document.referrer ? new URL(document.referrer).hostname : ''
    }, payload || {}));

    try {
      if (ENDPOINT && navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: 'application/json' }));
        return;
      }
      if (ENDPOINT && window.fetch) {
        fetch(ENDPOINT, { method: 'POST', body: body, headers: { 'Content-Type': 'application/json' }, keepalive: true });
        return;
      }
    } catch (e) { /* measurement must never break the page */ }

    // Static-hosting fallback: hold in a local ring buffer for the nightly collector.
    try {
      var q = JSON.parse(localStorage.getItem('shopnow_queue') || '[]');
      q.push(body);
      localStorage.setItem('shopnow_queue', JSON.stringify(q.slice(-50)));
    } catch (e2) { /* private mode — drop silently */ }
  }

  window.shopnowTrack = send;

  // The five defined events. Everything else is deliberately not captured.
  var EVENTS = ['page_view', 'product_click', 'guide_read', 'signup_submit', 'disclosure_view'];

  // 1. page_view (one per load)
  send('page_view');

  // 2. disclosure_view — fired when the disclosure strip has been on screen
  var strip = document.querySelector('[data-disclosure]');
  if (strip && 'IntersectionObserver' in window) {
    var seen = false;
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !seen) {
          seen = true;
          send('disclosure_view', { slot: strip.getAttribute('data-disclosure') });
        }
      });
    }, { threshold: 0.5 }).observe(strip);
  }

  // 3. product_click — every sponsored outbound link carries data-asin
  document.addEventListener('click', function (ev) {
    var link = ev.target.closest ? ev.target.closest('a[data-asin]') : null;
    if (!link) return;
    send('product_click', {
      asin: link.getAttribute('data-asin'),
      placement: link.getAttribute('data-placement') || 'unknown',
      destination: link.hostname
    });
  }, { passive: true });

  // 4. guide_read — a guide counts as read at 66% scroll depth
  var article = document.querySelector('[data-guide]');
  if (article && 'IntersectionObserver' in window) {
    var fired = false;
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !fired) {
          fired = true;
          send('guide_read', { slug: article.getAttribute('data-guide') });
        }
      });
    }, { threshold: 0 }, {}).observe(article.querySelector('[data-guide-end]') || article);
  }

  // 5. signup_submit — capture form is a gate until a capture provider is configured
  document.querySelectorAll('form[data-capture]').forEach(function (form) {
    form.addEventListener('submit', function (ev) {
      var providerReady = form.getAttribute('data-provider-ready') === 'true';
      if (!providerReady) {
        ev.preventDefault();
        var msg = form.querySelector('[data-capture-msg]');
        if (msg) {
          msg.textContent = 'Not live yet: no email provider is connected, so this form has nowhere to send your address. It is deliberately disabled rather than silently failing.';
          msg.hidden = false;
        }
        send('signup_submit', { state: 'blocked_no_provider' });
        return;
      }
      send('signup_submit', { state: 'sent' });
    });
  });

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  if (window.console && CFG.debug) {
    console.log('[shopnow] events tracked:', EVENTS.join(', '), 'endpoint:', ENDPOINT || '(none configured)');
  }
})();
