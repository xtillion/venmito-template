import os
from dotenv import load_dotenv
from src.db.db import Database

# Load environment variables
load_dotenv()

def test_connection():
    try:
        # Initialize database connection
        host = os.environ.get('DB_HOST')
        dbname = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        port = int(os.environ.get('DB_PORT', 5432))
        
        print(f"Connecting to {dbname} on {host}...")
        Database.initialize(host, dbname, user, password, port)
        
        # Test a simple query
        result = Database.execute_query("SELECT current_timestamp as time, current_database() as database")
        print(f"Connected successfully!")
        print(f"Time: {result[0][0]}")
        print(f"Database: {result[0][1]}")
        
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
    finally:
        Database.close()

if __name__ == "__main__":
    test_connection()