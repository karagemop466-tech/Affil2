# Executive Summary — ShopNow Kitchen (Affil2)

Date: 2026-11-20 · Tracking ID supplied: shopnow047c-20 (UNVERIFIED, FLG-002)

## What was built
A static, GitHub Pages buyer-guide site for 5 submitted links: 3 air fryers (P-01–P-03) and 2 meat thermometers (P-04–P-05). Every figure traces to an official Amazon listing; every outbound link is marked sponsored; disclosure appears above the fold and in the footer.

## Observed destinations (kept separate from intended ASINs)
- P-01: https://link.amazon/B04G1MEwY → B0CDY277D3 · CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black · amazon.com/dp/B0CDY277D3
- P-02: https://link.amazon/B02NbDxp3 → B09B7SB46R · Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included · amazon.com/dp/B09B7SB46R
- P-03: https://link.amazon/B00hJ57DV → B08DKYBTPH · Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel · amazon.com/dp/B08DKYBTPH
- P-04: https://link.amazon/B0c8moW59 → NOT CONFIRMED (FLG-012) · ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy | NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black · amazon.com/dp/B0DHZTCNR5
- P-05: https://link.amazon/B0f3GKalj → B0DZFD6R9Z · CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3 · amazon.com/dp/B0DZFD6R9Z

## Checked 2026-11-20
- Four short links resolved to the observed ASINs; P-04's short link (B0c8moW59) returned a checkpoint page and is unconfirmed (FLG-012).
- Corrections: P-03 power 1000 W (FLG-017); P-05 warranty two-year (FLG-019); titles now exact listing text (FLG-020).
- Disclosure checked against Operating Agreement §5 (S01); sponsored links per Google (S04); endorsement per FTC (S03).

## Measurement
- Five first-party events: `page_view`, `outbound_click`, `guide_read`, `search`, `suggestion_rank`.
- The reader-visible click counter stays in the reader's own browser (localStorage) and never leaves the device.
- A self-hosted collector now ships in the repository: `functions/api/collect.js` (Cloudflare Pages Function) and `analytics/server.js` (dependency-free Node server). No cookies, no IP address, no user agent, no fingerprint; a search is recorded as a length and a result count, never as the words typed.
- GitHub Pages cannot run a server-side function, so no collector is deployed and the live site records nothing server-side. The browser client probes once and stays inert when nothing answers (FLG-033, Q-08).
- The campaign ledger stays empty until an authorised Associates report fills it. No conversion score and no revenue forecast are published.

## Compliance in the publish path
- `scripts/check_site.py` is the publishing gate: disclosure on every page above the fold, `(paid link)` label, `rel="sponsored"` on every Amazon link, the Associates tracking tag on every Amazon **product** link, no prices, no star ratings, no review counts, no Amazon-hosted imagery, canonical and description on every page, internal links resolve, sitemap covers every page, intent and observation fields stay separate.
- `.github/workflows/pages.yml` now runs the generator, fails if the committed pages differ from the generator, runs the gate, runs the collector tests and runs the site tests — and only deploys if all of it passes.

## Not verified (blank, flagged)
- Intended ASINs (FLG-001); tracking-ID activity (FLG-002); short-link compliance (FLG-003); Special Link test (FLG-004).
- Prices, ratings, sales ranks, commissions (FLG-005).
- Conflicts: P-02 24 vs 25 presets (FLG-021); P-03 temperature (FLG-018); P-05 battery 50 h (FLG-008); P-02 model (FLG-009).

## Next
Owner decisions in questions.html; one Special Link test per product before scaling; deploy a collector and choose its retention policy (FLG-033, Q-08); see flagged.html for all irregularities.
