import argparse
from models.database import get_engine, create_tables

def main():
    parser = argparse.ArgumentParser(description="Initialize the database for Venmito")
    parser.add_argument('--user', type=str, required=True, help='Database username')
    parser.add_argument('--password', type=str, required=True, help='Database password')
    parser.add_argument('--host', type=str, default='localhost', help='Database host')
    parser.add_argument('--port', type=str, default='5432', help='Database port')
    parser.add_argument('--db', type=str, required=True, help='Database name')

    args = parser.parse_args()

    try:
        engine = get_engine(args.user, args.password, args.host, args.port, args.db)
        create_tables(engine)
        print("Database setup completed successfully.")
    except Exception as e:
        print(f"Error setting up the database: {e}")

if __name__ == "__main__":
    main() 