#!/usr/bin/env python3
"""Compliance + integrity gate (extended in the T-15 integration pass).

Fails on: missing disclosure, unmarked outbound links, price-like values, broken
internal links, sitemap gaps, malformed feed, missing JSON-LD, register-table rows
without a source link, missing SG-27..SG-30 rows, missing analytics surface, or
images without alt text. Run: python3 scripts/check_site.py
"""
import pathlib
import re
import sys
import xml.dom.minidom

root = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(root.rglob("*.html"))
errors = []

def err(msg):
    errors.append(msg)

# ---------- per-page checks ----------
for p in pages:
    t = p.read_text()
    rel = str(p.relative_to(root))
    if "As an Amazon Associate I earn from qualifying purchases" not in t:
        err(f"{rel}: missing disclosure")
    if "(paid link)" not in t:
        err(f"{rel}: missing (paid link) label")
    for m in re.finditer(r'href="(https://www\.amazon\.com[^"]*)"([^>]*)>', t):
        if "sponsored" not in m.group(2):
            err(f"{rel}: amazon link without sponsored: {m.group(1)}")
    if re.search(r'\$\s?\d', t):
        err(f"{rel}: contains price-like $ amount")
    if re.search(r'\d\.\d\s?out of\s?5 stars', t):
        err(f"{rel}: contains star rating")
    for m in re.finditer(r'href="([^"#]+?\.html)(#[^"]*)?"', t):
        if m.group(1).startswith("http"):
            continue
        target = (p.parent / m.group(1)).resolve()
        if not target.exists():
            err(f"{rel}: broken link {m.group(1)}")
    for m in re.finditer(r'(?:src|href)="(assets/[^"]+)"', t):
        if not (root / m.group(1)).exists():
            err(f"{rel}: missing asset {m.group(1)}")
    # images must carry alt text (publication polish gate)
    for m in re.finditer(r"<img\b[^>]*>", t):
        if "alt=" not in m.group(0):
            err(f"{rel}: <img> without alt: {m.group(0)[:60]}")

# ---------- findability: sitemap + feed + JSON-LD ----------
sm = (root / "sitemap.xml").read_text()
for p in pages:
    if str(p.relative_to(root)) not in sm:
        err(f"sitemap missing {p.relative_to(root)}")
for g in sorted((root / "guides").glob("*.html")):
    if g.name not in (root / "feed.xml").read_text():
        err(f"feed.xml missing guides/{g.name}")
try:
    xml.dom.minidom.parse(str(root / "feed.xml"))
except Exception as e:
    err(f"feed.xml is not well-formed XML: {e}")
if 'application/ld+json' not in (root / "index.html").read_text():
    err("index.html: missing JSON-LD")
for g in (root / "guides").glob("*.html"):
    if "application/ld+json" not in g.read_text():
        err(f"guides/{g.name}: missing JSON-LD")

# ---------- analytics surface ----------
app = (root / "assets" / "app.js").read_text()
for ev in ("page_view", "outbound_click", "guide_read", "search", "suggestion_rank"):
    if ev not in app:
        err(f"assets/app.js: defined event '{ev}' missing")
if not (root / "analytics" / "server.py").exists():
    err("analytics/server.py missing (self-hosted endpoint)")
if "analyticsEndpoint" not in (root / "assets" / "config.js").read_text():
    err("assets/config.js: analyticsEndpoint switch missing")

# ---------- registers ----------
sug = (root / "suggestions.html").read_text()
for sg in ("SG-27", "SG-28", "SG-29", "SG-30"):
    if sg not in sug:
        err(f"suggestions.html: parallel-pass row {sg} missing")
if not (root / "verification.html").exists():
    err("verification.html missing")

# register / data tables: every <tbody> row must carry a source link
def rows_without_source(fn):
    t = (root / fn).read_text()
    for tm in re.finditer(r"<table>.*?</table>", t, re.S):
        table = tm.group(0)
        body = table.split("</thead>")[-1]
        for rm in re.finditer(r"<tr>.*?</tr>", body, re.S):
            row = rm.group(0)
            if "<th" in row or not row.strip():
                continue
            if 'href=' not in row:
                err(f"{fn}: register row without source link: {row[:70]}")

for fn in ("verification.html", "sources.html"):
    rows_without_source(fn)
for p in (root / "products").glob("*.html"):
    rows_without_source("products/" + p.name)

# compare table: each product column header must carry its source listing link
cmp_t = (root / "compare.html").read_text()
if cmp_t.count("source listing") < 5:
    err("compare.html: fewer than 5 per-product source links in header")

# index at-a-glance table rows must carry official listing links
idx = (root / "index.html").read_text()
if idx.count("amazon.com/dp/") < 10:
    err("index.html: at-a-glance rows missing official listing links")

# product-intent fields stay separate
for p in (root / "products").glob("*.html"):
    t = p.read_text()
    if "Intended ASIN" not in t or "Observed redirect target" not in t:
        err(f"{p.name}: intent fields missing")
    if "PENDING" not in t:
        err(f"{p.name}: test status missing")

print(f"checked {len(pages)} pages")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("ALL CHECKS PASS")
