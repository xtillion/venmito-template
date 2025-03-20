import pandas as pd

class DataTransformer:
    def __init__(self):
        self.client_map = {}  # Map keeps track of unique clients that either share a phone or email

    # Clean phone numbers for match
    def clean_phone_number(self, phone):
        if isinstance(phone, str):
            return phone.replace('-', '').replace(' ', '')
        return phone

    # Clean column names to match
    def normalize_data(self, df):
        if df is not None:
            df['phone'] = df['phone'].apply(self.clean_phone_number)
            df.columns = df.columns.str.lower()
            return df
        return None

    # Remove or merge duplicates and fill missing data
    def clean_and_fix_data(self, df):
        if df is None:
            return None

        # This cleans duplicates by merging records with duplicate data

        # Firstly, group by phone and email
        if 'phone' in df.columns and 'email' in df.columns:
            df = df.groupby(['phone', 'email']).agg({
                'name': 'first',  # Prefer the first non-null value
                'city': 'first',
                'date': 'first',
                'amount': 'sum',  # Sum transaction values if applicable
                'promotion_type': 'first'
            }).reset_index()

        # Then fill missing fields with available data from other sources
        df['email'].fillna('unknown@example.com', inplace=True)
        df['phone'].fillna('0000000000', inplace=True)
        df['name'].fillna('Unknown', inplace=True)
        df['city'].fillna('Unknown City', inplace=True)

        # Now convert date fields to datetime objects
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Finally prioritize non-null data
        df = df.combine_first(df)

        return df


    # Create or retrieve a unique client_id
    def assign_client_id(self, df):
        if df is None:
            return None

        # Create a 'client_id' using phone and email as keys
        def get_client_id(row):
            key = (row['phone'], row['email'])
            if key not in self.client_map:
                self.client_map[key] = len(self.client_map) + 1
            return self.client_map[key]

        df['client_id'] = df.apply(get_client_id, axis=1)
        return df

    # Merge data based on client_id or phone number
    def merge_data(self, df1, df2):
        if df1 is None:
            return df2
        if df2 is None:
            return df1

        try:
            merged_df = pd.merge(
                df1, 
                df2, 
                on=['client_id', 'phone'], 
                how='outer'
            )
            return merged_df
        except Exception as e:
            print(f"Error merging data: {e}")
            return df1


    # Consolidate multiple dataframes into one unified dataset
    def consolidate_data(self, people, transactions, transfers, promotions):
        # Clean and normalize
        people = self.clean_and_fix_data(self.normalize_data(people))
        transactions = self.clean_and_fix_data(self.normalize_data(transactions))
        transfers = self.clean_and_fix_data(self.normalize_data(transfers))
        promotions = self.clean_and_fix_data(self.normalize_data(promotions))

        # Assign unique client IDs
        people = self.assign_client_id(people)
        transactions = self.assign_client_id(transactions)
        transfers = self.assign_client_id(transfers)
        promotions = self.assign_client_id(promotions)

        # Fallback handling to avoid NoneType issues
        consolidated = people if people is not None else pd.DataFrame()

        if transactions is not None:
            consolidated = self.merge_data(consolidated, transactions)
        if transfers is not None:
            consolidated = self.merge_data(consolidated, transfers)
        if promotions is not None:
            consolidated = self.merge_data(consolidated, promotions)

        # Final cleanup (only drop if the dataframe is not empty)
        if not consolidated.empty:
            consolidated.dropna(axis=1, how='all', inplace=True) 

        return consolidated

