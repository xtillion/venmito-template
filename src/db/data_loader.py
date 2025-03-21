"""
Database loader module for Venmito project.

This module provides functionality for loading processed data into 
the database from CSV files.
"""

import os
import numpy as np
import datetime
from dateutil.parser import parse
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
import psycopg2
from psycopg2.extras import execute_batch

from src.db.db import Database, DatabaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Class for loading processed data into a PostgreSQL database."""
    
    def __init__(self, connection_params: Dict[str, str], processed_dir: str = 'data/processed'):
        """
        Initialize the database loader with connection parameters.
        
        Args:
            connection_params (Dict[str, str]): PostgreSQL connection parameters
            processed_dir (str): Directory containing processed CSV files
        """
        self.connection_params = connection_params
        self.processed_dir = processed_dir
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL database: {str(e)}")
            raise
    
    def disconnect(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Disconnected from PostgreSQL database")
    
    def load_csv_to_df(self, filename: str) -> pd.DataFrame:
        """
        Load a CSV file from the processed directory into a DataFrame.
        
        Args:
            filename (str): Name of the CSV file (with extension)
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded data
        """
        filepath = os.path.join(self.processed_dir, filename)
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} rows from {filepath}")
            return df
        except Exception as e:
            error_msg = f"Error loading CSV file {filepath}: {str(e)}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
    
    def _prepare_df_for_db(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """
        Prepare DataFrame for database insertion by handling missing values and types.
        
        Args:
            df (pd.DataFrame): DataFrame to prepare
            table_name (str): Target table name (used for logging)
        
        Returns:
            pd.DataFrame: Prepared DataFrame
        """
        # Make a copy to avoid modifying the original
        df = df.copy()
        
        # Handle NaN values
        df.replace([np.nan], [None], inplace=True)
        
        logger.info(f"Prepared {len(df)} rows for insertion into {table_name} table")
        return df
    
    def prepare_parameters(self, data: pd.DataFrame, column_types: Dict[str, Any]) -> List[tuple]:
        """
        Prepare parameters from a DataFrame for database insertion.
        
        Args:
            data (pd.DataFrame): DataFrame containing the data to prepare
            column_types (Dict[str, Any]): Mapping of column names to expected Python types
        
        Returns:
            List[tuple]: List of parameter tuples ready for database insertion
        """
        params = []
        
        for _, row in data.iterrows():
            param_tuple = []
            
            for col, dtype in column_types.items():
                if col not in row:
                    param_tuple.append(None)
                    continue
                    
                value = row[col]
                
                # Handle null values
                if pd.isna(value):
                    param_tuple.append(None)
                elif dtype == int:
                    # For integer columns that can be null, handle empty strings and NaN
                    if value == '' or pd.isna(value):
                        param_tuple.append(None)
                    else:
                        try:
                            param_tuple.append(int(value))
                        except (ValueError, TypeError):
                            # If conversion fails, use None instead of causing an error
                            param_tuple.append(None)
                elif dtype == float:
                    # Handle float conversion
                    try:
                        param_tuple.append(float(value) if not pd.isna(value) else None)
                    except (ValueError, TypeError):
                        param_tuple.append(None)
                elif dtype == str:
                    # Convert to string, but handle NaN/None properly
                    param_tuple.append(str(value) if not pd.isna(value) else None)
                elif dtype == bool:
                    # Handle boolean conversion, treating various values as True/False
                    if isinstance(value, str):
                        lower_value = value.lower()
                        if lower_value in ('yes', 'y', 'true', 't', '1'):
                            param_tuple.append(True)
                        elif lower_value in ('no', 'n', 'false', 'f', '0'):
                            param_tuple.append(False)
                        else:
                            param_tuple.append(None)
                    else:
                        # For non-string values, attempt direct bool conversion
                        try:
                            param_tuple.append(bool(value) if not pd.isna(value) else None)
                        except (ValueError, TypeError):
                            param_tuple.append(None)
                elif dtype == datetime.date or dtype == datetime.datetime:
                    # Handle date/datetime conversion
                    try:
                        if pd.isna(value):
                            param_tuple.append(None)
                        elif isinstance(value, str):
                            parsed_date = parse(value)
                            if dtype == datetime.date:
                                param_tuple.append(parsed_date.date())
                            else:
                                param_tuple.append(parsed_date)
                        elif isinstance(value, (datetime.datetime, datetime.date)):
                            if dtype == datetime.date and isinstance(value, datetime.datetime):
                                param_tuple.append(value.date())
                            else:
                                param_tuple.append(value)
                        else:
                            param_tuple.append(None)
                    except:
                        param_tuple.append(None)
                else:
                    # For other types, try direct conversion or None if not possible
                    try:
                        param_tuple.append(dtype(value) if not pd.isna(value) else None)
                    except (ValueError, TypeError):
                        param_tuple.append(None)
            
            params.append(tuple(param_tuple))
        
        return params
    
    def _df_to_params_list(self, df: pd.DataFrame, columns: List[str]) -> List[tuple]:
        """
        Convert DataFrame rows to a list of parameter tuples for database insertion.
        
        Args:
            df (pd.DataFrame): DataFrame to convert
            columns (List[str]): List of column names to include
        
        Returns:
            List[tuple]: List of parameter tuples
        """
        params_list = []
        
        for _, row in df.iterrows():
            params = tuple(row[col] for col in columns)
            params_list.append(params)
        
        return params_list
    
    # DataFrame-based loading methods
    def load_people_df(self, people_df: pd.DataFrame) -> int:
        """
        Load people data into the database.
        
        Args:
            people_df (pd.DataFrame): DataFrame containing people data
        
        Returns:
            int: Number of records inserted
        """
        if people_df.empty:
            logger.warning("No people data to load")
            return 0
        
        column_types = {
            'user_id': int,
            'first_name': str,
            'last_name': str,
            'email': str,
            'phone': str,
            'city': str,
            'country': str,
            'devices': str,
            'dob': datetime.date
        }
        
        query = """
        INSERT INTO people (user_id, first_name, last_name, email, phone, city, country, devices, dob)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            email = EXCLUDED.email,
            phone = EXCLUDED.phone,
            city = EXCLUDED.city,
            country = EXCLUDED.country,
            devices = EXCLUDED.devices,
            dob = EXCLUDED.dob
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(people_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} people records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading people data: {str(e)}")
            raise
    
    def load_promotions_df(self, promotions_df: pd.DataFrame) -> int:
        """
        Load promotions data into the database.
        
        Args:
            promotions_df (pd.DataFrame): DataFrame containing promotions data
        
        Returns:
            int: Number of records inserted
        """
        if promotions_df.empty:
            logger.warning("No promotions data to load")
            return 0
        
        column_types = {
            'promotion_id': int,
            'user_id': int,  # This can be NULL if no matching user
            'promotion': str,
            'responded': str,
            'promotion_date': datetime.date
        }
        
        query = """
        INSERT INTO promotions (promotion_id, user_id, promotion, responded, promotion_date)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (promotion_id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            promotion = EXCLUDED.promotion,
            responded = EXCLUDED.responded,
            promotion_date = EXCLUDED.promotion_date
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(promotions_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} promotion records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading promotions data: {str(e)}")
            raise
    
    def load_transfers_df(self, transfers_df: pd.DataFrame) -> int:
        """
        Load transfers data into the database.
        
        Args:
            transfers_df (pd.DataFrame): DataFrame containing transfers data
        
        Returns:
            int: Number of records inserted
        """
        if transfers_df.empty:
            logger.warning("No transfers data to load")
            return 0
        
        column_types = {
            'transfer_id': int,
            'sender_id': int,
            'recipient_id': int,
            'amount': float,
            'timestamp': datetime.datetime
        }
        
        query = """
        INSERT INTO transfers (transfer_id, sender_id, recipient_id, amount, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (transfer_id) DO UPDATE SET
            sender_id = EXCLUDED.sender_id,
            recipient_id = EXCLUDED.recipient_id,
            amount = EXCLUDED.amount,
            timestamp = EXCLUDED.timestamp
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(transfers_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} transfer records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading transfers data: {str(e)}")
            raise
    
    def load_transactions_df(self, transactions_df: pd.DataFrame) -> int:
        """
        Load transactions data into the database.
        
        Args:
            transactions_df (pd.DataFrame): DataFrame containing transactions data
        
        Returns:
            int: Number of records inserted
        """
        if transactions_df.empty:
            logger.warning("No transactions data to load")
            return 0
        
        column_types = {
            'transaction_id': str,
            'user_id': int,  # This can be NULL if no matching user
            'item': str,
            'store': str,
            'price': float,
            'quantity': int,
            'price_per_item': float
        }
        
        query = """
        INSERT INTO transactions (transaction_id, user_id, item, store, price, quantity, price_per_item)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            item = EXCLUDED.item,
            store = EXCLUDED.store,
            price = EXCLUDED.price,
            quantity = EXCLUDED.quantity,
            price_per_item = EXCLUDED.price_per_item
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(transactions_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} transaction records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading transactions data: {str(e)}")
            raise
    
    def load_user_transfers_df(self, user_transfers_df: pd.DataFrame) -> int:
        """
        Load user transfer summaries into the database.
        
        Args:
            user_transfers_df (pd.DataFrame): DataFrame containing user transfer summaries
        
        Returns:
            int: Number of records inserted
        """
        if user_transfers_df.empty:
            logger.warning("No user transfer summaries to load")
            return 0
        
        column_types = {
            'user_id': int,
            'total_sent': float,
            'total_received': float,
            'net_transferred': float,
            'sent_count': int,
            'received_count': int,
            'transfer_count': int
        }
        
        query = """
        INSERT INTO user_transfers (user_id, total_sent, total_received, net_transferred, 
                                  sent_count, received_count, transfer_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            total_sent = EXCLUDED.total_sent,
            total_received = EXCLUDED.total_received,
            net_transferred = EXCLUDED.net_transferred,
            sent_count = EXCLUDED.sent_count,
            received_count = EXCLUDED.received_count,
            transfer_count = EXCLUDED.transfer_count
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(user_transfers_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} user transfer summary records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading user transfer summaries: {str(e)}")
            raise
    
    def load_user_transactions_df(self, user_transactions_df: pd.DataFrame) -> int:
        """
        Load user transaction summaries into the database.
        
        Args:
            user_transactions_df (pd.DataFrame): DataFrame containing user transaction summaries
        
        Returns:
            int: Number of records inserted
        """
        if user_transactions_df.empty:
            logger.warning("No user transaction summaries to load")
            return 0
        
        column_types = {
            'user_id': int,
            'total_spent': float,
            'transaction_count': int,
            'favorite_store': str,
            'favorite_item': str
        }
        
        query = """
        INSERT INTO user_transactions (user_id, total_spent, transaction_count, favorite_store, favorite_item)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            total_spent = EXCLUDED.total_spent,
            transaction_count = EXCLUDED.transaction_count,
            favorite_store = EXCLUDED.favorite_store,
            favorite_item = EXCLUDED.favorite_item
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(user_transactions_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} user transaction summary records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading user transaction summaries: {str(e)}")
            raise
    
    def load_item_summary_df(self, item_summary_df: pd.DataFrame) -> int:
        """
        Load item summary data into the database.
        
        Args:
            item_summary_df (pd.DataFrame): DataFrame containing item summaries
        
        Returns:
            int: Number of records inserted
        """
        if item_summary_df.empty:
            logger.warning("No item summary data to load")
            return 0
        
        # Add a sequential ID column if not present
        if 'item_id' not in item_summary_df.columns:
            item_summary_df['item_id'] = range(1, len(item_summary_df) + 1)
        
        column_types = {
            'item_id': int,
            'item': str,
            'total_revenue': float,
            'items_sold': int,
            'transaction_count': int,
            'average_price': float
        }
        
        query = """
        INSERT INTO item_summary (item_id, item, total_revenue, items_sold, transaction_count, average_price)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (item) DO UPDATE SET
            total_revenue = EXCLUDED.total_revenue,
            items_sold = EXCLUDED.items_sold,
            transaction_count = EXCLUDED.transaction_count,
            average_price = EXCLUDED.average_price
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(item_summary_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} item summary records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading item summary data: {str(e)}")
            raise
    
    def load_store_summary_df(self, store_summary_df: pd.DataFrame) -> int:
        """
        Load store summary data into the database.
        
        Args:
            store_summary_df (pd.DataFrame): DataFrame containing store summaries
        
        Returns:
            int: Number of records inserted
        """
        if store_summary_df.empty:
            logger.warning("No store summary data to load")
            return 0
        
        # Add a sequential ID column if not present
        if 'store_id' not in store_summary_df.columns:
            store_summary_df['store_id'] = range(1, len(store_summary_df) + 1)
        
        column_types = {
            'store_id': int,
            'store': str,
            'total_revenue': float,
            'items_sold': int,
            'total_transactions': int,
            'average_transaction_value': float,
            'most_sold_item': str,
            'most_profitable_item': str
        }
        
        query = """
        INSERT INTO store_summary (store_id, store, total_revenue, items_sold, total_transactions,
                                 average_transaction_value, most_sold_item, most_profitable_item)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (store) DO UPDATE SET
            total_revenue = EXCLUDED.total_revenue,
            items_sold = EXCLUDED.items_sold,
            total_transactions = EXCLUDED.total_transactions,
            average_transaction_value = EXCLUDED.average_transaction_value,
            most_sold_item = EXCLUDED.most_sold_item,
            most_profitable_item = EXCLUDED.most_profitable_item
        """
        
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Prepare parameters
            params = self.prepare_parameters(store_summary_df, column_types)
            
            # Execute batch insert
            execute_batch(self.cursor, query, params, page_size=100)
            self.conn.commit()
            
            logger.info(f"Loaded {len(params)} store summary records into database")
            return len(params)
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error loading store summary data: {str(e)}")
            raise
    
    # File-based loading methods
    def load_people(self) -> int:
        """
        Load people data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('people.csv')
            df = self._prepare_df_for_db(df, 'people')
            return self.load_people_df(df)
        except Exception as e:
            error_msg = f"Error loading people data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_promotions(self) -> int:
        """
        Load promotions data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('promotions.csv')
            df = self._prepare_df_for_db(df, 'promotions')
            return self.load_promotions_df(df)
        except Exception as e:
            error_msg = f"Error loading promotions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_transfers(self) -> int:
        """
        Load transfers data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('transfers.csv')
            df = self._prepare_df_for_db(df, 'transfers')
            return self.load_transfers_df(df)
        except Exception as e:
            error_msg = f"Error loading transfers data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_transactions(self) -> int:
        """
        Load transactions data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('transactions.csv')
            df = self._prepare_df_for_db(df, 'transactions')
            return self.load_transactions_df(df)
        except Exception as e:
            error_msg = f"Error loading transactions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_user_transactions(self) -> int:
        """
        Load user transactions summary data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('user_transactions.csv')
            df = self._prepare_df_for_db(df, 'user_transactions')
            return self.load_user_transactions_df(df)
        except Exception as e:
            error_msg = f"Error loading user transactions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_user_transfers(self) -> int:
        """
        Load user transfers summary data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('user_transfers.csv')
            df = self._prepare_df_for_db(df, 'user_transfers')
            return self.load_user_transfers_df(df)
        except Exception as e:
            error_msg = f"Error loading user transfers data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_item_summary(self) -> int:
        """
        Load item summary data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('item_summary.csv')
            df = self._prepare_df_for_db(df, 'item_summary')
            return self.load_item_summary_df(df)
        except Exception as e:
            error_msg = f"Error loading item summary data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_store_summary(self) -> int:
        """
        Load store summary data from CSV into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('store_summary.csv')
            df = self._prepare_df_for_db(df, 'store_summary')
            return self.load_store_summary_df(df)
        except Exception as e:
            error_msg = f"Error loading store summary data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_all(self) -> Dict[str, int]:
        """
        Load all processed data into the database.
        
        Returns:
            Dict[str, int]: Dictionary with table names and number of rows inserted
        
        Raises:
            DatabaseError: If any database insertion fails
        """
        results = {}
        
        # Order matters for foreign key constraints
        try:
            # Ensure we have a database connection
            if not self.conn or not self.cursor:
                self.connect()
                
            # Core tables
            results['people'] = self.load_people()
            results['promotions'] = self.load_promotions()
            results['transfers'] = self.load_transfers()
            results['transactions'] = self.load_transactions()
            
            # Summary tables
            results['user_transactions'] = self.load_user_transactions()
            results['user_transfers'] = self.load_user_transfers()
            results['item_summary'] = self.load_item_summary()
            results['store_summary'] = self.load_store_summary()
            
            logger.info(f"Successfully loaded all data into the database")
            return results
            
        except Exception as e:
            error_msg = f"Error loading all data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
        finally:
            # Always disconnect when done
            self.disconnect()