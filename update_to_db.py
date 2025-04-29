"""
Script to upload processed data to the Venmito database.
"""

import os
import logging
import pandas as pd
from dotenv import load_dotenv

from src.db.data_loader import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_connection_params():
    """Get database connection parameters from environment variables."""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'dbname': os.environ.get('DB_NAME', 'venmito'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres'),
        'port': os.environ.get('DB_PORT', '5432')
    }

def main():
    """Load processed data into the database."""
    try:
        # Get connection parameters
        connection_params = get_connection_params()
        
        # Create DataLoader
        processed_dir = "data/processed"
        loader = DataLoader(connection_params, processed_dir)
        
        # Connect to the database
        loader.connect()
        
        # Load people data
        people_file = os.path.join(processed_dir, "people.csv")
        if os.path.exists(people_file):
            people_df = pd.read_csv(people_file)
            logger.info(f"Loading {len(people_df)} people records into database")
            loader.load_people_df(people_df)
        
        # Load promotions data
        promotions_file = os.path.join(processed_dir, "promotions.csv")
        if os.path.exists(promotions_file):
            promotions_df = pd.read_csv(promotions_file)
            logger.info(f"Loading {len(promotions_df)} promotion records into database")
            loader.load_promotions_df(promotions_df)
        
        # Load transfers data
        transfers_file = os.path.join(processed_dir, "transfers.csv")
        if os.path.exists(transfers_file):
            transfers_df = pd.read_csv(transfers_file)
            logger.info(f"Loading {len(transfers_df)} transfer records into database")
            loader.load_transfers_df(transfers_df)
        
        # Load transactions data (without item columns)
        transactions_file = os.path.join(processed_dir, "transactions.csv")
        if os.path.exists(transactions_file):
            transactions_df = pd.read_csv(transactions_file)
            
            # Ensure only valid columns are included (no item, quantity, price_per_item)
            valid_columns = [
                'transaction_id', 'user_id', 'store', 'price', 
                'transaction_date', 'store_account_id'
            ]
            
            # Filter to keep only columns that exist in the dataframe
            existing_columns = [col for col in valid_columns if col in transactions_df.columns]
            transactions_df = transactions_df[existing_columns]
            
            logger.info(f"Loading {len(transactions_df)} transaction records into database")
            loader.load_transactions_df(transactions_df)
        
        # Load transaction items data
        transaction_items_file = os.path.join(processed_dir, "transaction_items.csv")
        if os.path.exists(transaction_items_file):
            transaction_items_df = pd.read_csv(transaction_items_file)
            logger.info(f"Loading {len(transaction_items_df)} transaction item records into database")
            
            # Check if the loader has a method for transaction items
            if hasattr(loader, 'load_transaction_items_df'):
                loader.load_transaction_items_df(transaction_items_df)
            else:
                # If the method doesn't exist, define logic here
                logger.warning("load_transaction_items_df method not found in DataLoader")
                # Implement direct database insertion here
                
                # Create a basic query
                item_query = """
                INSERT INTO transaction_items (transaction_id, item, quantity, price_per_item, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """
                
                # Convert to list of tuples for batch execution
                item_data = []
                for _, row in transaction_items_df.iterrows():
                    item_data.append((
                        row['transaction_id'],
                        row['item'],
                        row['quantity'],
                        row['price_per_item'],
                        row['subtotal']
                    ))
                
                # Execute batch query
                from psycopg2.extras import execute_batch
                execute_batch(loader.cursor, item_query, item_data, page_size=100)
                loader.conn.commit()
                logger.info(f"Loaded {len(item_data)} transaction item records into database")
        
        # Load summary data if available
        for summary_type in ['user_transactions', 'user_transfers', 'item_summary', 'store_summary']:
            summary_file = os.path.join(processed_dir, f"{summary_type}.csv")
            if os.path.exists(summary_file):
                summary_df = pd.read_csv(summary_file)
                logger.info(f"Loading {len(summary_df)} {summary_type} records into database")
                
                # Call the appropriate loader method
                method_name = f"load_{summary_type}_df"
                if hasattr(loader, method_name):
                    method = getattr(loader, method_name)
                    method(summary_df)
                else:
                    logger.warning(f"{method_name} method not found in DataLoader")
        
        logger.info("Data loading completed successfully")
        
    except Exception as e:
        logger.error(f"Error loading data into database: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Disconnect from the database
        if loader:
            loader.disconnect()

if __name__ == "__main__":
    main()