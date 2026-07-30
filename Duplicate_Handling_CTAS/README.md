# Episode 11 — Duplicate Handling (CTAS + DISTINCT)

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 11: "Why Did Removing ONE Duplicate Rewrite the ENTIRE Table?"

## The Question

A bad upstream feed sends the same record twice. Can we trust our reports — and why does fixing it with `CREATE OR REPLACE TABLE AS SELECT DISTINCT` rewrite the whole table instead of just the one duplicated row?

## What This Notebook Proves

This is a **fully self-contained** notebook — it creates and uses its own Delta table (`employees_ep11`) in a dedicated path. No other notebook needs to be run first.

Using real transaction log evidence, it verifies:
- A duplicate row can be detected with a simple `GROUP BY ... HAVING COUNT(*) > 1` query
- `CREATE OR REPLACE TABLE ... AS SELECT` is a CTAS operation, not row-level DML — Delta doesn't diff the new result against the old table, it replaces the table's contents outright
- The resulting commit contains `commitInfo`, `metaData`, `add`, and `remove` actions — a full logical rewrite, confirmed by reading the raw JSON directly
- Old files aren't physically deleted — they become orphaned garbage on disk, still there until `VACUUM` runs (setting up the next episode)
- The table's full version history stays intact — `CREATE OR REPLACE` is a new commit, not a DROP + CREATE

Every claim is checked programmatically in cells marked **VERIFY**, which print a pass/fail result rather than relying on visual inspection.

## Prerequisites

- None. This notebook is self-contained.
- Runtime: Databricks Free Edition
- Run Mode: Run All
- Safe to rerun: Yes — resets only its own demo data (`employees_ep11`)

## Watch the video

[Duplicate Handling in Delta Lake | Databricks Masterclass Episode 11](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
