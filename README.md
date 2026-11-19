# 💳 Personal Expense Tracker with Data Visualization

An end-to-end Python financial analytics and visualization system that ingests personal transaction logs, cleans and auto-categorizes spending, persists records in SQLite, exports monthly executive reports, and provides an interactive Streamlit dashboard.

---

## 📌 Problem Statement
Raw transaction records from bank statements, UPI apps, and receipts are difficult to interpret manually. Without structured categorization and visual trend tracking, individuals struggle to detect budget leaks, monitor recurring obligations, or control discretionary spending.

## 🏭 Industry Relevance
Automated transaction categorization, cash-flow visualization, and budget variance alerting form the core analytics backbone of modern FinTech platforms (such as Mint, CRED, Paytm, PhonePe, and RazorpayX). This project demonstrates practical competencies in **ETL data pipelines, relational database modeling, exploratory data analysis (EDA), automated reporting, and interactive BI dashboarding**.

---

## ✨ Key Features
- **Synthetic & CSV Data Ingestion:** Simulates 6 months of realistic personal spending and supports custom CSV bank/UPI uploads or manual form logging.
- **Automated Data Cleaning & Regex Categorization:** Handles missing values, removes duplicates, standardizes timestamps, and infers categories from merchant descriptions.
- **SQLite Persistence:** Stores transactions and monthly category budgets in a normalized relational database with duplicate prevention.
- **Multi-Dimensional Financial Analytics:** Computes cumulative spend, monthly trends (MoM % change), category breakdowns, payment mode shares, average daily spend, and budget overspend alerts.
- **High-Resolution Visualizations:** Generates 4 publication-grade charts (Category Bar Chart, Monthly Trend Line, Payment Method Pie Chart, and Daily 7-Day Rolling Trend).
- **Automated Reporting & Interactive Dashboard:** Exports `.txt` and `.csv` summaries alongside a full-featured Streamlit web app.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Processing & Analytics:** Pandas, NumPy
- **Database:** SQLite3
- **Data Visualization:** Matplotlib, Seaborn
- **Web Dashboard:** Streamlit

---

## 📂 Folder Structure
```text
Personal-Expense-Tracker-Visualization/
│
├── data/                        # Raw CSVs, cleaned datasets, and SQLite DB
├── notebooks/                   # Jupyter notebooks for EDA prototyping
├── src/                         # Modular Python source code
│   ├── data_generator.py        # Synthetic expense dataset generator
│   ├── database.py              # SQLite schema & CRUD operations
│   ├── processor.py             # Data cleaning & auto-categorization
│   ├── analyzer.py              # KPI, category, monthly & budget analytics
│   ├── visualizer.py            # Matplotlib/Seaborn chart generator
│   ├── report_generator.py      # TXT & CSV monthly report exporter
│   └── dashboard.py             # Interactive Streamlit web dashboard
├── outputs/                     # Processed summary CSV tables
├── images/                      # Saved visual charts & UI screenshots
├── reports/                     # Executive text & CSV reports
├── docs/                        # Supplementary documentation
├── main.py                      # End-to-end pipeline orchestrator
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git exclusion rules
└── README.md                    # Project documentation