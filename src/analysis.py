import pandas as pd

class DataAnalyzer:

    def format_percentage(self, x):
        return f"{x * 100:.2f}%" if pd.notnull(x) else "N/A"


    def format_currency(self, x):
        return f"${x:,.2f}" if pd.notnull(x) else "N/A"


    def __init__(self, people_df, transactions_df, transfers_df, promotions_df):
        self.people_df = people_df
        self.transactions_df = transactions_df
        self.transfers_df = transfers_df
        self.promotions_df = promotions_df


    # Which clients have what type of promotion?
    def get_client_promotions(self):
        merged = pd.merge(
            self.promotions_df,
            self.people_df,
            left_on='telephone',
            right_on='phone',
            how='inner'
        )
        result = merged[['name', 'promotion', 'responded', 'promotion_date']]

        # Rename columns for cleaner display
        result = result.rename(columns={
            'name': 'Name',
            'promotion': 'Promotion',
            'responded': 'Responded',
            'promotion_date': 'Promotion Date'
        })
        result = result.reset_index(drop=True)

        return result


    # What’s the most effective promotion type?
    def get_promotion_effectiveness(self):
        result = self.promotions_df.groupby('promotion')['responded'].mean().reset_index()
        result['responded'] = result['responded'].apply(self.format_percentage)

        # Rename columns for cleaner display
        result = result.rename(columns={
            'promotion': 'Promotion',
            'responded': 'Response Rate'
        }).sort_values(by='Response Rate', ascending=False).reset_index(drop=True)

        return result.sort_values(by='Response Rate', ascending=False)


    # What’s the most frequently purchased item?
    def get_top_items(self):
        result = self.transactions_df.groupby('item')['quantity'].sum().reset_index()
        result = result.rename(columns={
            'item': 'Item',
            'quantity': 'Quantity'
        }).sort_values(by='Quantity', ascending=False).reset_index(drop=True)
        return result


    # What store generates the highest revenue?
    def get_top_stores(self):
        result = self.transactions_df.groupby('store')['price'].sum().reset_index()
        result = result.rename(columns={
            'store': 'Store',
            'price': 'Price'
        }).sort_values(by='Price', ascending=False).reset_index(drop=True)
        return result


    # Which client spends the most?
    def get_top_clients(self):
        merged = pd.merge(
            self.transactions_df,
            self.people_df,
            left_on='phone',
            right_on='phone',
            how='inner'
        )
        result = merged.groupby('name')['price'].sum().reset_index()
        result['price'] = result['price'].apply(self.format_currency)

        # Rename columns for cleaner display
        result = result.rename(columns={
            'name': 'Client Name',
            'price': 'Total Spent'
        }).sort_values(by='Total Spent', ascending=False).reset_index(drop=True)


        result = result.reset_index(drop=True)

        return result.sort_values(by='Total Spent', ascending=False)


    # Who sends the most money?
    def get_top_senders(self):
        merged = pd.merge(
            self.transfers_df,
            self.people_df,
            left_on='sender_id',
            right_on='id',
            how='inner'
        ).dropna()

        # Remove duplicates before summing
        merged = merged.drop_duplicates(subset=['sender_id', 'recipient_id', 'amount'])

        result = merged.groupby('name', as_index=False)['amount'].sum()
        result['amount'] = result['amount'].apply(self.format_currency)

        # Reset index after sorting
        result = result.rename(columns={
            'name': 'Sender',
            'amount': 'Total Sent'
        }).sort_values(by='Total Sent', ascending=False).reset_index(drop=True)

        return result


    def get_top_recipients(self):
        merged = pd.merge(
            self.transfers_df,
            self.people_df,
            left_on='recipient_id',
            right_on='id',
            how='inner'
        ).dropna()

        # Remove duplicates before summing
        merged = merged.drop_duplicates(subset=['recipient_id', 'sender_id', 'amount'])

        result = merged.groupby('name', as_index=False)['amount'].sum()
        result['amount'] = result['amount'].apply(self.format_currency)

        # Reset index after sorting
        result = result.rename(columns={
            'name': 'Recipient',
            'amount': 'Total Received'
        }).sort_values(by='Total Received', ascending=False).reset_index(drop=True)

        return result


    # Are there any unusual patterns (e.g., large transfers)?
    def get_unusual_transfers(self) -> pd.DataFrame:
        threshold = self.transfers_df['amount'].mean() + (2 * self.transfers_df['amount'].std())

        # Create a copy to avoid SettingWithCopyWarning
        result = self.transfers_df[self.transfers_df['amount'] > threshold].copy()

        # Format currency
        result['amount'] = result['amount'].apply(self.format_currency)

        # Rename columns for cleaner display
        result = result.rename(columns={
            'id': 'ID',
            'sender_id': 'Sender ID',
            'recipient_id': 'Recipient ID',
            'amount': 'Amount',
            'date': 'Date'
        })

        # Clean indexing after filtering
        result = result.reset_index(drop=True)

        return result


    # Who are the most valuable clients?
    def get_most_valuable_clients(self):
        merged = pd.merge(
            self.transactions_df,
            self.people_df,
            left_on='phone',
            right_on='phone',
            how='inner'
        )
        result = merged.groupby('name')['price'].sum().reset_index().sort_values(by='price', ascending=False).head(10)

        result['price'] = result['price'].apply(self.format_currency)

        # Rename columns for cleaner display
        result = result.rename(columns={
            'name': 'VIP Client',
            'price': 'Total Spent'
        })
        result = result.reset_index(drop=True)

        return result


    # Are there any geographic trends in client spending?
    def get_location_patterns(self):
        merged = pd.merge(
            self.transactions_df,
            self.people_df,
            left_on='phone',
            right_on='phone',
            how='inner'
        )
        result = merged.groupby('city')['price'].sum().reset_index()
        result['price'] = result['price'].apply(self.format_currency)

        # Rename columns for cleaner display
        result = result.rename(columns={
            'city': 'City',
            'price': 'Total Revenue'
        }).sort_values(by='Total Revenue', ascending=False).reset_index(drop=True)


        result = result.reset_index(drop=True)

        return result.sort_values(by='Total Revenue', ascending=False)



    # How can the business improve customer targeting?
    def get_customer_targeting_insights(self):
        promo_data = pd.merge(
            self.promotions_df,
            self.people_df,
            left_on='telephone',
            right_on='phone',
            how='inner'
        )
        positive_responses = promo_data[promo_data['responded'] == 1]
        negative_responses = promo_data[promo_data['responded'] == 0]

        total_clients = len(promo_data)
        positive_response_rate = len(positive_responses) / total_clients
        negative_response_rate = len(negative_responses) / total_clients
        most_effective_promotion = self.get_promotion_effectiveness().iloc[0]['Promotion']

        return {
            'Total Clients': total_clients,
            'Positive Response Rate': self.format_percentage(positive_response_rate),
            'Negative Response Rate': self.format_percentage(negative_response_rate),
            'Most Effective Promotion': most_effective_promotion
        }
