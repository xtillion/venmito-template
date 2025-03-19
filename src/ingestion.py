import pandas as pd
import yaml
import xmltodict

class DataLoader:
    #Manages data extraction of json file
    def load_json(self, file_path):
        try:
            return pd.read_json(file_path)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None

    #Manages data extraction of yaml file
    def load_yaml(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                return pd.json_normalize(data)
        except Exception as e:
            print(f"Error loading YAML: {e}")
            return None

    #Manages data extraction of csv file
    def load_csv(self, file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

    #Manages data extraction of xml file
    def load_xml(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = xmltodict.parse(file.read())
                return pd.json_normalize(data['transactions']['transaction'])
        except Exception as e:
            print(f"Error loading XML: {e}")
            return None
