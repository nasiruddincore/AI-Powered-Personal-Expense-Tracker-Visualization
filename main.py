"""
Master Entry Point for Personal Expense Tracker with Data Visualization.
Executes the complete end-to-end ETL, SQLite storage, analytics, charting, and reporting pipeline.
"""

from src.data_generator import generate_synthetic_expenses
from src.processor import load_and_clean_expenses
from src.database import save_transactions_to_db, get_budgets
from src.analyzer import analyze_expenses
from src.visualizer import generate_all_charts
from src.report_generator import export_reports


def run_pipeline() -> None:
    print("\n" + "=" * 65)
    print("   PERSONAL EXPENSE TRACKER & DATA VISUALIZATION PIPELINE")
    print("=" * 65)

    # Step 1: Generate synthetic raw CSV dataset
    generate_synthetic_expenses(output_path="data/raw_expenses.csv")

    # Step 2: Load, clean, convert dates, and auto-categorize transactions
    cleaned_df = load_and_clean_expenses(
        raw_csv_path="data/raw_expenses.csv",
        cleaned_csv_path="data/cleaned_expenses.csv",
    )

    # Step 3: Persist cleaned transactions into SQLite database
    inserted_count = save_transactions_to_db(cleaned_df, db_path="data/expenses.db")
    print(f"[DATABASE] Synced SQLite database 'data/expenses.db' ({inserted_count} new records inserted).")

    # Step 4: Run financial KPI, category, monthly, payment, and budget analytics
    budgets_df = get_budgets(db_path="data/expenses.db")
    analysis = analyze_expenses(cleaned_df, budgets_df=budgets_df, export_dir="outputs")

    # Step 5: Generate high-resolution visualization charts
    generate_all_charts(analysis, images_dir="images")

    # Step 6: Export executive TXT and structured CSV reports
    export_reports(analysis, reports_dir="reports")

    # Step 7: Print key executive insights to terminal
    print("\n" + "-" * 65)
    print("KEY FINANCIAL INSIGHTS SUMMARY")
    print("-" * 65)
    print(f"• Analysis Period          : {analysis['date_range']}")
    print(f"• Total Cumulative Spend   : ₹{analysis['total_spend']:,.2f}")
    print(f"• Latest Monthly Spend     : ₹{analysis['latest_month_spend']:,.2f} ({analysis['latest_month']})")
    print(f"• Average Daily Spend      : ₹{analysis['avg_daily_spend']:,.2f}")
    print(f"• Highest Spend Category   : {analysis['highest_category']} (₹{analysis['highest_category_amount']:,.2f} | {analysis['highest_category_pct']}%)")
    print("-" * 65)
    print("Pipeline completed successfully! Run 'streamlit run src/dashboard.py' for interactive UI.\n")


if __name__ == "__main__":
    run_pipeline()