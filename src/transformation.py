import pandas as pd
import xml.etree.ElementTree as ET

class DataTransformer:
    def __init__(self):
        self.client_map = {}

    def create_people_dataframe(self, people_json, people_yml):
        # Load and Normalize People.json
        if people_json is not None:
            people_json['name'] = people_json['first_name'] + ' ' + people_json['last_name']
            people_json['phone'] = people_json['telephone'].str.replace('-', '').str.replace(' ', '')
            people_json['dob'] = pd.to_datetime(people_json['dob'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

            # Extract city and country from location
            people_json['city'] = people_json['location'].apply(lambda x: x.get('City') if isinstance(x, dict) else None)
            people_json['country'] = people_json['location'].apply(lambda x: x.get('Country') if isinstance(x, dict) else None)

            # Convert devices into binary flags
            people_json['android'] = people_json['devices'].apply(lambda x: 1 if 'Android' in x else 0)
            people_json['iphone'] = people_json['devices'].apply(lambda x: 1 if 'Iphone' in x else 0)
            people_json['desktop'] = people_json['devices'].apply(lambda x: 1 if 'Desktop' in x else 0)

            # Drop unwanted columns
            people_json = people_json[['id', 'name', 'phone', 'email', 'dob', 'city', 'country', 'android', 'iphone', 'desktop']]

        # Load and Normalize People.yml
        if people_yml is not None:
            people_yml['phone'] = people_yml['phone'].str.replace('-', '').str.replace(' ', '')
            people_yml['dob'] = pd.to_datetime(people_yml['dob'], format='%B %d, %Y', errors='coerce').dt.strftime('%Y-%m-%d')

            # Split city and country if combined
            people_yml[['city', 'country']] = people_yml['city'].str.split(', ', expand=True)

            # Convert device flags to binary
            people_yml['android'] = people_yml['Android'].apply(lambda x: 1 if x == 1 else 0)
            people_yml['iphone'] = people_yml['Iphone'].apply(lambda x: 1 if x == 1 else 0)
            people_yml['desktop'] = people_yml['Desktop'].apply(lambda x: 1 if x == 1 else 0)

            # Drop unwanted columns
            people_yml = people_yml[['id', 'name', 'phone', 'email', 'dob', 'city', 'country', 'android', 'iphone', 'desktop']]

        # Merge DataFrames
        combined_df = pd.merge(
            people_json,
            people_yml,
            on=['id', 'email'],
            how='outer',
            suffixes=('_json', '_yml')
        )

        # Resolve Conflicts
        combined_df['name'] = combined_df['name_json'].combine_first(combined_df['name_yml'])
        combined_df['phone'] = combined_df['phone_json'].combine_first(combined_df['phone_yml'])
        combined_df['dob'] = combined_df['dob_json'].combine_first(combined_df['dob_yml'])


        combined_df['city'] = combined_df['city_json'].combine_first(combined_df['city_yml'])
        combined_df['country'] = combined_df['country_json'].combine_first(combined_df['country_yml'])

        # If the row is only in people.json, keep the city/country directly
        combined_df.loc[combined_df['city'].isna(), 'city'] = combined_df['city_json']
        combined_df.loc[combined_df['country'].isna(), 'country'] = combined_df['country_json']

        # Merge binary flags - set to 1 if either file shows usage
        combined_df['android'] = combined_df[['android_json', 'android_yml']].max(axis=1)
        combined_df['iphone'] = combined_df[['iphone_json', 'iphone_yml']].max(axis=1)
        combined_df['desktop'] = combined_df[['desktop_json', 'desktop_yml']].max(axis=1)

        # Drop temporary columns used for merging
        combined_df.drop(
            columns=[
                'name_json', 'name_yml', 'phone_json', 'phone_yml', 
                'dob_json', 'dob_yml', 'city_json', 'city_yml',
                'country_json', 'country_yml', 
                'android_json', 'android_yml', 
                'iphone_json', 'iphone_yml', 
                'desktop_json', 'desktop_yml'
            ], 
            inplace=True
        )

        # Final Clean-up
        combined_df.fillna('', inplace=True)

        return combined_df

    def create_promotions_dataframe(self, promotions):
        if promotions is None:
            return None

        # Convert 'responded' to boolean
        promotions['responded'] = promotions['responded'].map({'Yes': 1, 'No': 0})

        # Format date to YYYY-MM-DD
        promotions['promotion_date'] = pd.to_datetime(promotions['promotion_date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Clean phone format (remove dashes and spaces)
        promotions['telephone'] = promotions['telephone'].str.replace('-', '').str.replace(' ', '')

        # Keep only necessary columns
        promotions = promotions[['id', 'client_email', 'telephone', 'promotion', 'responded', 'promotion_date']]

        return promotions

    def create_transactions_dataframe(self, transactions):
        if transactions is None:
            return None

        data = []

        root = ET.fromstring(transactions)

        for transaction in root.findall('transaction'):
            transaction_id = int(transaction.get('id'))
            phone = transaction.find('phone').text if transaction.find('phone') is not None else None
            store = transaction.find('store').text if transaction.find('store') is not None else None
            date = transaction.find('date').text if transaction.find('date') is not None else None

            items = transaction.find('items')
            if items is not None:
                for item in items.findall('item'):
                    data.append({
                        'transaction_id': transaction_id,
                        'item': item.find('item').text if item.find('item') is not None else None,
                        'price': float(item.find('price').text) if item.find('price') is not None else None,
                        'price_per_item': float(item.find('price_per_item').text) if item.find('price_per_item') is not None else None,
                        'quantity': int(item.find('quantity').text) if item.find('quantity') is not None else None,
                        'phone': phone.replace('-', '').replace(' ', '') if phone is not None else None,
                        'store': store,
                        'date': date
                    })

        df = pd.DataFrame(data)

        # Format date to YYYY-MM-DD
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Set compound key (optional)
        df.set_index(['transaction_id', 'item'], inplace=False)

        return df

    def create_transfers_dataframe(self, transfers):
        if transfers is None:
            return None

        # Format date to YYYY-MM-DD
        transfers['date'] = pd.to_datetime(transfers['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Keep only necessary columns
        transfers = transfers[['sender_id', 'recipient_id', 'amount', 'date']]

        # Add autoincrement index
        transfers.insert(0, 'id', range(1, len(transfers) + 1))

        return transfers
