#!/usr/bin/env python3
"""
Integration & regression test suite for ShopNow Kitchen.
Run: python3 -m unittest discover -s tests -p "test_*.py" -v
"""
import json
import pathlib
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
        """S25 and FLG-041..043 are registered, sourced and published (never quietly edited)."""
        sources = {x["id"]: x for x in json.loads((ROOT / "data" / "sources.json").read_text())}
        self.assertIn("people-first content", sources["S25"]["name"].lower())
        flags = json.loads((ROOT / "data" / "flags.json").read_text())
        by_id = {f["id"]: f for f in flags}
        for fid in ("FLG-041", "FLG-042", "FLG-043"):
            self.assertIn(fid, by_id)
            self.assertTrue(by_id[fid]["links"], f"{fid} has no source")
            published = (ROOT / "flagged.html").read_text(encoding="utf-8")
            self.assertIn(fid, published)
        # corrected findings stay visible: the dated changelog on sources.html must carry them
        changes = (ROOT / "sources.html").read_text(encoding="utf-8")
        for fid in ("FLG-041", "FLG-042"):
            self.assertIn(fid, changes, f"{fid} is not recorded in the dated changelog")
        self.assertIn("S25", changes)
        self.assertIn("people-first guidance", (ROOT / "how-we-choose.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
