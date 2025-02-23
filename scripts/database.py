import os
import sys
import sqlite3
import pandas as pd

# Ensure script can access other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.clean_data import get_cleaned_data

DATABASE_PATH = "data/venmito_data.sqlite"

def save_to_db():
    """Save cleaned data to SQLite database."""
    # Load cleaned data
    df_merged = get_cleaned_data()

    # Convert data types for SQLite compatibility
    df_merged["Client_ID"] = df_merged["Client_ID"].astype(int)
    df_merged["Amount_USD"] = df_merged["Amount_USD"].astype(float)
    df_merged["Transfer_Amount"] = df_merged["Transfer_Amount"].astype(float)
    df_merged["Transfer_Date"] = pd.to_datetime(df_merged["Transfer_Date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Connect to SQLite
    conn = sqlite3.connect(DATABASE_PATH)

    # Save data to SQLite table
    df_merged.to_sql("clients", conn, if_exists="replace", index=False, dtype={
        "Client_ID": "INTEGER",
        "First_Name": "TEXT",
        "Last_Name": "TEXT",
        "Phone": "TEXT",
        "email": "TEXT",
        "Transfer_Amount": "REAL",
        "Transfer_Date": "TEXT",
        "Promotion_ID": "INTEGER",
        "promotion": "TEXT",
        "responded": "TEXT",
        "Transaction_ID": "INTEGER",
        "Amount_USD": "REAL",
        "Store": "TEXT"
    })

    conn.close()
    print("✅ Data saved to SQLite successfully!")

def query_db(query):
    """Query SQLite database and return results as a Pandas DataFrame."""
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Run script to save data when executed directly
if __name__ == "__main__":
    save_to_db()