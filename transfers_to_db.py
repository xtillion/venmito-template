import sqlite3
import pandas as pd

def create_transfers_table(transfers_file, output_db="transfers_to_db.db", output_csv="transfers_to_db.csv"):
    """Create a transfers database storing all transfer data with standardized column names."""
    
    # Load transfers data
    transfers_df = pd.read_csv(transfers_file)
    
    # Standardize column names
    transfers_df.rename(columns={
        "sender_id": "sender_id",
        "recipient_id": "recipient_id",
        "amount": "amount",
        "date": "date"
    }, inplace=True)
    
    # Ensure sender_id and recipient_id are strings with leading zeros
    transfers_df['sender_id'] = transfers_df['sender_id'].astype(str).str.zfill(4)
    transfers_df['recipient_id'] = transfers_df['recipient_id'].astype(str).str.zfill(4)
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    transfers_df.to_sql('transfers', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    transfers_df.to_csv(output_csv, index=False)
    print(f"Transfers table created in '{output_db}' and data exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    create_transfers_table("data/transfers.csv")
