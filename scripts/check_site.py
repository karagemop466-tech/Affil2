#!/usr/bin/env python3
"""Compliance + integrity gate. Fails on: missing disclosure, unmarked outbound, prices, broken internal links, sitemap gaps."""
import pathlib, re, sys
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
print(f"checked {len(pages)} pages")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("ALL CHECKS PASS")
