# COORDINATION.md — shared task board

Branch for this session: `arena/990af5de-affil2` (base `12d49cd`, main). All work stays on this branch.
Other sessions: none detected at start (repo contained only `README.md`). Claims below are written in this file so any parallel session can see them.

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything).

## Task board

| ID | Task | Status | Owner (session) | Files touched |
|---|---|---|---|---|
| T-01 | Repo review + irregularity log | done | arena/990af5de-affil2 | `COORDINATION.md`, `data/findings.json` |
| T-02 | Verify supplied Amazon links (product-intent record) | needs review | arena/990af5de-affil2 | `data/products.json`, `docs/intent/` |
| T-03 | Verify official policy/regulation sources | done | arena/990af5de-affil2 | `data/sources.json` |
| T-04 | Site build (landing + category subpages) | done | arena/990af5de-affil2 | `tools/`, `docs/`, `data/` |
| T-05 | Disclosure strip + footer on every page | done | arena/990af5de-affil2 | `tools/build_site.py`, `docs/assets/` |
| T-06 | Outbound click + analytics endpoint | needs review (blocked on hosting decision; see Suggestions) | arena/990af5de-affil2 | `docs/assets/track.js`, `data/site.json` |
| T-07 | Findable: sitemap, robots, RSS feed | done | arena/990af5de-affil2 | `docs/sitemap.xml`, `docs/feed.xml`, `docs/robots.txt` |
| T-08 | Campaign ledger (empty, schema only) | done | arena/990af5de-affil2 | `data/campaign-ledger.csv`, `docs/ledger/` |
| T-09 | Suggestions + questions dashboard (no changes implemented) | done | arena/990af5de-affil2 | `data/suggestions.json`, `data/questions.json` |
| T-10 | Integration: check script, build, PR to main, merge, Pages | in progress | arena/990af5de-affil2 | `tools/check_site.py`, `COORDINATION.md` |

## Log

- **2026-11-20 · arena/990af5de-affil2 · claim** — Claimed T-01..T-10 (single session; no conflicting claims found). Scope: whole repo on this branch.
- **2026-11-20 · T-01** — Repo contained `README.md` only. No `data/`, no site, no prior COORDINATION file. Created this file.
- **2026-11-20 · T-02** — Opened the five supplied `link.amazon` short links (fetch on 2026-11-20). Findings: the path tokens are 9 characters long, not the 10-character ASIN length cited in third-party references; two links resolved to a different ASIN than their token; two resolved to the Amazon homepage; one resolved to a checkpoint page; two returned HTTP 500 on first attempt. Full detail in `data/findings.json` (F-01..F-04) and `data/products.json`.
- **2026-11-20 · T-03** — Read official sources: Associates Operating Agreement (updated Oct 15, 2025), Associates Program Policies (updated Apr 14, 2026, first chunks only), Google Search Central "Qualify your outbound links" (updated 2025-12-10), eCFR 16 CFR Part 255 (up to date as of 11/18/2026). Official Amazon ASIN definition was NOT located; the 10-character rule is cited only from third-party pages and is flagged.
- **2026-11-20 · T-04..T-09** — Built static site with `tools/build_site.py` from `data/*.json`; output in `docs/` (GitHub Pages source: `main` / `docs`).
- **2026-11-20 · T-06** — Client-side click/event hook is in place but DISABLED (no endpoint configured). GitHub Pages cannot run a server-side endpoint; the endpoint decision is listed on the Suggestions page.
- **2026-11-20 · T-10** — Pending: check script, PR, merge, Pages deploy confirmation.

## Handoff / conflicts

- No merge conflicts occurred. No other session's work was overwritten.
- Referenced IDs in the brief (S01, S07, S24, SG-27..SG-30, FLG-003, "Operating Agreement" register) do not exist in this repository. They were not used as sources. Logged as F-06.
