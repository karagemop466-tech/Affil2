// ShopNow Kitchen — site configuration (edit here, not in page code).
window.SITE_CONFIG = {
  // Self-hosted analytics endpoint (privacy-preserving, no cookies, no IP storage).
  // Leave null while the endpoint is not deployed (FLG-010 / Q-08); events then stay
  // in the visitor's own browser (localStorage) and can be exported as CSV.
  // To turn measurement on: deploy analytics/server.py (see analytics/README.md) and set:
  //   analyticsEndpoint: "https://analytics.example.org/v1/events",
  analyticsEndpoint: null,

  // Reader capture (email) endpoint — none connected yet (Q-09 / SG-30).
  // Set to a provider URL (e.g. Buttondown/Mailchimp form action) to enable email capture.
  readerCaptureEndpoint: null
};
