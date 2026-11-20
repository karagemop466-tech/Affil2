#!/usr/bin/env python3
"""
ShopNow Kitchen — campaign optimization advisor.

Reads first-party click events and the empty campaign ledger, then produces
prioritized optimization recommendations. Nothing here contacts Amazon or any
third party; it only analyzes events the reader's browser already stored.

Usage:
    python3 scripts/campaign_optimizer.py <events_export.json>

Outputs a ranked list of recommendations suitable for review in the Decision
Center before any change is implemented.
"""
import json
import sys
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent

VALID_EVENTS = {"outbound_click", "page_view", "guide_read"}


def load_events(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "events" in data:
        data = data["events"]
    return [e for e in data if isinstance(e, dict) and e.get("e") in VALID_EVENTS]


def optimize(events):
    """Return ranked campaign optimization recommendations."""

    clicks_by_product = Counter()
    clicks_by_page = Counter()
    guide_reads = Counter()
    product_pages = {
        "P-01": "products/p01-chefman-6qt-dual-basket.html",
        "P-02": "products/p02-emeril-26qt-french-door.html",
        "P-03": "products/p03-chefman-8qt-turbrofry.html",
        "P-04": "products/p04-thermomaven-1sec.html",
        "P-05": "products/p05-chefiq-sense-gen3.html",
    }

    for e in events:
        name = e.get("e")
        if name == "outbound_click":
            clicks_by_product[e.get("product", "unknown")] += 1
            clicks_by_page[e.get("page", "unknown")] += 1
        elif name == "guide_read":
            guide_reads[e.get("page", "unknown")] += 1

    recommendations = []

    # 1. Top-clicked products = invest more content
    total_clicks = sum(clicks_by_product.values())
    for product_id, count in clicks_by_product.most_common():
        share = count / total_clicks if total_clicks else 0
        recommendations.append({
            "area": "content_investment",
            "target": product_id,
            "title": f"Build more content around {product_id} ({count} clicks, {share:.0%} of outbound traffic)",
            "evidence": f"{count} outbound clicks recorded for this product.",
            "action": "Add a dedicated guide, comparison row, or seasonal feature for this product.",
            "priority": "high" if share >= 0.3 else "medium",
        })

    # 2. Products with zero clicks = review placement or replace
    for product_id, page in product_pages.items():
        if clicks_by_product.get(product_id, 0) == 0:
            recommendations.append({
                "area": "placement_review",
                "target": product_id,
                "title": f"Review {product_id} placement — zero outbound clicks",
                "evidence": f"No clicks recorded to the {product_id} Amazon listing.",
                "action": "Check CTA visibility, link placement, and whether the product still matches reader intent.",
                "priority": "medium",
            })

    # 3. High-read guides with no clicks = add product line
    for guide, reads in guide_reads.most_common():
        clicks = clicks_by_page.get(guide, 0)
        if reads >= 5 and clicks == 0:
            recommendations.append({
                "area": "conversion",
                "target": guide,
                "title": f"Add a product line to {guide} — {reads} reads, 0 clicks",
                "evidence": f"{reads} readers finished this guide but none clicked through.",
                "action": "Add a tagged product recommendation with a clear verdict at the end of the guide.",
                "priority": "high",
            })

    # Rank recommendations
    rank_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda r: rank_order.get(r["priority"], 9))

    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/campaign_optimizer.py <events_export.json>",
              file=sys.stderr)
        sys.exit(2)

    events = load_events(sys.argv[1])
    recommendations = optimize(events)

    print(f"Analysed {len(events)} first-party events.\n")
    if not recommendations:
        print("No optimization signals yet. Collect more outbound click data first.")
        return

    for i, r in enumerate(recommendations, 1):
        print(f"{i}. [{r['priority'].upper()}] {r['title']}")
        print(f"   Evidence: {r['evidence']}")
        print(f"   Action: {r['action']}")
        print()


if __name__ == "__main__":
    main()
