"""
Financial Analytics Engine.
Computes category-wise spend, monthly trends, payment method splits,
highest spending category, average daily spend, and budget variances.
"""

import os
import pandas as pd


def analyze_expenses(df: pd.DataFrame, budgets_df: pd.DataFrame | None = None, export_dir: str = "outputs") -> dict:
    """Run comprehensive financial analyses and return structured metrics + summary tables."""
    os.makedirs(export_dir, exist_ok=True)

    if df.empty:
        raise ValueError("Cannot analyze an empty expense DataFrame.")

    # 1. Overall & Daily Metrics
    total_spend = float(df["Amount"].sum())
    total_transactions = int(len(df))
    avg_transaction = float(df["Amount"].mean())

    start_date = df["Date"].min()
    end_date = df["Date"].max()
    total_calendar_days = max((end_date - start_date).days + 1, 1)
    avg_daily_spend = total_spend / total_calendar_days

    # 2. Category-Wise Spending Analysis
    category_summary = (
        df.groupby("Category", as_index=False)
        .agg(
            Total_Spent=("Amount", "sum"),
            Transaction_Count=("Amount", "count"),
            Avg_Spend=("Amount", "mean"),
        )
        .sort_values(by="Total_Spent", ascending=False)
        .reset_index(drop=True)
    )
    category_summary["Share_Pct"] = (category_summary["Total_Spent"] / total_spend * 100).round(2)

    highest_category = category_summary.iloc[0]["Category"]
    highest_category_amount = float(category_summary.iloc[0]["Total_Spent"])
    highest_category_pct = float(category_summary.iloc[0]["Share_Pct"])

    # 3. Monthly Spending Trend Analysis
    monthly_summary = (
        df.groupby("Month", as_index=False)
        .agg(
            Total_Spent=("Amount", "sum"),
            Transaction_Count=("Amount", "count"),
        )
        .sort_values(by="Month")
        .reset_index(drop=True)
    )
    monthly_summary["MoM_Change_Pct"] = monthly_summary["Total_Spent"].pct_change().mul(100).fillna(0).round(2)
    avg_monthly_spend = float(monthly_summary["Total_Spent"].mean())
    latest_month = monthly_summary.iloc[-1]["Month"]
    latest_month_spend = float(monthly_summary.iloc[-1]["Total_Spent"])

    # 4. Payment Method Analysis
    payment_summary = (
        df.groupby("Payment_Method", as_index=False)
        .agg(
            Total_Spent=("Amount", "sum"),
            Transaction_Count=("Amount", "count"),
        )
        .sort_values(by="Total_Spent", ascending=False)
        .reset_index(drop=True)
    )
    payment_summary["Share_Pct"] = (payment_summary["Total_Spent"] / total_spend * 100).round(2)

    # 5. Daily Spending Trend (for line/rolling trend chart)
    daily_summary = (
        df.groupby("Date", as_index=False)
        .agg(Daily_Spent=("Amount", "sum"))
        .sort_values(by="Date")
        .reset_index(drop=True)
    )
    daily_summary["Rolling_7D_Avg"] = daily_summary["Daily_Spent"].rolling(window=7, min_periods=1).mean().round(2)

    # 6. Latest Month Budget vs. Actual Check
    latest_month_df = df[df["Month"] == latest_month]
    latest_cat_spend = (
        latest_month_df.groupby("Category", as_index=False)
        .agg(Actual_Spent=("Amount", "sum"))
    )

    if budgets_df is not None and not budgets_df.empty:
        budget_status = budgets_df.merge(latest_cat_spend, on="Category", how="left").fillna({"Actual_Spent": 0.0})
        budget_status["Variance"] = budget_status["Monthly_Limit"] - budget_status["Actual_Spent"]
        budget_status["Status"] = budget_status["Variance"].apply(
            lambda v: "OVER BUDGET" if v < 0 else "Within Budget"
        )
        budget_status = budget_status.sort_values(by="Variance").reset_index(drop=True)
    else:
        budget_status = pd.DataFrame()

    # Save processed summary tables to outputs/
    category_summary.to_csv(os.path.join(export_dir, "category_summary.csv"), index=False)
    monthly_summary.to_csv(os.path.join(export_dir, "monthly_summary.csv"), index=False)
    payment_summary.to_csv(os.path.join(export_dir, "payment_summary.csv"), index=False)

    return {
        "total_spend": round(total_spend, 2),
        "total_transactions": total_transactions,
        "avg_transaction": round(avg_transaction, 2),
        "avg_daily_spend": round(avg_daily_spend, 2),
        "avg_monthly_spend": round(avg_monthly_spend, 2),
        "latest_month": latest_month,
        "latest_month_spend": round(latest_month_spend, 2),
        "highest_category": highest_category,
        "highest_category_amount": round(highest_category_amount, 2),
        "highest_category_pct": highest_category_pct,
        "date_range": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "payment_summary": payment_summary,
        "daily_summary": daily_summary,
        "budget_status": budget_status,
    }