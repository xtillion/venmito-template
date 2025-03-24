from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
import csv

from backend.model.people import People
from backend.model.promotions import Promotions
from backend.model.transactions import Transactions
from backend.model.transfer import Transfers
from backend.utils.logger import configure_logging

logger = configure_logging()

def clean_database(db_session):
    db_session.query(Promotions).delete()
    db_session.query(Transactions).delete()
    db_session.query(Transfers).delete()
    db_session.query(People).delete()
    db_session.commit()
    logger.info('Dropped all tables to start the program with a fresh state')

def create_tables_if_not_exists(db_session, filepath):
    with open(filepath, 'r') as f:
        schema = f.read()

    sql_statements = schema.split(';')
    sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]

    for statement in sql_statements:
        db_session.execute(text(statement))
        db_session.commit()

def load_data_to_table(csv_file: str, table_name: str, db_session):
    records_inserted = 0

    create_tables_if_not_exists(db_session, '../model/sql_schema/create_schema.sql')

    if table_name == 'People':

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                insert_query = insert(People).values(
                    id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    telephone=row[3],
                    email=row[4],
                    dob=row[5],
                    city=row[6],
                    country=row[7],
                    android=row[8].lower() == 'true',
                    iphone=row[9].lower() == 'true',
                    desktop=row[10].lower() == 'true'
                )

                db_session.execute(insert_query)
                db_session.commit()
                records_inserted += 1

    elif table_name == 'Promotions':

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                insert_query = insert(Promotions).values(
                    id=row[0],
                    promotion=row[1],
                    responded=row[2],
                    promotion_date=row[3],
                    email=row[4],
                    telephone=row[5]
                ).on_conflict_do_nothing(index_elements=['id'])

                db_session.execute(insert_query)
                db_session.commit()
                records_inserted += 1

    elif table_name == 'Transactions':

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                insert_query = insert(Transactions).values(
                    transaction_id=row[0],
                    telephone=row[1],
                    store=row[2],
                    item_name=row[3],
                    total_price=row[4],
                    price_per_item=row[5],
                    quantity=row[6],
                    date=row[7]
                )

                db_session.execute(insert_query)
                db_session.commit()
                records_inserted += 1

    elif table_name == 'Transfers':

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                insert_query = insert(Transfers).values(
                    sender_id=row[0],
                    recipient_id=row[1],
                    amount=row[2],
                    date=row[3]
                )

                db_session.execute(insert_query)
                db_session.commit()
                records_inserted += 1

    db_session.commit()

    if records_inserted > 0:
        logger.info(f'Created Table {table_name} and inserted {records_inserted} records')
    else:
        logger.info(f'Table {table_name} already exists, no records were inserted')