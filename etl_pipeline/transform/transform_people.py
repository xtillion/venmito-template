import pandas as pd
from etl_pipeline.extract.extract_json import extract_json
from etl_pipeline.extract.extract_yaml import extract_yaml

class People:
    def __init__(self, json_filepath, yaml_filepath):
        """Initializes the People class by merging data from JSON and YAML sources."""
        self.data = self.merge_data(json_filepath, yaml_filepath)

    def convert_json_to_pandas(self, json_df):
        """Cleans and transforms JSON people data."""
        if json_df.empty:
            return json_df  # Return empty DataFrame if no data

        # Standardizing column names (handling case sensitivity)
        json_df.columns = json_df.columns.str.lower()

        # Ensure correct renaming
        rename_mapping = {
            'location.city': 'city',
            'location.country': 'country'
        }
        json_df.rename(columns=rename_mapping, inplace=True)

        # Convert ID column to integer
        if 'id' in json_df.columns:
            json_df['id'] = json_df['id'].astype(int)

        return json_df

    def convert_yaml_to_pandas(self, yaml_df):  
        """Cleans and transforms YAML people data."""
        if yaml_df.empty:
            return yaml_df  # If no data, return empty DataFrame

        # Standardizing column names
        yaml_df.columns = yaml_df.columns.str.lower()

        # Splitting 'name' into 'first_name' and 'last_name'
        if 'name' in yaml_df.columns:
            name_df = yaml_df['name'].str.split(' ', n=1, expand=True)
            yaml_df['first_name'] = name_df[0]
            yaml_df['last_name'] = name_df[1].fillna('')

        # Splitting 'city' into 'city' and 'country'
        if 'city' in yaml_df.columns:
            city_df = yaml_df['city'].str.split(', ', n=1, expand=True)
            yaml_df['city'] = city_df[0]
            yaml_df['country'] = city_df[1].fillna('')

        # Handling device columns
        device_columns = ["Iphone", "Android", "Desktop"]

        def extract_devices(row):
            devices = []
            for device in device_columns:
                if row.get(device.lower(), 0) == 1:
                    devices.append(device)
            return devices

        yaml_df['devices'] = yaml_df.apply(extract_devices, axis=1)

        # Renaming columns
        yaml_df.rename(columns={'phone': 'telephone'}, inplace=True)

        # Drop unnecessary columns safely
        yaml_df.drop(columns=device_columns + ['name'] + [device.lower() for device in device_columns], errors='ignore', inplace=True)

        return yaml_df

    def merge_data(self, json_filepath, yaml_filepath):
        json_data = extract_json(json_filepath)
        yaml_data = extract_yaml(yaml_filepath)

        # Convert to DataFrame safely
        json_df = pd.json_normalize(json_data, sep=".") if json_data else pd.DataFrame()
        yaml_df = pd.json_normalize(yaml_data, sep=".") if yaml_data else pd.DataFrame()
        
        converted_json_df = self.convert_json_to_pandas(json_df)
        converted_yaml_df = self.convert_yaml_to_pandas(yaml_df)

        # Merge datasets
        combined_df = pd.concat([converted_json_df, converted_yaml_df], ignore_index=True)
        combined_df = combined_df.sort_values(by='id').drop_duplicates(subset='id')

        combined_df.rename(columns={'id': 'person_id'}, inplace=True)

        return combined_df
