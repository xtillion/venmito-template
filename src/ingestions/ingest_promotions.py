import os
import sqlite3

import pandas as pd

# File Paths
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Construct the correct paths
csv_file = os.path.join(BASE_DIR, "data", "promotions.csv")
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")


def load_promotions(filepath):
    """Load promotions.csv into a DataFrame and clean data."""
    df = pd.read_csv(filepath)

# Debugging: Print column names to see what exists
    print("Columns in CSV:", df.columns)

    
    # Standardize column names
    df.rename(columns={
        "id": "promotion_id",
        "client_email": "email",
        "promotion": "promotion_type",
        "responded": "accepted"
    }, inplace=True)
    
    # Normalize accepted values (ensure 'Yes' or 'No')
    df["accepted"] = df["accepted"].str.strip().str.capitalize()
    df["accepted"] = df["accepted"].apply(lambda x: "No" if x not in ["Yes", "No"] else x)
    
    return df

def insert_into_db(df, db_file):
    """Insert cleaned promotions data into SQLite."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Ensure emails exist in people table before inserting
    cursor.execute("SELECT email FROM people")
    valid_emails = set(row[0] for row in cursor.fetchall())
    
    df = df[df["email"].isin(valid_emails)]  # Filter out promotions for non-existent users
    
    df.to_sql("promotions", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print("Promotions data inserted successfully!")

if __name__ == "__main__":
    df = load_promotions(csv_file)
    insert_into_db(df, db_file)
