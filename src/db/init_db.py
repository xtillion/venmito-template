"""
Database initialization script for Venmito project.

This script initializes the database schema and loads data from processed CSV files.
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

from src.db.db import Database, init_db_from_env, load_schema
from src.db.data_loader import DataLoader, DatabaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database(schema_file: str, load_data: bool = True, processed_dir: str = 'data/processed'):
    """
    Initialize the database schema and optionally load data.
    
    Args:
        schema_file (str): Path to SQL schema file
        load_data (bool): Whether to load data from processed CSV files
        processed_dir (str): Directory containing processed CSV files
    
    Returns:
        bool: True if initialization succeeded, False otherwise
    """
    try:
        # Initialize database connection
        init_db_from_env()
        
        # Load schema
        logger.info(f"Loading database schema from {schema_file}...")
        load_schema(schema_file)
        
        # Optionally load data
        if load_data:
            logger.info(f"Loading data from {processed_dir}...")
            loader = DataLoader(processed_dir)
            results = loader.load_all()
            
            for table, count in results.items():
                logger.info(f"Loaded {count} rows into {table}")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        return False
    finally:
        # Close all database connections
        Database.close()


def main():
    """
    Main function to run the database initialization script.
    """
    parser = argparse.ArgumentParser(description='Initialize Venmito database')
    parser.add_argument('--schema', type=str, default='schema.sql', help='Path to SQL schema file')
    parser.add_argument('--no-data', action='store_true', help='Do not load data from CSV files')
    parser.add_argument('--data-dir', type=str, default='data/processed', help='Directory containing processed CSV files')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to .env file with database credentials')
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv(args.env_file)
    
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error(f"Please set them in the {args.env_file} file")
        sys.exit(1)
    
    schema_file = args.schema
    if not os.path.exists(schema_file):
        logger.error(f"Schema file not found: {schema_file}")
        sys.exit(1)
    
    load_data = not args.no_data
    if load_data and not os.path.exists(args.data_dir):
        logger.error(f"Data directory not found: {args.data_dir}")
        sys.exit(1)
    
    success = init_database(schema_file, load_data, args.data_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()