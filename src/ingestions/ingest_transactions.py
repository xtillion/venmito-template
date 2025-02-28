import sqlite3

import pandas as pd
import xmltodict

# File Paths
xml_file = "transactions.xml"
db_file = "venmito.db"

def load_transactions(filepath):
    """Load transactions.xml and extract transaction & item data."""
    with open(filepath, "r") as file:
        data = xmltodict.parse(file.read())
    
    transactions_list = []
    transaction_items_list = []
    
    for transaction in data["transactions"]["transaction"]:
        transaction_id = int(transaction["@id"])
        phone = transaction["phone"]
        store = transaction["store"]
        
        # Store transaction-level data
        transactions_list.append((transaction_id, phone, store))
        
        # Extract item details
        for item in transaction["items"]["item"]:
            item_name = item["item"]
            quantity = int(item["quantity"])
            price_per_item = float(item["price_per_item"])
            total_price = float(item["price"])
            transaction_items_list.append((transaction_id, item_name, quantity, price_per_item, total_price))
    
    return transactions_list, transaction_items_list

def insert_into_db(transactions, transaction_items, db_file):
    """Insert cleaned transactions and items into SQLite"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Insert transactions
    cursor.executemany("""
        INSERT INTO transactions (transaction_id, phone, store)
        VALUES (?, ?, ?)""", transactions)
    
    # Insert transaction items
    cursor.executemany("""
        INSERT INTO transaction_items (transaction_id, item_name, quantity, price_per_item, total_price)
        VALUES (?, ?, ?, ?, ?)""", transaction_items)
    
    conn.commit()
    conn.close()
    print("Transactions data inserted successfully!")

if __name__ == "__main__":
    transactions, transaction_items = load_transactions(xml_file)
    insert_into_db(transactions, transaction_items, db_file)
