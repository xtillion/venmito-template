import json
import yaml
import csv
import sqlite3
import xml.etree.ElementTree as ET

def create_database():
    """Create SQLite database and tables."""
    conn = sqlite3.connect("venmito.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transfers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id TEXT,
        receiver_id TEXT,
        amount REAL,
        date TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT,
        store TEXT,
        item TEXT,
        price REAL,
        date TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promotions (
        client_id TEXT,
        promotion TEXT,
        accepted TEXT
    )""")
    
    conn.commit()
    conn.close()

def load_json(file_path):
    """Load data from JSON."""
    with open(file_path, 'r') as f:
        return json.load(f)

def load_yaml(file_path):
    """Load data from YAML."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_csv(file_path):
    """Load data from CSV."""
    with open(file_path, 'r') as f:
        return list(csv.DictReader(f))

def load_xml(file_path):
    """Load data from XML."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []
    for trans in root.findall("transaction"):
        transactions.append({
            "client_id": trans.find("client_id").text,
            "store": trans.find("store").text,
            "item": trans.find("item").text,
            "price": float(trans.find("price").text),
            "date": trans.find("date").text
        })
    return transactions

def insert_data():
    """Insert data into the database."""
    conn = sqlite3.connect("venmito.db")
    cursor = conn.cursor()
    
    # Load data
    people = load_json("people.json") + load_yaml("people.yml")
    transfers = load_csv("transfers.csv")
    transactions = load_xml("transactions.xml")
    promotions = load_csv("promotions.csv")
    
    # Insert people
    for person in people:
        cursor.execute("INSERT OR IGNORE INTO people VALUES (?, ?, ?)", (person['id'], person['name'], person['email']))
    
    # Insert transfers
    for transfer in transfers:
        cursor.execute("INSERT INTO transfers (sender_id, receiver_id, amount, date) VALUES (?, ?, ?, ?)",
                       (transfer['sender_id'], transfer['receiver_id'], transfer['amount'], transfer['date']))
    
    # Insert transactions
    for transaction in transactions:
        cursor.execute("INSERT INTO transactions (client_id, store, item, price, date) VALUES (?, ?, ?, ?, ?)",
                       (transaction['client_id'], transaction['store'], transaction['item'], transaction['price'], transaction['date']))
    
    # Insert promotions
    for promo in promotions:
        cursor.execute("INSERT INTO promotions (client_id, promotion, accepted) VALUES (?, ?, ?)",
                       (promo['client_id'], promo['promotion'], promo['accepted']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    insert_data()
    print("Database setup complete!")
