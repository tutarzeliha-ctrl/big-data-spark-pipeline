import os
import pandas as pd

BRONZE_PATH = "output_bronze"
SILVER_PATH = "output_silver"
GOLD_PATH = "output_gold"
QUARANTINE_PATH = "output_quarantine"

# Create output directories for layers
os.makedirs(SILVER_PATH, exist_ok=True)
os.makedirs(GOLD_PATH, exist_ok=True)
os.makedirs(QUARANTINE_PATH, exist_ok=True)

print("🚀 Starting Enterprise Medallion Pipeline with Data Quality & Governance...")

# ---------------------------------------------------------
# 1. BRONZE TO SILVER (Data Quality Validation & Quarantine)
# ---------------------------------------------------------
print("🔄 Processing Bronze -> Silver layer with Data Quality Rules...")

bronze_files = [os.path.join(BRONZE_PATH, f) for f in os.listdir(BRONZE_PATH) if f.endswith(".parquet")]
if not bronze_files:
    raise FileNotFoundError("No Bronze data found! Please run generate_big_data.py first.")

df_bronze_list = [pd.read_parquet(f) for f in bronze_files]
df_bronze = pd.concat(df_bronze_list, ignore_index=True)

total_records = len(df_bronze)

# Define Data Quality Rules
is_valid_nulls = df_bronze["transaction_id"].notnull() & \
                 df_bronze["category"].notnull() & \
                 df_bronze["product_price"].notnull() & \
                 df_bronze["quantity"].notnull()

is_valid_values = (df_bronze["product_price"] > 0) & (df_bronze["quantity"] > 0)

# Separate valid data (Silver) and invalid data (Quarantine)
valid_mask = is_valid_nulls & is_valid_values

df_silver = df_bronze[valid_mask].copy()
df_quarantine = df_bronze[~valid_mask].copy()

# Save Silver layer with partitionBy optimization (partitioning by 'category' for high-performance querying)
silver_file_path = SILVER_PATH  # Pandas to_parquet partition_cols expects directory path
df_silver.to_parquet(silver_file_path, index=False, partition_cols=["category"])

# Save Quarantine layer for governance/auditing
quarantine_file_path = os.path.join(QUARANTINE_PATH, "quarantine_records.parquet")
df_quarantine.to_parquet(quarantine_file_path, index=False)

print(f"📊 Data Quality Report:")
print(f"   - Total Input Records: {total_records}")
print(f"   - Passed to Silver Layer: {len(df_silver)} ({len(df_silver)/total_records*100:.2f}%)")
print(f"   - Quarantined (Failed Rules): {len(df_quarantine)} ({len(df_quarantine)/total_records*100:.2f}%)")
print(f"✅ Silver layer successfully written with partitioning to: {silver_file_path}")

# ---------------------------------------------------------
# 2. SILVER TO GOLD (Business Aggregations Layer)
# ---------------------------------------------------------
print("🔄 Processing Silver -> Gold layer (Business Aggregations)...")

df_gold = df_silver.groupby(["category", "country"]).agg(
    total_revenue=("total_amount", lambda x: round(x.sum(), 2)),
    total_transactions=("transaction_id", "count"),
    avg_product_price=("product_price", lambda x: round(x.mean(), 2))
).reset_index()

gold_file_path = os.path.join(GOLD_PATH, "analytics_summary.parquet")
df_gold.to_parquet(gold_file_path, index=False)
print(f"✅ Gold layer successfully written to: {gold_file_path}")

print("🎉 Enterprise Medallion Pipeline with Governance completed successfully!")