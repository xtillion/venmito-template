import os
import sqlite3

import pandas as pd

# File Paths
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Construct the correct paths
csv_file = os.path.join(BASE_DIR, "data", "promotions.csv")
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")

def clean_csv(file_path):
    """Load CSV, normalize data, and ensure missing fields are replaced with empty strings."""
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)  # Keep all data
    
    # Ensure proper column structure
    expected_columns = ["id", "client_email","telephone", "promotion", "responded"]
    
    # Handle extra columns if they exist
    if len(df.columns) > len(expected_columns):
        df = df.iloc[:, :len(expected_columns)]
    
    # Assign correct column names
    df.columns = expected_columns
    
    # Strip whitespace and normalize data
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else "")
    
    return df

def insert_into_db(df, db_path):
    """Insert cleaned data into SQLite database without dropping any rows."""
    conn = sqlite3.connect(db_path)
    df.to_sql("promotions", conn, if_exists="replace", index=False)
    print("✅ Promotions data inserted successfully!")
    conn.close()

if __name__ == "__main__":
    df_cleaned = clean_csv(csv_file)
    insert_into_db(df_cleaned, db_file)
