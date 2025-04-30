#!/usr/bin/env python
"""
Upload processed CSV files directly to the database.

This standalone script can be used to upload previously processed CSV files
to the database without reprocessing the original data.

Usage:
    python upload_csv_to_db.py --dir data/processed
    python upload_csv_to_db.py --dir data/processed --types transactions transaction_items
"""

import os
import sys
import argparse
import pandas as pd
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def upload_csv_to_db(csv_dir, data_types=None, db_config=None):
    """
    Upload CSV files from a directory to the database.
    
    Args:
        csv_dir (str): Directory containing CSV files
        data_types (list, optional): Specific data types to upload
        db_config (dict, optional): Database configuration parameters
    
    Returns:
        dict: Results of database upload with counts of inserted rows
    """
    from src.db.data_loader import DataLoader
    
    # Load database configuration from environment if not provided
    if db_config is None:
        db_config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'database': os.environ.get('DB_NAME', 'venmito'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', 'postgres'),
            'port': os.environ.get('DB_PORT', '5432')
        }
    
    # Define the available data types and their loader methods
    available_types = {
        'people': 'load_people_df',
        'promotions': 'load_promotions_df',
        'transfers': 'load_transfers_df',
        'transactions': 'load_transactions_df',
        'transaction_items': 'load_transaction_items_df',
        'user_transactions': 'load_user_transactions_df',
        'user_transfers': 'load_user_transfers_df',
        'item_summary': 'load_item_summary_df',
        'store_summary': 'load_store_summary_df'
    }
    
    # Use all available types if none specified
    if data_types is None:
        data_types = list(available_types.keys())
    
    # Initialize DataLoader with configuration
    loader = DataLoader(connection_params=db_config, processed_dir=None)
    
    try:
        # Connect to database
        loader.connect()
        print(f"Connected to database {db_config['database']} on {db_config['host']}")
        
        results = {}
        
        # Process each data type
        for data_type in data_types:
            csv_file = os.path.join(csv_dir, f"{data_type}.csv")
            
            if not os.path.exists(csv_file):
                logger.warning(f"CSV file not found: {csv_file}")
                results[data_type] = "SKIPPED: File not found"
                continue
                
            # Check if file is empty
            if os.path.getsize(csv_file) == 0:
                logger.warning(f"Empty CSV file: {csv_file}")
                results[data_type] = "SKIPPED: Empty file"
                continue
            
            logger.info(f"Loading {data_type} from {csv_file}")
            try:
                # Try to read CSV file, handling potential parsing errors
                try:
                    df = pd.read_csv(csv_file)
                except pd.errors.EmptyDataError:
                    logger.warning(f"No data in CSV file: {csv_file}")
                    results[data_type] = "SKIPPED: No data in file"
                    continue
                except Exception as e:
                    logger.error(f"Error parsing CSV file {csv_file}: {str(e)}")
                    results[data_type] = f"ERROR: CSV parsing failed - {str(e)}"
                    continue
                
                if df.empty:
                    logger.warning(f"Empty DataFrame from {csv_file}")
                    results[data_type] = "SKIPPED: Empty DataFrame"
                    continue
                
                # Get appropriate loader method
                method_name = available_types.get(data_type)
                if not method_name or not hasattr(loader, method_name):
                    logger.warning(f"No loader method found for {data_type}")
                    results[data_type] = "SKIPPED: No loader method"
                    continue
                
                # Call the loader method
                method = getattr(loader, method_name)
                count = method(df)
                
                logger.info(f"Loaded {count} rows for {data_type}")
                results[data_type] = count
                
            except Exception as e:
                logger.error(f"Error loading {data_type}: {str(e)}")
                results[data_type] = f"ERROR: {str(e)}"
        
        return results
    
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return {'error': str(e)}
    
    finally:
        # Always disconnect when done
        loader.disconnect()
        logger.info("Database connection closed")


def main():
    """Main function for the script execution."""
    parser = argparse.ArgumentParser(description='Upload CSV files to database')
    parser.add_argument('--dir', '-d', type=str, default='data/processed',
                       help='Directory containing processed CSV files')
    parser.add_argument('--types', '-t', nargs='+', 
                       help='Specific data types to upload (space-separated)')
    parser.add_argument('--env-file', '-e', type=str, default='.env',
                       help='Path to .env file with database credentials')
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv(args.env_file)
    
    # Check if required database environment variables are present
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please ensure these are set in your .env file or environment")
        sys.exit(1)
    
    # Check if directory exists
    if not os.path.isdir(args.dir):
        logger.error(f"Directory not found: {args.dir}")
        sys.exit(1)
    
    # Upload CSV files to database
    print(f"Uploading data from {args.dir} to database...")
    results = upload_csv_to_db(args.dir, args.types)
    
    # Print results
    print("\nUpload results:")
    for data_type, result in results.items():
        print(f"  - {data_type}: {result}")
    
    # Check for errors
    has_errors = any(isinstance(r, str) and r.startswith("ERROR") for r in results.values())
    
    if has_errors:
        print("\nSome errors occurred during upload. Check the logs for details.")
        sys.exit(1)
    else:
        print("\nAll uploads completed successfully!")


if __name__ == "__main__":
    main()