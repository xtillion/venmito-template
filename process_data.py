import os
import time
import json
import pandas as pd
import yaml
import xmltodict
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Database connection (from docker-compose.yml environment variables)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin_pass@db:5432/venmito_db")

# Wait for the database to be ready (retry loop)
max_retries = 10
for i in range(max_retries):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready!")
        break
    except Exception as e:
        print(f"Database not ready, retrying... ({i+1}/{max_retries})")
        time.sleep(5)
else:
    raise Exception("Database not ready after several retries")

# File paths
DATA_DIR = "/app/data/"
FILES = {
    "people_json": os.path.join(DATA_DIR, "people.json"),
    "people_yml": os.path.join(DATA_DIR, "people.yml"),
    "transfers_csv": os.path.join(DATA_DIR, "transfers.csv"),
    "transactions_xml": os.path.join(DATA_DIR, "transactions.xml"),
    "promotions_csv": os.path.join(DATA_DIR, "promotions.csv")
}

# -------------------------
# Data Reading Functions
# -------------------------
def read_json(file_path):
    with open(file_path, "r") as f:
        return pd.DataFrame(json.load(f))

def read_yaml(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        return pd.DataFrame(data)

def read_csv(file_path):
    return pd.read_csv(file_path)

def read_xml_transactions(file_path):
    with open(file_path, "r") as f:
        data_dict = xmltodict.parse(f.read())
        # Expect structure: <transactions><transaction @id="...">...</transaction></transactions>
        records = data_dict["transactions"]["transaction"]
        if not isinstance(records, list):
            records = [records]
        for record in records:
            # Convert '@id' attribute to 'id'
            if "@id" in record:
                record["id"] = record["@id"]
                del record["@id"]
        return records

# -------------------------
# 1) Process People Data (JSON + YAML)
# -------------------------
df_people_json = read_json(FILES["people_json"])
df_people_yml = read_yaml(FILES["people_yml"])

# Process JSON: Convert 'devices' list into boolean columns
if "devices" in df_people_json.columns:
    df_people_json["Android"] = df_people_json["devices"].apply(lambda x: True if isinstance(x, list) and "Android" in x else False)
    df_people_json["Iphone"]  = df_people_json["devices"].apply(lambda x: True if isinstance(x, list) and "Iphone" in x else False)
    df_people_json["Desktop"] = df_people_json["devices"].apply(lambda x: True if isinstance(x, list) and "Desktop" in x else False)
    df_people_json.drop(columns=["devices"], inplace=True)

# Flatten location dictionary for JSON
if "location" in df_people_json.columns:
    df_people_json["city"] = df_people_json["location"].apply(lambda x: x.get("City") if isinstance(x, dict) else None)
    df_people_json["country"] = df_people_json["location"].apply(lambda x: x.get("Country") if isinstance(x, dict) else None)
    df_people_json.drop(columns=["location"], inplace=True)

# Rename 'telephone' to 'phone'
if "telephone" in df_people_json.columns:
    df_people_json.rename(columns={"telephone": "phone"}, inplace=True)

# Process YAML: Split 'city' if it contains a comma into 'city' and 'country'
if "city" in df_people_yml.columns:
    split_df = df_people_yml["city"].str.split(",", n=1, expand=True)
    if split_df.shape[1] == 2:
        df_people_yml["city"] = split_df[0].str.strip()
        df_people_yml["country"] = split_df[1].str.strip()
    else:
        df_people_yml["country"] = None

# Merge People Data and drop duplicate emails
df_people = pd.concat([df_people_json, df_people_yml], ignore_index=True)
df_people = df_people.drop_duplicates(subset=["email"], keep="first")
if "telephone" in df_people.columns:
    df_people.rename(columns={"telephone": "phone"}, inplace=True)
expected_cols_people = {"id", "first_name", "last_name", "email", "phone", "city", "country", "Android", "Desktop", "Iphone"}
df_people = df_people[[col for col in df_people.columns if col in expected_cols_people]]
for col in ["Android", "Desktop", "Iphone"]:
    if col in df_people.columns:
        df_people[col] = df_people[col].astype(bool)

# -------------------------
# 2) Load Transfers Data
# -------------------------
df_transfers = read_csv(FILES["transfers_csv"])

# -------------------------
# 3) Load Promotions Data
# -------------------------
df_promotions = read_csv(FILES["promotions_csv"])
expected_cols_promotions = ["id", "client_email", "telephone", "promotion", "responded"]
for col in expected_cols_promotions:
    if col not in df_promotions.columns:
        df_promotions[col] = None
df_promotions = df_promotions[expected_cols_promotions]

# -------------------------
# 4) Process Transactions Data and Split Items
# -------------------------
xml_records = read_xml_transactions(FILES["transactions_xml"])

transactions_list = []
items_list = []

for record in xml_records:
    # Extract transaction-level fields
    txn_id = record.get("id")
    phone = record.get("phone")
    store = record.get("store")
    
    transactions_list.append({
        "id": txn_id,
        "phone": phone,
        "store": store
    })
    
     # Extract item-level fields from the 'items' element
    items_block = record.get("items")
    if items_block:
        item_nodes = items_block.get("item", [])
        if not isinstance(item_nodes, list):
            item_nodes = [item_nodes]
        for node in item_nodes:
            item_name = node.get("item")
            price = node.get("price")
            price_per_item = node.get("price_per_item")
            quantity = node.get("quantity")
            items_list.append({
                "transaction_id": txn_id,
                "item_name": item_name,
                "price": price,
                "price_per_item": price_per_item,
                "quantity": quantity
            })

df_transactions = pd.DataFrame(transactions_list)
df_transaction_items = pd.DataFrame(items_list)

# -------------------------
# Insert Data into PostgreSQL
# -------------------------
df_people.to_sql("clients", engine, if_exists="append", index=False)
df_transfers.to_sql("transfers", engine, if_exists="replace", index=False)
df_promotions.to_sql("promotions", engine, if_exists="replace", index=False)
df_transactions.to_sql("transactions", engine, if_exists="append", index=False)
df_transaction_items.to_sql("transaction_items", engine, if_exists="replace", index=False)

print("✅ Data successfully ingested into PostgreSQL!")