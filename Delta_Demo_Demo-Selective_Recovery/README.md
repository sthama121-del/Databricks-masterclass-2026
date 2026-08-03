# Episode 12 (Part 2) — Selective Recovery

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 12: "RESTORE Can Undo a Mistake — But What If New Data Arrived Since Then?"

## The Question

A bad `UPDATE` corrupted 20 rows. Then 7 more, completely correct, rows arrived. Can we fix the 20 without losing the 7?

## What This Notebook Proves

Using real transaction log evidence (not just claims), this notebook verifies:
- `RESTORE TABLE` can only revert an **entire** table to one past version — there is no "restore only some rows" option
- Running a plain `RESTORE` after new legitimate data has arrived would silently destroy that new data along with the mistake
- A time-travel read of the old clean snapshot can be combined with the current table's untouched rows in a single `CREATE OR REPLACE TABLE AS SELECT`, fixing the corruption without losing anything that arrived afterward
- The corrupted commit stays permanently visible in `DESCRIBE HISTORY` even after being fixed forward — Delta never deletes it just because you moved past it

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## The Story

| Step | State | Row count |
|---|---|---|
| Day 1–3 | Clean baseline builds up normally | 20 rows |
| Mistake | Sign-error `UPDATE` (should be `+10%`, ran as `-10%`) with no `WHERE` clause corrupts every row | 20 rows, all negative |
| Day 4 | 7 fresh, correct rows arrive — nobody has noticed the mistake yet | 27 rows (20 bad + 7 good) |
| Recovery | Selective recovery: re-derive the 20 from the clean time-travel snapshot, keep the 7 as-is, in one query | 27 rows, all correct |

This builds directly on Episode 11's `CREATE OR REPLACE TABLE AS SELECT` pattern — here it's fed by two sources (a past version and the current table) instead of one.

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own table (`sales_ep12`) inside a Unity Catalog Volume
- Helpful to have watched Episode 12 Part 1 (Time Travel & RESTORE) and Episode 11 (`CREATE OR REPLACE TABLE AS SELECT DISTINCT`) first, though not required to follow along

## Notes

- All version numbers referenced in the markdown cells (e.g. "version 3 is the mistake") are captured programmatically inside the notebook, never hardcoded — if you rerun it, confirm your own numbers via `DESCRIBE HISTORY` rather than trusting the commentary.
- This is a continuation of Part 1's Time Travel + RESTORE material, using a fresh table (`sales_ep12`) and a different scenario, so it can be run independently without Part 1.

## Watch the video

[RESTORE Can Undo a Mistake — But What If New Data Arrived Since Then? | Databricks Masterclass Episode 12](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
