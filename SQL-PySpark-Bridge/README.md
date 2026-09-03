# SQL ↔ PySpark Bridge

Part of the **Data Dharma by Srikanth** Databricks Masterclass series.

A mini-series for SQL developers, ETL/Informatica developers, QA professionals, and Databricks beginners who already know SQL and want to translate that knowledge into PySpark — instead of learning PySpark from zero.

**Core message throughout:**
Same data. Same business requirement. Different syntax. Same result.

## How this series works

Every notebook follows the same pattern for every concept:

```
BUSINESS REQUIREMENT
        ↓
       SQL
        ↓
     RESULT
        ↓
   PYSPARK
        ↓
     RESULT
        ↓
SQL ↔ PYSPARK MAPPING
```

SQL and PySpark are never taught as two separate subjects — every example solves the *same* requirement both ways, then proves the results match.

## Notebooks

| # | Notebook | Covers |
|---|---|---|
| 1 | `01_SQL_vs_PySpark_Foundations.ipynb` | SELECT, aliasing, WHERE/filter, AND/OR (`&` / `\|`), DISTINCT, ORDER BY, LIMIT |
| 2 | `02_SQL_vs_PySpark_Transformations_Part2.ipynb` | CASE WHEN, CAST, IN, LIKE, NULL handling (`IS NULL`/`IS NOT NULL`/`COALESCE`), string functions, date functions |
| 3 | `03_SQL_vs_PySpark_Aggregations_Part3.ipynb` | GROUP BY, COUNT, SUM, AVG, MIN, MAX, multiple aggregations, multi-column GROUP BY, WHERE vs HAVING |
| 4 | `04_SQL_vs_PySpark_Joins_Part4.ipynb` | INNER, LEFT, RIGHT, FULL OUTER JOIN, join conditions vs. join types, selecting columns after a join, different key names, filtering after a join, ambiguous column names |

Each notebook builds on the last — run them in order for the full learning progression.

## The dataset

All notebooks share one small, realistic **retail `orders` dataset** (18 rows), created entirely in-memory inside each notebook — no external files, no cloud storage, no Unity Catalog permissions required.

- `order_amount` is calculated once, consistently, in every notebook: `(quantity * unit_price) - discount_amount`
- Part 2 extends the dataset with `customer_name`, `ship_date`, and `promo_code` — each added for a real teaching reason (string cleanup, genuine NULLs for unshipped/cancelled orders, and a COALESCE example), explained in-notebook
- Part 3 reuses the Part 2 dataset unchanged
- Part 4 adds a second table, **`customers`** (14 rows), to teach JOINs. It's deliberately built so one customer has no orders yet and one order references a customer with no record — so INNER, LEFT, RIGHT, and FULL OUTER JOIN each produce a visibly different, real result

The same DataFrame (`orders_df`) is exposed as a SQL temp view (`orders`) in every notebook, so SQL and PySpark examples always read the exact same underlying data:

```
orders_df
    ↓
createOrReplaceTempView("orders")
    ↓
orders
```

From Part 4 onward, `customers_df` / `customers` follows the same pattern alongside it.

## How to run

1. Import a notebook into a Databricks workspace (Workspace → Import).
2. Attach it to any cluster or serverless compute with a standard PySpark runtime.
3. Run all cells top to bottom.

No setup, credentials, or external data required.

## Coming next

**Part 5 — SQL ↔ PySpark Window Functions**

`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `PARTITION BY`, `ORDER BY` inside window functions.

## Links

- YouTube playlist: https://www.youtube.com/playlist?list=PLKGYxsBfjIpw
- Channel: [Data Dharma by Srikanth](https://youtube.com/@DataDharmaBySrikanth)
