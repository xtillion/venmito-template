from ingestion import DataLoader
from transformation import DataTransformer
from analysis import DataAnalyzer
from output import DatabaseHandler

def main():
    # Initiate DataLoader in instance and Load Data from every file
    loader = DataLoader()
    people_json = loader.load_json('data/people.json')
    people_yml = loader.load_yml('data/people.yml')
    transfers = loader.load_csv('data/transfers.csv')
    promotions = loader.load_csv('data/promotions.csv')
    transactions = loader.load_xml('data/transactions.xml')

    # Initiate DataTransformer to transform and merge data
    transformer = DataTransformer()
    # People DataFrame
    people_df = transformer.create_people_dataframe(people_json, people_yml)
    people_df.to_csv('consolidated_people.csv', index=False)

    promotions_df = transformer.create_promotions_dataframe(promotions)
    transactions_df = transformer.create_transactions_dataframe(transactions)
    transfers_df = transformer.create_transfers_dataframe(transfers)

    # Save to CSV (Optional)
    promotions_df.to_csv('promotions_output.csv', index=False)
    transactions_df.to_csv('transactions_output.csv', index=False)
    transfers_df.to_csv('transfers_output.csv', index=False)

    analyzer = DataAnalyzer(people_df, transactions_df, transfers_df, promotions_df)

    # Promotions Analysis
    print("\nClient Promotions: \n", analyzer.get_client_promotions())
    print("\nPromotion Effectiveness: \n", analyzer.get_promotion_effectiveness())

    # Transactions Analysis
    print("\nTop Items: \n", analyzer.get_top_items())
    print("\nTop Stores: \n", analyzer.get_top_stores())
    print("\nTop Clients: \n", analyzer.get_top_clients())

    # Transfers Analysis
    print("\nTop Senders: \n", analyzer.get_top_senders())
    print("\nTop Recipients: \n", analyzer.get_top_recipients())
    print("\nUnusual Transfers: \n", analyzer.get_unusual_transfers())

    # Client Insights
    print("\nVIP Clients: \n", analyzer.get_most_valuable_clients())
    print("\nLocation Patterns: \n", analyzer.get_location_patterns())
    print("\nCustomer Targetting Insights: \n", analyzer.get_customer_targeting_insights())


    # print("\nTop Products:")
    # print(top_products)
    # print("\nStore Performance:")
    # print(store_performance)

    # # Step 4: Save to Database
    # db = DatabaseHandler()
    # db.save_to_db(consolidated_df, 'consolidated_data')

if __name__ == "__main__":
    main()
