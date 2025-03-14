import sqlite3
import pandas as pd

def merge_all_tables(
    people_db, transfers_db, promotions_db, transactions_db,
    output_db="venmito_master.db", output_csv="venmito_master.csv"):
    """Merge all relevant tables into a single database and export as CSV."""
    
    conn_master = sqlite3.connect(output_db)
    
    # Load data from each database
    people_df = pd.read_sql_query("SELECT * FROM people", sqlite3.connect(people_db))
    transfers_df = pd.read_sql_query("SELECT * FROM transfers", sqlite3.connect(transfers_db))
    promotions_df = pd.read_sql_query("SELECT * FROM promotions", sqlite3.connect(promotions_db))
    transactions_df = pd.read_sql_query("SELECT * FROM transactions", sqlite3.connect(transactions_db))
    
    # Ensure date columns are in proper datetime format
    if 'date' in transfers_df.columns:
        transfers_df['date'] = pd.to_datetime(transfers_df['date'], errors='coerce')
    if 'date' in transactions_df.columns:
        transactions_df['date'] = pd.to_datetime(transactions_df['date'], errors='coerce')
    
    # Rename conflicting columns before merging
    promotions_df.rename(columns={"item": "promoted_item"}, inplace=True)
    transactions_df.rename(columns={"item": "purchased_item"}, inplace=True)
    
    # Merge promotions with people using email or phone_number
    merged_promotions = people_df.merge(promotions_df, on=["email", "phone_number"], how="left")
    
    # Merge transfers by sender_id and recipient_id
    merged_transfers = merged_promotions.merge(transfers_df, left_on="id", right_on="sender_id", how="left")
    merged_transfers = merged_transfers.merge(transfers_df, left_on="id", right_on="recipient_id", how="left", suffixes=("_sent", "_received"))
    
    # Rename columns for clarity
    merged_transfers.rename(columns={
        "sender_id_sent": "sent_from",
        "recipient_id_sent": "sent_to",
        "sender_id_received": "received_from",
        "recipient_id_received": "received_to"
    }, inplace=True)
    
    # Merge transactions using phone_number
    merged_transactions = merged_transfers.merge(transactions_df, on="phone_number", how="left")
    
    # Save merged data to the master database
    merged_transactions.to_sql("venmito_data", conn_master, if_exists="replace", index=False)
    conn_master.close()
    
    # Export to CSV with proper date formatting
    merged_transactions.to_csv(output_csv, index=False, date_format='%Y-%m-%d')
    print(f"All tables merged into '{output_db}' as 'venmito_data' table and exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    merge_all_tables(
        "merged_people.db", "transfers_to_db.db", "promotions_to_db.db", "transactions_to_db.db"
    )
