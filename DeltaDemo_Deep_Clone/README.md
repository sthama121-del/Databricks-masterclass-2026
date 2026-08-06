# Episode 17 — Deep Clone

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 17: "Why Deep Clone Survives When Shallow Clone Breaks."

## The Question

Episode 16 proved Shallow Clone shares physical files with its source — copying zero bytes. Does the exact same destructive test (OPTIMIZE + aggressive VACUUM on the source, then dropping it entirely) break a Deep Clone too?

## What This Notebook Proves

Using real transaction log, metrics, and raw file-listing evidence (not just claims), this notebook verifies:
- `DEEP CLONE` genuinely physically duplicates every data file — confirmed two independent ways: real `operationMetrics` (`numCopiedFiles > 0`, `copiedFilesSize > 0`, both exactly `0` for Shallow Clone in Episode 16), and literally listing the Parquet files in both folders to confirm the clone's files are separately-named and share zero filenames with the source
- Modifying the clone leaves the source completely untouched, same as Shallow Clone (this part isn't the interesting difference)
- Running the **exact same destructive sequence from Episode 16** (`OPTIMIZE`, retention override, `VACUUM`, then deleting the source entirely) against a Deep Clone's source still leaves the clone fully queryable — because it was never sharing files with the source to begin with

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## Why This Episode Returns to Path-Based Tables

Episode 16 had to switch to real Unity Catalog managed tables because `SHALLOW CLONE` requires them in this environment. `DEEP CLONE` has no such restriction — it works fine on ordinary path-based tables — so this episode returns to the standard `/Volumes/.../<name>` architecture used since Episode 10, and raw `%sh` file browsing is back.

## The Journey

| Step | What happens |
|---|---|
| 1 | Baseline path-based table, 5 employees |
| 2 | `DEEP CLONE` |
| 3 | Two independent proofs of real physical duplication: `operationMetrics`, then a raw filename comparison between the two folders |
| 4 | Modify the clone — confirm the source is untouched |
| 5 | The exact destructive sequence that (in Episode 16) broke the shared-file assumption: `OPTIMIZE` → 0-hour retention override → `VACUUM` on the source, then query the clone |
| 6 | Delete the source entirely (`rm -rf`) — query the clone again |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own tables (`employees_ep17_source`, `employees_ep17_clone`) inside a Unity Catalog Volume
- Watching Episode 16 (Shallow Clone) first makes the contrast land much better, though this notebook doesn't depend on it technically — Step 5's framing explicitly asks viewers to recall Episode 16's result before revealing this one

## Notes

- Step 5's `deletedFileRetentionDuration = 'interval 0 hours'` override is a **demo-only technique**, same caveat as Episodes 14 and 16 — never run this against a live production table without knowing exactly who else might be reading it.
- **Worth checking before you script this:** unlike Episode 14/16, Step 5 here does not verify `numDeletedFiles > 0` after the `VACUUM` — Cell 26's own comment notes that Free Edition serverless may block sub-7-day retention regardless of the table property override. If `VACUUM` turns out to be a no-op on your run, the clone surviving Step 5 wouldn't yet be a real test of anything — confirm real file deletion happened before treating the result as proof, the same way Episode 16 did.
- Step 6 (dropping the source entirely) is the cleaner, stronger proof either way, and doesn't depend on whether Step 5's VACUUM actually deleted anything.

## Watch the video

[Deep Clone — Why It Survives When Shallow Clone Breaks | Databricks Masterclass Episode 17](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
