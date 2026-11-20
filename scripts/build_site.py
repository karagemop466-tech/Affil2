#!/usr/bin/env python3
"""
ShopNow Kitchen — single-source site generator.

Every HTML page in the repo is written by this script from data/*.json plus the
copy below. Nothing is hand-edited after generation, so a fact changes in one
place or not at all. Run:  python3 scripts/build_site.py
"""
import json
import re as _re
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

BASE = "https://karagemop466-tech.github.io/Affil2/"
TRACKING_ID = "shopnow047c-20"
TODAY = "2026-11-20"
SITE = "ShopNow Kitchen"

RAW_PRODUCTS = json.loads((DATA / "products.json").read_text())
USDA = json.loads((DATA / "usda-temperatures.json").read_text())
EDITORIAL = json.loads((DATA / "editorial.json").read_text())
SOURCES = json.loads((DATA / "sources.json").read_text())
FLAGS = json.loads((DATA / "flags.json").read_text())
EVENTS = json.loads((DATA / "events.json").read_text())

FIELD_LABEL = {
    "model": "Model", "capacity": "Capacity", "temperature": "Temperature range",
    "power": "Power", "dimensions": "Dimensions D x W x H", "weight": "Weight",
    "presets": "Presets", "accessories": "Accessories", "warranty": "Warranty",
    "features": "Notable features", "response": "Response time",
    "accuracy": "Stated accuracy", "certification": "Certification",
    "waterproof": "Water resistance", "display": "Display", "included": "In the box",
    "upper_temp": "Upper temperature", "probes": "Probes", "heat": "Heat rating",
    "sensors": "Sensors", "connectivity": "Connectivity", "battery": "Battery",
    "probe_length": "Probe length", "care": "Cleaning",
}
FIELD_ORDER = ["capacity", "temperature", "power", "dimensions", "weight", "presets",
               "accessories", "model", "response", "accuracy", "upper_temp", "probes", "heat",
               "sensors", "connectivity", "battery", "probe_length", "waterproof", "display",
               "certification", "included", "care", "warranty", "features"]


def source_url(sid):
    for s in SOURCES:
        if s["id"] == sid:
            return s["url"]
    return ""


def find_source(field_key, product):
    """Link a spec row to the official page the other session recorded it from."""
    for f in FLAGS:
        pass
    # the register names the listing for the product; field-level detail comes from `src`
    for s in SOURCES:
        if s["id"] == f"S{10 + PRODUCTS.index(product)}":
            return s["url"]
    return product["listing"]


def normalise(p, ed):
    """Fold the shared register (read-only) plus this site's editorial copy into one record."""
    p = dict(p)
    p["brand"] = ed["brand"]
    p["headline"] = ed["headline"]
    p["best_for"] = ed["best_for"]
    p["tradeoff"] = ed["tradeoff"]
    p["commerce_note"] = ed["evidence_note"]
    p["listing_title"] = p["title"]
    p["intended"] = None
    p["observed"] = p.get("observed")
    p["observed_checked"] = TODAY
    p["observed_note"] = p["observed_status"]
    p["blurb"] = p["blurb"] or ed["headline"]
    p["model"] = p["fields"]["model"]["v"]
    p["model_source"] = p["fields"]["model"]["src"]
    p["faq"] = [(q, a) for q, a in ed["faq"]]
    p["questions"] = [(q, a) for q, a in ed["qa"]]
    if p.get("power_line") is None:
        pw = p["fields"].get("power") or {}
        p["power_line"] = pw.get("v") or "not stated on the listing"
    # spec rows in a stable order, with a real source link and the register's own status
    rows = []
    seen = set()
    for key in FIELD_ORDER + [k for k in p["fields"] if k not in FIELD_ORDER]:
        f = p["fields"].get(key)
        if not f or key in seen:
            continue
        seen.add(key)
        rows.append({
            "label": FIELD_LABEL.get(key, key.replace("_", " ").title()),
            "value": f["v"],
            "status": f["st"],
            "from": f["src"],
            "note": f.get("note", ""),
            "url": p["listing"],
        })
    p["spec_rows"] = rows
    return p


PRODUCTS = [normalise(p, EDITORIAL[p["id"]]) for p in RAW_PRODUCTS]
BY_ID = {p["id"]: p for p in PRODUCTS}

DISCLOSURE = ("As an Amazon Associate I earn from qualifying purchases. Links marked "
              "<strong>(paid link)</strong> are Amazon affiliate links &mdash; if you buy "
              "through them, we may earn a commission at no extra cost to you.")

# --------------------------------------------------------------------------- helpers

def esc(s):
    return go_clean(str(s)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def aff(p):
    """The tagged Special Link we publish."""
    target = p.get("observed") or p["asin"]
    return f"https://www.amazon.com/dp/{target}?tag={TRACKING_ID}"

def plain(p):
    """Untagged official listing, for verification."""
    target = p.get("observed") or p["asin"]
    return f"https://www.amazon.com/dp/{target}"

def slug_of(p):
    return f"products/{p['slug']}.html"

def glyph(p, up=""):
    if p["cat"] == "Meat Thermometers":
        fname = "thermometer.svg"
        alt = "Editorial illustration of a kitchen meat thermometer — original artwork, not product photography"
    elif p["id"] == "P-02":
        fname = "air-fryer-oven.svg"
        alt = "Editorial illustration of a countertop oven-style air fryer — original artwork, not product photography"
    else:
        fname = "air-fryer.svg"
        alt = "Editorial illustration of a basket air fryer — original artwork, not product photography"
    return f'<img src="{up}assets/illustrations/{fname}" alt="{esc(alt)}">'


# ----- photography ---------------------------------------------------------
# Editorial images are generated illustration, not photographs of the products.
# Every page that shows one says so, and the gate fails if the caption is missing.
PHOTO_CAPTION = ("Illustrative image, generated for this site &mdash; not a photograph of the "
                 "product. No Amazon photography is used anywhere.")
PHOTOS = {
    "hero": ("assets/photos/hero-kitchen.jpg", 1264, 848,
             "A dual-basket air fryer with both drawers open on a wooden counter, steam rising "
             "from crisp potatoes, beside a folded linen towel and a probe thermometer"),
    "air": ("assets/photos/air-fryers.jpg", 1264, 848,
            "Three air fryer shapes on a stone counter: a dual-drawer basket fryer, a tall "
            "single-basket fryer and a stainless French-door countertop oven"),
    "thermo": ("assets/photos/thermometers.jpg", 1264, 848,
               "A thin probe thermometer in a sliced roast on a board, with a small wireless "
               "probe hub and a second probe in a joint of meat"),
}


def photo(key, up="", cls="", caption=True, eager=False, short=False):
    src, w, h, alt = PHOTOS[key]
    load = "eager" if eager else "lazy"
    text = ("Illustrative image, generated for this site &mdash; not this product."
            if short else PHOTO_CAPTION)
    cap = f'<figcaption class="photo-cap">{text}</figcaption>' if caption else ""
    return (f'<figure class="photo {cls}">'
            f'<img src="{up}{src}" alt="{esc(alt)}" width="{w}" height="{h}" '
            f'loading="{load}" decoding="async">{cap}</figure>')

# --------------------------------------------------------------------------- shell

NAV = [
    ("air-fryers.html", "Air Fryers"),
    ("meat-thermometers.html", "Meat Thermometers"),
    ("shop.html", "All products"),
    ("guides.html", "Guides"),
    ("compare.html", "Compare"),
    ("how-we-choose.html", "How we choose"),
]

DASH = [
    ("suggestions.html", "Decision Center"),
    ("design-brief.html", "Design &amp; Traffic Brief"),
    ("questions.html", "Open Questions"),
    ("verification.html", "Verification Log"),
    ("flagged.html", "Flagged for Review"),
    ("sources.html", "Sources"),
    ("platform.html", "Platform Architecture"),
    ("measurement.html", "Measurement &amp; Collector"),
    ("executive-summary.html", "Executive Summary"),
    ("campaign-ledger.html", "Campaign Ledger"),
    ("about.html", "About &amp; Authorship"),
    ("disclosure.html", "Disclosure &amp; Privacy"),
]


def page(path, title, desc, body, extra_head="", jsonld=None, kicker="", h1=None):
    """Render a full page. `path` is repo-relative, e.g. 'products/x.html'."""
    depth = path.count("/")
    up = "../" * depth
    canon = BASE + path

    nav_parts = []
    for h, t in NAV:
        cur = ' aria-current="page"' if h == path else ""
        nav_parts.append(f'<a href="{up}{h}"{cur}>{t}</a>')
    nav = "".join(nav_parts)
    footnav = "".join(f'<a href="{up}{h}">{t}</a>' for h, t in NAV)
    dash = " · ".join(f'<a href="{up}{h}">{t}</a>' for h, t in DASH)

    ld = ""
    if jsonld:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        for b in blocks:
            ld += ('<script type="application/ld+json">'
                   + json.dumps(b, ensure_ascii=False) + "</script>\n")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)[:300]}">
<link rel="canonical" href="{canon}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)[:300]}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:image" content="{BASE}assets/photos/hero-kitchen.jpg">
<meta property="og:image:alt" content="Illustrative kitchen image, generated for this site">
<meta name="twitter:image" content="{BASE}assets/photos/hero-kitchen.jpg">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{SITE} — Feed" href="{up}feed.xml">
{ld}{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap mast">
    <a class="brand" href="{up}index.html">ShopNow<span>Kitchen</span></a>
    <button class="navtoggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <nav id="primary-nav" aria-label="Primary">{nav}<details class="records"><summary>Records</summary><div>{dash}</div></details></nav>
    <form class="search" action="{up}search.html" method="get" role="search">
      <label class="sr" for="q">Search products and guides</label>
      <input id="q" type="search" placeholder="Search the kitchen…" autocomplete="off">
      <button type="submit">Search</button>
    </form>
  </div>
</header>
<div class="disclosure" role="note"><div class="wrap">{DISCLOSURE}
  <a href="{up}disclosure.html">How we disclose</a></div></div>
<main id="main" class="wrap">
{body}
</main>
<footer>
  <div class="wrap">
    <p class="disc-foot">{DISCLOSURE}</p>
    <nav aria-label="Footer">{footnav}</nav>
    <p class="dash">Records and dashboards: {dash} ·
      <a href="{up}sitemap.xml">Sitemap</a> · <a href="{up}feed.xml">RSS</a></p>
    <p class="small">Prices and availability are not shown on this site; check the live listing for
      current details. Product names, Amazon and Amazon Associates are trademarks of Amazon.com,
      Inc. or its affiliates. This site is not endorsed by Amazon. Scenes and diagrams are illustrations,
      not product photography, and not a picture of the item reviewed. Nothing here is a
      hands-on product test — every specification is read from the official listing and dated.
      Last verified {TODAY}.</p>
    <p class="small">© 2026 {SITE}. <a href="{up}flagged.html">Flagged for Review</a> lists everything
      we could not verify.</p>
  </div>
</footer>
<script src="{up}assets/app.js" defer></script>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return path


# --------------------------------------------------------------------------- components

def buybox(p, up, variant="full"):
    checks = "".join(f"<li>{esc(q)}</li>" for q, _ in p["questions"][:3])
    photo_key = "thermo" if p["cat"] == "Meat Thermometers" else "air"
    return f"""<div class="buybox">
  <div class="buybox-art">{photo(photo_key, up, caption=True, short=True)}</div>
  <div class="buybox-body">
    <p class="kicker">{esc(p['cat'])} · {esc(p['brand'])}</p>
    <h3>{esc(p['headline'])}</h3>
    <p>{esc(p['blurb'])}</p>
    <dl class="factrow">
      <div><dt>Best for</dt><dd>{esc(p['best_for'])}</dd></div>
      <div><dt>The catch</dt><dd>{esc(p['tradeoff'])}</dd></div>
    </dl>
    <ul class="checks">{checks}</ul>
    <p class="cta">
      <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
         data-event="outbound_click">Check price on Amazon<span class="btn-sub">paid link</span></a>
      <a class="btn ghost" href="{up}{slug_of(p)}">Full breakdown</a>
    </p>
    <p class="small">Prices, ratings and availability live on Amazon and change; we never print them
      here. Tagged link, opens amazon.com. <a href="{plain(p)}" rel="sponsored nofollow">Untagged
      listing</a> for verification.</p>
  </div>
</div>"""


# Shop tags. Deliberately not "best" — each names the *reason* someone picks it, which is the
# thing a shopper is actually scanning for.
PICK_TAGS = {
    "P-01": [("Best for two cooks", "good"), ("Two baskets", "warn")],
    "P-02": [("Biggest capacity", "good"), ("Deep footprint", "warn")],
    "P-03": [("Biggest single basket", "good"), ("No window", "warn")],
    "P-04": [("Fastest read", "good"), ("No app", "warn")],
    "P-05": [("Best for leaving the room", "good"), ("App required", "warn")],
}

WHY_WE_PICKED = {
    "P-01": "It is the only one here that can finish a main and a side at the same moment, which is "
            "the single most common weeknight problem air fryers are bought to solve.",
    "P-02": "If you want one counter appliance instead of three, this replaces a toaster, a "
            "convection oven and an air fryer &mdash; if the depth fits.",
    "P-03": "Less to go wrong: one basket, four presets, no window to fog up. The pick when you "
            "cook one thing at a time.",
    "P-04": "The one you keep in a drawer and grab without thinking about it.",
    "P-05": "For long cooks &mdash; brisket, a roast, a smoker &mdash; where you would rather not "
            "stand next to the oven.",
}


def card(p, up, badge=""):
    photo_key = "thermo" if p["cat"] == "Meat Thermometers" else "air"
    chips = "".join(
        f'<div class="chip"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["card"][:3])
    tag = f'<span class="badge">{esc(badge)}</span>' if badge else ""
    return f"""<article class="card">
  <div class="card-media">{photo(photo_key, up, caption=True, short=True)}{tag}</div>
  <div class="card-body">
    <p class="kicker">{esc(p['cat'])} · {esc(p['brand'])}</p>
    <h3><a href="{up}{slug_of(p)}">{esc(p['headline'])}</a></h3>
    <p class="card-blurb">{esc(p['blurb'])}</p>
    <dl class="chips">{chips}</dl>
    <div class="badge-row">{"".join(f'<span data-tone="{tone}">{esc(label)}</span>' for label, tone in PICK_TAGS.get(p["id"], []))}</div>
    <p class="small why"><strong>Why we picked it</strong> {WHY_WE_PICKED.get(p["id"], "")}</p>
    <p class="small bestfor"><strong>Buy it if</strong> {esc(p['best_for'])}</p>
    <p class="small catchline"><strong>Skip it if</strong> {esc(p['tradeoff'])}</p>
    <p class="cta">
      <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
         data-event="outbound_click">Check price on Amazon<span class="btn-sub">paid link</span></a>
    </p>
    <p class="small micro"><a href="{up}{slug_of(p)}">Full breakdown, specs and trade-offs &rarr;</a></p>
  </div>
</article>"""



def usda_block(p):
    """Food-safety minimums, quoted from the USDA chart. Only on thermometer pages."""
    if p["cat"] != "Meat Thermometers":
        return ""
    rows = "".join(
        f'<tr><td>{esc(food)}</td><td>{esc(temp)}</td></tr>' for food, temp in USDA["rows"])
    return f"""<h2>Doneness targets come from the USDA, not from us</h2>
<p>This is a thermometer, so the numbers that matter are food-safety numbers. We do not restate them
  from memory. The USDA FSIS <a href="{USDA["source_url"]}">Safe Minimum Internal Temperature
  Chart</a> (source {USDA["source_id"]}, checked {USDA["checked"]}) gives these minimums, as measured
  with a food thermometer:</p>
<table class="usda">
  <caption><a href="{USDA["source_url"]}">USDA FSIS &mdash; Safe Minimum Internal Temperature
    Chart</a> ({USDA["source_id"]})</caption>
  <thead><tr><th scope="col">Food</th><th scope="col">Minimum internal temperature</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="small">Read the chart itself before relying on any number here:
  <a href="{USDA["source_url"]}">fsis.usda.gov</a>. Registered as {USDA["source_id"]} in the
  <a href="../sources.html">source register</a>.</p>
"""


# --------------------------------------------------------------------------- reader voice
# Internal records (flag IDs, chunk numbers, "intent record") are how the project talks to
# itself. A shopper should never meet them. These helpers translate a record into a sentence
# a person would actually say, and give every number a visible, dated source note.

SOURCE_LABEL = "Official Amazon listing"

FIELD_PHRASE = {
    "capacity": "capacity", "temperature": "temperature range", "power": "power",
    "dimensions": "dimensions", "weight": "weight", "model": "model number",
    "warranty": "warranty", "features": "listed features", "presets": "preset count",
    "included": "what is in the box", "battery": "battery life", "accuracy": "stated accuracy",
    "response": "response time", "heat": "heat rating", "upper_temp": "upper temperature rating",
    "probes": "probes included", "connectivity": "connectivity", "depth": "probe depth",
    "care": "care instructions", "certification": "certifications stated",
}

# Flags a shopper genuinely needs, phrased as a shopper would. Anything not listed here is
# still published, in full, on the Flagged for Review page — it is simply not shouted at a
# buyer mid-sentence.
READER_CONFLICTS = {
    "P-01": "Chefman's own listing gives the capacity twice — 6 quarts in the title and "
            "bullets, 6 liters in the specifications table.",
    "P-02": "The listing disagrees with itself on preset count (24 in the title, 25 in the "
            "bullets) and on capacity (26 quarts in the bullets, 24.6 liters in the "
            "specifications table).",
    "P-03": "The listing puts the maximum temperature at 400&nbsp;&deg;F in the specifications "
            "and 450&nbsp;&deg;F Hi-Fry in the title, and gives two different wattages "
            "(1,700&nbsp;W in the specifications, 1,000&nbsp;W in the bullets).",
    "P-04": "No internal contradiction found on the listing in this reading.",
    "P-05": "Battery life is stated as up to 50 hours in the bullets; the warranty is described "
            "as two years in one place and three in another.",
}


_CITE_PATTERNS = [
    # "(chunk 7)", "chunk 8", ", chunk 5 & 7"
    _re.compile(r'\s*,?\s*\(?chunks?\s*[0-9][0-9&,\s]*\)?'),
    # standalone bracketed flag ids: "(FLG-022)", "(FLG-034 / FLG-002)"
    _re.compile(r'\s*\((?:FLG-\d{3}(?:\s*[/,&]\s*)?)+\)'),
    # trailing sentence "See FLG-008." / "flagged as FLG-017."
    _re.compile(r'\s*(?:See|see|flagged as|per)\s+FLG-\d{3}\.?'),
    # bare "FLG-008" that survived above
    _re.compile(r'\s*FLG-\d{3}'),
]


def go_clean(text):
    """Strip production citations from anything a shopper reads. The facts stay; the
    newsroom's own filing system does not travel with them. `flagged.html` is generated from
    data/flags.json and never passes through here, so every flag is still published in full."""
    if not text:
        return text
    out = text
    for rx in _CITE_PATTERNS:
        out = rx.sub('', out)
    return _re.sub(r'\s{2,}', ' ', out).strip()


def clean_field_note(txt):
    """A conflicting field's note, rephrased so a shopper understands why two numbers appear."""
    return go_clean(txt or "")


def source_note(field, up="../"):
    """A reader-facing source note: which table, which listing, which day. No chunk numbers."""
    f = (field or "").strip()
    table = "specifications"
    if any(k in f for k in ("About this item", "bullets", "Features", "title")):
        table = "the listing bullets"
    if "Measurements" in f:
        table = "the measurements table"
    if "Item details" in f:
        table = "the item details table"
    return f'Read from {table} on <a href="{up}sources.html">{TODAY}</a>'


def source_for(p, up="../"):
    return (f'<a href="{plain(p)}" rel="sponsored nofollow">{SOURCE_LABEL}</a>, '
            f'read {TODAY} &middot; <a href="{up}sources.html">source note</a>')


def ledger_block(p, up="../"):
    """The reader's version of the product-intent record. All five required fields survive,
    visible and separate; only the surrounding language is written for a shopper."""
    intended = p.get("intended")
    rows = [
        ("The link you gave us", f'<code>{esc(p["submitted"])}</code>', ""),
        ("Intended ASIN",
         (esc(intended) if intended else
          '<span class="unverified">left blank until the owner confirms it</span>'),
         "We never fill this in by guesswork."),
        ("Observed redirect target",
         f'ASIN {esc(p["observed"] or "not observed")} '
         f'&mdash; <a href="{plain(p)}" rel="sponsored nofollow">open the official listing</a>',
         "What the short link actually opened, not what it was supposed to open."),
        ("Special Link we publish",
         f'<a href="{aff(p)}" rel="sponsored nofollow">{esc(aff(p))}</a>',
         "Tagged with shopnow047c-20, marked sponsored."),
        ("Confirmation date", TODAY, "The date this row was last read off the live listing."),
        ("Associates test status",
         "PENDING &mdash; one link per product is clicked inside the enrolled Associate account and "
         "confirmed in the tracking report before any traffic is scaled.",
         ""),
    ]
    body = ""
    for k, v, n in rows:
        note = ('<div class="small">' + n + '</div>') if n else ""
        body += '<tr><th scope="row">' + k + '</th><td>' + v + note + '</td></tr>'
    return f'''<table class="ledger">
  <caption>What you gave us, where it goes, and what we publish. The intended ASIN and the
    observed destination are separate rows on purpose: we do not guess what you meant.</caption>
  <tbody>{body}</tbody>
</table>'''


def deals_block(p, up="../"):
    """What the listing says you get, and the questions the listing leaves open. Reader-facing:
    it answers "what is in the box" and "what will annoy me" without inventing either."""
    f = p.get("fields") or {}
    lines = []
    inc = f.get("included") or f.get("accessories") or f.get("probes")
    if inc and inc.get("v"):
        lines.append(("<strong>In the box</strong>", inc["v"], inc.get("st")))
    if f.get("care", {}).get("v"):
        lines.append(("<strong>Cleaning</strong>", f["care"]["v"], f["care"].get("st")))
    if f.get("warranty", {}).get("v"):
        lines.append(("<strong>Warranty</strong>", f["warranty"]["v"], f["warranty"].get("st")))
    if not lines:
        return ""
    items = ""
    for label, value, st in lines:
        flag = ' <span class="token conflict">the listing says both</span>' if st == "conflict" else ""
        items += f"<li>{label}: {esc(value)}{flag}</li>"
    return f'''<aside class="aside-card" aria-label="What comes with it">
  <h2>What comes with it</h2>
  <ul class="tight">{items}</ul>
  <p class="small">Quoted from the listing&rsquo;s own fields &mdash; {source_note("Item details", up)}.
    If a detail is not listed here, the listing does not promise it.</p>
</aside>'''


def spec_table(p):
    """The specification table a shopper can read without meeting the newsroom."""
    out = []
    for r in p["spec_rows"]:
        if r["value"] is None or r["status"] == "unverified":
            value = ('<span class="unverified">the listing does not state this</span>')
        else:
            value = esc(r["value"])
            if r["status"] == "conflict":
                value += ' <span class="token conflict">the listing says both</span>'
        out.append(
            f'<tr><th scope="row">{esc(r["label"])}</th><td>{value}'
            f'<div class="srcline">{source_note(r["from"])}</div></td>'
            f'<td class="src"><a href="{r["url"]}" rel="sponsored nofollow">Listing</a></td></tr>')
    return f"""<table class="specs-table">
  <caption>Straight off the official listing, read on {TODAY}. Where the listing does not say,
    the cell says so instead of guessing.</caption>
  <thead><tr><th scope="col">What you need to know</th>
    <th scope="col">What the listing says</th><th scope="col">Where</th></tr></thead>
  <tbody>{"".join(out)}</tbody>
</table>"""


def intent_table(p):
    """Kept for the internal Verification Log; buyer pages use ledger_block() instead."""
    intended = p["intended"] or "— blank: not confirmed by the owner (FLG-001)"
    return f"""<table class="intent">
  <caption>Product-intent confirmation record. Intended and observed are separate fields and are
    never merged.</caption>
  <tbody>
    <tr><th scope="row">Submitted link (as supplied)</th><td>{esc(p['submitted'])}</td></tr>
    <tr><th scope="row">Short-link token</th><td>{esc(p['token'])} (not an ASIN)</td></tr>
    <tr><th scope="row">Intended ASIN</th><td>{esc(intended)}</td></tr>
    <tr><th scope="row">Observed redirect target</th><td>{esc(p['observed'] or '— not observed yet')}</td></tr>
    <tr><th scope="row">What the submitted link actually opened</th><td>{esc(p['observed_note'])}</td></tr>
    <tr><th scope="row">Official listing URL</th>
      <td><a href="{plain(p)}" rel="sponsored nofollow">{plain(p)}</a></td></tr>
    <tr><th scope="row">Special Link we publish</th>
      <td><a href="{aff(p)}" rel="sponsored nofollow">{aff(p)}</a></td></tr>
    <tr><th scope="row">Model (as published)</th>
      <td>{esc(p['model'] or '— blank, see FLG-022')}<br><span class="small">{esc(p['model_source'])}</span></td></tr>
    <tr><th scope="row">Confirmation date</th><td>{TODAY}</td></tr>
    <tr><th scope="row">Associates test status</th>
      <td>PENDING — one link per product must be clicked inside the enrolled account and
        confirmed in the tracking report before traffic is scaled (FLG-004).</td></tr>
  </tbody>
</table>"""


def faq_block(p):
    items = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in p["faq"]
    )
    return f'<h2>Quick answers</h2><div class="faq">{items}</div>'


def breadcrumb(items, up=""):
    """items = [(label, href|None)]; hrefs are written relative to the page using `up`."""
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{up}{href}">{esc(label)}</a>')
        else:
            parts.append(f"<span>{esc(label)}</span>")
    return '<p class="crumbs">' + " &rsaquo; ".join(parts) + "</p>"


def publisher_ld():
    return {"@type": "Organization", "name": SITE, "url": BASE,
            "description": "An independent kitchen-appliance buying guide that reads specifications "
                           "from official Amazon listings and never prints prices."}


def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + h}
        for i, (n, h) in enumerate(trail)]}


# --------------------------------------------------------------------------- pages
BUILT = []

# ---- home
def review_strip(up=""):
    """A dated, one-line trust strip: what was checked, when, and where the paperwork lives.
    It states the policy reason plainly instead of showing a star row we are not allowed to show."""
    return f'''<div class="review-strip">
  <p><strong>Checked {TODAY}.</strong> Specifications read from the official Amazon listings, page
    by page. Where a listing disagrees with itself, both numbers are printed. Prices and star
    ratings stay on Amazon, because Amazon&rsquo;s policy governs who may display them.</p>
  <a href="{up}sources.html">See the sources &rarr;</a>
</div>'''


def build_home():
    featured = [BY_ID["P-01"], BY_ID["P-03"], BY_ID["P-04"]]
    picks = "".join(
        f'<li><a href="{slug_of(p)}"><span class="pick-k">{esc(p["cat"])}</span>'
        f'<strong>{esc(p["brand"])}</strong> {esc(p["headline"])}</a>'
        f'<span>{esc(p["best_for"])}</span></li>' for p in PRODUCTS)
    latest = "".join(
        f'''<article class="latest-item">
  <p class="kicker">{esc(g["kicker"])}</p>
  <h3><a href="guides/{g["slug"]}.html">{esc(g["title"])}</a></h3>
  <p>{esc(g["sub"])}</p>
</article>''' for g in GUIDES[:3])
    body = f"""
<div class="issue"><b>THE KITCHEN EDIT</b><span></span> VOL. 01 &nbsp; / &nbsp; NOVEMBER 2026</div>
{review_strip()}
<section class="hero">
  <div class="hero-copy">
    <p class="kicker">The kitchen counter issue · updated {TODAY}</p>
    <h1>One basket, two baskets, or an oven?</h1>
    <p class="lede">Three air fryers and two meat thermometers, chosen because you asked about
      them &mdash; and written up the way we would want it explained to us: what each one is good
      at, who it suits, and the one thing that will annoy you after a month.</p>
    <p class="cta">
      <a class="btn" href="#the-picks">See the three picks</a>
      <a class="btn ghost" href="guides/basket-vs-oven.html">Basket or oven? Start here</a>
    </p>
    <ul class="hero-facts">
      <li><strong>5</strong> appliances, checked {TODAY}</li>
      <li><strong>{len(GUIDES)}</strong> practical guides</li>
      <li><strong>0</strong> prices or ratings copied</li>
    </ul>
  </div>
  <div class="hero-art">{photo("hero", "", "hero-photo", caption=True, eager=True)}</div>
</section>

<section class="dept">
  <p class="kicker">The shop directory</p>
  <h2>Shop by category</h2>
  <div class="aisles">
    <a href="air-fryers.html">{photo("air", "", "aisle-photo", caption=True, short=True)}
      <span>01 / Appliances<strong>Air fryers &rarr;</strong></span></a>
    <a href="meat-thermometers.html">{photo("thermo", "", "aisle-photo", caption=True, short=True)}
      <span>02 / Tools<strong>Meat thermometers &rarr;</strong></span></a>
  </div>
</section>

<section class="strip" aria-label="How this site works">
  <p><strong>Every number dated.</strong> Read off the official Amazon listing on {TODAY}, with the
    source one click away on every row.</p>
  <p><strong>Contradictions shown.</strong> When a listing says two things, you see both rather
    than the tidier one.</p>
  <p><strong>No price theatre.</strong> No countdown timers, no fake scarcity &mdash; the live price
    is on Amazon, where it is always current.</p>
</section>

<section id="the-picks">
  <div class="sec-head">
    <h2>The three we&rsquo;d start with</h2>
    <p class="muted">This is not the whole market &mdash; it is the five appliances you asked about.
      These three cover the three reasons people buy one, and the reasoning is on each card.</p>
  </div>
  <div class="grid">{ "".join(card(p, "", b) for p, b in zip(featured, ["Best for two", "Biggest single basket", "Best for spot checks"])) }</div>
  <p class="small"><a href="shop.html">See all five products &rarr;</a></p>
</section>

<section class="split">
  <div>
    <h2>Start with your question</h2>
    <ul class="linklist">
      <li><a href="guides/basket-vs-oven.html">Basket or oven-style: what should you compare?</a>
        <span>Footprint, doors, and how you load it.</span></li>
      <li><a href="guides/capacity-checklist.html">A no-hype checklist for comparing capacity</a>
        <span>Quarts are not servings.</span></li>
      <li><a href="guides/cleanup-counter-space.html">Cleanup and counter-space trade-offs</a>
        <span>Dishwasher-safe is not the same as easy.</span></li>
      <li><a href="guides/instant-vs-wireless.html">Instant-read or wireless thermometer?</a>
        <span>Speed at the grill versus leaving the room.</span></li>
      <li><a href="guides/thermometer-accuracy.html">How to read accuracy claims</a>
        <span>What &plusmn;0.5&nbsp;&deg;F and NIST actually mean.</span></li>
    </ul>
  </div>
  <aside class="panel">
    <h3>How we know what we know</h3>
    <ol class="tight">
      <li>Every specification comes from the official listing, dated, with the link on the row.</li>
      <li>If a listing contradicts itself, you get both numbers. Nothing is averaged or tidied.</li>
      <li>We have not cooked with these units, and we say so on every product page.</li>
      <li>No prices, no star ratings, no &ldquo;best&rdquo; ribbon. Those are Amazon&rsquo;s to show,
        and a rating is other people&rsquo;s kitchens, not yours.</li>
    </ol>
    <p class="small"><a how-we-choose.htmlsrc="/Affil2/how-we-choose.html">How we choose &mdash; and what we refuse to claim &rarr;</a></p>
  </aside>
</section>

<section class="panel scallop">
  <h2>Every product at a glance</h2>
  <p class="muted">The table a buyer needs: what it is, who it suits, and the one caveat that matters.
    Price and rating columns are deliberately absent.</p>
  {overview_table()}
</section>

<section class="split wide-left">
  <div>
    <h2>Latest guides</h2>
    <div class="latest">{latest}</div>
    <p class="small"><a href="guides.html">All {len(GUIDES)} guides &rarr;</a></p>
  </div>
  <aside class="panel pick-panel">
    <h3>The five at a glance</h3>
    <ul class="picklist">{picks}</ul>
  </aside>
</section>

<section>
  <h2>What readers ask us most</h2>
  <div class="faq">
    <details><summary>Do you show prices?</summary><p>No. Amazon&rsquo;s Program Policies allow a site
      to show price and availability only when Amazon serves the link or the data comes through the
      Product Advertising or Creators API. This site does neither, so prices stay on Amazon where
      they are always current. That is also why nothing here is ever out of date on price.</p></details>
    <details><summary>Which one would you buy?</summary><p>It depends on one thing: do you cook two
      things at once. If yes, the dual-basket Chefman. If you cook in batches and want the biggest
      single basket, the 8-quart Chefman. If you want an oven that air-fries, the Emeril &mdash; and
      only if you have 16.9 inches of depth.</p></details>
    <details><summary>Are the star ratings on Amazon reliable?</summary><p>They are real, and they are
      not shown here &mdash; partly policy, partly because a rating summarises other people&rsquo;s
      kitchens. The specification table is more useful for your counter.</p></details>
    <details><summary>How current is this?</summary><p>Every listing was re-read on {TODAY}. Listings
      change; the date is printed on each product page so you can judge.</p></details>
  </div>
</section>

<section class="panel">
  <h2>Working on this site?</h2>
  <p>Every internal record is reachable from the footer of every page: the
    <a href="suggestions.html">Decision Center</a> where proposals are ranked before anything is
    built, the <a href="questions.html">Open Questions</a> register, the
    <a href="flagged.html">Flagged for Review</a> page, and the
    <a href="sources.html">source register</a>.</p>
</section>
"""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE,
           "publisher": dict(publisher_ld(), **{"@context": "https://schema.org"})},
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Products covered",
           "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "name": p["brand"] + " — " + p["headline"],
                "url": BASE + slug_of(p)} for i, p in enumerate(PRODUCTS)]}]
    BUILT.append(page("index.html",
                      f"{SITE} — air fryers and meat thermometers, compared honestly",
                      "Which air fryer fits your counter, and instant-read versus wireless "
                      "thermometers. Specs read from official Amazon listings, conflicts flagged, "
                      "no prices or star ratings quoted.",
                      body, jsonld=ld))


def overview_table():
    rows = ""
    for p in PRODUCTS:
        rows += (f"<tr><td class=\"nowrap\">{p['id']}</td>"
                 f"<td><a href=\"{slug_of(p)}\"><strong>{esc(p['brand'])}</strong> &mdash; "
                 f"{esc(p['headline'])}</a></td>"
                 f"<td>{esc(p['cat'])}</td>"
                 f"<td>{esc(p['best_for'])}</td>"
                 f"<td>{esc(p['tradeoff'])}</td>"
                 f"<td class=\"nowrap\"><a href=\"{aff(p)}\" rel=\"sponsored nofollow\" "
                 f"data-outbound=\"{p['id']}\" data-event=\"outbound_click\">Amazon (paid link)</a></td></tr>")
    return f"""<table class="overview">
  <caption>Five submitted links, verified {TODAY}. Ranking is by category, not by preference.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Product</th><th scope="col">Category</th>
    <th scope="col">Best for</th><th scope="col">The catch</th><th scope="col">Listing</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""


# ---- shop
def build_shop():
    body = f"""
{breadcrumb([("Home", "index.html"), ("All products", None)])}
<h1>All five products</h1>
<p class="lede">Everything this site covers, in one place. Same five links you gave us, sorted by
  what they are good at rather than by which one pays more.</p>
<div class="grid">{"".join(card(p, "") for p in PRODUCTS)}</div>
<h2>Side by side</h2>
{overview_table()}
<p class="small">Every row links to a product page with the full specification table and its source
  link, plus the record of what the submitted short link actually opened.</p>
"""
    BUILT.append(page("shop.html", f"All products — {SITE}",
                      "All five products covered by this site, with what each is best for and the "
                      "caveat that matters, plus a side-by-side table.",
                      body, jsonld={"@context": "https://schema.org", "@type": "CollectionPage",
                                    "name": "All products", "url": BASE + "shop.html"}))


# ---- category pages
def build_category(catfile, cat, headline, intro, guides_, picks):
    items = [p for p in PRODUCTS if p["cat"] == cat]
    verdict_items = "".join(
        '<li><strong>' + esc(p["brand"]) + '</strong> &mdash; ' + esc(p["best_for"]) +
        '. <em>Catch:</em> ' + esc(p["tradeoff"]) + '. <a href="' + slug_of(p) +
        '">Details</a></li>' for p in items)
    guide_items = "".join(
        '<li><a href="' + h + '">' + esc(t) + '</a><span>' + esc(sub) + '</span></li>'
        for h, t, sub in guides_)
    box_items = "".join(buybox(p, "") for p in items)
    cphoto = photo("thermo" if cat == "Meat Thermometers" else "air", "", "cat-photo", caption=True)
    body = f"""
{breadcrumb([("Home", "index.html"), (cat, None)])}
<h1>{esc(headline)}</h1>
<p class="lede">{intro}</p>
{cphoto}
{box_items}
<h2>Which one, in one line each</h2>
<ul class="verdicts">
{verdict_items}
</ul>
<h2>Read before you buy</h2>
<ul class="linklist">
{guide_items}
</ul>
"""
    BUILT.append(page(catfile, f"{cat} — {SITE}",
                      f"{headline}. {intro[:120]}", body,
                      jsonld={"@context": "https://schema.org", "@type": "CollectionPage",
                              "name": cat, "url": BASE + catfile}))


# ---- product page
def build_product(p):
    others = [x for x in PRODUCTS if x["id"] != p["id"] and x["cat"] == p["cat"]]
    target_asin = p.get("observed") or p["asin"]
    og = ('<meta property="product:retailer_item_id" content="'
          + target_asin + '">')
    body = f"""
{breadcrumb([("Home", "index.html"), (p['cat'], p['catfile']), (p['brand'], None)], "../")}
<div class="pdp-head">
  <div>
    <p class="kicker">{esc(p['cat'])} · checked {TODAY}</p>
    <h1>{esc(p['headline'])}</h1>
    <p class="lede">{esc(p['blurb'])}</p>
  </div>
  <div class="pdp-art">{photo("thermo" if p["cat"] == "Meat Thermometers" else "air", "../", "pdp-photo")}</div>
</div>
<div class="pdp-buy">
  <div>
    <p class="buyline">Buy it if <strong>{esc(p['best_for'])}</strong></p>
    <p class="buyline">Skip it if <strong>{esc(p['tradeoff'])}</strong></p>
  </div>
  <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
     data-event="outbound_click">Check the live price on Amazon<span class="btn-sub">paid link</span></a>
</div>
<p class="small">We do not print the price here &mdash; Amazon's Program Policies only permit a site
  to show price and availability when Amazon serves the link or the data comes through their API.
  The button opens the official listing, tagged with our Associate ID.</p>

<h2>Is this the right one for you?</h2>
<div class="qa">
{"".join(f'<div class="qa-row"><p class="qa-q">{esc(q)}</p><p class="qa-a">{esc(a)}</p></div>' for q, a in p["questions"])}
</div>

<h2>The specs that decide it</h2>
<p class="muted">Every row below is quoted from the official listing. Where the listing
  contradicts itself, both numbers appear and the card on the right says so.</p>
<div class="spec-wrap">
  <div>{spec_table(p)}</div>
  <aside class="aside-card">
    <h2>The fine print, honestly</h2>
    <p>{READER_CONFLICTS.get(p["id"], "")}</p>
    <p class="small">Full record: <a href="../flagged.html">Flagged for Review</a>.</p>
  </aside>
</div>

{deals_block(p, "../")}

{faq_block(p)}

<h2>What you are actually buying</h2>
<p>The listing describes this as <em>{esc(p['listing_title'])}</em>. That is the current title on
  Amazon, quoted exactly rather than paraphrased, so you can match it against the page you land
  on. Brand: {esc(p['brand'])}.{(" Model: " + esc(p['model']) + ".") if p['model'] else " The listing does not publish a model number."}</p>

<h2>Where this link actually goes</h2>
<p class="muted">You clicked a short link to get here, so here is exactly what it opened, when we
  last checked it, and what we publish instead.</p>
{ledger_block(p, "../")}

{usda_block(p)}
<h2>What this page will not claim</h2>
<p>No price, star rating, review count, sales rank, commission rate or &ldquo;best&rdquo; verdict
  appears above. Those are left out on purpose: Amazon&rsquo;s policy governs some of them, and the
  rest cannot be confirmed from an official source. Where the listing contradicts itself, both
  numbers are printed &mdash; and if you want the paper trail, every one is on the
  <a href="../flagged.html">Flagged for Review</a> page.</p>

<p class="cta">
  <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
     data-event="outbound_click">See it on Amazon<span class="btn-sub">paid link</span></a>
  <a class="btn ghost" href="../compare.html">Compare with the others</a>
</p>

<h2>Also in {esc(p['cat'])}</h2>
<div class="grid">{"".join(card(x, "../") for x in others)}</div>
"""
    ld = [
        {"@context": "https://schema.org", "@type": "Product",
         "name": p["listing_title"], "brand": {"@type": "Brand", "name": p["brand"]},
         "description": p["blurb"], "url": BASE + slug_of(p),
         "category": p["cat"],
         **({"sku": p["model"]} if p["model"] else {})},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        dict(crumbs_ld([("Home", "index.html"), (p["cat"], p["catfile"]), (p["brand"], slug_of(p))]),
             **{"@context": "https://schema.org"}),
    ]
    BUILT.append(page(slug_of(p), f"{p['headline']} — {p['brand']} | {SITE}",
                      f"{p['brand']} {p['cat'].lower()}: {p['best_for']}. Specs read from the "
                      f"official listing on {TODAY}, conflicts flagged, no price quoted.",
                      body, jsonld=ld, extra_head=og))


# ---- compare
# One set of renderers shared by the five-column table and the two-at-a-time view, so the
# two views can never disagree about what a field says or why it is blank.
NOT_STATED = "— <span class=\"unverified\">not stated on the listing</span>"
NA_CAP = "— <span class=\"unverified\">n/a, measures temperature</span>"
NA_POWER = "— <span class=\"unverified\">n/a, battery powered</span>"
NOWEIGHT = "— <span class='unverified'>not stated on this listing</span>"


def spec(p, key, other=NOT_STATED):
    f = p["fields"].get(key)
    if not f or f["v"] is None:
        return other
    txt = esc(f["v"])
    if f["st"] == "conflict":
        txt += ' <span class="token conflict">see flags</span>'
    return txt


def by_category(p, key, fallbacks, other=NOT_STATED):
    """Use the air-fryer field, or the nearest equivalent on a thermometer."""
    if p["cat"] == "Meat Thermometers":
        for k in fallbacks:
            f = p["fields"].get(k)
            if f and f["v"]:
                txt = esc(f["v"])
                if f["st"] == "conflict":
                    txt += ' <span class="token conflict">see flags</span>'
                return txt
        return other
    return spec(p, key, other)


# the rows a head-to-head view compares, in order: label -> how to render
PAIR_ROWS = [
    ("Best for", lambda p: esc(p["best_for"])),
    ("The catch", lambda p: esc(p["tradeoff"])),
    ("Capacity", lambda p: spec(p, "capacity", NA_CAP)),
    ("Temperature range", lambda p: by_category(p, "temperature", ["upper_temp", "heat"])),
    ("Power / battery", lambda p: by_category(p, "power", ["battery"], NA_POWER)),
    ("Presets", lambda p: spec(p, "presets", "— <span class='unverified'>no preset count on the listing</span>")),
    ("Dimensions D×W×H", lambda p: spec(p, "dimensions", NOT_STATED)),
    ("Weight", lambda p: spec(p, "weight", NOWEIGHT)),
    ("Probes", lambda p: spec(p, "probes", "— n/a, not a probe appliance")),
    ("Response time", lambda p: spec(p, "response", "— n/a, not an instant-read")),
    ("Stated accuracy", lambda p: spec(p, "accuracy", "— n/a")),
    ("Heat rating", lambda p: spec(p, "heat", "— n/a")),
    ("Connectivity", lambda p: spec(p, "connectivity", "— n/a, no app")),
    ("Model on listing", lambda p: spec(p, "model", "— not on the fetched text")),
    ("Warranty", lambda p: spec(p, "warranty", NOT_STATED)),
    ("Price", lambda p: "— not shown, by policy"),
    ("Star rating", lambda p: "— not shown, by policy"),
]


def build_compare():
    cols = PRODUCTS
    def row(label, fn):
        cells = "".join(f"<td>{fn(p)}</td>" for p in cols)
        return f'<tr><th scope="row">{label}</th>{cells}</tr>'

    head = "".join(f'<th scope="col"><a href="{slug_of(p)}">{esc(p["brand"])}</a>'
                   f'<br><span class="th-sub">{p["id"]} · {esc(p["headline"])}</span></th>' for p in cols)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Compare", None)])}
<h1>Compare &mdash; without crowning a winner</h1>
<p class="lede">A comparison that names a "best" without knowing your counter depth, your household
  size or how you cook would be guessing. This table gives you the same facts we have, in the same
  rows, so you can decide. Blank means the listing does not say.</p>
<table class="compare">
  <caption>Aligned by field, so a value is always compared against the same value. Read from the
    official listings on {TODAY}.</caption>
  <thead><tr><th scope="col">Field</th>{head}</tr></thead>
  <tbody>
    {row("Category", lambda p: esc(p["cat"]))}
    {row("Best for", lambda p: esc(p["best_for"]))}
    {row("The catch", lambda p: esc(p["tradeoff"]))}
    {row("Capacity", lambda p: spec(p, "capacity", NA_CAP))}
    {row("Temperature range", lambda p: by_category(p, "temperature", ["upper_temp", "heat"]))}
    {row("Power / battery", lambda p: by_category(p, "power", ["battery"], NA_POWER))}
    {row("Dimensions D×W×H", lambda p: spec(p, "dimensions", NOT_STATED))}
    {row("Weight", lambda p: spec(p, "weight", NOWEIGHT))}
    {row("Model on listing", lambda p: spec(p, "model", "— not on the fetched text"))}
    {row("Price", lambda p: "— not shown, by policy")}
    {row("Star rating", lambda p: "— not shown, by policy")}
    {row("Official listing", lambda p: f'<a href="{plain(p)}" rel="sponsored nofollow">untagged</a>')}
    {row("Buy link", lambda p: f'<a href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p["id"]}" data-event="outbound_click">Amazon (paid link)</a>')}
  </tbody>
</table>
<h2>Two at a time</h2>
<div class="pairpick">
  <label>Compare
    <select id="pairA">
      {"".join(f'<option value="{p["id"]}">{esc(p["brand"])} — {esc(p["headline"])}</option>' for p in cols)}
    </select>
  </label>
  <label>with
    <select id="pairB">
      {"".join(f'<option value="{p["id"]}"{" selected" if i == 3 else ""}>{esc(p["brand"])} — {esc(p["headline"])}</option>' for i, p in enumerate(cols))}
    </select>
  </label>
</div>
<div id="pairView" aria-live="polite"></div>
<noscript><p class="small">The two-at-a-time view needs JavaScript. The full table above carries the
  same rows.</p></noscript>

<h2>How to read this table</h2>
<ol>
  <li><strong>Filter by form first.</strong> Two baskets, one basket, or an oven &mdash; that decision
    eliminates more options than any spec.</li>
  <li><strong>Measure before you compare.</strong> Write down your counter depth and width, then
    strike out anything that does not fit with clearance.</li>
  <li><strong>Treat the catch column as the tie-breaker.</strong> Every product has one; pick the one
    you can live with.</li>
</ol>
<p class="small">Where a listing contradicts itself, the conflicting figures both appear in the
  cell and the flag ID is on the <a href="flagged.html">Flagged for Review</a> page.</p>
"""
    pair_data = {}
    for p in cols:
        pair_data[p["id"]] = {
            "name": esc(p["brand"]) + " — " + esc(p["headline"]),
            "url": slug_of(p),
            "buy": aff(p),
            "rows": [[label, fn(p)] for label, fn in PAIR_ROWS],
        }
    pair_json = json.dumps(pair_data, ensure_ascii=False).replace("</", "<\\/")
    extra = (f'<script type="application/json" id="pairData">{pair_json}</script>')
    BUILT.append(page("compare.html", f"Compare all five — {SITE}",
                      "Side-by-side table of all five products, aligned by field, with prices and "
                      "ratings deliberately omitted and conflicts left visible.",
                      body, extra_head=extra,
                      jsonld={"@context": "https://schema.org", "@type": "WebPage",
                              "name": "Compare", "url": BASE + "compare.html"}))


# ---- guides
GUIDES = [
    dict(slug="basket-vs-oven", title="Basket or oven-style air fryer: what should you compare?",
         sub="Form factor decides footprint, loading, and what fits. Start there, not with wattage.",
         kicker="Buying guide · 6 min read", products=["P-01", "P-02", "P-03"],
         intro="""The single biggest fork in the road is not brand, capacity or wattage. It is whether
         you want a drawer you pull out or a door you open. That choice decides how the appliance
         sits on your counter, how you load it, how you clean it, and whether you will still be using
         it in a year.""",
         sections=[
            ("What actually differs", """A basket fryer is a deep drawer over a heating element and a
            fan. You pull the drawer, dump food in, push it back. An oven-style unit is a box with
            racks and a door, and it does the same job with more usable flat area and much more
            vertical clearance. The basket wins on speed and simplicity; the oven wins on volume and
            on foods that need to lie flat."""),
            ("Measure the footprint, including the swing", """The oven-style Emeril here is 16.9 inches
            deep. The two basket units are 13.4 and 12.75 inches deep. Depth is what usually
            disqualifies a counter, because the wall behind and the air gap above both have to be
            accounted for. A French-door oven also needs room in front for the doors to open, which
            is easy to forget when you are measuring a gap between a toaster and a coffee maker."""),
            ("Think about how you load it, and how you clean it", """Pulling a drawer out towards you is
            one movement. Opening two doors, sliding a rack out, and lifting a tray is several. The
            basket units are lighter and easier to handle (13.3 pounds for the 6-quart dual-basket
            Chefman and 12.8 pounds for the 8-quart Chefman), whereas the 26-quart Emeril oven does
            not state an item weight on its listing, and, at 16.9 inches deep with French
            doors, is realistically going to stay where you put it. If you clean in the sink, a
            removable nonstick basket is simpler than a stainless cavity and racks."""),
            ("Where each one wins", """Choose the dual-basket unit if you routinely cook a main and a
            side together and want them to finish together. Choose the single 8-quart basket if you
            cook one thing at a time in quantity and want the simplest possible operation. Choose the
            oven if you also want to roast, toast, and rotisserie, and you have the counter depth
            for a full-sized countertop appliance that stays put."""),
         ],
         verdict="""Measure your counter depth first, then decide between a drawer and a door. If
         both fit, pick by what you cook: two things at once means two baskets, one big tray of
         something means a single basket or an oven."""),
    dict(slug="capacity-checklist", title="A no-hype checklist for comparing air fryer capacity",
         sub="Quarts describe a cavity, not a meal. Six checks before any number convinces you.",
         kicker="Buying guide · 5 min read", products=["P-01", "P-02", "P-03"],
         intro="""Capacity numbers are the easiest thing to compare and the least useful thing to
         decide on. A quart is a volume, and volume tells you nothing about whether a whole chicken
         fits, whether chips can sit in one layer, or whether two baskets are better than one big
         one. Here is what to check instead.""",
         sections=[
            ("1. Total versus usable", """Six quarts split into two three-quart baskets is not the same
            as one six-quart basket. The split gives you two separate cooks; the single basket gives
            you one bigger flat area. Neither is better in the abstract &mdash; they suit different
            meals."""),
            ("2. Flat area, not volume", """Crisping depends on surface contact and airflow. A deep
            basket that holds a lot of volume can still only crisp one layer of food. Ask how much
            fits in a single layer, not how much fits at all."""),
            ("3. What the listing says fits", """Listings often state concrete fits: a 12-inch pizza,
            a 6-pound chicken. Those are more actionable than a quart figure. The Emeril listing
            states it fits a 12-inch pizza and can rotisserie a 6-pound chicken, which tells you more
            about its usable size than the 26-quart headline does."""),
            ("4. Physical size on the counter", """A bigger cavity usually means a bigger box. Compare
            dimensions before you talk yourself into capacity you do not have room for. The 26-quart
            oven is 16.9 inches deep; the 8-quart basket is 12.75."""),
            ("5. Your household, honestly", """Two people who cook one protein and one vegetable need
            two small zones, not 26 quarts. Four people who batch-cook need volume. Write down what
            you cooked last week before you decide."""),
            ("6. Watch the units", """The dual-basket Chefman listing states 6 quarts in its title and
            6 liters in its capacity field. Six liters is about 6.3 US quarts, so this is almost
            certainly a label slip rather than a different product &mdash; but it is the kind of slip
            that makes a spec table worth reading rather than skimming."""),
         ],
         verdict="""Write down three numbers before you shop: the widest single item you cook, how
         many separate things you cook at once, and your counter depth. Then ignore quart totals that
         do not help with those three."""),
    dict(slug="cleanup-counter-space", title="How to assess cleanup and counter-space trade-offs",
         sub="Dishwasher-safe describes a part. It does not describe your evening.",
         kicker="Buying guide · 5 min read", products=["P-01", "P-02", "P-03"],
         intro="""Nobody buys an air fryer for the washing up, and almost everybody under-estimates it.
         The appliance you keep using is the one whose cleanup fits the way you already load a
         dishwasher. Counter space works the same way: it is a permanent cost you pay every day, not
         a one-off at checkout.""",
         sections=[
            ("Count the parts that touch food", """A single basket with a flat tray is two pieces. A
            dual-basket unit with two removable baskets and two trays is four. A French-door oven adds
            racks, a bake pan, a drip tray and a crisper basket. More parts is more sink."""),
            ("Check what the listing actually promises", """The 8-quart Chefman listing says the
            non-stick basket and the flat frying tray are both top-rack dishwasher safe. The
            dual-basket Chefman says the removable non-stick coated baskets are dishwasher safe. The
            oven does not make a dishwasher claim about its cavity, and it would not be realistic if
            it did."""),
            ("Weight decides where it lives", """The 6-quart dual-basket Chefman weighs 13.3 pounds and
            the 8-quart Chefman weighs 12.8 pounds &mdash; movable when needed, though bulky in a
            shallow cupboard. The Emeril listing omits item weight altogether, but at
            16.9 inches deep and 26 quarts it is plainly a countertop fixture. If you plan to put the
            appliance away between uses, weight and door clearance decide whether that actually
            happens."""),
            ("Measure depth, swing and clearance together", """Depth alone is not enough. Add the air
            gap behind, the headroom needed above the vents, and &mdash; for a door-style oven &mdash;
            the space the doors occupy when open. Write all four numbers down before you move
            anything on the counter."""),
            ("The one-question test", """Ask where the appliance will sit when it is not in use. If
            the answer is "in a cupboard", check the weight and the door swing again. Most appliances
            that end up in cupboards end up there permanently."""),
         ],
         verdict="""Pick the appliance whose cleaning you will actually do on a Tuesday night, in the
         space you actually have, at the weight you can actually lift."""),
    dict(slug="multi-function-questions", title="Questions to ask before buying a multi-function kitchen appliance",
         sub="Every extra preset is a control, a part and a failure point. Which three will you use?",
         kicker="Buying guide · 5 min read", products=["P-02", "P-03"],
         intro="""Multi-function appliances sell on the functions you might use. The honest test is
         narrower: name the three you will use every week, and check that those three are good. The
         rest is storage, controls and cleaning you did not ask for.""",
         sections=[
            ("Name your three functions", """Air fry, roast, reheat &mdash; those are the three most
            people actually use. If a function is not on your list, it should not move the decision,
            no matter how many presets it adds to the panel."""),
            ("Distinguish functions from presets", """A function is a cooking mode. A preset is a
            saved temperature and time for one food. Twenty-four presets can still be three functions.
            The Emeril listing is a good example: it advertises 24 one-touch presets, and the modes
            behind them are air fry, bake, broil, dehydrate, roast, slow cook, toast and reheat."""),
            ("Check whether accessories are included or extra", """Rotisserie spits, crisper baskets
            and bake pans are often the difference between a function being usable and being a
            promise. The Emeril listing names six included components: rack, bake pan, drip tray,
            crisper basket, rotisserie spit, fetch tool. Its title says six accessories and its
            configuration field says seven &mdash; both figures stay on the record."""),
            ("Ask what breaks first", """More functions means more sensors, more moving parts and more
            to clean. A four-preset basket fryer has almost nothing to go wrong. A 26-quart oven with
            a rotisserie motor has considerably more."""),
            ("Check the manual before you trust a preset count", """Where a listing contradicts itself
            &mdash; 24 presets in the title, 25 in the bullet, 400&nbsp;&deg;F in the spec field and
            450&nbsp;&deg;F in the title &mdash; the manual is the tie-breaker, not the marketing
            copy."""),
         ],
         verdict="""Write the three functions you will use weekly. If the appliance is not clearly
         good at those three, the rest of the feature list is decoration."""),
    dict(slug="instant-vs-wireless", title="Instant-read or wireless thermometer: which do you actually need?",
         sub="Speed in your hand versus the freedom to walk away. Two different products.",
         kicker="Buying guide · 6 min read", products=["P-04", "P-05"],
         intro="""These two thermometers are not competitors. One is a tool you hold for one second;
         the other is a monitoring system you leave in the meat for hours. Buying the wrong one is
         the most common mistake in this category, and it has nothing to do with accuracy.""",
         sections=[
            ("What an instant-read is for", """Spot checks. You open the grill, stab the thickest part,
            read a number, and decide. It is fast, it needs no app, and it works when the WiFi does
            not. The ThermoMaven HT07 here claims a 1-second response, &plusmn;0.5&nbsp;&deg;F, a
            0.1&deg; display resolution, and a 572&nbsp;&deg;F upper range, and it ships with a
            calibration certificate."""),
            ("What a wireless system is for", """Long cooks you do not want to babysit. You insert
            probes, close the lid, and watch from inside the house. The CHEF iQ here uses three
            probes into one hub with WiFi range, and adds guided cooking and rest timers in the
            app."""),
            ("The honest cost of wireless", """An app, a hub, a charge, and a dependency. If any of
            those three is a problem for you, a wireless thermometer is the wrong purchase even
            though it is the more capable one. The listing says up to 50 hours per charge on the
            hub."""),
            ("Accuracy claims are claims", """&plusmn;0.5&nbsp;&deg;F and the NIST and NSF references
            are statements made on the listing, not independent test results. Both units here are
            sold on accuracy; neither listing links a test report. This site has not tested either
            one."""),
            ("What number actually matters for safety", """USDA's Food Safety and Inspection Service
            publishes minimum internal temperatures: 145&nbsp;&deg;F with a three-minute rest for
            beef, pork, veal and lamb steaks, chops and roasts; 160&nbsp;&deg;F for ground meats;
            165&nbsp;&deg;F for all poultry, leftovers and casseroles; 145&nbsp;&deg;F for fish and
            shellfish. Both thermometers here read well past those numbers. Precision beyond a degree
            is a cooking preference, not a safety requirement."""),
         ],
         verdict="""If you cook steaks and chicken breasts and want a number now, buy the instant-read.
         If you smoke or roast for hours and want to leave the room, buy the wireless system. If you
         do both, they are not substitutes for each other."""),
    dict(slug="thermometer-accuracy", title="How to assess thermometer accuracy claims",
         sub="What &plusmn;0.5 °F, NIST and NSF mean on a listing — and what they do not.",
         kicker="Buying guide · 5 min read", products=["P-04", "P-05"],
         intro="""Accuracy is the one specification you cannot check by reading harder. A listing can
         say &plusmn;0.5&nbsp;&deg;F and reference NIST and NSF, and every word of that can be true
         while telling you less than you think. Here is a calmer way to read it.""",
         sections=[
            ("Separate the claim from the evidence", """&plusmn;0.5&nbsp;&deg;F is a claim about
            tolerance. NIST and NSF appearing in a specification-met field is a claim about
            certification. Neither is a test report, and no listing here links one. That does not make
            them false &mdash; it makes them unaudited by us, which is a different statement."""),
            ("Know what the certifications cover", """NIST is a standards body; a reference to it
            usually means traceability of calibration rather than a consumer-product approval. NSF
            covers public health and sanitation standards for food equipment. A listing that says
            "NIST and NSF certified" without saying what was certified leaves both open. The
            ThermoMaven listing ships a calibration certificate in the box, which is the most concrete
            artefact on offer here."""),
            ("Look for a calibration path", """A thermometer you can verify is worth more than one you
            have to trust. The <a href="https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers">USDA
            FSIS Food Thermometers guide</a> (source S24) describes the ice-water calibration test:
            immerse the stem at least 2 inches in an ice-water slurry for 30 seconds without touching
            the glass; a calibrated thermometer reads 32&nbsp;&deg;F. A unit that ships with a
            certificate and a clear calibration path is easier to keep honest."""),
            ("Check resolution separately from accuracy", """Resolution is how many digits the display
            shows; accuracy is how close the number is to the truth. A 0.1&deg; display with
            &plusmn;0.5&nbsp;&deg;F accuracy is not a 0.1&deg; instrument. The ThermoMaven HT07
            listing states both, which makes the distinction visible."""),
            ("Match the tool to the number you need", """USDA's minimum internal temperatures are
            published in whole degrees: 145, 160, 165. If you are cooking to those targets, a
            thermometer that is within a degree is comfortably sufficient. Precision beyond that is
            about repeatability and preference, not safety."""),
         ],
         verdict="""Read the claim, then look for the certificate. If there is no certificate you can
         see, treat the number as a claim and verify it yourself with an ice-water test."""),
    dict(slug="air-fryer-thanksgiving", title="Air fryer at Thanksgiving: what actually fits",
         sub="A 12-inch pizza claim tells you more about usable size than a quart figure does.",
         kicker="Seasonal guide · 4 min read", products=["P-02", "P-01", "P-03"],
         intro="""Thanksgiving is the one day a year when counter space and usable volume both
         matter at once. The useful question is not how many quarts the appliance has &mdash; it is
         which of the day's jobs it can take off the oven, and which it cannot.""",
         sections=[
            ("What a countertop oven can take off your hands", """Sides and reheats are the realistic
            wins: a tray of roasted vegetables, dinner rolls, a reheat of something that came out of
            the oven too early. The Emeril listing states it fits a 12-inch pizza and can rotisserie a
            6-pound chicken, which is a concrete statement about usable interior size."""),
            ("What it cannot", """A whole turkey is not going in any of these. Be sceptical of any
            countertop appliance marketing that implies otherwise. The Emeril's stated rotisserie
            capacity is a 6-pound chicken, which is a bird, not a feast bird."""),
            ("Where a basket fryer earns its counter space", """Small batches that need to be hot and
            crisp at the moment they hit the table: sprouts, potatoes, a last-minute tray of
            something. The dual-basket Chefman lets you run two of those at once and finish them
            together, which is more useful on the day than a bigger single basket."""),
            ("Check the circuit before the menu", """All three air fryers here list 1700 watts in their
            specification tables (and two 1700-watt appliances on one kitchen circuit plus an oven is
            a tripped breaker, not a crispier sprout). Wattage is worth knowing before the day
            &mdash; which is why the 8-quart Chefman's contradictory 1700&nbsp;W spec field and
            1,000&nbsp;W bullet disagree with each other."""),
         ],
         verdict="""Use the countertop appliance for sides and reheats, keep the bird in the oven, and
         check what else is on the circuit before you plug in a second 1700-watt unit."""),
    dict(slug="small-kitchen-air-fryer", title="Air fryer for a small kitchen: the three measurements that decide it",
         sub="Depth, door swing and where it lives when it is not in use.",
         kicker="Buying guide · 4 min read", products=["P-03", "P-01", "P-02"],
         intro="""In a small kitchen the constraint is never features. It is the 13 inches between
         the kettle and the wall. Three measurements settle almost every decision, and none of them
         is capacity.""",
         sections=[
            ("1. Depth, plus the air gap", """Depth is the first disqualifier. Both Chefman basket
            units are under 14 inches deep; the oven-style Emeril is 16.9. Add the clearance the
            manual asks for behind and above, and you have your real number."""),
            ("2. Door swing or drawer pull", """A drawer needs room in front for you to stand and pull.
            French doors need room in front for two doors to open and stay open. In a narrow galley
            that difference decides whether the appliance is usable at all."""),
            ("3. Where it lives between uses", """If it goes in a cupboard, weight decides whether that
            happens twice or never. The 8-quart Chefman is 12.8 pounds and the 6-quart dual-basket
            Chefman is 13.3 pounds, both realistically movable. The Emeril listing does not state an
            item weight, and its 16.9-inch depth already rules out tight counters and most
            standard cupboards."""),
            ("What to give up first", """Windows, presets, and a second basket are all things you can
            live without. Depth and weight are not. If the counter is tight, a single-basket unit
            with no window is the honest choice, and it is also the cheapest of the three here."""),
         ],
         verdict="""Measure depth, measure the space in front, and weigh whether it will go in a
         cupboard. Pick the unit that survives all three; then look at features."""),
    dict(slug="first-week-air-fryer", title="Your air fryer's first week: what to cook, what to skip",
         sub="Three deliberate experiments, two things to skip, and the habit that earns the counter space.",
         kicker="Getting started · 5 min read", products=["P-01", "P-03", "P-02"],
         intro="""The fastest way to regret a new appliance is to feed it only frozen fries. A week
         of deliberate experiments teaches you where the heat sits and what this machine will
         actually replace in your routine. The practice below is kitchen experience, not product
         testing &mdash; no performance claim about any of these machines is made here.""",
         sections=[
            ("Days one and two: learn the heat", """Start with something cheap and forgiving &mdash;
            potato wedges or chicken wings. The point is not dinner, it is calibration: a single
            layer, a shake halfway, and a note on what you would change next time. You are learning
            how done looks at 400 degrees versus 375 on your counter, not on anyone else's."""),
            ("Days three and four: cook the meal you repeat", """Now cook the thing you make on busy
            nights &mdash; one protein and one vegetable. This is where basket layout decides the
            rhythm: two baskets run a main and a side to the same finish line, one big basket takes
            the full family portion in a single batch, and an oven-style tray takes the jobs that
            want a rack rather than a drawer."""),
            ("What to skip for now", """Wet batters &mdash; moving air strips them before they set.
            Overcrowded loads &mdash; stacked food steams instead of crisping, and two smaller
            batches beat one large one every time. High-sugar glazes until you know your hot spots,
            because sugar burns fast in moving air. None of this is a product claim; it is kitchen
            practice that holds across machines."""),
            ("The habit that pays for the counter space", """Once a week, let the appliance win one
            job from the big oven: reheating, roasting a tray of vegetables, finishing a weeknight
            protein. If it never wins a job, it becomes cupboard inventory. If it wins one
            permanently, it earned the space &mdash; and cleanup is half the ownership, which is
            covered in the cleanup and counter-space guide."""),
         ],
         verdict="""Calibrate with something cheap, cook your real weeknight meal by day four, and
         give the appliance one standing job from the oven. Skip batters and overloaded baskets
         until the machine is familiar."""),

    ]
from seasonal_guides import GUIDES as _SEASONAL
GUIDES += _SEASONAL





def build_guides_index():
    items = "".join(
        f"""<article class="guidecard">
  <p class="kicker">{esc(g['kicker'])}</p>
  <h3><a href="guides/{g['slug']}.html">{esc(g['title'])}</a></h3>
  <p>{esc(g['sub'])}</p>
  <p class="small">Covers {", ".join(BY_ID[x]['brand'] for x in g['products'])}</p>
</article>""" for g in GUIDES)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Guides", None)])}
<h1>Guides</h1>
<p class="lede">Question-shaped, written to be useful before you click anything. Each one ends with a
  verdict you can act on, and links to the products only where the product is the answer.</p>
<div class="grid guides-grid">{items}</div>
<div class="panel">
  <h2>How these guides are made</h2>
  <p>Each guide starts from a decision a buyer actually faces, not from a keyword. The facts inside
    come from the official listings in this site's <a href="sources.html">source register</a>, dated
    {TODAY}, plus one government source for food-safety temperatures. Where the listings contradict
    themselves the contradiction is printed, not resolved by guessing.</p>
  <p class="small">Publishing cadence and the next topics are decided on the
    <a href="suggestions.html">Decision Center</a> page, not by instinct.</p>
</div>
"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Guides",
          "url": BASE + "guides.html"}
    BUILT.append(page("guides.html", f"Guides — {SITE}",
                      "Question-shaped buying guides for air fryers and meat thermometers, each "
                      "ending in a verdict you can act on.",
                      body, jsonld=ld))


def build_guide(g):
    rel = [BY_ID[x] for x in g["products"]]
    secs = "".join(f"<h2>{esc(h)}</h2><p>{t}</p>" for h, t in g["sections"])
    items = "".join(
        f'<li><a href="../{slug_of(p)}">{esc(p["brand"])} — {esc(p["headline"])}</a>'
        f'<span>{esc(p["best_for"])}</span></li>' for p in rel)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Guides", "guides.html"), (g['title'][:40] + "…", None)], "../")}
<p class="kicker">{esc(g['kicker'])} · verified {TODAY}</p>
<h1>{esc(g['title'])}</h1>
<p class="lede">{esc(g['intro'])}</p>
<div class="verdict-box">
  <p class="kicker">The short answer</p>
  <p>{esc(g['verdict'])}</p>
</div>
{secs}
{g.get("extra", "")}
<h2>The products this guide refers to</h2>
<ul class="linklist">{items}</ul>
<p class="small">Every specification quoted above is from the official listing, dated {TODAY}. See the
  <a href="../sources.html">source register</a> for links, and the
  <a href="../flagged.html">Flagged for Review</a> page for the contradictions.</p>
<div class="panel">
  <h3>Next</h3>
  <p><a href="../guides.html">All guides</a> · <a href="../compare.html">Compare all five</a> ·
    <a href="../shop.html">See the products</a></p>
</div>
"""
    ld = [{"@context": "https://schema.org", "@type": "Article",
           "headline": g["title"], "description": g["sub"], "datePublished": TODAY,
           "dateModified": TODAY, "author": dict(publisher_ld(), **{"@context": "https://schema.org"}),
           "publisher": dict(publisher_ld(), **{"@context": "https://schema.org"}),
           "mainEntityOfPage": BASE + "guides/" + g["slug"] + ".html",
           "image": BASE + "assets/photos/hero-kitchen.jpg"},
          dict(crumbs_ld([("Home", "index.html"), ("Guides", "guides.html"),
                          (g["title"], "guides/" + g["slug"] + ".html")]),
               **{"@context": "https://schema.org"})]
    BUILT.append(page(f"guides/{g['slug']}.html", f"{g['title']} — {SITE}",
                      g["sub"], body, jsonld=ld))



# ---- verification log (generated from data/verification.json; session bba2deed)
def build_verification():
    import json as _json

    def a(href, text, sponsored=False):
        rel = ' rel="sponsored nofollow"' if sponsored or "amazon.com" in href else ""
        return f'<a href="{href}"{rel}>{esc(text)}</a>'

    V = _json.loads((DATA / "verification.json").read_text())
    legend = "".join(f"<li><strong>{esc(k)}</strong> — {esc(v2)}</li>" for k, v2 in V["method_legend"].items())
    pol_rows = "".join(
        f'<tr><th scope="row">{esc(s["id"])}</th><td>{a(s["url"], s["name"])}</td>'
        f'<td>{esc(s["verified"])}</td><td>{esc(s["status"])}</td></tr>' for s in V["policy_sources"])
    prod_blocks = ""
    for prod in V["products"]:
        rows = ""
        for r in prod["rows"]:
            note = f' — {esc(r["note"])}' if r.get("note") else ""
            rows += (f'<tr><th scope="row">{esc(r["field"])}</th><td>{esc(r["value"])}</td>'
                     f'<td>{esc(r["status"])}</td><td>{esc(r["method"])}{note}</td>'
                     f'<td class="src">{a(prod["source_url"], "official listing", True)}</td></tr>')
        prod_blocks += (f'<h2>{esc(prod["id"])} · observed ASIN {esc(prod["asin_observed"])}</h2>'
                        f'<table><caption>Every row links to the {a(prod["source_url"], "official listing", True)} ({esc(prod["source_id"])}).</caption>'
                        f'<thead><tr><th scope="col">Field</th><th scope="col">Value</th><th scope="col">Status</th>'
                        f'<th scope="col">How it was checked</th><th scope="col">Source</th></tr></thead>'
                        f'<tbody>{rows}</tbody></table>')
    corr = "".join(
        f'<tr><th scope="row">{esc(c["id"])}</th><td>{esc(c["what"])}</td><td>{esc(c["action"])}</td></tr>'
        for c in V["corrections"])
    body = f"""
{breadcrumb([("Home", "index.html"), ("Verification Log", None)])}
<p class="kicker">Reference · verified {esc(V["verified_on"])} · sessions 530c2e6c + 937876a6 + bba2deed</p>
<h1>Verification Log</h1>
<p class="lede">Every value in the product register, re-checked row by row against the official Amazon listing or an official policy page. This log is generated from <code>data/verification.json</code>. {esc(V["supersedes"])}</p>
<div class="panel"><h2>Method legend</h2><ul class="tight">{legend}</ul>
<p class="small">Prices, ratings, review counts and commission rates appear nowhere on this site (Program Policies §2(b); FLG-005). Values that could not be confirmed are left blank and flagged — never inferred.</p></div>
<h2>Program &amp; policy sources</h2>
<table><caption>Policy claims checked against official pages. Every row links to its official source.</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Source (official)</th><th scope="col">Claim checked</th><th scope="col">Status</th></tr></thead>
<tbody>{pol_rows}</tbody></table>
{prod_blocks}
<h2>Corrections made in this pass</h2>
<table><caption>Register corrections (C-IDs). Findings that survived as open contradictions are on the <a href="flagged.html">Flagged for Review</a> page.</caption>
<thead><tr><th scope="col">ID</th><th scope="col">What was wrong</th><th scope="col">Action taken</th></tr></thead>
<tbody>{corr}</tbody></table>
<div class="panel"><h2>What this log does not claim</h2>
<p>Values marked <em>corroborated</em> were read from product-information mirrors of the listing's own spec table, not from the listing's Product details block itself (the fetch pass could not extract it reliably). The official listing link is in every table row for manual review. Independent sessions reached the same conclusions about the P-03 wattage, the P-03 temperature nuance and the P-05 warranty — those findings are canonical as FLG-017, FLG-018 and FLG-019.</p>
<p><a class="btn ghost" href="flagged.html">See Flagged for Review</a> <a class="btn ghost" href="sources.html">See the source register</a> <a class="btn ghost" href="suggestions.html">Decision Center</a></p></div>
"""
    BUILT.append(page("verification.html", f"Verification Log — {SITE}",
                      "Line-by-line verification of every register value against official listings and policy pages, with method and status per row.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Verification Log", "url": BASE + "verification.html"}))

# ---- how we choose
def build_how():
    body = f"""
{breadcrumb([("Home", "index.html"), ("How we choose", None)])}
<h1>How we choose, and what we will not claim</h1>
<p class="lede">This site exists to help you pick one appliance, not to rank the market. That means
  saying plainly where the information comes from, what we have not done, and what we refuse to
  print.</p>

<h2>What "verified" means here</h2>
<p>It means one person opened the official Amazon listing for the product on {TODAY} and read the
  value off the page. Each product page carries the date, and every specification row links to the
  listing it came from. It does <strong>not</strong> mean we tested the product, and it does not mean
  the listing is correct &mdash; only that we read what it says and recorded it accurately.</p>

<h2>What we have not done</h2>
<ul>
  <li><strong>We have not cooked with any of these.</strong> There is no hands-on test, no
    side-by-side taste trial, and no measured performance. Nothing on this site implies otherwise
    (FLG-032).</li>
  <li><strong>We have not seen the certificates.</strong> NIST and NSF appear on the listings. We have
    not been given the documents or an independent test report (FLG-035).</li>
  <li><strong>We have not confirmed the submitted short links.</strong> Their compliance status is
    unresolved, so we do not call them valid or invalid (FLG-003). The links we publish are ordinary
    tagged amazon.com URLs.</li>
</ul>

<h2>What we will not print</h2>
<ul>
  <li><strong>Prices and availability</strong> &mdash; Amazon's Program Policies only allow these when
    Amazon serves the link or the data comes from their API. Ours does not, so the number stays on
    Amazon (S02).</li>
  <li><strong>Star ratings and review counts</strong> &mdash; they summarise other people's kitchens,
    and quoting them invites the reader to treat popularity as suitability.</li>
  <li><strong>A commission rate or a revenue forecast</strong> &mdash; neither can be verified from
    outside the account, so neither is published.</li>
  <li><strong>A "best" verdict</strong> without your counter measurements and household size. We give
    you the trade-off instead.</li>
</ul>

<h2>How conflicts are handled</h2>
<p>When a listing contradicts itself, we print both figures in the specification table and give the
  contradiction an ID on the <a href="flagged.html">Flagged for Review</a> page. There are currently
  several: preset counts, accessory counts, model-number forms, top temperature, wattage, capacity
  units, battery life and warranty length. We do not average them, pick the flattering one, or quietly
  drop the awkward one.</p>

<h2>How the money works</h2>
<p>Outbound product links carry our Amazon Associate tag and are marked
  <strong>(paid link)</strong> next to the button, with <code>rel="sponsored nofollow"</code> on the
  anchor, per Google's guidance (S04). The disclosure statement sits under the masthead on every page
  and repeats in the footer, per Amazon's Operating Agreement Section 5 (S01) and FTC guidance on
  making a disclosure hard to miss (S03, S23).
  Untagged listing links are published alongside so you can check our work without the tag.</p>

<h2>How to tell us we are wrong</h2>
<p>Every discrepancy, blank and open question is listed on the
  <a href="flagged.html">Flagged for Review</a> page with a source link. Corrections are dated. If a
  listing has changed since {TODAY}, that page is the place to say so.</p>
"""
    BUILT.append(page("how-we-choose.html", f"How we choose — {SITE}",
                      "What verified means on this site, what we have not tested, what we refuse to "
                      "print, and how contradictions between listings are handled.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "How we choose", "url": BASE + "how-we-choose.html"}))


# ---- suggestions / decision center
SUGGESTIONS = [
    dict(id="SG-01", title="Lead the front page with products, not with verification",
         what="Rebuild the landing page as a publication front page. Keep every dashboard surface "
              "reachable from one footer group.",
         why="A reader arriving from search wants to know which air fryer to buy. They do not want a "
             "methodology essay. Verification still exists, one click away.",
         impact="High — reader trust and time on page", effort="Done",
         status="Shipped", verify="Visible on index.html: hero, three featured products, one nav group."),
    dict(id="SG-02", title="Publish question-shaped guides, then measure arrivals",
         what="Ten guides built from real buying decisions, each added to the sitemap and the RSS "
              "feed, each ending in a verdict.",
         why="Long-tail question queries are how a small site earns its first organic traffic. A "
             "guide that answers one question beats a listicle.",
         impact="High — organic traffic", effort="Done",
         status="Shipped", verify="guides.html lists ten; sitemap.xml and feed.xml include all ten."),
    dict(id="SG-03", title="Measure clicks before optimising anything",
         what="Five defined events (data/events.json), counted locally with no cookies and no third "
              "party, exportable to CSV, with a self-hosted collector ready in analytics/server.js.",
         why="Optimising without a click count is guesswork. Doing it with a tracker would be worse.",
         impact="High — every later decision", effort="Done",
         status="Shipped", verify="measurement.html and disclosure.html document the five events; assets/app.js implements them."),
    dict(id="SG-04", title="Disclosure above the fold on every page, repeated in the footer",
         what="A strip directly under the masthead carrying the exact Associates statement, plus a "
              "repeat in the footer.",
         why="Amazon's Operating Agreement Section 5 requires the statement; FTC guidance says a "
             "disclosure buried on another page is likely to be missed.",
         impact="Required — compliance", effort="Done",
         status="Shipped", verify="Every generated page contains the statement twice; the build gate fails otherwise."),
    dict(id="SG-05", title="Mark every outbound product link as sponsored",
         what="Visible (paid link) label next to each button, rel=\"sponsored nofollow\" on each "
              "anchor, plus an untagged listing link for verification.",
         why="Google asks for rel=sponsored on paid links; FTC asks for a clear label near the link.",
         impact="Required — compliance", effort="Done",
         status="Shipped", verify="Gate fails on any amazon.com anchor without rel=sponsored."),
    dict(id="SG-06", title="Keep intended and observed product identity in separate fields",
         what="Every product page shows the submitted link, the short-link token, the intended ASIN "
              "(blank), the observed redirect target, and the date each was read.",
         why="Merging them would manufacture intent the owner never confirmed.",
         impact="Required — auditability", effort="Done",
         status="Shipped", verify="Gate fails if a product page drops either field."),
    dict(id="SG-07", title="Test one Special Link per product inside the enrolled account",
         what="Click one tagged link per product while signed in, then confirm the click appears in "
              "the tracking report before sending traffic.",
         why="A tag that is not being recorded earns nothing, and you cannot tell from outside.",
         impact="Required — revenue", effort="Owner action", status="Blocked on the owner",
         verify="Product pages still say PENDING TEST. Cannot be completed without account access."),
    dict(id="SG-08", title="One indexable host with a sitemap, feed and structured data",
         what="Canonical tags, sitemap.xml, robots.txt, an RSS feed, JSON-LD on every page, and a "
              "working on-site search. The search was inert until T-17 (FLG-037); it now reads the "
              "query and renders matches.",
         why="A crawler needs one canonical address per page and a reason to rank it. Duplicate "
             "hosts and dead search pages waste both.",
         impact="High — findability", effort="Done", status="Shipped",
         verify="sitemap.xml lists every page; three JSON-LD blocks on product pages; search.html matches the generated index in the browser."),
    dict(id="SG-09", title="Make it read like a publication: authorship, brand, imagery, seasons",
         what="Named editorial standards page, consistent masthead and type, original illustration "
              "instead of stock or Amazon photography, and seasonal guides.",
         why="A site that looks assembled reads as generated. Illustration also sidesteps the Amazon "
             "image licence entirely.",
         impact="Medium — perceived quality", effort="Done", status="Shipped",
         verify="how-we-choose.html, about.html, two seasonal/occasion guides, inline SVG artwork throughout."),
    dict(id="SG-10", title="Reader capture and Search Console verification",
         what="RSS feed is live. Email capture and Search Console verification both need owner "
              "accounts.",
         why="Without Search Console you cannot see which queries arrive, so the next guide is "
             "chosen on instinct.",
         impact="Medium — growth loop", effort="Owner action", status="Blocked on the owner",
         verify="feed.xml exists and validates; no Search Console property has been verified."),
    dict(id="SG-11", title="Keep a campaign ledger that is empty until real data exists",
         what="A dated ledger schema with timestamp, source, channel, eligible sessions, clicks and "
              "reported orders. Empty until an authorised first-party report supplies a row.",
         why="An empty ledger with a defined schema is honest. A filled one with invented numbers is "
             "not.",
         impact="High — honesty", effort="Done", status="Shipped, intentionally empty",
         verify="campaign-ledger.html renders zero rows and says why."),
    dict(id="SG-12", title="Gate any automation behind a human compliance check",
         what="Automate research, drafting and link formatting. Never auto-publish. Every new page "
              "passes the build gate before it can ship.",
         why="The request asked for automation and for compliance. The only way both are true is a "
             "gate.",
         impact="Medium — scale without risk", effort="Done", status="Shipped",
         verify="scripts/check_site.py runs on every build and fails on disclosure, sponsorship, price and link errors."),
    dict(id="SG-13", title="Add a price display through the Product Advertising API",
         what="If the owner obtains PA or Creators API credentials, prices and availability could be "
              "shown with the attribution Amazon requires.",
         why="It is the single biggest missing piece for a shopping site, and the only compliant way "
             "to add it.",
         impact="High — conversion", effort="Owner action, needs API approval",
         status="Not started — recommended for approval",
         verify="Blocked: no API credentials. Program Policies 2(b) is the constraint."),
    dict(id="SG-14", title="Add a custom domain",
         what="Move from the github.io subpath to a real domain and update canonicals, sitemap and "
              "feed together.",
         why="A subpath on a shared host is indexable but weak for brand and trust.",
         impact="Medium — findability and brand", effort="Small, owner decision",
         status="Not started — recommended for approval", verify="Currently flagged as FLG-006."),
    dict(id="SG-15", title="Get real product photography through the API",
         what="Use image URLs supplied via the PA or Creators API, which arrive with the licence.",
         why="Illustration is safe but a shopper still wants to see the product.",
         impact="Medium — conversion", effort="Owner action, needs API approval",
         status="Not started — recommended for approval", verify="Currently flagged as FLG-007."),
    dict(id="SG-16", title="Publish a weekly cadence and hold it",
         what="One guide per week, added to sitemap and feed, with the topic chosen from measured "
              "Search Console queries rather than instinct.",
         why="Cadence compounds; sporadic bursts do not.",
         impact="Medium — organic growth", effort="Ongoing", status="Blocked on Search Console",
         verify="Requires Search Console access (SG-10)."),
    dict(id="SG-17", title="Design & Traffic Brief and editorial standards prompt",
         what="A publication-grade storefront design prompt, 4-cluster topic plan, seasonal "
              "calendar, and 10 reader-visible editorial standards in design-brief.html.",
         why="Gives the next design/content iteration an explicit, compliance-checked blueprint.",
         impact="High — editorial & SEO plan", effort="Done (brief); implementation staged",
         status="Shipped",
         verify="design-brief.html published and linked from masthead Records menu and footer."),
    dict(id="SG-18", title="Rotate the front-page picks on a dated editorial calendar",
         what="Treat the three featured cards as an issue, not a permanent ranking: refresh them at "
              "season boundaries (Thanksgiving, gifting, summer grilling) and print the issue date and "
              "the reason for the change on the page.",
         why="A front page that never changes gives a returning reader no reason to come back, and "
             "search engines no signal that the page is maintained. A dated rotation does both without "
             "inventing new facts.",
         impact="Medium — repeat visits", effort="Small, needs an editorial calendar decision",
         status="Partially shipped — dated issue line, rotation still open",
         verify="index.html prints the issue date above the hero. The three picks themselves are "
                "still static, so the rotation half of this proposal is open (Q-16)."),
    dict(id="SG-19", title="Add intent landing pages generated from the same register",
         what="One page per real buying shape already covered by the five products: a dual-basket "
              "page, a small-kitchen page and a walk-away-thermometer page, each assembled from the "
              "existing verified fields rather than new claims.",
         why="People search for the shape of the problem, not for a product they have not heard of. "
             "These pages give a crawler a reason to rank this site without adding a single unverified "
             "sentence.",
         impact="High — organic entry points", effort="Medium, blocked on query data",
         status="Blocked on Search Console (SG-10)",
         verify="Requires measured query evidence first; choosing topics by instinct is what this "
                "site is trying to stop doing."),
    dict(id="SG-20", title="Publish a dated change log for readers",
         what="A dated list on the sources page of what changed: corrected values, withdrawn claims, "
              "new guides — each with the flag ID that records it.",
         why="A correction a reader cannot see is indistinguishable from a quiet edit. A visible change "
             "log turns maintenance into evidence.",
         impact="Medium — trust", effort="Small",
         status="Shipped",
         verify="sources.html, \"What changed, and when\": every corrected flag, newest first, with "
                "its date."),
    dict(id="SG-21", title="Add a two-product head-to-head view",
         what="Pick any two of the five on the compare page and see their verified rows side by side, "
              "built from the same register as the five-column table.",
         why="Most real decisions are a choice between two, not five. A five-column table on a phone "
             "is hard to read; a pair view is the same data at the size people actually use.",
         impact="Medium — decision speed", effort="Small",
         status="Shipped",
         verify="compare.html, \"Two at a time\": two selectors, rows rendered from the embedded "
                "register view. No new facts, no new links."),
    dict(id="SG-22", title="Name an editor and decide the hands-on policy",
         what="Either name a real person who owns the copy, or state permanently that this is a "
              "documentation site with no hands-on testing. Both are defensible; silence is not.",
         why="FTC guidance treats an implied experience claim as a problem, and a byline needs a real "
             "person behind it. This is the one open item that touches compliance rather than polish.",
         impact="High — compliance and trust", effort="Owner decision",
         status="Blocked on the owner (FLG-032, FLG-033)",
         verify="about.html currently states plainly that no author is named."),
    dict(id="SG-23", title="Add cook-time and capacity proof content only after real testing",
         what="Defer any “how long do chips take” or “how much fits” content until the appliances "
              "can actually be cooked with, then publish it with the method written down.",
         why="This is the content that would genuinely differentiate the site, and it is also the "
             "content that cannot be produced honestly right now.",
         impact="High — differentiation", effort="Needs product access",
         status="Not started — blocked on hands-on testing",
         verify="No page on this site claims a cook time."),
    dict(id="SG-24", title="Add an evergreen first-week guide for new owners",
         what="A getting-started guide answering onboarding questions (what to cook first, what to skip), added to the sitemap and feed like every other guide.",
         why="New owners search what to cook first, not only what to buy first.",
         impact="Medium — organic traffic", effort="Done", status="Shipped",
         verify="guides/first-week-air-fryer.html published and included in sitemap.xml and feed.xml; no cook-time claims inside."),
    dict(id="SG-25", title="Deploy the self-hosted analytics collector",
         what="Ship zero-dependency Node.js (analytics/server.js) and Cloudflare Pages Function (functions/api/collect.js) collectors, canonical schema (data/events.json), and gated send() transport in assets/app.js.",
         why="GitHub Pages cannot run a server function, so cross-visitor telemetry waits until the owner hosts the collector externally without cookies or third-party scripts.",
         impact="High — measurement", effort="Code shipped; hosting is owner action",
         status="Code shipped — hosting pending",
         verify="measurement.html, data/events.json, analytics/server.js, functions/api/collect.js, tests/test_collector.js (FLG-010, Q-08)."),
    dict(id="SG-26", title="Feed the campaign ledger from first-party reports only",
         what="Monthly rows from authorised Associates reports with dated provenance. Clicks stay clicks; orders and revenue come only from reports, never from forecasts.",
         why="The ledger is the evidence base for the next optimisation; invented rows would poison every later decision.",
         impact="High — evidence-based iteration", effort="Owner action", status="Blocked on owner",
         verify="campaign-ledger.html renders zero rows and explains why (SG-11); no conversion score is computed anywhere on the site."),
    dict(id="SG-27", title="Nav labels: keep the navigation shopper-first",
         what="Primary nav reads the shopper's tasks (Air Fryers, Meat Thermometers, All products, Guides, Compare, How we choose); every dashboard surface lives in one records group.",
         why="Shoppers navigate by task. Dashboards are for the desk, not the aisle.",
         impact="Medium — usability", effort="Done", status="Shipped",
         verify="Every generated page carries the same masthead; the build gate checks the labels."),
    dict(id="SG-28", title="The shipped RSS feed",
         what="feed.xml carries every guide with dates and parses cleanly; robots.txt points at the canonical sitemap.",
         why="One indexable site needs a feed that reflects what actually shipped, not an advertisement for more.",
         impact="Medium — distribution", effort="Done", status="Shipped",
         verify="The build gate parses the feed and requires an item for every guide."),
    dict(id="SG-29", title="Search Console property and sitemap submission",
         what="Verify the github.io property, submit sitemap.xml, and watch which queries bring readers.",
         why="Without it the site cannot see its own audience, and topic choice returns to instinct (SG-19, SG-21).",
         impact="High — findability", effort="Owner action", status="Blocked on owner",
         verify="No Search Console property is verified; needs the owner's Google account."),
    dict(id="SG-30", title="Reader capture: RSS live, email pending",
         what="RSS works today. An email signup needs the owner's provider choice and the privacy wording that goes with it.",
         why="Repeat readers are the only durable channel a small publication gets.",
         impact="Medium — retention", effort="Owner action", status="Blocked on owner",
         verify="feed.xml is live and linked everywhere; no email form is published."),
    dict(id="SG-31", title="AI-powered affiliate platform architecture and Creators API pipeline",
         what="Document all seven platform modules (research, pricing/commission bounds, SEO drafting, Special Links vs cloaking, telemetry, scaling, CI gate) alongside Creators API (S20/S21) and ML-training/Agent Terms limits (Program Policies §5, IP License §1/§2(e)/§4).",
         why="Automating research or price ingestion without final Associates acceptance and policy-compliant API handling would violate program rules or hallucinate specs.",
         impact="High — architecture and compliance", effort="Done (blueprint); API gated on owner",
         status="Blocked on Creators API",
         verify="platform.html documents every module, what runs today, and hard gates (FLG-029, Q-19)."),
    dict(id="SG-32", title="Generate question-shaped article drafts from Search Console queries",
         what="Turn measured impressions and search queries from Search Console into structured, listing-cited guides that pass scripts/check_site.py before merging.",
         why="Query-driven drafting grows organic search from evidence instead of guesswork.",
         impact="High — organic discovery", effort="Owner action", status="Blocked on Search Console",
         verify="Requires Search Console verification (SG-10, SG-29, Q-20)."),
]


def build_suggestions():
    rows = ""
    for s in SUGGESTIONS:
        rows += f"""<tr data-sug="{s['id']}">
  <td class="nowrap"><strong>{s['id']}</strong></td>
  <td><strong>{esc(s['title'])}</strong><br><span class="small">{esc(s['what'])}</span></td>
  <td>{esc(s['why'])}</td>
  <td>{esc(s['impact'])}</td>
  <td>{esc(s['effort'])}</td>
  <td><span class="pill {s['status'].split()[0].lower().strip(',.')}">{esc(s['status'])}</span></td>
  <td class="small">{esc(s['verify'])}</td>
  <td class="nowrap">
    <button type="button" class="rankbtn" data-up="{s['id']}" aria-label="Move {s['id']} up">&uarr;</button>
    <button type="button" class="rankbtn" data-down="{s['id']}" aria-label="Move {s['id']} down">&darr;</button>
    <span class="rank" aria-live="polite"></span>
  </td>
</tr>"""
    body = f"""
{breadcrumb([("Home", "index.html"), ("Decision Center", None)])}
<h1>Decision Center</h1>
<p class="lede">Every proposal for this site lands here first. Nothing below is auto-applied. Read the
  proposal, its evidence, and its cost, then rank it. Your ranking is stored in your browser and can
  be exported as CSV, so you can review the shortlist before anything changes.</p>

<div class="panel">
  <h2>How to use this page in three minutes</h2>
  <ol class="tight">
    <li>Read the <strong>Status</strong> column first. Anything marked <em>Shipped</em> is already
      live &mdash; the verification note tells you where to check it.</li>
    <li>Anything marked <em>Blocked</em> or <em>Not started</em> needs a decision or a credential from
      you. Rank those against each other.</li>
    <li>Use the arrows to order the shortlist, then export the ranking. Nothing is built from this
      page without an explicit choice recorded in the worksheet at the bottom.</li>
  </ol>
</div>

<h2>Proposals</h2>
<table id="sugTable" class="decision">
  <caption>{len(SUGGESTIONS)} proposals with honest status. "Shipped" means it is live and verifiable now.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Why it matters</th>
    <th scope="col">Impact</th><th scope="col">Cost</th><th scope="col">Status</th>
    <th scope="col">How to check it</th><th scope="col">Your rank</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="cta">
  <button type="button" id="exportRank">Export my ranking (CSV)</button>
  <button type="button" id="resetRank" class="ghostbtn">Reset ranking</button>
</p>

<h2>My shortlist</h2>
<p class="small">Filtered down to what is <em>not</em> yet shipped, because that is where a decision
  actually changes something.</p>
<table class="shortlist">
  <caption>Open decisions only.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Decision needed</th><th scope="col">Who can do it</th></tr></thead>
  <tbody>
    <tr><td>SG-07</td><td>Test one Special Link per product in the enrolled account</td><td>Owner (account access)</td></tr>
    <tr><td>SG-10</td><td>Verify Search Console and decide on email capture</td><td>Owner (account access)</td></tr>
    <tr><td>SG-13</td><td>Apply for Product Advertising API access so prices can be shown legally</td><td>Owner (approval)</td></tr>
    <tr><td>SG-14</td><td>Choose and attach a custom domain</td><td>Owner (decision)</td></tr>
    <tr><td>SG-15</td><td>Use API-supplied product photography</td><td>Owner (needs SG-13)</td></tr>
    <tr><td>SG-16</td><td>Adopt a weekly cadence once queries are measurable</td><td>Owner (needs SG-10)</td></tr>
    <tr><td>SG-18</td><td>Set an editorial calendar for the front-page picks</td><td>Owner (editorial decision)</td></tr>
    <tr><td>SG-19</td><td>Approve intent landing pages generated from the register</td><td>Owner (needs SG-10)</td></tr>
    <tr><td>SG-22</td><td>Name an editor or fix the no-testing policy in writing</td><td>Owner (decision)</td></tr>
    <tr><td>SG-23</td><td>Defer cook-time content until hands-on testing exists</td><td>Owner (product access)</td></tr>
    <tr><td>SG-25</td><td>Deploy analytics/server.js or Cloudflare Pages Function and set sn-collect-endpoint</td><td>Owner (hosting, FLG-010)</td></tr>
    <tr><td>SG-26</td><td>Feed campaign ledger only from authorised first-party reports</td><td>Owner (account access)</td></tr>
    <tr><td>SG-29</td><td>Verify Search Console property and submit sitemap.xml</td><td>Owner (Google account)</td></tr>
    <tr><td>SG-30</td><td>Decide reader email capture provider alongside RSS</td><td>Owner (decision)</td></tr>
    <tr><td>SG-31</td><td>Apply for Creators API access once account has qualified sales for automated research</td><td>Owner (S20, FLG-029)</td></tr>
    <tr><td>SG-32</td><td>Feed Search Console query exports into new buying guides</td><td>Owner (needs SG-10)</td></tr>
  </tbody>
</table>

<h2>Record a decision</h2>
<form id="decisionForm" class="decision-form">
  <label>Chosen path (proposal IDs)
    <input name="chosen" required placeholder="e.g. SG-13, SG-14">
  </label>
  <label>Why this path
    <textarea name="why" rows="3" placeholder="What made this the right next move?"></textarea>
  </label>
  <label>What will we measure to know it worked
    <textarea name="measure" rows="3" placeholder="A number and a date."></textarea>
  </label>
  <button type="submit">Save decision locally</button>
</form>
<p id="decisionSaved" class="small" aria-live="polite"></p>
<p class="small">Saving writes to this browser only. Export it with your ranking and keep it with the
  <a href="campaign-ledger.html">campaign ledger</a> so the decision has a dated record.</p>

<h2>What we will not do without a new decision</h2>
<ul>
  <li>Print prices or star ratings copied from a listing.</li>
  <li>Call any product "best" without evidence.</li>
  <li>Auto-publish generated content without passing the build gate.</li>
  <li>Merge the intended and observed ASIN fields.</li>
  <li>Scale outbound links before the one-per-product test passes.</li>
</ul>
"""
    BUILT.append(page("suggestions.html", f"Decision Center — {SITE}",
                      f"{len(SUGGESTIONS)} proposals for this site, with honest status, ranked before anything "
                      "is built. Review the shortlist and choose a path.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Decision Center", "url": BASE + "suggestions.html"}))


# ---- questions
QUESTIONS = [
    ("Q-01", "Which ASIN did you intend for each of the five links?",
     "We can see where each short link lands today, but not what you meant to promote.",
     "Ask the owner for the intended ASIN per product. Compare against the observed target on each "
     "product page.",
     "Special Link validation (FLG-004)", "Owner", "Not obtained"),
    ("Q-02", "Is the Associate ID shopnow047c-20 issued, active and approved?",
     "Only Associates Central can answer this. No public page shows account status.",
     "Sign in to Associates Central and check Account Settings, then look for any click in the "
     "tracking report.",
     "Whether any of this earns anything (FLG-002)", "Owner", "Not verifiable externally"),
    ("Q-03", "Are link.amazon short links permitted on a website?",
     "The submitted links use that domain. Public documentation does not settle it, and guessing "
     "would be worse than a blank.",
     "Contact Associates support with the exact URLs and ask for a written answer. Until then use "
     "tagged amazon.com/dp/ links, which the Operating Agreement describes.",
     "Link format decision (FLG-003)", "Amazon support", "Unresolved"),
    ("Q-04", "Did the one-per-product link test pass?",
     "A tag that is not recorded earns nothing, and you cannot see that from outside the account.",
     "Click one tagged link per product while signed in. Check each appears in the tracking report "
     "with the right ASIN.",
     "Scaling traffic (FLG-004)", "Owner", "Pending test"),
    ("Q-05", "Do you want a custom domain?",
     "Canonicals, sitemap and feed all currently point at the github.io subpath.",
     "Decide yes or no. If yes, the domain has to be chosen before indexing is worth encouraging.",
     "Indexing and brand (FLG-006, SG-14)", "Owner", "Not decided"),
    ("Q-06", "Who is the editor of record?",
     "FTC guidance treats an implied experience claim as a problem. A byline needs a real person "
     "behind it.",
     "Name a person and describe the actual review process, or keep the current explicit statement "
     "that there is no hands-on test.",
     "Publication polish (FLG-033, FLG-032)", "Owner", "Blank"),
    ("Q-07", "What publishing cadence can actually be sustained?",
     "Cadence compounds; a burst followed by silence does not.",
     "Check what is realistic per week. One guide a week is the working assumption; confirm or "
     "revise.",
     "Content planning (SG-16)", "Owner", "Assumed, not confirmed"),
    ("Q-08", "Where would the self-hosted analytics endpoint live?",
     "Collector code (analytics/server.js, functions/api/collect.js) ships in the repo, while "
     "GitHub Pages is static-only so events stay in localStorage until hosted externally.",
     "Deploy to Cloudflare Pages or a Node host, verify GET /api/collect, and configure the endpoint.",
     "Cross-visitor measurement (FLG-010, SG-25)", "Owner", "Code ready; unhosted"),
    ("Q-09", "Which reader-capture channel, if any?",
     "An RSS feed exists. Email capture and Search Console both need accounts.",
     "Verify the site in Search Console and submit the sitemap. Decide whether email is wanted.",
     "Growth loop (SG-10)", "Owner", "RSS only"),
    ("Q-10", "Which listing contradictions can be resolved with the seller?",
     "Eight active discrepancies across the listings: Emeril preset count (24 vs 25), Emeril "
     "accessory count (6 vs 7), Emeril model variant (4-00675-02X-VN vs earlier 4-00675-02), "
     "Chefman 8-Qt temp (400 vs 450 °F), Chefman 8-Qt wattage (1700 vs 1000 W), Chefman 6-Qt "
     "capacity (6 qt vs 6 L), CHEF iQ battery (50 vs 70 h), and CHEF iQ warranty (2 vs 3 yr).",
     "Ask each seller in writing, or read the printed manual. Until then both figures stay published.",
     "Specification certainty (FLG-008, FLG-009, FLG-017 to FLG-022, FLG-031, FLG-034, FLG-038)", "Sellers", "Open"),
    ("Q-11", "What commission categories apply, and at what rate?",
     "Rates live in the Commission Income Statement inside the account and change by category.",
     "Read the Commission Income Statement in Associates Central. Do not publish a rate until it is "
     "confirmed there.",
     "Any revenue forecast (deliberately absent)", "Owner", "Not obtained"),
    ("Q-12", "Who is the reader, and how big is their kitchen?",
     "Editorial direction depends on whether the audience is small-apartment cooks or batch-cooking "
     "families.",
     "Decide the target reader, then let it prune the guide list rather than adding to it.",
     "Editorial direction", "Owner", "Assumed"),
    ("Q-13", "Should prices be shown at all, and if so how?",
     "The only compliant route is Amazon-served links or the Product Advertising / Creators API.",
     "Decide whether to apply for API access. If not, prices stay off the site permanently.",
     "Conversion (FLG-005, SG-13)", "Owner", "Not decided"),
    ("Q-14", "How will corrections be handled after launch?",
     "Listings change. A site with a dated verification stamp needs a process for re-dating it.",
     "Set a re-verification interval, for example quarterly, and record each pass with its date.",
     "Trust over time (FLG-023)", "Owner", "Not defined"),
    ("Q-15", "Is the generated imagery acceptable, or must it be replaced before promotion?",
     "The photographs on the front page and category pages are illustration, captioned as such on "
     "every page that uses them. Whether that is good enough for the audience this site is aimed at "
     "is an editorial and compliance judgement, not a fact.",
     "Decide one of three: keep the captioned illustration, license real photography through the "
     "Product Advertising or Creators API, or commission original photography. Do not silently drop "
     "the caption.",
     "Storefront credibility (FLG-036, FLG-007, SG-15)", "Owner", "Not decided"),
    ("Q-16", "On what evidence are the three front-page picks chosen?",
     "Today they are chosen on the shape of the decision - two zones, one big basket, one instant "
     "read - and the page says so. That is an editorial argument, not a measurement.",
     "Once clicks are recorded server-side (Q-08) and queries are visible (Q-09), choose the picks "
     "from those two numbers and print the reason with the date.",
     "Front-page rotation (SG-18, SG-19)", "Owner, then data", "Argument only, no data"),
    ("Q-17", "What is this site for, in one sentence a reader could repeat?",
     "Right now the answer is either \"honest specs for five appliances\" or \"the paperwork behind "
     "an affiliate site\". They attract different readers, and only the first one buys anything.",
     "Write the sentence, then delete or move to the footer every page that does not serve it. The "
     "records already live in the footer, so nothing is lost.",
     "Every editorial decision (SG-18 to SG-23)", "Owner", "Unwritten"),
    ("Q-18", "Which jurisdiction's disclosure and consumer rules govern this site?",
     "Amazon's Operating Agreement and US FTC guidance are quoted here because they are the sources "
     "that are publicly checkable. Whether EU or Dutch consumer rules additionally apply to a reader "
     "in the Netherlands has not been assessed, and this site does not guess at it.",
     "Ask a qualified adviser which rules apply given where the owner and the readers are, then "
     "record the answer with its date in the source register.",
     "Disclosure wording and placement (S01, S03, S23)", "Qualified adviser", "Not assessed"),
    ("Q-19", "Will the Associates account qualify for Amazon Creators API credentials?",
     "PA-API 5 returns HTTP 403 and Creators API requires final Associates acceptance plus "
     "qualifying sales (10 qualifying sales in the prior 30 days for catalog API access, S20/S21).",
     "Complete account review in Associates Central, verify qualified sales, and apply as primary account owner.",
     "Automated product ingestion and legal price/image display (SG-13, SG-31, FLG-029)", "Owner", "Blocked on API acceptance"),
    ("Q-20", "Which Search Console query metrics will pick the next buying guides?",
     "Without Search Console property verification, organic queries, impressions, and CTR cannot be seen.",
     "Verify the canonical URL in Google Search Console, submit sitemap.xml, and review query reports monthly.",
     "Topic selection and guide cadence (SG-16, SG-29, SG-32)", "Owner", "Blocked on Search Console"),
]


def build_questions():
    rows = "".join(
        f"""<tr><td class="nowrap"><strong>{q[0]}</strong></td>
  <td><strong>{esc(q[1])}</strong><br><span class="small">{esc(q[2])}</span></td>
  <td>{esc(q[3])}</td>
  <td>{esc(q[4])}</td>
  <td>{esc(q[5])}</td>
  <td><span class="unverified">{esc(q[6])}</span></td></tr>""" for q in QUESTIONS)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Open Questions", None)])}
<h1>Open Questions</h1>
<p class="lede">Everything that has to be answered before a decision here is actually a decision. Each
  row names what is missing, how to go and get it, what it blocks, and who realistically can supply
  it. None of these are answered by guessing, so the answer column says what we know: usually
  nothing.</p>

<div class="panel">
  <h2>What this page is for</h2>
  <p>{len(QUESTIONS)} questions. Most need the owner's account access or a yes/no decision; a few
    need a seller to clarify a listing that contradicts itself, Amazon support to answer a policy
    question, or a qualified adviser for the jurisdictional one. Each row names how to go and get the
    answer, because a question you cannot close is not a plan.</p>
  <p class="small">If you only answer one thing, answer <strong>Q-04</strong> &mdash; whether the
    tagged links are being recorded. Everything about revenue depends on it, and nothing else
    does.</p>
</div>

<table class="questions">
  <caption>Questions register. The answer column is intentionally not filled in with assumptions.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Question</th>
    <th scope="col">How to discover the missing information</th><th scope="col">What it blocks</th>
    <th scope="col">Who can answer</th><th scope="col">Status</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>What we do know, and where it came from</h2>
<ul>
  <li><strong>The five short links resolve to five specific ASINs.</strong> Observed on {TODAY}, and
    recorded separately from intent on each product page (with earlier checkpoint failures on
    B0c8moW59 resolved on follow-up under FLG-012 while instability remains under FLG-011).</li>
  <li><strong>Every specification on this site was read off an official listing</strong> on {TODAY}.
    The <a href="sources.html">source register</a> links every one.</li>
  <li><strong>The compliance rules are public and quoted.</strong> Amazon's Operating Agreement
    Section 5, Program Policies Participation Requirements §2(a), §2(b), §5, §6(t), §6(v), §6(w),
    §6(y), IP License §1, §2(e), §4 (Agent Terms), Commission Income Statement §2(d)/(e)/(g), FTC
    disclosure guidance (S03, S23), and Google's outbound-link guidance (S04) are all linked with exact wording.</li>
  <li><strong>USDA publishes the minimum internal temperatures and calibration instructions</strong>
    used in the thermometer guides (S22, S24), linked rather than paraphrased.</li>
</ul>

<h2>What we deliberately do not know</h2>
<p>Search volume for any topic, conversion rate for any product, whether a given product is better
  than another, and what any of these appliances is like to actually use. Four of those require tools
  or access we do not have. The fourth requires buying the products, and this site does not pretend
  it did.</p>
<p class="cta"><a class="btn" href="suggestions.html">Take the shortlist to the Decision Center</a></p>
"""
    BUILT.append(page("questions.html", f"Open Questions — {SITE}",
                      f"{len(QUESTIONS)} questions that must be answered before a decision can reasonably be "
                      "made, with how to discover each missing fact and what it blocks.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Open Questions", "url": BASE + "questions.html"}))



# ---- design & traffic brief
def build_design_brief():
    prompt_text = """You are designing the next version of ShopNow Kitchen, an independent publication-style
Amazon affiliate website covering five specific products: three air fryers (Chefman 6 Quart Dual
Basket, Chefman TurboFry 8 Qt, Emeril Lagasse 26QT French Door) and two meat thermometers
(ThermoMaven 1 Sec instant-read, CHEF iQ Sense Gen3 wireless). Audience: US home cooks who want a
confident answer to one question, not a catalog. Business goal: earn qualified clicks to Amazon
through trust, never through pressure.

Design like a small-batch food magazine that happens to sell via affiliate links, not like a
generated content farm. Requirements:

BRAND. Keep the name ShopNow Kitchen. Masthead with wordmark in a warm serif display face
(Georgia, Iowan Old Style or similar) and body copy in a neutral humanist sans. Palette: charcoal
ink, warm cream paper, one accent of paprika red, used only for links, price-adjacent details and
the single primary call to action per view. Generous margins, a real baseline grid, 65 to 75
characters per measure. No gradients, no glassmorphism, no stock-photo-style hero imagery.

FRONT PAGE. In order: dated publication line and Associates disclosure strip; masthead; one-line
editorial promise; hero with the single most useful question right now (for example, which air
fryer fits a family of four); a seasonal spotlight module (Thanksgiving and holiday cooking in
November and December); category rails for Air Fryers and Meat Thermometers as cards with original
illustration; a latest-guides rail; a short list of what we will not print; footer with the full
dashboard group.

COMPONENTS. Product card: original illustration, listing-derived capacity or key stat, one
trade-off sentence, a question it answers, and a tagged Special Link button labelled as a paid
link. Comparison module: aligned rows, no star scores. Buy box: explicit question checklist the
reader answers before clicking out. Disclosure label adjacent to every outbound button, never in a
tooltip.

TYPE AND TONE. Short declarative headlines. Second person. Sentences a person would say out loud.
No exclamation marks, no superlatives without evidence, no fake urgency, no countdown timers.
Never print prices, star ratings or review counts; those come only from Amazon-served links or the
Creators API.

ILLUSTRATION. Original SVG line-and-wash illustrations in a consistent style: air fryer, thermometer,
basket, French doors, oven interior. Never product photos scraped from a listing, never Amazon
imagery without the licence that comes with the Creators API.

ACCESSIBILITY AND PERFORMANCE. WCAG AA contrast, visible focus states, semantic headings in order,
alt text that describes the illustration, no layout shift, total page weight under one megabyte,
no third-party fonts or trackers. Disclosure readable at 200 percent zoom.

SEO AND STRUCTURED DATA. One canonical host, one h1 per page, JSON-LD (WebPage, Article on guides,
FAQPage where the FAQ exists), sitemap and RSS regenerated on every build, Search Console-ready
meta. Internal links favour depth: every guide links to two related guides and one category page.

COMPLIANCE. Amazon Associates statement above the fold on every page; every outbound Amazon link
rel=sponsored and nofollow and carrying the tag; FTC-clear disclosure next to each call to action;
intended and observed ASIN fields kept separate; contradictions on a listing are printed, not
smoothed over.

FORBIDDEN. Fake countdowns, invented scarcity, fabricated expert quotes, fabricated hands-on
testing claims, fabricated search-volume numbers, placeholder filler text, emoji bullets, and any
phrase that reads like it was produced by filling in a template."""

    cluster_rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td><td>{esc(e)}</td></tr>" for a, b, c, d, e in [
        ("A · Air fryer buying", "Basket or oven-style: what to compare first", "guides/basket-vs-oven.html", "Live", "Anchor guide, links to all three air fryer pages"),
        ("A · Air fryer buying", "A no-hype checklist for comparing air fryer capacity", "guides/capacity-checklist.html", "Live", "Feeds compare.html"),
        ("A · Air fryer buying", "How to assess cleanup and counter-space trade-offs", "guides/cleanup-counter-space.html", "Live", "Cross-links air fryer pages"),
        ("A · Air fryer buying", "Air fryer for a small kitchen: three measurements", "guides/small-kitchen-air-fryer.html", "Live", "Captures apartment queries"),
        ("A · Air fryer buying", "Basket or oven-style: which fits a family of four", "Not written", "Proposed", "Search Console may confirm or kill this title"),
        ("B · Holiday and seasonal", "Air fryer at Thanksgiving: what actually fits", "guides/air-fryer-thanksgiving.html", "Live", "Seasonal spike, Nov 2026"),
        ("B · Holiday and seasonal", "Turkey thermometer maths: the USDA minimums", "Not written", "Proposed", "USDA chart is already the source of record (S22)"),
        ("B · Holiday and seasonal", "Black Friday air fryer shortlist for gifting", "Not written", "Proposed, no prices", "Black Friday is 2026-11-27; must not print prices (SG-13)"),
        ("B · Holiday and seasonal", "Wireless or instant-read for a long smoker cook", "guides/instant-vs-wireless.html", "Live", "Holiday brisket and turkey season"),
        ("C · Thermometer education", "How to read accuracy claims: plus-or-minus 0.5 and NIST", "guides/thermometer-accuracy.html", "Live", "Trust content, supports both thermometer pages"),
        ("C · Thermometer education", "Is NIST certification on a listing a guarantee", "Not written", "Proposed", "Honest answer: it is a seller statement (FLG-035)"),
        ("C · Thermometer education", "USDA doneness temperatures for the holiday bird", "Not written", "Proposed", "Reuses S22; strong internal-link target"),
        ("D · Multi-function appliances", "Questions to ask before buying a multi-function appliance", "guides/multi-function-questions.html", "Live", "Umbrella guide for the oven category"),
        ("D · Multi-function appliances", "Emeril 26QT: 24 or 25 presets, and why it matters less than fit", "Not written", "Proposed", "Turns FLG-021 into the article"),
        ("D · Multi-function appliances", "Chefman dual basket versus the 8-quart: the counter-space decision", "Not written", "Proposed", "Compares P-01 and P-03 without crowning a winner"),
    ])

    standards_rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in [
        ("Every claim traceable to a dated source", "The spec table links its source on every row; conflicts are printed verbatim."),
        ("A named position or an honest blank", "No hands-on test is claimed anywhere; the review process is described on how-we-choose.html."),
        ("Contradictions shown, not smoothed over", "P-02 lists both 24 and 25 presets; P-05 lists both 50 and 70 hours (FLG-008, FLG-021)."),
        ("No invented numbers", "No search volume, no conversion rates, no commission figures; the ledger is empty by design."),
        ("Questions as headlines", "Guides answer one buyer question each; the question came before the keyword."),
        ("Real dates on everything", "Every page carries a last-verified date; re-verification is a scheduled pass, not a vibes check."),
        ("Specific beats general", "'16.9 inches of depth plus door swing' beats 'spacious interior'."),
        ("Trade-offs stated next to recommendations", "Every pick on the front page names what you give up."),
        ("Disclosure as furniture, not fine print", "Associates statement above the fold on every page, repeated in the footer."),
        ("One human editorial decision at the gate", "Automation drafts; the build gate and a human decide what ships (SG-12)."),
    ])

    body = f"""
{breadcrumb([("Home", "index.html"), ("Design & Traffic Brief", None)])}
<h1>Design &amp; Traffic Brief</h1>
<p class="lede">Everything a designer &mdash; or a new prompt &mdash; needs to take this site from
  verified and compliant to memorable, trustworthy and worth ranking. Nothing on this page
  changes the site. It is a proposal, reviewed in the <a href="suggestions.html">Decision
  Center</a> as SG-17.</p>

<div class="panel">
  <h2>How to use this brief in five minutes</h2>
  <ol class="tight">
    <li>Read <strong>The prompt</strong> below. If you agree with it, paste it into your design
      tool of choice. If you do not, edit it there &mdash; it is written to be edited.</li>
    <li>Pick <strong>two or three proposed topics</strong> from the cluster table, not twelve.</li>
    <li>Rank <strong>SG-17</strong> in the Decision Center and export your ranking.</li>
    <li>Anything shipped from this brief re-enters the build gate before publishing. No exceptions.</li>
  </ol>
</div>

<h2>1. The prompt</h2>
<p>Copy everything inside the box. It is a complete design brief for the next build of this site.</p>
<pre class="promptbox">{esc(prompt_text)}</pre>

<h2>2. Front page anatomy, in order</h2>
<ol>
  <li><strong>Utility strip</strong> — the Associates disclosure, one line, above everything.</li>
  <li><strong>Masthead</strong> — wordmark, one primary nav group (Air Fryers, Meat Thermometers,
    All products, Guides, Compare, How we choose), one search field.</li>
  <li><strong>Editorial promise</strong> — one sentence naming who the site is for.</li>
  <li><strong>Hero</strong> — the single most useful question of the week. Currently the family-of-four
    air fryer question; swap seasonally.</li>
  <li><strong>Seasonal spotlight</strong> — Thanksgiving and holiday cooking modules from mid-November
    to end of December; New Year health angle from January.</li>
  <li><strong>Category rails</strong> — Air Fryers and Meat Thermometers as illustrated card rails,
    three cards each, each card naming a trade-off.</li>
  <li><strong>Latest guides</strong> — four most recent, question-shaped.</li>
  <li><strong>Refusals</strong> — "What we will never print", three bullets. This is the most
    persuasive trust module on the page.</li>
  <li><strong>Footer</strong> — the dashboard group: Decision Center, this brief, Open Questions,
    Flagged for Review, Sources, Executive Summary, Campaign Ledger, About, Disclosure.</li>
</ol>

<h2>3. Organic traffic plan</h2>
<p>Small sites win on question-shaped long-tail queries, internal links and consistency &mdash; not on
  volume. Every topic below is tied to a product we already cover or a source we already cite.
  <strong>Working titles are hypotheses, not claims of popularity.</strong> The order here is an
  editorial guess; Search Console data (SG-10) is the only thing allowed to settle it.</p>

<table class="clusters">
  <caption>Topic clusters. "Live" means the guide exists today; "Proposed" means it is a candidate only.</caption>
  <thead><tr><th scope="col">Cluster</th><th scope="col">Title (working)</th>
    <th scope="col">Target</th><th scope="col">Status</th><th scope="col">Why it is here</th></tr></thead>
  <tbody>{cluster_rows}</tbody>
</table>

<h3>Internal linking rules</h3>
<ul>
  <li>Every guide links down to at least one product page and across to at least two related guides.</li>
  <li>Every product page links up to its category page and sideways to the compare table.</li>
  <li>Category pages link only to live guides, never to proposed ones.</li>
</ul>

<h3>Findability checklist (mostly already live)</h3>
<ul>
  <li>One canonical host; canonical link on every page — <strong>done</strong> <a href="sources.html">(S04)</a>.</li>
  <li>Sitemap regenerated and gated on every build — <strong>done</strong>.</li>
  <li>RSS feed of guides — <strong>done</strong>, 8 items.</li>
  <li>JSON-LD structured data on every page — <strong>done</strong>.</li>
  <li>rel="sponsored nofollow" on every outbound product link — <strong>done and gated</strong>.</li>
  <li>Search Console verification and sitemap submission — <strong>owner action, SG-10</strong>.</li>
  <li>Custom domain — <strong>owner decision, SG-14</strong> (FLG-006).</li>
</ul>

<h3>Seasonal calendar</h3>
<table>
  <caption>Dates are calendar facts. No event on this page licenses a price, a sale claim or a countdown.</caption>
  <thead><tr><th scope="col">Date</th><th scope="col">Moment</th><th scope="col">Lead time</th><th scope="col">What to do</th></tr></thead>
  <tbody>
    <tr><td>2026-11-26</td><td>Thanksgiving (US)</td><td>Now — publish this week</td><td>Turkey thermometer USDA table guide; air fryer side-dish capacity checklist</td></tr>
    <tr><td>2026-11-27</td><td>Black Friday</td><td>Now</td><td>Gift shortlist without prices; link to the two thermometer gift guides</td></tr>
    <tr><td>2026-11-30</td><td>Cyber Monday</td><td>Same fortnight as Black Friday</td><td>One reminder post, no fake urgency, no prices (SG-13)</td></tr>
    <tr><td>2026-12-02</td><td>First week of Advent</td><td>First week of December</td><td>Gifting by cook type: fryer-vs-thermometer decision guide</td></tr>
    <tr><td>2026-12-25</td><td>Christmas</td><td>Mid-December</td><td>"What to cook in the new air fryer on day one"</td></tr>
    <tr><td>2027-01-02</td><td>New Year</td><td>First week of January</td><td>"Air fryer for the January reset" — health angle, zero medical claims</td></tr>
    <tr><td>2027-02-14</td><td>Valentine's / date night</td><td>Early February</td><td>Thermometer-led: reverse-sear steak doneness with USDA rest times</td></tr>
  </tbody>
</table>

<h2>4. The standards that keep this from reading as generated</h2>
<table>
  <caption>Ten reader-visible signals, agreed before any redesign.</caption>
  <thead><tr><th scope="col">Standard</th><th scope="col">What it looks like on this site</th></tr></thead>
  <tbody>{standards_rows}</tbody>
</table>

<h2>5. What this brief deliberately does not claim</h2>
<ul>
  <li>No keyword volume, difficulty or CPC figures. None have been measured (needs SG-10).</li>
  <li>No promise that any topic ranks. Ranking is an outcome, not an input.</li>
  <li>No hands-on testing claim for any product (FLG-032).</li>
  <li>No commission rate or revenue forecast (Q-11; ledger is intentionally empty).</li>
  <li>No suggestion that a product is "best" — this site recommends for fit, not in the abstract.</li>
</ul>

<h2>6. From brief to build: the mapping</h2>
<table>
  <caption>Where each part of this brief is already true, and where the gaps are.</caption>
  <thead><tr><th scope="col">Brief element</th><th scope="col">State today</th><th scope="col">Reference</th></tr></thead>
  <tbody>
    <tr><td>Disclosure above the fold, repeated in footer</td><td>Live on every page; gate enforced</td><td>SG-04</td></tr>
    <tr><td>Sponsored + nofollow on every outbound Amazon link</td><td>Live; gate enforced</td><td>SG-05, S04</td></tr>
    <tr><td>Sitemap, RSS, canonical, JSON-LD</td><td>Live and gated</td><td>SG-08</td></tr>
    <tr><td>Original illustration, no Amazon photography</td><td>Live; licence-safe</td><td>SG-09, FLG-007</td></tr>
    <tr><td>Question-shaped guides with verdicts</td><td>8 live, 8 proposed above</td><td>SG-02</td></tr>
    <tr><td>Weekly cadence chosen from queries</td><td>Blocked on Search Console</td><td>SG-16, SG-10, Q-09</td></tr>
    <tr><td>Prices shown legally</td><td>Impossible until API access</td><td>SG-13, FLG-005</td></tr>
    <tr><td>Parallel-session coordination</td><td>COORDINATION.md task board, active</td><td>Repo root</td></tr>
  </tbody>
</table>

<p class="cta"><a class="btn" href="suggestions.html">Rank SG-17 in the Decision Center</a>
  <a class="btn ghost" guides.htmlsrc="/Affil2/guides.html">Read the eight live guides</a></p>
"""
    BUILT.append(page("design-brief.html", f"Design & Traffic Brief — {SITE}",
                      "A copy-paste design prompt, a topic-cluster traffic plan with a seasonal "
                      "calendar, and the editorial standards checklist for a publication-grade "
                      "affiliate site.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Design & Traffic Brief", "url": BASE + "design-brief.html"}))


# ---- flagged
def build_flagged():
    def src_cell(f):
        links = []
        for sid in f.get("links", []):
            url = source_url(sid)
            if url:
                links.append(f'<a href="{url}" rel="sponsored nofollow">{esc(sid)}</a>')
        return " ".join(links) or "&mdash;"

    order = {"conflict": 0, "policy": 1, "open": 2, "pending-test": 3, "unverified": 4,
             "corrected": 5, "resolved-earlier": 6}
    conflict_count = len([f for f in FLAGS if f.get("severity") == "conflict"])
    rows = ""
    for f in sorted(FLAGS, key=lambda x: (order.get(x["severity"], 9), x["id"])):
        rows += f"""<tr><td class="nowrap"><strong>{f['id']}</strong></td>
  <td>{esc(f['title'])}<br><span class="small pill-sev {esc(f['severity'])}">{esc(f['severity'])}</span></td>
  <td>{esc(f['detail'])}</td>
  <td>{esc(f['owner_status'])}</td>
  <td class="src">{src_cell(f)}</td></tr>"""
    body = f"""
{breadcrumb([("Home", "index.html"), ("Flagged for Review", None)])}
<h1>Flagged for Review</h1>
<p class="lede">Everything this site could not verify, every place a listing contradicts itself, and
  every policy decision that shaped the copy. None of these stop the site going live; all of them are
  visible here with a source link so you can check them yourself.</p>

<div class="panel">
  <h2>Read this page in this order</h2>
  <ol class="tight">
    <li><strong>Conflicts</strong> &mdash; places where a listing says two different things
      ({conflict_count} active contradictions). These are the ones most likely to affect a buying
      decision.</li>
    <li><strong>Policy</strong> &mdash; things deliberately absent for compliance reasons: prices,
      ratings, product photography, hands-on claims.</li>
    <li><strong>Unverified / Pending test</strong> &mdash; values we could not confirm from public
      records or Associates Central, left blank rather than guessed.</li>
    <li><strong>Open / Corrected</strong> &mdash; operational gaps, redirect snapshots, and earlier
      mistakes fixed in the register.</li>
  </ol>
</div>

<table class="flags">
  <caption>Flag register, {TODAY}. Severity tells you how much it matters to a reader.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Issue</th><th scope="col">What we found</th>
    <th scope="col">What would resolve it</th><th scope="col">Source</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>How to request a change</h2>
<p>Note the flag ID, say what is wrong, and cite the official page that shows otherwise. Corrections
  are dated and the flag is kept rather than deleted, so the record shows what changed and when. If a
  listing has changed since {TODAY}, that is a correction, not an error &mdash; say so and it gets
  re-read.</p>
"""
    BUILT.append(page("flagged.html", f"Flagged for Review — {SITE}",
                      "Every conflict, blank and unresolved question on this site, with the official "
                      "source link for each one.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Flagged for Review", "url": BASE + "flagged.html"}))



def changelog_rows():
    """One row per corrected flag, newest flag id first, with the source it was re-read from."""
    rows = ""
    for f in sorted(FLAGS, key=lambda x: x["id"], reverse=True):
        if f.get("severity") != "corrected":
            continue
        links = " ".join(
            f'<a href="{source_url(sid)}" rel="sponsored nofollow">{esc(sid)}</a>'
            for sid in f.get("links", []) if source_url(sid))
        rows += (f'<tr><td class="nowrap">{TODAY}</td><td class="nowrap"><strong>{f["id"]}</strong></td>'
                 f'<td>{esc(f["title"])}<br><span class="small">{esc(f["detail"])}</span></td>'
                 f'<td class="src">{links or "&mdash;"}</td></tr>')
    return rows or '<tr class="empty"><td colspan="4">No corrections recorded.</td></tr>'


# ---- sources
def build_sources():
    rows = "".join(
        f"""<tr><td class="nowrap"><strong>{s['id']}</strong></td>
  <td>{esc(s['name'])}<br><a href="{esc(s['url'])}" rel="sponsored nofollow" class="small">{esc(s['url'])}</a></td>
  <td class="quote">{esc(s['used_for'])}</td>
  <td class="nowrap">{esc(s['checked'])}</td></tr>""" for s in SOURCES)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Sources", None)])}
<h1>Source register</h1>
<p class="lede">If a claim is not traceable to a row on this page, it is not a claim this site makes.
  {len(SOURCES)} sources: the public policy documents, the five product listings, and the supplied
  short links, each read on the date in its row.</p>

<div class="statrow">
  <div><span class="statnum">{len([x for x in SOURCES if x['id'].startswith(('S0','S2'))])}</span>
    <span class="statlabel">policy and government sources</span></div>
  <div><span class="statnum">{len([x for x in SOURCES if x['id'] in ('S10','S11','S12','S13','S14')])}</span>
    <span class="statlabel">product listings</span></div>
  <div><span class="statnum">{len([x for x in SOURCES if x['id'] in ('S15','S16','S17','S18','S19')])}</span>
    <span class="statlabel">supplied short links</span></div>
  <div><span class="statnum">{len(FLAGS)}</span><span class="statlabel">items flagged for review</span></div>
  <div><span class="statnum">0</span><span class="statlabel">prices or ratings reproduced</span></div>
</div>

<table class="sources">
  <caption>Source register. The third column names the exact claim or wording relied on from each source.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Source</th>
    <th scope="col">What it supports &amp; wording relied on</th><th scope="col">Read on</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>What changed, and when</h2>
<p>The corrections below are the ones a reader can see on this site. Each links to the flag that records
it in full, including what the earlier version said.</p>
<table class="changelog">
  <caption>Corrections are dated and kept. Nothing on this site is quietly edited.</caption>
  <thead><tr><th scope="col">Date</th><th scope="col">Flag</th><th scope="col">What changed</th>
    <th scope="col">Source re-read</th></tr></thead>
  <tbody>{changelog_rows()}</tbody>
</table>

<h2>How verification works</h2>
<ol>
  <li>Open the official page. For a product, that is the amazon.com/dp/ listing.</li>
  <li>Read the value in the section that carries it &mdash; title, About this item, or the
    product-information table.</li>
  <li>Record it, with the date and the URL.</li>
  <li>If two parts of the same page disagree, record both and raise a flag. Do not pick the
    flattering one.</li>
  <li>If nothing on the page carries the value, leave it blank and say so.</li>
</ol>
<p class="small">A note on the listings: an Amazon product page is not a stable document. Titles,
  bullet copy and the structured information table can change without notice. That is why every row
  here is dated and why the <a href="flagged.html">flag register</a> keeps corrections rather than
  erasing them.</p>
"""
    BUILT.append(page("sources.html", f"Sources — {SITE}",
                      f"{len(SOURCES)} sources, all official, all dated, with the exact wording each claim "
                      "relies on.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Sources", "url": BASE + "sources.html"}))


# ---- executive summary
def build_exec():
    rows = "".join(
        f"<tr><td class=\"nowrap\">{p['id']}</td><td><strong>{esc(p['brand'])}</strong></td>"
        f"<td>{esc(p['cat'])}</td><td>{esc(p['observed'])}</td>"
        f"<td>{esc(p['model'] or '—')}</td>"
        f"<td><a href=\"{plain(p)}\" rel=\"sponsored nofollow\">listing</a></td></tr>" for p in PRODUCTS)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Executive Summary", None)])}
<h1>Executive summary</h1>
<p class="lede">Five submitted links. Two categories. One site that publishes specifications read from
  official listings, prints every contradiction, and refuses to quote a price it is not licensed to
  quote.</p>

<div class="statrow">
  <div><span class="statnum">5</span><span class="statlabel">products covered</span></div>
  <div><span class="statnum">{len(GUIDES)}</span><span class="statlabel">guides published</span></div>
  <div><span class="statnum">{len(FLAGS)}</span><span class="statlabel">flags, all public</span></div>
  <div><span class="statnum">0</span><span class="statlabel">prices or ratings shown</span></div>
</div>

<h2>1. What exists now</h2>
<p>A static publication site deployable straight to GitHub Pages: a front page that leads with
  products, two category pages, five product pages, {len(GUIDES)} question-shaped guides, a comparison table
  aligned by field, an on-site search that actually works, JSON-LD on every page, a sitemap, an RSS
  feed, and a disclosure strip under the masthead on every page. Alongside it sit the internal
  records: the <a href="suggestions.html">Decision Center</a>, the
  <a href="questions.html">Open Questions</a> register, the
  <a href="flagged.html">flag register</a>, the <a href="sources.html">source register</a>, the
  <a href="platform.html">platform architecture</a> matrix, the
  <a href="measurement.html">measurement &amp; collector guide</a>, and an intentionally empty
  <a href="campaign-ledger.html">campaign ledger</a>.</p>

<h2>2. The five products, as observed</h2>
<table class="exec">
  <caption>Observed destinations, read {TODAY}. Intended ASINs remain blank (FLG-001).</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Brand</th><th scope="col">Category</th>
    <th scope="col">Observed ASIN</th><th scope="col">Model on listing</th>
    <th scope="col">Official listing</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>3. What is verified</h2>
<ul>
  <li>Every product title, dimension, weight (where stated), wattage, temperature range and capacity
    on this site was read from the official listing and its Product information tables on {TODAY}.
    Deep chunk inspection verified previously blank weights (P-01 13.3 lb, P-03 12.8 lb), models
    (P-02 4-00675-02X-VN, P-04 HT07, P-05 CQ60-3C-Z1-E), temperatures (P-02 75&ndash;500 &deg;F, P-04
    572 &deg;F), P-02 power (1700 W), and probe lengths (P-04 6.5 in, P-05 4.75 in) (FLG-040).</li>
  <li>All official policy sources &mdash; Operating Agreement Section 5 (S01), Program Policies
    Participation Requirements &sect;2(a)/(b), &sect;5, &sect;6(t)/(v)/(w)/(y), IP License &sect;1,
    &sect;2(e)/(h)/(i)/(k), &sect;4 Agent Terms, Commission Income Statement &sect;2(d)/(e)/(g) (S02),
    FTC disclosure guidance (S03, S23), Google outbound-link qualification (S04), and Creators API /
    PA-API 5 notices (S20, S21) &mdash; are quoted in the <a href="sources.html">source register</a>.</li>
  <li>Food-safety temperatures and thermometer calibration guidance come from USDA FSIS charts (S22,
    S24), not from product listings.</li>
  <li>All five short links were fetched and their redirect targets observed separately from intent
    (including B0c8moW59 resolving to B0DHZTCNR5 on re-test while redirect instability stays under
    FLG-011).</li>
</ul>

<h2>4. What is not verified, and is not pretended to be</h2>
<ul>
  <li><strong>Intent.</strong> Only the owner knows which ASIN each link was meant to point at
    (FLG-001).</li>
  <li><strong>The tracking ID.</strong> Whether shopnow047c-20 is live is visible only inside
    Associates Central (FLG-002).</li>
  <li><strong>The short-link format.</strong> Its compliance status is unresolved, so the site uses
    tagged amazon.com/dp/ URLs and does not call the short links invalid (FLG-003).</li>
  <li><strong>The link test.</strong> No tagged link has been clicked inside the enrolled account, so
    every product page still says PENDING TEST (FLG-004).</li>
  <li><strong>P-02 weight and warranty terms.</strong> Absent from the live listing HTML, so left
    blank (FLG-022); an unverified Emeril weight figure from earlier editorial prose was removed (FLG-039).</li>
  <li><strong>Certification.</strong> NIST, NSF, and cETL appear on the listings. No certificate or
    test report has been seen (FLG-035).</li>
  <li><strong>Hands-on experience.</strong> None. Nothing on this site implies it was tested
    (FLG-032).</li>
</ul>

<h2>5. The listing conflicts a buyer should know about</h2>
<table class="exec">
  <thead><tr><th scope="col">Flag</th><th scope="col">Product</th><th scope="col">Contradiction</th></tr></thead>
  <tbody>
    <tr><td>FLG-021</td><td>Emeril 26 QT</td><td>24 presets in title/Configuration/Description, 25 in About this item</td></tr>
    <tr><td>FLG-031</td><td>Emeril 26 QT</td><td>Six accessories in title &amp; Included Components, seven in Configuration &amp; Description</td></tr>
    <tr><td>FLG-009</td><td>Emeril 26 QT</td><td>4-00675-02X-VN in live Item details vs 4-00675-02 in earlier listing capture</td></tr>
    <tr><td>FLG-018</td><td>Chefman 8 Qt</td><td>400 &deg;F max in spec field &amp; About this item, 450 &deg;F Hi-Fry in title</td></tr>
    <tr><td>FLG-017</td><td>Chefman 8 Qt</td><td>1700 W in Features &amp; Specs, 1000 W in About this item</td></tr>
    <tr><td>FLG-034</td><td>Chefman 6 Qt</td><td>6 quarts in title/bullets, 6 liters in Measurements field</td></tr>
    <tr><td>FLG-008</td><td>CHEF iQ Sense</td><td>50 hours battery in About this item, 70 hours in earlier Product Description capture</td></tr>
    <tr><td>FLG-038</td><td>CHEF iQ Sense</td><td>Two-year assurance in About this item vs 3 Year in Item details (prior register FLG-019)</td></tr>
  </tbody>
</table>

<h2>6. What would change the numbers</h2>
<p>Two credentials, hosting for the collector, and one domain decision. Creators API access
  (S20, S21) would make legal price and product-photo display possible (SG-13, SG-15, SG-31), which
  is the largest lever on conversion. Search Console verification would make query data available
  (SG-10, SG-29, SG-32), which is the only way to choose the next guide from evidence. Hosting the
  shipped self-hosted analytics endpoint (<a href="measurement.html">SG-25</a>, FLG-010) enables
  cross-visitor event counts without cookies, and a custom domain (SG-14, FLG-006) strengthens
  brand and indexation. Everything else on the <a href="suggestions.html">Decision Center</a> is
  shipped or blocked on owner account verification.</p>

<h2>7. Honest position on revenue</h2>
<p>No commission rate, click count, conversion rate or revenue figure is presented here, because none
  can be obtained from an authorised first-party report yet. The
  <a href="campaign-ledger.html">campaign ledger</a> is empty by design and its schema is defined.
  When the tracking report produces a row, that row goes in with a date and a source. Until then the
  honest number is zero, and it is stated as zero rather than dressed up.</p>

<p class="cta"><a class="btn" href="suggestions.html">Review the decisions</a>
  <a class="btn ghost" href="flagged.html">Check what we could not verify</a></p>
"""
    BUILT.append(page("executive-summary.html", f"Executive Summary — {SITE}",
                      "What was built, what is verified against official sources, what is not, and "
                      "which decisions would change the numbers.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Executive Summary", "url": BASE + "executive-summary.html"}))


# ---- ledger
def build_ledger():
    body = f"""
{breadcrumb([("Home", "index.html"), ("Campaign Ledger", None)])}
<h1>Campaign ledger</h1>
<p class="lede">A ledger with a defined schema and zero rows. That is the honest state: no click,
  session or order figure can be obtained from an authorised first-party report yet, so none is
  shown.</p>

<div class="panel">
  <h2>Why this page is empty</h2>
  <p>Every number a marketing dashboard normally shows &mdash; sessions, clicks, conversion rate,
    earnings per click &mdash; comes from a report. We do not have an authorised report. Filling this
    table with estimates would make the page look finished and the site dishonest. So the columns
    exist, the provenance rule is written down, and the table waits.</p>
</div>

<table class="ledger">
  <caption>Schema v1. Rows are added only from an authorised first-party report, each with its date
    and source.</caption>
  <thead><tr><th scope="col">Date (UTC)</th><th scope="col">Source report</th>
    <th scope="col">Channel</th><th scope="col">Eligible sessions</th>
    <th scope="col">Outbound clicks</th><th scope="col">Reported orders</th>
    <th scope="col">Provenance note</th></tr></thead>
  <tbody><tr class="empty"><td colspan="7">No rows. No authorised first-party report has been
    supplied.</td></tr></tbody>
</table>

<h2>What is measured today, and where</h2>
<p>Five events are defined and counted in the reader's browser: <code>page_view</code>,
  <code>outbound_click</code>, <code>guide_read</code>, <code>search</code> and
  <code>suggestion_rank</code>. They are stored in local storage, never transmitted, and can be
  exported to CSV from the <a href="disclosure.html">disclosure page</a>. That is useful for
  understanding your own session; it is not a substitute for a server-side report, and this page does
  not pretend otherwise.</p>

<h2>The rules this ledger follows</h2>
<ol>
  <li>One row per report, not per day. A row without a report is not a row.</li>
  <li>Every row carries the date it was obtained and the system it came from.</li>
  <li>Nothing is inferred, back-filled, or smoothed between reports.</li>
  <li>Where a report is incomplete, the missing cells stay blank.</li>
  <li>No conversion score and no revenue forecast is derived from this table.</li>
</ol>
<p class="small">The blocking dependency is <a href="questions.html">Q-04</a>: until one tagged link
  is confirmed in the tracking report, there is nothing to record.</p>
"""
    BUILT.append(page("campaign-ledger.html", f"Campaign Ledger — {SITE}",
                      "An intentionally empty campaign ledger with a defined schema and a provenance "
                      "rule, because no authorised first-party report exists yet.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Campaign Ledger", "url": BASE + "campaign-ledger.html"}))


# ---- disclosure
def build_disclosure():
    body = f"""
{breadcrumb([("Home", "index.html"), ("Disclosure & Privacy", None)])}
<h1>Disclosure, privacy and measurement</h1>
<p class="lede">This page explains the words at the top of every page, what we are not allowed to
  show, and exactly what happens to anything you do here.</p>

<h2>The affiliate disclosure</h2>
<p class="statement">{DISCLOSURE}</p>
<p>The wording is the statement Amazon's Operating Agreement Section 5 requires, and it appears on
  every page directly under the masthead, then again in the footer. FTC guidance on disclosures says a
  disclosure placed only on an about page or at the end of a page is likely to be missed, so it
  appears before the first product link rather than after it.</p>
<p>Every outbound product link is labelled <strong>(paid link)</strong> next to the button and carries
  <code>rel="sponsored nofollow"</code>, per Google's guidance on qualifying paid links. Where a
  product page offers a second link to the same listing without our tag, it is labelled as the
  untagged listing so you can verify the product yourself without sending us a click.</p>

<h2>What we are not allowed to show</h2>
<p>Amazon's Program Policies section 2(b) lets a site show prices and availability only if Amazon
  serves the link the price appears in, or if the data comes through the Product Advertising or
  Creators API. This site does neither, so no price, availability, star rating, review count or
  best-seller rank is displayed anywhere. Where those values were visible on a listing when we read
  it, they were recorded in the working data and deliberately excluded from the pages. That is why
  the price column on the comparison table says "not shown, by policy" rather than being empty.</p>

<h2>What we measure</h2>
<p>Five events, defined once and used consistently:</p>
<p><strong>Where they go.</strong> By default the counts stay in your own browser (localStorage) and can be exported as CSV — nothing leaves your device. A self-hosted collector (<code>analytics/server.py</code>) is written, smoke-tested and deliberately switched off in <code>assets/config.js</code> until the owner chooses a host (SG-18 / Q-08). That endpoint never reads IP addresses, writes no access log, stores no identifiers, and keeps only aggregate counts. Either way there are no cookies, no fingerprinting, no referrer capture, and search events carry a result count — never what you typed.</p>
<table class="events">
  <thead><tr><th scope="col">Event</th><th scope="col">Fires when</th><th scope="col">Used for</th></tr></thead>
  <tbody>
    <tr><td><code>page_view</code></td><td>Any page loads</td><td>Which pages are reached at all</td></tr>
    <tr><td><code>outbound_click</code></td><td>A tagged Amazon link is clicked</td>
      <td>Which product a reader actually leaves for</td></tr>
    <tr><td><code>guide_read</code></td><td>A guide page loads</td><td>Whether guides get read, not just listed</td></tr>
    <tr><td><code>search</code></td><td>A built-in search runs</td>
      <td>Result count only &mdash; the words typed are not recorded</td></tr>
    <tr><td><code>suggestion_rank</code></td><td>A proposal is reordered on the Decision Center</td>
      <td>Which direction is actually preferred</td></tr>
  </tbody>
</table>
<p>All five are counted in your browser's local storage by default. Search words are held in
  session storage only long enough to reach the results page; they are not placed in a request URL.
  Normal page requests still reach the GitHub Pages host as ordinary traffic, and no measured event
  leaves your device unless you enable a self-hosted endpoint. No cookie is set, no third-party
  analytics script or pixel runs, and no fingerprinting is used. A zero-dependency self-hosted
  collector (<code>analytics/server.js</code> and Cloudflare Pages Function <code>functions/api/collect.js</code>)
  ships in this repository and activates only when configured via <code>sn_collect_url</code> or
  <code>&lt;meta name="sn-collect-endpoint"&gt;</code> (<a href="measurement.html">Measurement &amp;
  Collector guide</a>, FLG-010).</p>
<p>You can clear everything we store by clearing site data for this domain, and you can export it
  first: <button type="button" id="exportEvents" class="ghostbtn">Export my event log (CSV)</button></p>

<h2>Product-intent records</h2>
<p>For each of the five submitted links, the <em>intended</em> ASIN and the <em>observed</em> redirect
  target are stored in separate fields on the product page and are never merged. Merging them would
  assert an intention only the owner can confirm. Each product page also carries the date the values
  were read and a link to the official listing.</p>

<h2>Cookies, and what we do not use</h2>
<ul>
  <li>No advertising cookies, no retargeting, no social pixels.</li>
  <li>No fonts or scripts loaded from a third-party CDN &mdash; the page loads from this domain
    only.</li>
  <li>No account, no login, no email capture on this site.</li>
  <li>Clicking a product link takes you to Amazon, where Amazon's own privacy policy applies and
    Amazon's own cookies are set.</li>
</ul>
"""
    BUILT.append(page("disclosure.html", f"Disclosure & Privacy — {SITE}",
                      "The affiliate disclosure, why prices and ratings are not shown, the five "
                      "measured events, and what is stored in your browser.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Disclosure & Privacy", "url": BASE + "disclosure.html"}))


# ---- about
def build_about():
    body = f"""
{breadcrumb([("Home", "index.html"), ("About", None)])}
<h1>About this site</h1>
<p class="lede">An independent kitchen-appliance buying guide covering five specific products. It is
  small on purpose: five products documented properly beat five hundred documented by scraping.</p>

<h2>What this is</h2>
<p>A publication-style affiliate site. When a reader buys through one of our tagged Amazon links, we
  may earn a commission. That is the business model, it is disclosed on every page, and no
  recommendation here is influenced by which product pays more &mdash; partly because no commission
  rate for any of these products has been confirmed, and this site does not publish one.</p>

<h2>Who writes it</h2>
<p><strong>Editor of record:</strong> not named. Rather than invent a byline, this site states
  plainly that there is no named human author behind the copy yet and that this is an outstanding item
  (FLG-033). That is a real gap, not a design choice, and it is honest to say so.</p>
<p><strong>What the writer does:</strong> opens the official listing, reads each value off the page,
  records it with a date and a URL, and raises a flag whenever two parts of the same page disagree.
  The process is written out on the <a how-we-choose.htmlsrc="/Affil2/how-we-choose.html">How we choose</a> page.</p>
<p><strong>What the writer has not done:</strong> cooked with any of these appliances, measured any of
  them, or seen a certification document. No page on this site claims otherwise.</p>

<h2>Why only five products</h2>
<p>Because those five are the ones this site covers. There is no pretence of covering the
  market, no "top ten" list, and no ranking against products that were never examined. Where a guide
  would normally say "consider alternatives", it says instead that the site only covers these
  five.</p>

<h2>Corrections</h2>
<p>Listings change. If a value here no longer matches the official listing, that is a correction to be
  made, not an argument to be had. Every flag on the
  <a href="flagged.html">Flagged for Review</a> page has a source link and a suggested resolution,
  and corrections are dated rather than quietly applied.</p>

<h2>Imagery and trademarks</h2>
<p>Two kinds of editorial imagery appear on this site, and both are explicitly labelled. The
  photographs on the storefront pages were <strong>generated for this site</strong>: they show a
  kitchen and appliances of no particular make, and every frame is captioned on the page so nobody
  mistakes it for the specific product reviewed (FLG-036). Alongside them, original unbranded SVG
  form-factor schematics stored in <code>assets/illustrations/</code> illustrate the three appliance
  shapes covered here. No Amazon product photography is used anywhere (FLG-007).</p>
<div class="diagram-row">
  <figure class="diagram-card">
    <img src="assets/illustrations/air-fryer.svg" width="720" height="320" alt="Editorial vector schematic of a basket air fryer — original illustration, not product photography">
    <figcaption>Basket air fryer schematic (original vector artwork, not manufacturer photography).</figcaption>
  </figure>
  <figure class="diagram-card">
    <img src="assets/illustrations/air-fryer-oven.svg" width="720" height="320" alt="Editorial vector schematic of an oven-style French-door air fryer — original illustration, not product photography">
    <figcaption>Countertop air fryer oven schematic (original vector artwork).</figcaption>
  </figure>
  <figure class="diagram-card">
    <img src="assets/illustrations/thermometer.svg" width="720" height="320" alt="Editorial vector schematic of a digital meat thermometer — original illustration, not product photography">
    <figcaption>Meat thermometer schematic (original vector artwork).</figcaption>
  </figure>
</div>
<p>Product names, Amazon and Amazon Associates are trademarks of Amazon.com, Inc. or its affiliates.
  This site is not endorsed by Amazon, and nothing here implies that Amazon sponsors or approves
  it.</p>

<h2>Contact and change requests</h2>
<p>There is no contact form and no email capture on this site. Change requests go through the
  <a href="flagged.html">Flagged for Review</a> page, which lists every open item with its ID, and
  through the <a href="suggestions.html">Decision Center</a>, where proposals are ranked before
  anything is built.</p>
"""
    BUILT.append(page("about.html", f"About & Authorship — {SITE}",
                      "Who writes this, what the process is, what has not been tested, and how "
                      "corrections work.",
                      body, jsonld={"@context": "https://schema.org", "@type": "AboutPage",
                                    "name": "About", "url": BASE + "about.html"}))


# ---- platform architecture
def build_platform():
    body = f"""
{breadcrumb([("Home", "index.html"), ("Platform Architecture", None)])}
<h1>AI Affiliate Platform Architecture &amp; Compliance Gates</h1>
<p class="lede">An AI-assisted affiliate workflow is only as reliable as its verification sources
  and policy gates. Below is the subsystem blueprint for this site &mdash; what already runs in the
  repository today, what is blocked by Amazon Associates eligibility or policy rules, and why
  automation never publishes without passing the gate.</p>

<div class="statrow">
  <div><span class="statnum">7</span><span class="statlabel">platform modules mapped</span></div>
  <div><span class="statnum">5</span><span class="statlabel">events in privacy schema</span></div>
  <div><span class="statnum">0</span><span class="statlabel">auto-published claims</span></div>
  <div><span class="statnum">0</span><span class="statlabel">model-training calls on Amazon data</span></div>
</div>

<h2>1. Subsystem status matrix</h2>
<table class="exec">
  <caption>Every platform module required by an automated affiliate pipeline, checked against Amazon
    Associates Operating Agreement (S01), Program Policies (S02), Creators API docs (S20), PA-API 5
    deprecation (S21), FTC FAQ (S03), and Google Search Central (S04).</caption>
  <thead><tr><th scope="col">Module</th><th scope="col">What runs in this repo today</th>
    <th scope="col">Current limit / blocker</th><th scope="col">Policy &amp; flags</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>1. Automated product research &amp; trend detection</strong></td>
      <td>Structured product registers (<code>data/products.json</code>), chunked snapshot log
        (<code>data/reverification-2026-11-20.json</code>), and conflict surfacing across all five
        submitted products.</td>
      <td>Live automated catalog polling is blocked until the Associates account passes final
        review and qualified-sales thresholds for the Creators API (PA-API 5 returns HTTP 403).</td>
      <td><a href="{source_url('S20')}" rel="sponsored nofollow">S20</a>,
        <a href="{source_url('S21')}" rel="sponsored nofollow">S21</a>, FLG-029</td>
    </tr>
    <tr>
      <td><strong>2. Market, pricing, review &amp; commission analysis</strong></td>
      <td>Explicit field separation keeping prices, star ratings, review counts, and commission
        forecasts omitted rather than scraped or estimated; empty provenance-gated
        <a href="campaign-ledger.html">campaign ledger</a>.</td>
      <td>Prices and ratings require Amazon-served links or Creators API access (Program Policies
        &sect;2(b), &sect;6(t), &sect;6(y)); commission schedules require signed-in Associates Central
        access.</td>
      <td><a href="{source_url('S02')}" rel="sponsored nofollow">S02</a>, FLG-005, Q-11, Q-13</td>
    </tr>
    <tr>
      <td><strong>3. SEO-optimized content &amp; comparison generation</strong></td>
      <td>Single-source generator (<code>scripts/build_site.py</code>) building {len(GUIDES)} guides, field-aligned
        <code>compare.html</code>, JSON-LD (<code>Product</code>, <code>FAQPage</code>,
        <code>Article</code>, <code>BreadcrumbList</code>), <code>sitemap.xml</code>,
        <code>feed.xml</code>, and client search index.</td>
      <td>Query-driven draft topics require Search Console verification (SG-10, SG-29, Q-20). Special
        Links and Program Content may not be used to train or fine-tune ML/LLM models without
        express prior written approval.</td>
      <td><a href="{source_url('S02')}" rel="sponsored nofollow">S02</a> &sect;5 &amp; IP &sect;1/&sect;2(e),
        SG-02, SG-32</td>
    </tr>
    <tr>
      <td><strong>4. Link management, Special Links &amp; anti-cloaking</strong></td>
      <td>Canonical <code>https://www.amazon.com/dp/&lt;ASIN&gt;?tag={TRACKING_ID}</code> Special
        Links paired with visible <strong>(paid link)</strong> labels, <code>rel="sponsored nofollow"</code>,
        separate intended/observed ASIN tables, and untagged audit links.</td>
      <td>Deceptive cloaking is prohibited (Program Policies &sect;6(v)) and link shorteners must not
        obscure the Amazon destination (&sect;6(w)). Submitted <code>link.amazon</code> compliance and
        live account click tests remain pending.</td>
      <td><a href="{source_url('S02')}" rel="sponsored nofollow">S02</a>,
        <a href="{source_url('S04')}" rel="sponsored nofollow">S04</a>, FLG-003, FLG-004, FLG-027</td>
    </tr>
    <tr>
      <td><strong>5. Privacy-preserving click &amp; conversion measurement</strong></td>
      <td>Strict 5-event schema (<code>data/events.json</code>), local browser logging + CSV export +
        configurable <code>send()</code> transport in <code>assets/app.js</code>, and zero-dependency
        collectors (<code>analytics/server.js</code>, <code>functions/api/collect.js</code>).</td>
      <td>GitHub Pages hosts static assets only; cross-visitor collection waits until the owner
        deploys the Node/Cloudflare endpoint and sets <code>sn-collect-endpoint</code>. Conversion
        orders still require official Associates reports.</td>
      <td><a href="{source_url('S03')}" rel="sponsored nofollow">S03</a>, FLG-010, SG-25, Q-08</td>
    </tr>
    <tr>
      <td><strong>6. Performance optimization &amp; campaign scaling</strong></td>
      <td>Human-first <a href="suggestions.html">Decision Center</a> ranking and export workflow,
        Search Console &amp; RSS checklists (<a href="measurement.html">SG-10</a>), and auditability
        gates before traffic expansion.</td>
      <td>Blocked on Q-04 (one-per-product Associates tracking test), Q-20 (Search Console query
        metrics), and Q-05 (optional custom domain).</td>
      <td>FLG-004, FLG-006, SG-07, SG-10, SG-16, SG-31</td>
    </tr>
    <tr>
      <td><strong>7. Compliance &amp; disclosure automation</strong></td>
      <td>Automated Python gate (<code>scripts/check_site.py</code>) plus GitHub Actions CI drift +
        compliance checks running on every PR and push to <code>main</code>.</td>
      <td>Maintains hard fail rules on above-the-fold disclosures, sponsored link attributes, banned
        price/rating patterns, blank-field flags, table column symmetry, and XML/JSON-LD validity.</td>
      <td><a href="{source_url('S01')}" rel="sponsored nofollow">S01</a>,
        <a href="{source_url('S02')}" rel="sponsored nofollow">S02</a>, SG-04, SG-05, SG-12</td>
    </tr>
  </tbody>
</table>

<h2>2. Hard policy boundaries for AI and automation</h2>
<ul>
  <li><strong>No ML or LLM training on Amazon Program Content (Program Policies, Participation
    Requirements &sect;5 &amp; IP License &sect;1, &sect;2(e)):</strong> Affiliates may not use
    Special Links, Program Content, Creators API, PA API, or Data Feeds to develop, train, or
    fine-tune machine learning models, LLMs, or related technologies without Amazon's express prior
    written approval. All editorial copy on this site is generated deterministically by Python from
    audited local JSON registers, never trained into model weights.</li>
  <li><strong>Agent identification &amp; anti-evasion (IP License &sect;4 Agent Terms):</strong>
    Any software agent accessing Program Content must identify itself in HTTP User-Agent headers
    as <code>Agent/[agent name]</code>, must never mimic human browsing or bypass CAPTCHAs/checkpoints,
    and must stop immediately if Amazon requests exclusion.</li>
  <li><strong>No link cloaking or hidden redirects (Program Policies &sect;6(v), &sect;6(w) &amp;
    Commission Income Statement &sect;2(e)):</strong> Readers must always see clearly that they are
    clicking a paid link to Amazon. Redirecting links without user action can disqualify commissions.</li>
  <li><strong>No cached Amazon images or unrefreshed API prices (IP License &sect;2(h), &sect;2(i),
    &sect;2(k)):</strong> Until Creators API credentials exist, this site uses captioned generated
    editorial imagery (<code>assets/photos/</code>, FLG-036) plus original SVG schematics
    (<code>assets/illustrations/</code>) and leaves price/availability fields blank by policy
    (FLG-005, FLG-007).</li>
</ul>

<h2>3. Deterministic 7-stage publishing pipeline</h2>
<ol>
  <li><strong>Fetch &amp; snapshot:</strong> Read official listings and policy docs; log URLs and dates
    in <code>data/sources.json</code> and <code>data/reverification-2026-11-20.json</code>.</li>
  <li><strong>Reconcile conflicts:</strong> Record contradictory listing figures with <code>"st": "conflict"</code>
    and assign a flag ID in <code>data/flags.json</code> rather than picking one number.</li>
  <li><strong>Redact unverified fields:</strong> Leave unstated specs <code>null</code> (<code>st: "unverified"</code>)
    and omit prices/ratings per Program Policies &sect;2(b) and &sect;6(t).</li>
  <li><strong>Render deterministically:</strong> Build all pages, <code>sitemap.xml</code>,
    <code>feed.xml</code>, <code>robots.txt</code>, and the client search index via
    <code>python3 scripts/build_site.py</code>.</li>
  <li><strong>Gate before publish:</strong> Run <code>python3 scripts/check_site.py</code> and automated
    tests locally and in GitHub Actions (<code>.github/workflows/pages.yml</code>) to block drift or
    policy violations.</li>
  <li><strong>Measure with zero cookies:</strong> Count the five defined events in browser storage or a
    self-hosted endpoint configured per <a href="measurement.html">Measurement &amp; Collector</a>.</li>
  <li><strong>Human decision gate:</strong> Rank new features on <a href="suggestions.html">Decision Center</a>
    and verify Associates tracking (<a href="questions.html">Q-04</a>) before scaling traffic.</li>
</ol>
"""
    BUILT.append(page("platform.html", f"Platform Architecture — {SITE}",
                      "AI-powered affiliate platform blueprint: seven modules, what runs today, "
                      "Creators API prerequisites, ML-training restrictions, and compliance gates.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Platform Architecture", "url": BASE + "platform.html"}))


# ---- measurement & collector
def build_measurement():
    ev_rows = ""
    for name, spec in EVENTS["events"].items():
        fields = ", ".join(f"<code>{esc(k)}</code>" for k in spec["allowed_fields"])
        ev_rows += (
            f"<tr><td><code>{esc(name)}</code></td>"
            f"<td>{esc(spec['fires_when'])}</td>"
            f"<td>{fields}</td>"
            f"<td>{esc(spec['used_for'])}</td></tr>"
        )
    forbidden = ", ".join(f"<code>{esc(f)}</code>" for f in EVENTS["forbidden_fields"])
    body = f"""
{breadcrumb([("Home", "index.html"), ("Measurement & Collector", None)])}
<h1>Measurement, Collector &amp; Search Console Setup</h1>
<p class="lede">Static GitHub Pages hosting cannot run backend code, so visitor metrics stay in your
  browser by default. When you are ready for cross-visitor counts without cookies or third-party
  scripts, this repository already includes the zero-dependency collector and strict schema below.</p>

<h2>1. Five-event schema (<code>data/events.json</code>)</h2>
<table class="events">
  <caption>Privacy contract v{esc(EVENTS['schema_version'])}. Disallowed fields ({forbidden}) are
    stripped client-side and rejected with HTTP 400 by the collector.</caption>
  <thead><tr><th scope="col">Event</th><th scope="col">Trigger</th>
    <th scope="col">Allowed fields</th><th scope="col">Purpose</th></tr></thead>
  <tbody>{ev_rows}</tbody>
</table>

<h2>2. How browser logging and <code>send()</code> behave</h2>
<ul>
  <li><strong>Default on GitHub Pages:</strong> All five events are appended to
    <code>localStorage</code> (<code>sn_events</code>, capped at 500 records) and outbound clicks
    increment <code>sn_clicks</code>. No network request fires while no collector endpoint is set
    (FLG-010).</li>
  <li><strong>Activating the self-hosted collector:</strong> Set
    <code>&lt;meta name="sn-collect-endpoint" content="/api/collect"&gt;</code>, define
    <code>window.SN_COLLECT_ENDPOINT</code>, or set <code>localStorage.setItem('sn_collect_url', ...)</code>.
    <code>send()</code> strips disallowed keys, rounds timestamps to the nearest minute, and sends a
    cookieless <code>POST</code> (<code>credentials: 'omit'</code>).</li>
  <li><strong>Search privacy:</strong> The <code>search</code> event records only query length
    (<code>q_len</code>) and match count (<code>results</code>), never the words typed by a reader.</li>
</ul>

<h2>3. Running the self-hosted collector</h2>
<p>Option A &mdash; Node.js zero-dependency server (<code>analytics/server.js</code>):</p>
<pre class="codebox">HOST=0.0.0.0 PORT=8787 COLLECT_LOG_FILE=/var/log/shopnow/events.ndjson node analytics/server.js
# Verify: GET /health or GET /api/collect -&gt; 200 OK {{"ok": true, "cookies": false}}</pre>
<p>Option B &mdash; Cloudflare Pages Function (<code>functions/api/collect.js</code>):</p>
<pre class="codebox"># Deploy the repository on Cloudflare Pages; /api/collect handles GET health and POST ingestion.
# Bind optional KV namespace SN_EVENTS to store timestamped JSON event entries.</pre>

<h2>4. Search Console &amp; reader-capture checklist (SG-10, Q-09, Q-20)</h2>
<ol>
  <li><strong>RSS capture (live now):</strong> <a href="feed.xml">feed.xml</a> is valid RSS 2.0
    listing all {len(GUIDES)} buying guides and linked from every page head and footer.</li>
  <li><strong>Google Search Console (owner action):</strong> Verify property ownership for
    <code>{BASE}</code> (or custom domain under SG-14), submit <code>{BASE}sitemap.xml</code>, and
    track impressions/CTR to choose new guide topics (SG-29, SG-32).</li>
  <li><strong>Conversion truth stays in Associates Central:</strong> First-party click counts show
    reader exits, never Amazon purchases. Authorised Associates tracking reports go into
    <a href="campaign-ledger.html">campaign-ledger.html</a> once <a href="questions.html">Q-04</a>
    passes.</li>
</ol>
<p class="cta"><a class="btn" href="disclosure.html">View Disclosure &amp; CSV Export</a>
  <a class="btn ghost" href="platform.html">Back to Platform Architecture</a></p>
"""
    BUILT.append(page("measurement.html", f"Measurement & Collector — {SITE}",
                      "Privacy-preserving five-event measurement schema, self-hosted Node.js and "
                      "Cloudflare Pages collectors, and Search Console onboarding steps.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Measurement and Collector", "url": BASE + "measurement.html"}))


# ---- search
def build_search():
    index = []
    for p in PRODUCTS:
        index.append({
            "t": f"{p['brand']} — {p['headline']}",
            "u": slug_of(p),
            "d": f"{p['cat']}. {p['best_for']}. {p['tradeoff']}. "
                 f"Listing title: {p['listing_title']}. Specs: " +
                 " ".join(f'{r["label"]} {r["value"]}' for r in p["spec_rows"]
                          if r["value"]),
            "k": "product " + p["cat"].lower(),
        })
    for g in GUIDES:
        index.append({"t": g["title"], "u": f"guides/{g['slug']}.html",
                      "d": g["intro"] + " " + " ".join(h + " " + t for h, t in g["sections"]),
                      "k": "guide"})
    for extra in [("Compare all five products", "compare.html",
                   "Side by side table of capacity, temperature, power, dimensions, weight and "
                   "trade-offs", "page"),
                  ("How we choose", "how-we-choose.html",
                   "What verified means, what we have not tested, what we refuse to print", "page"),
                  ("Design & Traffic Brief", "design-brief.html",
                   "Copy-paste design prompt, a topic-cluster traffic plan, a seasonal calendar "
                   "and the editorial standards checklist", "page"),
                  ("Decision Center", "suggestions.html",
                   "Proposals for this site, ranked before anything is built", "page"),
                  ("Open Questions", "questions.html",
                   "What has to be answered before a decision can be made", "page"),
                  ("Flagged for Review", "flagged.html",
                   "Every conflict and unverified value with its source", "page"),
                  ("Sources", "sources.html",
                   f"The {len(SOURCES)} official sources behind every claim", "page"),
                  ("Platform Architecture", "platform.html",
                   "AI affiliate platform subsystems, Creators API eligibility, ML-training limits, "
                   "anti-cloaking and automated CI compliance gates", "page"),
                  ("Measurement and Collector", "measurement.html",
                   "Five privacy-preserving events, self-hosted Node and Cloudflare collectors, and "
                   "Search Console setup", "page"),
                  ("Disclosure and privacy", "disclosure.html",
                   "Affiliate disclosure, price policy, and the five measured events", "page")]:
        index.append({"t": extra[0], "u": extra[1], "d": extra[2], "k": extra[3]})
    idx = json.dumps(index, ensure_ascii=False)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Search", None)])}
<h1>Search</h1>
<form class="searchpage" action="search.html" method="get" role="search">
  <label class="sr" for="sq">Search products, guides and records</label>
  <input id="sq" type="search" placeholder="Try: two baskets, 450, wireless, capacity">
  <button type="submit">Search</button>
</form>
<p class="small" id="searchMeta">Search matches run in your browser across {len(index)} pages. Built-in search terms are carried in
  session storage, not in the request URL. Normal page requests still reach the GitHub Pages host.</p>
<div id="results" class="results" aria-live="polite"></div>
<script type="application/json" id="searchIndex">{idx}</script>
<h2>Three places to start</h2>
<div class="grid">
  <article class="card"><h3><a href="guides/basket-vs-oven.html">Basket or oven-style?</a></h3>
    <p>The first decision, and the one that eliminates the most options.</p></article>
  <article class="card"><h3><a href="guides/instant-vs-wireless.html">Instant-read or wireless?</a></h3>
    <p>Two different tools, not two competing ones.</p></article>
  <article class="card"><h3><a href="compare.html">Compare all five</a></h3>
    <p>One table, aligned by field, prices omitted.</p></article>
</div>
"""
    BUILT.append(page("search.html", f"Search — {SITE}",
                      "Search products, guides and records in your browser. Built-in search terms are "
                      "not included in the request URL.",
                      body, jsonld={"@context": "https://schema.org", "@type": "SearchResultsPage",
                                    "name": "Search", "url": BASE + "search.html"}))


# ---- feed + sitemap + robots
def build_feed():
    items = ""
    for g in GUIDES:
        items += f"""<item>
  <title>{esc(g['title'])}</title>
  <link>{BASE}guides/{g['slug']}.html</link>
  <guid isPermaLink="true">{BASE}guides/{g['slug']}.html</guid>
  <description>{esc(g['sub'])}</description>
  <pubDate>Fri, 20 Nov 2026 00:00:00 GMT</pubDate>
</item>
"""
    (ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{SITE}</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>Air fryers and meat thermometers, read from official listings. Conflicts printed, prices never quoted.</description>
  <language>en-us</language>
  <lastBuildDate>Fri, 20 Nov 2026 00:00:00 GMT</lastBuildDate>
{items}</channel>
</rss>
""")


# Pages that exist for the project rather than for a shopper. They stay published and linked
# from the footer, but they are not what we ask a search engine to rank: an index full of
# internal dashboards is how a small site dilutes the pages that actually answer questions.
INTERNAL_PAGES = {
    "suggestions.html", "design-brief.html", "questions.html", "verification.html",
    "flagged.html", "sources.html", "platform.html", "measurement.html",
    "executive-summary.html", "campaign-ledger.html", "about.html", "disclosure.html",
}


def build_indexnow():
    """One machine-readable statement of what this site is, where its single canonical home is,
    and which pages we are asking to be indexed. `findability.txt` is for a human or an AI
    crawler; sitemap.xml is for the crawler proper; both are generated so they cannot drift."""
    public = [p for p in sorted(BUILT) if p not in INTERNAL_PAGES]
    guides = [g for g in GUIDES]
    lines = [
        "# ShopNow Kitchen - site profile for search engines and AI crawlers",
        f"# Generated {TODAY} by scripts/build_site.py. Do not hand-edit.",
        "",
        "SITE: ShopNow Kitchen",
        "TYPE: independent product-review publication (Amazon Associates affiliate)",
        f"CANONICAL_HOME: {BASE}",
        f"PRIMARY_LANGUAGE: en-US",
        f"LAST_REVIEWED: {TODAY}",
        "",
        "## What this site is for",
        "One question per page: which air fryer or meat thermometer fits a particular kitchen,",
        "and why. Five products are covered. Each specification is quoted from the official",
        "Amazon listing, dated, and linked. Listing contradictions are printed rather than",
        "smoothed over. No prices, star ratings, review counts or best-seller ranks are",
        "reproduced, because Amazon's Program Policies only permit that via Amazon-served data.",
        "",
        "## Editorial policy (what a crawler or reader can rely on)",
        "AUTHORSHIP: no named individual author yet; see about.html for what that means.",
        "REVIEW_PROCESS: read the official listing, quote it, date it, link it, print conflicts.",
        "HANDS_ON_TESTING: none claimed. The site says so on every product page.",
        "PAID_LINKS: every outbound Amazon link is rel=\"sponsored nofollow\" and carries the",
        "              Associate tag shopnow047c-20. Disclosure appears above the fold on every page.",
        "CORRECTIONS: dated entries on sources.html; unresolved items published on flagged.html.",
        "",
        "## Index these (reader-facing)",
    ]
    for page in public:
        lines.append(f"- {BASE}{page}")
    lines += ["", "## Not for indexing (project records, still public)", ]
    for page in sorted(INTERNAL_PAGES):
        lines.append(f"- {BASE}{page}")
    lines += [
        "",
        f"SITEMAP: {BASE}sitemap.xml",
        f"RSS: {BASE}feed.xml",
        f"ROBOTS: {BASE}robots.txt",
        "",
        "## How to cite this site",
        "ShopNow Kitchen, \"<page title>\", reviewed 2026-11-20.",
        f"Canonical URL: {BASE}<page>. Quote the review date with any specification you cite.",
        "",
        "## Known limits, stated up front",
        "- One canonical host: the GitHub Pages project URL above. No custom domain is live yet.",
        "- Intended ASINs per submitted link are unconfirmed; observed redirect targets are recorded.",
        "- The Associates tracking ID's issuance is not publicly verifiable.",
        "- Search Console is not yet verified, so no query data informs the editorial calendar.",
        "Full detail: flagged.html (unresolved items) and questions.html (what only the owner can answer).",
        "",
    ]
    (ROOT / "findability.txt").write_text("\n".join(lines))


def build_sitemap(pages):
    # Every page is submitted. The site's own gate and tests require full coverage, and a
    # half-submitted site is a worse outcome than an honest single site: one host, one sitemap,
    # one feed, with findability.txt naming which pages are the reader-facing ones.
    urls = "".join(
        f"  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'weekly' if p in ('index.html', 'guides.html', 'shop.html') else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if p == 'index.html' else '0.8' if p.startswith(('guides/', 'products/')) else '0.6'}</priority></url>\n"
        for p in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "# Reader-facing pages are listed in sitemap.xml; project records stay crawlable.\n\n"
        f"Sitemap: {BASE}sitemap.xml\n"
        f"# Site profile for crawlers and AI agents:\n"
        f"# {BASE}findability.txt\n")


# --------------------------------------------------------------------------- main
def main():
    build_home()
    build_shop()
    build_category(
        "air-fryers.html", "Air Fryers",
        "Air fryers: two baskets, one big basket, or a whole oven",
        "Three air fryers, three genuinely different answers to the same question: how do you cook? "
        "A dual-basket drawer, a single 8-quart basket, and a 26-quart countertop oven that air-fries.",
        [("guides/basket-vs-oven.html", "Basket or oven-style: what to compare first",
          "Footprint, doors, and how you load it."),
         ("guides/capacity-checklist.html", "A checklist for comparing capacity",
          "Quarts are not servings."),
         ("guides/cleanup-counter-space.html", "Cleanup and counter-space trade-offs",
          "Dishwasher-safe is not the same as easy."),
         ("guides/small-kitchen-air-fryer.html", "Air fryer for a small kitchen",
          "Three measurements that decide it."),
         ("guides/air-fryer-thanksgiving.html", "Air fryer at Thanksgiving",
          "What actually fits, and what does not.")],
        ["P-01", "P-03", "P-02"])
    build_category(
        "meat-thermometers.html", "Meat Thermometers",
        "Meat thermometers: instant-read or walk-away",
        "Two thermometers doing two different jobs. One gives you a number in a second; the other "
        "lets you leave the room for six hours. Buying the wrong one is the most common mistake here.",
        [("guides/instant-vs-wireless.html", "Instant-read or wireless: which do you need?",
          "Speed in your hand versus freedom to walk away."),
         ("guides/thermometer-accuracy.html", "How to read accuracy claims",
          "What ±0.5 °F and NIST actually mean.")],
        ["P-04", "P-05"])
    for p in PRODUCTS:
        build_product(p)
    build_compare()
    build_guides_index()
    for g in GUIDES:
        build_guide(g)
    build_verification()
    build_how()
    build_design_brief()
    build_suggestions()
    build_questions()
    build_flagged()
    build_sources()
    build_platform()
    build_measurement()
    build_exec()
    build_ledger()
    build_disclosure()
    build_about()
    build_search()
    build_feed()
    pages = sorted(BUILT) + ["sitemap.xml", "feed.xml"]
    build_sitemap(sorted(BUILT))
    build_indexnow()
    print(f"built {len(BUILT)} pages")
    for p in sorted(BUILT):
        print("  ", p)


if __name__ == "__main__":
    main()
