from database import engine
from data_ingestion.read_formats import * # read file format functions
from data_ingestion.data_handlers import * # irregularities in file formats functions

# Store Data in Database
def store_in_db(table, df):
    if table == "people":
        store_people_and_devices(df)  # Handle people & devices separately
    elif table == "transfers":
        store_transfers(df)  # Handle transfers separately
    elif table == "promotions":
        store_promotions(df)  # Handle promotions with our new function
    else:
        df.drop_duplicates(inplace=True)  # Remove duplicates before insertion
        df.to_sql(table, engine, if_exists="append", index=False, method="multi")

# Function to trigger data ingestion directly
def ingest_data():
    store_in_db("people", read_json("data/people.json"))
    store_in_db("people", read_yaml("data/people.yml"))
    store_in_db("transfers", read_csv("data/transfers.csv"))
    transactions_df, items_df = read_xml("data/transactions.xml")  # Get both DataFrames
    store_transactions(transactions_df, items_df)  # Store both
    store_in_db("promotions", read_csv("data/promotions.csv"))
    print("Data ingestion completed!")

# Run the ingestion
if __name__ == '__main__':
    ingest_data()