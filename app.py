import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Big Data Spark Analytics",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Big Data Spark Pipeline & Advanced Analytics Dashboard")
st.markdown("This enterprise-grade dashboard ingests processed PySpark analytics, providing deep multi-dimensional data exploration and export capabilities.")

# Data Loading Function with Caching
@st.cache_data
def load_data():
    output_path = "output_processed_analytics"
    if os.path.exists(output_path):
        # Read parquet chunks using pandas
        df_list = []
        for root, dirs, files in os.walk(output_path):
            for file in files:
                if file.endswith(".parquet"):
                    df_list.append(pd.read_parquet(os.path.join(root, file)))
        if df_list:
            return pd.concat(df_list, ignore_index=True)
    
    # Return dummy fallback data if Spark pipeline hasn't been executed yet
    return pd.DataFrame({
        "category": ["Electronics", "Clothing", "Home", "Electronics"],
        "country": ["USA", "DE", "TR", "UK"],
        "total_revenue": [150000, 85000, 62000, 110000],
        "total_transactions": [1200, 800, 500, 950],
        "avg_product_price": [125.0, 106.2, 124.0, 115.8]
    })

df = load_data()

# Sidebar Multi-Select Filters
st.sidebar.header("🔍 Advanced Filter Controls")

# Country multi-select filter
all_countries = list(df["country"].unique())
selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=all_countries)

# Category multi-select filter
all_categories = list(df["category"].unique())
selected_categories = st.sidebar.multiselect("Select Categories", options=all_categories, default=all_categories)

# Apply filters to dataframe
filtered_df = df[
    df["country"].isin(selected_countries) & 
    df["category"].isin(selected_categories)
]

# Main Dashboard Metrics
st.subheader("📈 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
col2.metric("Total Transactions", f"{filtered_df['total_transactions'].sum():,}")
col3.metric("Avg Product Price", f"${filtered_df['avg_product_price'].mean():,.2f}")

st.divider()

# Advanced Visualizations Layout
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Revenue Breakdown by Category")
    if not filtered_df.empty:
        revenue_by_cat = filtered_df.groupby("category")["total_revenue"].sum()
        st.bar_chart(revenue_by_cat)
    else:
        st.warning("No data available for the selected filters.")

with col_chart2:
    st.subheader("🌍 Transaction Share by Country")
    if not filtered_df.empty:
        trans_by_country = filtered_df.groupby("country")["total_transactions"].sum()
        st.bar_chart(trans_by_country)
    else:
        st.warning("No data available for the selected filters.")

st.divider()

# Processed Spark Data Inspector and Download Section
st.subheader("📁 Processed Spark Data Inspector & Export")

st.dataframe(filtered_df, width='stretch')

# CSV Export Download Button
if not filtered_df.empty:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="spark_analytics_filtered.csv",
        mime="text/csv"
    )