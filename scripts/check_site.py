#!/usr/bin/env python3
"""Compliance + integrity gate for ShopNow Kitchen.

Fails on: missing/late disclosure, unmarked outbound links, price-like values,
broken internal links/assets, sitemap or feed gaps, missing intent/link-test
register fields. Run: python3 scripts/check_site.py
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(root.rglob("*.html"))
errors = []

for p in pages:
    t = p.read_text()
    rel = str(p.relative_to(root))

    # 1. Disclosure present AND above the fold (before <main)
    if "As an Amazon Associate I earn from qualifying purchases" not in t:
        errors.append(f"{rel}: missing disclosure")
    mi = t.find("<main")
    di = t.find("As an Amazon Associate I earn from qualifying purchases")
    if mi != -1 and di != -1 and di > mi:
        errors.append(f"{rel}: disclosure not above the fold (appears after <main>)")

    # 2. Brand fonts + canonical (findability)
    if "fonts.googleapis.com" not in t:
        errors.append(f"{rel}: missing brand font link")
    if 'rel="canonical"' not in t:
        errors.append(f"{rel}: missing canonical")

    # 3. Outbound Amazon links must carry sponsored + (paid link)
    for m in re.finditer(r'href="(https://www\.amazon\.com[^"]*)"([^>]*)>([^<]*)', t):
        if "sponsored" not in m.group(2):
            errors.append(f"{rel}: amazon link without sponsored: {m.group(1)}")
    for m in re.finditer(r'data-outbound="[^"]*"', t):
        seg = t[max(0, m.start() - 400): m.end() + 400]
        if "(paid link)" not in seg:
            errors.append(f"{rel}: data-outbound link without nearby (paid link) label")

    # 4. No prices / star ratings (Program Policies §2(b))
    if re.search(r'\$\s?\d', t):
        errors.append(f"{rel}: contains price-like $ amount")
    if re.search(r'\d\.\d\s?out of\s?5 stars', t):
        errors.append(f"{rel}: contains star rating")

    # 5. Internal links + assets resolve
    for m in re.finditer(r'href="([^"#]+?\.html)(#[^"]*)?"', t):
        if m.group(1).startswith("http"):
            continue
        target = (p.parent / m.group(1)).resolve()
        if not target.exists():
            errors.append(f"{rel}: broken link {m.group(1)}")
    for m in re.finditer(r'(?:src|href)="((?:\.\./)?assets/[^"]+)"', t):
        target = (p.parent / m.group(1)).resolve()
        if not target.exists():
            errors.append(f"{rel}: missing asset {m.group(1)}")

# 6. Sitemap covers every page
sm = (root / "sitemap.xml").read_text()
for p in pages:
    if str(p.relative_to(root)) not in sm:
        errors.append(f"sitemap missing {p.relative_to(root)}")

# 7. RSS feed covers every guide
feed = (root / "feed.xml").read_text()
for g in sorted((root / "guides").glob("*.html")):
    if g.name not in feed:
        errors.append(f"feed.xml missing guides/{g.name}")
if "<language>en-us</language>" not in feed:
    errors.append("feed.xml: malformed <language> tag")

# 8. Product pages: intent fields separate + link-test status + no merged fields
for p in (root / "products").glob("*.html"):
    t = p.read_text()
    if "Intended ASIN" not in t or "Observed redirect target" not in t:
        errors.append(f"{p.name}: intent fields missing")
    if "PENDING" not in t:
        errors.append(f"{p.name}: test status missing")

# 9. Data registers carry the separate-field rule
import json
products = json.load(open(root / "data" / "products.json"))
for rec in products:
    for field in ("intended_asin", "observed_redirect_target", "official_listing_url",
                  "confirmation_date", "confirmation_source", "link_test"):
        if field not in rec:
            errors.append(f"products.json {rec.get('id')}: missing field {field}")
    if rec.get("intended_asin") and rec["intended_asin"] == rec.get("observed_redirect_target"):
        errors.append(f"products.json {rec['id']}: intended ASIN must never equal observed (fields merged)")

# 10. Analytics layer: five defined events in app.js
appjs = (root / "assets" / "app.js").read_text()
for ev in ("page_view", "outbound_click", "guide_read", "search", "suggestion_rank"):
    if f"'{ev}'" not in appjs and f'"{ev}"' not in appjs:
        errors.append(f"app.js: event {ev} not instrumented")

print(f"checked {len(pages)} pages")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("ALL CHECKS PASS")
