import json
import yaml
import pandas as pd
import xmltodict
import argparse
import os
import shutil

from models.database import get_engine
from models.promotion import Promotion
from models.item import Item
from models.transaction import Transaction
from models.transfer import Transfer
from models.person import Person

class DataImporter:
    def __init__(self, directory, engine):
        self.directory = directory
        self.engine = engine
        self.processed_dir = os.path.join(directory, 'processed')

        # Create the processed directory if it doesn't exist
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return None

    def read_yaml(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            return data
        except Exception as e:
            print(f"Error reading YAML file {file_path}: {e}")
            return None

    def read_csv(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            print(f"Error reading CSV file {file_path}: {e}")
            return None

    def read_xml(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = xmltodict.parse(file.read())
            return data
        except Exception as e:
            print(f"Error reading XML file {file_path}: {e}")
            return None

    def parse_people(self, data, file_type):
        try:
            for entry in data:
                if file_type == 'json':
                    person = Person(
                        id=entry.get('id'),
                        first_name=entry.get('first_name') or None,
                        last_name=entry.get('last_name') or None,
                        telephone=entry.get('telephone') or None,
                        email=entry.get('email') or None,
                        android=1 if 'Android' in entry.get('devices', []) else 0,
                        desktop=1 if 'Desktop' in entry.get('devices', []) else 0,
                        iphone=1 if 'Iphone' in entry.get('devices', []) else 0,
                        city=entry.get('location', {}).get('City') or None,
                        country=entry.get('location', {}).get('Country') or None
                    )
                elif file_type == 'yaml':
                    name_parts = entry.get('name', '').split()
                    person = Person(
                        id=entry.get('id'),
                        first_name=name_parts[0] if name_parts else None,
                        last_name=name_parts[-1] if len(name_parts) > 1 else None,
                        telephone=entry.get('phone') or None,
                        email=entry.get('email') or None,
                        android=entry.get('Android', 0),
                        desktop=entry.get('Desktop', 0),
                        iphone=entry.get('Iphone', 0),
                        city=entry.get('city', '').split(',')[0] or None,
                        country=entry.get('city', '').split(',')[-1].strip() or None
                    )
                Person.insert_person(self.engine, person)
        except Exception as e:
            print(f"Error parsing people data: {e}")

    def parse_promotions(self, data):
        try:
            for _, row in data.iterrows():
                promotion = Promotion(
                    id=row['id'],
                    client_email=row['client_email'] if pd.notna(row['client_email']) else None,
                    telephone=row['telephone'] if pd.notna(row['telephone']) else None,
                    promotion=row['promotion'],
                    responded=row['responded']
                )
                Promotion.insert_promotion(self.engine, promotion)
        except Exception as e:
            print(f"Error parsing promotions data: {e}")

    def parse_transactions(self, data):
        try:
            transactions_data = data.get('transactions', {}).get('transaction', [])
            if not isinstance(transactions_data, list):
                transactions_data = [transactions_data]  # Ensure it's a list

            for transaction in transactions_data:
                transaction_obj = Transaction(
                    id=transaction.get('@id'),
                    phone=transaction.get('phone'),
                    store=transaction.get('store')
                )
                Transaction.insert_transaction(self.engine, transaction_obj)

                items_data = transaction.get('items', {}).get('item', [])
                if not isinstance(items_data, list):
                    items_data = [items_data]  # Ensure it's a list

                for item in items_data:
                    item_obj = Item(
                        transaction_id=transaction_obj.id,
                        item_name=item.get('item'),
                        price=float(item.get('price', 0)),
                        price_per_item=float(item.get('price_per_item', 0)),
                        quantity=int(item.get('quantity', 0))
                    )
                    Item.insert_item(self.engine, item_obj)
        except Exception as e:
            print(f"Error parsing transactions data: {e}")

    def parse_transfers(self, data):
        try:
            for _, row in data.iterrows():
                transfer = Transfer(
                    sender_id=row['sender_id'] if pd.notna(row['sender_id']) else None,
                    recipient_id=row['recipient_id'] if pd.notna(row['recipient_id']) else None,
                    amount=row['amount'] if pd.notna(row['amount']) else None,
                    date=row['date'] if pd.notna(row['date']) else None
                )
                Transfer.insert_transfer(self.engine, transfer)
        except Exception as e:
            print(f"Error parsing transfers data: {e}")

    def import_data(self):
        if not os.path.isdir(self.directory):
            print(f"Error: {self.directory} is not a valid directory.")
            return

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)

            # Ensure file_path is a file, not a directory
            if not os.path.isfile(file_path):
                continue

            print("--------------------------------")

            if filename.startswith('people'):
                if filename.endswith('.json'):
                    data = self.read_json(file_path)
                    if data:
                        self.parse_people(data, 'json')
                elif filename.endswith('.yml') or filename.endswith('.yaml'):
                    data = self.read_yaml(file_path)
                    if data:
                        self.parse_people(data, 'yaml')
                else:
                    print(f"Skipping unsupported file type: {filename}")
                    continue
            elif filename.startswith('promotions') and filename.endswith('.csv'):
                data = self.read_csv(file_path)
                if data is not None:
                    self.parse_promotions(data)
            if filename.startswith('transactions') and filename.endswith('.xml'):
                data = self.read_xml(file_path)
                if data:
                    self.parse_transactions(data)
            elif filename.startswith('transfers') and filename.endswith('.csv'):
                data = self.read_csv(file_path)
                if data is not None:
                    self.parse_transfers(data)
            else:
                print(f"Skipping unsupported file type: {filename}")

            # Debugging: Print paths before moving
            processed_path = os.path.join(self.processed_dir, filename)
            print(f"Moving {file_path} to {processed_path}")

            # Move the processed file to the 'processed' directory
            try:
                shutil.move(file_path, processed_path)
                print(f"Moved {filename} to {self.processed_dir}")
            except Exception as e:
                print(f"Error moving file {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Data Importer for Venmito")
    parser.add_argument('directory', type=str, help='Directory containing data files')
    parser.add_argument('--user', type=str, required=True, help='Database username')
    parser.add_argument('--password', type=str, required=True, help='Database password')
    parser.add_argument('--host', type=str, default='localhost', help='Database host')
    parser.add_argument('--port', type=str, default='5432', help='Database port')
    parser.add_argument('--db', type=str, required=True, help='Database name')

    args = parser.parse_args()

    # Database connection setup
    engine = get_engine(args.user, args.password, args.host, args.port, args.db)

    importer = DataImporter(args.directory, engine)
    importer.import_data()

if __name__ == "__main__":
    main() 