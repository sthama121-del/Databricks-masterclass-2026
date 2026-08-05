# Episode 16 — Shallow Clone

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 16: "Copy a Delta Table Without Copying Data — Does It Survive VACUUM? 😲"

## The Question

Can you create a full, independently-queryable copy of a Delta table without physically duplicating its data — and does it survive if someone cleans up the original afterward?

## What This Notebook Proves

Using real metadata and operation-log evidence (not just claims), this notebook verifies:
- `SHALLOW CLONE` creates an instantly-queryable copy with **zero files and zero bytes physically copied** — confirmed directly from the clone's own `operationMetrics` (`numCopiedFiles: 0`, `copiedFilesSize: 0`), not assumed from how fast it ran
- The clone has its own independent transaction log — writing to the clone never touches the source's history, and vice versa
- A genuine, confirmed physical file deletion on the source — via `OPTIMIZE` + `deletedFileRetentionDuration = 0` + real `VACUUM` (not a `DRY RUN`) — is verified by checking `numDeletedFiles > 0` before drawing any conclusion
- **The clone keeps working even after that real deletion, and even after the source table is `DROP TABLE`'d entirely** — tested directly by querying and then updating the clone post-deletion, not predicted

## The Twist — Why This Episode Deliberately Breaks Series Convention

Every episode since Episode 10 has used path-based tables in a Unity Catalog Volume. This one **switches to real Unity Catalog managed tables** instead — a source-code confirmed necessity, since `SHALLOW CLONE` on a path-based table in this environment throws a real `CANNOT_SHALLOW_CLONE_NON_UC_MANAGED_TABLE_AS_SOURCE_OR_TARGET` error.

That switch has a real consequence: **the commonly-cited warning that "Shallow Clone breaks once the source is VACUUMed" does not hold here.** Unity Catalog's managed-table relationship tracking protects the clone even after the source's underlying files are genuinely deleted — confirmed against real Databricks documentation, not just this notebook's own run. The classic/Hive-metastore pattern most tutorials describe is a different architecture with a different (breakable) result.

## The Journey

| Step | What happens |
|---|---|
| 1 | Baseline managed table, 5 employees |
| 2 | `SHALLOW CLONE` — instant |
| 3 | Confirm 0 files / 0 bytes physically copied, from real `operationMetrics` |
| 4 | Modify the clone — confirm the source is completely untouched |
| 5 | Force a **real, confirmed** physical deletion on the source (`OPTIMIZE` → 0-hour retention → `VACUUM`, verified via `numDeletedFiles > 0`) |
| 6 | Query the clone — still works. Then `DROP TABLE` the source entirely — clone still works, and is still independently updatable |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own tables (`employees_ep16_source`, `employees_ep16_clone`) as real Unity Catalog managed tables (not path-based, unlike most of this series)
- Helpful context, not required: Episode 14's VACUUM mechanics (retention override, `DRY RUN` vs. real deletion) are reused here as the tool that forces the source's real physical deletion

## Notes

- Step 5's `deletedFileRetentionDuration = 'interval 0 hours'` override is a **demo-only technique**, same caveat as Episode 14 — never run this against a live production table without knowing exactly who else might be reading it.
- Step 5 includes a real fallback: if `numDeletedFiles` comes back as 0 on your run (can happen depending on auto-OPTIMIZE timing), the notebook tells you to re-run the UPDATE + OPTIMIZE + VACUUM cycle until it's genuinely greater than 0 before trusting the result in Step 6 — don't skip that check.
- The very last few cells (after "END") continue querying and updating the clone post-DROP as informal extra proof of independence — no new claims are introduced there.

## Watch the video

[Shallow Clone — Does It Survive VACUUM? | Databricks Masterclass Episode 16](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
