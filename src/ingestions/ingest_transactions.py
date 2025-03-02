import os
import sqlite3
import xml.etree.ElementTree as ET

import pandas as pd

# File Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
xml_file = os.path.join(BASE_DIR, "data", "transactions.xml")
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")

import sqlite3
import xml.etree.ElementTree as ET

import pandas as pd


def load_transactions(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()  # <transactions> is the root
    
    transactions_data = []       # will become transactions_df
    transaction_items_data = []  # will become transaction_items_df

    for trans_el in root.findall('transaction'):
        # Extract transaction fields
        t_id = int(trans_el.get('id', 0))
        phone_el = trans_el.find('phone')
        store_el = trans_el.find('store')
        phone = phone_el.text if phone_el is not None else ""
        store = store_el.text if store_el is not None else ""

        # Build up transaction total
        transaction_total = 0.0

        items_el = trans_el.find('items')
        if items_el is not None:
            for item_el in items_el.findall('item'):
                item_name_el = item_el.find('item')
                qty_el = item_el.find('quantity')
                ppi_el = item_el.find('price_per_item')
                price_el = item_el.find('price')
                
                item_name = item_name_el.text if item_name_el is not None else ""
                quantity = int(qty_el.text) if qty_el is not None else 0
                price_per_item = float(ppi_el.text) if ppi_el is not None else 0.0
                item_total_price = float(price_el.text) if price_el is not None else 0.0

                # Append to items data
                transaction_items_data.append([
                    t_id, item_name, quantity, price_per_item, item_total_price
                ])

                # Aggregate item total into the transaction total
                transaction_total += item_total_price

        # Add transaction row
        transactions_data.append([t_id, phone, store, transaction_total])

    # Create DataFrames
    transactions_df = pd.DataFrame(transactions_data, columns=[
        'transaction_id', 'phone', 'store', 'total_price'
    ])
    transaction_items_df = pd.DataFrame(transaction_items_data, columns=[
        'transaction_id', 'item_name', 'quantity', 'price_per_item', 'total_price'
    ])

    return transactions_df, transaction_items_df

def insert_into_db(transactions_df, transaction_items_df, db_path):
    """Insert transactions and transaction items into the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Ensure foreign key constraints are enforced
    
    # Insert DataFrames into their respective tables
    transactions_df.to_sql("transactions", conn, if_exists="append", index=False)
    transaction_items_df.to_sql("transaction_items", conn, if_exists="append", index=False)
    print("✅ Transactions and transaction items inserted successfully!")   
    conn.close()

if __name__ == "__main__":
    # Load transactions and transaction items
    transactions_df, transaction_items_df = load_transactions(xml_file)
    
    # Insert them into the database
    insert_into_db(transactions_df, transaction_items_df, db_file)

