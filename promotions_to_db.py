import sqlite3
import pandas as pd

def create_promotions_table(promotions_file, output_db="promotions_to_db.db", output_csv="promotions_to_db.csv"):
    """Create a promotions database storing all promotion data with standardized column names."""
    
    # Load promotions data
    promotions_df = pd.read_csv(promotions_file)
    
    # Standardize column names
    promotions_df.rename(columns={
        "id": "promotion_id",
        "client_email": "email",
        "telephone": "phone_number",
        "promotion": "item",
        "responded": "responded"
    }, inplace=True)
    
    # Ensure promotion_id is a string with leading zeros
    promotions_df['promotion_id'] = promotions_df['promotion_id'].astype(str).str.zfill(4)
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    promotions_df.to_sql('promotions', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    promotions_df.to_csv(output_csv, index=False)
    print(f"Promotions table created in '{output_db}' and data exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    create_promotions_table("data/promotions.csv")
