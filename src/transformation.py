import pandas as pd

#DataTransformer class to clean data
class DataTransformer:
    #Transform remove unwanted symbols from phone numbers
    def clean_phone_number(self, phone):
        if isinstance(phone, str):
            return phone.replace('-', '')
        return phone

    def normalize_data(self, df):
        # Clean phone numbers
        df['phone'] = df['phone'].apply(self.clean_phone_number)

        # Standardize column names (convert to lowercase)
        df.columns = df.columns.str.lower()
        return df

    def merge_data(self, df1, df2, on):
        try:
            merged_df = pd.merge(df1, df2, on=on, how='outer')
            return merged_df
        except Exception as e:
            print(f"Error merging data: {e}")
            return None
