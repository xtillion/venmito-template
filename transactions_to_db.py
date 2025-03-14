import sqlite3
import pandas as pd
import xml.etree.ElementTree as ET

def create_transactions_table(transactions_file, output_db="transactions_to_db.db", output_csv="transactions_to_db.csv"):
    """Create a transactions database by parsing transactions.xml and standardizing column names."""
    
    # Parse XML file
    tree = ET.parse(transactions_file)
    root = tree.getroot()
    
    transactions = []
    
    # Extract data from XML
    for transaction in root.findall('transaction'):
        transaction_id = transaction.get('id')
        phone_number = transaction.find('phone').text
        store = transaction.find('store').text
        
        # Extract items
        for item in transaction.find('items').findall('item'):
            item_name = item.find('item').text
            price = float(item.find('price').text)
            price_per_item = float(item.find('price_per_item').text)
            quantity = int(item.find('quantity').text)
            
            transactions.append({
                "transaction_id": transaction_id,
                "phone_number": phone_number,
                "store": store,
                "item": item_name,
                "price": price,
                "price_per_item": price_per_item,
                "quantity": quantity
            })
    
    # Convert to DataFrame
    transactions_df = pd.DataFrame(transactions)
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    transactions_df.to_csv(output_csv, index=False)
    print(f"Transactions table created in '{output_db}' and data exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    create_transactions_table("data/transactions.xml")
