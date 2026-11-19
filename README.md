# 💳 AI-Powered Personal Expense Tracker with Data Visualization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas%20%7C%20NumPy-150458?logo=pandas)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

**Repository:** `AI-Powered-Personal-Expense-Tracker-Visualization`

An end-to-end, industry-oriented Python financial analytics and visualization system that ingests personal transaction logs, cleans and auto-categorizes spending using intelligent pattern rules, persists structured records in SQLite, exports monthly executive reports, and serves an interactive Streamlit web dashboard.

---

## 📋 Table of Contents
- [Problem Statement](#-problem-statement)
- [Industry Relevance](#-industry-relevance)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#️-tech-stack)
- [Folder Structure](#-folder-structure)
- [Installation & Setup (Windows PowerShell)](#-installation--setup-windows-powershell)
- [How to Run the Project](#-how-to-run-the-project)
- [Sample Output & Visualizations](#-sample-output--visualizations)
- [Future AI/ML Enhancements](#-future-aiml-enhancements)
- [Learning Outcomes](#-learning-outcomes)

---

## 📌 Problem Statement
Raw transaction records from bank statements, UPI apps, and digital receipts are fragmented and difficult to interpret manually. Without structured categorization, historical persistence, and visual trend tracking, individuals and small businesses struggle to detect budget leaks, monitor recurring obligations, or control discretionary spending.

---

## 🏭 Industry Relevance
Automated transaction categorization, cash-flow visualization, and budget variance alerting form the core analytics backbone of modern FinTech platforms (such as CRED, Mint, Paytm, PhonePe, and RazorpayX). This project demonstrates practical, job-ready competencies across **Data Analyst, Python Developer, Business Analyst, and FinTech Analytics** roles—spanning ETL pipelines, relational schema design, data cleaning, statistical visualization, and interactive BI dashboarding.

---

## ✨ Key Features
- **Synthetic & Multi-Source Ingestion:** Generates 6 months of realistic personal spending (`data_generator.py`) and supports custom bank/UPI CSV uploads or manual form logging via the UI.
- **Automated Data Wrangling & Smart Categorization:** Removes duplicate rows, handles missing/corrupt amounts, standardizes timestamps and casing, and auto-classifies unlabelled descriptions using regex pattern intelligence.
- **SQLite Relational Persistence:** Stores transactions and monthly category budget limits in `data/expenses.db` with composite `UNIQUE` constraints to prevent duplicate imports.
- **Multi-Dimensional Financial Analytics:** Computes cumulative spend, monthly trends (MoM % change), category shares, payment method distributions, average daily spend, 7-day rolling averages, and `OVER BUDGET` alerts.
- **Publication-Grade Visualizations:** Automatically exports 4 high-resolution (`300 DPI`) Matplotlib/Seaborn charts to `images/`.
- **Automated Reporting & Interactive Web UI:** Generates formatted `.txt` and `.csv` reports in `reports/` alongside a live Streamlit dashboard for dynamic exploration.

---

## 📐 System Architecture
```text
+-------------------------------------------------------------------+
|                        1. INPUT LAYER                             |
|  [ Synthetic Generator ]   [ Bank/UPI CSV ]   [ Manual UI Entry ] |
+---------------------------------+---------------------------------+
                                  |
                                  ▼
+-------------------------------------------------------------------+
|                     2. PROCESSING & STORAGE                       |
|  • Data Cleaning & Date Parsing (Pandas)                          |
|  • Intelligent Rule-Based Auto-Categorizer (Regex Engine)         |
|  • Relational Persistence (SQLite: transactions & budgets)        |
|  • KPI, Rolling Average & Budget Variance Engine (Pandas / NumPy) |
+---------------------------------+---------------------------------+
                                  |
                 +----------------+----------------+
                 ▼                                 ▼
+---------------------------------+ +-------------------------------+
|    3A. AUTOMATED ARTIFACTS      | |   3B. INTERACTIVE FRONTEND    |
|  • 4 High-Res PNG Charts        | |  • Streamlit Web Dashboard    |
|  • Monthly Summary (.txt)       | |  • Live Month/Category Filters|
|  • Category Breakdown (.csv)    | |  • Budget Overspend Alerts    |
+---------------------------------+ +-------------------------------+
🛠️ Tech StackProgramming Language: Python 3.10+Data Processing & Analytics: Pandas, NumPyRelational Database: SQLite3Static Data Visualization: Matplotlib, SeabornInteractive Web Dashboard: Streamlit📂 Folder StructurePlaintextAI-Powered-Personal-Expense-Tracker-Visualization/
│
├── data/                        # Raw CSVs, cleaned datasets, and SQLite DB (auto-populated)
├── notebooks/                   # Jupyter notebooks for exploratory data analysis (EDA)
├── src/                         # Modular Python source code
│   ├── __init__.py              # Marks src as a Python package
│   ├── data_generator.py        # Synthetic 6-month expense dataset generator
│   ├── database.py              # SQLite schema initialization, upsert & budget CRUD
│   ├── processor.py             # Data cleaning, date conversion & auto-categorization
│   ├── analyzer.py              # KPI, category, monthly, daily & budget analytics
│   ├── visualizer.py            # Matplotlib/Seaborn 300-DPI chart generator
│   ├── report_generator.py      # Executive TXT & structured CSV report exporter
│   └── dashboard.py             # Interactive Streamlit web dashboard
├── outputs/                     # Processed summary CSV tables (auto-populated)
├── images/                      # Saved visual charts & UI screenshots
├── reports/                     # Generated monthly text & CSV reports
├── docs/                        # Supplementary project documentation
├── main.py                      # Single-command master pipeline orchestrator
├── requirements.txt             # Python package dependencies
├── .gitignore                   # Git exclusion rules (venv, cache, local .db)
└── README.md                    # Portfolio project documentation
⚙️ Installation & Setup (Windows PowerShell)Open Windows PowerShell inside the project root directory (AI-Powered-Personal-Expense-Tracker-Visualization/) and run the following commands step by step:1. Create Project SubfoldersPowerShellNew-Item -ItemType Directory -Force -Path "data", "notebooks", "src", "outputs", "images", "reports", "docs"
2. Create & Activate Virtual EnvironmentPowerShellpython -m venv venv
.\venv\Scripts\Activate.ps1
(Note: If PowerShell restricts script execution, run Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned once and re-run .\venv\Scripts\Activate.ps1.)3. Install Required LibrariesUsing python -m pip ensures smooth installation even on restricted university/corporate Windows environments where standalone .exe wrappers are blocked:PowerShellpython -m pip install --upgrade pip
python -m pip install -r requirements.txt
(Or install packages directly: python -m pip install pandas numpy matplotlib seaborn streamlit)4. Verify InstallationPowerShellpython -c "import pandas, numpy, matplotlib, seaborn, streamlit, sqlite3; print('All libraries installed successfully!')"
🚀 How to Run the ProjectStep 1: Execute the Automated ETL, Analytics, Charting & Reporting PipelinePowerShellpython main.py
This single command generates synthetic transactions, cleans and auto-categorizes the data, syncs SQLite (data/expenses.db), exports 4 charts to images/, and writes executive reports to reports/.Step 2: Launch the Interactive Streamlit DashboardPowerShellpython -m streamlit run src/dashboard.py
Open http://localhost:8501 in your browser to filter months/categories, add manual expenses, upload custom bank CSVs, and manage monthly category budgets.📊 Sample Output & VisualizationsExpected Terminal Output (python main.py)Plaintext=================================================================
   PERSONAL EXPENSE TRACKER & DATA VISUALIZATION PIPELINE
=================================================================
[DATA GENERATOR] Created 448 raw expense records at 'data/raw_expenses.csv'.
[PROCESSOR] Cleaned dataset: 446 valid rows retained (2 corrupt/duplicate rows removed).
[DATABASE] Synced SQLite database 'data/expenses.db' (446 new records inserted).
[VISUALIZER] Generated 4 high-resolution charts in 'images/'.
[REPORTER] Saved text report to 'reports/monthly_expense_summary.txt' and CSV report to 'reports/category_monthly_report.csv'.
Generated Visual ChartsCategory-Wise SpendingMonthly Spending TrendPayment Method DistributionDaily Spending & 7-Day Rolling Trend🔮 Future AI/ML EnhancementsMachine Learning Auto-Categorizer: Upgrade from regex rules to a TF-IDF + Multinomial Naive Bayes / Logistic Regression classifier trained on historical user-labeled transactions.Time-Series Spend Forecasting: Integrate ARIMA or Facebook Prophet to forecast next month's expected category expenditure.OCR Receipt Scanner: Add Tesseract OCR support to extract merchant names and amounts directly from uploaded receipt photos.Automated Budget Alerts: Trigger email or Telegram notifications whenever a category exceeds 85% of its monthly budget threshold.🎯 Learning OutcomesArchitecting modular, production-style Python ETL pipelines separating data ingestion, cleaning, persistence, analytics, and UI presentation.Enforcing data integrity and deduplication using SQLite relational schemas alongside Pandas data-wrangling workflows.Translating raw financial logs into executive KPIs, rolling time-series metrics, automated reports, and interactive Streamlit dashboards.
