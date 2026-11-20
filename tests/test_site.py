#!/usr/bin/env python3
"""
Integration & regression test suite for ShopNow Kitchen.
Run: python3 -m unittest discover -s tests -p "test_*.py" -v
"""
import json
import pathlib
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent


class SiteIntegrationTests(unittest.TestCase):
    def test_generator_is_idempotent_and_gate_passes(self):
        build_one = subprocess.run(
            [sys.executable, "scripts/build_site.py"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        pages_on_disk = len([q for q in sorted(ROOT.rglob("*.html")) if ".git" not in q.parts])
        self.assertIn(f"built {pages_on_disk} pages", build_one.stdout)
        snap_a = {
            p.relative_to(ROOT): p.read_text(encoding="utf-8")
            for p in sorted(ROOT.rglob("*.html")) if ".git" not in p.parts
        }
        subprocess.run(
            [sys.executable, "scripts/build_site.py"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        snap_b = {
            p.relative_to(ROOT): p.read_text(encoding="utf-8")
            for p in sorted(ROOT.rglob("*.html")) if ".git" not in p.parts
        }
        self.assertEqual(snap_a, snap_b)

        gate = subprocess.run(
            [sys.executable, "scripts/check_site.py"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(gate.returncode, 0, msg=gate.stdout + "\n" + gate.stderr)
        self.assertIn("ALL CHECKS PASS", gate.stdout)

    def test_verified_live_product_specs_and_conflicts(self):
        products = {
            p["id"]: p
            for p in json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
        }
        self.assertEqual(len(products), 5)
        for p in products.values():
            self.assertFalse(p.get("intended"))
            self.assertRegex(p["observed"], r"^B0[A-Z0-9]{8}$")

        self.assertEqual(products["P-01"]["fields"]["weight"]["v"], "13.3 pounds")
        self.assertEqual(products["P-01"]["fields"]["capacity"]["st"], "conflict")

        self.assertEqual(products["P-02"]["fields"]["model"]["v"].split()[0], "4-00675-02X-VN")
        self.assertIn("75–500 °F", products["P-02"]["fields"]["temperature"]["v"])
        self.assertEqual(products["P-02"]["fields"]["power"]["v"], "120 volts / 1700 watts")
        self.assertIsNone(products["P-02"]["fields"]["weight"]["v"])
        self.assertEqual(products["P-02"]["fields"]["weight"]["st"], "unverified")
        self.assertEqual(products["P-02"]["fields"]["accessories"]["st"], "conflict")

        self.assertEqual(products["P-03"]["fields"]["weight"]["v"], "12.8 pounds")
        self.assertEqual(products["P-03"]["fields"]["power"]["st"], "conflict")
        self.assertIn("1700", products["P-03"]["fields"]["power"]["v"])
        self.assertIn("1000", products["P-03"]["fields"]["power"]["v"])

        self.assertEqual(products["P-04"]["observed"], "B0DHZTCNR5")
        self.assertEqual(products["P-04"]["fields"]["model"]["v"], "HT07")
        self.assertEqual(products["P-04"]["fields"]["upper_temp"]["v"], "572 °F")

        self.assertEqual(products["P-05"]["fields"]["model"]["v"], "CQ60-3C-Z1-E")
        self.assertIn("4.75 inches", products["P-05"]["fields"]["probe_length"]["v"])
        self.assertEqual(products["P-05"]["fields"]["warranty"]["st"], "conflict")

    def test_platform_and_measurement_pages_and_svg_usage(self):
        platform = " ".join((ROOT / "platform.html").read_text(encoding="utf-8").split())
        for expected in ("Creators API", "HTTP 403", "Participation Requirements",
                         "Agent/", "rel=\"sponsored nofollow\"", "analytics/server.js"):
            self.assertIn(expected, platform)

        measurement = (ROOT / "measurement.html").read_text(encoding="utf-8")
        for expected in ("data/events.json", "analytics/server.js", "functions/api/collect.js",
                         "sn-collect-endpoint", "Search Console"):
            self.assertIn(expected, measurement)

        sources_html = (ROOT / "sources.html").read_text(encoding="utf-8")
        self.assertNotIn("Ten sources", sources_html)
        self.assertIn("S23", sources_html)
        self.assertIn("S24", sources_html)
        self.assertTrue((ROOT / "design-brief.html").exists())
        self.assertTrue((ROOT / "guides" / "first-week-air-fryer.html").exists())

        sitemap = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = {u.find(ns + "loc").text for u in sitemap.findall(ns + "url")}
        self.assertTrue(any(loc.endswith("/platform.html") for loc in locs))
        self.assertTrue(any(loc.endswith("/measurement.html") for loc in locs))


    def test_shop_copy_carries_no_audit_codes_and_no_invented_numbers(self):
        """Reader-facing polish rules the site promises the owner (SG-33, SG-34, SG-35)."""
        import re
        buyer = ["index.html", "shop.html", "air-fryers.html", "meat-thermometers.html", "compare.html"]
        buyer += [f"guides/{g.name}" for g in (ROOT / "guides").glob("*.html")]
        for rel in buyer:
            html = (ROOT / rel).read_text(encoding="utf-8")
            prose = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S)
            prose = re.sub(r"<[^>]+>", " ", prose)
            self.assertNotIn("FLG-", prose, f"{rel}: register code leaked into buyer-facing copy")

        for g in sorted((ROOT / "guides").glob("*.html")):
            html = g.read_text(encoding="utf-8")
            stated = re.findall(r"(\d+)\s*min read", html)
            self.assertEqual(len(stated), 1, f"{g.name}: exactly one stated read time")
            self.assertIn('class="byline"', html, f"{g.name}: no dated desk byline")
            self.assertIn("about.html#who-writes-it", html)

    def test_howto_guides_are_sourced_and_in_every_index(self):
        """The two new guides cite only the .gov factsheet and the dated listing register (SG-36)."""
        for slug in ("thermometer-ice-test", "read-an-air-fryer-listing"):
            page = (ROOT / "guides" / f"{slug}.html").read_text(encoding="utf-8")
            self.assertIn("fsis.usda.gov" if slug == "thermometer-ice-test" else "compare.html", page)
            self.assertIn(f"guides/{slug}.html", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
            self.assertIn(f"guides/{slug}.html", (ROOT / "feed.xml").read_text(encoding="utf-8"))
        def norm(x):
            return x.replace("&nbsp;", " ").replace("\u00a0", " ")
        ice = norm((ROOT / "guides" / "thermometer-ice-test.html").read_text(encoding="utf-8"))
        for must in ("Immerse the stem a minimum of 2 inches", "Wait a minimum of 30 seconds",
                     "Most food thermometers will give an accurate reading within 2 to 4 degrees F",
                     "thickest part", "It should read 32 degrees F"):
            self.assertIn(must, ice, f"ice-water guide missing the USDA wording {must!r}")
        listing = norm((ROOT / "guides" / "read-an-air-fryer-listing.html").read_text(encoding="utf-8"))
        for must in ("1700", "1000 watts", "24 one-touch", "16.9", "12.8 pounds", "13.3 pounds"):
            self.assertIn(must, listing, f"listing guide missing the register figure {must!r}")
        # no invented authority: the guides never claim a test was run
        for slug in ("thermometer-ice-test", "read-an-air-fryer-listing"):
            page = (ROOT / "guides" / f"{slug}.html").read_text(encoding="utf-8")
            self.assertNotIn("we tested", page.lower())
            self.assertNotIn("our lab", page.lower())

    def test_decision_center_assembles_a_build_prompt(self):
        """SG-37: the shortlist becomes the instruction, from one payload, with the constraints in it."""
        import json as _json
        import re
        html = (ROOT / "suggestions.html").read_text(encoding="utf-8")
        payload = _json.loads(re.search(
            r'<script type="application/json" id="sugData">(.*?)</script>', html, re.S).group(1)
            .replace("<\\/", "</"))
        proposals = payload["proposals"]
        self.assertIn("SG-33", proposals)
        self.assertIn("SG-37", proposals)
        for row in re.findall(r'<tr data-sug="(SG-\d+)"', html):
            self.assertIn(row, proposals, f"{row} is in the table but not in the prompt payload")
        box = re.search(r'<textarea id="buildPrompt"[^>]*>(.*?)</textarea>', html, re.S).group(1)
        self.assertIn("Standing constraints", box)
        self.assertIn("Do not assume answers", payload["unanswered"])
        js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
        for token in ("promptAssemble", "promptDefaultIds", "data-pick", "copyPrompt"):
            self.assertIn(token, js)

    def test_new_flags_and_source_are_published(self):
        """S27 (people-first guidance) and this session's flags are registered, sourced and published, never quietly edited."""
        sources = {x["id"]: x for x in json.loads((ROOT / "data" / "sources.json").read_text())}
        self.assertIn("people-first content", sources["S27"]["name"].lower())
        flags = json.loads((ROOT / "data" / "flags.json").read_text())
        by_id = {f["id"]: f for f in flags}
        for fid in ("FLG-055", "FLG-056", "FLG-057", "FLG-058"):
            self.assertIn(fid, by_id)
            self.assertTrue(by_id[fid]["links"], f"{fid} has no source")
            published = (ROOT / "flagged.html").read_text(encoding="utf-8")
            self.assertIn(fid, published)
        # corrected findings stay visible: the dated changelog on sources.html must carry them
        changes = (ROOT / "sources.html").read_text(encoding="utf-8")
        for fid in ("FLG-055", "FLG-056", "FLG-057"):
            self.assertIn(fid, changes, f"{fid} is not recorded in the dated changelog")
        self.assertIn("S27", changes)
        self.assertIn("people-first guidance", (ROOT / "how-we-choose.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()


class GuideWaveRouteTests(unittest.TestCase):
    """Every guide record must be a page and a route, whatever module wrote it (T-31)."""

    def _slugs(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from seasonal_guides import GUIDES as seasonal
            from howto_guides import GUIDES as howto
            from traffic_guides import GUIDES as traffic
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        base = re.findall(r'dict\(slug="(\w[\w-]*)"', (ROOT / "scripts" / "build_site.py").read_text())
        return base + [g["slug"] for g in seasonal] + [g["slug"] for g in howto] + [g["slug"] for g in traffic]

    def test_every_guide_record_is_a_page_and_a_route(self):
        slugs = self._slugs()
        self.assertGreaterEqual(len(slugs), 16)
        self.assertEqual(len(slugs), len(set(slugs)), "duplicate guide slug")
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        sm = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        locs = {u.find(ns + "loc").text for u in sm.findall(ns + "url")}
        feed = ET.fromstring((ROOT / "feed.xml").read_text(encoding="utf-8"))
        links = {i.find("link").text for i in feed.findall("./channel/item")}
        findability = (ROOT / "findability.txt").read_text(encoding="utf-8")
        for slug in slugs:
            page = ROOT / "guides" / f"{slug}.html"
            self.assertTrue(page.exists(), f"missing page for guide {slug}")
            url = "https://karagemop466-tech.github.io/Affil2/guides/" + slug + ".html"
            self.assertIn(url, locs, f"{slug} not submitted in the sitemap")
            self.assertIn(url, links, f"{slug} not in the feed")
            self.assertIn(f"guides/{slug}.html", findability, f"{slug} missing from findability.txt")
            html = page.read_text(encoding="utf-8")
            self.assertIn("flip-list", html, f"{slug}: no product line at the end")
            self.assertIn("amazon.com/dp/", html, f"{slug}: product line has no tagged link")

    def test_the_live_wave_is_on_the_front_page(self):
        """A guide nobody can reach from the home page is a guide nobody reads (T-31)."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from traffic_guides import GUIDES as traffic
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        for g in traffic:
            self.assertIn(f'href="guides/{g["slug"]}.html"', home,
                          f"{g['slug']}: not linked from index.html")

    def test_no_stale_guide_pages(self):
        """A guide removed from the registers must not stay published on disk."""
        slugs = set(self._slugs())
        for page in (ROOT / "guides").glob("*.html"):
            self.assertIn(page.stem, slugs, f"{page.name} is on disk with no guide record")

    def test_the_traffic_wave_quotes_only_registered_figures(self):
        """The November wave may only state figures the register marks verified, or USDA's chart."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from traffic_guides import GUIDES as traffic
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        products = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
        allowed = set()
        for prod in products:
            for f in prod["fields"].values():
                allowed.update(re.findall(r"\d+(?:\.\d+)?", str(f.get("v") or "")))
        usda = json.loads((ROOT / "data" / "usda-temperatures.json").read_text(encoding="utf-8"))
        for _, temp in usda["rows"]:
            allowed.update(re.findall(r"\d+(?:\.\d+)?", str(temp)))
        allowed |= {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
                    "15", "20", "24", "25", "30", "32", "36", "60", "70", "212", "1000", "2026",
                    "2027", "01", "02", "03", "04", "05", "06", "07"}
        for g in traffic:
            prose = " ".join([g["title"], g["sub"], g["intro"], g["verdict"]] +
                             [t for _, t in g["sections"]])
            prose = re.sub(r"<[^>]+>", " ", prose).replace("&nbsp;", " ")
            for m in re.finditer(r"\b\d+(?:\.\d+)?\s*(?:°F|degrees?|watts?|volts?|quarts?|"
                                 r"liters?|inches|pounds?|hours?|seconds?)\b", prose):
                for num in re.findall(r"\d+(?:\.\d+)?", m.group(0)):
                    self.assertIn(num, allowed,
                                  f"{g['slug']}: {m.group(0).strip()!r} is not a registered figure")


class BuyerPageVoiceTests(unittest.TestCase):
    """The gate's reader-voice rules were unreachable for a while; these hold the line in CI too."""

    def test_no_product_page_prints_the_same_record_twice(self):
        for page in sorted((ROOT / "products").glob("*.html")):
            txt = page.read_text(encoding="utf-8")
            self.assertEqual(0, txt.count("Product-intent confirmation record"),
                             f"{page.name}: audit heading on a buyer page")
            self.assertEqual(0, len(re.findall(r"FLG-\d{3}", txt)),
                             f"{page.name}: register code visible to a shopper")
            # the five required fields still exist, in reader language, exactly once
            for label in ("The link you gave us", "Intended ASIN", "Observed redirect target",
                          "Special Link we publish", "Confirmation date", "Associates test status"):
                self.assertIn(label, txt, f"{page.name}: provenance field {label!r} missing")
            self.assertEqual(1, txt.count("Intended ASIN"),
                             f"{page.name}: the intent record is printed more than once")

    def test_the_intend_record_function_still_matches_the_register(self):
        """intent_table() is not rendered on buyer pages; it must still agree with the data."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import build_site as bs
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        for prod in bs.PRODUCTS:
            html = bs.intent_table(prod)
            self.assertIn(prod["submitted"], html)
            self.assertIn(prod["observed"], html)
            self.assertIn(str(bs.TODAY), html)
            self.assertIn("PENDING", html)
