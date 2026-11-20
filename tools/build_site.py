#!/usr/bin/env python3
"""Build the static site in docs/ from data/*.json and data/campaign-ledger.csv.

No third-party dependencies. Run:  python3 tools/build_site.py
Every value shown on the site comes from data/. Blank data stays blank and is marked unverified.
"""
import csv
import datetime as dt
import html
import json
import shutil
from email.utils import format_datetime
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SITE = load("site.json")
PRODUCTS = load("products.json")["products"]
SOURCES = load("sources.json")["sources"]
FINDINGS = load("findings.json")["findings"]
QUESTIONS = load("questions.json")["questions"]
SUGGESTIONS = load("suggestions.json")["suggestions"]
UPDATES = load("updates.json")["items"]
FEED_TITLE = load("updates.json")["feed_title"]
BASE = SITE["base_url"]
ASSOC = SITE["associates_statement"]
TAG = SITE["tracking_id"]

NAV = [
    ("products/", "Products"),
    ("guides/", "Guides"),
    ("intent/", "Intent record"),
    ("sources/", "Sources"),
    ("findings/", "Findings"),
    ("questions/", "Questions"),
    ("suggestions/", "Suggestions"),
    ("ledger/", "Ledger"),
    ("flagged/", "Flagged for review"),
    ("executive-summary/", "Executive summary"),
]

PAGES = []  # (relative path, title, description, body_html, page_kind)


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def cell(value):
    """Blank data renders as a blank, flagged cell (never a guessed value)."""
    if value is None or str(value).strip() == "":
        return '<td class="blank" aria-label="unverified"></td>'
    return f"<td>{e(value)}</td>"


def link_cell(url, label=None):
    if not url:
        return '<td class="blank" aria-label="no source"></td>'
    return f'<td><a href="{e(url)}" rel="noopener">{e(label or url)}</a></td>'


def sponsored(url, label, pid=""):
    """Outbound product link: always rel=sponsored (Google guidance, SRC-03)."""
    attr = f' data-outbound="{e(pid)}"' if pid else ""
    return f'<a href="{e(url)}" rel="sponsored noopener" target="_blank"{attr}>{e(label)} <span aria-hidden="true">↗</span><span class="sr"> (sponsored link)</span></a>'


def src_html(u):
    """Source link. Supplied short links are affiliate links, so they get rel=sponsored."""
    if u.startswith("https://link.amazon/"):
        return sponsored(u, "link")
    return f'<a href="{e(u)}" rel="noopener">link</a>'


def page_shell(rel, title, desc, body, kind=""):
    depth = rel.count("/")
    pre = "../" * depth
    canonical = BASE + ("" if rel == "index.html" else rel.replace("index.html", ""))
    cur = ' aria-current="page"'
    nav_items = "".join(
        f'<li><a href="{pre}{href}"{cur if (href and rel.startswith(href)) else ""}>{e(label)}</a></li>'
        for href, label in NAV
    )
    footer_nav = "".join(f'<li><a href="{pre}{href}">{e(label)}</a></li>' for href, label in NAV)
    body_attr = f' data-page="{kind}"' if kind else ""
    # Body links are written relative to the site root; make them relative to this page.
    body = re.sub(
        r'href="((?:products|guides|intent|sources|findings|questions|suggestions|ledger|flagged|executive-summary|disclosure)/[^"]*|index\.html[^"]*)"',
        lambda m: f'href="{pre}{m.group(1)}"',
        body,
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · {e(SITE['name'])}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<link rel="stylesheet" href="{pre}assets/site.css">
<link rel="alternate" type="application/rss+xml" title="{e(FEED_TITLE)}" href="{BASE}feed.xml">
<meta name="robots" content="index,follow">
<script>window.AFFIL_CONFIG = {{ endpoint: "" }};</script>
<script src="{pre}assets/track.js" defer></script>
</head>
<body{body_attr}>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap">
    <div class="row">
      <div>
        <a class="brand" href="{pre}index.html">{e(SITE['name'])}</a><span class="wip">Working title</span>
        <p class="tagline">{e(SITE['tagline'])}</p>
      </div>
    </div>
  </div>
</header>
<div class="disclosure" role="note" aria-label="Affiliate disclosure">
  <div class="wrap"><strong>Disclosure:</strong> {e(ASSOC)} Links marked <em>Sponsored</em> are affiliate links.
  <a href="{pre}disclosure/">Full disclosure</a></div>
</div>
<nav class="nav" aria-label="Site">
  <div class="wrap"><ul><li class="label">Dashboard</li>{nav_items}</ul></div>
</nav>
<main id="main" class="wrap">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <div><h4>Dashboard</h4><ul>{footer_nav}</ul></div>
      <div><h4>Site</h4><ul>
        <li><a href="{pre}index.html">Front page</a></li>
        <li><a href="{pre}disclosure/">Disclosure</a></li>
        <li><a href="{pre}sitemap.xml" data-event="sitemap_view">Sitemap</a></li>
        <li><a href="{pre}feed.xml" data-event="feed_open">RSS feed</a></li>
      </ul></div>
      <div><h4>Official sources</h4><ul>
        <li><a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener">Associates Operating Agreement</a></li>
        <li><a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener">Associates Program Policies</a></li>
        <li><a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener">Google: qualify outbound links</a></li>
        <li><a href="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255" rel="noopener">16 CFR Part 255 (FTC)</a></li>
      </ul></div>
    </div>
    <div class="disc">
      <p><strong>Disclosure (repeated):</strong> {e(ASSOC)} Links marked <em>Sponsored</em> are affiliate links. Prices and availability can change; check the listing before you buy.</p>
      <p>Last updated {e(SITE['updated'])}. Source code and data: <a href="{e(SITE['repo_url'])}" rel="noopener">GitHub repository</a>.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def add(rel, title, desc, body, kind=""):
    PAGES.append((rel, title, desc, body, kind))


def table(headers, rows, extra_class=""):
    th = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in headers)
    return f'<div class="table-wrap"><table class="{extra_class}"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def badge(text, kind=""):
    return f'<span class="badge {kind}">{e(text)}</span>'


def src_link(sid):
    s = next((x for x in SOURCES if x["id"] == sid), None)
    return s


# ---------- derived values (counted from data, never hand-typed) ----------
n_reached = sum(1 for p in PRODUCTS if p.get("observed_title"))
n_open_q = sum(1 for q in QUESTIONS if q["status"] == "Open")
n_flag = sum(1 for f in FINDINGS if f["status"] == "needs review")
n_guides_pub = 0  # no guide is published (see Suggestions S-06)
n_ledger = max(0, sum(1 for _ in csv.DictReader((DATA / "campaign-ledger.csv").open(encoding="utf-8"))))

# ---------- FRONT PAGE ----------
cards = []
for p in PRODUCTS:
    if p.get("observed_title"):
        st = badge("Product page reached", "ok")
        title = p["observed_title_short"]
        desc = f'{p["category"]} · observed ASIN <span class="mono">{e(p["observed_asin"])}</span>. Intended ASIN not confirmed.'
    else:
        st = badge("Link not confirmed", "")
        title = "Link under review"
        desc = f'{p["supplied_token"]} did not reach a product page ({e(p["observed_redirect_url"]) or "no target"}).'
    cards.append(f"""
      <article class="card" id="{e(p['id'])}">
        {st}
        <h3>{e(title)}</h3>
        <p>{desc}</p>
        <p class="cta">{sponsored(p['supplied_link'], 'Check on Amazon', p['id'])}</p>
        <p><a href="products/#{e(p['id'])}">Details and sources →</a></p>
      </article>""")

questions_preview = [
    ("Basket or oven-style air fryer: what should you compare?", "Compare the format first: baskets and ovens cook and clean differently."),
    ("A no-hype checklist for comparing air fryer capacity", "Capacity claims need a unit (quarts, litres) and a method."),
    ("How to assess cleanup and counter-space trade-offs", "Footprint and cleaning effort are measurable before you buy."),
    ("Questions to ask before buying a multi-function kitchen appliance", "Which jobs does it replace, and what does it crowd out?"),
]
qcards = "".join(
    f"""<article class="card"><span class="badge muted">Working title · not published</span>
      <h3>{e(t)}</h3><p>{e(d)}</p></article>"""
    for t, d in questions_preview
)

front = f"""
<p class="kicker">Buyer guide · air fryers and multi-function appliances</p>
<h1>Start with the products. Check the questions before you buy.</h1>
<p class="lede">These are the products whose links we were given. For each one we show what the link actually reaches, what is confirmed, and what is still open.</p>

<h2>Products we're tracking</h2>
<div class="grid">{''.join(cards)}</div>

<div class="stats" aria-label="Key figures">
  <div class="stat"><b>{n_reached} of {len(PRODUCTS)}</b><span>links reached a product page</span></div>
  <div class="stat"><b>0</b><span>prices or ratings verified</span></div>
  <div class="stat"><b>{n_open_q}</b><span>open questions</span></div>
  <div class="stat"><b>{n_flag}</b><span>items flagged for review</span></div>
  <div class="stat"><b>{n_ledger}</b><span>campaign ledger rows</span></div>
</div>

<h2>Questions we're researching</h2>
<p class="meta">Working titles drawn from the owner's brief. They are hypotheses, not claims about popularity, search volume, or product quality. None is published yet (see <a href="suggestions/#S-06">Suggestion S-06</a>).</p>
<div class="grid">{qcards}</div>

<h2>How this site handles facts</h2>
<ul class="points">
  <li>Every product row links to the page it came from. Anything not confirmed is left blank and marked.</li>
  <li>Affiliate links are marked <em>sponsored</em>. The required Associates statement is shown above the fold on every page.</li>
  <li>No commission, click, or revenue figure is shown. The campaign ledger is empty until authorized reports are imported.</li>
</ul>

<div class="note"><strong>Executive summary:</strong> the site is built, but it cannot yet send buyers to confirmed products or measure clicks. <a href="executive-summary/">Read the full summary →</a></div>
"""
add("index.html", "Air fryers and kitchen appliances: buyer questions", SITE["tagline"], front)

# ---------- PRODUCTS ----------
rows = []
for p in PRODUCTS:
    rows.append(f"""<tr id="{e(p['id'])}">
      <td class="mono">{e(p['id'])}</td>
      <td>{e(p['observed_title_short']) if p['observed_title_short'] else '<span class="badge">Not confirmed</span>'}</td>
      <td>{e(p['category']) if p['category'] else ''}</td>
      <td>{sponsored(p['supplied_link'], p['supplied_token'], p['id'])}</td>
      <td class="mono">{e(p['observed_asin'])}</td>
      <td class="blank" aria-label="price not verified"></td>
      <td class="blank" aria-label="rating not verified"></td>
      <td>{e(p['status'])}</td>
      {link_cell(p['observed_source'], 'Source')}
    </tr>""")
prod_body = f"""
<p class="kicker">Dashboard · products</p>
<h1>Products</h1>
<p class="lede">One row per supplied link. Price and rating are blank because the main product's values were not captured reliably (F-08). The 'observed' ASIN is where the link resolved, not a confirmed intent.</p>
<div class="flagbox"><strong>Flagged:</strong> the supplied tokens are 9 characters, not the 10-character ASIN length cited by third-party sources (F-01). Three of five links did not reach a product page (F-03). See <a href="flagged/">Flagged for review</a>.</div>
{table(['ID','Product (observed title)','Category','Supplied link','Observed ASIN','Price','Rating','Status','Source'], rows)}
<h2>Notes</h2>
<ul class="points">
  <li>Affiliate links are the owner's supplied short links, unchanged, marked sponsored. They are not yet tested as Associates Special Links (F-05).</li>
  <li>Tracking ID <span class="mono">{e(TAG)}</span> was supplied and is not validated against the Associates account.</li>
</ul>
"""
add("products/index.html", "Products", "Five supplied Amazon links: what each one reaches, what is confirmed, and what is blank.", prod_body, "product")

# ---------- GUIDES ----------
g_rows = []
for g in SITE["guides"]:
    g_rows.append(f"""<tr><td class="mono">{e(g['id'])}</td><td>{e(g['working_title'])}</td><td>{badge('Not published','muted')}</td><td>{e(g['note'])}</td><td><a href="suggestions/#S-06">S-06</a></td></tr>""")
guide_body = f"""
<p class="kicker">Editorial backlog</p>
<h1>Guides</h1>
<p class="lede">Question-shaped guides based on the owner's four working titles. None is published. Each needs sources for every product claim before it goes live.</p>
<div class="flagbox">Published guides: <strong>{n_guides_pub}</strong>. Reason: the product data behind them is not yet confirmed (F-01..F-08).</div>
{table(['ID','Working title','Status','Note','Decision'], g_rows)}
"""
add("guides/index.html", "Guides (backlog)", "Question-shaped buyer guides. Working titles, not yet published.", guide_body, "guide")

# ---------- INTENT RECORD ----------
i_rows = []
for p in PRODUCTS:
    i_rows.append(f"""<tr>
      <td class="mono">{e(p['id'])}</td>
      <td>{sponsored(p['supplied_link'], p['supplied_token'], p['id'])}</td>
      <td>{e(p['supplied_token_length'])}</td>
      {cell(p['intended_asin'])}
      {cell(p['official_listing_url'])}
      {cell(p['confirmation_date'])}
      {cell(p['confirmation_source'])}
      <td class="sep-l">{e(p['observed_redirect_url'])}</td>
      <td class="mono">{e(p['observed_asin'])}</td>
      <td>{e(p['observed_on'])}</td>
      {link_cell(p['observed_source'], 'Source')}
    </tr>""")
intent_body = f"""
<p class="kicker">Dashboard · verification</p>
<h1>Product-intent confirmation record</h1>
<p class="lede">Each supplied link has two separate fields. <strong>Intended</strong> (left) is what the owner meant the link to be; it stays blank until confirmed. <strong>Observed</strong> (right) is where the link resolved when fetched. The two are never merged.</p>
<div class="note">Rationale: Amazon's ASIN is a 10-character product identifier (third-party sources only; F-01). A checkable ASIN lets the intended product be compared with the observed one.</div>
{table(['ID','Supplied link','Token length','Intended ASIN','Official listing URL','Confirmation date','Confirmation source','Observed redirect target','Observed ASIN','Observed on','Source'], i_rows)}
<h2>What is missing for each row</h2>
<ul class="points">
  <li>Intended ASIN, official listing URL, confirmation date, and confirmation source: blank for all five rows. Reason: token length and mismatch (F-01, F-02).</li>
  <li>Special Link test (one per product in the enrolled Associates account): not performed (F-05).</li>
</ul>
"""
add("intent/index.html", "Product-intent confirmation record", "Intended ASIN and listing URL kept separate from the observed redirect target.", intent_body)

# ---------- SOURCES ----------
s_rows = []
for s in SOURCES:
    s_rows.append(f"""<tr>
      <td class="mono">{e(s['id'])}</td>
      <td><a href="{e(s['url'])}" rel="noopener">{e(s['title'])}</a></td>
      <td>{e(s['publisher'])}</td>
      <td>{e(s['version_stated'])}</td>
      <td>{badge(s['checked'], 'ok' if s['checked']=='Verified' else ('muted' if s['checked']=='Observed' else ''))}</td>
      <td>{e(s['what_was_checked'])}</td>
      <td>{e('; '.join(s['used_for']))}</td>
    </tr>""")
src_body = f"""
<p class="kicker">Dashboard · verification</p>
<h1>Sources</h1>
<p class="lede">Every source below was opened on 2026-11-20. 'Verified' means the claim was read on that page. 'Partial' means only some pages were read. 'Observed' means a live retailer page was viewed, not confirmed as intent. 'Not official' is shown only to make clear what was not confirmed.</p>
{table(['ID','Source (link)','Publisher','Version / date','Check','What was checked','Used for'], s_rows)}
"""
add("sources/index.html", "Sources", "Official sources and how each claim was checked.", src_body)

# ---------- FINDINGS ----------
f_rows = []
for f in FINDINGS:
    srcs = " · ".join(src_html(u) for u in f["sources"]) if f["sources"] else "<span class=\"meta\">Internal (no external source)</span>"
    f_rows.append(f"""<tr>
      <td class="mono">{e(f['id'])}</td>
      <td>{badge(f['severity'], 'ok' if f['severity']=='low' else '')}</td>
      <td><strong>{e(f['title'])}</strong></td>
      <td>{e(f['detail'])}</td>
      <td>{e(f['impact'])}</td>
      <td>{e(f['action'])}</td>
      <td>{srcs}</td>
      <td>{e(f['status'])}</td>
    </tr>""")
find_body = f"""
<p class="kicker">Dashboard · analysis</p>
<h1>Findings and irregularities</h1>
<p class="lede">Repo review and link checks, line by line. Each finding has its action and sources. These are flagged for review; they do not block publication.</p>
{table(['ID','Severity','Finding','Detail','Impact','Action','Sources','Status'], f_rows)}
"""
add("findings/index.html", "Findings and irregularities", "What was checked, what was found, and what needs action.", find_body)

# ---------- QUESTIONS ----------
q_rows = []
for q in QUESTIONS:
    q_rows.append(f"""<tr>
      <td class="mono">{e(q['id'])}</td>
      <td>{badge(q['status'], 'ok' if q['status']=='Answered' else '')}</td>
      <td>{e(q['question'])}</td>
      <td>{e(q['answer']) if q['answer'] else '<span class="blank"></span>'}</td>
      <td>{e(q['source'])}</td>
      <td>{e(q['how_to_close'])}</td>
    </tr>""")
qbody = f"""
<p class="kicker">Dashboard · decisions</p>
<h1>Questions before any decision</h1>
<p class="lede">What we know, what we don't, and how to close each gap. Nothing should be decided on the open items yet.</p>
{table(['ID','Status','Question','Current answer','Source / reference','How to close it'], q_rows)}
"""
add("questions/index.html", "Questions before any decision", "Open and answered questions with how to close each gap.", qbody)

# ---------- SUGGESTIONS ----------
sug_cards = []
for s in SUGGESTIONS:
    opts = "".join(
        f"<tr><td>{e(o['id'])}</td><td>{e(o['label'])}</td><td>{e(o['pros'])}</td><td>{e(o['cons'])}</td></tr>"
        for o in s["options"]
    )
    sug_cards.append(f"""
    <section class="sugg" id="{e(s['id'])}">
      <header><h3>{e(s['id'])} · {e(s['topic'])}</h3>
        <span>{badge(s['priority'], 'ok' if s['priority'] in ('Medium',) else '')} {badge(s['status'], 'muted')}</span></header>
      <p class="meta">{e(s['why'])}</p>
      <div class="table-wrap opt"><table class="opt" style="min-width:520px"><thead><tr><th>Option</th><th>Path</th><th>For</th><th>Against</th></tr></thead><tbody>{opts}</tbody></table></div>
      <p><strong>Lean (not a decision):</strong> {e(s['lean'])}</p>
      <p class="meta">To choose: reply with <span class="mono">{e(s['id'])}: [option letter]</span>. Nothing changes until you choose.</p>
    </section>""")
sug_body = f"""
<p class="kicker">Dashboard · decisions</p>
<h1>Suggestions</h1>
<p class="lede">Ways to improve the site and the decisions behind it. Review each item and choose one option. Nothing marked 'Awaiting' has been implemented.</p>
<div class="note">Blocking first: <a href="#S-01">S-01 measurement</a> and <a href="#S-02">S-02 link format</a>. Everything else can wait.</div>
{''.join(sug_cards)}
"""
add("suggestions/index.html", "Suggestions", "Options to choose from before anything is implemented.", sug_body)

# ---------- LEDGER ----------
ledger_rows_csv = list(csv.DictReader((DATA / "campaign-ledger.csv").open(encoding="utf-8")))
ledger_cols = ["timestamp_utc", "source", "channel", "eligible_sessions", "clicks", "reported_orders", "report_id", "provenance_note"]
schema_rows = [
    ("timestamp_utc", "When the figure was taken (UTC).", "Owner brief (internal; no external source)"),
    ("source", "Authorized first-party report the figure came from.", "Owner brief (internal; no external source)"),
    ("channel", "Where the traffic came from.", "Owner brief (internal; no external source)"),
    ("eligible_sessions", "Sessions as the Associates program defines them (24-hour session window, SRC-02 §1).", "https://affiliate-program.amazon.com/help/operating/policies"),
    ("clicks", "Clicks on Special Links in the reporting period.", "Owner brief (internal; no external source)"),
    ("reported_orders", "Orders as reported by Associates. Left blank until imported.", "https://affiliate-program.amazon.com/help/operating/policies"),
    ("report_id", "Identifier of the report used.", "Owner brief (internal; no external source)"),
    ("provenance_note", "How the row was obtained.", "Owner brief (internal; no external source)"),
]
def _schema_src(c):
    if c.startswith("http"):
        return link_cell(c)
    return '<td><span class="meta">' + e(c) + "</span></td>"


sch_html = table(["Field", "Meaning", "Source"], [
    "<tr><td class=\"mono\">" + e(a) + "</td><td>" + e(b) + "</td>" + _schema_src(c) + "</tr>"
    for a, b, c in schema_rows
])
ledger_body = f"""
<p class="kicker">Dashboard · measurement</p>
<h1>Campaign ledger</h1>
<p class="lede">Empty by design. Rows are added only from authorized first-party reports, with a dated provenance note. No conversion score, revenue, or forecast is shown.</p>
<div class="stats"><div class="stat"><b>{len(ledger_rows_csv)}</b><span>rows imported</span></div><div class="stat"><b>0</b><span>clicks recorded</span></div><div class="stat"><b>0</b><span>reported orders</span></div></div>
<p>Download the empty ledger: <a href="campaign-ledger.csv" download>campaign-ledger.csv</a></p>
<h2>Columns</h2>
{sch_html}
<p class="meta">Clicks cannot be recorded until the measurement path is chosen (Suggestion S-01).</p>
"""
add("ledger/index.html", "Campaign ledger", "Empty campaign ledger with defined columns and provenance rules.", ledger_body)

# ---------- FLAGGED ----------
flag_items = [f for f in FINDINGS if f["status"] == "needs review"]
fl_rows = []
for f in flag_items:
    srcs = " · ".join(src_html(u) for u in f["sources"]) if f["sources"] else "<span class=\"meta\">Internal</span>"
    fl_rows.append(f"<tr><td class=\"mono\">{e(f['id'])}</td><td>{e(f['title'])}</td><td>{e(f['action'])}</td><td>{srcs}</td></tr>")
blank_rows = []
for p in PRODUCTS:
    for field, label in [("intended_asin", "Intended ASIN"), ("official_listing_url", "Official listing URL"), ("observed_price", "Price"), ("observed_rating", "Rating")]:
        if not p.get(field):
            why = p.get("intended_asin_note") if field == "intended_asin" else p.get("price_note", "Not captured.")
            blank_rows.append(f"<tr><td class=\"mono\">{e(p['id'])}</td><td>{e(label)}</td><td>{badge('Unverified','')}</td><td>{e(why)}</td><td>{link_cell(p['observed_source'], 'Source')}</td></tr>")
flag_body = f"""
<p class="kicker">Review queue</p>
<h1>Flagged for review</h1>
<p class="lede">Items the owner should review after the site is live. Flagged and unverified items do not block the merge or the deploy. Source links are included so each one can be checked.</p>
<div class="flagbox">Ask for changes by item ID (for example, <span class="mono">F-03: test the link in my browser</span>).</div>
<h2>Irregularities ({len(fl_rows)})</h2>
{table(['ID','Finding','Action needed','Sources'], fl_rows)}
<h2>Unverified fields (left blank)</h2>
{table(['Product','Field','Status','Why blank','Source'], blank_rows)}
<h2>Unverified claims</h2>
<ul class="points">
  <li>The 10-character ASIN length rule: only third-party sources found (<a href="sources/#SRC-10">SRC-10</a>, <a href="sources/#SRC-11">SRC-11</a>).</li>
  <li>Program Policies sections not read (chunks 2–10 of 11). Only §1 and part of §2 were checked (<a href="sources/#SRC-02">SRC-02</a>).</li>
  <li>Source IDs S01, S07, S24, SG-27..SG-30 and FLG-003 from the brief: not in the repo, not used (F-06).</li>
</ul>
"""
add("flagged/index.html", "Flagged for review", "Irregularities and unverified items, with the action needed and source links.", flag_body)

# ---------- EXECUTIVE SUMMARY ----------
es = SITE["executive_summary"]
es_body = f"""
<p class="kicker">Summary · {e(SITE['updated'])}</p>
<h1>Executive summary</h1>
<p class="lede">{e(es['headline'])}</p>
<ul class="points">{''.join(f'<li>{e(p)}</li>' for p in es['points'])}</ul>
<h2>Decisions needed from the owner</h2>
<ol class="points">
  <li>Confirm the ASIN or listing URL for each product (<a href="intent/">intent record</a>).</li>
  <li>Test one Special Link per product in the Associates account and report the result (<a href="flagged/">F-05</a>).</li>
  <li>Choose a measurement path (<a href="suggestions/#S-01">S-01</a>).</li>
  <li>Choose a publishing cadence and approve or change the working titles (<a href="suggestions/#S-04">S-04</a>, <a href="suggestions/#S-06">S-06</a>).</li>
</ol>
<h2>Key sources</h2>
<ul class="points">
  <li><a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener">Associates Operating Agreement (§5 identification statement)</a></li>
  <li><a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener">Associates Program Policies (§2 disqualifications)</a></li>
  <li><a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener">Google: qualify outbound links (rel=sponsored)</a></li>
  <li><a href="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255" rel="noopener">16 CFR Part 255 (endorsements and material connections)</a></li>
</ul>
"""
add("executive-summary/index.html", "Executive summary", "Summary of what is built, what is confirmed, and what is blocked.", es_body)

# ---------- DISCLOSURE ----------
disc_body = f"""
<p class="kicker">Policy</p>
<h1>Disclosure</h1>
<p class="lede">{e(ASSOC)}</p>
<p>This site participates in the Amazon Associates Program. Links to Amazon marked <em>sponsored</em> are affiliate links. When a purchase qualifies, the site may earn a commission at no extra cost to you.</p>
<p>How disclosure is handled here: the Associates statement is shown under the masthead and in the footer of every page, as the Operating Agreement §5 requires (<a href="sources/#SRC-01">SRC-01</a>). Affiliate links carry <code>rel="sponsored"</code> (<a href="sources/#SRC-03">SRC-03</a>). The disclosure is written to be clear and conspicuous under 16 CFR 255.5 (<a href="sources/#SRC-04">SRC-04</a>).</p>
<p class="meta">Tracking ID supplied by the owner: <span class="mono">{e(TAG)}</span> (not yet validated, F-05).</p>
"""
add("disclosure/index.html", "Disclosure", "Associates identification statement, affiliate link handling, and FTC-style disclosure.", disc_body)

# ---------- 404 ----------
add("404.html", "Page not found", "This page does not exist.", """
<h1>Page not found</h1>
<p class="lede">That page is not on the site. Start at the <a href="index.html">front page</a> or the <a href="products/">products</a>.</p>""")


# ---------- WRITE ----------
def write_pages():
    for rel, title, desc, body, kind in PAGES:
        out = DOCS / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(rel, title, desc, body, kind), encoding="utf-8")


def write_sitemap():
    urls = []
    for rel, *_ in PAGES:
        if rel == "404.html":
            continue
        loc = BASE + ("" if rel == "index.html" else rel.replace("index.html", ""))
        urls.append(f"  <url><loc>{e(loc)}</loc><lastmod>{SITE['updated']}</lastmod></url>")
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n",
        encoding="utf-8",
    )


def write_feed():
    items = []
    for it in UPDATES:
        d = dt.datetime.fromisoformat(it["date"]).replace(tzinfo=dt.timezone.utc)
        items.append(
            f"<item><title>{e(it['title'])}</title><link>{e(BASE + it['link'])}</link>"
            f"<guid isPermaLink=\"false\">{e(BASE + it['link'] + '#' + it['date'])}</guid>"
            f"<pubDate>{format_datetime(d)}</pubDate><description>{e(it['summary'])}</description></item>"
        )
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
        f"<title>{e(FEED_TITLE)}</title><link>{e(BASE)}</link>"
        f"<description>{e(SITE['tagline'])}</description><language>en-us</language>"
        + "".join(items) + "</channel></rss>\n"
    )
    (DOCS / "feed.xml").write_text(feed, encoding="utf-8")


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    write_pages()
    write_sitemap()
    write_feed()
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (DOCS / "ledger").mkdir(parents=True, exist_ok=True)
    shutil.copy(DATA / "campaign-ledger.csv", DOCS / "ledger" / "campaign-ledger.csv")
    print(f"built {len(PAGES)} pages into {DOCS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
