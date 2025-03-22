"""
Database module for Venmito project.

This module provides database connection and operations functionality 
for the Venmito data processing pipeline.
"""

import os
import logging
import psycopg2
from psycopg2 import pool
from typing import Dict, Any, Optional, List, Tuple, Union
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    pass


class Database:
    """Database connection manager class."""
    
    _connection_pool = None
    
    @classmethod
    def initialize(cls, 
                 host: str, 
                 dbname: str, 
                 user: str, 
                 password: str, 
                 port: int = 5432,
                 min_connections: int = 1,
                 max_connections: int = 10):
        """
        Initialize the database connection pool.
        
        Args:
            host (str): Database host
            dbname (str): Database name
            user (str): Database user
            password (str): Database password
            port (int): Database port
            min_connections (int): Minimum number of connections in the pool
            max_connections (int): Maximum number of connections in the pool
        
        Raises:
            DatabaseError: If connection to the database fails
        """
        try:
            cls._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                min_connections,
                max_connections,
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port
            )
            logger.info(f"Initialized database connection pool to {dbname} on {host}")
        except Exception as e:
            error_msg = f"Failed to initialize database connection pool: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    @classmethod
    def close(cls):
        """
        Close all database connections in the pool.
        """
        if cls._connection_pool:
            cls._connection_pool.closeall()
            logger.info("Closed all database connections")
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """
        Get a connection from the pool.
        
        Yields:
            conn: Database connection
        
        Raises:
            DatabaseError: If getting a connection from the pool fails
        """
        if cls._connection_pool is None:
            error_msg = "Database connection pool not initialized"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
        
        conn = None
        try:
            conn = cls._connection_pool.getconn()
            yield conn
        except Exception as e:
            error_msg = f"Error getting connection from pool: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
        finally:
            if conn:
                cls._connection_pool.putconn(conn)
    
    @classmethod
    @contextmanager
    def get_cursor(cls, commit: bool = False):
        """
        Get a cursor from a connection in the pool.
        
        Args:
            commit (bool): Whether to commit changes after executing queries
        
        Yields:
            cursor: Database cursor
        
        Raises:
            DatabaseError: If an error occurs during cursor operations
        """
        with cls.get_connection() as conn:
            cursor = None
            try:
                cursor = conn.cursor()
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                if commit:
                    conn.rollback()
                error_msg = f"Error during cursor operation: {str(e)}"
                logger.error(error_msg)
                raise DatabaseError(error_msg)
            finally:
                if cursor:
                    cursor.close()
    
    @classmethod
    def execute_query(cls, query: str, params: Optional[tuple] = None, commit: bool = False) -> List[tuple]:
        """
        Execute a query with parameters.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            commit (bool): Whether to commit changes after executing the query
        
        Returns:
            List[tuple]: Query results as a list of tuples
        
        Raises:
            DatabaseError: If query execution fails
        """
        results = []
        with cls.get_cursor(commit=commit) as cursor:
            try:
                cursor.execute(query, params)
                if cursor.description:  # Check if the query returns any results
                    results = cursor.fetchall()
            except Exception as e:
                error_msg = f"Error executing query: {str(e)}"
                logger.error(error_msg)
                raise DatabaseError(error_msg)
        
        return results
    
    @classmethod
    def execute_many(cls, query: str, params_list: List[tuple]) -> int:
        """
        Execute a query with multiple parameter sets.
        
        Args:
            query (str): SQL query to execute
            params_list (List[tuple]): List of parameter tuples
        
        Returns:
            int: Number of rows affected
        
        Raises:
            DatabaseError: If query execution fails
        """
        with cls.get_cursor(commit=True) as cursor:
            try:
                cursor.executemany(query, params_list)
                return cursor.rowcount
            except Exception as e:
                error_msg = f"Error executing batch query: {str(e)}"
                logger.error(error_msg)
                raise DatabaseError(error_msg)
    
    @classmethod
    def execute_script(cls, script: str) -> None:
        """
        Execute a SQL script.
        
        Args:
            script (str): SQL script to execute
        
        Raises:
            DatabaseError: If script execution fails
        """
        with cls.get_cursor(commit=True) as cursor:
            try:
                cursor.execute(script)
                logger.info("Successfully executed SQL script")
            except Exception as e:
                error_msg = f"Error executing SQL script: {str(e)}"
                logger.error(error_msg)
                raise DatabaseError(error_msg)


def init_db_from_env():
    """
    Initialize the database connection from environment variables.
    
    Environment variables required:
        - DB_HOST: Database host
        - DB_NAME: Database name
        - DB_USER: Database user
        - DB_PASSWORD: Database password
        - DB_PORT: Database port (optional, defaults to 5432)
    
    Raises:
        DatabaseError: If required environment variables are missing
    """
    try:
        host = os.environ.get('DB_HOST')
        dbname = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        port = int(os.environ.get('DB_PORT', 5432))
        
        if not all([host, dbname, user, password]):
            raise ValueError("Missing required database environment variables")
        
        Database.initialize(host, dbname, user, password, port)
    except Exception as e:
        error_msg = f"Failed to initialize database from environment: {str(e)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg)


def load_schema(schema_file: str) -> None:
    """
    Load database schema from a SQL file.
    
    Args:
        schema_file (str): Path to SQL schema file
    
    Raises:
        DatabaseError: If schema loading fails
    """
    try:
        with open(schema_file, 'r') as f:
            schema_script = f.read()
        
        Database.execute_script(schema_script)
        logger.info(f"Successfully loaded schema from {schema_file}")
    except Exception as e:
        error_msg = f"Failed to load schema from {schema_file}: {str(e)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg)