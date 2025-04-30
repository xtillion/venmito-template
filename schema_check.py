#!/usr/bin/env python
"""
Check database schema for Venmito.

This script checks the database schema to verify that all required tables,
columns, and constraints are properly defined.
"""

import os
import sys
import argparse
import psycopg2
import psycopg2.extras
import logging
from dotenv import load_dotenv
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection(db_config=None):
    """Create a database connection using provided config or environment vars."""
    if db_config is None:
        db_config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'database': os.environ.get('DB_NAME', 'venmito'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', 'postgres'),
            'port': os.environ.get('DB_PORT', '5432')
        }
    
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def check_table_existence(cursor):
    """Check if all required tables exist in the database."""
    required_tables = [
        'people', 'promotions', 'transfers', 'transactions', 
        'transaction_items', 'user_transactions', 'user_transfers', 
        'item_summary', 'store_summary'
    ]
    
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """
    
    cursor.execute(query)
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    results = []
    for table in required_tables:
        exists = table in existing_tables
        results.append([table, '✓' if exists else '✗'])
    
    print("\n== Table Existence Check ==")
    print(tabulate(results, headers=['Table', 'Exists'], tablefmt='grid'))
    print()
    
    missing_tables = [table for table, exists in results if exists == '✗']
    if missing_tables:
        print(f"WARNING: Missing tables: {', '.join(missing_tables)}")
    else:
        print("All required tables exist.")
    
    return existing_tables

def check_table_constraints(cursor, table_name):
    """Check primary keys and unique constraints for a specific table."""
    # Check primary key
    pk_query = """
    SELECT c.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = %s
    """
    
    cursor.execute(pk_query, (table_name,))
    primary_keys = [row[0] for row in cursor.fetchall()]
    
    # Check unique constraints
    unique_query = """
    SELECT tc.constraint_name, 
           string_agg(ccu.column_name, ', ' ORDER BY ccu.ordinal_position) as columns
    FROM information_schema.table_constraints tc
    JOIN information_schema.constraint_column_usage AS ccu 
      ON ccu.constraint_name = tc.constraint_name 
      AND ccu.constraint_schema = tc.constraint_schema
    WHERE tc.constraint_type = 'UNIQUE' AND tc.table_name = %s
    GROUP BY tc.constraint_name
    """
    
    cursor.execute(unique_query, (table_name,))
    unique_constraints = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Check foreign keys
    fk_query = """
    SELECT
        tc.constraint_name,
        kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
    """
    
    cursor.execute(fk_query, (table_name,))
    foreign_keys = {}
    for row in cursor.fetchall():
        foreign_keys[row[1]] = f"{row[2]}({row[3]})"
    
    return {
        'name': table_name,
        'primary_keys': primary_keys,
        'unique_constraints': unique_constraints,
        'foreign_keys': foreign_keys
    }

def check_all_constraints(cursor, existing_tables):
    """Check constraints for all existing tables."""
    constraint_info = []
    for table in existing_tables:
        info = check_table_constraints(cursor, table)
        constraint_info.append(info)
    
    print("\n== Primary Keys ==")
    pk_data = [[info['name'], ', '.join(info['primary_keys']) or 'None'] 
              for info in constraint_info]
    print(tabulate(pk_data, headers=['Table', 'Primary Keys'], tablefmt='grid'))
    
    print("\n== Unique Constraints ==")
    unique_data = []
    for info in constraint_info:
        if info['unique_constraints']:
            for name, cols in info['unique_constraints'].items():
                unique_data.append([info['name'], name, cols])
        else:
            unique_data.append([info['name'], 'None', 'None'])
    print(tabulate(unique_data, headers=['Table', 'Constraint Name', 'Columns'], tablefmt='grid'))
    
    print("\n== Foreign Keys ==")
    fk_data = []
    for info in constraint_info:
        if info['foreign_keys']:
            for col, ref in info['foreign_keys'].items():
                fk_data.append([info['name'], col, ref])
        else:
            fk_data.append([info['name'], 'None', 'None'])
    print(tabulate(fk_data, headers=['Table', 'Column', 'References'], tablefmt='grid'))
    
    # Check specific requirements for our application
    issues = []
    
    # Check transactions table
    transactions_info = next((info for info in constraint_info if info['name'] == 'transactions'), None)
    if transactions_info:
        if 'transaction_id' not in transactions_info['primary_keys']:
            issues.append("transactions table missing PRIMARY KEY on transaction_id")
    
    # Check transaction_items table
    items_info = next((info for info in constraint_info if info['name'] == 'transaction_items'), None)
    if items_info:
        has_transaction_item_unique = any('transaction_id, item' in cols or 'item, transaction_id' in cols 
                                         for cols in items_info['unique_constraints'].values())
        if not has_transaction_item_unique:
            issues.append("transaction_items table missing UNIQUE constraint on (transaction_id, item)")
    
    # Report any issues found
    if issues:
        print("\n== Schema Issues ==")
        for issue in issues:
            print(f"- {issue}")
        
        print("\nConsider applying these fixes:")
        if "transactions table missing PRIMARY KEY on transaction_id" in issues:
            print("ALTER TABLE transactions ADD PRIMARY KEY (transaction_id);")
        if "transaction_items table missing UNIQUE constraint on (transaction_id, item)" in issues:
            print("ALTER TABLE transaction_items ADD CONSTRAINT transaction_items_unique UNIQUE (transaction_id, item);")
    else:
        print("\nNo schema issues found. All required constraints are in place.")
    
    return constraint_info, issues

def check_sample_data(cursor):
    """Check for sample data in tables."""
    
    tables = ['people', 'transactions', 'transaction_items', 'transfers']
    
    data_info = []
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            data_info.append([table, count])
        except Exception as e:
            data_info.append([table, f"ERROR: {str(e)}"])
    
    print("\n== Sample Data ==")
    print(tabulate(data_info, headers=['Table', 'Row Count'], tablefmt='grid'))

def main():
    parser = argparse.ArgumentParser(description='Check database schema for Venmito')
    parser.add_argument('--env-file', type=str, default='.env',
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
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            print(f"Connected to database {os.environ.get('DB_NAME')} on {os.environ.get('DB_HOST')}")
            
            existing_tables = check_table_existence(cursor)
            constraint_info, issues = check_all_constraints(cursor, existing_tables)
            check_sample_data(cursor)
            
            if issues:
                print("\n⚠️ Schema issues found! Please fix before proceeding.")
                sys.exit(1)
            else:
                print("\n✅ Schema check completed successfully.")
    except Exception as e:
        logger.error(f"Error checking schema: {str(e)}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()