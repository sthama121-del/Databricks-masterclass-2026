# Episode 18 — Change Data Feed (CDF)

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 18: "How Do Downstream Systems Know EXACTLY What Changed — Without Re-Reading the Whole Table?"

## The Question

A downstream analytics system needs to know exactly what changed since yesterday — not the whole table, just the changes. Re-reading and diffing the entire table every time doesn't scale. Is there a better way?

## What This Notebook Proves

Using real transaction log, change-feed, and raw file evidence (not just claims), this notebook verifies:
- Change Data Feed only records changes made **after** it's enabled — it cannot retroactively reconstruct history from before, which is why it's turned on at table creation in the same write
- Querying `readChangeFeed` between two captured version boundaries returns exact row-level change records — 2 `insert` rows, 1 `delete` row, and (the interesting part) **two** rows for a single `UPDATE`: an `update_preimage` (old value) and `update_postimage` (new value), both explicitly captured
- A downstream consumer only needs to remember one number — the last version it already processed — to correctly pull everything new, without ever re-scanning the full table or diffing two snapshots itself
- Whether change data lives in a dedicated `_change_data/` folder or a `cdc` action in the JSON commit log is checked directly against real output, not assumed either way — the notebook explicitly notes Delta can sometimes derive change records from existing `add`/`remove` metadata instead of writing separate files, depending on the operation

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## The Journey

| Step | What happens |
|---|---|
| 1 | Baseline table (3 employees), CDF enabled **at creation**, verified via `DESCRIBE DETAIL` |
| 2 | Starting version captured programmatically |
| 3 | Realistic daily batch: 2 inserts, 1 update, 1 delete |
| 4 | Query the change feed between the two captured versions — inspect `_change_type` row by row |
| 5 | Look for where change data physically lives — `_change_data/` folder, then raw `_delta_log` JSON for `cdc` actions |
| 6 | Simulate a real downstream consumer: track one version number, ask for everything newer |
| 7 | Enterprise framing — and an honest note that CDF isn't free |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own table (`employees_ep18`) inside a Unity Catalog Volume
- Standard path-based architecture, same as every episode since Episode 10 (Episode 17 explains why — CDF has no managed-table restriction, unlike Shallow Clone in Episode 16)

## Notes

- **CDF has a real cost, stated explicitly in Step 7:** enabling it means Delta keeps additional change-tracking data around, with a genuine storage and write overhead. It's a deliberate trade-off for tables that need incremental change tracking, not something to default on everywhere — worth keeping that caveat in the video, not just the "how" of CDF.
- Step 5's outcome (whether a `_change_data/` folder or `cdc` log action actually appears) is explicitly left open in the notebook itself, since it depends on which operations were run and Delta's own internal decision to derive vs. persist change records. Confirm your own run's real output before scripting a definite claim either way.
- This episode's closing line points to **OPTIMIZE** as the next episode.

## Watch the video

[Change Data Feed — How Downstream Systems Know Exactly What Changed | Databricks Masterclass Episode 18](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
