# Episode 21 — What Happens When a Delta Log JSON Commit File Is Accidentally Deleted?

Part of the **Data Dharma** Databricks Delta Lake series — *hype కాదు, exact truth.*

## The Question

A checkpoint summarizes a Delta table's state so readers don't have to replay every commit from version 0. But does that mean a checkpoint *protects* the table if someone deletes a piece of its transaction log?

This notebook answers that with a small, six-sale ledger — not a big synthetic dataset, so every result fits on one screen. Same visual language throughout: **JSON commit = receipt. Checkpoint = running summary. Latest table = today's total. Time travel = an old day's exact report.**

## What This Notebook Proves

Four short experiments, each ending in the same three-line scoreboard (`LATEST READ` / `TIME TRAVEL` / `NEW WRITE`):

- **A — Healthy ledger.** Six sales rung up one at a time, checkpoint written automatically at `delta.checkpointInterval = 3`. This is the baseline every later experiment deliberately damages.
- **B — Delete a receipt *before* the checkpoint.** Sale #2's own commit file is deleted, but the checkpoint at version 3 already absorbed it.
- **C — Delete a receipt *after* the checkpoint, but not the newest one.** Sale #7's commit is deleted while Sale #8's commit still physically exists — proving this isn't secretly "delete the latest commit" in disguise.
- **D — Delete the *newest* receipt.** The very last commit is deleted, then a new sale is attempted — twice, including in a completely fresh Python session, to rule out caching.

The closing takeaway printed by the notebook: **CHECKPOINT ≠ BACKUP.** A checkpoint helps Delta reconstruct table state efficiently — it does not guarantee every old version survives manual deletion of transaction-log files.

## The Journey

| Step | What happens | Why it matters |
|---|---|---|
| 0 — Reset | Clears all four demo paths | Guarantees a true clean slate on every re-run |
| 1 — Create table | `CREATE TABLE` with `checkpointInterval = 3` | Forces a checkpoint early, so it fits in six sales |
| 2 — Ring up 6 sales | One `INSERT` per sale, running total shown each time | Makes "one commit = one sale" literal and visible |
| 3 — Confirm the checkpoint | Lists the real `_delta_log/` files, finds the checkpoint version programmatically | Never assumes where the checkpoint landed — checks |
| 4 — Build three twin ledgers | Fresh `CREATE TABLE` + `INSERT` per experiment, not cloned | A clone would front-load all rows into version 0, making "delete Sale #2's commit" delete an empty placeholder instead of a real one |
| Experiment B | Delete Sale #2's JSON, run the scoreboard | Before-checkpoint deletion |
| Experiment C | Delete Sale #7's JSON (Sale #8 survives), run the scoreboard | After-checkpoint, non-latest deletion — the genuinely dangerous case |
| Experiment D | Delete Sale #6's JSON (the newest), attempt a new write | Latest-commit deletion |
| 5 — Summary | Auto-generated from the scoreboard variables set above | No manual copy-pasting of results |
| Bonus | `%restart_python`, then retry the write with zero prior reads | Confirms Experiment D's failure isn't a caching artifact |

## Prerequisites

- Databricks Free Edition (Serverless) or any workspace with Unity Catalog Volumes enabled
- A writable Volume path — this notebook uses `/Volumes/workspace/delta_demo/demo_files/`, update the four path variables in Step 0 if yours differs
- No cluster configuration needed beyond what Serverless provides by default

## Notes

- **This is the SQL-centric variant** of the demo. Python is used only where SQL genuinely can't do the job: listing `_delta_log/` files, finding the checkpoint version, and the shared test-helper functions (`try_read_sql`, `try_write_sql`, `scoreboard`). Every table creation, insert, and history check is plain `%sql`.
- **Checkpoint timing is not perfectly deterministic on Serverless.** If Step 3 reports no checkpoint found, re-run that cell once, or add one more sale — this is a real, honestly-reported product behavior, not a bug in the notebook.
- **`DEEP CLONE` was deliberately avoided when building the three twin ledgers.** A clone copies all rows into a single version-0 snapshot, which would make "delete Sale #2's own commit" meaningless — that data would already be sitting in version 0 before any per-sale commit existed to delete. Every ledger here is built fresh, one `INSERT` per sale, so every version is a genuine single-sale commit.
- **Experiment D's fresh-session bonus cell must run with nothing else in between.** `%restart_python` clears every variable from the earlier experiments, including the scoreboard results — that's intentional. If you need those values again, re-run from Step 0.
- **One claim in this notebook's own markdown is currently asserted, not tested** — see the note above the fresh-session cell about `DESCRIBE HISTORY`. Verify it directly before treating it as proven, or add the verification cell described in this repo's episode notes.
- Results reported in this README (PASS/FAIL per scoreboard line) reflect what this exact experiment structure produced when run — re-running on a different workspace, runtime version, or checkpoint interval should be treated as its own independent test, not assumed identical.

## Watch the video

Episode 21 — *What Happens When a Delta Log JSON Commit File Is Accidentally Deleted?* — on the Data Dharma YouTube channel.
