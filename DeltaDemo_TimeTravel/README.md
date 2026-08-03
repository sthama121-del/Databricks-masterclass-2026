# Episode 12 — Time Travel & RESTORE

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 12, Part 1: "Two Real Recoveries, Plus: What Actually Triggers a Checkpoint?"

## The Question

Two different real-world mistakes happen to the same table. Can Time Travel and RESTORE recover from both — and does recovering trigger anything else happening behind the scenes?

## What This Notebook Proves

Using real transaction log evidence (not just claims), this notebook verifies:
- Time Travel (`VERSION AS OF`) can read a table's state as of any earlier commit, even after every row has been deleted from the current version
- `RESTORE TABLE ... TO VERSION AS OF` brings a table back to an earlier state as a **new forward commit** — it does not delete or rewrite history
- A full accidental `DELETE` (Scenario 1) and a partially corrupted batch (Scenario 2) call for different recovery judgment, even though both use the same Time Travel + RESTORE mechanism
- Whether `RESTORE` specifically triggers an immediate Delta checkpoint — tested twice against real evidence, and contrasted with 8 ordinary `UPDATE` commits that (on this run) triggered none

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## The Two Scenarios

| Scenario | What happens | How it's recovered |
|---|---|---|
| **1 — Accidental full DELETE** | A production job runs `DELETE FROM employees;` with no `WHERE` clause | `RESTORE` straight back to the last known-good version |
| **2 — Truncated Day 2 batch** | A source system bug cuts the first 2 characters off every name in a new batch | `RESTORE` back to the clean Day 1 version, then request a correct resend — never try to reconstruct lossy truncated data yourself |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own table (`employees_ep12`) inside a Unity Catalog Volume
- Basic SQL familiarity; no prior Delta Lake experience required

## Notes

- The checkpoint-trigger result (RESTORE creating a checkpoint, ordinary commits not) is real evidence from one specific run on Free Edition serverless compute — not documented Delta behavior. If you rerun this notebook and get a different result, that's a genuinely interesting finding in its own right; trust your own `DESCRIBE HISTORY` and `_delta_log` output over the notebook's narration.
- This is **Part 1**. Part 2 continues the same table with legitimate new data arriving between a mistake and its fix — a messier, more realistic recovery scenario.

## Watch the video

[Time Travel & RESTORE — Two Real Recoveries | Databricks Masterclass Episode 12](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
