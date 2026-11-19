"""
Interactive Streamlit Web Dashboard for Personal Expense Tracker.
Supports CSV ingestion, manual expense entry, live filtering, budget alerts,
interactive charts, and one-click report downloads.
"""

import os
import sys
from pathlib import Path
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ensure root directory is on sys.path regardless of launch directory
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_generator import generate_synthetic_expenses
from src.processor import load_and_clean_expenses, auto_categorize
from src.database import (
    load_transactions_from_db,
    save_transactions_to_db,
    add_single_transaction,
    get_budgets,
    update_budget,
)
from src.analyzer import analyze_expenses


st.set_page_config(page_title="Personal Expense Tracker", page_icon="💳", layout="wide")
st.title("💳 Personal Expense Tracker & Financial Analytics Dashboard")
st.markdown("Track daily expenses, auto-categorize transactions, monitor monthly budgets, and visualize spending trends.")

# Auto-seed database if empty on first launch
df_all = load_transactions_from_db()
if df_all.empty:
    generate_synthetic_expenses("data/raw_expenses.csv")
    cleaned = load_and_clean_expenses("data/raw_expenses.csv", "data/cleaned_expenses.csv")
    save_transactions_to_db(cleaned)
    df_all = load_transactions_from_db()

# --- SIDEBAR: MANUAL ENTRY, CSV UPLOAD & FILTERS ---
st.sidebar.header("➕ Log New Expense")
with st.sidebar.form("manual_expense_form", clear_on_submit=True):
    tx_date = st.date_input("Date", value=date.today())
    tx_desc = st.text_input("Description", placeholder="e.g., Swiggy Lunch / Metro Recharge")
    tx_amt = st.number_input("Amount (₹)", min_value=1.0, step=50.0, value=250.0)
    tx_cat = st.selectbox(
        "Category (Auto-detect if 'Auto')",
        ["Auto", "Food & Dining", "Groceries", "Transport", "Rent", "Bills & Utilities", "Shopping", "Entertainment", "Healthcare", "Other"],
    )
    tx_pay = st.selectbox("Payment Method", ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"])
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if not tx_desc.strip():
            st.sidebar.error("Please enter a transaction description.")
        else:
            final_cat = auto_categorize(tx_desc) if tx_cat == "Auto" else tx_cat
            added = add_single_transaction(
                tx_date=tx_date.strftime("%Y-%m-%d"),
                category=final_cat,
                amount=tx_amt,
                payment_method=tx_pay,
                description=tx_desc,
            )
            if added:
                st.sidebar.success(f"Added ₹{tx_amt:,.2f} under '{final_cat}'!")
                st.rerun()
            else:
                st.sidebar.warning("Duplicate transaction ignored.")

st.sidebar.divider()
st.sidebar.header("📤 Import Bank/UPI CSV")
uploaded_csv = st.sidebar.file_uploader("Upload CSV (Date, Category, Amount, Payment_Method, Description)", type=["csv"])
if uploaded_csv is not None:
    temp_path = "data/uploaded_temp.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded_csv.getbuffer())
    try:
        cleaned_upload = load_and_clean_expenses(temp_path, "data/cleaned_expenses.csv")
        new_rows = save_transactions_to_db(cleaned_upload)
        st.sidebar.success(f"Imported {new_rows} new transactions!")
        st.rerun()
    except Exception as exc:
        st.sidebar.error(f"CSV Error: {exc}")

st.sidebar.divider()
st.sidebar.header("🔍 Dashboard Filters")
all_months = sorted(df_all["Month"].unique())
selected_months = st.sidebar.multiselect("Filter Months", options=all_months, default=all_months)
all_cats = sorted(df_all["Category"].unique())
selected_cats = st.sidebar.multiselect("Filter Categories", options=all_cats, default=all_cats)

filtered_df = df_all[
    (df_all["Month"].isin(selected_months)) & (df_all["Category"].isin(selected_cats))
].copy()

if filtered_df.empty:
    st.warning("No transactions match the selected filters. Adjust your sidebar filters.")
    st.stop()

budgets_df = get_budgets()
analysis = analyze_expenses(filtered_df, budgets_df=budgets_df)

# --- TOP KPI CARDS ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Spend (Filtered)", f"₹{analysis['total_spend']:,.2f}", f"{analysis['total_transactions']} txns")
k2.metric("Average Daily Spend", f"₹{analysis['avg_daily_spend']:,.2f}")
k3.metric("Latest Month Spend", f"₹{analysis['latest_month_spend']:,.2f}", analysis["latest_month"])
k4.metric(
    "Top Spending Category",
    analysis["highest_category"],
    f"₹{analysis['highest_category_amount']:,.0f} ({analysis['highest_category_pct']}%)",
)

st.divider()

# --- CHARTS ROW 1 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category-Wise Spending")
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    cat_df = analysis["category_summary"]
    sns.barplot(data=cat_df, x="Total_Spent", y="Category", hue="Category", palette="viridis", legend=False, ax=ax1)
    ax1.set_xlabel("Total Spent (₹)")
    ax1.set_ylabel("")
    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.subheader("📈 Monthly Spending Trend")
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    mon_df = analysis["monthly_summary"]
    ax2.plot(mon_df["Month"], mon_df["Total_Spent"], marker="o", linewidth=2.5, color="#1f77b4")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Total Spent (₹)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig2)
    plt.close(fig2)

# --- CHARTS ROW 2 ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("💳 Payment Method Split")
    fig3, ax3 = plt.subplots(figsize=(6.5, 4.5))
    pay_df = analysis["payment_summary"]
    ax3.pie(pay_df["Total_Spent"], labels=pay_df["Payment_Method"], autopct="%1.1f%%", startangle=140)
    ax3.axis("equal")
    st.pyplot(fig3)
    plt.close(fig3)

with col4:
    st.subheader("📅 Daily Spending & 7-Day Rolling Trend")
    fig4, ax4 = plt.subplots(figsize=(7, 4.5))
    day_df = analysis["daily_summary"]
    ax4.plot(day_df["Date"], day_df["Daily_Spent"], alpha=0.35, color="gray", label="Daily")
    ax4.plot(day_df["Date"], day_df["Rolling_7D_Avg"], color="#e74c3c", linewidth=2, label="7-Day Avg")
    ax4.legend()
    plt.xticks(rotation=25)
    st.pyplot(fig4)
    plt.close(fig4)

st.divider()

# --- BUDGET TRACKER & TRANSACTIONS TABLE ---
b_col, t_col = st.columns([1, 1.3])

with b_col:
    st.subheader(f"🎯 Budget Status ({analysis['latest_month']})")
    st.dataframe(analysis["budget_status"], use_container_width=True, hide_index=True)

    with st.expander("⚙️ Edit Monthly Category Budget"):
        edit_cat = st.selectbox("Category", budgets_df["Category"].tolist())
        new_lim = st.number_input("New Monthly Limit (₹)", min_value=500.0, step=500.0, value=5000.0)
        if st.button("Save Budget Limit"):
            update_budget(edit_cat, new_lim)
            st.success(f"Updated {edit_cat} limit to ₹{new_lim:,.0f}")
            st.rerun()

with t_col:
    st.subheader("🧾 Recent Transactions")
    display_df = filtered_df[["Date", "Category", "Amount", "Payment_Method", "Description"]].sort_values(
        by="Date", ascending=False
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Transactions (CSV)",
        data=csv_bytes,
        file_name="filtered_expenses_export.csv",
        mime="text/csv",
    )