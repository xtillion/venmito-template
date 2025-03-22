import sqlite3
import pandas as pd
from analysis import DataAnalyzer

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
    def __init__(self, analyzer, db_name='venmito.db'):
        self.conn = sqlite3.connect(db_name)
        self.analyzer = analyzer

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
        print("5. View top senders")
        print("6. View top recipients")
        print("7. View unusual transfers")
        print("8. View most valuable clients (VIP)")
        print("9. View location-based client spending")
        print("10. View average transaction value per store")
        print("11. View most common transfer amount")
        print("12. View store customer count")
        print("13. View most popular store for items")
        print("14. View transfer pattern by day of week")
        print("15. Run custom SQL query")
        print("16. Exit")

    # Predefined options based on analyzer methods
    def handle_option(self, option):
        if option == '1':
            print("\n[Top Clients]\n")
            print(self.analyzer.get_top_clients())

        elif option == '2':
            print("\n[Most Profitable Stores]\n")
            print(self.analyzer.get_top_stores())

        elif option == '3':
            print("\n[Most Popular Store for Each Item]\n")
            print(self.analyzer.get_most_popular_store_for_items())

        elif option == '4':
            print("\n[Promotion Suggestions]\n")
            print(self.analyzer.get_promotion_suggestions())

        elif option == '5':
            print("\n[Top Senders]\n")
            print(self.analyzer.get_top_senders())

        elif option == '6':
            print("\n[Top Recipients]\n")
            print(self.analyzer.get_top_recipients())

        elif option == '7':
            print("\n[Unusual Transfers]\n")
            print(self.analyzer.get_unusual_transfers())

        elif option == '8':
            print("\n[Most Valuable Clients]\n")
            print(self.analyzer.get_most_valuable_clients())

        elif option == '9':
            print("\n[Location-Based Spending]\n")
            print(self.analyzer.get_location_patterns())

        elif option == '10':
            print("\n[Average Transaction Value per Store]\n")
            print(self.analyzer.get_average_transaction_value())

        elif option == '11':
            print("\n[Most Common Transfer Amount]\n")
            print(self.analyzer.get_most_common_transfer_amount())

        elif option == '12':
            print("\n[Store Customer Count]\n")
            print(self.analyzer.get_store_customers())

        elif option == '13':
            print("\n[Most Popular Store for Each Item]\n")
            print(self.analyzer.get_most_popular_store_for_items())

        elif option == '14':
            print("\n[Transfer Pattern by Day of Week]\n")
            print(self.analyzer.get_transfer_pattern_by_day())

        elif option == '15':
            custom_query = input("\nEnter your custom SQL query:\n> ")
            self.run_query(custom_query)

        elif option == '16':
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
            option = input("\nChoose an option (1-16): ")
            running = self.handle_option(option)

    # Close connection
    def close(self):
        if self.conn:
            self.conn.close()
            print("\n🔒 Database connection closed.")
