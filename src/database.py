from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/venmito")  # Use 'db' as hostname
engine = create_engine(db_url)

# Create necessary tables
def setup_database():
    with engine.connect() as conn:
        # people table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY, 
            first_name TEXT, 
            last_name TEXT, 
            telephone TEXT, 
            email TEXT, 
            city TEXT, 
            country TEXT
        )'''))

        conn.execute(text('''CREATE TABLE IF NOT EXISTS devices (
            id SERIAL PRIMARY KEY,
            person_id TEXT REFERENCES people(id),
            device_type TEXT
        )'''))

        # transfers table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS transfers (
            sender_id TEXT, recipient_id TEXT, amount REAL, date TEXT
        )'''))

        # transactions table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY, 
            client_id TEXT,  
            store TEXT, 
            timestamp TEXT 
        )'''))

        conn.execute(text('''CREATE TABLE IF NOT EXISTS transaction_items (
            id SERIAL PRIMARY KEY,
            transaction_id TEXT REFERENCES transactions(transaction_id),
            item_name TEXT, 
            price REAL,
            price_per_item REAL,
            quantity INTEGER
        )'''))

        # promotions table
        conn.execute(text('''CREATE TABLE IF NOT EXISTS promotions (
            id TEXT PRIMARY KEY,
            client_email TEXT,
            telephone TEXT,
            promotion TEXT,
            responded TEXT
        )'''))

        conn.commit()

if __name__ == '__main__':
    setup_database()
    print("Database setup completed successfully!")