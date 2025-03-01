import sqlite3


def create_database():
    conn = sqlite3.connect("venmito.db")
    cursor = conn.cursor()

    # People Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        telephone TEXT UNIQUE,
        city TEXT,
        country TEXT,
        android INTEGER,
        iphone INTEGER,
        desktop INTEGER
    )
    ''')

    # Transactions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (n
        transaction_id INTEGER PRIMARY KEY,
        phone TEXT,
        store TEXT,
        total_price REAL,
        FOREIGN KEY (phone) REFERENCES people(telephone)
    )
    ''')

    # Transaction Items Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaction_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price_per_item REAL,
        total_price REAL,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    )
    ''')


    # Transfers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transfers (
        transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        recipient_id INTEGER,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (sender_id) REFERENCES people(id),
        FOREIGN KEY (recipient_id) REFERENCES people(id)
    )
''')

    # Promotions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS promotions (
        promotion_id INTEGER PRIMARY KEY,
        email TEXT,
        telephone TEXT,           
        promotion TEXT,
        responded TEXT,
        FOREIGN KEY (email) REFERENCES people(email)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database setup done")

if __name__ == "__main__":
    create_database()
