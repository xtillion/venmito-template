#!/usr/bin/env python
# src/db/init_db.py

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

from src.db.db import Database, init_db_from_env, load_schema
from src.db.data_loader import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database(schema_file, processed_dir='data/processed'):
    """Initialize the database using the DataLoader class."""
    try:
        # Initialize database connection
        init_db_from_env()
        
        # Load schema
        logger.info(f"Loading database schema from {schema_file}...")
        load_schema(schema_file)
        
        # Initialize data loader
        loader = DataLoader(processed_dir=processed_dir)
        
        # Load all data
        logger.info("Loading all data into the database...")
        results = loader.load_all()
        
        # Report results
        for table, count in results.items():
            logger.info(f"Loaded {count} rows into {table} table")
        
        logger.info("Database initialization completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        return False
    finally:
        Database.close()

def main():
    parser = argparse.ArgumentParser(description='Initialize Venmito database')
    parser.add_argument('--schema', type=str, default='schema.sql', help='Path to SQL schema file')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to .env file with database credentials')
    parser.add_argument('--data-dir', type=str, default='data/processed', help='Path to processed data directory')
    
    args = parser.parse_args()
    
    load_dotenv(args.env_file)
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    schema_file = args.schema
    if not os.path.exists(schema_file):
        logger.error(f"Schema file not found: {schema_file}")
        sys.exit(1)
    
    data_dir = args.data_dir
    if not os.path.exists(data_dir):
        logger.error(f"Data directory not found: {data_dir}")
        sys.exit(1)
    
    success = init_database(schema_file, data_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()