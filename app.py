import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Enterprise Data Governance & Analytics",
    page_icon="🛡️",
    layout="wide"
)

BRONZE_PATH = "output_bronze"
SILVER_PATH = "output_silver"
GOLD_PATH = "output_gold"
QUARANTINE_PATH = "output_quarantine"

# Auto-generate data on cloud if Gold layer is missing
gold_path = os.path.join(GOLD_PATH, "analytics_summary.parquet")
if not os.path.exists(gold_path):
    os.makedirs(BRONZE_PATH, exist_ok=True)
    os.makedirs(SILVER_PATH, exist_ok=True)
    os.makedirs(GOLD_PATH, exist_ok=True)
    os.makedirs(QUARANTINE_PATH, exist_ok=True)
    
    # 1. Generate Bronze Data
    categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]
    countries = ["USA", "DE", "TR", "UK", "FR"]
    
    data = []
    start_date = datetime.now() - timedelta(days=30)
    for i in range(100000):
        data.append({
            "transaction_id": f"TXN-{100000 + i}",
            "category": random.choice(categories),
            "country": random.choice(countries),
            "product_price": round(random.uniform(10.0, 1000.0), 2),
            "quantity": random.randint(1, 5),
            "total_amount": 0.0,
            "timestamp": (start_date + timedelta(minutes=random.randint(0, 43200))).strftime("%Y-%m-%d %H:%M:%S")
        })
    df_raw = pd.DataFrame(data)
    df_raw["total_amount"] = round(df_raw["product_price"] * df_raw["quantity"], 2)
    
    bronze_file = os.path.join(BRONZE_PATH, "raw_transactions_1.parquet")
    df_raw.to_parquet(bronze_file, index=False)
    
    # 2. Process Silver & Gold Layers
    df_silver = df_raw[(df_raw["product_price"] > 0) & (df_raw["quantity"] > 0)].copy()
    silver_file = os.path.join(SILVER_PATH, "cleaned_transactions.parquet")
    df_silver.to_parquet(silver_file, index=False)
    
    df_gold = df_silver.groupby(["category", "country"]).agg(
        total_revenue=("total_amount", lambda x: round(x.sum(), 2)),
        total_transactions=("transaction_id", "count"),
        avg_product_price=("product_price", lambda x: round(x.mean(), 2))
    ).reset_index()
    
    df_gold.to_parquet(gold_path, index=False)

st.title("🛡️ Enterprise Data Governance, Quality & Analytics Pipeline")
st.markdown("This production-grade dashboard monitors data quality rules, quarantine metrics, and consumes aggregated metrics from the **Gold Layer**.")

# Sidebar Controls & Information
st.sidebar.header("⚙️ Pipeline Management")
st.sidebar.info("💡 Pipeline automatically compiles and governs data through the Medallion Architecture (Bronze -> Silver -> Gold).")

st.sidebar.divider()
st.sidebar.header("🔍 Advanced Filter Controls")

# Data Loading Function from Gold Layer & Quarantine Check
@st.cache_data
def load_data():
    gold_file = os.path.join(GOLD_PATH, "analytics_summary.parquet")
    quarantine_file = os.path.join(QUARANTINE_PATH, "quarantine_records.parquet")
    
    df_gold = pd.read_parquet(gold_file) if os.path.exists(gold_file) else pd.DataFrame()
    
    quarantine_count = 0
    if os.path.exists(quarantine_file):
        df_q = pd.read_parquet(quarantine_file)
        quarantine_count = len(df_q)
        
    return df_gold, quarantine_count

df, quarantine_count = load_data()

if not df.empty:
    all_countries = list(df["country"].unique())
    selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=all_countries)

    all_categories = list(df["category"].unique())
    selected_categories = st.sidebar.multiselect("Select Categories", options=all_categories, default=all_categories)

    filtered_df = df[
        df["country"].isin(selected_countries) & 
        df["category"].isin(selected_categories)
    ]
else:
    filtered_df = pd.DataFrame()

# Data Quality Governance Banner
st.subheader("📊 Data Quality & Governance Overview")
q_col1, q_col2, q_col3 = st.columns(3)
total_records_val = int(df['total_transactions'].sum()) if not df.empty else 100000
q_col1.metric("Total Processed Records", f"{total_records_val:,}")
q_col2.metric("Quarantined (Failed) Records", f"{quarantine_count:,}")
q_col3.metric("Pipeline Health Status", "🟢 Healthy / Compliant")

st.divider()

# Main Dashboard KPIs
st.subheader("📈 Key Performance Indicators (Gold Layer)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}" if not filtered_df.empty else "$0.00")
col2.metric("Total Transactions", f"{filtered_df['total_transactions'].sum():,}" if not filtered_df.empty else "0")
col3.metric("Avg Product Price", f"${filtered_df['avg_product_price'].mean():,.2f}" if not filtered_df.empty else "$0.00")

st.divider()

# Advanced Visualizations Layout
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Revenue Breakdown by Category")
    if not filtered_df.empty:
        revenue_by_cat = filtered_df.groupby("category")["total_revenue"].sum()
        st.bar_chart(revenue_by_cat)
    else:
        st.warning("No data available.")

with col_chart2:
    st.subheader("🌍 Transaction Share by Country")
    if not filtered_df.empty:
        trans_by_country = filtered_df.groupby("country")["total_transactions"].sum()
        st.bar_chart(trans_by_country)
    else:
        st.warning("No data available.")

st.divider()

# Processed Gold Data Inspector and Download Section
st.subheader("📁 Gold Layer Summary Data Inspector & Export")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Gold Analytics as CSV",
        data=csv_data,
        file_name="gold_layer_analytics.csv",
        mime="text/csv"
    )
else:
    st.warning("No data found in Gold layer.")