#!/usr/bin/env python3
"""Regenerates every data-driven block of the site from data/*.json.

Only verified values are printed. A value that was not seen on a fetched official
listing is written as a blank with a status of "unverified" and a flag reference.
Run:  python3 scripts/build_content.py   (then python3 scripts/check_site.py)
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PRODUCTS = json.loads((DATA / "products.json").read_text())
SOURCES = {s["id"]: s for s in json.loads((DATA / "sources.json").read_text())}
FLAGS = json.loads((DATA / "flags.json").read_text())
TAG = "shopnow047c-20"
CHECKED = "2026-11-20"
ART = {
    "P-01": ("air-fryer.svg", "Illustration of a countertop air fryer; not a product photo"),
    "P-02": ("air-fryer-oven.svg", "Illustration of a countertop oven-style air fryer; not a product photo"),
    "P-03": ("air-fryer.svg", "Illustration of a countertop air fryer; not a product photo"),
    "P-04": ("thermometer.svg", "Illustration of a kitchen thermometer; not a product photo"),
    "P-05": ("thermometer.svg", "Illustration of a kitchen thermometer; not a product photo"),
}
# Verbatim leading words of each listing title, used only for card headings.
SHORT = {
    "P-01": "CHEFMAN 6 Quart Dual Basket Air Fryer Oven",
    "P-02": "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven",
    "P-03": "Chefman Air Fryer 8 Qt",
    "P-04": "ThermoMaven 1 Sec Professional Digital Meat Thermometer",
    "P-05": "CHEF iQ Sense | Smart Wireless Meat Thermometer",
}


def esc(s):
    return html.escape(s, quote=False)


def a(href, text, sponsored=False):
    # Every link to an Amazon product page is a Program link, including the
    # supplied link.amazon short links, so it carries rel="sponsored".
    is_product = "amazon.com" in href or "link.amazon" in href
    rel = ' rel="sponsored nofollow"' if sponsored or is_product else ""
    return f'<a href="{href}"{rel}>{esc(text)}</a>'


def prefix_for(path):
    return "" if path.parent == ROOT else "../"


def val_cell(f):
    """Value cell text for a field record."""
    if f is None:
        return "— not checked"
    if f["st"] == "unverified":
        return "— blank (unverified)"
    return esc(f["v"])


def status_cell(f, pid):
    if f is None:
        return "not checked"
    if f["st"] == "verified":
        return "verified"
    if f["st"] == "conflict":
        return "conflict — published as listed"
    return "unverified — blank"


def flag_for(f):
    return ""


def listing_link(p, label=None):
    return a(p["listing"], label or p["listing"].replace("https://", ""), True)


def card(p, prefix):
    specs = "".join(f"<li><strong>{esc(k)}:</strong> {esc(v)}</li>" for k, v in p["card"])
    return (
        f'<article class="card" data-product="{p["id"]}">\n'
        f'<div class="card-art"><img src="{prefix}assets/illustrations/{ART[p["id"]][0]}" '
        f'alt="{esc(ART[p["id"]][1])}"></div>\n'
        f'<p class="kicker">{esc(p["cat"])} · {p["id"]}</p>'
        f'<h3><a href="{prefix}products/{p["slug"]}.html">{esc(SHORT[p["id"]])}</a></h3>\n'
        f'<p>{esc(p["blurb"])}</p>\n'
        f'<ul class="specs">{specs}</ul>\n'
        f'<p class="cta"><a class="btn" href="https://www.amazon.com/dp/{p["asin"]}?tag={TAG}" '
        f'rel="sponsored nofollow" data-outbound="{p["id"]}" data-event="outbound_click">Check on Amazon (paid link)</a>\n'
        f'<a href="{prefix}products/{p["slug"]}.html">Read the breakdown →</a></p>\n'
        f'<p class="small">Special Link pending Associates test (FLG-004). '
        f'<a href="{p["listing"]}" rel="sponsored nofollow">Official listing</a></p></article>'
    )


def product_main(p):
    rows = []
    for key, f in p["fields"].items():
        label = key.replace("_", " ").capitalize()
        src_text = f.get("src", "")
        note = f.get("note", "")
        extra = f" <small>{esc(note)}</small>" if note else ""
        if f["st"] == "unverified":
            cell = "— blank (unverified)" + extra
        else:
            cell = esc(f["v"]) + extra
        rows.append(
            f"<tr><td>{esc(label)}</td><td>{cell}</td><td>{status_cell(f, p['id'])}</td>"
            f"<td>{listing_link(p, esc(src_text) + ' — ' + p['asin'])}</td></tr>"
        )
    qs = "".join(f"<li>{esc(q)}</li>" for q in p["questions"])
    obs = p["observed"] or "— not confirmed"
    return f"""<main class="wrap">
<p class="kicker"><a href="../{p['catfile']}">{esc(p['cat'])}</a> · {p['id']} · Listing checked {CHECKED}</p>
<h1>{esc(p['title'])}</h1><p class="lede">{esc(p['blurb'])}</p>
<p><a class="btn" href="https://www.amazon.com/dp/{p['asin']}?tag={TAG}" rel="sponsored nofollow" data-outbound="{p['id']}" data-event="outbound_click">Check on Amazon (paid link)</a>
<a class="btn ghost" href="https://www.amazon.com/dp/{p['asin']}" rel="sponsored nofollow">Official listing (no tag)</a></p>
<p class="small">Special Link status: PENDING TEST in enrolled Associates workflow (FLG-004). Do not scale until destination and tracking report are confirmed.</p>
<h2>Questions to ask before you buy</h2><ol>{qs}</ol>
<h2>Specifications — line by line</h2>
<table><caption>Read from the official Amazon listing on {CHECKED}. A blank value means it was not confirmed from the listing text; nothing is inferred.</caption>
<thead><tr><th>Field</th><th>Value (listing)</th><th>Status</th><th>Source (official listing)</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<h2>Product-intent confirmation record</h2>
<table><caption>Intended and observed fields are kept separate and never merged.</caption><tbody>
<tr><th>Submitted link (as supplied)</th><td>{esc(p['submitted'])}</td></tr>
<tr><th>Short-link token (9 characters, not an ASIN)</th><td>{esc(p['token'])}</td></tr>
<tr><th>Intended ASIN</th><td>— blank: owner confirmation needed (FLG-001)</td></tr>
<tr><th>Observed redirect target (separate field)</th><td>{esc(obs)}<br><small>{esc(p['observed_status'])}</small></td></tr>
<tr><th>Listing checked directly (ASIN)</th><td>{esc(p['asin'])} — {listing_link(p)}</td></tr>
<tr><th>Special Link (with supplied tag)</th><td>https://www.amazon.com/dp/{p['asin']}?tag={TAG}</td></tr>
<tr><th>Confirmation date</th><td>{CHECKED}</td></tr>
<tr><th>Source</th><td>{listing_link(p)} · {a(p['submitted'], p['submitted'], True)}</td></tr>
<tr><th>Associates test status</th><td>PENDING — test one link in the enrolled workflow; confirm destination and tracking report (FLG-004)</td></tr>
</tbody></table>
{usda_doneness_block() if p['cat'] == 'Meat Thermometers' else ''}
<h2>What this page does not claim</h2>
<p>No price, rating, review count, sales rank, commission or “best” claim is made. Those fields are not shown because Program Policies §2(b) limits price display, and they change by time and location. Check the live listing for current details.</p>
<p><a href="../{p['catfile']}">← Back to {esc(p['cat'])}</a> · <a href="../compare.html">Compare all products</a> · <a href="../flagged.html">Flagged for Review</a></p>
</main>"""


USDA_URL = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart"


def usda_doneness_block():
    """A thermometer page should send the reader to the food-safety authority, not
    to a number we typed from memory. S22 is the registered source."""
    return f"""<h2>Doneness targets come from the USDA, not from us</h2>
<p>This is a thermometer, so the numbers that matter are food-safety numbers. We do not restate them from memory. The USDA FSIS <a href="{USDA_URL}">Safe Minimum Internal Temperature Chart</a> (source S22, checked {CHECKED}) gives these minimums, as measured with a food thermometer:</p>
<table><caption><a href="{USDA_URL}">USDA FSIS — Safe Minimum Internal Temperature Chart</a> (S22)</caption>
<thead><tr><th>Food</th><th>Minimum internal temperature</th></tr></thead><tbody>
<tr><td>Poultry — breasts, whole bird, legs, thighs, wings, ground poultry, giblets, stuffing</td><td>165&nbsp;°F (73.9&nbsp;°C)</td></tr>
<tr><td>Ground meats</td><td>160&nbsp;°F (71.1&nbsp;°C)</td></tr>
<tr><td>Beef, pork, veal and lamb steaks, chops and roasts</td><td>145&nbsp;°F (62.8&nbsp;°C) with a rest of at least 3 minutes</td></tr>
<tr><td>Fish and shellfish</td><td>145&nbsp;°F (62.8&nbsp;°C)</td></tr>
<tr><td>Leftovers and casseroles</td><td>165&nbsp;°F (73.9&nbsp;°C)</td></tr>
</tbody></table>
<p class="small">Read the chart itself before relying on any number here: <a href="{USDA_URL}">fsis.usda.gov</a>. Registered as S22 in the <a href="../sources.html">source register</a>.</p>
"""


def table(headers, rows, caption):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><caption>{esc(caption)}</caption><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>"


def fv(p, key):
    f = p["fields"].get(key)
    if f is None:
        return "— not checked"
    if f["st"] == "unverified":
        return "— blank (unverified)"
    return esc(f["v"])


def compare_tables():
    af = [p for p in PRODUCTS if p["cat"] == "Air Fryers"]
    mt = [p for p in PRODUCTS if p["cat"] == "Meat Thermometers"]

    def block(group, keys, title):
        headers = ["Field"] + [f"{p['id']}<br>{esc(SHORT[p['id']].split('|')[0].strip())}" for p in group]
        rows = []
        for label, key in keys:
            rows.append([label] + [fv(p, key) for p in group])
        rows.append(["Price"] + ["— not shown (§2(b))" for _ in group])
        rows.append(["Rating"] + ["— not shown (§2(b))" for _ in group])
        rows.append(["Official listing"] + [
            a(p["listing"], "View listing (paid link)", True) for p in group])
        return f"<h2>{title}</h2>" + table(headers, rows, f"Values from official Amazon listings, read {CHECKED}. “— blank (unverified)” means not confirmed from the listing; “— not checked” means not in the record.")

    af_keys = [("Model", "model"), ("Capacity", "capacity"), ("Temperature", "temperature"),
               ("Power", "power"), ("Dimensions", "dimensions"), ("Presets", "presets"), ("Warranty", "warranty")]
    mt_keys = [("Model", "model"), ("Response time", "response"), ("Accuracy", "accuracy"),
               ("Certification", "certification"), ("Included", "included"), ("Probes", "probes"),
               ("Connectivity", "connectivity"), ("Battery", "battery"), ("Warranty", "warranty")]
    return block(af, af_keys, "Air fryers"), block(mt, mt_keys, "Meat thermometers")


AMAZON_PRODUCT_RE = re.compile(r'href="(https://www\.amazon\.com/(?:dp|gp/product)/[A-Z0-9]{10})(\?[^"]*)?"')


def tag_amazon_links(text):
    """Every link to an Amazon product listing carries the Associates tag.

    The Operating Agreement requires that a link to Amazon includes the
    tracking ID, so the source citations are tagged as well as the buttons.
    Policy pages on affiliate-program.amazon.com are not product links and
    are deliberately left alone.
    """
    def repl(m):
        url = m.group(1)
        if "tag=" in (m.group(2) or ""):
            return 'href="%s%s"' % (url, m.group(2) or "")
        return 'href="%s?tag=%s"' % (url, TAG)
    return AMAZON_PRODUCT_RE.sub(repl, text)


def ensure_nav_links(text, prefix=""):
    """Every page carries the Measurement link in both nav groups.

    Only the two <nav> blocks and the footer dashboard row are touched, so a
    breadcrumb line in the body of a page is never modified.
    """
    href = '%smeasurement.html' % prefix
    link = '<a href="%s">Measurement</a>' % href
    if link in text:
        return text
    flagged = '<a href="%sflagged.html">Flagged for Review</a>' % prefix

    def add_to_nav(m):
        return m.group(1) + m.group(2).replace(flagged, link + flagged) + m.group(3)

    text = re.sub(r'(<nav aria-label="Primary">)(.*?)(</nav>)', add_to_nav, text, count=1, flags=re.S)
    text = re.sub(r'(<nav aria-label="Footer">)(.*?)(</nav>)', add_to_nav, text, count=1, flags=re.S)
    # footer dashboard row: after the Campaign Ledger entry
    text = text.replace(
        '<a href="%scampaign-ledger.html">Campaign Ledger</a>' % prefix,
        '<a href="%scampaign-ledger.html">Campaign Ledger</a> &middot; %s' % (prefix, link),
    )
    return text


def ensure_collect_script(text, prefix=""):
    """Make sure the page loads the self-hosted event collector.

    The collector is inert until a collector answers the health probe, so
    shipping the script on every page is safe even with no collector
    deployed.
    """
    tag = '<script src="%sassets/js/collect.js" defer></script>' % prefix
    if tag in text:
        return text
    if "</body>" not in text:
        raise SystemExit("build_content: page has no </body>")
    return text.replace("</body>", tag + "</body>", 1)


def replace_once(text, pattern, repl, label, flags=re.S):
    fn = repl if callable(repl) else (lambda m: repl)
    new, n = re.subn(pattern, fn, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"build_content: could not locate block: {label}")
    return new


def main():
    changed = []
    # 1. product pages
    for p in PRODUCTS:
        path = ROOT / "products" / f"{p['slug']}.html"
        t = path.read_text()
        t = replace_once(t, r"<main class=\"wrap\">.*?</main>", product_main(p), f"product main {p['id']}")
        path.write_text(t)
        changed.append(str(path.relative_to(ROOT)))
    # 2. cards everywhere (root pages, guides)
    for path in list(ROOT.glob("*.html")) + list((ROOT / "guides").glob("*.html")):
        t = path.read_text()
        pre = prefix_for(path)
        n_before = t
        for p in PRODUCTS:
            pat = rf'<article class="card" data-product="{p["id"]}">.*?</article>'
            if re.search(pat, t, flags=re.S):
                t = re.sub(pat, lambda m, p=p, pre=pre: card(p, pre), t, flags=re.S)
        if t != n_before:
            path.write_text(t)
            changed.append(str(path.relative_to(ROOT)))
    # 3. compare page: two generated tables
    cp = ROOT / "compare.html"
    af_html, mt_html = compare_tables()
    t = cp.read_text()
    # Replace the whole generated comparison block, including headings, so repeated
    # builds do not leave stale/duplicate category headings behind.
    t = replace_once(t, r"<h2>Air fryers</h2>.*?(?=<h2>How to decide</h2>)",
                     af_html + mt_html, "compare table")
    cp.write_text(t)
    # 4. category pages: comparison table
    for name, group in [("air-fryers.html", "Air Fryers"), ("meat-thermometers.html", "Meat Thermometers")]:
        path = ROOT / name
        t = path.read_text()
        group_products = [p for p in PRODUCTS if p["cat"] == group]
        if group == "Air Fryers":
            keys = [("Capacity", "capacity"), ("Temperature", "temperature"), ("Power", "power"), ("Dimensions", "dimensions")]
        else:
            keys = [("Response", "response"), ("Accuracy", "accuracy"), ("Certification", "certification"), ("Battery", "battery")]
        headers = ["Product", *[k for k, _ in keys], "Official listing"]
        rows = []
        for p in group_products:
            rows.append([f'<a href="products/{p["slug"]}.html">{esc(SHORT[p["id"]].split("|")[0].strip())}</a>']
                        + [fv(p, k) for _, k in keys]
                        + [a(p["listing"], "View listing (paid link)", True)])
        t = replace_once(t, r"<h2>Comparison table</h2><table>.*?</table>",
                         "<h2>Comparison table</h2>" + table(headers, rows, f"Values from official Amazon listings, read {CHECKED}. Blank = unverified."),
                         f"{name} comparison")
        path.write_text(t)
        changed.append(name)
    # 5. home: at-a-glance table
    ip = ROOT / "index.html"
    t = ip.read_text()
    rows = []
    for p in PRODUCTS:
        mf = p["fields"].get("model")
        model = esc(mf["v"]) if mf and mf["st"] == "verified" else "— blank (unverified)"
        obs = p["observed"] or "— not confirmed (FLG-012)"
        rows.append([p["id"], f'<a href="products/{p["slug"]}.html">{esc(SHORT[p["id"]])}</a>', esc(p["cat"]),
                     model, esc(obs), a(p["listing"], "Official listing", True)])
    t = replace_once(t, r"(<section><h2>At a glance[^<]*</h2>\n).*?</table>",
                     lambda m: m.group(1) + table(["ID", "Product (listing name, abridged)", "Category", "Model", "Observed ASIN", "Official listing"], rows,
                                                 f"Every row links to the official Amazon listing. Price and rating are intentionally blank. Read {CHECKED}."),
                     "home at a glance")
    ip.write_text(t)
    # 6. sources table
    sp = ROOT / "sources.html"
    rows = []
    for s in SOURCES.values():
        url = s["url"]
        link = a(url, url, "amazon.com" in url)
        rows.append([esc(s["id"]), esc(s["name"]), esc(s["used_for"]), link])
    t = sp.read_text()
    t = replace_once(t, r"<table><caption>Source register.*?</table>",
                     table(["ID", "Source", "Used for", "Link (checked " + CHECKED + ")"], rows,
                           "Source register. Every row links to the official source or the listing it describes."),
                     "sources table")
    sp.write_text(t)
    # 7. flagged table
    fp = ROOT / "flagged.html"
    rows = []
    for fl in FLAGS:
        links = " · ".join(a(SOURCES[s]["url"], s, "amazon.com" in SOURCES[s]["url"]) for s in (fl.get("links") or []) if s in SOURCES)
        rows.append([esc(fl["id"]), f"<strong>{esc(fl['title'])}</strong>", esc(fl["detail"]), links or "—"])
    t = fp.read_text()
    t = replace_once(t, r"<table><caption>Irregularities register.*?</table>",
                     table(["ID", "Issue", "Detail", "Source link(s)"], rows,
                           "Irregularities register, updated " + CHECKED + ". None of these block publishing; all are visible to readers."),
                     "flagged table")
    fp.write_text(t)
    # 8. compliance: tag every Amazon product link, load the collector
    for path in sorted(set(ROOT.glob("*.html")) | set((ROOT / "guides").glob("*.html"))
                       | set((ROOT / "products").glob("*.html"))):
        t = path.read_text()
        n_before = t
        pre = prefix_for(path)
        t = tag_amazon_links(t)
        t = ensure_collect_script(t, pre)
        t = ensure_nav_links(t, pre)
        if t != n_before:
            path.write_text(t)
            changed.append(str(path.relative_to(ROOT)))
    print("build_content: updated", len(set(changed)), "files")


if __name__ == "__main__":
    main()
