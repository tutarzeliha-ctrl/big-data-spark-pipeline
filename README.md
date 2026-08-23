# ⚡ Enterprise Medallion Architecture: Big Data Spark & Analytics Pipeline

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