Markdown
# ⚡ Big Data Spark Pipeline & Interactive Analytics

An enterprise-grade, end-to-end Big Data Engineering and Analytics project built with **Python**, **PySpark**, **Parquet**, and **Streamlit**. This pipeline demonstrates large-scale dataset generation, distributed processing, and an interactive web-based analytics dashboard.

---

## 🏗️ Architecture & Tech Stack

* **Data Generation (`generate_big_data.py`):** Generates large-scale synthetic e-commerce transactional datasets in chunked Parquet format using Pandas and NumPy.
* **Distributed Processing (`spark_pipeline.py`):** Initializes an optimized PySpark session, loads distributed Parquet chunks, performs high-performance SQL-like aggregations (revenue, transaction counts, averages), and writes partitioned output data.
* **Interactive Dashboard (`app.py`):** A modern Streamlit application featuring advanced multi-select filtering, real-time KPIs, dynamic charts, and a CSV export utility.

---

## 🚀 Getting Started Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git](https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git)
   cd big-data-spark-pipeline
Install dependencies:

Bash
pip install pyspark pandas numpy streamlit pyarrow
Generate the large dataset:

Bash
python generate_big_data.py
Run the PySpark pipeline:

Bash
python spark_pipeline.py
Launch the Streamlit dashboard:

Bash
streamlit run app.py
📊 Dashboard Preview & Features
Multi-Dimensional Filters: Filter data dynamically by country and product category.

Key Performance Indicators (KPIs): Real-time tracking of Total Revenue, Total Transactions, and Average Product Price.

Data Export: Instant download of filtered dataset chunks via CSV format.