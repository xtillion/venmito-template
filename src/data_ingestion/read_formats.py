import pandas as pd
import json
import yaml
import xml.etree.ElementTree as ET

# Read JSON file
def read_json(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)

# Read YAML file
def read_yaml(filepath):
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
    return pd.DataFrame(data)

# Read CSV file
def read_csv(filepath):
    return pd.read_csv(filepath)

# Read XML file
def read_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    transactions = []
    transaction_items = []  # For separate item storage

    for transaction in root.findall("transaction"):
        transaction_id = transaction.get("id")  # Extract from XML attribute
        store = transaction.find("store").text if transaction.find("store") is not None else None
        client_id = transaction.find("phone").text if transaction.find("phone") is not None else None
        timestamp = transaction.find("timestamp").text if transaction.find("timestamp") is not None else None
        
        # Create transaction entry (ignoring item details for now)
        transactions.append({
            "transaction_id": transaction_id,
            "client_id": client_id,
            "store": store,
            "timestamp": timestamp
        })
        
        # Extract each item separately
        items = transaction.findall(".//item")
        for item in items:
            item_name = item.find("item").text if item.find("item") is not None else None
            price = float(item.find("price").text) if item.find("price") is not None else None
            price_per_item = float(item.find("price_per_item").text) if item.find("price_per_item") is not None else None
            quantity = int(item.find("quantity").text) if item.find("quantity") is not None else None

            transaction_items.append({
                "transaction_id": transaction_id,
                "item_name": item_name,
                "price": price,
                "price_per_item": price_per_item,
                "quantity": quantity
            })

    transactions_df = pd.DataFrame(transactions)
    items_df = pd.DataFrame(transaction_items)

    return transactions_df, items_df  # Return both tables separately