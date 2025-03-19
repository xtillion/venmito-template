from ingestion import DataLoader
from transformation import DataTransformer
from analysis import DataAnalyzer
from output import DatabaseHandler

def main():
    # Step 1: Load Data
    loader = DataLoader()
    people = loader.load_json('../data/people.json')
    transfers = loader.load_csv('../data/transfers.csv')
    promotions = loader.load_csv('../data/promotions.csv')
    transactions = loader.load_xml('../data/transactions.xml')

    # Step 2: Transform Data
    transformer = DataTransformer()
    people = transformer.normalize_data(people)
    transfers = transformer.normalize_data(transfers)
    promotions = transformer.normalize_data(promotions)
    transactions = transformer.normalize_data(transactions)

    # Step 3: Merge Data
    combined_df = transformer.merge_data(people, transactions, on="phone")

    # Step 4: Analyze Data
    analyzer = DataAnalyzer()
    top_products = analyzer.get_top_selling_products(combined_df)
    store_performance = analyzer.get_store_performance(combined_df)

    print("\nTop Products:")
    print(top_products)
    print("\nStore Performance:")
    print(store_performance)

    # Step 5: Save to Database
    db = DatabaseHandler()
    db.save_to_db(combined_df, 'consolidated_data')

if __name__ == "__main__":
    main()
