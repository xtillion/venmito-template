import pandas as pd
import numpy as np

class DataTransformer:
    def __init__(self):
        self.client_map = {}

    # Clean phone numbers for consistency
    def clean_phone_number(self, phone):
        if isinstance(phone, str):
            return phone.replace('-', '').replace(' ', '')
        return phone

    # Standardize column names + Fix data format mismatches
    def normalize_data(self, df, source):
        if df is not None:
            if source == 'people_json':
                # Fix nested structure and map columns
                df['phone'] = df['telephone'].apply(self.clean_phone_number)
                df['name'] = df['first_name'] + ' ' + df['last_name']
                df['city'] = df['location'].apply(lambda x: x.get('City', 'Unknown City'))
                df['country'] = df['location'].apply(lambda x: x.get('Country', 'Unknown Country'))
            elif source == 'transactions_xml':
                df['phone'] = df['phone'].apply(self.clean_phone_number)
            elif source == 'people_yml':
                df['phone'] = df['phone'].apply(self.clean_phone_number)

            # Clean up column names
            df.columns = df.columns.str.lower()
            return df
        return None

    # Remove duplicates, fill missing data, aggregate values where necessary
    def clean_and_fix_data(self, df):
        if df is None:
            return None

        # First, merge by phone (ignore email in first pass)
        if 'phone' in df.columns:
            df = df.groupby('phone').agg({
                'name': 'first', 
                'email': 'first', 
                'city': 'first', 
                'country': 'first',
                'dob': 'first',
                'date': 'first',
                'amount': 'sum', 
                'promotion_type': 'first'
            }).reset_index()

        # Second pass — fill missing data by merging on email
        if 'email' in df.columns:
            email_merge = df.groupby('email').agg({
                'name': 'first', 
                'phone': 'first', 
                'city': 'first', 
                'country': 'first',
                'dob': 'first',
                'date': 'first',
                'amount': 'sum', 
                'promotion_type': 'first'
            }).reset_index()

            # Use combine_first to fill in missing data
            df = df.set_index('email').combine_first(email_merge.set_index('email')).reset_index()

        # Fill remaining missing values with placeholders
        df['email'].fillna('unknown@example.com', inplace=True)
        df['phone'].fillna('0000000000', inplace=True)
        df['name'].fillna('Unknown', inplace=True)
        df['city'].fillna('Unknown City', inplace=True)
        df['country'].fillna('Unknown Country', inplace=True)

        # Convert dates to consistent format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        return df

    # Create or retrieve unique client IDs
    def assign_client_id(self, df):
        if df is None:
            return None

        def get_client_id(row):
            key = (row['phone'], row['email'])
            if key not in self.client_map:
                self.client_map[key] = len(self.client_map) + 1
            return self.client_map[key]

        df['client_id'] = df.apply(get_client_id, axis=1)
        return df

    # Merge based on multiple keys
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

    # Consolidate all datasets into one master table
    def consolidate_data(self, people, transactions, transfers, promotions):
        # Clean and normalize
        people = self.clean_and_fix_data(self.normalize_data(people, 'people_json'))
        transactions = self.clean_and_fix_data(self.normalize_data(transactions, 'transactions_xml'))
        transfers = self.clean_and_fix_data(self.normalize_data(transfers, 'transfers_csv'))
        promotions = self.clean_and_fix_data(self.normalize_data(promotions, 'promotions_csv'))

        # Assign unique IDs
        people = self.assign_client_id(people)
        transactions = self.assign_client_id(transactions)
        transfers = self.assign_client_id(transfers)
        promotions = self.assign_client_id(promotions)

        # Start merging
        consolidated = people if people is not None else pd.DataFrame()
        if transactions is not None:
            consolidated = self.merge_data(consolidated, transactions)
        if transfers is not None:
            consolidated = self.merge_data(consolidated, transfers)
        if promotions is not None:
            consolidated = self.merge_data(consolidated, promotions)

        # Final cleanup
        if not consolidated.empty:
            consolidated.dropna(axis=1, how='all', inplace=True)

        return consolidated
