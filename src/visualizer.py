"""
Data Visualization Engine using Matplotlib and Seaborn.
Generates 4 publication-grade charts saved to the images/ directory.
"""

import os
import matplotlib
matplotlib.use("Agg")  # Headless backend for reliable cross-platform saving
import matplotlib.pyplot as plt
import seaborn as sns


def generate_all_charts(analysis: dict, images_dir: str = "images") -> list[str]:
    """Generate and save all 4 required expense visualization charts."""
    os.makedirs(images_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    saved_paths = []

    # 1. Category-Wise Spending Bar Chart
    cat_df = analysis["category_summary"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(
        data=cat_df,
        x="Total_Spent",
        y="Category",
        hue="Category",
        palette="viridis",
        legend=False,
        ax=ax,
    )
    ax.set_title("Total Spending by Category (INR)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Total Spent (₹)", fontsize=11)
    ax.set_ylabel("Expense Category", fontsize=11)
    for container in ax.containers:
        ax.bar_label(container, fmt=" ₹%.0f", padding=4, fontsize=9)
    ax.set_xlim(0, cat_df["Total_Spent"].max() * 1.18)
    plt.tight_layout()
    p1 = os.path.join(images_dir, "category_bar_chart.png")
    plt.savefig(p1, dpi=300)
    plt.close(fig)
    saved_paths.append(p1)

    # 2. Monthly Spending Trend Line Chart
    mon_df = analysis["monthly_summary"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        mon_df["Month"],
        mon_df["Total_Spent"],
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#1f77b4",
        label="Monthly Spend",
    )
    for i, row in mon_df.iterrows():
        ax.annotate(
            f"₹{row['Total_Spent']:,.0f}",
            (row["Month"], row["Total_Spent"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=9,
            fontweight="bold",
        )
    ax.set_title("Monthly Expense Trend (6-Month Trajectory)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Total Spend (₹)", fontsize=11)
    ax.set_ylim(0, mon_df["Total_Spent"].max() * 1.22)
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    p2 = os.path.join(images_dir, "monthly_trend_line.png")
    plt.savefig(p2, dpi=300)
    plt.close(fig)
    saved_paths.append(p2)

    # 3. Payment Method Distribution Pie Chart
    pay_df = analysis["payment_summary"]
    fig, ax = plt.subplots(figsize=(7.5, 6))
    colors = sns.color_palette("Set2", len(pay_df))
    wedges, texts, autotexts = ax.pie(
        pay_df["Total_Spent"],
        labels=pay_df["Payment_Method"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")
    ax.set_title("Spending Share by Payment Method", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    p3 = os.path.join(images_dir, "payment_method_pie.png")
    plt.savefig(p3, dpi=300)
    plt.close(fig)
    saved_paths.append(p3)

    # 4. Daily Spending Trend Chart (with 7-Day Rolling Average)
    day_df = analysis["daily_summary"]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(
        day_df["Date"],
        day_df["Daily_Spent"],
        alpha=0.35,
        color="#7f8c8d",
        label="Daily Spend (₹)",
    )
    ax.plot(
        day_df["Date"],
        day_df["Rolling_7D_Avg"],
        color="#e74c3c",
        linewidth=2.2,
        label="7-Day Rolling Average (₹)",
    )
    ax.set_title("Daily Spending Fluctuations & 7-Day Rolling Trend", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Amount Spent (₹)", fontsize=11)
    ax.legend(loc="upper right")
    plt.xticks(rotation=30)
    plt.tight_layout()
    p4 = os.path.join(images_dir, "daily_spending_trend.png")
    plt.savefig(p4, dpi=300)
    plt.close(fig)
    saved_paths.append(p4)

    print(f"[VISUALIZER] Generated {len(saved_paths)} high-resolution charts in '{images_dir}/'.")
    return saved_paths