## What this changes

Finishes the T-13..T-20 scope claimed in `COORDINATION.md`: verified specifications, a front page that
leads with products, four new guides, a review workflow on the Suggestions page, and a stricter gate.

### Verified from the official listings (dated 2026-11-20)

| Field | Product | Value | Source |
|---|---|---|---|
| Weight | P-01 Chefman 6 Qt | 13.3 lb | https://www.amazon.com/dp/B0CDY277D3 |
| Temperature range | P-02 Emeril 26 QT | 75–500 °F | https://www.amazon.com/dp/B09B7SB46R |
| Power | P-02 Emeril 26 QT | 120 V, 1700 W | https://www.amazon.com/dp/B09B7SB46R |
| Model | P-02 Emeril 26 QT | 4-00675-02X-VN | https://www.amazon.com/dp/B09B7SB46R |
| Accuracy | P-05 CHEF iQ Sense | ±1 °F | https://www.amazon.com/dp/B0DZFD6R9Z |
| Commission table | category rate | Kitchen 4.50% (website), 1.25% (Onsite, different program) | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ · https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA |
| Food temperatures | guide content | USDA FSIS chart | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart |

### Flags opened or closed this pass

- **FLG-036** — editorial copy cited four flag numbers that had been reassigned; repointed, and the gate
  now fails on any flag reference that does not resolve.
- **FLG-037** — three weight figures (26.5 lb, "around 13 pounds", 12.8 lb) had no source and are removed.
  Only 13.3 lb is printed anywhere, and the gate fails on any other weight.
- **FLG-038** — P-03 was previously "corrected" to 1000 W. Both 1000 W and 1700 W are on the listing, so
  both are printed as a conflict rather than one being chosen.
- **FLG-039** — the previous executive summary described SG-17..SG-20 and Q-15/Q-16 that did not exist.
  Those IDs now exist; the summary is regenerated from what ships.
- **FLG-040** — several fields looked absent because the fetched text hid the spec panel. Filled where the
  panel was readable; what is still missing stays blank (P-04 upper temperature, for example).
- **FLG-028** — updated: S24 was added, so only S07 remains missing.

Still open and unchanged: FLG-001 (intended ASIN), FLG-002 (tracking ID live?), FLG-003 (short-link
format — **unresolved, not "invalid"**), FLG-004 (one-link test), FLG-011 (unstable redirects), FLG-012
(P-04 link returned a checkpoint page every time).

### Also in here

- Front page rebuilt: products first, dashboards only in one footer group. A gate rule now fails if a
  dashboard link appears in the page body.
- Four new guides: `quarts-vs-litres`, `counter-depth`, `wattage-and-circuits`, `usda-temperature-chart`
  (12 total, all in the sitemap and the feed).
- Suggestions page: approve / defer / reject per row with a live tally and CSV exports, rank arrows,
  reset buttons, and a decision form. 22 proposals, all reviewable before anything is implemented.
- Questions page: 20 questions, each with how to discover the missing fact.
- `EXECUTIVE-SUMMARY.md` and `executive-summary.html` regenerated to match what ships.

### Verification

`python3 scripts/build_site.py` then `python3 scripts/check_site.py` → **33 pages, 5 products, 40 flags,
19 sources, ALL CHECKS PASS**. CI regenerates and diffs the committed pages, so a drift between
generator and output fails the build.

### Irregularities flagged for manual review

1. P-03 lists 1000 W in About this item and 1700 W in the Product Description (FLG-038).
2. P-01 says 6 quarts in the title and 6 liters in the capacity field (FLG-034).
3. P-05 says 50 hours of battery in one section and 70+ hours in another (FLG-008).
4. The site shows no price or star rating, because Program Policies 2(b)/6(t) require Amazon-served
   links or API data for that — no API access exists (FLG-007).
