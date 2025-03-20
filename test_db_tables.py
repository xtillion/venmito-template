#!/usr/bin/env python
# test_db_tables.py

import os
import sys
import logging
import random
from dotenv import load_dotenv

from src.db.db import Database, init_db_from_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def random_id(prefix=""):
    """Generate a random ID that's unlikely to conflict with existing IDs."""
    random_num = random.randint(10000000, 99999999)  # 8-digit number
    return f"{prefix}{random_num}"

def convert_to_dict(columns, row):
    """Convert a row tuple to a dictionary using column names."""
    return {columns[i][0]: row[i] for i in range(len(columns))}

def test_table_structure(table):
    """Test that a table exists and get its column information."""
    try:
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
        """
        columns = Database.execute_query(query, (table,))
        
        if not columns:
            logger.error(f"Table {table} does not exist or has no columns")
            return False
        
        # Convert results to a more readable format
        column_info = []
        for row in columns:
            column_info.append({"column_name": row[0], "data_type": row[1]})
        
        logger.info(f"Table {table} exists with {len(column_info)} columns")
        for col in column_info:
            logger.info(f"  - {col['column_name']} ({col['data_type']})")
        
        return True
    except Exception as e:
        logger.error(f"Error checking table structure for {table}: {str(e)}")
        return False

def test_insert_and_query(table, test_data, select_by=None):
    """Test inserting data into a table and querying it."""
    try:
        # Get column names and values
        columns = list(test_data.keys())
        values = list(test_data.values())
        
        # Build the insert query
        column_str = ', '.join(columns)
        placeholder_str = ', '.join(['%s'] * len(columns))
        
        # Insert query with ON CONFLICT DO NOTHING
        insert_query = f"INSERT INTO {table} ({column_str}) VALUES ({placeholder_str}) ON CONFLICT DO NOTHING"
        
        # Execute insert
        Database.execute_query(insert_query, tuple(values), commit=True)
        logger.info(f"Successfully inserted test data into {table} table")
        
        # Build the select query
        where_clause = ""
        where_params = []
        if select_by:
            where_parts = []
            for col, val in select_by.items():
                where_parts.append(f"{col} = %s")
                where_params.append(val)
            where_clause = "WHERE " + " AND ".join(where_parts)
        
        # Execute select
        select_query = f"SELECT COUNT(*) FROM {table} {where_clause}"
        result = Database.execute_query(select_query, tuple(where_params))
        count = result[0][0] if result else 0
        
        logger.info(f"Successfully queried {table} table, found {count} matching rows")
        return count > 0
    
    except Exception as e:
        logger.error(f"Error testing {table} table: {str(e)}")
        return False

def test_all_tables():
    """Test all tables in the database."""
    try:
        # Initialize database connection
        init_db_from_env()
        
        # First test that we can connect and list tables
        tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """
        table_results = Database.execute_query(tables_query)
        
        if not table_results:
            logger.error("No tables found in the database")
            return False
        
        # Extract table names from results
        table_names = [row[0] for row in table_results]
        logger.info(f"Found {len(table_names)} tables: {', '.join(table_names)}")
        
        # Now test each expected table structure
        expected_tables = [
            'people', 'promotions', 'transfers', 'transactions', 
            'user_transactions', 'user_transfers', 'item_summary', 'store_summary'
        ]
        
        structure_results = {}
        for table in expected_tables:
            if table in table_names:
                structure_results[table] = test_table_structure(table)
            else:
                logger.error(f"Expected table {table} not found in database")
                structure_results[table] = False
        
        # Generate random test IDs
        test_user_id = random_id()
        test_people_id = random_id()
        test_promotion_id = random_id()
        test_transfer_id = random_id()
        test_transaction_id = f"T{random_id()}"
        test_item_id = random_id()
        test_store_id = random_id()
        
        # Test data for each table
        test_data = {
            'people': {
                'user_id': test_people_id,
                'first_name': 'Test',
                'last_name': 'User',
                'email': f'test{random_id()}@example.com',
                'city': 'Test City',
                'country': 'Test Country',
                'devices': 'Test Device',
                'phone': f'+1{random_id()}'
            },
            'people_secondary': {  # Need a second user for recipient
                'user_id': test_user_id,
                'first_name': 'Test2',
                'last_name': 'User2',
                'email': f'test{random_id()}@example.com',
                'city': 'Test City2',
                'country': 'Test Country2',
                'devices': 'Test Device2',
                'phone': f'+1{random_id()}'
            },
            'promotions': {
                'promotion_id': test_promotion_id,
                'user_id': test_people_id,
                'promotion': f'Test Promotion {random_id()}',
                'responded': 'Yes'
            },
            'transfers': {
                'transfer_id': test_transfer_id,
                'sender_id': test_people_id,
                'recipient_id': test_user_id,  # Using the second user
                'amount': 100.00
            },
            'transactions': {
                'transaction_id': test_transaction_id,
                'user_id': test_people_id,
                'item': f'Test Item {random_id()}',
                'store': f'Test Store {random_id()}',
                'price': 100.00,
                'quantity': 1,
                'price_per_item': 100.00
            },
            'user_transactions': {
                'user_id': test_people_id,
                'total_spent': 100.00,
                'transaction_count': 1,
                'favorite_store': f'Test Store {random_id()}',
                'favorite_item': f'Test Item {random_id()}'
            },
            'user_transfers': {
                'user_id': test_people_id,
                'total_sent': 100.00,
                'total_received': 0.00,
                'net_transferred': -100.00,
                'sent_count': 1,
                'received_count': 0,
                'transfer_count': 1
            },
            'item_summary': {
                'item_id': test_item_id,
                'item': f'Test Item Summary {random_id()}',
                'total_revenue': 100.00,
                'items_sold': 1,
                'transaction_count': 1,
                'average_price': 100.00
            },
            'store_summary': {
                'store_id': test_store_id,
                'store': f'Test Store Summary {random_id()}',
                'total_revenue': 100.00,
                'items_sold': 1,
                'total_transactions': 1,
                'average_transaction_value': 100.00,
                'most_sold_item': f'Test Item {random_id()}',
                'most_profitable_item': f'Test Item {random_id()}'
            }
        }
        
        # Select where clauses for each table
        select_by = {
            'people': {'user_id': test_people_id},
            'promotions': {'promotion_id': test_promotion_id},
            'transfers': {'transfer_id': test_transfer_id},
            'transactions': {'transaction_id': test_transaction_id},
            'user_transactions': {'user_id': test_people_id},
            'user_transfers': {'user_id': test_people_id},
            'item_summary': {'item_id': test_item_id},
            'store_summary': {'store_id': test_store_id}
        }
        
        # Insert test results
        insert_results = {}
        
        # First insert people (needed for foreign key constraints)
        insert_results['people'] = test_insert_and_query('people', test_data['people'], select_by['people'])
        
        # Insert secondary person (for transfer recipient)
        test_insert_and_query('people', test_data['people_secondary'], {'user_id': test_user_id})
        
        # Test remaining tables
        for table in ['promotions', 'transfers', 'transactions', 'user_transactions', 
                     'user_transfers', 'item_summary', 'store_summary']:
            insert_results[table] = test_insert_and_query(table, test_data[table], select_by[table])
        
        # Report results
        all_passed = True
        for table, passed in structure_results.items():
            status = "PASS" if passed else "FAIL"
            if passed:
                logger.info(f"Table structure {table}: {status}")
            else:
                logger.error(f"Table structure {table}: {status}")
                all_passed = False
        
        for table, passed in insert_results.items():
            status = "PASS" if passed else "FAIL"
            if passed:
                logger.info(f"Table insert/query {table}: {status}")
            else:
                logger.error(f"Table insert/query {table}: {status}")
                all_passed = False
        
        return all_passed
    
    except Exception as e:
        logger.error(f"Error during database testing: {str(e)}")
        return False
    finally:
        Database.close()

def main():
    load_dotenv('.env')
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    success = test_all_tables()
    
    if success:
        logger.info("All database table tests passed successfully")
        sys.exit(0)
    else:
        logger.error("One or more database table tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()