"""
Database cleanup script for Venmito project.

This script drops all tables and can be used to reset the database before re-initializing.
"""

import logging
import argparse
import os
from dotenv import load_dotenv

from src.db.db import Database, init_db_from_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SQL to drop all tables in the correct order (respecting foreign key constraints)
DROP_TABLES_SQL = """
DROP TABLE IF EXISTS user_transfers CASCADE;
DROP TABLE IF EXISTS user_transactions CASCADE;
DROP TABLE IF EXISTS store_summary CASCADE;
DROP TABLE IF EXISTS item_summary CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS transfers CASCADE;
DROP TABLE IF EXISTS promotions CASCADE;
DROP TABLE IF EXISTS people CASCADE;
"""

def cleanup_database():
    """
    Drop all tables from the database.
    
    Returns:
        bool: True if cleanup succeeded, False otherwise
    """
    try:
        # Initialize database connection
        init_db_from_env()
        
        # Execute drop tables script
        logger.info("Dropping all tables...")
        Database.execute_script(DROP_TABLES_SQL)
        
        logger.info("Database cleanup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during database cleanup: {str(e)}")
        return False
    finally:
        # Close all database connections
        Database.close()

def main():
    """
    Main function to run the database cleanup script.
    """
    parser = argparse.ArgumentParser(description='Clean up Venmito database')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to .env file with database credentials')
    parser.add_argument('--confirm', action='store_true', help='Confirm database cleanup without prompting')
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv(args.env_file)
    
    if not args.confirm:
        confirm = input("This will drop all tables in the database. Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            logger.info("Cleanup cancelled")
            return
    
    success = cleanup_database()
    if success:
        logger.info("Database has been reset. Run init_db.py to re-initialize.")

if __name__ == "__main__":
    main()