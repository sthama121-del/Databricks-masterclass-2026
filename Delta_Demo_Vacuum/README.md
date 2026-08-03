# Episode 14 — VACUUM

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 14: "The Mistake Is Still in History Forever... But Is the DATA Still Recoverable Forever?"

## The Question

We've spent three episodes proving Delta keeps old, tombstoned files around after every UPDATE, DELETE, and CTAS. How long does that actually last — and what happens to Time Travel once those files are gone for good?

## What This Notebook Proves

Using real transaction log and filesystem evidence (not just claims), this notebook verifies:
- Ordinary UPDATE and DELETE operations genuinely leave orphaned files sitting on disk — confirmed by comparing active files (what a query reads) against physical files (what's actually on disk), not assumed
- `VACUUM ... DRY RUN` only lists deletion candidates — it changes nothing, and by default nothing recent qualifies anyway
- VACUUM's default 7-day retention window (`delta.deletedFileRetentionDuration`) exists specifically to protect concurrent readers, not as an arbitrary number
- After a real `VACUUM ... RETAIN 0 HOURS` (demo-only override), physical file count genuinely drops to match active file count — the orphaned garbage is truly gone, not just hidden
- Whether Time Travel to an early version still works AFTER vacuuming is tested directly against the exact same command that worked before — the real result is reported plainly, whichever way it goes, rather than assumed in advance

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball.

## The Journey

| Step | What happens |
|---|---|
| Baseline | 5-row `employees_ep14` table created |
| A few ordinary updates | 2 `UPDATE`s + 1 `DELETE` — each tombstones a file without physically removing it |
| Confirm real garbage | Active files vs. physical files on disk — proves orphaned data genuinely exists |
| `VACUUM ... DRY RUN` | Lists what *would* be deleted — likely empty, since everything is only minutes old |
| Override retention (demo only) | `delta.deletedFileRetentionDuration = 'interval 0 hours'`, explicitly flagged as never-do-this-in-production |
| Real `VACUUM ... RETAIN 0 HOURS` | Orphaned files are physically deleted — verified by re-checking active vs. physical counts |
| Time Travel, again | The exact same version-0 read that worked earlier is retried post-VACUUM — real pass/fail result, not predicted |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own table (`employees_ep14`) inside a Unity Catalog Volume
- Helpful context, not required: the "active files vs. physical files on disk" check used here was first introduced as a closing teaser in Episode 11 — this episode is where it becomes the main event

## Notes

- **`RETAIN 0 HOURS` is a demo-only technique.** The notebook explicitly overrides both the retention window and Delta's built-in safety check that normally blocks unsafely-low retention values. Never run this against a live production table without knowing exactly who else might be reading it — a concurrent query relying on an old snapshot can be broken by an aggressive VACUUM.
- Whether the specific version-0 Time Travel read survives the VACUUM depends on whether the file(s) it needed happened to be among the ones removed — the notebook reports the real outcome from its own run rather than a predicted one. If you rerun it and get a different result than what's shown, trust your own output.
- Serverless compute doesn't expose all cluster-level Spark configs (see the cell handling `spark.databricks.clusterUsageTags.clusterAllTags`) — the notebook works around this by passing `RETAIN 0 HOURS` directly on the `VACUUM` command instead of a session-level override.

## Watch the video

[VACUUM — The Mistake Is Still in History Forever... But Is the Data? | Databricks Masterclass Episode 14](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
