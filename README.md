Markdown
# 🛡️ Enterprise Data Governance, Quality & Analytics Pipeline

A production-grade, end-to-end Big Data pipeline implementing the **Medallion Architecture (Bronze -> Silver -> Gold)** combined with **Data Quality Governance**, automated quarantine auditing, and an interactive **Streamlit** analytics dashboard.

---

## 🏗️ Architecture Overview

This project simulates a real-world enterprise data platform designed to ingest raw transactions, enforce strict data quality rules, isolate corrupted records, and serve aggregated business insights.

[ Raw Data Generator ]
│
▼
[ Bronze Layer ] ──(Data Quality Gates)──► [ Quarantine Layer ] (Failed Records Audit)
│
▼ (Cleaning & Validation)
[ Silver Layer ]
│
▼ (Business Aggregations)
[ Gold Layer ] ──► [ Streamlit Cloud Dashboard ]


---

## 🛠️ Tech Stack & Tools

* **Language:** Python
* **Data Processing & Modeling:** Pandas, PyArrow (Parquet)
* **Data Architecture:** Medallion Architecture (Bronze, Silver, Gold, Quarantine)
* **Data Governance & Quality:** Automated null-checks, boundary validation (positive price/quantity rules)
* **Visualization & Web App:** Streamlit, Streamlit Cloud
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
big-data-spark-pipeline/
│
├── output_bronze/          # Raw ingested transactional data (Parquet)
├── output_silver/          # Cleaned and validated transaction records
├── output_gold/            # Aggregated business metrics for reporting
├── output_quarantine/      # Isolated records that failed data quality checks
├── app.py                  # Interactive Streamlit dashboard & automated pipeline runner
└── README.md               # Project documentation
🚀 Key Features
Automated Data Ingestion (Bronze): Generates large-scale synthetic e-commerce transaction datasets with simulated noise.

Data Governance & Quality Gates (Silver & Quarantine): Enforces data contracts (e.g., preventing null values in critical fields, filtering out negative prices or quantities). Invalid rows are automatically routed to a Quarantine Layer for auditing.

Business Intelligence (Gold): Computes high-level KPIs such as total revenue, transaction counts, and average product prices grouped by product categories and countries.

Interactive Dashboard & Cloud Readiness: Built with Streamlit, featuring advanced multi-select filters, real-time KPI metrics, data inspector tables, and CSV export capabilities.

💻 Local Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git](https://github.com/tutarzeliha-ctrl/big-data-spark-pipeline.git)
cd big-data-spark-pipeline
Install dependencies:

Bash
pip install streamlit pandas pyarrow
Run the Streamlit application:

Bash
streamlit run app.py
🌐 Live Demo
You can access the live production-grade application deployed on Streamlit Cloud via the repository link.

---
### 🚀 [Access Live Streamlit Cloud Application](https://big-data-spark-pipeline-fpq9fozykr3m6bkpvq8fhz.streamlit.app/)