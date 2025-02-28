import json
import os
import sqlite3

import pandas as pd
import yaml

# File Paths
base_path_data = os.path.abspath("data")
base_path_db = os.path.abspath("data")
json_file = os.path.join(base_path_data, "people.json")
yaml_file = os.path.join(base_path_data, "people.yml")
db_file = os.path.join(base_path_db, "venmito.db")


def load_json(filepath):
    """Load people.json using the built-in json module instead of pandas."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)
    # Flatten location data
    df["city"] = df["location"].apply(lambda x: x["City"])
    df["country"] = df["location"].apply(lambda x: x["Country"])
    df.drop(columns=["location"], inplace=True)
    # Convert devices list to binary flags
    df["android"] = df["devices"].apply(lambda x: 1 if "Android" in x else 0)
    df["iphone"] = df["devices"].apply(lambda x: 1 if "Iphone" in x else 0)
    df["desktop"] = df["devices"].apply(lambda x: 1 if "Desktop" in x else 0)
    df.drop(columns=["devices"], inplace=True)
    return df

def load_yaml(filepath):
    """Load people.yml into a DataFrame"""
    with open(filepath, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    df = pd.DataFrame(data)
    # Standardize column names
    df.rename(columns={"name": "full_name", "phone": "telephone", "email": "email"}, inplace=True)
    # Split full_name into first_name and last_name
    df[["first_name", "last_name"]] = df["full_name"].str.split(" ", 1, expand=True)
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
    print("People data inserted successfully!")

if __name__ == "__main__":
    json_df = load_json(json_file)
    yaml_df = load_yaml(yaml_file)
    cleaned_df = merge_and_clean(json_df, yaml_df)
    insert_into_db(cleaned_df, db_file)
