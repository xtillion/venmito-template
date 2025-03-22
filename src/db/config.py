"""
Database configuration module for Venmito project.

This module provides the connection to the PostgreSQL database and helper functions.
"""

import os
import logging
from typing import Dict, Any, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection parameters
DB_CONFIG = {
    'dbname': os.environ.get('DB_NAME', 'venmito'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432')
}

def get_db_connection():
    """
    Get a connection to the database.
    
    Returns:
        connection: A PostgreSQL database connection
    """
    try:
        # Return connection with RealDictCursor to get results as dictionaries
        connection = psycopg2.connect(
            **DB_CONFIG,
            cursor_factory=RealDictCursor
        )
        logger.info("Database connection established")
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise


def execute_query(query: str, params: Optional[Dict[str, Any]] = None, fetchall: bool = True):
    """
    Execute a SQL query and return the results.

    Args:
        query (str): SQL query to execute
        params (Dict[str, Any], optional): Parameters for the query
        fetchall (bool): If True, fetch all results, otherwise fetch one

    Returns:
        list or dict: Query results as a list of dictionaries or a single dictionary
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params or {})

            if cursor.description is None:  # No results to fetch (e.g., INSERT/UPDATE)
                connection.commit()
                return None

            if fetchall:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()

            return result
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Query execution error: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()



def execute_transaction(queries: list):
    """
    Execute multiple queries in a single transaction.
    
    Args:
        queries (list): List of (query, params) tuples
    
    Returns:
        list: List of results for each query that returns data
    """
    connection = None
    try:
        connection = get_db_connection()
        results = []
        
        with connection.cursor() as cursor:
            for query, params in queries:
                cursor.execute(query, params or {})
                
                if cursor.description is not None:  # Query returns data
                    results.append(cursor.fetchall())
            
            connection.commit()
        
        return results
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Transaction execution error: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()