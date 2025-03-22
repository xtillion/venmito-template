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

class CLIHandler:
    def __init__(self, db_name='venmito.db'):
        self.conn = sqlite3.connect(db_name)

    # Function to execute and display query results
    def run_query(self, query):
        try:
            result = pd.read_sql_query(query, self.conn)
            if result.empty:
                print("\n⚠️ No results found.")
            else:
                print("\n", result.to_string(index=False))
        except Exception as e:
            print(f"\n❌ Error: {e}")

    # Display available options
    def display_menu(self):
        print("\n[Venmito CLI]")
        print("1. View top clients")
        print("2. View most profitable store")
        print("3. View most popular store for items")
        print("4. View promotion suggestions")
        print("5. Run custom SQL query")
        print("6. Exit")

    # Predefined queries
    def handle_option(self, option):
        if option == '1':
            query = """
                SELECT name AS 'Client Name', SUM(price) AS 'Total Spent'
                FROM transactions
                JOIN clients ON transactions.phone = clients.phone
                GROUP BY name
                ORDER BY SUM(price) DESC
                LIMIT 10
            """
            self.run_query(query)

        elif option == '2':
            query = """
                SELECT store AS 'Store', SUM(price) AS 'Total Revenue'
                FROM transactions
                GROUP BY store
                ORDER BY SUM(price) DESC
                LIMIT 5
            """
            self.run_query(query)

        elif option == '3':
            query = """
                SELECT item AS 'Item', store AS 'Top Store', COUNT(*) AS 'Units Sold'
                FROM transactions
                GROUP BY item, store
                ORDER BY COUNT(*) DESC
                LIMIT 5
            """
            self.run_query(query)

        elif option == '4':
            query = """
                SELECT promotion AS 'Promotion', city AS 'City', COUNT(*) AS 'Negative Responses'
                FROM promotions
                JOIN clients ON promotions.telephone = clients.phone
                WHERE responded = 0
                GROUP BY promotion, city
                ORDER BY COUNT(*) DESC
                LIMIT 5
            """
            self.run_query(query)

        elif option == '5':
            custom_query = input("\nEnter your custom SQL query:\n> ")
            self.run_query(custom_query)

        elif option == '6':
            print("\n👋 Exiting CLI. Goodbye!")
            return False

        else:
            print("\n❌ Invalid option. Try again.")

        return True

    # Start CLI loop
    def run(self):
        running = True
        while running:
            self.display_menu()
            option = input("\nChoose an option (1-6): ")
            running = self.handle_option(option)

    # Close connection
    def close(self):
        if self.conn:
            self.conn.close()
            print("\n🔒 Database connection closed.")

