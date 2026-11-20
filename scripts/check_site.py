#!/usr/bin/env python3
"""Compliance + integrity gate. Fails on: missing disclosure, unmarked outbound, prices, broken internal links, sitemap gaps."""
import json, pathlib, re, sys
root=pathlib.Path(__file__).resolve().parent.parent
pages=sorted(root.rglob("*.html"))
errors=[]
for p in pages:
    t=p.read_text()
    rel=str(p.relative_to(root))
    if "As an Amazon Associate I earn from qualifying purchases" not in t: errors.append(f"{rel}: missing disclosure")
    if "(paid link)" not in t: errors.append(f"{rel}: missing (paid link) label")
    # outbound amazon links must have sponsored
    for m in re.finditer(r'href="(https://www\.amazon\.com[^"]*)"([^>]*)>', t):
        if "sponsored" not in m.group(2): errors.append(f"{rel}: amazon link without sponsored: {m.group(1)}")
    # every link to an Amazon PRODUCT page carries the Associates tracking tag
    for m in re.finditer(r'href="(https://www\.amazon\.com/(?:dp|gp/product)/[A-Z0-9]{10}[^"]*)"', t):
        if "tag=shopnow047c-20" not in m.group(1):
            errors.append(f"{rel}: amazon product link without the Associates tag: {m.group(1)}")
    # the supplied short links are Amazon product links too, so they carry rel=sponsored
    for m in re.finditer(r'<a href="(https://link\.amazon/[^"]*)"([^>]*)>', t):
        if "sponsored" not in m.group(2):
            errors.append(f"{rel}: link.amazon link without sponsored: {m.group(1)}")
    # no Amazon-hosted imagery (Program Policies: use your own or licensed images)
    for host in ("m.media-amazon.com", "images-na.ssl-images-amazon.com", "ssl-images-amazon.com"):
        if host in t: errors.append(f"{rel}: references Amazon-hosted imagery ({host})")
    # page metadata
    if 'rel="canonical"' not in t: errors.append(f"{rel}: no canonical link")
    if 'name="description"' not in t: errors.append(f"{rel}: no meta description")
    # the collector client is loaded on every page
    if "assets/js/collect.js" not in t: errors.append(f"{rel}: collector client not loaded")
    # broader rating / review-count patterns
    if re.search(r"\b\d(?:\.\d)?\s*(?:out of 5|/5|stars)\b", t, re.I):
        errors.append(f"{rel}: contains a star rating")
    if re.search(r"\b\d{1,3},\d{3}\s+(?:ratings|reviews)\b", t, re.I):
        errors.append(f"{rel}: contains a review count")
    # no prices: dollar amounts (allow none)
    if re.search(r'\$\s?\d', t): errors.append(f"{rel}: contains price-like $ amount")
    if re.search(r'\d\.\d\s?out of\s?5 stars', t): errors.append(f"{rel}: contains star rating")
    # internal links
    for m in re.finditer(r'href="([^"#]+?\.html)(#[^"]*)?"', t):
        if m.group(1).startswith("http"): continue
        target=(p.parent/m.group(1)).resolve()
        if not target.exists(): errors.append(f"{rel}: broken link {m.group(1)}")
    for m in re.finditer(r'(?:src|href)="(assets/[^"]+)"', t):
        if not (root/m.group(1)).exists(): errors.append(f"{rel}: missing asset {m.group(1)}")
# sitemap covers all pages
sm=(root/"sitemap.xml").read_text()
for p in pages:
    if str(p.relative_to(root)) not in sm: errors.append(f"sitemap missing {p.relative_to(root)}")
# intent fields separate on product pages
for p in (root/"products").glob("*.html"):
    t=p.read_text()
    if "Intended ASIN" not in t or "Observed redirect target" not in t: errors.append(f"{p.name}: intent fields missing")
    if "PENDING" not in t: errors.append(f"{p.name}: test status missing")
# XML well-formedness for feed and sitemap
import xml.dom.minidom as _mx
for x in ["feed.xml", "sitemap.xml"]:
    try:
        _mx.parse(str(root / x))
    except Exception as ex:
        errors.append(f"{x}: not well-formed XML ({ex})")
# stale values: allowed only when the surrounding text marks them as a correction/conflict
STALE = [
    (r"Verified 2026", None),
    (r"Last verified", None),
    (r"4-00675-02X-VN", None),
    (r"HT07", None),
    (r"CQ60", None),
    (r"26\.5 ?lb", None),
    (r"70 ?hours?", None),
    (r"\b572\s?°F", None),
    (r"4\.75", None),
    (r"\[2025 Model\]", None),
    (r"Chefman TurboFry Touch", None),
]
ALLOW = re.compile(r"record title|record ['’“\"]|quoted|register|corrected|correction|conflict|FLG-|not confirmed|unverified|blank|previously|not found|said|listed", re.I)
for p in pages:
    t = p.read_text(); rel = str(p.relative_to(root))
    if rel.startswith("products/p03"):
        for m in re.finditer(r"1700 ?W", t):
            if not ALLOW.search(t[max(0, m.start() - 160): m.end() + 160]):
                errors.append(f"{rel}: P-03 shows 1700 W outside a correction note")
    for pat, _ in STALE:
        for m in re.finditer(pat, t):
            ctx = t[max(0, m.start() - 160): m.end() + 160]
            if not ALLOW.search(ctx):
                errors.append(f"{rel}: stale value {m.group(0)!r}")
# the measurement layer must exist and the schema must match the collector
for required in ("functions/api/collect.js", "analytics/server.js", "assets/js/collect.js",
                 "data/events.json", "measurement.html"):
    if not (root/required).exists(): errors.append(f"missing measurement file: {required}")
if (root/"data/events.json").exists() and (root/"functions/api/collect.js").exists():
    schema=json.loads((root/"data/events.json").read_text())
    declared=[e["name"] for e in schema["events"]]
    collector=(root/"functions/api/collect.js").read_text()
    for name in declared:
        if f'"{name}"' not in collector:
            errors.append(f"event {name} is declared in data/events.json but not accepted by the collector")
    if "measurement.html" not in (root/"sitemap.xml").read_text():
        errors.append("sitemap missing measurement.html")
print(f"checked {len(pages)} pages")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("ALL CHECKS PASS")
