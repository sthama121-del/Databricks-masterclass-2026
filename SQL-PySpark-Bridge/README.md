# Ep25 — SQL ↔ PySpark Bridge — Part 1: Foundations

Part of the **Data Dharma by Srikanth** Databricks Masterclass series.

## What this covers
SELECT, column aliasing, WHERE/filter, AND/OR (`&` / `|`), DISTINCT, ORDER BY,
LIMIT, and one combined real-world requirement — each shown side-by-side in
SQL and PySpark, proven to return the same result.

## Dataset
A self-contained, in-memory retail `orders` dataset (18 rows) — created entirely
inside the notebook. No external files, no cloud storage, no Unity Catalog
permissions required.

## How to run
1. Import `01_SQL_vs_PySpark_Foundations.ipynb` into a Databricks workspace.
2. Attach it to any cluster or serverless compute running a standard PySpark runtime.
3. Run all cells top to bottom — Step 0 resets the temp view so the notebook
   is safe to re-run any number of times.

## Series
- Part 1 — Foundations *(this notebook)*
- Part 2 — Transformations & Data Cleaning *(coming next)*
- Part 3 — Aggregations & Joins
- Part 4 — Advanced Data Engineering / Delta

## Links
- YouTube playlist: https://www.youtube.com/playlist?list=PLKGYxsBfjIpw
- Channel: [Data Dharma by Srikanth](https://youtube.com/@DataDharmaBySrikanth)
