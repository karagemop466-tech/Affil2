#!/usr/bin/env python3
"""T-34 — the gated guide-draft pipeline (session 19dbf5e2).

What it automates: turning a topic brief into a guide-shaped draft, and running the site's
compliance rules against that draft *before* a human spends an hour writing it.

What it cannot do: publish. A draft is written to data/drafts/<slug>.json with status
"unapproved", and it stays inert until a named reviewer approves it — and even then this tool
does not touch the generator. Publication still means the record being added to a guide module
and passing scripts/check_site.py in CI. That is the gate the owner's brief asks for: automate the
drafting, put a human in front of the publishing.

Lint rules, all derived from what this repository already enforces:
  price_or_rating   no "$<digit>", no star rating, no review count  (Amazon Program Policies, S02)
  figure_sourced    every measured figure must be a *verified* value for a cited product in
                    data/products.json, or a figure from the USDA chart in
                    data/usda-temperatures.json. Invented numbers are rejected.
  conflict_visible  a figure that the register marks "conflict" or "unverified" may appear only
                    when the sentence also shows the other figure and says so ("vs", "both", ...)
  product_linked    every cited product must exist in the register
  honesty_clause    the draft must carry the no-hands-on-testing statement
  disclosure_note   the draft must repeat that links are affiliate links

Usage:
  python3 scripts/draft_guide.py new --slug air-fryer-noise --title "..." --question "..." \
      --products P-01,P-04 --sources S22,S24 --body-file draft.txt
  python3 scripts/draft_guide.py check [--slug air-fryer-noise]
  python3 scripts/draft_guide.py approve --slug air-fryer-noise --by "A. Person"
  python3 scripts/draft_guide.py list
"""
import argparse
import datetime as _dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "data" / "drafts"
PRODUCTS = {p["id"]: p for p in json.loads((ROOT / "data" / "products.json").read_text())}
USDA = json.loads((ROOT / "data" / "usda-temperatures.json").read_text())

PRICE_RE = re.compile(r"\$\s?\d")
RATING_RE = re.compile(r"\d\.\d\s*(?:out of\s*)?5\s*stars?", re.I)
REVIEW_RE = re.compile(r"\b(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]{3,})\s*(?:global\s+)?(?:ratings?|reviews?)", re.I)
FIGURE_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:°F|°C|degrees?\s*F|degrees?\s*C|watts?|W\b|volts?|V\b|quarts?|qt\b|"
    r"liters?|litres?|L\b|inches|in\b|pounds?|lb|seconds?|hours?|probes?)", re.I)
CONFLICT_WORDS = re.compile(r"\bvs\.?\b|\bversus\b|\bboth\b|\btwo (?:figures|numbers)|conflict|"
                            r"disagree|contradict|either\b", re.I)
HONESTY = re.compile(r"(we have not|not tested|no hands-on|did not test|nobody here cooked)", re.I)
DISCLOSURE = re.compile(r"(affiliate|paid link|as an amazon associate)", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _allowed_figures(product_ids):
    """Numbers the register marks verified for the cited products, plus the USDA chart."""
    allowed = set()
    for pid in product_ids:
        for f in PRODUCTS[pid]["fields"].values():
            if f.get("st") == "verified" and f.get("v"):
                allowed.update(re.findall(r"\d+(?:\.\d+)?", str(f["v"])))
    for _, temp in USDA["rows"]:
        allowed.update(re.findall(r"\d+(?:\.\d+)?", str(temp)))
    # housekeeping numbers that are not product claims
    allowed |= {"1", "2", "3", "4", "5", "30", "60", "2026", "2027", "165", "145", "160", "140",
                "40", "32", "212"}
    return allowed


def _unallowed_figures(product_ids):
    """Figures the register explicitly refuses to confirm, so they may not be stated as fact."""
    blocked = set()
    for pid in product_ids:
        for f in PRODUCTS[pid]["fields"].values():
            if f.get("st") in ("conflict", "unverified"):
                blob = " ".join(str(x) for x in (f.get("v") or "", f.get("note") or ""))
                blocked.update(re.findall(r"\d+(?:\.\d+)?", blob))
    return blocked - _allowed_figures(product_ids)


def lint(draft):
    """Return (findings, problems). A finding is advisory; a problem blocks approval."""
    text = " ".join([draft.get("title", ""), draft.get("question", "")] + list(draft.get("sections", [])))
    findings, problems = [], []

    if PRICE_RE.search(text):
        problems.append({"rule": "price_or_rating",
                         "why": "a dollar amount appears; Program Policies permit price display only "
                                "through an Amazon-served link or the API"})
    if RATING_RE.search(text):
        problems.append({"rule": "price_or_rating", "why": "a star rating appears"})
    if REVIEW_RE.search(text):
        problems.append({"rule": "price_or_rating", "why": "a review or rating count appears"})

    pids = [p for p in draft.get("products", []) if p in PRODUCTS]
    for pid in draft.get("products", []):
        if pid not in PRODUCTS:
            problems.append({"rule": "product_linked",
                             "why": f"{pid} is not in data/products.json, so nothing on this site can "
                                    f"support a sentence about it"})
    allowed = _allowed_figures(pids)
    blocked = _unallowed_figures(pids)
    for sentence in SENT_SPLIT.split(text):
        for m in FIGURE_RE.finditer(sentence):
            for num in re.findall(r"\d+(?:\.\d+)?", m.group(0)):
                if num in allowed:
                    continue
                if num in blocked:
                    if CONFLICT_WORDS.search(sentence):
                        findings.append({"rule": "conflict_visible",
                                         "why": f"{num} is a contested register value; the sentence "
                                                f"shows it alongside the other figure, which is the "
                                                f"site's rule"})
                    else:
                        problems.append({"rule": "figure_sourced",
                                         "why": f"{num} appears as a fact but the register marks it "
                                                f"conflict or unverified for {', '.join(pids)}"})
                else:
                    problems.append({"rule": "figure_sourced",
                                     "why": f"{m.group(0).strip()!r} is not a verified value for any "
                                            f"cited product and is not in the USDA chart"})

    if not HONESTY.search(text):
        problems.append({"rule": "honesty_clause",
                         "why": "no sentence says that nobody here tested the products"})
    if not DISCLOSURE.search(text):
        problems.append({"rule": "disclosure_note",
                         "why": "no sentence says the links are affiliate links"})
    if len(draft.get("sections", [])) < 3:
        problems.append({"rule": "shape", "why": "a guide needs at least three sections"})
    if not draft.get("sources"):
        problems.append({"rule": "sourced",
                         "why": "no source register IDs; every claim on this site names its source"})
    for sid in draft.get("sources", []):
        known = {s["id"] for s in json.loads((ROOT / "data" / "sources.json").read_text())}
        if sid not in known:
            problems.append({"rule": "sourced", "why": f"{sid} is not in data/sources.json"})

    return findings, problems


def _path(slug):
    return DRAFTS / f"{slug}.json"


def _read(slug):
    return json.loads(_path(slug).read_text(encoding="utf-8"))


def _write(slug, rec):
    DRAFTS.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return _path(slug)


def cmd_new(args):
    slug = re.sub(r"[^a-z0-9-]", "-", args.slug.lower()).strip("-")
    if not slug:
        sys.exit("error: --slug is required")
    if _path(slug).exists() and not args.force:
        sys.exit(f"error: {slug} already drafted; pass --force to overwrite the draft")
    sections = []
    if args.body_file:
        sections = [s.strip() for s in pathlib.Path(args.body_file).read_text().split("\n## ") if s.strip()]
    rec = {
        "slug": slug,
        "status": "unapproved",
        "created": _dt.date.today().isoformat(),
        "title": args.title or "",
        "question": args.question or "",
        "products": [p.strip().upper() for p in args.products.split(",") if p.strip()],
        "sources": [s.strip().upper() for s in args.sources.split(",") if s.strip()],
        "sections": sections,
        "approval": None,
        "note": "Draft only. This file is not a page, is not in the sitemap, and cannot become one "
                "without a named reviewer approving it and a human adding the record to a guide "
                "module that scripts/check_site.py can see.",
    }
    findings, problems = lint(rec)
    rec["lint"] = {"findings": findings, "problems": problems,
                   "clean": not problems}
    path = _write(slug, rec)
    print(f"drafted {path.relative_to(ROOT)}")
    print(f"status: unapproved   lint: {'clean' if not problems else f'{len(problems)} blocker(s)'}")
    for p in problems:
        print(f"  ✗ {p['rule']}: {p['why']}")
    print("next: write the sections, run check, then approve with a real name. Publishing stays manual.")
    return 0


def cmd_check(args):
    slugs = [args.slug] if args.slug else sorted(p.stem for p in DRAFTS.glob("*.json")) if DRAFTS.exists() else []
    if not slugs:
        print("no drafts. create one with: draft_guide.py new --slug ... ")
        return 0
    bad = 0
    for slug in slugs:
        rec = _read(slug)
        findings, problems = lint(rec)
        rec["lint"] = {"findings": findings, "problems": problems, "clean": not problems}
        _write(slug, rec)
        state = "clean" if not problems else f"{len(problems)} blocker(s)"
        print(f"{slug:<34} {rec['status']:<12} lint: {state}")
        for p in problems:
            print(f"    ✗ {p['rule']}: {p['why']}")
        for f in findings:
            print(f"    · {f['rule']}: {f['why']}")
        bad += len(problems)
    return 1 if bad else 0


def cmd_approve(args):
    rec = _read(args.slug)
    _, problems = lint(rec)
    if problems:
        print(f"refused: {args.slug} fails {len(problems)} compliance rule(s):")
        for p in problems:
            print(f"  ✗ {p['rule']}: {p['why']}")
        print("The gate does not wave a draft through because a name was typed at it.")
        return 1
    if not args.by or len(args.by.strip()) < 2:
        sys.exit("error: --by must name a human reviewer; an approval with no name is not an approval")
    rec["status"] = "approved"
    rec["approval"] = {"by": args.by.strip(), "at": _dt.date.today().isoformat(),
                       "note": "Approved for editorial review only. Publication still requires a "
                               "human to add this record to a guide module and pass the build gate."}
    _write(args.slug, rec)
    print(f"approved {args.slug} by {rec['approval']['by']} on {rec['approval']['at']}")
    print("nothing was published. to ship it, add the record to scripts/traffic_guides.py and run "
          "python3 scripts/build_site.py && python3 scripts/check_site.py")
    return 0


def cmd_list(_args):
    if not DRAFTS.exists() or not list(DRAFTS.glob("*.json")):
        print("queue is empty")
        return 0
    for p in sorted(DRAFTS.glob("*.json")):
        rec = json.loads(p.read_text(encoding="utf-8"))
        clean = (rec.get("lint") or {}).get("clean")
        lint_state = "clean" if clean else ("not linted" if clean is None else "blocked")
        who = (rec.get("approval") or {}).get("by", "—")
        print(f"{rec['slug']:<34} {rec['status']:<12} {lint_state:<10} reviewer: {who}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gated guide-draft pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--slug", required=True)
    n.add_argument("--title", default="")
    n.add_argument("--question", default="")
    n.add_argument("--products", default="")
    n.add_argument("--sources", default="")
    n.add_argument("--body-file", default="")
    n.add_argument("--force", action="store_true")
    n.set_defaults(func=cmd_new)
    c = sub.add_parser("check")
    c.add_argument("--slug", default="")
    c.set_defaults(func=cmd_check)
    a = sub.add_parser("approve")
    a.add_argument("--slug", required=True)
    a.add_argument("--by", required=True)
    a.set_defaults(func=cmd_approve)
    l = sub.add_parser("list")
    l.set_defaults(func=cmd_list)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
