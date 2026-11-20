#!/usr/bin/env python3
"""
Build gate for ShopNow Kitchen. Fails the build if a page breaks a rule that is not
negotiable: disclosure present and above the fold, every Amazon link marked sponsored,
no reproduced prices or ratings, no broken internal links or assets, every page in the
sitemap and every sitemap entry real, feed consistent, structured data parseable, and
the product pages still carrying their separate intended/observed fields.

Run: python3 scripts/check_site.py
Exit 0 = pass, exit 1 = fail with a list of problems.
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://karagemop466-tech.github.io/Affil2/"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases"

errors = []
notes = []


def err(msg):
    errors.append(msg)


def slug_page(prod):
    return f"products/{prod['slug']}.html"


def alt_ok(tag):
    m = re.search(r'alt="([^"]*)"', tag)
    return bool(m and m.group(1).strip())


class TableColumnChecker(HTMLParser):
    def __init__(self, rel):
        super().__init__()
        self.rel = rel
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        if tag == "table":
            self.stack.append({"thead_cols": None, "section": None, "row_cols": 0, "row_idx": 0})
        elif self.stack:
            cur = self.stack[-1]
            if tag in ("thead", "tbody"):
                cur["section"] = tag
            elif tag == "tr":
                cur["row_cols"] = 0
                cur["row_idx"] += 1
            elif tag in ("th", "td"):
                try:
                    span = max(1, int(attr_map.get("colspan", "1")))
                except ValueError:
                    span = 1
                cur["row_cols"] += span

    def handle_endtag(self, tag):
        if not self.stack:
            return
        cur = self.stack[-1]
        if tag == "tr":
            if cur["section"] == "thead":
                cur["thead_cols"] = cur["row_cols"]
            elif cur["section"] == "tbody" and cur["thead_cols"] is not None:
                if cur["row_cols"] != cur["thead_cols"]:
                    err(f"{self.rel}: table row {cur['row_idx']} has {cur['row_cols']} cell(s), "
                        f"expected {cur['thead_cols']} matching thead")
        elif tag in ("thead", "tbody"):
            cur["section"] = None
        elif tag == "table":
            self.stack.pop()


pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
page_rels = [str(p.relative_to(ROOT)) for p in pages]

# ---------------------------------------------------------------- per-page checks
for p in pages:
    rel = str(p.relative_to(ROOT))
    html = p.read_text(encoding="utf-8")
    depth = rel.count("/")
    up = "../" * depth

    if not html.lstrip().startswith("<!DOCTYPE html>"):
        err(f"{rel}: missing doctype")
    if lang := re.search(r'<html lang="([^"]+)"', html):
        if lang.group(1) != "en":
            err(f"{rel}: html lang is {lang.group(1)}, expected en")
    else:
        err(f"{rel}: missing html lang attribute")

    # --- required head furniture
    for tag, label in ((r'<meta charset="utf-8">', "charset"),
                       (r'<meta name="viewport"', "viewport"),
                       (r'<title>[^<]{10,}</title>', "title"),
                       (r'<meta name="description" content="[^"]{40,}"', "meta description"),
                       (r'<link rel="canonical" href="https://karagemop466-tech\.github\.io/Affil2/'
                        r'[^"]*">', "canonical")):
        if not re.search(tag, html):
            err(f"{rel}: missing or invalid {label}")

    # canonical must point at this page
    can = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if can and can.group(1) != BASE + rel:
        err(f"{rel}: canonical {can.group(1)} does not match {BASE + rel}")

    # --- disclosure: must appear twice (above the fold + footer) and before <main>
    count = html.count(DISCLOSURE)
    if count < 2:
        err(f"{rel}: disclosure appears {count} time(s), expected 2 (strip + footer)")
    first_main = html.find("<main")
    first_disc = html.find(DISCLOSURE)
    if first_disc == -1 or first_disc > first_main:
        err(f"{rel}: disclosure is not above the fold (appears after <main>)")

    # --- every amazon.com link must be sponsored + nofollow
    for m in re.finditer(r"<a\b[^>]*href=\"(https://www\.amazon\.com[^\"]*)\"[^>]*>", html):
        tag = m.group(0)
        if "sponsored" not in tag:
            err(f"{rel}: amazon link without rel=sponsored — {m.group(1)[:70]}")
        if "nofollow" not in tag:
            err(f"{rel}: amazon link without rel=nofollow — {m.group(1)[:70]}")

    # --- tagged links must carry the Associate ID
    for m in re.finditer(r'href="(https://www\.amazon\.com/dp/[^"]*)"[^>]*data-outbound', html):
        if "tag=shopnow047c-20" not in m.group(1):
            err(f"{rel}: outbound product link missing the Associates tag — {m.group(1)[:70]}")

    # --- no reproduced prices or ratings
    for m in re.finditer(r"\$\s?\d", html):
        err(f"{rel}: contains a price-like amount near ...{html[max(0, m.start()-40):m.start()+12]!r}")
    if re.search(r"\d\.\d\s*(out of\s*)?5\s*stars", html, re.I):
        err(f"{rel}: contains a star rating")
    if re.search(r"\b(1[0-9]|[1-9]),(?:[0-9]{3})\s*(ratings|reviews|global ratings)", html, re.I):
        err(f"{rel}: contains a review count")

    # --- internal links resolve
    for m in re.finditer(r'href="([^"#:]+?\.(?:html|xml|txt))(?:\?[^"]*)?(?:#[^"]*)?"', html):
        target = (p.parent / m.group(1)).resolve()
        if not target.exists():
            err(f"{rel}: broken internal link -> {m.group(1)}")
    for m in re.finditer(r'(?:src|href)="((?:\.\./)*assets/[^"]+)"', html):
        target = (p.parent / m.group(1)).resolve()
        if not target.exists():
            err(f"{rel}: missing asset -> {m.group(1)}")

    # --- absolute internal links are a smell (host mistakes)
    for m in re.finditer(r'href="(https://karagemop466-tech\.github\.io/Affil2/[^"]+\.html)"', html):
        if not re.search(r'rel="canonical"|property="og:url"|application/ld\+json', html):
            notes.append(f"{rel}: absolute internal link {m.group(1)}")
    if re.search(r'href="/[a-z]', html):
        err(f"{rel}: root-relative link (breaks under a Pages subpath)")

    # --- navigation must be present and consistent
    for label in ("Air Fryers", "Meat Thermometers", "Guides", "Compare"):
        if f">{label}</a>" not in html:
            err(f"{rel}: primary navigation missing '{label}'")
    # --- every page reachable dashboard link group in the footer
    for target in ("suggestions.html", "design-brief.html", "questions.html", "flagged.html",
                   "sources.html", "platform.html", "measurement.html", "executive-summary.html",
                   "campaign-ledger.html", "disclosure.html", "about.html",
                   "sitemap.xml", "feed.xml"):
        if (up + target) not in html:
            err(f"{rel}: footer missing link to {target}")

    # --- og:url matches canonical
    og_url = re.search(r'<meta property="og:url" content="([^"]+)">', html)
    if not og_url or og_url.group(1) != BASE + rel:
        err(f"{rel}: og:url missing or does not match {BASE + rel}")

    # --- table thead/tbody column symmetry
    TableColumnChecker(rel).feed(html)

    # --- unverified leaked prose check (26.5 lb was absent from B09B7SB46R)
    if re.search(r"\b26\.5\s*(?:lb|pound)", html, re.I):
        err(f"{rel}: contains unverified '26.5 lb/pounds' claim absent from live listing")

    # --- images: every generated photo must be captioned as illustration, never as the product
    for m in re.finditer(r'<img\b[^>]*src="((?:\.\./)*assets/photos/[^"]+)"[^>]*>', html):
        asset = (p.parent / m.group(1)).resolve()
        if not asset.exists():
            err(f"{rel}: missing image {m.group(1)}")
        if "assets/photos/" in m.group(1):
            window = html[m.end():m.end() + 900]
            if "Illustrative image, generated for this site" not in window:
                err(f"{rel}: generated photo {m.group(1)} is not captioned as illustration")
        tag = m.group(0)
        if "alt=\"\"" in tag or "alt=" not in tag:
            err(f"{rel}: image {m.group(1)} has no alt text")
        if not re.search(r'width="\d+" height="\d+"', tag):
            err(f"{rel}: image {m.group(1)} has no intrinsic dimensions")
    # --- search controls must not serialize query text into a request URL
    for form in re.finditer(r'<form\b[^>]*\brole="search"[^>]*>(.*?)</form>', html, re.S | re.I):
        for input_tag in re.findall(r"<input\b[^>]*>", form.group(1), re.I):
            if re.search(r"\bname=", input_tag):
                err(f"{rel}: search input has a name and could serialize query text into a request URL")

    # --- structured data must parse
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            err(f"{rel}: JSON-LD does not parse ({e})")
            continue
        if "@context" not in obj:
            err(f"{rel}: JSON-LD block has no @context")
    if rel not in ("search.html",):
        if "application/ld+json" not in html:
            err(f"{rel}: no structured data")

    # --- single H1
    h1s = re.findall(r"<h1[ >]", html)
    if len(h1s) != 1:
        err(f"{rel}: {len(h1s)} h1 elements, expected exactly 1")

    # --- no cross-row placeholders: a cell must not point at another row
    for bad in ("see battery row", "see flags row", "n/a, not a capacity appliance",
                "TODO", "TBD"):
        if bad in html:
            err(f"{rel}: placeholder cell text {bad!r}")

    # --- double-escaped entities: an entity written inside escaped copy prints as "&amp;#8212;"
    if re.search(r"&amp;(?:[a-z]{2,8}|#\d{2,5});", html):
        m = re.search(r"&amp;(?:[a-z]{2,8}|#\d{2,5});", html)
        err(f"{rel}: double-escaped entity {m.group(0)!r} would print literally on the page")

    # --- every image carries alt text, intrinsic dimensions and lazy loading
    for tag in re.findall(r"<img\b[^>]*>", html):
        src = re.search(r'src="([^"]+)"', tag)
        if not alt_ok(tag):
            err(f"{rel}: <img> without alt text — {src.group(1) if src else tag[:50]}")
        if not re.search(r'width="\d+"\s+height="\d+"', tag):
            err(f"{rel}: <img> without intrinsic width/height — {src.group(1) if src else tag[:50]}")
        if "loading=" not in tag:
            err(f"{rel}: <img> without loading attribute — {src.group(1) if src else tag[:50]}")

    # --- no placeholder or template debris (outside script bodies, which hold JSON)
    prose = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
    prose = re.sub(r"<style\b.*?</style>", "", prose, flags=re.S)
    for bad in ("{{", "}}", "TODO", "FIXME", "lorem ipsum", "%cardName%", "${"):
        if bad in prose:
            err(f"{rel}: contains template debris {bad!r}")


# ---------------------------------------------------------------- product identity
# A card that says only "Chefman" twice (P-01 and P-03 are both Chefman) tells a shopper nothing.
# Every product must be identified by the distinguishing name in products.json (`short`), and that
# name must be printed on the front page, the shop index and its own product page.
_reg = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
for prod in _reg:
    if not prod.get("short"):
        err(f"products.json {prod['id']}: no distinguishing 'short' name")
        continue
    for page_rel in ("index.html", "shop.html", slug_page(prod)):
        f = ROOT / page_rel
        if not f.exists():
            continue
        if prod["short"] not in f.read_text(encoding="utf-8"):
            err(f"{page_rel}: product {prod['id']} is not identified as '{prod['short']}'")
_shorts = [prod.get("short") for prod in _reg]
if len(set(_shorts)) != len(_shorts):
    err("products.json: distinguishing names are not unique")


# ---------------------------------------------------------------- product pages
prod_pages = sorted((ROOT / "products").glob("*.html"))
if len(prod_pages) != 5:
    err(f"expected 5 product pages, found {len(prod_pages)}")
for p in prod_pages:
    html = p.read_text()
    rel = str(p.relative_to(ROOT))
    for field in ("Intended ASIN", "Observed redirect target", "Special Link we publish",
                  "Confirmation date", "Associates test status"):
        if field not in html:
            err(f"{rel}: product-intent record missing '{field}'")
    if "PENDING" not in html:
        err(f"{rel}: Special Link test status missing")
    if "authorization" in html.lower():
        err(f"{rel}: stray text")
    # each spec row must link to a source
    rows = re.findall(r'<tr><th scope="row">[^<]+</th><td>.*?</td>\s*<td class="src">.*?</td></tr>',
                      html, re.S)
    if len(rows) < 5:
        err(f"{rel}: only {len(rows)} sourced spec rows found")

# ---------------------------------------------------------------- food safety block
usda = json.loads((ROOT / "data" / "usda-temperatures.json").read_text())
src_ids_pre = {x["id"] for x in json.loads((ROOT / "data" / "sources.json").read_text())}
if usda["source_id"] not in src_ids_pre:
    err(f"usda-temperatures.json cites {usda['source_id']}, which is not in sources.json")
for p in prod_pages:
    rel = str(p.relative_to(ROOT))
    html = p.read_text()
    is_thermo = "products/p04-" in rel or "products/p05-" in rel
    has_block = "Safe Minimum Internal Temperature" in html
    if is_thermo and not has_block:
        err(f"{rel}: thermometer page is missing the USDA food-safety block")
    if not is_thermo and has_block:
        err(f"{rel}: food-safety block on a page that is not a thermometer")
    if has_block:
        for food, _ in usda["rows"]:
            if food.split(" —")[0] not in html:
                err(f"{rel}: USDA row missing: {food[:40]}")


# ---------------------------------------------------------------- FAQ claims
# A FAQ may not state a value the register marks as unverified or conflicting without saying so.
reg_by_id = {d["id"]: d for d in json.loads((ROOT / "data" / "products.json").read_text())}
ed_all = json.loads((ROOT / "data" / "editorial.json").read_text())
UNITS = r"(?:°F|°C|watts?|W\b|volts|hours?|quarts?|liters?|inches|in\b|pounds|lb\b|seconds?|probes?)"
for pid, rec in ed_all.items():
    reg = reg_by_id[pid]
    verified_nums = set()
    for key, f in reg["fields"].items():
        if f["v"] and f["st"] == "verified":
            verified_nums.update(re.findall(r"\d+(?:\.\d+)?", f["v"]))
    unver_nums = set()
    for key, f in reg["fields"].items():
        if f["v"] is None or f["st"] in ("unverified", "conflict"):
            # a figure mentioned only as "removed, was 572 F" is still not a confirmed value
            blob = " ".join(str(x) for x in (f["v"] or "", f.get("src", ""), f.get("note", "")))
            unver_nums.update(re.findall(r"\d+(?:\.\d+)?", blob))
    for q, a in rec["faq"]:
        names_conflict = re.search(r"FLG-\d{3}|both|vs\.?|two figures|conflict|against each other",
                                   a, re.I) is not None
        for num in re.findall(r"\d+(?:\.\d+)?", a):
            if num in unver_nums and num not in verified_nums and not names_conflict:
                err(f"editorial.json {pid} FAQ '{q[:40]}': states {num} as fact, but the register "
                    f"marks that value unverified or conflicting and the answer does not say so")
        if re.search(r"\b(is|are|reads|reaches)\s+(?:exactly\s+)?\d+" + UNITS, a) and \
                "flag" not in a.lower() and "blank" not in a.lower() and "not " not in a.lower()[:40]:
            notes.append(f"editorial.json {pid} FAQ states a figure as fact: {q[:40]}")

# ---------------------------------------------------------------- data integrity
raw = json.loads((ROOT / "data" / "products.json").read_text())
editorial = json.loads((ROOT / "data" / "editorial.json").read_text())
flags = json.loads((ROOT / "data" / "flags.json").read_text())
sources = json.loads((ROOT / "data" / "sources.json").read_text())

if len(raw) != 5:
    err(f"products.json holds {len(raw)} products, expected 5")
seen = set()
for d in raw:
    for key in ("id", "slug", "submitted", "token", "observed", "asin", "title", "listing",
                "fields", "cat", "catfile", "questions"):
        if key not in d:
            err(f"products.json {d.get('id','?')}: missing key {key}")
    target = d.get("observed") or d.get("asin")
    if not target:
        err(f"products.json {d['id']}: no observed ASIN recorded")
        continue
    if target in seen:
        err(f"products.json: duplicate observed ASIN {target}")
    seen.add(target)
    if not re.fullmatch(r"B0[A-Z0-9]{8}", target):
        err(f"products.json {d['id']}: observed ASIN {target} is not a valid ASIN shape")
    if target in d["submitted"]:
        err(f"products.json {d['id']}: the submitted short link should not embed the ASIN")
    if "intended" in d and d["intended"]:
        err(f"products.json {d['id']}: intended ASIN must stay blank until the owner confirms it")
    if d["id"] not in editorial:
        err(f"editorial.json missing a record for {d['id']}")
    for key, f in d["fields"].items():
        if not f.get("src"):
            err(f"products.json {d['id']}.{key}: no provenance string")
        if f["v"] is None and f["st"] != "unverified":
            err(f"products.json {d['id']}.{key}: blank value must be marked unverified")
        if re.search(r"\$\s?\d", str(f["v"])):
            err(f"products.json {d['id']}.{key}: contains a price")

flag_ids = {f["id"] for f in flags}
src_ids = {s["id"] for s in sources}
for f in flags:
    if not f["links"]:
        err(f"flags.json {f['id']}: no source link")
    for sid in f["links"]:
        if sid not in src_ids:
            err(f"flags.json {f['id']}: link {sid} is not in sources.json")
    if len(f["detail"]) < 60:
        err(f"flags.json {f['id']}: detail is too thin to be useful")
    if "severity" not in f:
        err(f"flags.json {f['id']}: no severity")
for s in sources:
    if not s["url"].startswith("https://"):
        err(f"sources.json {s['id']}: url is not https")

# every flag referenced in the HTML must exist, and every defined flag must be published
flag_refs = set()
for p in pages:
    flag_refs |= set(re.findall(r"FLG-\d{3}", p.read_text()))
missing = flag_refs - flag_ids
if missing:
    err(f"pages reference undefined flags: {sorted(missing)}")
unused = flag_ids - flag_refs
if unused:
    err(f"flags defined but never published on a page: {sorted(unused)}")

# ---------------------------------------------------------------- sitemap + feed
sm_text = (ROOT / "sitemap.xml").read_text()
try:
    sm = ET.fromstring(sm_text)
except ET.ParseError as e:
    err(f"sitemap.xml does not parse: {e}")
    sm = None
if sm is not None:
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [u.find(ns + "loc").text for u in sm.findall(ns + "url")]
    for rel in page_rels:
        if BASE + rel not in locs:
            err(f"sitemap.xml is missing {rel}")
    for loc in locs:
        if not loc.startswith(BASE):
            err(f"sitemap.xml: {loc} is outside the canonical host")
            continue
        target = ROOT / loc[len(BASE):]
        if not target.exists():
            err(f"sitemap.xml lists a page that does not exist: {loc}")
    dups = {x for x in locs if locs.count(x) > 1}
    if dups:
        err(f"sitemap.xml: duplicate entries {sorted(dups)}")

feed_text = (ROOT / "feed.xml").read_text()
try:
    feed = ET.fromstring(feed_text)
except ET.ParseError as e:
    err(f"feed.xml does not parse: {e}")
    feed = None
if feed is not None:
    items = feed.findall("./channel/item")
    if len(items) < 9:
        err(f"feed.xml has {len(items)} items, expected at least 9 guides")
    for it in items:
        link = it.find("link").text
        if not link.startswith(BASE):
            err(f"feed.xml item outside canonical host: {link}")
            continue
        if not (ROOT / link[len(BASE):]).exists():
            err(f"feed.xml item points at a missing page: {link}")
    lang = feed.find("./channel/language")
    if lang is None or not lang.text or not lang.text.startswith("en"):
        err("feed.xml: missing or malformed <language>")

robots = (ROOT / "robots.txt").read_text()
if "Sitemap: " + BASE + "sitemap.xml" not in robots:
    err("robots.txt does not point at the canonical sitemap")
if "Disallow: /" in robots:
    err("robots.txt blocks the site")

# ---------------------------------------------------------------- weight accuracy & unverified claim guard
# Only weights verified in data/products.json (e.g. Measurements table P-01 13.3 lb, P-03 12.8 lb)
# may appear outside flagged.html/sources.html; unverified weights (e.g. 26.5 lb on P-02) fail.
verified_weights = set()
for prod in json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8")):
    w_field = (prod.get("fields") or {}).get("weight") or {}
    if w_field.get("st") == "verified" and w_field.get("v"):
        for num in re.findall(r"\b\d+(?:\.\d+)?\b", w_field["v"]):
            verified_weights.add(num)

WEIGHT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s?(?:lb|lbs|pounds?)\b", re.I)
WEIGHT_EXEMPT = {"flagged.html", "sources.html"}
for f in pages:
    rel = f.name if f.parent == ROOT else f"{f.parent.name}/{f.name}"
    if rel in WEIGHT_EXEMPT:
        continue
    txt = re.sub(r"<[^>]+>", " ", f.read_text())
    for m in WEIGHT_RE.finditer(txt):
        if m.group(1) not in verified_weights:
            err(f"{rel}: quotes an unverified product weight ({m.group(0).strip()}) not verified in data/products.json (FLG-022/FLG-039)")
    if re.search(r"\b(?:footprint and weight|weight and footprint|weigh(?:s|ing) \w+ ?(?:lb|pounds))", txt, re.I):
        err(f"{rel}: promises unverified weight information (FLG-022)")

# ---------------------------------------------------------------- compare pair view
comp = (ROOT / "compare.html").read_text()
pm = re.search(r'<script type="application/json" id="pairData">(.*?)</script>', comp, re.S)
if not pm:
    err("compare.html: no embedded pair view data")
else:
    try:
        pair = json.loads(pm.group(1))
    except json.JSONDecodeError as e:
        err(f"compare.html pair data does not parse: {e}")
        pair = {}
    if len(pair) != 5:
        err(f"compare.html pair data holds {len(pair)} products, expected 5")
    for pid, rec in pair.items():
        if not (ROOT / rec["url"]).exists():
            err(f"compare.html pair data links a missing page: {rec['url']}")
        if "tag=shopnow047c-20" not in rec["buy"]:
            err(f"compare.html pair data buy link for {pid} lacks the Associates tag")
        if len(rec["rows"]) < 12:
            err(f"compare.html pair data for {pid} has only {len(rec['rows'])} rows")
# ---------------------------------------------------------------- analytics switch is real
# assets/config.js documents window.SITE_CONFIG.analyticsEndpoint as the way to turn measurement
# on, and assets/app.js reads it. It shipped unloaded by any page (FLG-049), so check both ends.
for p in pages:
    rel_p = str(p.relative_to(ROOT))
    up_p = "../" * rel_p.count("/")
    h = p.read_text(encoding="utf-8")
    if f'src="{up_p}assets/config.js"' not in h:
        err(f"{rel_p}: assets/config.js is not loaded; window.SITE_CONFIG would be undefined")
    if h.find(f'src="{up_p}assets/config.js"') > h.find(f'src="{up_p}assets/app.js"'):
        err(f"{rel_p}: config.js is loaded after app.js and would be read too late")
_app = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
if "SITE_CONFIG" not in _app or "analyticsEndpoint" not in _app:
    err("assets/app.js: does not read window.SITE_CONFIG.analyticsEndpoint")

# ---------------------------------------------------------------- search privacy
app_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
if re.search(r"URLSearchParams\(\s*location\.search", app_js) or ".get('q')" in app_js or '.get("q")' in app_js:
    err("assets/app.js: reads search text from the request URL; built-in search must use session storage")
if "sn_search_query" not in app_js or "sessionStorage" not in app_js:
    err("assets/app.js: session-storage handoff for built-in search is missing")
if "session storage" not in (ROOT / "disclosure.html").read_text(encoding="utf-8").lower():
    err("disclosure.html: search query handling is not explained in the privacy statement")

# ---------------------------------------------------------------- search index
search_html = (ROOT / "search.html").read_text()
if re.search(r"nothing is sent to\s+a server", search_html, re.I):
    err("search.html: claims nothing is sent to a server, but page requests reach the host; use the session-storage wording")
m = re.search(r'<script type="application/json" id="searchIndex">(.*?)</script>',
              search_html, re.S)
if not m:
    err("search.html: no embedded search index")
else:
    try:
        idx = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        err(f"search.html index does not parse: {e}")
        idx = []
    for entry in idx:
        target = ROOT / entry["u"]
        if not target.exists():
            err(f"search.html index points at missing page {entry['u']}")
    if len(idx) < 20:
        err(f"search.html index has only {len(idx)} entries")

# ---------------------------------------------------------------- editorial & illustrations & telemetry
ed_text = (ROOT / "data" / "editorial.json").read_text(encoding="utf-8")
if re.search(r"\b26\.5\s*(?:lb|pound)", ed_text, re.I):
    err("data/editorial.json contains unverified '26.5 lb/pounds'")
ed_flags = set(re.findall(r"FLG-\d{3}", ed_text))
if ed_flags - flag_ids:
    err(f"data/editorial.json cites undefined flags: {sorted(ed_flags - flag_ids)}")

all_html_text = "\n".join(p.read_text(encoding="utf-8") for p in pages)
svg_files = sorted((ROOT / "assets" / "illustrations").glob("*.svg"))
if not svg_files:
    err("assets/illustrations/: expected editorial SVG files")
for svg in svg_files:
    try:
        ET.fromstring(svg.read_text(encoding="utf-8"))
    except ET.ParseError as e:
        err(f"{svg.relative_to(ROOT)} does not parse as XML: {e}")
    if f"assets/illustrations/{svg.name}" not in all_html_text:
        err(f"{svg.relative_to(ROOT)} is orphaned (not referenced in any generated HTML page)")

events_data = json.loads((ROOT / "data" / "events.json").read_text(encoding="utf-8"))
expected_events = {"page_view", "outbound_click", "guide_read", "search", "suggestion_rank"}
if set(events_data.get("events", {}).keys()) != expected_events:
    err("data/events.json must define the exact five measurement events")
app_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
for token in ("function send(", "exportEvents", "searchIndex", ".navtoggle",
              "page_view", "outbound_click", "guide_read", "suggestion_rank"):
    if token not in app_js:
        err(f"assets/app.js missing required capability: {token}")

# ---------------------------------------------------------------- report
print(f"checked {len(pages)} pages, {len(prod_pages)} product records, "
      f"{len(flags)} flags, {len(sources)} sources")
if notes:
    print("\nnotes (not failures):")
    for n in notes:
        print("  -", n)
if errors:
    print(f"\n{len(errors)} PROBLEM(S):")
    for e in errors:
        print("  ✗", e)
    sys.exit(1)
print("ALL CHECKS PASS")


# ---------------------------------------------------------------- analytics surface (session bba2deed)
app = (ROOT / "assets" / "app.js").read_text()
for ev in ("page_view", "outbound_click", "guide_read", "search", "suggestion_rank"):
    if ev not in app:
        err(f"assets/app.js: defined event {ev!r} missing")
if not (ROOT / "analytics" / "server.py").exists():
    err("analytics/server.py missing (self-hosted endpoint, SG-18)")
if "analyticsEndpoint" not in (ROOT / "assets" / "config.js").read_text():
    err("assets/config.js: analyticsEndpoint switch missing")
vt = (ROOT / "verification.html").read_text()
if "Verification Log" not in vt:
    err("verification.html: content missing")
for tm in re.finditer(r"<tbody>(.*?)</tbody>", vt, re.S):
    for rm in re.finditer(r"<tr>.*?</tr>", tm.group(1), re.S):
        if "<th" in rm.group(0) and "href=" not in rm.group(0) and 'scope="row"' in rm.group(0):
            err("verification.html: register row without source link")
