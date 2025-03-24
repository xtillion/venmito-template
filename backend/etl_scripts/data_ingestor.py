import xml.etree.ElementTree as ET

import pandas as pd
import yaml

from backend.utils.logger import configure_logging

logger = configure_logging()

def ingest_data_from_file(filepath: str):
    if filepath.__contains__('.csv'):
        logger.info('Ingesting data from csv file')
        df_csv = pd.read_csv(filepath)
        return df_csv
    elif filepath.__contains__('.json'):
        logger.info('Ingesting data from json file')
        df_json = pd.read_json(filepath)
        return df_json
    elif filepath.__contains__('.xml'):
        logger.info('Ingesting data from xml file')
        df_xml = parse_xml(filepath)
        return df_xml
    elif filepath.__contains__('.yml'):
        logger.info('Ingesting data from yml file')
        with open(filepath, 'r', encoding='utf-8') as f:
            df_yml = yaml.safe_load(f)

        cleaned_df_yaml = clean_strings(df_yml)
        cleaned_df_yaml = pd.DataFrame(cleaned_df_yaml)
        return cleaned_df_yaml

def clean_strings(obj):
    if isinstance(obj, dict):
        return {k: clean_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_strings(i) for i in obj]
    elif isinstance(obj, str):
        return obj.strip('"').strip("'")  # Removes extra quotes
    return obj

def parse_xml(filepath: str):
    tree = ET.parse(filepath)
    root = tree.getroot()

    children = []
    for transaction in root.findall('transaction'):
        transaction_id = transaction.get('id')
        telephone = transaction.find('phone').text
        store = transaction.find('store').text
        date = transaction.find('date').text

        # Flatten the items_item structure to make data easier to manipulate
        for item in transaction.find('items').findall('item'):
            item_name = item.find('item').text
            total_price = float(item.find('price').text)
            price_per_item = float(item.find('price_per_item').text)
            quantity = int(item.find('quantity').text)

            children.append({
                'transaction_id': transaction_id,
                'telephone': telephone,
                'store': store,
                'item_name': item_name,
                'total_price': total_price,
                'price_per_item': price_per_item,
                'quantity': quantity,
                'date': date
            })

    return pd.DataFrame(children)