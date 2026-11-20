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
        self.assertIn("built 36 pages", build_one.stdout)
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
            # Intended and observed are separate registers: the intended field stays blank until
            # the owner confirms it, and it is never back-filled from the redirect we observed.
            self.assertIsNone(p["intended_asin"])
            self.assertTrue(p["intended_status"])
            self.assertRegex(p["observed"], r"^B0[A-Z0-9]{8}$")
            self.assertNotEqual(p["intended_asin"], p["observed"])
            self.assertRegex(p["confirmed"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertEqual(p["listing"], f"https://www.amazon.com/dp/{p['observed']}")
            self.assertEqual(len(p["token"]), 9)
            self.assertNotEqual(p["token"], p["observed"])

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

    def test_intent_and_observed_never_merge(self):
        """A regression guard for the field-merge this task exists to prevent."""
        for p in json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8")):
            self.assertNotIn("asin", p, f"{p['id']} still carries the ambiguous legacy key")
            self.assertEqual(
                set(), {"intended_asin", "observed"} - set(p),
                f"{p['id']} is missing one half of the register",
            )
            html = (ROOT / "products" / f"{p['slug']}.html").read_text(encoding="utf-8")
            self.assertIn("Intended ASIN", html)
            self.assertIn("Observed redirect target", html)
            self.assertIn("what an ASIN is", html)
            self.assertIn("sell.amazon.com/blog/what-is-an-asin", html)

    def test_every_source_is_dated_and_registered(self):
        sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
        ids = [s["id"] for s in sources]
        self.assertEqual(len(ids), len(set(ids)), "duplicate source id")
        for src in sources:
            self.assertRegex(src["checked"], r"^\d{4}-\d{2}-\d{2}$", src["id"])
            self.assertTrue(src["url"].startswith("https://"), src["id"])
            self.assertTrue(src["used_for"].strip(), src["id"])
        by_id = {s["id"]: s for s in sources}
        self.assertIn("S27", by_id)
        self.assertEqual(by_id["S27"]["url"], "https://sell.amazon.com/blog/what-is-an-asin")
        # Pages that publish their own revision date must have it recorded, not just the read date.
        for sid in ("S01", "S02", "S04"):
            self.assertTrue(by_id[sid].get("page_date"), sid)

    def test_no_page_cites_an_unregistered_host(self):
        from urllib.parse import urlparse
        sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
        allowed = {urlparse(s["url"]).netloc for s in sources}
        allowed |= {"karagemop466-tech.github.io", "github.com"}
        offenders = []
        for f in sorted(ROOT.rglob("*.html")):
            if ".git" in f.parts:
                continue
            for host in re.findall(r'href="https?://([^/"]+)', f.read_text(encoding="utf-8")):
                if host not in allowed:
                    offenders.append(f"{f.relative_to(ROOT)} -> {host}")
        self.assertEqual([], offenders)

    def test_flagged_review_page_publishes_every_open_flag(self):
        flagged = (ROOT / "flagged.html").read_text(encoding="utf-8")
        flags = json.loads((ROOT / "data" / "flags.json").read_text(encoding="utf-8"))
        for f in flags:
            self.assertIn(f["id"], flagged, f"{f['id']} is not published on the review page")
        # Every flag must be answerable: a source link and an owner status.
        for f in flags:
            self.assertTrue(f["links"], f["id"])
            self.assertTrue(f["owner_status"].strip(), f["id"])

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
