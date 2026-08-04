# Episode 15 — MERGE Internals

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 15: "Same Result, One Statement Instead of Four — What Does Delta Actually Do Differently?"

## The Question

Yesterday's HR feed contains updates, new hires, and resignations, all mixed together. Do we really need UPDATE, UPDATE, DELETE, and INSERT — four separate statements — or can Delta handle everything with ONE command?

## What This Notebook Proves

Using real transaction log and commit evidence (not just claims), this notebook verifies:
- The exact same daily feed, applied two different ways — 4 manual statements vs. 1 `MERGE INTO` — reaches an **identical final data state**
- In this scenario, MERGE completes the same logical work in **fewer commits** than the manual approach — checked directly via `DESCRIBE HISTORY`, not assumed
- MERGE's `operationMetrics` reports exactly how many rows were updated, deleted, and inserted — all in a single commit — and those numbers are checked against the feed's real intent (2 updated, 1 deleted, 2 inserted)
- MERGE's raw `_delta_log` commit JSON contains genuine `add`/`remove` evidence, confirmed by actually reading the file rather than assumed
- MERGE performs a **targeted** change, not a full rewrite — contrasted directly against Episode 11's finding that `CREATE OR REPLACE TABLE AS SELECT` touches every active file regardless of how much data actually changed

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball. A prediction cell (Step 4) also asks viewers to guess the commit counts before revealing the real numbers.

## The Setup

Two independent tables, identical starting data (5 employees), fed the exact same daily HR update:

| Change | Rows |
|---|---|
| Update | eno 1, eno 3 (salary changes) |
| Delete | eno 5 (resigned) |
| Insert | eno 6, eno 7 (new hires) |

| | Table A — `employees_ep15_manual` | Table B — `employees_ep15_merge` |
|---|---|---|
| Method | 2× `UPDATE`, 1× `DELETE`, 1× `INSERT` (4 statements) | 1× `MERGE INTO` (1 statement) |
| Final data | Identical to Table B | Identical to Table A |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own tables (`employees_ep15_manual`, `employees_ep15_merge`) inside a Unity Catalog Volume
- Helpful context, not required: Episode 11's finding that CTAS rewrites every active file is directly referenced as the comparison point in Step 8 — worth watching first if you want the full contrast

## Notes

- The comparison table in Step 9 has a placeholder line — *"Fill in the exact commit counts from Step 5's real output before using this on a slide"* — confirm your own run's numbers before scripting, per this series' standing rule of never hardcoding a number that should come from real output.
- The notebook includes a second, near-duplicate validation pass near the end (cells under "Additional post vacuum validation steps") re-checking the same four claims — final row match, commit counts, MERGE metrics, and physical file counts — using `assert` instead of `if/else`. Both passes check the same things; keep either version depending on how strict you want the on-camera failure behavior to be (`assert` halts the notebook on a failed check, the earlier `if/else` cells just print `❌` and continue).
- MERGE's fewer-commits result is stated as true **for this scenario**, not as a universal guarantee — the exact commit count depends on how a workload is structured.

## Watch the video

[MERGE Internals — Same Result, One Statement Instead of Four | Databricks Masterclass Episode 15](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
