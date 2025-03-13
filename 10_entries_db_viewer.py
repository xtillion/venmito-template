import sqlite3
import pandas as pd

def view_database_entries(db_name, table_name, limit=10):
    """Fetch and display the first few entries from a specified table in the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit};", conn)
        conn.close()
        
        # Display the dataframe
        print(df)
        return df
    except Exception as e:
        print(f"Error accessing database: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    view_database_entries('venmito.db', 'people', 10)
