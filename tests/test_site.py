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
        # The count is asserted against the pages on disk, never against a literal: a hardcoded
        # "built 36 pages" fails every time a guide is legitimately published, which teaches
        # people to ignore the test.
        claimed = int(re.search(r"built (\d+) pages", build_one.stdout).group(1))
        on_disk = len([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])
        self.assertEqual(claimed, on_disk)
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

    def test_every_guide_is_a_page_and_a_route(self):
        """A guide that is not in the sitemap, the feed and the findability profile is unwritten."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from seasonal_guides import GUIDES as seasonal
            from traffic_guides import GUIDES as traffic
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        base = re.findall(r'dict\(slug="([\w-]+)"', (ROOT / "scripts" / "build_site.py").read_text())
        slugs = base + [g["slug"] for g in seasonal] + [g["slug"] for g in traffic]
        self.assertGreaterEqual(len(slugs), 17)
        self.assertEqual(len(slugs), len(set(slugs)), "duplicate guide slug")

        sm = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = {u.find(ns + "loc").text for u in sm.findall(ns + "url")}
        feed = ET.fromstring((ROOT / "feed.xml").read_text(encoding="utf-8"))
        links = {i.find("link").text for i in feed.findall("./channel/item")}
        findability = (ROOT / "findability.txt").read_text(encoding="utf-8")
        home = (ROOT / "index.html").read_text(encoding="utf-8")

        for slug in slugs:
            page = ROOT / "guides" / f"{slug}.html"
            self.assertTrue(page.exists(), f"missing page for guide {slug}")
            url = "https://karagemop466-tech.github.io/Affil2/guides/" + slug + ".html"
            self.assertIn(url, locs, f"{slug} not submitted in the sitemap")
            self.assertIn(url, links, f"{slug} not in the feed")
            self.assertIn(f"guides/{slug}.html", findability, f"{slug} missing from findability.txt")
            html = page.read_text(encoding="utf-8")
            # the artefact that makes a page look generated: an entity escaped twice, so a reader
            # sees the markup instead of the character
            self.assertNotIn("&amp;#", html, f"{slug}: a double-escaped entity reached the page")
            self.assertIn("flip-list", html, f"{slug}: no product line at the end")
            self.assertIn("amazon.com/dp/", html, f"{slug}: product line has no tagged link")

        # the homepage rail must point at real guides, and it shows the newest wave
        rail = re.findall(r'href="guides/([\w-]+)\.html"', home)
        for slug in rail:
            self.assertIn(slug, slugs, f"homepage rail links an unknown guide: {slug}")

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


if __name__ == "__main__":
    unittest.main()
