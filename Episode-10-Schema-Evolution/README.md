# Episode 10 — Schema Evolution

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 10: "Will Adding a Column Rewrite My Delta Table?"

## The Question

Business asks for a new column. Does Delta Lake rewrite the entire table to add it — even at billions of rows?

## What This Notebook Proves

Using real transaction log evidence (not just claims), this notebook verifies:
- `ALTER TABLE ADD COLUMNS` creates a new commit containing **only** a `metaData` action — no `add`, no `remove`
- Every existing Parquet file's name **and** byte size is unchanged after the schema change
- Existing rows automatically show the new column as `NULL`, with zero backfill required
- The table's logical schema updates instantly, even though no data file was touched

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## Prerequisites

- Delta_Demo_Day1_Load, Day2_Load, and Day3_Load (from `Delta-Table-Demo`) must already have been run — this episode needs a table with real accumulated history, not a fresh empty one
- Databricks Free Edition

## Watch the video

[Will Adding a Column Rewrite My Delta Table? | Databricks Masterclass Episode 10](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
