from sqlalchemy import inspect

from data_ingestor import ingest_data_from_file
from data_transformer import *
from data_loader import *

def tables_exist(table_names, db_engine):
    inspector = inspect(db_engine)
    existing_tables = inspector.get_table_names()
    return all(table in existing_tables for table in table_names)

def run_etl(db_session):
    df_promotions = ingest_data_from_file("../data/promotions.csv")
    df_transfers = ingest_data_from_file("../data/transfers.csv")
    df_transactions = ingest_data_from_file("../data/transactions.xml")
    df_people_1 = ingest_data_from_file("../data/people.json")
    df_people_2 = ingest_data_from_file("../data/people.yml")

    df_people_1 = transform_json_data(df_people_1)
    df_people_2 = transform_yml_data(df_people_2)
    df_promotions = transform_csv_data(df_promotions)

    merged_df_people = merge_people_data(df_people_1, df_people_2)

    complete_df_promotions = complete_promotions_data(df_promotions, merged_df_people)

    save_data_as_csv(merged_df_people, 'people')
    save_data_as_csv(complete_df_promotions, 'promotions')
    save_data_as_csv(df_transfers, 'transfers')
    save_data_as_csv(df_transactions, 'transactions')

    load_data_to_table('../output_data/people.csv', 'People', db_session)
    load_data_to_table('../output_data/promotions.csv', 'Promotions', db_session)
    load_data_to_table('../output_data/transactions.csv', 'Transactions', db_session)
    load_data_to_table('../output_data/transfers.csv', 'Transfers', db_session)