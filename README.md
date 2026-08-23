Markdown
# ⚡ Enterprise Medallion Architecture: Big Data Spark & Analytics Pipeline

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://big-data-spark-pipeline-fpq9fozykr3m6bkpvq8fhz.streamlit.app)

An enterprise-grade, end-to-end Big Data Engineering and Analytics project built with **Python**, **Pandas/PySpark**, **Parquet**, and **Streamlit**. This pipeline implements the modern **Medallion Architecture (Bronze -> Silver -> Gold)** for large-scale e-commerce transactional data processing, cleaning, aggregations, and an interactive web analytics dashboard.

---

## 🏗️ Architecture & Medallion Layers

* **Bronze Layer (`output_bronze/`):** Ingests raw, uncleaned e-commerce transactional datasets in chunked Parquet format generated via Python.
* **Silver Layer (`output_silver/`):** Cleans raw data by removing null values, filtering invalid prices/quantities, and structuring high-performance transactional records.
* **Gold Layer (`output_gold/`):** Computes business-critical aggregations (total revenue, transaction counts, average product prices grouped by category and country) ready for business intelligence consumption.
* **Interactive Dashboard (`app.py`):** A modern Streamlit application consuming metrics directly from the Gold Layer, featuring multi-select filtering, real-time KPIs, dynamic charts, and CSV data export.

---

## 🚀 Getting Started Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git](https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git)
   cd big-data-spark-pipeline
Install dependencies:

Bash
pip install -r requirements.txt
Step 1: Generate Raw Data (Bronze Layer):

Bash
python generate_big_data.py
Step 2: Run Medallion Pipeline (Bronze -> Silver -> Gold):

Bash
python spark_pipeline.py
Step 3: Launch the Streamlit Analytics Dashboard:

Bash
streamlit run app.py