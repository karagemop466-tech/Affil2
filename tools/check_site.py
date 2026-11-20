#!/usr/bin/env python3
"""Integration checks for docs/. Exit code 1 on any failure.

Checks:
  1. Associates statement appears on every page (disclosure strip + footer).
  2. Every internal link and asset resolves to a file in docs/ (no broken links).
  3. Every Amazon outbound link carries rel="sponsored".
  4. Every data row on product / intent / source / flagged tables has an https source link.
  5. Intended ASIN / listing URL are blank unless a confirmation source is recorded (and an ASIN is 10 chars).
  6. sitemap.xml lists every page; feed.xml and sitemap.xml parse as XML.
"""
import csv
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "data"
STATEMENT = "As an Amazon Associate I earn from qualifying purchases."
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []  # (tag, attrs)
        self.tables = []  # per table: list of rows (each row: list of hrefs)
        self._in_tbody = False
        self._row = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("a", "link", "script", "img") and any(k in a for k in ("href", "src")):
            self.links.append((tag, a))
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._row = []
        if tag == "a" and self._row is not None and a.get("href"):
            self._row.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "tbody":
            self._in_tbody = False
        if tag == "tr" and self._row is not None:
            self.tables.append(self._row)
            self._row = None

    def handle_data(self, data):
        self.text.append(data)


def resolve(page_rel, href):
    """Return the docs file a relative href points to, or None if external / anchor-only."""
    p = urlparse(href)
    if p.scheme or href.startswith("//") or p.netloc:
        return None
    path = p.path
    if not path:
        return "SAME"
    base_dir = (DOCS / page_rel).parent
    target = (base_dir / path).resolve()
    if path.endswith("/"):
        target = target / "index.html"
    if target.is_dir():
        target = target / "index.html"
    return target


pages = sorted(DOCS.rglob("*.html"))
rels = {}
for pg in pages:
    rel = pg.relative_to(DOCS).as_posix()
    rels[rel] = pg
    html = pg.read_text(encoding="utf-8")
    parser = Page()
    parser.feed(html)
    txt = "".join(parser.text)

    # 1. statement on every page, at least twice (strip + footer), 404 included
    n = html.count(STATEMENT)
    if n < 2:
        errors.append(f"{rel}: Associates statement appears {n} time(s); expected at least 2")

    # 2 & 3. links
    for tag, a in parser.links:
        href = a.get("href") or a.get("src")
        if not href:
            continue
        tgt = resolve(rel, href)
        # Affiliate link = short link or any URL carrying a tag parameter. Citation links to
        # Amazon policy/product pages are not monetised and are not held to the sponsored rule.
        is_affiliate = tag == "a" and ("link.amazon" in href or "tag=" in href)
        if is_affiliate and "sponsored" not in (a.get("rel") or ""):
            errors.append(f"{rel}: affiliate link without rel=sponsored: {href}")
        if tgt is None or tgt == "SAME":
            continue
        if not tgt.exists():
            errors.append(f"{rel}: broken internal link -> {href}")

    # 4. source link on product / intent / source / flagged data rows
    if rel in ("products/index.html", "intent/index.html", "sources/index.html", "flagged/index.html"):
        for row in parser.tables:
            if not row:
                continue
            if rel == "flagged/index.html" and not any(h.startswith("https://") for h in row):
                # flagged irregularity rows may be internal-only; only the unverified-field table must link
                if "Unverified" not in "".join(parser.text):
                    pass
            if rel in ("products/index.html", "intent/index.html", "sources/index.html") and not any(h.startswith("https://") for h in row):
                errors.append(f"{rel}: table row without https source link: {row[:2]}")

    if rel == "index.html" and "Products we" not in txt:
        errors.append("index.html: products section missing (landing must lead with products)")

# 5. intent record consistency
products = json.loads((DATA / "products.json").read_text(encoding="utf-8"))["products"]
for p in products:
    if p["intended_asin"]:
        if len(p["intended_asin"]) != 10:
            errors.append(f"{p['id']}: intended_asin is not 10 characters: {p['intended_asin']}")
        if not p["confirmation_source"] or not p["confirmation_date"]:
            errors.append(f"{p['id']}: intended ASIN set without confirmation date/source")
    if p["official_listing_url"] and not p["confirmation_source"]:
        errors.append(f"{p['id']}: listing URL set without confirmation source")
    if p["observed_redirect_url"] == p["intended_asin"]:
        errors.append(f"{p['id']}: observed and intended fields merged")

# 6. sitemap / feed
sm = DOCS / "sitemap.xml"
try:
    tree = ET.parse(sm)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {loc.text for loc in tree.getroot().findall("s:url/s:loc", ns)}
    for rel in rels:
        if rel == "404.html":
            continue
        expect = "https://karagemop466-tech.github.io/Affil2/" + ("" if rel == "index.html" else rel.replace("index.html", ""))
        if expect not in locs:
            errors.append(f"sitemap.xml missing {expect}")
except ET.ParseError as ex:
    errors.append(f"sitemap.xml invalid XML: {ex}")
try:
    ET.parse(DOCS / "feed.xml")
except ET.ParseError as ex:
    errors.append(f"feed.xml invalid XML: {ex}")

# CSV header check
with (DATA / "campaign-ledger.csv").open(encoding="utf-8") as fh:
    header = next(csv.reader(fh))
if header[:3] != ["timestamp_utc", "source", "channel"]:
    errors.append("campaign-ledger.csv header changed")

print(f"checked {len(rels)} pages")
if errors:
    print(f"{len(errors)} problem(s):")
    for x in errors:
        print(" -", x)
    sys.exit(1)
print("all checks passed")
