# COORDINATION.md — shared task board

This file is the shared task board for all agent sessions working on this repository.
Read it before starting work. Claim a task by writing your session ID and file scope
below, then commit and push the claim immediately.

**Current branch of record:** `arena/9397cc0c-affil2`
**Repository:** `karagemop466-tech/Affil2`
**Base commit:** `12d49cdc2523508f8cc6d2d36257b48e6ffc5529`

> **Note on branch naming.** The house convention is `session-<id>/<task>`. This session is
> bound by the hosting platform to a single branch, `arena/9397cc0c-affil2`, and cannot
> create or push other branches. All work therefore happens on that branch, with one
> session acting as both build session and integration session. This deviation is recorded
> here rather than hidden. Any future session that can use per-task branches should do so.

---

## 1. Task board

| ID | Task | Status | Session | File scope | Notes |
|----|------|--------|---------|-----------|-------|
| T-01 | Repo audit and baseline read | **done** | `arena-9397cc0c` | `README.md` | Repo contained a single 8-byte README. No prior content, no prior COORDINATION.md. |
| T-02 | Resolve the five supplied Amazon short links | **done** | `arena-9397cc0c` | `content/data.json` | All five fetched. One resolved inconsistently — see FLG-001. |
| T-03 | Build the source register from primary sources | **done** | `arena-9397cc0c` | `content/data.json` | 12 sources, all linked and accessed 2026-11-20. |
| T-04 | Product-intent confirmation record with split fields | **done** | `arena-9397cc0c` | `content/data.json` | `intendedAsin` and `observedAsin` are separate keys and are never merged. |
| T-05 | Editorial guides (6, question-shaped) | **done** | `arena-9397cc0c` | `content/guides.json`, `content/bodies/` | Two clusters: choosing a shape, and doneness. |
| T-06 | Suggestions review surface | **done** | `arena-9397cc0c` | `content/suggestions.json` | 13 proposals with evidence, cost and dependencies. |
| T-07 | Open-questions register | **done** | `arena-9397cc0c` | `content/questions.json` | 19 questions across 5 groups; every row names how to close it. |
| T-08 | Empty campaign ledger with defined columns | **done** | `arena-9397cc0c` | `content/ledger.json` | Deliberately zero rows. No forecasts. |
| T-09 | Research / automation boundary page | **done** | `arena-9397cc0c` | `content/research.json` | Documents the three API gates that block automation. |
| T-10 | Site build (single navigation group, disclosure gate) | **done** | `arena-9397cc0c` | `build.js`, `assets/` | Build fails if any page lacks the disclosure. |
| T-11 | Analytics: five events, no identifiers | **done** | `arena-9297cc0c` | `assets/js/site.js` | Collector not deployed; events buffer locally. No endpoint configured. |
| T-12 | Sitemap, RSS feed, robots.txt | **done** | `arena-9397cc0c` | `build.js` | Generated from the same data file as the pages. |
| T-13 | Flagged-for-review publication | **done** | `arena-9397cc0c` | `content/data.json` | 16 items, ordered by severity. |
| T-14 | Integration: merge, re-verify, confirm build | **in progress** | `arena-9397cc0c` | all | Acting as final integration session. |
| T-15 | Open pull request and merge to `main` | **unclaimed** | — | — | Blocked until T-14 signs off. |
| T-16 | Confirm GitHub Pages deploy | **unclaimed** | — | — | Pages source is currently `main` / root. |

Status vocabulary: `unclaimed` · `in progress` · `done` · `needs review`.

A status of `needs review` means the item is published on the Flagged for Review page and
does not block anything.

---

## 2. File ownership

| Scope | Owner | Rule |
|-------|-------|------|
| `content/**` | `arena-9397cc0c` | Shared data. Change only in the integration step once other sessions are done. |
| `build.js` | `arena-9397cc0c` | Generates `docs/**`. Do not hand-edit `docs/**`. |
| `assets/**` | `arena-9397cc0c` | Styles and the event script. |
| `docs/**` | build output | Generated. Never edited by hand. |
| `COORDINATION.md` | `arena-9397cc0c` | Update on every state change. |

If you need a change in a file owned by another session, log the request in section 5
instead of editing the file.

---

## 3. Verification performed

Every row below was checked against a primary source on **2026-11-20**. Sources are
enumerated with links in `content/data.json` and rendered at `/sources/`.

| Check | Method | Result |
|-------|--------|--------|
| Store ID format `shopnow047c-20` | Amazon Associates help, node 51812349011 | Matches documented US format; Amazon states it appends `-20` to all Store IDs. **Verified format only.** |
| Link `B04G1MEwY` | HTTP GET, redirects followed | Resolves to `amazon.com/dp/B0CDY277D3`. |
| Link `B02NbDxp3` | HTTP GET, redirects followed | Resolves to `amazon.com/dp/B09B7SB46R`. |
| Link `B00hJ57DV` | HTTP GET; one bot checkpoint, then success | Resolves to `amazon.com/dp/B08DKYBTPH`. |
| Link `B0c8moW59` | HTTP GET twice | **Inconsistent**: product page once, Amazon homepage once. Held from publication. |
| Link `B0f3GKalj` | HTTP GET twice | Resolves to `amazon.com/dp/B0DZFD6R9Z` both times. |
| Short code length | Programmatic count | All five codes are 9 characters; ASINs are 10. Codes are opaque, not ASINs. |
| Required disclosure wording | Operating Agreement §5 | Quoted exactly; rendered twice per page. |
| Price / rating display limits | Participation Requirements 2(b), 3(t) | Prices and ratings suppressed site-wide. Build gate enforces this. |
| Link integrity rules | Participation Requirements 3(v), 3(w) | No cloaking, no third-party shortener used anywhere on the site. |
| PA-API 5 status | Creators API deprecation notice | Deprecated; returns HTTP 403. Replacement is the Creators API. |
| Creators API prerequisite | Creators API introduction | Requires enrollment plus ≥10 qualifying sales in 30 days. Not met. |
| Food-safety temperatures | USDA FSIS chart | Quoted and linked; not restated from memory. |

All five supplied links are also rendered as live `rel="sponsored nofollow"` anchors, so a
reviewer can re-check them by hand in a browser.

---

## 4. Irregularities

Sixteen items are published on the site at `/flagged/`, ordered by severity, each with its
evidence link. The highest-consequence ones:

- **FLG-001** — `B0c8moW59` resolved to a product page once and the Amazon homepage once.
- **FLG-003** — Compliance status of the supplied `link.amazon` short links is unresolved. No
  claim is made that they are invalid.
- **FLG-004** — No tracking tag was observed in any resolved destination.
- **FLG-010** — Prices observed during verification are deliberately not published.

These do **not** block the merge. They are published for review.

---

## 5. Cross-session requests

None outstanding. No other session has claimed work in this repository as of the latest
commit on this branch.

---

## 6. Log

| When (UTC) | Session | Event |
|-----------|---------|-------|
| 2026-11-20 | `arena-9397cc0c` | Read repo at `12d49cd`, found only an 8-byte README. Created this board. |
| 2026-11-20 | `arena-9397cc0c` | Claimed T-01 through T-14. |
| 2026-11-20 | `arena-9397cc0c` | Resolved all five short links; recorded one inconsistency. |
| 2026-11-20 | `arena-9397cc0c` | Built the site: 24 pages, sitemap, feed, robots, 404, four compliance gates. |
| 2026-11-20 | `arena-9397cc0c` | Pages source on `main/root` could not be switched via API (token lacks Pages admin). Mitigation applied — see §7. |

---

## 7. Handoff notes

- **Pages source.** The Pages API returned `403 Resource not accessible by integration`
  when asked to switch the source to `docs/` on this branch. The token lacks Pages
  administration. Fallback in place: the build output is committed at the repository root
  after merge, which matches the existing `main` / `/` Pages configuration.
- **No collector.** `assets/js/config.js` has an empty `analyticsEndpoint`. Events buffer in
  a 50-entry local ring buffer and are never transmitted. This is intentional until a
  collector and a privacy notice exist.
- **Capture form.** Disabled by design. It reports that no provider is connected rather
  than silently discarding an address.
- **Never hand-edit `docs/`.** Run `node build.js`.

---

## 8. Pull request and merge record

| Field | Value |
|-------|-------|
| PR | _pending_ |
| Merge result | _pending_ |
| Pages deploy | _pending_ |
| Live URL | https://karagemop466-tech.github.io/Affil2/ |
