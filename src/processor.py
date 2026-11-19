"""
Data Loading, Cleaning, Date Conversion, and Rule-Based Auto-Categorization Module.
"""

import os
import re
import pandas as pd


CATEGORY_RULES = {
    "Food & Dining": [r"swiggy", r"zomato", r"starbucks", r"cafe", r"canteen", r"pizza", r"restaurant", r"coffee", r"snacks"],
    "Groceries": [r"blinkit", r"d-mart", r"dmart", r"reliance fresh", r"zepto", r"supermarket", r"grocery", r"vegetables", r"dairy"],
    "Transport": [r"uber", r"ola", r"metro", r"petrol", r"diesel", r"fuel", r"rapido", r"bus", r"cab", r"train"],
    "Bills & Utilities": [r"electricity", r"broadband", r"wifi", r"mobile", r"recharge", r"water", r"gas", r"bill"],
    "Rent": [r"rent", r"lease", r"landlord", r"pg accommodation"],
    "Shopping": [r"amazon", r"myntra", r"flipkart", r"decathlon", r"bookstore", r"apparel", r"electronics"],
    "Entertainment": [r"netflix", r"bookmyshow", r"movie", r"spotify", r"gaming", r"bowling", r"cinema"],
    "Healthcare": [r"pharmacy", r"apollo", r"dental", r"blood test", r"hospital", r"doctor", r"medicine", r"supplements"],
}


def auto_categorize(description: str) -> str:
    """Infer expense category from transaction description using regex rules."""
    text = str(description).lower().strip()
    for category, patterns in CATEGORY_RULES.items():
        if any(re.search(pattern, text) for pattern in patterns):
            return category
    return "Other"


def load_and_clean_expenses(
    raw_csv_path: str = "data/raw_expenses.csv",
    cleaned_csv_path: str = "data/cleaned_expenses.csv",
) -> pd.DataFrame:
    """Load raw CSV, clean anomalies, standardize fields, and enrich date features."""
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Input CSV not found at '{raw_csv_path}'.")

    df = pd.read_csv(raw_csv_path)
    initial_rows = len(df)

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # 2. Convert Date and Amount to proper data types
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # 3. Drop records with invalid Date, missing/non-positive Amount, or missing Description
    df = df.dropna(subset=["Date", "Amount", "Description"])
    df = df[df["Amount"] > 0].copy()

    # 4. Standardize text formatting
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Payment_Method"] = df["Payment_Method"].fillna("UPI").astype(str).str.strip()
    df["Payment_Method"] = df["Payment_Method"].replace({"upi": "UPI", "Upi": "UPI"})

    # 5. Fill missing or blank categories via rule-based auto-categorization
    df["Category"] = df["Category"].fillna("").astype(str).str.strip()
    df["Category"] = df.apply(
        lambda row: auto_categorize(row["Description"]) if row["Category"] == "" else row["Category"].title(),
        axis=1,
    )

    # Fix title-casing edge cases like 'And' -> '&'
    df["Category"] = df["Category"].str.replace(" And ", " & ", regex=False)

    # 6. Feature engineering for temporal analysis
    df = df.sort_values(by="Date").reset_index(drop=True)
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Month_Label"] = df["Date"].dt.strftime("%b %Y")
    df["Day_Name"] = df["Date"].dt.day_name()

    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)
    df.to_csv(cleaned_csv_path, index=False)

    removed_rows = initial_rows - len(df)
    print(f"[PROCESSOR] Cleaned dataset: {len(df)} valid rows retained ({removed_rows} corrupt/duplicate rows removed).")
    return df