"""
Automated Financial Report Generator.
Exports both an executive text summary (.txt) and a structured CSV report (.csv).
"""

import os
from datetime import datetime


def export_reports(analysis: dict, reports_dir: str = "reports") -> tuple[str, str]:
    """Generate human-readable TXT summary and structured CSV report."""
    os.makedirs(reports_dir, exist_ok=True)

    txt_path = os.path.join(reports_dir, "monthly_expense_summary.txt")
    csv_path = os.path.join(reports_dir, "category_monthly_report.csv")

    # Export category summary table as clean report CSV
    analysis["category_summary"].to_csv(csv_path, index=False)

    # Build executive text report
    lines = [
        "=" * 68,
        "         PERSONAL EXPENSE TRACKER - EXECUTIVE FINANCIAL REPORT",
        "=" * 68,
        f"Generated On          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Analysis Period       : {analysis['date_range']}",
        f"Total Transactions    : {analysis['total_transactions']}",
        "-" * 68,
        "1. KEY FINANCIAL METRICS",
        "-" * 68,
        f"Total Cumulative Spend : ₹{analysis['total_spend']:,.2f}",
        f"Average Monthly Spend  : ₹{analysis['avg_monthly_spend']:,.2f}",
        f"Latest Month ({analysis['latest_month']})  : ₹{analysis['latest_month_spend']:,.2f}",
        f"Average Daily Spend    : ₹{analysis['avg_daily_spend']:,.2f}",
        f"Average Transaction    : ₹{analysis['avg_transaction']:,.2f}",
        f"Highest Spend Category : {analysis['highest_category']} (₹{analysis['highest_category_amount']:,.2f} | {analysis['highest_category_pct']}%)",
        "",
        "-" * 68,
        "2. CATEGORY-WISE SPENDING BREAKDOWN",
        "-" * 68,
    ]

    for row in analysis["category_summary"].itertuples(index=False):
        lines.append(
            f"  • {row.Category:<20} | ₹{row.Total_Spent:>10,.2f} | {row.Share_Pct:>5.1f}% | ({row.Transaction_Count} txns)"
        )

    lines.extend([
        "",
        "-" * 68,
        "3. MONTHLY SPENDING TREND",
        "-" * 68,
    ])
    for row in analysis["monthly_summary"].itertuples(index=False):
        lines.append(
            f"  • {row.Month:<10} | ₹{row.Total_Spent:>10,.2f} | MoM Change: {row.MoM_Change_Pct:>+6.2f}%"
        )

    lines.extend([
        "",
        "-" * 68,
        "4. PAYMENT METHOD DISTRIBUTION",
        "-" * 68,
    ])
    for row in analysis["payment_summary"].itertuples(index=False):
        lines.append(
            f"  • {row.Payment_Method:<15} | ₹{row.Total_Spent:>10,.2f} | {row.Share_Pct:>5.1f}%"
        )

    budget_df = analysis.get("budget_status")
    if budget_df is not None and not budget_df.empty:
        lines.extend([
            "",
            "-" * 68,
            f"5. BUDGET HEALTH CHECK ({analysis['latest_month']})",
            "-" * 68,
        ])
        for row in budget_df.itertuples(index=False):
            lines.append(
                f"  • {row.Category:<18} | Limit: ₹{row.Monthly_Limit:>8,.0f} | Spent: ₹{row.Actual_Spent:>8,.0f} | [{row.Status}]"
            )

    lines.append("=" * 68)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[REPORTER] Saved text report to '{txt_path}' and CSV report to '{csv_path}'.")
    return txt_path, csv_path