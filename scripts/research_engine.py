#!/usr/bin/env python3
"""
ShopNow Kitchen — AI-powered product research engine.

Reads privacy-preserving measurement data (localStorage export format) and
produces product-research suggestions for the Decision Center. Nothing here
scrapes Amazon, contacts third parties, or displays prices/ratings. It only
works with first-party, cookieless event data the reader's browser already
collected.

Usage:
    python3 scripts/research_engine.py <events_export.json>

Reads a JSON array of events (the shape emitted by assets/app.js into
localStorage.sn_events) and prints ranked research suggestions.
"""
import json
import sys
import pathlib
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

VALID_EVENTS = {"page_view", "outbound_click", "guide_read", "search", "suggestion_rank"}


def load_events(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "events" in data:
        data = data["events"]
    return [e for e in data if isinstance(e, dict) and e.get("e") in VALID_EVENTS]


def research_suggestions(events):
    """Return a ranked list of research suggestions from first-party events."""

    clicks_by_product = Counter()
    clicks_by_page = Counter()
    guide_reads = Counter()
    zero_result_searches = 0
    total_searches = 0
    page_views = Counter()

    for e in events:
        name = e.get("e")
        if name == "outbound_click":
            clicks_by_product[e.get("product", "unknown")] += 1
            clicks_by_page[e.get("page", "unknown")] += 1
        elif name == "guide_read":
            guide_reads[e.get("page", "unknown")] += 1
        elif name == "search":
            total_searches += 1
            if e.get("results", 1) == 0:
                zero_result_searches += 1
        elif name == "page_view":
            page_views[e.get("page", "unknown")] += 1

    suggestions = []

    # 1. Products with the most outbound clicks = reader demand
    for product_id, count in clicks_by_product.most_common():
        suggestions.append({
            "type": "product_demand",
            "target": product_id,
            "title": f"Add more coverage for {product_id} — {count} outbound clicks",
            "evidence": f"{count} readers clicked through to the Amazon listing.",
            "action": "Write an additional buying guide or comparison row for this product.",
            "priority": "high" if count >= 5 else "medium",
        })

    # 2. Guides with the most reads = topic resonance
    for guide, count in guide_reads.most_common():
        suggestions.append({
            "type": "topic_resonance",
            "target": guide,
            "title": f"Expand the {guide.split('/')[-1]} topic — {count} guide reads",
            "evidence": f"{count} readers finished reading this guide.",
            "action": "Publish a follow-up guide in the same cluster.",
            "priority": "high" if count >= 5 else "medium",
        })

    # 3. Zero-result searches = unmet demand
    if total_searches > 0:
        zero_rate = zero_result_searches / total_searches
        suggestions.append({
            "type": "unmet_search_demand",
            "target": "search",
            "title": f"Address {zero_result_searches} zero-result searches ({zero_rate:.0%} of all searches)",
            "evidence": f"{zero_result_searches} of {total_searches} searches returned no matches.",
            "action": "Add content or products matching those search terms.",
            "priority": "high" if zero_rate > 0.3 else "medium",
        })

    # 4. Pages with high views but no clicks = conversion opportunity
    for page, views in page_views.most_common():
        clicks = clicks_by_page.get(page, 0)
        if views >= 10 and clicks == 0:
            suggestions.append({
                "type": "conversion_gap",
                "target": page,
                "title": f"Improve conversion on {page} — {views} views, 0 outbound clicks",
                "evidence": f"{views} page views with no outbound click recorded.",
                "action": "Review the page's product line and CTA placement.",
                "priority": "medium",
            })

    # Rank: high priority first, then by evidence strength
    rank_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda s: (rank_order.get(s["priority"], 9), -len(s["evidence"])))

    return suggestions


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/research_engine.py <events_export.json>", file=sys.stderr)
        sys.exit(2)

    events = load_events(sys.argv[1])
    suggestions = research_suggestions(events)

    print(f"Analysed {len(events)} first-party events.\n")
    if not suggestions:
        print("No research signals yet. Keep running the site and collecting events.")
        return

    for i, s in enumerate(suggestions, 1):
        print(f"{i}. [{s['priority'].upper()}] {s['title']}")
        print(f"   Evidence: {s['evidence']}")
        print(f"   Action: {s['action']}")
        print()


if __name__ == "__main__":
    main()
