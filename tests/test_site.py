"""
Site tests.

The publishing gate in scripts/check_site.py is the authority that runs on
every push. These tests exist so that a failure is readable and specific
rather than a list of 40 identical strings, and so the compliance rules are
covered by something that can be run on its own:

    python3 -m unittest discover -s tests -p "test_*.py" -v

Everything here is standard library. No dependencies, no network.
"""

import html
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

TRACKING_ID = "shopnow047c-20"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

PRODUCT_URL = re.compile(r'href="(https://www\.amazon\.com/(?:dp|gp/product)/[A-Z0-9]{10}[^"]*)"')
SHORT_URL = re.compile(r'<a href="(https://link\.amazon/[^"]*)"([^>]*)>')
AMAZON_IMAGE_HOSTS = (
    "m.media-amazon.com",
    "images-na.ssl-images-amazon.com",
    "ssl-images-amazon.com",
)


def pages():
    return sorted(ROOT.rglob("*.html"))


class DisclosureTests(unittest.TestCase):
    def test_disclosure_appears_on_every_page(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn(DISCLOSURE, text, "%s: missing disclosure" % page.name)

    def test_disclosure_is_above_the_fold(self):
        """The strip has to come before the main content, not after it."""
        for page in pages():
            text = page.read_text(encoding="utf-8")
            disclosure_at = text.find(DISCLOSURE)
            main_at = text.find("<main")
            self.assertNotEqual(main_at, -1, "%s: no main content" % page.name)
            self.assertLess(disclosure_at, main_at, "%s: disclosure is below the fold" % page.name)

    def test_disclosure_is_repeated_in_the_footer(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            footer_at = text.find("<footer")
            self.assertNotEqual(footer_at, -1, "%s: no footer" % page.name)
            self.assertIn(DISCLOSURE, text[footer_at:], "%s: no footer disclosure" % page.name)


class OutboundLinkTests(unittest.TestCase):
    def test_every_amazon_product_link_is_tagged(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            for url in PRODUCT_URL.findall(text):
                self.assertIn(
                    "tag=" + TRACKING_ID,
                    url,
                    "%s: product link without the Associates tag: %s" % (page.name, url),
                )

    def test_every_amazon_link_is_sponsored(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            for match in re.finditer(r'<a href="(https://www\.amazon\.com[^"]*)"([^>]*)>', text):
                self.assertIn(
                    "sponsored",
                    match.group(2),
                    "%s: not marked sponsored: %s" % (page.name, match.group(1)),
                )

    def test_every_supplied_short_link_is_sponsored(self):
        """The submitted link.amazon links are Amazon product links too."""
        for page in pages():
            text = page.read_text(encoding="utf-8")
            for url, attrs in SHORT_URL.findall(text):
                self.assertIn(
                    "sponsored",
                    attrs,
                    "%s: short link not marked sponsored: %s" % (page.name, url),
                )

    def test_no_amazon_hosted_imagery(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            for host in AMAZON_IMAGE_HOSTS:
                self.assertNotIn(host, text, "%s: uses Amazon-hosted imagery" % page.name)


class PolicyTests(unittest.TestCase):
    def test_no_prices_on_any_page(self):
        price = re.compile(r"\$\s?\d")
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIsNone(price.search(text), "%s: contains a price" % page.name)

    def test_no_ratings_or_review_counts_on_any_page(self):
        rating = re.compile(r"\b\d(?:\.\d)?\s*(?:out of 5|/5|stars)\b", re.I)
        reviews = re.compile(r"\b\d{1,3},\d{3}\s+(?:ratings|reviews)\b", re.I)
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIsNone(rating.search(text), "%s: contains a star rating" % page.name)
            self.assertIsNone(reviews.search(text), "%s: contains a review count" % page.name)

    def test_every_page_has_metadata(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn('rel="canonical"', text, page.name)
            self.assertIn('name="description"', text, page.name)
            self.assertIn("<title>", text, page.name)

    def test_intent_and_observation_stay_separate(self):
        for page in sorted((ROOT / "products").glob("*.html")):
            text = page.read_text(encoding="utf-8")
            self.assertIn("Intended ASIN", text, page.name)
            self.assertIn("Observed redirect target", text, page.name)
            self.assertIn("Confirmation date", text, page.name)
            # The intended ASIN is blank until the owner confirms it.
            self.assertIn("owner confirmation needed", text, page.name)


class StructureTests(unittest.TestCase):
    def test_internal_links_resolve(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', text):
                if href.startswith("http"):
                    continue
                target = (page.parent / href).resolve()
                self.assertTrue(target.exists(), "%s: broken link %s" % (page.name, href))

    def test_sitemap_covers_every_page(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in pages():
            rel = str(page.relative_to(ROOT))
            self.assertIn(rel, sitemap, "sitemap missing %s" % rel)

    def test_feed_and_sitemap_are_well_formed(self):
        import xml.dom.minidom
        for name in ("feed.xml", "sitemap.xml"):
            try:
                xml.dom.minidom.parse(str(ROOT / name))
            except Exception as exc:  # pragma: no cover - failure path
                self.fail("%s is not well-formed XML: %s" % (name, exc))

    def test_every_page_loads_the_collector(self):
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn("assets/js/collect.js", text, "%s: collector not loaded" % page.name)

    def test_measurement_page_exists_and_is_linked(self):
        self.assertTrue((ROOT / "measurement.html").exists())
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn("measurement.html", text, "%s: no link to the measurement page" % page.name)

    def test_platform_page_exists_and_is_linked(self):
        """The platform concept is a required surface, so it is reachable everywhere."""
        self.assertTrue((ROOT / "platform.html").exists())
        for page in pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn("platform.html", text, "%s: no link to the platform concept" % page.name)

    def test_platform_page_separates_shipped_from_designed(self):
        """The platform page must not read as a claim that automation exists."""
        text = (ROOT / "platform.html").read_text(encoding="utf-8")
        self.assertIn("concept, not a product", text)
        for module in ("Research", "commission analysis", "Content generation",
                       "Link management", "Click and conversion tracking", "Optimization"):
            self.assertIn(module, text, "platform page does not cover %s" % module)
        # It must name the blocker for each module rather than claiming completion.
        self.assertIn("FLG-033", text)
        self.assertIn("FLG-004", text)
        self.assertIn("FLG-003", text)


class MeasurementTests(unittest.TestCase):
    def test_event_schema_matches_the_collector(self):
        schema = json.loads((ROOT / "data/events.json").read_text(encoding="utf-8"))
        names = [event["name"] for event in schema["events"]]
        self.assertEqual(
            names,
            ["page_view", "outbound_click", "guide_read", "search", "suggestion_rank"],
        )
        collector = (ROOT / "functions/api/collect.js").read_text(encoding="utf-8")
        for name in names:
            self.assertIn('"%s"' % name, collector, "%s is not accepted by the collector" % name)

    def test_the_collector_files_exist(self):
        for path in (
            "functions/api/collect.js",
            "analytics/server.js",
            "assets/js/collect.js",
            "data/events.json",
            "measurement.html",
        ):
            self.assertTrue((ROOT / path).exists(), "missing %s" % path)

    def test_the_schema_states_what_is_never_collected(self):
        schema = json.loads((ROOT / "data/events.json").read_text(encoding="utf-8"))
        never = " ".join(schema["endpoint"]["what_is_never_stored"]).lower()
        for phrase in ("ip address", "user agent", "cookies", "the text of a search query"):
            self.assertIn(phrase, never, "schema does not state: %s" % phrase)

    def test_the_campaign_ledger_is_empty(self):
        ledger = json.loads((ROOT / "data/campaign-ledger.json").read_text(encoding="utf-8"))
        rows = ledger.get("rows") if isinstance(ledger, dict) else ledger
        self.assertIsNotNone(rows, "campaign ledger has no rows key")
        self.assertEqual(len(rows), 0, "campaign ledger is not empty")


if __name__ == "__main__":
    unittest.main()
