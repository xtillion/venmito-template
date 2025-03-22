from ingestion import DataLoader
from transformation import DataTransformer
from analysis import DataAnalyzer
from output import DatabaseHandler, CLIHandler

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

    db = DatabaseHandler()
    db.connect()
    db.create_tables()

    db.insert_clients(people_df)
    db.insert_transactions(transactions_df)
    db.insert_transfers(transfers_df)
    db.insert_promotions(promotions_df)

    # Example Query
    db.query_clients()

    # Close connection
    db.close()

    # Start CLI
    cli = CLIHandler(analyzer)
    cli.run()
    cli.close()

if __name__ == "__main__":
    main()
