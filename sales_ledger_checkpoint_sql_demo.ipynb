# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Sales Ledger Checkpoint Demo (SQL Version)
# MAGIC %md
# MAGIC # Sales ledger checkpoint demo (SQL-centric version)
# MAGIC
# MAGIC Four short experiments, same visual language throughout:
# MAGIC **Receipt = JSON commit. Summary = Checkpoint. Today's Table = Latest snapshot. Old Version = Time travel.**
# MAGIC
# MAGIC - **A — Healthy ledger**: how Delta normally works.
# MAGIC - **B — Delete an old receipt** (before a later summary): does today's total still work? Does that old day's exact report still work?
# MAGIC - **C — Delete a receipt after the summary, but not the newest one**: can Delta still cross that gap?
# MAGIC - **D — Delete the newest receipt**: what happens on the very next sale?
# MAGIC
# MAGIC **This notebook uses SQL commands wherever possible.** Python is only used for:
# MAGIC - File system operations (deleting Delta log files)
# MAGIC - Finding checkpoint versions (SQL can't list files)
# MAGIC - Helper functions for testing
# MAGIC
# MAGIC Every experiment ends in the same three-line scoreboard:
# MAGIC `LATEST READ` / `TIME TRAVEL` / `NEW WRITE` — pass or fail, one line each.

# COMMAND ----------

# DBTITLE 1,Step 0 - Reset
# MAGIC %md
# MAGIC ### Step 0 — Reset
# MAGIC Clear all demo paths for a fresh start.

# COMMAND ----------

# DBTITLE 1,Clear demo paths
BASE = "/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo"
BEFORE_PATH = "/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_before_cp"
AFTER_PATH  = "/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_after_cp"
LATEST_PATH = "/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_latest_delete"

for p in [BASE, BEFORE_PATH, AFTER_PATH, LATEST_PATH]:
    try:
        dbutils.fs.rm(p, recurse=True)
        print(f"[RESET] Cleared: {p}")
    except:
        pass

# COMMAND ----------

# DBTITLE 1,Step 1 - Create table
# MAGIC %md
# MAGIC ### Step 1 — Create the sales table (SQL)
# MAGIC `delta.checkpointInterval` is set to 3, so a checkpoint gets written right after the 3rd sale.

# COMMAND ----------

# DBTITLE 1,CREATE TABLE with checkpoint interval
# MAGIC %sql
# MAGIC CREATE TABLE delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` (
# MAGIC   sale_id INT,
# MAGIC   item STRING,
# MAGIC   amount DOUBLE
# MAGIC )
# MAGIC USING DELTA
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.checkpointInterval' = '3',
# MAGIC   'delta.autoOptimize.autoCompact' = 'false',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'false'
# MAGIC );
# MAGIC
# MAGIC -- Verify empty table
# MAGIC SELECT '[CREATE] Table created (Version 0, empty)' as status;
# MAGIC SELECT * FROM delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Step 2 - Insert sales
# MAGIC %md
# MAGIC ### Step 2 — Ring up 6 sales, one commit at a time (SQL)
# MAGIC Each INSERT is its own version. We'll check the running total after each one.

# COMMAND ----------

# DBTITLE 1,Insert Sale 1
# MAGIC %sql
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (1, 'Coffee', 5.0);
# MAGIC SELECT '[Sale 1] Coffee, $5.0' as sale, SUM(amount) as running_total FROM delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Insert Sale 2
# MAGIC %sql
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (2, 'Sandwich', 8.0);
# MAGIC SELECT '[Sale 2] Sandwich, $8.0' as sale, SUM(amount) as running_total FROM delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Insert Sale 3
# MAGIC %sql
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (3, 'Coffee', 5.0);
# MAGIC SELECT '[Sale 3] Coffee, $5.0 → CHECKPOINT CREATED HERE' as sale, SUM(amount) as running_total FROM delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Insert Sales 4-6
# MAGIC %sql
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (4, 'Cake', 6.0);
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (5, 'Tea', 4.0);
# MAGIC INSERT INTO delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo` VALUES (6, 'Coffee', 5.0);
# MAGIC SELECT '[Sales 4-6] All sales complete' as status, SUM(amount) as final_total FROM delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Step 3 - Check history
# MAGIC %md
# MAGIC ### Step 3 — Check Delta history (SQL) and find checkpoint (Python helper)

# COMMAND ----------

# DBTITLE 1,Show Delta history
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta.`/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_demo`;

# COMMAND ----------

# DBTITLE 1,Find checkpoint version
import re

def find_checkpoint_version(path):
    files = dbutils.fs.ls(f"{path}/_delta_log/")
    versions = []
    for f in files:
        m = re.match(r"^(\d+)\.checkpoint(\.\d+\.\d+)?\.parquet$", f.name)
        if m:
            versions.append(int(m.group(1)))
    return max(versions) if versions else None

checkpoint_v = find_checkpoint_version(BASE)
all_json = sorted([f.name for f in dbutils.fs.ls(f"{BASE}/_delta_log/") if f.name.endswith(".json")])
print("JSON commit files:", all_json)
print("Checkpoint found at version:", checkpoint_v)
if checkpoint_v is None:
    print("No checkpoint yet — re-run this cell or add one more sale.")

# COMMAND ----------

# DBTITLE 1,Step 4 - Build twin ledgers
# MAGIC %md
# MAGIC ### Step 4 — Build three twin ledgers for Experiments B, C, D
# MAGIC Built fresh with the same structure. Python loops the SQL commands.

# COMMAND ----------

# DBTITLE 1,Build ledgers using SQL
def build_ledger_sql(path, sale_list):
    spark.sql(f"""
        CREATE TABLE delta.`{path}` (
          sale_id INT, item STRING, amount DOUBLE
        )
        USING DELTA
        TBLPROPERTIES (
          'delta.checkpointInterval' = '3',
          'delta.autoOptimize.autoCompact' = 'false',
          'delta.autoOptimize.optimizeWrite' = 'false'
        )
    """)
    for sid, item, amt in sale_list:
        spark.sql(f"INSERT INTO delta.`{path}` VALUES ({sid}, '{item}', {amt})")
    cp = find_checkpoint_version(path)
    v = spark.sql(f"DESCRIBE HISTORY delta.`{path}`").agg({"version": "max"}).collect()[0][0]
    print(f"[BUILD] {path.split('/')[-1]:35s} -> v{v}, checkpoint at {cp}")

sales = [(1, "Coffee", 5.0), (2, "Sandwich", 8.0), (3, "Coffee", 5.0),
         (4, "Cake", 6.0), (5, "Tea", 4.0), (6, "Coffee", 5.0)]

build_ledger_sql(BEFORE_PATH, sales)
build_ledger_sql(AFTER_PATH, sales + [(7, "Muffin", 4.5), (8, "Bagel", 4.0)])
build_ledger_sql(LATEST_PATH, sales)

# COMMAND ----------

# DBTITLE 1,Shared testing framework
# MAGIC %md
# MAGIC ### Shared testing framework (Python helpers)
# MAGIC These functions test read/write operations and format results consistently.

# COMMAND ----------

# DBTITLE 1,Test helpers
def short_reason(e):
    text = str(e)
    for stop in ["\n\nJVM stacktrace", "\nJVM stacktrace", "\n\tat "]:
        if stop in text:
            text = text.split(stop)[0]
            break
    text = text.strip()
    return text if len(text) <= 160 else text[:157] + "..."

def try_read_sql(path, version_as_of=None):
    try:
        df = spark.read.format("delta")
        if version_as_of is not None:
            df = df.option("versionAsOf", version_as_of)
        df.load(path).count()
        return True, None
    except Exception as e:
        return False, short_reason(e)

def try_write_sql(path, sid, item, amt):
    try:
        spark.sql(f"INSERT INTO delta.`{path}` VALUES ({sid}, '{item}', {amt})")
        v = spark.sql(f"DESCRIBE HISTORY delta.`{path}`").agg({"version": "max"}).collect()[0][0]
        return True, v
    except Exception as e:
        return False, short_reason(e)

def scoreboard(title, rows):
    print(f"\n{title}")
    print("-" * len(title))
    for label, passed, detail in rows:
        mark = "PASS" if passed else "FAIL"
        line = f"  {label:<28s} {mark}"
        if detail:
            line += f"   ({detail})"
        print(line)

# COMMAND ----------

# DBTITLE 1,Experiment B
# MAGIC %md
# MAGIC ### Experiment B — Delete an OLD receipt (before the summary)
# MAGIC Delete Sale #2's commit (before checkpoint at version 3).

# COMMAND ----------

# DBTITLE 1,Delete and test - Experiment B
target_before = 2
dbutils.fs.rm(f"{BEFORE_PATH}/_delta_log/{target_before:020d}.json")

latest_ok, latest_detail = try_read_sql(BEFORE_PATH)
vao_ok, vao_detail = try_read_sql(BEFORE_PATH, version_as_of=target_before)
write_ok, write_detail = try_write_sql(BEFORE_PATH, 99, "Test Item", 1.0)

scoreboard("EXPERIMENT B -- Delete Sale #2 (before the summary)", [
    ("Can I read LATEST?", latest_ok, latest_detail),
    (f"Can I TIME TRAVEL to v{target_before}?", vao_ok, vao_detail),
    ("Can I make a NEW WRITE?", write_ok, f"landed at v{write_detail}" if write_ok else write_detail),
])

before_latest_read, before_vao, before_new_write = latest_ok, vao_ok, write_ok

# COMMAND ----------

# DBTITLE 1,Experiment C
# MAGIC %md
# MAGIC ### Experiment C — Delete a receipt AFTER the summary (not the newest)
# MAGIC Delete Sale #7's commit. Sale #8 still exists, proving a gap in the chain.

# COMMAND ----------

# DBTITLE 1,Delete and test - Experiment C
target_after = 7
dbutils.fs.rm(f"{AFTER_PATH}/_delta_log/{target_after:020d}.json")

latest_ok, latest_detail = try_read_sql(AFTER_PATH)
vao7_ok, vao7_detail = try_read_sql(AFTER_PATH, version_as_of=7)
vao8_ok, vao8_detail = try_read_sql(AFTER_PATH, version_as_of=8)
write_ok, write_detail = try_write_sql(AFTER_PATH, 9, "Croissant", 5.5)

scoreboard("EXPERIMENT C -- Delete Sale #7, Sale #8 survives", [
    ("Can I read LATEST?", latest_ok, latest_detail),
    ("Can I TIME TRAVEL to v7?", vao7_ok, vao7_detail),
    ("Can I TIME TRAVEL to v8?", vao8_ok, vao8_detail),
    ("Can I make a NEW WRITE?", write_ok, f"landed at v{write_detail}" if write_ok else write_detail),
])

after_latest_read, after_vao_7, after_vao_8, after_new_write = latest_ok, vao7_ok, vao8_ok, write_ok

# COMMAND ----------

# DBTITLE 1,Experiment D
# MAGIC %md
# MAGIC ### Experiment D — Delete the NEWEST receipt
# MAGIC Delete Sale #6 (the newest) and see if the next write reuses version 6.

# COMMAND ----------

# DBTITLE 1,Delete and test - Experiment D
latest_before_delete = spark.sql(f"DESCRIBE HISTORY delta.`{LATEST_PATH}`").agg({"version": "max"}).collect()[0][0]
target_latest = latest_before_delete
dbutils.fs.rm(f"{LATEST_PATH}/_delta_log/{target_latest:020d}.json")

write_ok, new_version = try_write_sql(LATEST_PATH, 7, "Muffin", 4.5)

print(f"\nEXPERIMENT D -- Delete Sale #{target_latest} (the newest), then ring up a new sale")
print("-" * 60)
print(f"  Version deleted        : {target_latest}")
if write_ok:
    print(f"  Next sale landed at    : version {new_version}")
    if new_version == target_latest:
        print(f"  -> Delta REUSED version {target_latest}. It never saw Sale #{target_latest} commit as existing.")
    else:
        print(f"  -> Delta skipped past version {target_latest} to {new_version}.")
else:
    print(f"  New write FAILED: {new_version}")

latest_delete_reused = write_ok and (new_version == target_latest)

# COMMAND ----------

# DBTITLE 1,Summary
# MAGIC %md
# MAGIC ### Step 5 — Validate all at once
# MAGIC Auto-generated summary of all experiments.

# COMMAND ----------

# DBTITLE 1,Summary scoreboard
print("EXPERIMENT B -- delete BEFORE the summary (Sale #2)")
print(f"  Latest read : {'PASS' if before_latest_read else 'FAIL'}   Time travel : {'PASS' if before_vao else 'FAIL'}   New write : {'PASS' if before_new_write else 'FAIL'}")
print()
print("EXPERIMENT C -- delete AFTER the summary, not newest (Sale #7, #8 survives)")
print(f"  Latest read : {'PASS' if after_latest_read else 'FAIL'}   Time travel v7 : {'PASS' if after_vao_7 else 'FAIL'}   Time travel v8 : {'PASS' if after_vao_8 else 'FAIL'}   New write : {'PASS' if after_new_write else 'FAIL'}")
print()
print("EXPERIMENT D -- delete the NEWEST receipt")
print(f"  Next write reused the deleted version number : {'YES' if latest_delete_reused else 'NO'}")
print()
print("=" * 60)
print("CHECKPOINT != BACKUP")
print("A checkpoint helps Delta reconstruct table state efficiently.")
print("It does NOT guarantee every old version survives manual")
print("deletion of transaction logs.")
print("=" * 60)

# COMMAND ----------

# DBTITLE 1,Bonus verification
# MAGIC %md
# MAGIC ### Bonus — Fresh-session verification for Experiment D
# MAGIC Runs after the summary. `%restart_python` wipes the session to re-confirm Experiment D with zero cached reads.

# COMMAND ----------

# DBTITLE 1,Restart Python (prepare for fresh test)
# MAGIC %restart_python

# COMMAND ----------

# DBTITLE 1,Describe table structure
# MAGIC %md
# MAGIC ### Fresh session verification
# MAGIC
# MAGIC **What happened in Experiment D:**
# MAGIC * We deleted version 6 (the newest receipt).
# MAGIC * Python was restarted to clear all cached metadata.
# MAGIC
# MAGIC **What we're about to test:**
# MAGIC * Can we insert a new sale into this table?
# MAGIC * Will Delta reuse version 6, or skip to version 7?
# MAGIC
# MAGIC **Note:** We CANNOT read or describe this table right now — even `DESCRIBE HISTORY` fails because the latest commit file (version 6) is missing. This is exactly what Experiment D showed: deleting the newest receipt breaks **everything** until a new write repairs the chain.

# COMMAND ----------

# DBTITLE 1,Fresh session test
LATEST_PATH = "/Volumes/workspace/delta_demo/demo_files/sql_sales_ledger_latest_delete"

try:
    spark.sql(f"INSERT INTO delta.`{LATEST_PATH}` VALUES (7, 'Muffin', 4.5)")
    v = spark.sql(f"DESCRIBE HISTORY delta.`{LATEST_PATH}`").agg({"version": "max"}).collect()[0][0]
    print(f"FRESH SESSION -- New write: SUCCESS, landed at version {v}")
except Exception as e:
    print(f"FRESH SESSION -- New write: FAILED")
    print(f"Reason: {str(e).split(chr(10))[0]}")