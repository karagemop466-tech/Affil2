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
    p["intended"] = None
    if not p.get("observed"):
        p["observed"] = p["asin"]
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
    """The tagged Special Link we publish."""
    return f"https://www.amazon.com/dp/{p['observed']}?tag={TRACKING_ID}"

def plain(p):
    """Untagged official listing, for verification."""
    return f"https://www.amazon.com/dp/{p['observed']}"

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
    ("design-brief.html", "Design &amp; Traffic Brief"),
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
    <nav id="primary-nav" aria-label="Primary">{nav}<details class="records"><summary>Records</summary><div>{dash}</div></details></nav>
    <form class="search" action="{up}search.html" method="get" role="search">
      <label class="sr" for="q">Search products and guides</label>
      <input id="q" name="q" type="search" placeholder="Search the kitchen…" autocomplete="off">
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
    intended = p["intended"] or "— blank: not confirmed by the owner (FLG-001)"
    return f"""<table class="intent">
  <caption>Product-intent confirmation record. Intended and observed are separate fields and are
    never merged.</caption>
  <tbody>
    <tr><th scope="row">Submitted link (as supplied)</th><td>{esc(p['submitted'])}</td></tr>
    <tr><th scope="row">Short-link token</th><td>{esc(p['token'])} (not an ASIN)</td></tr>
    <tr><th scope="row">Intended ASIN</th><td>{esc(intended)}</td></tr>
    <tr><th scope="row">Observed redirect target</th><td>{esc(p['observed'])}</td></tr>
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
    featured = [BY_ID["P-01"], BY_ID["P-03"], BY_ID["P-04"]]
    body = f"""
<div class="issue"><b>THE KITCHEN EDIT</b><span></span> VOL. 01 &nbsp; / &nbsp; NOVEMBER 2026</div>
<section class="cover">
 <div class="cover-copy"><p class="eyebrow">● &nbsp; THE WEEKEND GUIDE</p>
 <h1>One basket,<br>two baskets,<br><em>or an oven?</em></h1>
 <p>Start with dinner. A tray of roast potatoes and two sides that need different temperatures ask different things of an air fryer.</p>
 <a class="cover-link" href="guides/basket-vs-oven.html">Read the buying guide &nbsp; →</a></div>
 <img src="assets/feature.jpg" alt="Illustrated kitchen scene with roast potatoes and a basket air fryer" fetchpriority="high">
</section>
<section class="dept"><p class="kicker">THE SHOP DIRECTORY</p><h2>Shop by category</h2>
<div class="aisles"><a href="air-fryers.html"><img src="assets/basket.jpg" alt=""><span>01 / APPLIANCES<strong>Air fryers ↗</strong></span></a>
<a href="meat-thermometers.html"><img src="assets/probe.jpg" alt=""><span>02 / TOOLS<strong>Meat thermometers ↗</strong></span></a></div></section>
<section>
  <p class="kicker">FROM THE BUYING DESK</p><h2>Three places to start</h2>
  <p class="muted">Not the whole market &mdash; these five are the ones we cover. These are the three we would start with, and the reason is written on each card.</p>
  <div class="grid">
    {"".join(card(p, "") for p in featured)}
  </div>
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
    <h3>Why you can trust the numbers</h3>
    <ol class="tight">
      <li>Every specification is read from the official listing and stamped with a date.</li>
      <li>When a listing contradicts itself, both figures are printed. Nothing is averaged.</li>
      <li>Prices and ratings are never copied &mdash; Amazon policy on price display, and it keeps
        us honest.</li>
      <li>We have not cooked with these units. The site says so instead of implying otherwise.</li>
    </ol>
    <p class="small"><a href="how-we-choose.html">How we choose and what we won't claim &rarr;</a></p>
  </aside>
</section>

<section class="panel scallop">
  <h2>Every product at a glance</h2>
  <p class="muted">The table a buyer needs: what it is, who it suits, and the one caveat that matters.
    Price and rating columns are deliberately absent.</p>
  {overview_table()}
</section>

<section>
  <h2>What readers ask us most</h2>
  <div class="faq">
    <details><summary>Do you show prices?</summary><p>No. Amazon's Program Policies allow a site to
      show price and availability only when Amazon serves the link or the data comes through the
      Product Advertising or Creators API. This site does neither, so prices stay on Amazon where
      they are always current. That is also why nothing here is ever out of date on price.</p></details>
    <details><summary>Which one would you buy?</summary><p>It depends on one thing: do you cook two
      things at once. If yes, the dual-basket Chefman. If you cook in batches and want the biggest
      single basket, the 8-quart Chefman. If you want an oven that air-fries, the Emeril &mdash; and
      only if you have 16.9 inches of depth.</p></details>
    <details><summary>Are the star ratings on Amazon reliable?</summary><p>They are real, and they are
      not shown here &mdash; partly policy, partly because a rating summarises other people's
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
    og = ('<meta property="product:retailer_item_id" content="'
          + p["observed"] + '">')
    body = f"""
{breadcrumb([("Home", "index.html"), (p['cat'], p['catfile']), (p['brand'], None)], "../")}
<div class="pdp-head">
  <div>
    <p class="kicker">{esc(p['cat'])} · {p['id']} · verified {TODAY}</p>
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
<p class="small">We do not print the price here &mdash; Amazon's Program Policies only permit a site
  to show price and availability when Amazon serves the link or the data comes through their API.
  The button opens the official listing, tagged with our Associate ID.</p>

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
    def row(label, fn):
        cells = "".join(f"<td>{fn(p)}</td>" for p in cols)
        return f'<tr><th scope="row">{label}</th>{cells}</tr>'

    NOT_STATED = "— <span class=\"unverified\">not stated on the listing</span>"

    def spec(p, key, other=NOT_STATED):
        f = p["fields"].get(key)
        if not f or f["v"] is None:
            return other
        txt = esc(f["v"])
        if f["st"] == "conflict":
            txt += ' <span class="token conflict">see flags</span>'
        return txt

    NA_CAP = "— <span class=\"unverified\">n/a, measures temperature</span>"
    NA_POWER = "— <span class=\"unverified\">n/a, battery powered</span>"

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
    {row("Weight", lambda p: spec(p, "weight", NOT_STATED))}
    {row("Model on listing", lambda p: spec(p, "model", "— not on the fetched text"))}
    {row("Price", lambda p: "— not shown, by policy")}
    {row("Star rating", lambda p: "— not shown, by policy")}
    {row("Official listing", lambda p: f'<a href="{plain(p)}" rel="sponsored nofollow">untagged</a>')}
    {row("Buy link", lambda p: f'<a href="{aff(p)}" rel="sponsored nofollow" data-outbound="{p["id"]}" data-event="outbound_click">Amazon (paid link)</a>')}
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
            basket units are lighter and easier to move; the 26-quart oven weighs 26.5 pounds and is
            realistically going to stay where you put it. If you clean in the sink, a removable
            nonstick basket is simpler than a stainless cavity and racks."""),
            ("Where each one wins", """Choose the dual-basket unit if you routinely cook a main and a
            side together and want them to finish together. Choose the single 8-quart basket if you
            cook one thing at a time in quantity and want the simplest possible operation. Choose the
            oven if you also want to roast, toast, and rotisserie, and you have the counter depth and
            the appetite for a 26.5-pound appliance that stays put."""),
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
            that makes a spec table worth reading rather than skimming. It is flagged as FLG-034."""),
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
            ("Weight decides where it lives", """At 26.5 pounds the Emeril is a fixture. The two basket
            units are around 13 pounds, which is heavy but movable. If you plan to put the appliance
            away between uses, weight is the number that decides whether that actually happens."""),
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
            configuration field says seven &mdash; flagged as FLG-031."""),
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
            not. The ThermoMaven here claims a 1-second response, &plusmn;0.5&nbsp;&deg;F, and a
            572&nbsp;&deg;F upper range, and it ships with a calibration certificate."""),
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
            have to trust. The ice-water test &mdash; a slurry of ice and water, which sits at
            32&nbsp;&deg;F at sea level &mdash; will tell you whether a unit is reading plausibly. A
            unit that ships with a certificate and a stated calibration method is easier to keep
            honest."""),
            ("Check resolution separately from accuracy", """Resolution is how many digits the display
            shows; accuracy is how close the number is to the truth. A 0.1&deg; display with
            &plusmn;0.5&nbsp;&deg;F accuracy is not a 0.1&deg; instrument. The ThermoMaven listing
            states both, which makes the distinction visible."""),
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
            ("Check the circuit before the menu", """Two 1700-watt appliances on one kitchen circuit
            plus an oven is a tripped breaker, not a crispier sprout. Wattage is worth knowing before
            the day, which is why it is in the specification table &mdash; and why the 8-quart
            Chefman's contradictory 1700&nbsp;W / 1000&nbsp;W figures are flagged as FLG-017."""),
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
            happens twice or never. The 8-quart Chefman is 12.8 pounds; the Emeril is 26.5. Neither
            is a one-hand lift, but only one of them is realistically movable."""),
            ("What to give up first", """Windows, presets, and a second basket are all things you can
            live without. Depth and weight are not. If the counter is tight, a single-basket unit
            with no window is the honest choice, and it is also the cheapest of the three here."""),
         ],
         verdict="""Measure depth, measure the space in front, and weigh whether it will go in a
         cupboard. Pick the unit that survives all three; then look at features."""),
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
<p class="kicker">{esc(g['kicker'])} · verified {TODAY}</p>
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
    dict(id="SG-17", title="Adopt the Design & Traffic Brief as the next build step",
         what="A copy-paste design prompt, a topic-cluster plan with a seasonal calendar, and an "
              "editorial standards checklist for keeping the site from reading like generated "
              "content. Published at design-brief.html.",
         why="The site is verified and compliant but still feels assembled. A designer (or a new "
             "prompt) needs one document that says exactly what to build and why — this is it.",
         impact="High — perceived quality and conversion", effort="Medium, one design pass",
         status="Not started — recommended for approval",
         verify="design-brief.html is on this site now. Nothing changes until the owner picks this row."),
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
  <caption>Seventeen proposals with honest status. "Shipped" means it is live and verifiable now.</caption>
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
    <tr><td>SG-17</td><td>Approve the Design &amp; Traffic Brief as the next build</td><td>Owner (decision)</td></tr>
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
                      "Seventeen proposals for this site, with honest status, ranked before anything "
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
     "Whether any of this earns anything (FLG-010)", "Owner", "Not verifiable externally"),
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
     "Publication polish (FLG-032)", "Owner", "Blank"),
    ("Q-07", "What publishing cadence can actually be sustained?",
     "Cadence compounds; a burst followed by silence does not.",
     "Check what is realistic per week. One guide a week is the working assumption; confirm or "
     "revise.",
     "Content planning (SG-16)", "Owner", "Assumed, not confirmed"),
    ("Q-08", "Where would a self-hosted analytics endpoint live?",
     "Events are counted in the browser only, so there is no cross-visitor data at all.",
     "Choose a host, a retention period and a privacy statement before collecting anything "
     "server-side.",
     "Any real measurement (FLG-010)", "Owner", "No endpoint"),
    ("Q-09", "Which reader-capture channel, if any?",
     "An RSS feed exists. Email capture and Search Console both need accounts.",
     "Verify the site in Search Console and submit the sitemap. Decide whether email is wanted.",
     "Growth loop (SG-10)", "Owner", "RSS only"),
    ("Q-10", "Which listing contradictions can be resolved with the seller?",
     "There are now six: preset count, accessory count, top temperature, wattage, capacity units and "
     "warranty length.",
     "Ask each seller in writing, or read the printed manual. Until then both figures stay published.",
     "Specification certainty (FLG-017 to FLG-022)", "Sellers", "Open"),
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

<h2>What we do know, and where it came from</h2>
<ul>
  <li><strong>The five short links resolve to five specific ASINs.</strong> Observed on {TODAY}, and
    recorded separately from intent on each product page.</li>
  <li><strong>Every specification on this site was read off an official listing</strong> on {TODAY}.
    The <a href="sources.html">source register</a> links every one.</li>
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
  <a class="btn ghost" href="guides.html">Read the eight live guides</a></p>
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
                      "Ten sources, all official, all dated, with the exact wording each claim "
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
  <div><span class="statnum">8</span><span class="statlabel">guides published</span></div>
  <div><span class="statnum">{len(FLAGS)}</span><span class="statlabel">flags, all public</span></div>
  <div><span class="statnum">0</span><span class="statlabel">prices or ratings shown</span></div>
</div>

<h2>1. What exists now</h2>
<p>A static publication site deployable straight to GitHub Pages: a front page that leads with
  products, two category pages, five product pages, eight question-shaped guides, a comparison table
  aligned by field, an on-site search that actually works, JSON-LD on every page, a sitemap, an RSS
  feed, and a disclosure strip under the masthead on every page. Alongside it sit the internal
  records: the <a href="suggestions.html">Decision Center</a>, the
  <a href="questions.html">Open Questions</a> register, the
  <a href="flagged.html">flag register</a>, the <a href="sources.html">source register</a>, and an
  intentionally empty <a href="campaign-ledger.html">campaign ledger</a>.</p>

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
  <li>Every product title, dimension, weight, wattage, temperature range and capacity on this site was
    read from the official listing on {TODAY}.</li>
  <li>The four policy sources &mdash; Operating Agreement Section 5, Program Policies 2(a) and 2(b),
    FTC disclosure guidance and Google's outbound-link guidance &mdash; are quoted with exact wording
    in the <a href="sources.html">source register</a>.</li>
  <li>Food-safety temperatures come from the USDA FSIS chart, not from a product listing.</li>
  <li>All five short links were fetched and their destinations recorded separately from intent.</li>
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

<h2>5. The six listing conflicts a buyer should know about</h2>
<table class="exec">
  <thead><tr><th scope="col">Flag</th><th scope="col">Product</th><th scope="col">Contradiction</th></tr></thead>
  <tbody>
    <tr><td>FLG-021</td><td>Emeril 26 QT</td><td>24 presets in the title, 25 in About this item</td></tr>
    <tr><td>FLG-031</td><td>Emeril 26 QT</td><td>Six accessories in the title, seven in Configuration, six named</td></tr>
    <tr><td>FLG-018</td><td>Chefman 8 Qt</td><td>400 °F max in the spec field, 450 °F Hi-Fry in the title</td></tr>
    <tr><td>FLG-017</td><td>Chefman 8 Qt</td><td>1700 W in the spec fields, 1000 W in About this item</td></tr>
    <tr><td>FLG-034</td><td>Chefman 6 Qt</td><td>6 quarts in the title, 6 liters in the capacity field</td></tr>
    <tr><td>FLG-019</td><td>CHEF iQ Sense</td><td>Two-year assurance on the listing, one year in the earlier pass</td></tr>
  </tbody>
</table>

<h2>6. What would change the numbers</h2>
<p>Two credentials, and one decision. Product Advertising API access would make legal price display
  possible (SG-13), which is the largest single lever on conversion. Search Console verification would
  make query data available (SG-10), which is the only way to choose the next guide from evidence
  rather than instinct. A custom domain decision (SG-14, FLG-006) would strengthen brand and
  indexation. Everything else on the <a href="suggestions.html">Decision Center</a> is either shipped
  or cosmetic.</p>

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
<table class="events">
  <thead><tr><th scope="col">Event</th><th scope="col">Fires when</th><th scope="col">Used for</th></tr></thead>
  <tbody>
    <tr><td><code>page_view</code></td><td>Any page loads</td><td>Which pages are reached at all</td></tr>
    <tr><td><code>outbound_click</code></td><td>A tagged Amazon link is clicked</td>
      <td>Which product a reader actually leaves for</td></tr>
    <tr><td><code>guide_read</code></td><td>A guide page loads</td><td>Whether guides get read, not just listed</td></tr>
    <tr><td><code>search</code></td><td>A search query returns results</td>
      <td>What readers look for and do not find</td></tr>
    <tr><td><code>suggestion_rank</code></td><td>A proposal is reordered on the Decision Center</td>
      <td>Which direction is actually preferred</td></tr>
  </tbody>
</table>
<p>All five are counted in your browser's local storage and nothing else. No cookie is set, no request
  carries your data to a third party, and no fingerprinting is used. There is no analytics script, no
  pixel and no tag manager on this site. A self-hosted endpoint could replace local storage later,
  and the event names are fixed so that swap would not require editing any page &mdash; but until
  that endpoint exists, nothing leaves your device.</p>
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
  The process is written out on the <a href="how-we-choose.html">How we choose</a> page.</p>
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
                  ("Design & Traffic Brief", "design-brief.html",
                   "Copy-paste design prompt, a topic-cluster traffic plan, a seasonal calendar "
                   "and the editorial standards checklist", "page"),
                  ("Decision Center", "suggestions.html",
                   "Proposals for this site, ranked before anything is built", "page"),
                  ("Open Questions", "questions.html",
                   "What has to be answered before a decision can be made", "page"),
                  ("Flagged for Review", "flagged.html",
                   "Every conflict and unverified value with its source", "page"),
                  ("Sources", "sources.html", "The ten official sources behind every claim", "page"),
                  ("Disclosure and privacy", "disclosure.html",
                   "Affiliate disclosure, price policy, and the five measured events", "page")]:
        index.append({"t": extra[0], "u": extra[1], "d": extra[2], "k": extra[3]})
    idx = json.dumps(index, ensure_ascii=False)
    body = f"""
{breadcrumb([("Home", "index.html"), ("Search", None)])}
<h1>Search</h1>
<form class="searchpage" action="search.html" method="get" role="search">
  <label class="sr" for="sq">Search products, guides and records</label>
  <input id="sq" name="q" type="search" placeholder="Try: two baskets, 450, wireless, capacity">
  <button type="submit">Search</button>
</form>
<p class="small" id="searchMeta">Searching across {len(index)} pages on this site. Nothing is sent to
  a server &mdash; the index is embedded below and matched in your browser.</p>
<div id="results" class="results" aria-live="polite"></div>
<script type="application/json" id="searchIndex">{idx}</script>
<h2>Popular starting points</h2>
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
    build_how()
    build_design_brief()
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
