import os
import sqlite3

import pandas as pd

# File Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
csv_file = os.path.join(BASE_DIR, "data", "transfers.csv")
db_file = os.path.join(BASE_DIR, "src/database" ,"venmito.db")

def load_transfers(filepath):
    """Load transfers.csv into a DataFrame and clean data."""
    df = pd.read_csv(filepath)
    
    # Standardize column names
    df.rename(columns={
        "id": "transfer_id",
        "from": "from_phone",
        "to": "to_phone",
        "amount": "amount",
        "date": "date"
    }, inplace=True)
    
    # Convert date to a consistent format
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    return df

def insert_into_db(df, db_file):
    """Insert cleaned transfers data into SQLite."""
    conn = sqlite3.connect(db_file)
    
    df.to_sql("transfers", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
    print("Transfers data inserted successfully!")

if __name__ == "__main__":
    df = load_transfers(csv_file)
    insert_into_db(df, db_file)
import os
import sqlite3

import pandas as pd

# File Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
csv_file = os.path.join(BASE_DIR, "data", "transfers.csv")
db_file = os.path.join(BASE_DIR, "venmito.db")

def load_transfers(filepath):
    """Load transfers.csv into a DataFrame and clean data."""
    df = pd.read_csv(filepath)
    
    # Standardize column names
    df.rename(columns={
        "id": "transfer_id",
        "from": "from_phone",
        "to": "to_phone",
        "amount": "amount",
        "date": "date"
    }, inplace=True)
    
    # Convert date to a consistent format
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    return df

def insert_into_db(df, db_file):
    """Insert cleaned transfers data into SQLite."""
    conn = sqlite3.connect(db_file)
    
    df.to_sql("transfers", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
    print("Transfers data inserted successfully!")

if __name__ == "__main__":
    df = load_transfers(csv_file)
    insert_into_db(df, db_file)
