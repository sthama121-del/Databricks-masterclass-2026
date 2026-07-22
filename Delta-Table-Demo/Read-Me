# Delta Lake Internals Demo — Data Dharma

A hands-on Databricks notebook series exploring what's actually happening inside `_delta_log` when you run everyday DML — `INSERT`, `UPDATE`, `DELETE`, schema evolution, and `MERGE INTO`. Built as companion material for the **Data Dharma** YouTube channel's Delta Lake video series (Telugu, by Srikanth).

Instead of treating Delta Lake as a black box, these notebooks read the raw JSON transaction log and raw Parquet files directly with plain shell commands and pandas — bypassing Delta's own reader — so you can see exactly what a commit contains: `add`/`remove` actions, deletion vectors, auto-compaction, and more.

## Prerequisites

- A Databricks workspace (built and tested on **Databricks Free Edition**, Unity Catalog enabled, serverless compute)
- No external cloud storage account needed — everything runs inside a Unity Catalog **Volume**, which Free Edition provides out of the box
- Basic familiarity with SQL; no prior Delta Lake or PySpark experience required — every code cell has an explanatory comment above it

### Why a Volume instead of a normal managed table?

Unity Catalog deliberately hides a managed table's physical storage path — `DESCRIBE DETAIL` returns `location: null`, and there's no way to `%sh ls` or `%sh cat` its files directly. Since the entire point of this series is looking at the raw log and data files, every table here is created as a **path-based Delta table** living inside a Volume (`/Volumes/workspace/delta_demo/demo_files/...`) instead of a catalog-registered table. This has zero effect on how Delta itself behaves — it's the exact same table format and transaction log mechanics — it just keeps the files visible.

## Notebook order

Run these in sequence. Each one states its prerequisite at the top.

| Notebook | What it does |
|---|---|
| **Delta_Demo_Day0_Load** | Resets everything — deletes the demo table's files, the Volume, and the schema. Run this any time you want a clean slate. |
| **Delta_Demo_Day1_Load** | Creates the schema + Volume, writes the first 3 rows as a brand-new Delta table, then deep-dives into the raw JSON commit and Parquet file it produced. |
| **Delta_Demo_Day2_Load** | Inserts 2 more rows. Shows that INSERT only ever adds a new file — Day 1's file is left completely untouched. |
| **Delta_Demo_Day3_Load** | Runs `UPDATE`, `DELETE`, another `UPDATE`, and `INSERT`. Explores **Deletion Vectors** (merge-on-read) in detail, watches Databricks' automatic `OPTIMIZE` compaction kick in on its own, and investigates when Delta actually writes its first checkpoint file. |
| **Delta_Demo_Day4_Load** | Deep Clones the table and re-expresses a set of changes as a single atomic `MERGE INTO` statement — one commit instead of several separate ones. |

> Note: the numbering intentionally skips a dedicated "Day" for Time Travel (`VERSION AS OF` / `TIMESTAMP AS OF`), which is covered as its own separate video/notebook, since it deserves its own focused walkthrough once a table has real accumulated history to travel through.

## What you'll see demonstrated

- How `_delta_log` JSON commits are structured (`commitInfo`, `metaData`, `protocol`, `add`, `remove`)
- Why each JSON file is newline-delimited JSON (NDJSON), not one single JSON object
- How Deletion Vectors let `UPDATE`/`DELETE` avoid rewriting entire Parquet files (merge-on-read)
- How Databricks' automatic `OPTIMIZE` compaction fires without being explicitly requested
- The difference between a file being *logically* removed (tombstoned in the log) vs *physically* deleted (only `VACUUM` does that)
- How `DEEP CLONE` creates a fully independent copy, and how `VERSION AS OF` lets you clone from any point in a table's history
- How `MERGE INTO` bundles several logical changes into a single atomic transaction

## Notes

- Some exact file names, byte sizes, and version numbers in the markdown commentary reflect one specific real run — your own numbers may differ slightly depending on write parallelism and whether auto-compaction triggers. Where this matters, the notebooks tell you to check `DESCRIBE HISTORY` yourself rather than trust a hardcoded number.
- These notebooks intentionally use Databricks' newer Deletion Vector behavior (`delta.enableDeletionVectors = true`, on by default). If you're following along on an older Delta version without Deletion Vectors enabled, `UPDATE`/`DELETE` will instead show the older copy-on-write behavior (full file rewrite + tombstone) rather than the deletion-vector pattern described here.

## License

Feel free to reuse, adapt, and build on these notebooks for your own learning or teaching content.
