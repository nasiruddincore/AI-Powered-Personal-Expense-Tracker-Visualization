"""
SQLite Database Layer for Personal Expense Tracker.
Handles schema creation, deduplicated transaction storage, and budget management.
"""

import os
import sqlite3
import pandas as pd


DEFAULT_DB_PATH = "data/expenses.db"


def init_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialize SQLite tables for transactions and monthly category budgets."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                description TEXT NOT NULL,
                month TEXT NOT NULL,
                UNIQUE(tx_date, category, amount, payment_method, description)
            );

            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                monthly_limit REAL NOT NULL
            );
            """
        )

        # Seed default monthly category budgets if table is empty
        cursor.execute("SELECT COUNT(*) FROM budgets")
        if cursor.fetchone()[0] == 0:
            default_budgets = [
                ("Rent", 12500.0),
                ("Food & Dining", 6500.0),
                ("Groceries", 5500.0),
                ("Transport", 3500.0),
                ("Shopping", 4500.0),
                ("Bills & Utilities", 2500.0),
                ("Entertainment", 2000.0),
                ("Healthcare", 2000.0),
                ("Other", 1500.0),
            ]
            cursor.executemany(
                "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)",
                default_budgets,
            )
        conn.commit()


def save_transactions_to_db(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH) -> int:
    """Insert cleaned transactions into SQLite while ignoring exact duplicates."""
    init_database(db_path)
    inserted = 0
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for row in df.itertuples(index=False):
            cursor.execute(
                """
                INSERT OR IGNORE INTO transactions
                (tx_date, category, amount, payment_method, description, month)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row.Date.strftime("%Y-%m-%d"),
                    row.Category,
                    float(row.Amount),
                    row.Payment_Method,
                    row.Description,
                    row.Month,
                ),
            )
            inserted += cursor.rowcount
        conn.commit()
    return inserted


def add_single_transaction(
    tx_date: str,
    category: str,
    amount: float,
    payment_method: str,
    description: str,
    db_path: str = DEFAULT_DB_PATH,
) -> bool:
    """Insert a single manual transaction from the Streamlit UI."""
    init_database(db_path)
    month_str = pd.to_datetime(tx_date).strftime("%Y-%m")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO transactions
            (tx_date, category, amount, payment_method, description, month)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tx_date, category.strip().title(), float(amount), payment_method.strip(), description.strip(), month_str),
        )
        conn.commit()
        return cursor.rowcount > 0


def load_transactions_from_db(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Fetch all transactions from SQLite as a typed Pandas DataFrame."""
    init_database(db_path)
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            """
            SELECT tx_date AS Date, category AS Category, amount AS Amount,
                   payment_method AS Payment_Method, description AS Description, month AS Month
            FROM transactions
            ORDER BY tx_date ASC
            """,
            conn,
        )
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Day_Name"] = df["Date"].dt.day_name()
    return df


def get_budgets(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Retrieve monthly category budget limits."""
    init_database(db_path)
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT category AS Category, monthly_limit AS Monthly_Limit FROM budgets", conn)


def update_budget(category: str, monthly_limit: float, db_path: str = DEFAULT_DB_PATH) -> None:
    """Update or insert a monthly budget limit for a category."""
    init_database(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit
            """,
            (category, float(monthly_limit)),
        )
        conn.commit()