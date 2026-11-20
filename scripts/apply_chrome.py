#!/usr/bin/env python3
"""Apply shared chrome (masthead nav + footer) and JSON-LD to every HTML page.
Idempotent: safe to re-run after adding pages. Used by the T-11 publication pass.
Nav keeps dashboard surfaces in ONE group (Reference) + the footer, per the brief."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-11-20"
SITE = "https://karagemop466-tech.github.io/Affil2"

NAV = [
    ("index.html", "Home", ""),
    ("air-fryers.html", "Air Fryers", ""),
    ("meat-thermometers.html", "Meat Thermometers", ""),
    ("guides.html", "Guides", ""),
    ("compare.html", "Compare", ""),
    ("about.html", "About", ""),
    ("reference.html", "Reference", "ref"),
]
RECORDS = [
    ("reference.html", "Reference hub"),
    ("executive-summary.html", "Executive Summary"),
    ("verification.html", "Verification Log"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for Review"),
    ("suggestions.html", "Suggestions &amp; Direction"),
    ("questions.html", "Open Questions"),
    ("campaign-ledger.html", "Campaign Ledger"),
    ("disclosure.html", "Disclosure, Privacy &amp; Analytics"),
]

def prefix_for(rel):
    """Relative href prefix for a page at `rel` (e.g. 'guides/x.html' -> '../')."""
    return "../" * (len(Path(rel).parts) - 1)

def build_header(rel):
    p = prefix_for(rel)
    links = "\n".join(
        f'<a href="{p}{href}" class="{cls}">{label}</a>' for href, label, cls in NAV
    )
    return (
        '<header class="masthead"><div class="wrap mast">'
        f'<a class="brand" href="{p}index.html"><b>ShopNow <em>Kitchen</em></b>'
        "<small>Air fryers &amp; meat thermometers, compared honestly</small></a>"
        f'<nav aria-label="Primary">{links}</nav>'
        '<form class="search" action="' + p + 'search.html" method="get" role="search">'
        '<label class="sr" for="q">Search guides and products</label>'
        '<input id="q" name="q" type="search" placeholder="Search: basket, capacity, thermometer…">'
        "<button type=\"submit\">Search</button></form></div></header>"
    )

def build_footer(rel):
    p = prefix_for(rel)
    recs = "\n".join(f'<li><a href="{p}{href}">{label}</a></li>' for href, label in RECORDS)
    return (
        '<footer><div class="wrap">'
        '<p class="disc-foot"><strong>As an Amazon Associate I earn from qualifying purchases.</strong> '
        "Links marked <strong>(paid link)</strong> are Amazon affiliate links — if you buy through them, "
        "we may earn a commission at no extra cost to you.</p>"
        '<div class="foot-grid">'
        f'<div><h4>ShopNow Kitchen</h4><p>An independent buying-guide publication for air fryers and '
        "meat thermometers. Every specification is traced to the official Amazon listing; every gap is "
        "flagged instead of filled in. No prices, no star ratings, no “best” claims.</p>"
        f'<p><a href="{p}feed.xml">RSS feed</a> · <a href="{p}sitemap.xml">Sitemap</a> · '
        f'<a href="{p}guides.html">All guides</a> · <a href="{p}about.html">About &amp; authorship</a></p></div>'
        f'<div><h4>Shop</h4><ul><li><a href="{p}air-fryers.html">Air Fryers</a></li>'
        f'<li><a href="{p}meat-thermometers.html">Meat Thermometers</a></li>'
        f'<li><a href="{p}compare.html">Compare</a></li><li><a href="{p}guides.html">Guides</a></li>'
        f'<li><a href="{p}search.html">Search</a></li></ul></div>'
        f'<div><h4>Records &amp; dashboards</h4><ul>{recs}</ul></div>'
        "</div>"
        '<div class="foot-legal">'
        "<p>Prices and availability are not shown on this site — check the live listing on Amazon for current "
        "details (Program Policies §2(b)). Product names and Amazon are trademarks of Amazon.com, Inc. or its "
        "affiliates. This site is not endorsed by Amazon. Imagery is original editorial artwork, not product "
        f"photography. Last verified: {DATE}.</p>"
        f"<p>© 2026 ShopNow Kitchen. Original editorial content. <a href=\"{p}flagged.html\">Flagged for Review</a> "
        f"lists everything we could not verify. <a href=\"{p}disclosure.html\">Privacy &amp; analytics</a>.</p>"
        "</div></div></footer>"
    )

def build_jsonld(rel, title):
    p = prefix_for(rel)
    org = {
        "@context": "https://schema.org", "@type": "Organization", "name": "ShopNow Kitchen",
        "url": f"{SITE}/index.html", "logo": f"{SITE}/assets/img/hero-kitchen.jpg",
        "description": "Independent buying guides for air fryers and meat thermometers, compared from official listings.",
    }
    parts = []
    if rel == "index.html":
        parts.append({"@context": "https://schema.org", "@type": "WebSite",
                      "name": "ShopNow Kitchen", "url": f"{SITE}/index.html",
                      "description": "Air fryers and meat thermometers compared from official listings. No prices, no hype.",
                      "publisher": {"@id": f"{SITE}/index.html#org"}})
        org["@id"] = f"{SITE}/index.html#org"
        parts.append(org)
    crumbs = []
    crumbs.append({"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/index.html"})
    if rel != "index.html":
        label = title.split("—")[0].strip() if "—" in title else title
        crumbs.append({"@type": "ListItem", "position": 2, "name": label, "item": f"{SITE}/{rel}"})
        parts.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs})
    if rel.startswith("guides/"):
        parts.append({
            "@context": "https://schema.org", "@type": "Article",
            "headline": title.split("—")[0].strip() if "—" in title else title,
            "datePublished": DATE, "dateModified": DATE,
            "author": {"@type": "Organization", "name": "ShopNow Kitchen editorial desk"},
            "publisher": {"@type": "Organization", "name": "ShopNow Kitchen"},
            "mainEntityOfPage": f"{SITE}/{rel}",
        })
    return "\n".join(
        '<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in parts
    )

def main():
    changed = 0
    for page in sorted(ROOT.rglob("*.html")):
        rel = str(page.relative_to(ROOT))
        html = page.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        title = (m.group(1).strip() if m else "ShopNow Kitchen").replace("&amp;", "&")
        new = re.sub(r"<header class=\"masthead\">.*?</header>", build_header(rel), html, flags=re.S)
        new = re.sub(r"<footer>.*?</footer>", build_footer(rel), new, flags=re.S)
        new = re.sub(r"\n?<script type=\"application/ld\+json\">.*?</script>", "", new, flags=re.S)
        ld = build_jsonld(rel, title)
        if ld:
            new = new.replace("</head>", ld + "\n</head>", 1)
        if new != html:
            page.write_text(new, encoding="utf-8")
            changed += 1
    print(f"chrome applied: {changed} pages changed")

if __name__ == "__main__":
    main()
