import pandas as pd
import yaml
import json
import xml.etree.ElementTree as ET

def load_all_data():
    """Loads data from different file formats into Pandas DataFrames."""

    # Load JSON File
    with open("data/people.json", "r") as f:
        people_data = json.load(f)
    df_people_json = pd.DataFrame(people_data)

    # Load YAML File
    with open("data/people.yml", "r") as f:
        people_yaml_data = yaml.safe_load(f)
    df_people_yaml = pd.DataFrame(people_yaml_data)

    # Load CSV Files
    df_transfers = pd.read_csv("data/transfers.csv")
    df_promotions = pd.read_csv("data/promotions.csv")

    # Load XML File
    tree = ET.parse("data/transactions.xml")
    root = tree.getroot()

    data = []
    for transaction in root.findall("transaction"):
        transaction_id = transaction.get("id")
        store = transaction.find("store").text if transaction.find("store") is not None else None
        phone = transaction.find("phone").text if transaction.find("phone") is not None else None

        total_amount = sum(
            float(item.text) if item.text is not None else 0 for item in transaction.findall(".//item/price")
        )

        data.append({
            "Transaction_ID": transaction_id,
            "Amount_USD": total_amount,
            "Store": store if store else "No Store",
            "Phone": phone if phone else "Unknown"
        })

    df_transactions = pd.DataFrame(data)

    return df_people_json, df_people_yaml, df_transfers, df_promotions, df_transactions

# Run the script to check the data
if __name__ == "__main__":
    load_all_data()