import os
import sqlite3

import pandas as pd
import yaml

# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Construct the correct paths
json_file = os.path.join(BASE_DIR, "data", "people.json")
yaml_file = os.path.join(BASE_DIR, "data", "people.yml")
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")

def load_json(filepath):
    """Load people.json into a DataFrame"""
    df = pd.read_json(filepath)
    # Flatten location data
    df["city"] = df["location"].apply(lambda x: x["City"])
    df["country"] = df["location"].apply(lambda x: x["Country"])
    df.drop(columns=["location"], inplace=True)
    # Convert devices list to binary flags
    df["Android"] = df["devices"].apply(lambda x: 1 if "Android" in x else 0)
    df["Iphone"] = df["devices"].apply(lambda x: 1 if "Iphone" in x else 0)
    df["Desktop"] = df["devices"].apply(lambda x: 1 if "Desktop" in x else 0)
    df.drop(columns=["devices"], inplace=True)
    return df

def load_yaml(filepath):
    """Load people.yml into a DataFrame"""
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
    df = pd.DataFrame(data)
    # Standardize column names
    df.rename(columns={"name": "full_name", "phone": "telephone", "email": "email"}, inplace=True)
    # Split full_name into first_name and last_name
    df[["first_name", "last_name"]] = df["full_name"].str.split(" ", n=1, expand=True)
    df.drop(columns=["full_name"], inplace=True)
    return df

def merge_and_clean(json_df, yaml_df):
    """Merge the two DataFrames and clean duplicates"""
    # Merge on email and telephone (inner join to remove exact duplicates)
    merged_df = pd.concat([json_df, yaml_df], ignore_index=True)
    merged_df.drop_duplicates(subset=["email", "telephone"], keep="first", inplace=True)
    return merged_df

def insert_into_db(df, db_file):
    """Insert the cleaned people data into SQLite"""
    conn = sqlite3.connect(db_file)
    df.to_sql("people", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print("✅ People data inserted successfully!")

if __name__ == "__main__":
    json_df = load_json(json_file)
    yaml_df = load_yaml(yaml_file)
    cleaned_df = merge_and_clean(json_df, yaml_df)
    insert_into_db(cleaned_df, db_file)
