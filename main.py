import numpy as np
import pandas as pd
import json
import yaml

def data_parser (file_path):
    file_type = str(file_path.split('.')[-1])
    match file_type:
        case "json":
            return pd.read_json(file_path)
        case "yml":
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                return pd.DataFrame(data)
        case "csv":
            return pd.read_csv(file_path)
        case "xml":
            return pd.read_xml(file_path)
        case _:
            return "File type not supported (supported types: json, yml, csv, xml)"

ppl_json = data_parser("data/people.json")

# Cleaning Up People Json

# ppl_json.isna().sum() = results show that there are no missing values
# ppl_yml = data_parser("data/people.yml")
# promo_csv = data_parser("data/promotions.csv")
# transaction_csv = data_parser("data/transactions.xml")
# transfer_csv = data_parser("data/transfers.csv")

