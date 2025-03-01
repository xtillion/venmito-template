import os
import sqlite3
from io import StringIO

import pandas as pd
from lxml import etree

# File Paths
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Construct the correct paths
xml_file = os.path.join(BASE_DIR, "data", "transactions.xml")
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")

def load_transactions(filepath):
    """Load transactions.xml using lxml and pandas."""
    tree = etree.parse(filepath)
    root = tree.getroot()
    
    transactions_list = []
    items_list = []
    
    for transaction in root.findall("transaction"):
        transaction_id = int(transaction.get("id"))
        phone = transaction.find("phone").text
        store = transaction.find("store").text
        transactions_list.append((transaction_id, phone, store))
        
        for item in transaction.find("items").findall("item"):
            item_name = item.find("item").text
            quantity = int(item.find("quantity").text)
            price_per_item = float(item.find("price_per_item").text)
            total_price = float(item.find("price").text)
            items_list.append((transaction_id, item_name, quantity, price_per_item, total_price))
    
    transactions_df = pd.DataFrame(transactions_list, columns=["transaction_id", "phone", "store"])
    transaction_items_df = pd.DataFrame(items_list, columns=["transaction_id", "item_name", "quantity", "price_per_item", "total_price"])
    
    return transactions_df, transaction_items_df

def insert_into_db(transactions, transaction_items, db_file):
    """Insert cleaned transactions and items into SQLite"""
    conn = sqlite3.connect(db_file)
    
    transactions.to_sql("transactions", conn, if_exists="append", index=False)
    transaction_items.to_sql("transaction_items", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
    print("Transactions data inserted successfully!")

if __name__ == "__main__":
    transactions_df, transaction_items_df = load_transactions(xml_file)
    insert_into_db(transactions_df, transaction_items_df, db_file)
