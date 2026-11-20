#!/usr/bin/env python3
"""
ShopNow Kitchen — single-source site generator.

Every HTML page in the repo is written by this script from data/*.json plus the
copy below. Nothing is hand-edited after generation, so a fact changes in one
place or not at all. Run:  python3 scripts/build_site.py
"""
import json
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

FIELD_LABEL = {
    "model": "Model", "capacity": "Capacity", "temperature": "Temperature range",
    "power": "Power", "dimensions": "Dimensions D x W x H", "weight": "Weight",
    "presets": "Presets", "warranty": "Warranty", "features": "Notable features",
    "response": "Response time", "accuracy": "Stated accuracy", "certification": "Certification",
    "waterproof": "Water resistance", "display": "Display", "included": "In the box",
    "upper_temp": "Upper temperature", "probes": "Probes", "heat": "Heat rating",
    "sensors": "Sensors", "connectivity": "Connectivity", "battery": "Battery",
    "probe_length": "Probe length", "care": "Cleaning",
}
FIELD_ORDER = ["capacity", "temperature", "power", "dimensions", "weight", "presets", "model",
               "response", "accuracy", "upper_temp", "probes", "heat", "sensors",
               "connectivity", "battery", "probe_length", "waterproof", "display",
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
    # `asin` and `listing` describe the direct Amazon page; `observed` is only
    # populated when the submitted short link was actually observed reaching it.
    # Never substitute the direct listing ID for an unconfirmed short-link target.
    p["intended"] = p.get("intended")
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
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def aff(p):
    """Tagged link to the direct listing reference; Associates testing is still pending."""
    listing = p["listing"].rstrip("/")
    return f"{listing}?tag={TRACKING_ID}"

def plain(p):
    """Untagged direct listing reference, separate from short-link observations."""
    return p["listing"]

def slug_of(p):
    return f"products/{p['slug']}.html"

AIRFRYER_GLYPH = """<svg viewBox="0 0 120 90" role="img" aria-label="Illustration of a basket air fryer">
<rect x="14" y="18" width="92" height="54" rx="10" fill="#f4e3d3" stroke="#c2410c" stroke-width="2.5"/>
<rect x="22" y="27" width="76" height="22" rx="5" fill="#fffdf8" stroke="#c2410c" stroke-width="2"/>
<circle cx="96" cy="60" r="5" fill="#c2410c"/><path d="M34 60h40" stroke="#c2410c" stroke-width="3" stroke-linecap="round"/>
<path d="M30 72v6M90 72v6" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/></svg>"""

OVEN_GLYPH = """<svg viewBox="0 0 120 90" role="img" aria-label="Illustration of an oven-style air fryer">
<rect x="12" y="16" width="96" height="58" rx="8" fill="#f4e3d3" stroke="#c2410c" stroke-width="2.5"/>
<rect x="22" y="26" width="34" height="38" rx="4" fill="#fffdf8" stroke="#c2410c" stroke-width="2"/>
<rect x="64" y="26" width="34" height="38" rx="4" fill="#fffdf8" stroke="#c2410c" stroke-width="2"/>
<circle cx="39" cy="45" r="9" fill="none" stroke="#c2410c" stroke-width="2"/>
<path d="M70 45h22M70 53h14" stroke="#c2410c" stroke-width="3" stroke-linecap="round"/></svg>"""

THERMO_GLYPH = """<svg viewBox="0 0 120 90" role="img" aria-label="Illustration of a meat thermometer">
<rect x="26" y="26" width="40" height="44" rx="7" fill="#f4e3d3" stroke="#c2410c" stroke-width="2.5"/>
<rect x="32" y="33" width="28" height="15" rx="3" fill="#fffdf8" stroke="#c2410c" stroke-width="2"/>
<path d="M70 47h26" stroke="#1c1917" stroke-width="4" stroke-linecap="round"/>
<path d="M96 47l8 -4v8z" fill="#1c1917"/>
<circle cx="41" cy="60" r="3.5" fill="#c2410c"/><circle cx="51" cy="60" r="3.5" fill="#c2410c"/></svg>"""

def glyph(p):
    if p["cat"] == "Meat Thermometers":
        return THERMO_GLYPH
    return OVEN_GLYPH if p["id"] == "P-02" else AIRFRYER_GLYPH

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
    ("questions.html", "Open Questions"),
    ("flagged.html", "Flagged for Review"),
    ("sources.html", "Sources"),
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
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{SITE} — Feed" href="{up}feed.xml">
{ld}{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap mast">
    <a class="brand" href="{up}index.html">ShopNow<span>Kitchen</span></a>
    <button class="navtoggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <nav id="primary-nav" aria-label="Primary">{nav}</nav>
    <form class="search" action="{up}search.html" method="get" role="search">
      <label class="sr" for="q">Search products and guides</label>
      <input id="q" name="q" type="search" placeholder="Search air fryers, thermometers, guides" autocomplete="off">
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
      Inc. or its affiliates. This site is not endorsed by Amazon. Artwork is original illustration,
      not product photography. Nothing here is a hands-on product test — every specification is read
      from the official listing and dated. Last verified {TODAY}.</p>
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
    return f"""<div class="buybox">
  <div class="buybox-art">{glyph(p)}</div>
  <div class="buybox-body">
    <p class="kicker">{esc(p['cat'])} · {p['id']}</p>
    <h3>{esc(p['headline'])}</h3>
    <p>{esc(p['blurb'])}</p>
    <dl class="factrow">
      <div><dt>Best for</dt><dd>{esc(p['best_for'])}</dd></div>
      <div><dt>The catch</dt><dd>{esc(p['tradeoff'])}</dd></div>
    </dl>
    <ul class="checks">{checks}</ul>
    <p class="cta">
      <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
         data-event="outbound_click">{esc(p['headline'])} — see it on Amazon (paid link)</a>
      <a class="btn ghost" href="{up}{slug_of(p)}">Full breakdown</a>
    </p>
    <p class="small">Prices, ratings and availability live on Amazon and change; we never print them
      here. Tagged link, opens amazon.com. <a href="{plain(p)}" rel="sponsored nofollow">Untagged
      listing</a> for verification.</p>
  </div>
</div>"""


def card(p, up):
    return f"""<article class="card">
  <div class="card-art">{glyph(p)}</div>
  <p class="kicker">{esc(p['cat'])}</p>
  <h3><a href="{up}{slug_of(p)}">{esc(p['headline'])}</a></h3>
  <p class="brandline">{esc(p['brand'])}</p>
  <p>{esc(p['blurb'])}</p>
  <p class="cta">
    <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
       data-event="outbound_click">Check price on Amazon (paid link)</a>
  </p>
  <p class="small"><a href="{up}{slug_of(p)}">Specs, trade-offs and questions &rarr;</a></p>
</article>"""



def usda_block(p):
    """Food-safety minimums, quoted from the USDA chart. Only on thermometer pages."""
    if p["cat"] != "Meat Thermometers":
        return ""
    rows = "".join(
        f'<tr><td>{esc(food)}</td><td>{esc(temp)}</td>'
        f'<td><a href="{USDA["source_url"]}">USDA FSIS source</a></td></tr>'
        for food, temp in USDA["rows"])
    return f"""<h2>Doneness targets come from the USDA, not from us</h2>
<p>This is a thermometer, so the numbers that matter are food-safety numbers. The USDA FSIS
  <a href="{USDA["source_url"]}">Safe Minimum Internal Temperature Chart</a> (source
  {USDA["source_id"]}, checked {USDA["checked"]}) gives these minimums, as measured with a food
  thermometer:</p>
<table class="usda">
  <caption><a href="{USDA["source_url"]}">USDA FSIS &mdash; Safe Minimum Internal Temperature
    Chart</a> ({USDA["source_id"]})</caption>
  <thead><tr><th scope="col">Food</th><th scope="col">Minimum internal temperature</th>
    <th scope="col">Official source</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="small">Read the chart itself before relying on any number here:
  <a href="{USDA["source_url"]}">fsis.usda.gov</a>. Registered as {USDA["source_id"]} in the
  <a href="../sources.html">source register</a>.</p>
"""


def spec_table(p):
    out = []
    for r in p["spec_rows"]:
        if r["value"] is None or r["status"] == "unverified":
            value = ('<span class="unverified">left blank &mdash; not in the listing text we '
                     'fetched</span>')
        else:
            value = esc(r["value"])
            if r["status"] == "conflict":
                value += ' <span class="token conflict">conflicting figures &mdash; both shown</span>'
        out.append(
            f'<tr><th scope="row">{esc(r["label"])}</th><td>{value}'
            f'<div class="srcline">Stated in: {esc(r["from"])}</div></td>'
            f'<td class="src"><a href="{r["url"]}" rel="sponsored nofollow">listing</a></td></tr>')
    return f"""<table class="specs-table">
  <caption>Every value below was read from the official listing on {TODAY}. A blank cell means the
    value was not in the text we fetched &mdash; nothing here is inferred.</caption>
  <thead><tr><th scope="col">Field</th><th scope="col">Value as stated on the listing</th>
    <th scope="col">Source</th></tr></thead>
  <tbody>{"".join(out)}</tbody>
</table>"""


def intent_table(p):
    intended = p.get("intended") or "— blank: not confirmed by the owner (FLG-001)"
    observed = p.get("observed") or "— not confirmed from the supplied short link (FLG-012)"
    return f"""<table class="intent">
  <caption>Product-intent confirmation record. Intended ASIN, observed redirect target, and direct
    listing reference are separate; an unresolved redirect is not filled from the direct listing.</caption>
  <tbody>
    <tr><th scope="row">Submitted link (as supplied)</th><td>{esc(p['submitted'])}</td></tr>
    <tr><th scope="row">Short-link token</th><td>{esc(p['token'])} (not an ASIN)</td></tr>
    <tr><th scope="row">Intended ASIN</th><td>{esc(intended)}</td></tr>
    <tr><th scope="row">Observed redirect target</th><td>{esc(observed)}</td></tr>
    <tr><th scope="row">What the submitted link actually opened</th><td>{esc(p['observed_note'])}</td></tr>
    <tr><th scope="row">Official listing URL</th>
      <td><a href="{plain(p)}" rel="sponsored nofollow">{plain(p)}</a></td></tr>
    <tr><th scope="row">Special Link we publish</th>
      <td><a href="{aff(p)}" rel="sponsored nofollow">{aff(p)}</a></td></tr>
    <tr><th scope="row">Model (as published)</th>
      <td>{esc(p['model'] or '— blank, see FLG-022')}<br><span class="small">{esc(p['model_source'])}</span></td></tr>
    <tr><th scope="row">Confirmation date</th><td>{TODAY}</td></tr>
    <tr><th scope="row">Associates test status</th>
      <td>PENDING &mdash; one link per product must be clicked inside the enrolled account and
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
def build_home():
    featured = PRODUCTS
    body = f"""
<section class="hero">
  <div class="hero-copy">
    <p class="kicker">ShopNow Kitchen · a counter-side buying guide</p>
    <h1>Which air fryer fits your counter — and which thermometer fits your cooking style?</h1>
    <p class="lede">Start with the things that change your day: room to open a drawer or door, the
      way you cook a weeknight meal, and whether you want a quick temperature check or a reading you
      can monitor during a cook. Five submitted listings, two categories, and no hands-on product tests.</p>
    <p class="cta">
      <a class="btn" href="air-fryers.html">Compare air fryers</a>
      <a class="btn ghost" href="meat-thermometers.html">Compare thermometers</a>
      <a class="btn ghost" href="compare.html">See all five</a>
    </p>
    <p class="small">Listing details are dated and sourced; unresolved conflicts stay open rather than guessed.</p>
  </div>
  <div class="hero-art" aria-hidden="true">
    <div class="hero-tile">{AIRFRYER_GLYPH}</div>
    <div class="hero-tile">{THERMO_GLYPH}</div>
  </div>
</section>

<section>
  <h2>The five products in this edition</h2>
  <p class="muted">A small selection drawn from the links supplied for this project, not a market ranking.
    Open a product page for listing details, fit questions, and the unresolved items we have not filled in.</p>
  <div class="grid">
    {"".join(card(p, "") for p in featured)}
  </div>
  <p class="small"><a href="shop.html">Browse the product index &rarr;</a></p>
</section>

<section class="split">
  <div>
    <h2>Start with a buyer question</h2>
    <ul class="linklist">
      <li><a href="guides/basket-vs-oven.html">Basket or oven-style air fryer: what should you compare?</a>
        <span>Footprint, doors, drawers, and the way you load it.</span></li>
      <li><a href="guides/capacity-checklist.html">How should you compare air-fryer capacity?</a>
        <span>Check the interior shape and your regular meals, not a guessed serving count.</span></li>
      <li><a href="guides/cleanup-counter-space.html">What should you check about cleanup and counter space?</a>
        <span>Read the care instructions and measure the place it will live.</span></li>
      <li><a href="guides/instant-vs-wireless.html">Instant-read or wireless thermometer: which workflow fits?</a>
        <span>Choose by when and where you want a reading.</span></li>
      <li><a href="guides/thermometer-accuracy.html">How do you assess a thermometer accuracy claim?</a>
        <span>Separate a seller-stated tolerance from a test you can inspect.</span></li>
    </ul>
  </div>
  <aside class="panel">
    <h3>Before you add it to the counter</h3>
    <ol class="tight">
      <li>Measure width, depth, height, and the path a door or drawer needs.</li>
      <li>Write down a meal or cooking task you want the appliance to handle.</li>
      <li>Check the live listing and the maker's manual for the details that matter to that task.</li>
      <li>If two listing sections disagree, read the open note before deciding which figure to use.</li>
    </ol>
    <p class="small"><a href="how-we-choose.html">What these pages can and cannot tell you &rarr;</a></p>
  </aside>
</section>

<section class="panel scallop">
  <h2>All five, side by side</h2>
  <p class="muted">Use this as a first comparison, then follow the product-page source links and fit questions.
    It is not a lab test or a ranking.</p>
  {overview_table()}
</section>

<section>
  <h2>A few questions worth asking</h2>
  <div class="faq">
    <details><summary>Can I see today's price here?</summary><p>No. This publication does not display
      prices or availability. Follow a clearly labelled listing link and check the current details
      on Amazon before buying.</p></details>
    <details><summary>What should I compare first?</summary><p>Measure the space and clearances, then
      match the interior or thermometer workflow to a meal you cook often. Features matter after those
      practical fit questions.</p></details>
    <details><summary>Are these hands-on reviews?</summary><p>No. The product pages summarize seller-stated
      listing details and questions to check in the maker's instructions. No appliance or thermometer
      was independently tested for this site.</p></details>
    <details><summary>How current are the listing details?</summary><p>The product pages display the
      date the source pages were checked. Listings change; revisit the linked listing and manual for
      current details.</p></details>
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
           "publisher": dict(publisher_ld(), **{"@context": "https://schema.org"})}]
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
    body = f"""
{breadcrumb([("Home", "index.html"), (cat, None)])}
<h1>{esc(headline)}</h1>
<p class="lede">{intro}</p>
{box_items}
<h2>The fit question, one line each</h2>
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
    # The retailer ID describes the directly checked listing, not a short-link redirect.
    og = ('<meta property="product:retailer_item_id" content="'
          + p["asin"] + '">') if p.get("asin") else ""
    observation_note = ""
    if not p.get("observed"):
        observation_note = ('<p class="small">The supplied short link did not reproduce this direct '
                            'listing in the latest recorded check; the listing reference is separate '
                            'from a confirmed redirect (FLG-012).</p>')
    body = f"""
{breadcrumb([("Home", "index.html"), (p['cat'], p['catfile']), (p['brand'], None)], "../")}
<div class="pdp-head">
  <div>
    <p class="kicker">{esc(p['cat'])} · {p['id']} · listing reference checked {TODAY}</p>
    <h1>{esc(p['headline'])}</h1>
    <p class="lede">{esc(p['blurb'])}</p>
  </div>
  <div class="pdp-art">{glyph(p)}</div>
</div>
<div class="pdp-buy">
  <div>
    <p class="buyline">Best for <strong>{esc(p['best_for'])}</strong></p>
    <p class="buyline">The catch <strong>{esc(p['tradeoff'])}</strong></p>
  </div>
  <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
     data-event="outbound_click">Check the live price on Amazon (paid link)</a>
</div>
<p class="small">This paid link opens the direct listing reference, tagged with the supplied Associates ID.
  The tagged link has not yet been tested in the enrolled account.</p>
{observation_note}

<h2>Is this the right one for you?</h2>
<div class="qa">
{"".join(f'<div class="qa-row"><p class="qa-q">{esc(q)}</p><p class="qa-a">{esc(a)}</p></div>' for q, a in p["questions"])}
</div>

<h2>Specifications, line by line</h2>
{spec_table(p)}

{faq_block(p)}

<h2>What you are actually buying</h2>
<p>The listing describes this as <em>{esc(p['listing_title'])}</em>. That is the current title on
  Amazon, quoted exactly rather than paraphrased, so you can match it against the page you land
  on. Brand: {esc(p['brand'])}.{(" Model: " + esc(p['model']) + ".") if p['model'] else " The listing does not publish a model number."}</p>

<h2>Product-intent confirmation record</h2>
{intent_table(p)}

{usda_block(p)}
<h2>What this page does not claim</h2>
<p>No price, star rating, review count, sales rank, commission rate or "best" verdict appears above.
  Those values are left out on purpose, either because Amazon's policy governs them or because they
  cannot be confirmed from an official source. Where the listing contradicts itself, both figures are
  printed and the contradiction is listed on the
  <a href="../flagged.html">Flagged for Review</a> page with its ID.</p>

<p class="cta">
  <a class="btn" href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p['id']}"
     data-event="outbound_click">See it on Amazon (paid link)</a>
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
def build_compare():
    cols = PRODUCTS
    def row(label, fn, source="listing"):
        cells = []
        for p in cols:
            value = fn(p)
            if source == "policy":
                cite = (f'<div class="srcline">Policy source: '
                        f'<a href="{source_url("S02")}">Amazon Program Policies §2(b), §6(t)</a></div>')
            elif source == "editorial":
                cite = (f'<div class="srcline">Editorial fit note based on listed facts — verify '
                        f'on the listing: <a href="{plain(p)}" rel="sponsored nofollow">Amazon listing</a></div>')
            elif source == "listing":
                cite = (f'<div class="srcline">Listing source: '
                        f'<a href="{plain(p)}" rel="sponsored nofollow">Amazon listing</a></div>')
            else:
                cite = ""
            cells.append(f"<td>{value}{cite}</td>")
        return f'<tr><th scope="row">{label}</th>{"".join(cells)}</tr>'

    def spec(p, key, other="— <span class=\"unverified\">not stated on the listing</span>"):
        f = p["fields"].get(key)
        if not f or f["v"] is None:
            return other
        txt = esc(f["v"])
        if f["st"] == "conflict":
            txt += ' <span class="token conflict">see flags</span>'
        return txt

    NOCAP = "— <span class=\"unverified\">n/a, not a capacity appliance</span>"
    NOTSTATED = "— <span class=\"unverified\">not stated in the fetched listing text</span>"

    head = "".join(f'<th scope="col"><a href="{slug_of(p)}">{esc(p["brand"])}</a>'
                   f'<br><span class="th-sub">{p["id"]} · {esc(p["headline"])}</span></th>' for p in cols)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Compare", None)])}
<h1>Compare &mdash; without crowning a winner</h1>
<p class="lede">A comparison that names a "best" without knowing your counter depth, your household
  size or how you cook would be guessing. This table gives you the same facts we have, in the same
  rows, so you can decide. Blank means the listing does not say.</p>
<table class="compare">
  <caption>Listing facts link to their official source in each product column. "Best for" and "The catch" are editorial fit notes, not seller claims. Checked {TODAY}.</caption>
  <thead><tr><th scope="col">Field</th>{head}</tr></thead>
  <tbody>
    {row("Category", lambda p: esc(p["cat"]))}
    {row("Best for", lambda p: esc(p["best_for"]), source="editorial")}
    {row("The catch", lambda p: esc(p["tradeoff"]), source="editorial")}
    {row("Capacity", lambda p: spec(p, "capacity", NOCAP))}
    {row("Temperature range", lambda p: spec(p, "temperature", NOTSTATED))}
    {row("Power / battery", lambda p: spec(p, "power", "see battery row"))}
    {row("Dimensions D×W×H", lambda p: spec(p, "dimensions", NOTSTATED))}
    {row("Weight", lambda p: spec(p, "weight", NOTSTATED))}
    {row("Model on listing", lambda p: spec(p, "model", NOTSTATED))}
    {row("Price", lambda p: "— not shown, by policy", source="policy")}
    {row("Star rating", lambda p: "— not shown, by policy", source="policy")}
    {row("Official listing", lambda p: f'<a href="{plain(p)}" rel="sponsored nofollow">untagged listing source</a>', source=None)}
    {row("Buy link", lambda p: f'<a href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p["id"]}" data-event="outbound_click">Amazon (paid link)</a>', source=None)}
  </tbody>
</table>
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
    BUILT.append(page("compare.html", f"Compare all five — {SITE}",
                      "Side-by-side table of all five products, aligned by field, with prices and "
                      "ratings deliberately omitted and conflicts left visible.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Compare", "url": BASE + "compare.html"}))


# ---- guides
GUIDES = [
    dict(slug="basket-vs-oven", title="Basket or oven-style air fryer: what should you compare?",
         sub="Drawer versus door affects access, placement, and how you load food. Measure before comparing features.",
         kicker="Buying guide · 6 min read", products=["P-01", "P-02", "P-03"],
         intro="""A useful first question is how the appliance opens: a drawer to pull, or a door to swing. That
         affects where it can sit and how you load it. Shape alone does not say which one will cook
         better for your meals.""",
         sections=[
            ("What actually differs", """A basket model uses a removable drawer or basket; an oven-style model has a door and may include
            racks or trays. Check the exact configuration on the listing and manual. Compare the access
            route, removable parts, and where you will set down hot food; we have not tested cooking
            speed or results."""),
            ("Measure the footprint, including the swing", """The current records list P-02 at 16.9 inches deep, P-01 at 13.38 inches, and P-03 at 12.75 inches.
            Recheck those values on each live listing and use the maker's manual for clearance. Include
            the wall behind it, space above it, handles, and the path a door or drawer needs."""),
            ("Think about how you load it, and how you clean it", """A drawer and a door-and-rack layout involve different loading and unloading steps. Check which
            pieces are removable and how the manual says to clean them. If you plan to store the unit
            between uses, check the listing's weight and the storage space needed for its accessories."""),
            ("Map the layout to your meals", """If you often cook two things at once, check whether separate
            baskets and their timing controls suit that routine. If one larger cooking area matters
            more, compare the listed basket dimensions. If you want oven modes or accessories, confirm
            exactly what the current listing and manual include."""),
         ],
         verdict="""Measure the usable space and clearances, then compare how each model opens and what fits inside.
         Use a regular meal to decide whether one area, separate baskets, or listed oven accessories
         matter to you."""),
    dict(slug="capacity-checklist", title="A no-hype checklist for comparing air fryer capacity",
         sub="A capacity label describes volume, not a serving count. Check the usable shape and the food you make.",
         kicker="Buying guide · 5 min read", products=["P-01", "P-02", "P-03"],
         intro="""Capacity is one clue, but a volume label alone does not show the shape of the cooking area or how
         your usual food will fit. Check the interior layout, maker's fit examples, and the appliance's
         outside dimensions before deciding what the number means for your kitchen.""",
         sections=[
            ("1. Total versus usable", """Six quarts split into two three-quart baskets is not the same
            as one six-quart basket. The split gives you two separate cooks; the single basket gives
            you one bigger flat area. Neither is better in the abstract &mdash; they suit different
            meals."""),
            ("2. Flat area, not volume", """A volume figure does not tell you the usable width or arrangement of a basket or tray. Look for
            interior dimensions or maker-stated fit examples; if the listing does not give them, leave
            the fit question open rather than inferring from the quart figure."""),
            ("3. What the listing says fits", """A model's listing may give a fit example. The current P-02 listing mentions a 12-inch pizza and
            rotisserie for a 6-pound chicken. Treat those as seller-stated examples, check the live
            listing and manual, and do not assume they describe every food or rack position."""),
            ("4. Physical size on the counter", """A bigger cavity usually means a bigger box. Compare
            dimensions before you talk yourself into capacity you do not have room for. The 26-quart
            oven is 16.9 inches deep; the 8-quart basket is 12.75."""),
            ("5. Your household, honestly", """Do not convert the label into a guessed number of diners. Write down a meal you cook often, the
            largest ingredient or dish, and whether you would rather cook in one area, separate zones,
            or batches."""),
            ("6. Watch the units", """The P-01 listing uses different units in its title and capacity field: 6 quarts and 6 liters.
            Both statements are retained in the record; this site does not decide which unit to prefer.
            See FLG-034."""),
         ],
         verdict="""Write down the largest item you expect to cook, how many different foods you prepare at once, and
         your usable counter space. Compare those needs with the maker's listed dimensions and layout."""),
    dict(slug="cleanup-counter-space", title="How to assess cleanup and counter-space trade-offs",
         sub="Dishwasher-safe applies to named parts. Read the care instructions and plan where they will dry.",
         kicker="Buying guide · 5 min read", products=["P-01", "P-02", "P-03"],
         intro="""Cleanup and storage are easy to overlook when comparing feature lists. Check which parts touch
         food, what the manual says about cleaning, and whether the appliance has a usable place on your
         counter or in a cupboard.""",
         sections=[
            ("Count the parts that touch food", """Count the removable food-contact parts named in each listing and manual: baskets, trays, racks,
            pans, or drip trays. Check where they will dry and how they will be stored. Do not assume
            an accessory pictured on a page is included unless the listing says so."""),
            ("Check what the listing actually promises", """The current P-03 listing states that the basket and flat tray are top-rack dishwasher safe; the
            P-01 listing states that its removable baskets are dishwasher safe. Check the live listing
            and manual for each part and do not infer a care instruction for a surface the maker does
            not mention."""),
            ("Weight decides where it lives", """If you plan to put the appliance away between uses, check its listed weight and the storage space
            needed for accessories. The P-01 weight is not confirmed in the fetched listing record; do
            not infer it from the other basket models."""),
            ("Measure depth, swing and clearance together", """Compare the appliance's listed dimensions with your usable counter space, then follow the maker's
            manual for ventilation clearances. Include room for a door to open or a drawer to slide out."""),
            ("The one-question test", """Ask where the appliance will sit when not in use. If you plan to store it, check the weight,
            handling instructions, door or drawer access, and space for accessories."""),
         ],
         verdict="""Compare the removable parts and care instructions, then measure the counter or storage space
         before choosing a layout."""),
    dict(slug="multi-function-questions", title="Questions to ask before buying a multi-function kitchen appliance",
         sub="A long feature list is useful only if it matches tasks you do. Which three would you use?",
         kicker="Buying guide · 5 min read", products=["P-02", "P-03"],
         intro="""Start with the meals or tasks you repeat. For each one, check whether the product listing and
         manual explain the mode and accessories you would need. Count the storage and cleaning steps
         before treating a long list of functions as useful.""",
         sections=[
            ("Name your three functions", """Write down the three modes you expect to use in your own kitchen. Then check whether each one is
            named in the current listing and described in the manual. Do not assume a preset is a
            separate cooking function."""),
            ("Distinguish functions from presets", """A function label and a preset count are different kinds of listing detail. Check what each preset
            does in the manual rather than assuming a larger count means more useful modes. The P-02
            listing has a preset-count conflict; see FLG-009."""),
            ("Check whether accessories are included or extra", """Rotisserie spits, crisper baskets
            and bake pans are often the difference between a function being usable and being a
            promise. The Emeril listing names six included components: rack, bake pan, drip tray,
            crisper basket, rotisserie spit, fetch tool. Its title says six accessories and its
            configuration field says seven &mdash; flagged as FLG-031."""),
            ("Count accessories and cleanup steps", """List the accessories the seller says are included,
            verify them in the current listing, and check their care instructions. If a function needs
            a part that is not listed, leave that detail open instead of assuming it comes in the box."""),
            ("Check the manual before you trust a preset count", """Where a listing contradicts itself, record both statements and check the model's instructions or
            ask the maker. This site's open P-02 and P-03 conflicts remain flagged rather than resolved
            by choosing a convenient value."""),
         ],
         verdict="""Write down the tasks you want the appliance to handle, then verify the mode and any required
         accessory in the maker's instructions before deciding."""),
    dict(slug="instant-vs-wireless", title="Instant-read or wireless thermometer: which do you actually need?",
         sub="Compare a quick spot check with a leave-in monitoring workflow, subject to each model's instructions.",
         kicker="Buying guide · 6 min read", products=["P-04", "P-05"],
         intro="""These are different workflows. An instant-read tool is used when you pause to take a reading; a
         wireless probe is designed to stay in during a cook only as its maker's instructions allow.
         Compare setup, connectivity, probe care, and charging before choosing.""",
         sections=[
            ("What an instant-read is for", """An instant-read thermometer is for a reading taken at the time you choose to check. The P-04
            listing states a 1-second response claim, an accuracy tolerance, and a calibration
            certificate in the box. These are seller statements, not results from our own test; check
            the current listing and the instructions."""),
            ("What a wireless system is for", """The P-05 listing describes three probes, a hub, and app connectivity. Check the current listing
            and manual for connection limits, compatible devices, cooking instructions, and what
            happens if the connection is lost."""),
            ("The honest cost of wireless", """A wireless setup may involve an app, a hub, and charging. The P-05 battery statements conflict
            in the listing (FLG-008); check current instructions and do not rely on either duration
            until the conflict is resolved."""),
            ("Accuracy claims are claims", """The P-04 listing includes an accuracy tolerance and references NIST and NSF. We have not seen
            supporting certification documents or an independent test report for either thermometer;
            treat those words as seller claims, not our test result."""),
            ("What number actually matters for safety", """Use the USDA FSIS chart linked on this page for food-safety targets and follow the thermometer
            maker's instructions for probe placement. Do not treat a thermometer listing as food-safety
            guidance or infer performance from its maximum temperature rating."""),
         ],
         verdict="""Choose by the workflow you need: a spot-check reading or a leave-in probe supported by the maker's
         instructions. If you need both workflows, compare the separate products on their own terms."""),
    dict(slug="thermometer-accuracy", title="How to assess thermometer accuracy claims",
         sub="Separate a seller-stated accuracy tolerance from a test report, calibration procedure, and certification document.",
         kicker="Buying guide · 5 min read", products=["P-04", "P-05"],
         intro="""A listing's accuracy tolerance is a seller-stated claim, not independent test data. Check what
         range and conditions it covers, whether supporting documentation is available, and how the
         maker says to check or calibrate the instrument.""",
         sections=[
            ("Separate the claim from the evidence", """Read an accuracy tolerance separately from response time, resolution, and calibration. The P-04
            listing states a tolerance, but this site has not independently measured it or seen a test
            report. The P-05 listing does not provide an equivalent result in the material recorded here."""),
            ("Ask what a certification statement covers", """The P-04 seller listing uses the words NIST and
            NSF, and states that a calibration certificate is included. We have not inspected a
            certificate or verified what the seller's certification wording applies to. Ask the maker
            for the scope and supporting documentation before treating the wording as independent proof."""),
            ("Read the calibration instructions", """Check the maker's instructions for calibration or
            verification steps, conditions, and what to do if a reading is outside tolerance. A
            certificate mentioned in a listing is not the same as a procedure we have independently
            checked."""),
            ("Check resolution separately from accuracy", """Do not treat the number of displayed digits or a fast response-time claim as evidence of accuracy.
            Compare those fields separately and check the exact conditions attached to the stated
            tolerance."""),
            ("Use an official food-safety source", """For cooking targets, use the USDA FSIS chart linked on
            this page. A seller's accuracy number is not a food-safety target; follow the chart and the
            thermometer maker's instructions for placement and use."""),
         ],
         verdict="""Read the exact tolerance and conditions, look for the maker's supporting documentation, and use
         official food-safety guidance for cooking targets. We have not independently tested either model."""),
    dict(slug="air-fryer-thanksgiving", title="Air fryer at Thanksgiving: what actually fits",
         sub="Use the listed fit examples as checks for a particular meal; do not extrapolate them to other foods.",
         kicker="Seasonal guide · 4 min read", products=["P-02", "P-01", "P-03"],
         intro="""Planning a holiday meal? List the dishes that need oven space, then check which tasks a
         countertop appliance's current listing and manual actually support. These are planning prompts,
         not a claim about what is popular or a tested serving recommendation.""",
         sections=[
            ("What a countertop oven can take off your hands", """The current P-02 listing gives fit examples including a 12-inch pizza and a 6-pound rotisserie
            chicken. Check the current listing and manual before mapping those examples to a holiday
            dish; they are seller statements, not our capacity test."""),
            ("Do not extrapolate a fit example", """A listed 6-pound chicken fit does not confirm that a
            whole turkey or another dish will fit. Measure your food and check the usable interior and
            manual before planning a meal around it."""),
            ("Check your batch plan", """If you are considering the P-01 dual-basket layout, check the
            listing's separate-basket and timing claims against the number of dishes you want to cook.
            We have not tested how quickly a particular holiday side cooks in this unit."""),
            ("Check power and setup", """Verify the current listing's voltage and wattage, and follow the
            appliance manual and your home's electrical guidance. The P-03 listing has conflicting
            power values (FLG-017), so this page does not choose one."""),
         ],
         verdict="""Plan around verified dimensions and maker-stated fit examples. Confirm clearance, instructions,
         and any power details in the live listing and manual before the meal."""),
    dict(slug="small-kitchen-air-fryer", title="Air fryer for a small kitchen: the three measurements that decide it",
         sub="Measure depth, access, and the storage spot before comparing features.",
         kicker="Buying guide · 4 min read", products=["P-03", "P-01", "P-02"],
         intro="""In a small kitchen, measure the actual counter or cupboard space first. Check the appliance's
         depth, how it opens, and where it will be stored before comparing feature lists.""",
         sections=[
            ("1. Depth, plus the air gap", """Depth is the first disqualifier. Both Chefman basket
            units are under 14 inches deep; the oven-style Emeril is 16.9. Add the clearance the
            manual asks for behind and above, and you have your real number."""),
            ("2. Door swing or drawer pull", """A drawer needs room in front for you to stand and pull.
            French doors need room in front for two doors to open and stay open. In a narrow galley
            that difference decides whether the appliance is usable at all."""),
            ("3. Where it lives between uses", """If you plan to put the appliance away, compare the listed weight, handling instructions, and
            storage space. The P-03 listing states 12.8 pounds and the P-02 listing 26.5 pounds; check
            those values on the current pages before buying."""),
            ("Choose the trade-offs you can live with", """A window, presets, and separate baskets are
            features to compare against your routine. If none is important to you, do not let its
            presence decide the purchase. Check dimensions and handling for every model you consider."""),
         ],
         verdict="""Measure the counter and door/drawer access, then check storage and the maker's clearance
         instructions. Compare features only after the physical fit is clear."""),
]


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
<p class="kicker">{esc(g['kicker'])} · listing references checked {TODAY}</p>
<h1>{esc(g['title'])}</h1>
<p class="lede">{esc(g['intro'])}</p>
<div class="verdict-box">
  <p class="kicker">The short answer</p>
  <p>{esc(g['verdict'])}</p>
</div>
{secs}
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
           "mainEntityOfPage": BASE + "guides/" + g["slug"] + ".html"},
          dict(crumbs_ld([("Home", "index.html"), ("Guides", "guides.html"),
                          (g["title"], "guides/" + g["slug"] + ".html")]),
               **{"@context": "https://schema.org"})]
    BUILT.append(page(f"guides/{g['slug']}.html", f"{g['title']} — {SITE}",
                      g["sub"], body, jsonld=ld))


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
  several: preset counts, accessory counts, top temperature, wattage, capacity units and warranty
  length. We do not average them, pick the flattering one, or quietly drop the awkward one.</p>

<h2>How the money works</h2>
<p>Outbound product links carry our Amazon Associate tag and are marked
  <strong>(paid link)</strong> next to the button, with <code>rel="sponsored nofollow"</code> on the
  anchor, per Google's guidance (S04). The disclosure statement sits under the masthead on every page
  and repeats in the footer, per Amazon's Operating Agreement Section 5 (S01) and FTC guidance (S03).
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
         what="Eight guides built from real buying decisions, each added to the sitemap and the RSS "
              "feed, each ending in a verdict.",
         why="Long-tail question queries are how a small site earns its first organic traffic. A "
             "guide that answers one question beats a listicle.",
         impact="High — organic traffic", effort="Done",
         status="Shipped", verify="guides.html lists eight; sitemap.xml and feed.xml include all eight."),
    dict(id="SG-03", title="Measure clicks before optimising anything",
         what="Five defined events, counted locally with no cookies and no third party, exportable "
              "to CSV by the reader or the owner.",
         why="Optimising without a click count is guesswork. Doing it with a tracker would be worse.",
         impact="High — every later decision", effort="Done",
         status="Shipped", verify="disclosure.html lists the five events; assets/app.js implements them."),
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
              "working on-site search.",
         why="A crawler needs one canonical address per page and a reason to rank it. Duplicate "
             "hosts and dead search pages waste both.",
         impact="High — findability", effort="Done", status="Shipped",
         verify="sitemap.xml lists every page; three JSON-LD blocks on product pages; search.html reads a generated index."),
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
  <caption>Sixteen proposals with honest status. "Shipped" means it is live and verifiable now.</caption>
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
                      "Sixteen proposals for this site, with honest status, ranked before anything "
                      "is built. Review the shortlist and choose a path.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Decision Center", "url": BASE + "suggestions.html"}))


# ---- questions
QUESTIONS = [
    ("Q-01", "Which product and ASIN did you intend each supplied link to represent?",
     "Intent is owner-only. Observed short-link results are not a guarantee of a stable destination; P-04 was not reproduced in the latest recorded check.",
     "Confirm the intended product and ASIN for each submitted URL. Keep that answer separate from the dated redirect observation and direct listing reference.",
     "Special Link validation (FLG-001, FLG-012)", "Owner", "Not obtained"),
    ("Q-02", "Is the Associate ID shopnow047c-20 issued, active and approved?",
     "Only Associates Central can answer this. No public page shows account status.",
     "Sign in to Associates Central and check Account Settings, then look for any click in the "
     "tracking report.",
     "Whether any of this earns anything (FLG-010)", "Owner", "Not verifiable externally"),
    ("Q-03", "Do the supplied link.amazon URLs meet Associates link requirements?",
     "Amazon's policies describe conditions for redirecting and improperly formatted links, but this site has not determined whether each submitted URL meets them.",
     "Ask Associates support about the exact URLs and keep the answer with the dated redirect tests. Do not label a supplied short link invalid based on a failed or checkpointed attempt.",
     "Link-format decision (FLG-003, FLG-015)", "Amazon support", "Unresolved"),
    ("Q-04", "Did the one-per-product link test pass?",
     "A tag that is not recorded earns nothing, and you cannot see that from outside the account.",
     "Click one tagged link per product while signed in. Check each appears in the tracking report "
     "with the right ASIN.",
     "Scaling traffic (FLG-004)", "Owner", "Pending test"),
    ("Q-05", "Should the live GitHub Pages URL remain canonical, or would you prefer a custom domain?",
     "The Pages project URL is live and already used by the canonical tags. The GitHub Pages API reports no custom CNAME; the current host is not a placeholder (FLG-006).",
     "This is an optional brand/domain choice. If a custom domain is selected, configure it and update canonicals, sitemap, and feed together. Search Console ownership is a separate setup step.",
     "Optional domain migration, not indexing on the current host (SG-14)", "Owner", "Current host live; custom-domain choice open"),
    ("Q-06", "Who is the editor of record?",
     "FTC guidance treats an implied experience claim as a problem. A byline needs a real person "
     "behind it.",
     "Name a person and describe the actual review process, or keep the current explicit statement "
     "that there is no hands-on test.",
     "Publication polish (FLG-032)", "Owner", "Blank"),
    ("Q-07", "What publishing cadence can actually be sustained?",
     "Cadence compounds; a burst followed by silence does not.",
     "Check what is realistic per week. One guide a week is the working assumption; confirm or "
     "revise.",
     "Content planning (SG-16)", "Owner", "Assumed, not confirmed"),
    ("Q-08", "Where would a privacy-reviewed site-wide analytics endpoint live, if one is wanted?",
     "Current events are browser-local aggregate counts. They do not provide cross-visitor totals, and GitHub Pages does not accept event writes.",
     "Choose a host, data-minimization plan, and retention window before collecting any server-side events. No endpoint is configured now.",
     "Site-wide measurement (FLG-010)", "Owner", "No endpoint"),
    ("Q-09", "Do you want to verify a Search Console property or add an email reader-capture channel?",
     "The RSS feed is available. No Search Console property has been verified and no email provider has been chosen.",
     "Use the official Search Console ownership instructions (S24) if an owner chooses to verify the property; separately decide whether email capture and a privacy notice are wanted.",
     "Owner-approved reader-capture and Search Console setup (SG-10)", "Owner", "RSS only; other choices open"),
    ("Q-10", "Which listing contradictions can be resolved with the maker?",
     "The open records include conflicting preset/accessory counts, temperature and power, capacity units, and warranty wording.",
     "Check the current listing and maker's manual, or contact the maker about the exact wording. Until resolved, both statements remain visible and neither is chosen.",
     "Specification certainty (FLG-017 to FLG-022, FLG-031, FLG-034)", "Makers", "Open"),
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
  <p>Fourteen questions, grouped by who can answer them. Six need the owner's account access or a
    yes/no decision. Four need a seller to clarify a listing that contradicts itself. Two need Amazon
    support. Two are editorial choices that only the owner can make.</p>
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

<h2>What the records support</h2>
<ul>
  <li><strong>Short-link observations are recorded separately from direct listing references and intent.</strong>
    One supplied link (P-04) returned a checkpoint rather than a product page on the latest recorded
    check; do not treat the direct listing as proof of that redirect.</li>
  <li><strong>Published product facts link to the official listing used as their source</strong> on
    {TODAY}. Values that were not in the fetched text stay blank, and conflicts stay flagged. See the
    <a href="sources.html">source register</a>.</li>
  <li><strong>The compliance rules are public and quoted.</strong> Amazon's Operating Agreement
    Section 5, Program Policies 2(a) and 2(b), FTC disclosure guidance and Google's outbound-link
    guidance are all linked with the exact wording used.</li>
  <li><strong>USDA publishes the minimum internal temperatures</strong> used in the thermometer
    guides, and that page is linked rather than paraphrased.</li>
</ul>

<h2>What we deliberately do not know</h2>
<p>Search volume for any topic, conversion rate for any product, whether a given product is better
  than another, and what any of these appliances is like to actually use. Four of those require tools
  or access we do not have. The fourth requires buying the products, and this site does not pretend
  it did.</p>
<p class="cta"><a class="btn" href="suggestions.html">Take the shortlist to the Decision Center</a></p>
"""
    BUILT.append(page("questions.html", f"Open Questions — {SITE}",
                      "Fourteen questions that must be answered before a decision can reasonably be "
                      "made, with how to discover each missing fact and what it blocks.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Open Questions", "url": BASE + "questions.html"}))


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
    <li><strong>Conflicts</strong> &mdash; places where a listing says two different things. Six of
      them. These are the ones most likely to affect a buying decision.</li>
    <li><strong>Unverified</strong> &mdash; values we could not confirm, so they are blank rather than
      filled in.</li>
    <li><strong>Policy</strong> &mdash; things deliberately absent for compliance reasons: prices,
      ratings, product photography.</li>
    <li><strong>Open</strong> &mdash; operational gaps that need an account or a decision.</li>
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
  {len(SOURCES)} dated sources cover program policy, platform and government guidance, the five product
  listings, and the supplied short-link observations.</p>

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
  <caption>Source register. The "used for" column names the exact point taken from each source.</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">What it supports</th>
    <th scope="col">Wording relied on</th><th scope="col">Read on</th></tr></thead>
  <tbody>{rows}</tbody>
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
                      f"{len(SOURCES)} dated sources, with the point each one supports.",
                      body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                                    "name": "Sources", "url": BASE + "sources.html"}))


# ---- executive summary
def build_exec():
    rows = "".join(
        f"<tr><td class=\"nowrap\">{p['id']}</td><td><strong>{esc(p['brand'])}</strong></td>"
        f"<td>{esc(p['cat'])}</td><td>{esc(p['observed'] or '— not confirmed (FLG-012)')}</td>"
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
  <div><span class="statnum">8</span><span class="statlabel">guides published</span></div>
  <div><span class="statnum">{len(FLAGS)}</span><span class="statlabel">flags, all public</span></div>
  <div><span class="statnum">0</span><span class="statlabel">prices or ratings shown</span></div>
</div>

<h2>1. What exists now</h2>
<p>A static publication site deployable straight to GitHub Pages: a front page that leads with
  products, two category pages, five product pages, eight question-shaped guides, a comparison table
  aligned by field, an on-site browser search that renders results as text, JSON-LD on every page,
  a sitemap, an RSS
  feed, and a disclosure strip under the masthead on every page. Alongside it sit the internal
  records: the <a href="suggestions.html">Decision Center</a>, the
  <a href="questions.html">Open Questions</a> register, the
  <a href="flagged.html">flag register</a>, the <a href="sources.html">source register</a>, and an
  intentionally empty <a href="campaign-ledger.html">campaign ledger</a>.</p>

<h2>2. The five product records and current listing references</h2>
<table class="exec">
  <caption>Observed short-link targets are shown only where reproduced. P-04 is unconfirmed; its direct
    listing reference is not represented as an observed redirect. Intended ASINs remain blank (FLG-001).</caption>
  <thead><tr><th scope="col">ID</th><th scope="col">Brand</th><th scope="col">Category</th>
    <th scope="col">Observed short-link target</th><th scope="col">Model on listing</th>
    <th scope="col">Direct listing reference</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>3. What the source record supports</h2>
<ul>
  <li>Each published listing fact has an official source link and a check date. Details missing from
    the fetched text remain blank; conflicting statements remain flagged.</li>
  <li>The program-policy, FTC, Google, GitHub Pages, and USDA references are linked in the
    <a href="sources.html">source register</a>.</li>
  <li>Food-safety temperatures are linked to the USDA FSIS chart, not attributed to a product listing.</li>
  <li>Short-link redirect behavior is not guaranteed by a single observation. P-04 was not reproduced
    in the latest recorded check; compliance status remains unresolved.</li>
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
  <li><strong>Certification.</strong> NIST and NSF appear on the listings. No certificate or test
    report has been seen (FLG-035).</li>
  <li><strong>Hands-on experience.</strong> None. Nothing on this site implies it was tested
    (FLG-032).</li>
</ul>

<h2>5. Listing conflicts that affect a buying decision</h2>
<table class="exec">
  <thead><tr><th scope="col">Flag</th><th scope="col">Product</th><th scope="col">Contradiction</th>
    <th scope="col">Official source</th></tr></thead>
  <tbody>
    <tr><td>FLG-021</td><td>Emeril 26 QT</td><td>24 presets in the title, 25 in About this item</td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow">Amazon listing</a></td></tr>
    <tr><td>FLG-031</td><td>Emeril 26 QT</td><td>Six accessories in the title, seven in Configuration, six named</td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow">Amazon listing</a></td></tr>
    <tr><td>FLG-018</td><td>Chefman 8 Qt</td><td>400 °F max in the spec field, 450 °F Hi-Fry in the title</td><td><a href="https://www.amazon.com/dp/B08DKYBTPH" rel="sponsored nofollow">Amazon listing</a></td></tr>
    <tr><td>FLG-017</td><td>Chefman 8 Qt</td><td>1700 W in the spec fields, 1000 W in About this item</td><td><a href="https://www.amazon.com/dp/B08DKYBTPH" rel="sponsored nofollow">Amazon listing</a></td></tr>
    <tr><td>FLG-034</td><td>Chefman 6 Qt</td><td>6 quarts in the title, 6 liters in the capacity field</td><td><a href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored nofollow">Amazon listing</a></td></tr>
    <tr><td>FLG-019</td><td>CHEF iQ Sense</td><td>Current and earlier warranty statements differ</td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z" rel="sponsored nofollow">Amazon listing</a></td></tr>
  </tbody>
</table>

<h2>6. Owner-level setup still open</h2>
<p>Associates Central access is needed to confirm the tracking ID and test one tagged link per product
  (Q-02, Q-04). Search Console setup and any reader-capture choice remain open (Q-09); this site has
  not accessed Search Console data. GitHub Pages cannot receive event writes, so site-wide counters
  require a separately chosen host and privacy policy (Q-08). The current Pages URL is canonical;
  choosing a custom domain is optional. No traffic, conversion, or revenue effect is forecast.</p>

<h2>7. Honest position on revenue</h2>
<p>No commission rate, site-wide click count, order total, conversion rate or revenue figure is
  presented, because no authorized first-party report has been supplied. The
  <a href="campaign-ledger.html">campaign ledger</a> is empty by design. An empty ledger means no
  report was entered; it does not mean there were zero visits, clicks, or orders. Any future row must
  carry its report date and source, and no forecast will be substituted for missing data.</p>

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
<p>Five events are counted as aggregate totals in the reader's browser: <code>page_view</code>,
  <code>outbound_click</code>, <code>guide_read</code>, <code>search</code> and
  <code>suggestion_rank</code>. No raw search term or event-by-event timeline is stored, and nothing is
  transmitted to a server. These counts describe only this browser, not site-wide traffic, and are
  not a substitute for an authorized first-party report.</p>
<p>Local outbound product clicks in this browser: <span id="localClicks">0</span>.
  <button type="button" id="exportClicks" class="ghostbtn">Export local click counts (CSV)</button>
  These are convenience counters, not Associate reports, orders, or conversions. The export is for
  this browser only.</p>

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
<p>The five events below are counted locally in this browser. The measurement record stores aggregate
  counts only; it does not retain raw search terms, a page-by-page event timeline, timestamps, referrers,
  IP addresses, or decision text.</p>
<table class="events">
  <thead><tr><th scope="col">Event</th><th scope="col">Fires when</th><th scope="col">What is counted</th></tr></thead>
  <tbody>
    <tr><td><code>page_view</code></td><td>A page loads</td><td>One aggregate increment; no page path is attached</td></tr>
    <tr><td><code>outbound_click</code></td><td>A tagged product link is clicked</td>
      <td>An aggregate total and product ID only</td></tr>
    <tr><td><code>guide_read</code></td><td>A guide page loads</td><td>A guide-load count, not proof that its text was read</td></tr>
    <tr><td><code>search</code></td><td>A non-empty search is submitted and evaluated</td>
      <td>One aggregate increment; the query and result text are not stored</td></tr>
    <tr><td><code>suggestion_rank</code></td><td>A proposal is moved in the Decision Center</td>
      <td>One aggregate increment; the chosen order is stored separately in this browser</td></tr>
  </tbody>
</table>
<p>These counters are not site-wide analytics and are not sent to us. They persist in this browser's
  local storage until the site's data is cleared, and can be exported as counts:
  <button type="button" id="exportEvents" class="ghostbtn">Export aggregate event counts (CSV)</button>.</p>
<p>The suggestion ranking and decision worksheet are separate local browser data. The worksheet may
  contain text you choose to enter; it is not transmitted, and you can export or clear it from the
  Decision Center. No server-side analytics endpoint is deployed. GitHub Pages is a static host; its
  <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#data-collection">host documentation</a>
  says visitor IP addresses are logged for security purposes. That host-level logging is separate
  from the counters described here.</p>
<p>With JavaScript enabled, the built-in header search carries a one-time query in a URL fragment,
  which browsers do not send in the HTTP request, and clears it after the results load. A legacy URL
  containing <code>?q=</code> or the no-JavaScript form fallback may include the query in the request
  URL and ordinary host logs. Do not include sensitive personal information in a search.</p>

<h2>Product-intent records</h2>
<p>For each of the five submitted links, the <em>intended</em> ASIN and the <em>observed</em> redirect
  target are stored in separate fields on the product page and are never merged. The observed target
  is a dated observation, not confirmation of the owner's intended product or a guarantee of a stable
  redirect. Each product page links to the direct listing used as its reference.</p>

<h2>Cookies, and what we do not use</h2>
<ul>
  <li>No advertising cookies, retargeting, social pixels, or fingerprinting.</li>
  <li>No third-party analytics script, pixel, or tag manager.</li>
  <li>No account, login, or email capture on this site.</li>
  <li>Clicking an Amazon link leaves this site; Amazon's privacy practices then apply.</li>
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
  The process is written out on the <a href="how-we-choose.html">How we choose</a> page.</p>
<p><strong>What the writer has not done:</strong> cooked with any of these appliances, measured any of
  them, or seen a certification document. No page on this site claims otherwise.</p>

<h2>Why only five products</h2>
<p>Because those are the five links this site was asked to cover. There is no pretence of covering the
  market, no "top ten" list, and no ranking against products that were never examined. Where a guide
  would normally say "consider alternatives", it says instead that the site only covers these
  five.</p>

<h2>Corrections</h2>
<p>Listings change. If a value here no longer matches the official listing, that is a correction to be
  made, not an argument to be had. Every flag on the
  <a href="flagged.html">Flagged for Review</a> page has a source link and a suggested resolution,
  and corrections are dated rather than quietly applied.</p>

<h2>Artwork and trademarks</h2>
<p>All illustrations on this site are original CSS and inline SVG drawn for it. No Amazon product
  photography is used anywhere, because the licence for those images runs through Amazon's own terms
  (FLG-007). Product names, Amazon and Amazon Associates are trademarks of Amazon.com, Inc. or its
  affiliates. This site is not endorsed by Amazon, and nothing here implies that Amazon sponsors or
  approves it.</p>

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
                  ("Decision Center", "suggestions.html",
                   "Proposals for this site, ranked before anything is built", "page"),
                  ("Open Questions", "questions.html",
                   "What has to be answered before a decision can be made", "page"),
                  ("Flagged for Review", "flagged.html",
                   "Every conflict and unverified value with its source", "page"),
                  ("Sources", "sources.html", "Dated official sources behind every published claim", "page"),
                  ("Disclosure and privacy", "disclosure.html",
                   "Affiliate disclosure, price policy, and the five measured events", "page")]:
        index.append({"t": extra[0], "u": extra[1], "d": extra[2], "k": extra[3]})
    # Prevent a title in the JSON index from closing its script element.
    idx = (json.dumps(index, ensure_ascii=False)
           .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))
    body = f"""
{breadcrumb([("Home", "index.html"), ("Search", None)])}
<h1>Search</h1>
<form class="searchpage" action="search.html" method="get" role="search">
  <label class="sr" for="sq">Search products, guides and records</label>
  <input id="sq" name="q" type="search" placeholder="Try: two baskets, 450, wireless, capacity">
  <button type="submit">Search</button>
</form>
<p class="small" id="searchMeta">Search runs in this browser. With JavaScript enabled, the query stays in a URL fragment
  and is cleared after results load; it is not saved in the local measurement counters.</p>
<div id="results" class="results" aria-live="polite"></div>
<script type="application/json" id="searchIndex">{idx}</script>
<h2>Start with a buyer question</h2>
<div class="grid">
  <article class="card"><h3><a href="guides/basket-vs-oven.html">Basket or oven-style?</a></h3>
    <p>Compare footprint, access, and the way you load it.</p></article>
  <article class="card"><h3><a href="guides/instant-vs-wireless.html">Instant-read or wireless?</a></h3>
    <p>Choose by when and where you want a temperature reading.</p></article>
  <article class="card"><h3><a href="compare.html">Compare all five</a></h3>
    <p>Seller-stated details, source links, and unresolved conflicts.</p></article>
</div>
"""
    BUILT.append(page("search.html", f"Search — {SITE}",
                      "Search the products, guides and records on this site. Matching happens in "
                      "your browser; nothing is sent to a server.",
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


def build_sitemap(pages):
    urls = "".join(
        f"  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'weekly' if p in ('index.html', 'guides.html', 'shop.html') else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if p == 'index.html' else '0.8' if p.startswith(('guides/', 'products/')) else '0.6'}</priority></url>\n"
        for p in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE}sitemap.xml\n")


# --------------------------------------------------------------------------- main
def main():
    build_home()
    build_shop()
    build_category(
        "air-fryers.html", "Air Fryers",
        "Air fryers: two baskets, one big basket, or a whole oven",
        "Compare three layouts: a two-basket drawer, a single basket, and a French-door countertop oven. "
        "The product pages link to the seller-stated dimensions, fit examples, and unresolved conflicts.",
        [("guides/basket-vs-oven.html", "Basket or oven-style: what to compare first",
          "Footprint, doors, and how you load it."),
         ("guides/capacity-checklist.html", "A checklist for comparing capacity",
          "Quarts are not servings."),
         ("guides/cleanup-counter-space.html", "Cleanup and counter-space trade-offs",
          "Dishwasher-safe is not the same as easy."),
         ("guides/small-kitchen-air-fryer.html", "Air fryer for a small kitchen",
          "Measure depth, access, and the storage spot."),
         ("guides/air-fryer-thanksgiving.html", "Planning a holiday meal with an air fryer",
          "Use listing fit examples without extrapolating.")],
        ["P-01", "P-03", "P-02"])
    build_category(
        "meat-thermometers.html", "Meat Thermometers",
        "Meat thermometers: instant-read or walk-away",
        "The product records describe a hand-held instant-read model and a separate wireless probe "
        "system. Compare setup, connectivity, care instructions, and the claims made on each listing.",
        [("guides/instant-vs-wireless.html", "Instant-read or wireless: which workflow fits?",
          "Compare when and how you take a reading."),
         ("guides/thermometer-accuracy.html", "How to assess thermometer accuracy claims",
          "Separate seller-stated tolerance from independent test evidence.")],
        ["P-04", "P-05"])
    for p in PRODUCTS:
        build_product(p)
    build_compare()
    build_guides_index()
    for g in GUIDES:
        build_guide(g)
    build_how()
    build_suggestions()
    build_questions()
    build_flagged()
    build_sources()
    build_exec()
    build_ledger()
    build_disclosure()
    build_about()
    build_search()
    build_feed()
    pages = sorted(BUILT) + ["sitemap.xml", "feed.xml"]
    build_sitemap(sorted(BUILT))
    print(f"built {len(BUILT)} pages")
    for p in sorted(BUILT):
        print("  ", p)


if __name__ == "__main__":
    main()
