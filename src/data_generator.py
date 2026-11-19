"""
Generates realistic synthetic personal expense data (6 months)
including intentional data quality imperfections to demonstrate cleaning.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def generate_synthetic_expenses(output_path: str = "data/raw_expenses.csv", seed: int = 42) -> pd.DataFrame:
    """Create a realistic 6-month personal expense dataset and save to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(seed)
    np.random.seed(seed)

    # Realistic category templates: (min_amt, max_amt, descriptions, preferred_payments)
    catalog = {
        "Food & Dining": (
            80, 950,
            ["Swiggy Dinner Order", "Zomato Lunch", "Starbucks Coffee", "Local Cafe Snacks", "Campus Canteen", "Domino's Pizza"],
            ["UPI", "Credit Card", "Debit Card", "Cash"]
        ),
        "Groceries": (
            250, 2800,
            ["Blinkit Instant Groceries", "D-Mart Monthly Ration", "Reliance Fresh Vegetables", "Zepto Dairy & Fruits", "Supermarket Essentials"],
            ["UPI", "Debit Card", "Credit Card"]
        ),
        "Transport": (
            40, 1400,
            ["Uber Cab Ride", "Ola Auto", "Metro Card Recharge", "HP Petrol Fuel", "Rapido Bike Taxi", "Intercity Bus Ticket"],
            ["UPI", "Cash", "Credit Card"]
        ),
        "Shopping": (
            450, 5500,
            ["Amazon Electronics", "Myntra Apparel", "Flipkart Accessories", "Decathlon Sportswear", "Bookstore Purchase"],
            ["Credit Card", "UPI", "Debit Card"]
        ),
        "Entertainment": (
            150, 1600,
            ["Netflix Subscription", "BookMyShow Movie Tickets", "Spotify Premium", "Gaming Top-up", "Weekend Bowling"],
            ["Credit Card", "UPI"]
        ),
        "Healthcare": (
            200, 3200,
            ["Apollo Pharmacy Medicines", "Dental Checkup", "Lab Blood Test", "Wellness Supplements"],
            ["UPI", "Debit Card", "Cash"]
        ),
    }

    records = []
    start_date = datetime(2026, 5, 1)
    num_days = 184  # May 2026 through October 2026 (6 months)

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        is_weekend = current_date.weekday() >= 5

        # Fixed monthly bills on the 1st and 5th of each month
        if current_date.day == 1:
            records.append({
                "Date": date_str,
                "Category": "Rent",
                "Amount": 12000.00,
                "Payment_Method": "Net Banking",
                "Description": "Monthly Apartment Rent"
            })
        if current_date.day == 5:
            records.append({
                "Date": date_str,
                "Category": "Bills & Utilities",
                "Amount": round(random.uniform(1100, 1850), 2),
                "Payment_Method": "UPI",
                "Description": "Electricity & Broadband WiFi Bill"
            })
            records.append({
                "Date": date_str,
                "Category": "Bills & Utilities",
                "Amount": 399.00,
                "Payment_Method": "UPI",
                "Description": "Mobile Postpaid Recharge"
            })

        # Daily variable expenses (more transactions on weekends)
        daily_tx_count = random.choices([1, 2, 3], weights=[0.45, 0.40, 0.15])[0]
        if is_weekend:
            daily_tx_count += 1

        for _ in range(daily_tx_count):
            cat = random.choices(
                list(catalog.keys()),
                weights=[0.35, 0.20, 0.20, 0.10, 0.10, 0.05]
            )[0]
            min_a, max_a, descs, pays = catalog[cat]
            amount = round(random.uniform(min_a, max_a), 2)
            desc = random.choice(descs)
            pay = random.choice(pays)

            # Leave ~10% of categories blank to test rule-based auto-categorization
            assigned_cat = "" if random.random() < 0.10 else cat

            records.append({
                "Date": date_str,
                "Category": assigned_cat,
                "Amount": amount,
                "Payment_Method": pay,
                "Description": desc
            })

    # Inject a few realistic dirty rows (duplicates, inconsistent casing, null amount) to test cleaning
    records.append(records[10].copy())  # Duplicate row
    records.append({
        "Date": "2026-07-14",
        "Category": "  food & dining ",
        "Amount": 320.50,
        "Payment_Method": "upi",
        "Description": "Evening Tea & Snacks"
    })
    records.append({
        "Date": "2026-08-09",
        "Category": "Shopping",
        "Amount": np.nan,
        "Payment_Method": "Credit Card",
        "Description": "Corrupt Failed Transaction"
    })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"[DATA GENERATOR] Created {len(df)} raw expense records at '{output_path}'.")
    return df


if __name__ == "__main__":
    generate_synthetic_expenses()