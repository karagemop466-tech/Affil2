#!/usr/bin/env python3
"""Apply shared site chrome (masthead, footer, fonts) across all HTML pages.

Reader-facing nav stays shopper-first; every dashboard surface lives in one
footer nav group ("Studio & records"). Idempotent: safe to re-run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Fraunces:ital,wght@0,400;0,600;0,700;1,400&'
         'family=Inter:wght@400;500;600;700&display=swap">')


def masthead(p):
    return (
        '<header class="masthead"><div class="wrap mast">'
        f'<a class="brand" href="{p}index.html">ShopNow <span>Kitchen</span><small>Compare before you buy</small></a>'
        f'<nav aria-label="Primary"><a href="{p}index.html">Shop</a>'
        f'<a href="{p}air-fryers.html">Air Fryers</a>'
        f'<a href="{p}meat-thermometers.html">Meat Thermometers</a>'
        f'<a href="{p}guides.html">Guides</a>'
        f'<a href="{p}compare.html">Compare</a></nav>\n'
        f'<form class="search" action="{p}search.html" method="get" role="search">'
        '<label class="sr" for="q">Search guides and products</label>'
        '<input id="q" name="q" type="search" placeholder="Search: basket, capacity, thermometer…">'
        '<button type="submit">Search</button></form></div></header>'
    )


def footer(p):
    return (
        '<footer><div class="wrap">'
        '<p class="disc-foot">As an Amazon Associate I earn from qualifying purchases. Links marked '
        '<strong>(paid link)</strong> are Amazon affiliate links — if you buy through them, we may '
        'earn a commission at no extra cost to you.</p>'
        '<div class="foot-grid">'
        '<div><h4>ShopNow Kitchen</h4><p>Independent buying notes on air fryers and meat '
        'thermometers — five products, two categories, every spec from the official listing. '
        'We show you what fits your kitchen; you decide what to buy.</p></div>'
        f'<div><h4>Read</h4><a href="{p}index.html">Shop home</a><a href="{p}air-fryers.html">Air Fryers</a>'
        f'<a href="{p}meat-thermometers.html">Meat Thermometers</a><a href="{p}guides.html">Guides</a>'
        f'<a href="{p}compare.html">Compare</a></div>'
        '<div><h4>Studio &amp; records</h4>'
        f'<a href="{p}executive-summary.html">Executive Summary</a>'
        f'<a href="{p}suggestions.html">Suggestions &amp; Direction</a>'
        f'<a href="{p}questions.html">Open Questions</a>'
        f'<a href="{p}sources.html">Sources</a>'
        f'<a href="{p}campaign-ledger.html">Campaign Ledger</a>'
        f'<a href="{p}flagged.html">Flagged for Review</a>'
        f'<a href="{p}about.html">About &amp; Authorship</a>'
        f'<a href="{p}disclosure.html">Privacy &amp; Analytics</a>'
        f'<a href="{p}sitemap.xml">Sitemap</a>'
        f'<a href="{p}feed.xml">RSS Feed</a></div>'
        '</div>'
        '<p class="legal">Prices and availability are not shown on this site — check the live '
        'listing on Amazon for current details. Product names and Amazon are trademarks of '
        'Amazon.com, Inc. or its affiliates. This site is not endorsed by Amazon. Editorial '
        'illustrations are original artwork, not product photographs. '
        f'<a href="{p}disclosure.html">Affiliate disclosure &amp; privacy</a> · '
        f'<a href="{p}flagged.html">Flagged for Review</a> · Last updated 2026-11-20.<br>'
        '© 2026 ShopNow Kitchen. Original editorial content.</p>'
        '</div></footer>'
    )


def update(path, rel):
    html = path.read_text(encoding='utf-8')
    orig = html
    # fonts: insert before the local stylesheet link
    if 'fonts.googleapis.com' not in html:
        html = re.sub(r'(<link rel="stylesheet" href="(?:\.\./)?assets/style\.css">)',
                      FONTS + r'\1', html, count=1)
    # masthead
    html = re.sub(r'<header class="masthead">.*?</header>', masthead(rel), html,
                  count=1, flags=re.S)
    # footer
    html = re.sub(r'<footer>.*?</footer>', footer(rel), html, count=1, flags=re.S)
    if html != orig:
        path.write_text(html, encoding='utf-8')
        print('updated', path.relative_to(ROOT))
    else:
        print('unchanged', path.relative_to(ROOT))


def main():
    pages = [p for p in ROOT.rglob('*.html')
             if 'node_modules' not in p.parts and p.name != 'index.html']
    for p in sorted(pages):
        rel = '../' if p.parent.name in ('products', 'guides') else ''
        update(p, rel)
    print(f'chrome applied to {len(pages)} pages (index.html handled separately)')


if __name__ == '__main__':
    sys.exit(main())
