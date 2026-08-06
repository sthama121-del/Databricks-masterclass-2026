# Episode 19 — OPTIMIZE

Companion notebook for the **Data Dharma** YouTube channel's Databricks Masterclass — Episode 19: "Ten Small Files, One Slow Query — Can We Fix This Without Deleting Anything?"

## The Question

A table built from many small writes ends up with many small files. Does that matter — and if so, how do you fix it without deleting any data?

## What This Notebook Proves

Using real file counts, commit metrics, and raw log evidence (not just claims), this notebook verifies:
- 10 separate small writes genuinely produce 10 separate physical files — confirmed by deliberately disabling auto-compaction at table creation, so nothing gets silently cleaned up before it can be shown
- `OPTIMIZE` collapses the active file count down (to exactly 1, at this demo's tiny scale) — because the real compaction rule is "aim for ~256MB per file," not "always produce exactly one file"
- **The original 10 small files are still physically on disk after OPTIMIZE** — active file count (`inputFiles()`) is strictly less than physical file count on disk, proving OPTIMIZE only changes what's *active*, never physically deletes anything. That's VACUUM's job (Episode 14), not OPTIMIZE's
- Every file in this series has carried an `OPTIMIZE_TARGET_SIZE` tag (268435456 bytes = 256MB) since the very first commit back in Episode 10 — OPTIMIZE was always the intended eventual step for every file, whether or not it's manually run

Every claim above is checked programmatically in the notebook itself — look for the cells marked **VERIFY**, which print a pass/fail result rather than just output to eyeball. A prediction cell (Step 4) also asks viewers to guess the post-OPTIMIZE file count before revealing the real number.

## The Journey

| Step | What happens |
|---|---|
| 1 | 10 separate small writes, auto-compaction explicitly disabled from the first write |
| 2 | Confirm the mess is real — 10 physical files, real sizes on disk |
| 3 | Why it matters — per-file overhead, independent of how much data is inside each file |
| 4 | Run `OPTIMIZE` — verify the active file count actually dropped |
| 5 | Confirm the old files are still on disk, just inactive — same active-vs-physical distinction used throughout the series |
| 6 | Read the real `OPTIMIZE` commit — `operationMetrics`, and the `OPTIMIZE_TARGET_SIZE` tag in the raw JSON |
| 7 | Enterprise framing — OPTIMIZE vs. VACUUM, and an honest note about what was deliberately controlled for the demo |

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No prior episode needs to be run first — this notebook is fully self-contained and creates its own table (`employees_ep19`) inside a Unity Catalog Volume
- Helpful context, not required: the active-files-vs-physical-files-on-disk check reused here was first introduced in Episode 11 and became the centerpiece of Episode 14 (VACUUM) — this episode reuses the exact same evidence method from the opposite direction

## Notes

- **Auto-compaction is deliberately disabled here, and the notebook says so plainly in Step 7.** Real Databricks tables often auto-compact without anyone running `OPTIMIZE` by hand — this demo's clean "10 messy files" starting point is a controlled setup, not the typical default behavior. Worth keeping that honesty in the video rather than implying small-file buildup always requires manual intervention.
- Step 2 includes a real fallback check: if the file count comes back as anything other than exactly 10, the notebook flags that auto-compaction may have fired anyway and points to checking `DESCRIBE HISTORY` for unexpected OPTIMIZE rows — confirm your own run's count before trusting the "10 small files" framing on camera.
- This episode's closing line points to **ZORDER and Liquid Clustering** as the next episode — matches Episode 20's already-built content.

## Watch the video

[OPTIMIZE — Ten Small Files, One Slow Query | Databricks Masterclass Episode 19](PASTE_REAL_VIDEO_URL_HERE)

Full playlist: [Databricks Masterclass 2026 (Telugu)](https://www.youtube.com/playlist?list=PLKGYxsBfjIpw)

## Connect

LinkedIn: [srisrisrikanth](https://www.linkedin.com/in/srisrisrikanth/)

---

**Data Dharma by Srikanth**
