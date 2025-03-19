import pandas as pd

class DataAnalyzer:
    def get_top_selling_products(self, df):
        return df.groupby('item')['price'].sum().reset_index().sort_values(by='price', ascending=False)

    def get_store_performance(self, df):
        return df.groupby('store')['price'].sum().reset_index().sort_values(by='price', ascending=False)

    def get_client_activity(self, df):
        return df['phone'].value_counts().reset_index().rename(columns={'index': 'phone', 'phone': 'transaction_count'})
