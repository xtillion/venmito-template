from ingestion import DataLoader
from transformation import DataTransformer
from analysis import DataAnalyzer
from output import DatabaseHandler

def main():
    # Initiate DataLoader in instance and Load Data from every file
    loader = DataLoader()
    people = loader.load_json('../data/people.json')
    transfers = loader.load_csv('../data/transfers.csv')
    promotions = loader.load_csv('../data/promotions.csv')
    transactions = loader.load_xml('../data/transactions.xml')

    # Initiate DataTransformer to transform and merge data
    transformer = DataTransformer()
    consolidated_df = transformer.consolidate_data(people, transactions, transfers, promotions)
    print(consolidated_df)

    # Placeholder Data Analysis phase logic
    analyzer = DataAnalyzer()
    top_products = analyzer.get_top_selling_products(consolidated_df)
    store_performance = analyzer.get_store_performance(consolidated_df)

    print("\nTop Products:")
    print(top_products)
    print("\nStore Performance:")
    print(store_performance)

    # Step 4: Save to Database
    db = DatabaseHandler()
    db.save_to_db(consolidated_df, 'consolidated_data')

if __name__ == "__main__":
    main()
