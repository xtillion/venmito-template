import sqlite3
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_name='venmito.db'):
        self.db_name = db_name
        self.conn = None

    # Connect to SQLite database
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        print(f"Connected to database: {self.db_name}")

    # Create tables
    def create_tables(self):
        cursor = self.conn.cursor()

        # Create Clients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT UNIQUE,
                email TEXT,
                dob TEXT,
                city TEXT,
                country TEXT,
                android INTEGER,
                iphone INTEGER,
                desktop INTEGER
            )
        ''')

        # Create Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                phone TEXT,
                store TEXT,
                item TEXT,
                price REAL,
                quantity INTEGER,
                date TEXT,
                FOREIGN KEY(phone) REFERENCES clients(phone)
            )
        ''')

        # Create Transfers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY,
                sender_id INTEGER,
                recipient_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(sender_id) REFERENCES clients(id),
                FOREIGN KEY(recipient_id) REFERENCES clients(id)
            )
        ''')

        # Create Promotions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY,
                client_email TEXT,
                telephone TEXT,
                promotion TEXT,
                responded INTEGER,
                promotion_date TEXT,
                FOREIGN KEY(telephone) REFERENCES clients(phone)
            )
        ''')

        self.conn.commit()
        print("Tables created successfully")

    # Insert data into clients table
    def insert_clients(self, clients_df):
        clients_df.to_sql('clients', self.conn, if_exists='replace', index=False)
        print(f"{len(clients_df)} clients inserted")

    # Insert data into transactions table
    def insert_transactions(self, transactions_df):
        transactions_df.to_sql('transactions', self.conn, if_exists='replace', index=False)
        print(f"{len(transactions_df)} transactions inserted")

    # Insert data into transfers table
    def insert_transfers(self, transfers_df):
        transfers_df.to_sql('transfers', self.conn, if_exists='replace', index=False)
        print(f"{len(transfers_df)} transfers inserted")

    # Insert data into promotions table
    def insert_promotions(self, promotions_df):
        promotions_df.to_sql('promotions', self.conn, if_exists='replace', index=False)
        print(f"{len(promotions_df)} promotions inserted")

    # Example: Query to validate data
    def query_clients(self):
        query = "SELECT * FROM clients LIMIT 5"
        result = pd.read_sql(query, self.conn)
        print("\nSample Clients Data:")
        print(result)

    # Close connection
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")
