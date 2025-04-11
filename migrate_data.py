"""
Migration script for Venmito database structure updates.

This script:
1. Alters the database schema for the new transaction items structure
2. Migrates existing transaction data to the new format
3. Identifies store accounts and links transfers to transactions
"""

import os
import sys
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get a database connection from environment variables."""
    host = os.environ.get('DB_HOST', 'localhost')
    dbname = os.environ.get('DB_NAME', 'venmito')
    user = os.environ.get('DB_USER', 'postgres')
    password = os.environ.get('DB_PASSWORD', 'postgres')
    port = os.environ.get('DB_PORT', '5432')
    
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(connection_string)

def update_schema():
    """Apply schema changes to the database."""
    logger.info("Updating database schema...")
    
    # Define schema changes
    schema_changes = """
    -- 1. Create a backup of the transactions table
    CREATE TABLE IF NOT EXISTS transactions_backup AS 
    SELECT * FROM transactions;
    
    -- 2. Create a new transaction_items table for individual items
    CREATE TABLE IF NOT EXISTS transaction_items (
        item_id SERIAL PRIMARY KEY,
        transaction_id VARCHAR(20) NOT NULL,
        item VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        price_per_item DECIMAL(10, 2) NOT NULL,
        subtotal DECIMAL(10, 2) NOT NULL,
        CONSTRAINT fk_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
    );
    
    -- 3. Create an index on transaction_id for faster lookups
    CREATE INDEX IF NOT EXISTS idx_transaction_items_transaction ON transaction_items(transaction_id);
    
    -- 4. Add a store_account_id column to transactions to link to the corresponding store account
    ALTER TABLE transactions
    ADD COLUMN IF NOT EXISTS store_account_id INTEGER REFERENCES people(user_id);
    
    -- 5. Update the transfers table to add a related_transaction_id column
    ALTER TABLE transfers
    ADD COLUMN IF NOT EXISTS related_transaction_id VARCHAR(20) REFERENCES transactions(transaction_id);
    
    -- 6. Create an index for the new relationship
    CREATE INDEX IF NOT EXISTS idx_transfers_transaction ON transfers(related_transaction_id);
    
    -- 7. Add a flag to people table to identify store accounts
    ALTER TABLE people
    ADD COLUMN IF NOT EXISTS is_store_account BOOLEAN DEFAULT FALSE;
    """
    
    # Connect to the database
    engine = get_db_connection()
    
    try:
        # Execute schema changes
        with engine.connect() as connection:
            connection.execute(text(schema_changes))
            connection.commit()
        
        logger.info("Schema updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating schema: {str(e)}")
        return False

def migrate_transaction_items():
    """Migrate transaction data to the new schema."""
    logger.info("Starting transaction items migration...")
    
    # Connect to the database
    engine = get_db_connection()
    
    try:
        # Read existing transactions
        query = "SELECT * FROM transactions"
        transactions_df = pd.read_sql(query, engine)
        
        if transactions_df.empty:
            logger.warning("No transactions found to migrate")
            return
        
        logger.info(f"Found {len(transactions_df)} transactions to process")
        
        # Create items DataFrame
        items_data = []
        
        for _, tx in transactions_df.iterrows():
            transaction_id = tx['transaction_id']
            
            # Process item field
            items = []
            if 'item' in tx and tx['item'] is not None:
                if isinstance(tx['item'], str) and ',' in tx['item']:
                    items = [item.strip() for item in tx['item'].split(',')]
                else:
                    items = [tx['item']]
            
            # Process quantity field
            quantities = []
            if 'quantity' in tx:
                if isinstance(tx['quantity'], str) and ',' in tx['quantity']:
                    quantities = [int(q.strip()) for q in tx['quantity'].split(',')]
                else:
                    # If single quantity, distribute among items or use as is
                    if len(items) > 1:
                        qty_per_item = int(tx['quantity']) // len(items)
                        quantities = [qty_per_item] * len(items)
                        # Add remainder to first item
                        quantities[0] += int(tx['quantity']) % len(items)
                    else:
                        quantities = [int(tx['quantity'])]
            
            # Create item records
            for i, item in enumerate(items):
                quantity = quantities[i] if i < len(quantities) else 1
                price_per_item = float(tx.get('price_per_item', float(tx['price']) / quantity))
                subtotal = quantity * price_per_item
                
                items_data.append({
                    'transaction_id': transaction_id,
                    'item': item,
                    'quantity': quantity,
                    'price_per_item': price_per_item,
                    'subtotal': subtotal
                })
        
        # Create DataFrame from items data
        items_df = pd.DataFrame(items_data)
        
        if items_df.empty:
            logger.warning("No transaction items generated")
            return
        
        logger.info(f"Generated {len(items_df)} transaction items")
        
        # Insert items into the new table
        items_df.to_sql('transaction_items', engine, if_exists='append', index=False)
        
        logger.info("Transaction items migration completed successfully")
    
    except Exception as e:
        logger.error(f"Error during transaction items migration: {str(e)}")
        raise

def identify_store_accounts_and_link_transfers():
    """Identify store accounts and link transfers to transactions."""
    logger.info("Starting store account identification and transfer linking...")
    
    # Connect to the database
    engine = get_db_connection()
    
    try:
        # Load necessary data
        people_df = pd.read_sql("SELECT * FROM people", engine)
        transfers_df = pd.read_sql("SELECT * FROM transfers", engine)
        transactions_df = pd.read_sql("SELECT * FROM transactions", engine)
        
        logger.info(f"Loaded data: {len(people_df)} people, {len(transfers_df)} transfers, {len(transactions_df)} transactions")
        
        # STEP 1: Identify store accounts
        # Count how many times each user appears as a recipient in transfers
        recipient_counts = transfers_df['recipient_id'].value_counts()
        
        # Find transaction amounts
        transaction_amounts = set(transactions_df['price'].round(2))
        
        # Identify store accounts
        store_accounts = []
        
        for user_id, count in recipient_counts.items():
            if count >= 10:  # Threshold for potential store account
                # Get transfers received by this user
                user_transfers = transfers_df[transfers_df['recipient_id'] == user_id]
                
                # Round transfer amounts for comparison
                transfer_amounts = set(user_transfers['amount'].round(2))
                
                # Check overlap between transfer amounts and transaction amounts
                common_amounts = transaction_amounts.intersection(transfer_amounts)
                
                # Calculate ratio of matching amounts
                match_ratio = len(common_amounts) / len(transfer_amounts) if len(transfer_amounts) > 0 else 0
                
                # If high match ratio, mark as store account
                if match_ratio > 0.5 and len(common_amounts) >= 5:
                    store_accounts.append(int(user_id))
                    logger.info(f"Identified user_id {user_id} as potential store account " +
                               f"(match ratio: {match_ratio:.2f}, matching amounts: {len(common_amounts)})")
        
        # Update store accounts in database
        if store_accounts:
            with engine.connect() as connection:
                update_sql = text("UPDATE people SET is_store_account = TRUE WHERE user_id = :user_id")
                for user_id in store_accounts:
                    connection.execute(update_sql, {"user_id": user_id})
                connection.commit()
            
            logger.info(f"Updated {len(store_accounts)} users as store accounts")
        
        # STEP 2: Link transfers to transactions
        # Create transaction lookup by user_id and amount
        transaction_lookup = {}
        for _, tx in transactions_df.iterrows():
            user_id = tx['user_id']
            price = round(float(tx['price']), 2)
            tx_id = tx['transaction_id']
            
            key = (user_id, price)
            if key not in transaction_lookup:
                transaction_lookup[key] = []
            transaction_lookup[key].append(tx_id)
        
        # Try to match transfers to transactions
        matched_transfers = []
        
        for idx, transfer in transfers_df.iterrows():
            sender_id = transfer['sender_id']
            amount = round(float(transfer['amount']), 2)
            transfer_id = transfer['transfer_id']
            
            # Look for matching transaction
            key = (sender_id, amount)
            if key in transaction_lookup and transaction_lookup[key]:
                # Use the first matching transaction and remove it from the list
                tx_id = transaction_lookup[key].pop(0)
                matched_transfers.append((transfer_id, tx_id))
        
        # Update transfers in database
        if matched_transfers:
            with engine.connect() as connection:
                update_sql = text("UPDATE transfers SET related_transaction_id = :tx_id WHERE transfer_id = :transfer_id")
                for transfer_id, tx_id in matched_transfers:
                    connection.execute(update_sql, {"transfer_id": transfer_id, "tx_id": tx_id})
                connection.commit()
            
            logger.info(f"Linked {len(matched_transfers)} transfers to transactions")
        
        # STEP 3: Update transactions with store_account_id
        # For each transaction, find the corresponding transfer and set store_account_id
        with engine.connect() as connection:
            update_sql = text("""
                UPDATE transactions
                SET store_account_id = t.recipient_id
                FROM transfers t
                WHERE t.related_transaction_id = transactions.transaction_id
                AND t.recipient_id IN (SELECT user_id FROM people WHERE is_store_account = TRUE)
            """)
            result = connection.execute(update_sql)
            connection.commit()
            
            logger.info(f"Updated {result.rowcount} transactions with store_account_id")
        
    except Exception as e:
        logger.error(f"Error during store account identification and transfer linking: {str(e)}")
        raise

def main():
    """Main function to run the migration."""
    try:
        # Step 1: Update schema
        if not update_schema():
            logger.error("Schema update failed, aborting migration")
            return
        
        # Step 2: Migrate transaction items
        migrate_transaction_items()
        
        # Step 3: Identify store accounts and link transfers to transactions
        identify_store_accounts_and_link_transfers()
        
        logger.info("Migration completed successfully")
    
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()