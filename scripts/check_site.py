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

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://karagemop466-tech.github.io/Affil2/"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases"

errors = []
notes = []


def err(msg):
    errors.append(msg)


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
    for target in ("suggestions.html", "questions.html", "flagged.html", "sources.html",
                   "executive-summary.html", "campaign-ledger.html", "disclosure.html",
                   "about.html", "sitemap.xml", "feed.xml"):
        if (up + target) not in html:
            err(f"{rel}: footer missing link to {target}")

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

    # --- no placeholder or template debris (outside script bodies, which hold JSON)
    prose = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
    prose = re.sub(r"<style\b.*?</style>", "", prose, flags=re.S)
    for bad in ("{{", "}}", "TODO", "FIXME", "lorem ipsum", "%cardName%", "${"):
        if bad in prose:
            err(f"{rel}: contains template debris {bad!r}")


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
    if len(items) < 8:
        err(f"feed.xml has {len(items)} items, expected at least 8 guides")
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

# ---------------------------------------------------------------- search index
search_html = (ROOT / "search.html").read_text()
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
    if len(idx) < 15:
        err(f"search.html index has only {len(idx)} entries")

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
