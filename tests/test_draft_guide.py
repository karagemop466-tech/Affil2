#!/usr/bin/env python3
"""T-34 tests: the draft pipeline must catch exactly the things a careful editor would catch.

Run: python3 -m unittest discover -s tests
"""
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import draft_guide as dg  # noqa: E402


def draft(**over):
    base = {
        "slug": "test-draft",
        "status": "unapproved",
        "title": "Does an air fryer need 1700 watts?",
        "question": "What a wattage line can and cannot tell you",
        "products": ["P-01"],
        "sources": ["S10"],
        "sections": [
            "The listing states 120 volts and 1700 watts in its specification table.",
            "Reheating leftovers is a temperature question: USDA puts leftovers at 165 degrees.",
            "Nobody here cooked in this unit, and no cook time appears on this page. Links to the "
            "listing are affiliate links, marked as paid.",
        ],
    }
    base.update(over)
    return base


class DraftLintTests(unittest.TestCase):
    def test_a_clean_draft_is_clean(self):
        findings, problems = dg.lint(draft())
        self.assertEqual([], problems, msg=json.dumps(problems, indent=1))

    def test_a_price_is_rejected(self):
        _, problems = dg.lint(draft(sections=["It costs $79.99 on the listing today."]))
        self.assertIn("price_or_rating", {p["rule"] for p in problems})

    def test_a_star_rating_is_rejected(self):
        _, problems = dg.lint(draft(sections=["It holds 4.6 out of 5 stars."]))
        self.assertIn("price_or_rating", {p["rule"] for p in problems})

    def test_an_unverified_figure_is_rejected(self):
        _, problems = dg.lint(draft(sections=["The housing runs at 26.5 pounds and 1450 watts."]))
        rules = {p["rule"] for p in problems}
        self.assertIn("figure_sourced", rules)

    def test_a_contested_figure_needs_the_conflict_in_the_sentence(self):
        base = draft()["sections"]
        trio = ["P-01", "P-04", "P-05"]
        # a figure the register refuses to confirm may not be stated as fact
        _, problems = dg.lint(draft(products=trio, sections=base + [
            "The probes run 70 hours on a charge."]))
        self.assertIn("figure_sourced", {p["rule"] for p in problems})

        # the same figure is allowed when the sentence shows the other one and says they disagree
        findings, problems = dg.lint(draft(products=trio, sections=base + [
            "The listing gives 50 hours in one field and 70 hours in another; both figures are "
            "published here and they disagree."]))
        self.assertEqual([], problems, msg=json.dumps(problems, indent=1))
        self.assertIn("conflict_visible", {f["rule"] for f in findings})

    def test_missing_honesty_and_disclosure_are_blockers(self):
        _, problems = dg.lint(draft(sections=[
            "The listing states 1700 watts.", "A second section.", "A third section."]))
        rules = {p["rule"] for p in problems}
        self.assertIn("honesty_clause", rules)
        self.assertIn("disclosure_note", rules)

    def test_an_unknown_product_or_source_is_a_blocker(self):
        _, problems = dg.lint(draft(products=["P-99"], sources=["S99"]))
        rules = {p["rule"] for p in problems}
        self.assertIn("product_linked", rules)
        self.assertIn("sourced", rules)

    def test_approval_requires_a_clean_draft_and_a_named_human(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = dg.DRAFTS
            dg.DRAFTS = pathlib.Path(tmp)
            try:
                blocked = draft(sections=["It costs $19.99 and nobody tested it; affiliate link."])
                dg._write("blocked", blocked)
                rc = dg.cmd_approve(type("A", (), {"slug": "blocked", "by": "Editor"})())
                self.assertEqual(1, rc, "a draft that fails the rules must not be approvable")
                self.assertEqual("unapproved", dg._read("blocked")["status"])

                dg._write("fine", draft())
                with self.assertRaises(SystemExit):
                    dg.cmd_approve(type("A", (), {"slug": "fine", "by": "x"})())
                rc = dg.cmd_approve(type("A", (), {"slug": "fine", "by": "R. Editor"})())
                self.assertEqual(0, rc)
                rec = dg._read("fine")
                self.assertEqual("approved", rec["status"])
                self.assertEqual("R. Editor", rec["approval"]["by"])
                # approval is not publication: the generator is untouched by this tool
                self.assertNotIn("fine", (ROOT / "scripts" / "traffic_guides.py").read_text())
            finally:
                dg.DRAFTS = old

    def test_a_draft_is_never_a_page(self):
        # the build gate treats every .html file in the repo as a submitted page, so drafts must
        # stay JSON; a .json draft cannot enter the sitemap accidentally.
        self.assertFalse(list((ROOT / "data" / "drafts").glob("*.html")))


if __name__ == "__main__":
    unittest.main()
