# Draft queue

This directory holds **inert drafts**, produced by `scripts/draft_guide.py`. Nothing here is a page.

* A file is `<slug>.json` with `status: "unapproved"` until a named reviewer approves it.
* Approval requires the compliance lint to pass: no price, no rating, no review count, no figure
  that `data/products.json` does not mark verified (or that the USDA chart does not carry), no
  claim without a source register ID, and the two honesty sentences this site insists on
  (nobody here tested these products; the links are affiliate links).
* Even an approved draft is **not published by the tool**. Publication means a human moving the
  record into a guide module (`scripts/traffic_guides.py` or `scripts/seasonal_guides.py`) and the
  build gate passing in CI. That is deliberate: the brief asks for automation *and* a compliance
  gate, and the only honest shape is a drafter that cannot open the gate.

Files must stay JSON. The build gate treats every `.html` file in the repository as a submitted
page, so a draft written as HTML would enter the sitemap by accident.
