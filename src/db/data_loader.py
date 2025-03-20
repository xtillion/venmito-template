"""
Database loader module for Venmito project.

This module provides functionality for loading processed data into 
the database from CSV files.
"""

import os
import logging
import pandas as pd
from typing import Dict, Any, Optional, List, Union

from src.db.db import Database, DatabaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Class for loading processed data into the database."""
    
    def __init__(self, processed_dir: str = 'data/processed'):
        """
        Initialize the DataLoader.
        
        Args:
            processed_dir (str): Directory containing processed CSV files
        """
        self.processed_dir = processed_dir
        logger.info(f"Initialized DataLoader with processed directory: {processed_dir}")
    
    def load_csv_to_df(self, filename: str) -> pd.DataFrame:
        """
        Load a CSV file into a pandas DataFrame.
        
        Args:
            filename (str): Name of the CSV file (without directory path)
        
        Returns:
            pd.DataFrame: DataFrame containing the CSV data
        
        Raises:
            FileNotFoundError: If the CSV file does not exist
        """
        file_path = os.path.join(self.processed_dir, filename)
        
        if not os.path.exists(file_path):
            error_msg = f"CSV file not found: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            error_msg = f"Error loading CSV file {file_path}: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _prepare_df_for_db(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """
        Prepare a DataFrame for database insertion.
        
        Args:
            df (pd.DataFrame): DataFrame to prepare
            table_name (str): Target database table name
        
        Returns:
            pd.DataFrame: Prepared DataFrame
        """
        # Make a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Handle specific table requirements
        if table_name == 'people':
            # Ensure user_id is present
            if 'user_id' not in df_copy.columns:
                logger.warning("user_id column missing from people data, using index")
                df_copy['user_id'] = df_copy.index + 1
                
        elif table_name == 'promotions':
            # Handle column name differences
            if 'promotion_date' in df_copy.columns and 'date' not in df_copy.columns:
                df_copy['date'] = df_copy['promotion_date']
                logger.info("Renamed promotion_date column to date")
        
        # Fill NA values appropriately
        for col in df_copy.columns:
            if df_copy[col].dtype == 'object':
                df_copy[col] = df_copy[col].fillna('')
            elif 'amount' in col or 'price' in col or 'revenue' in col or 'spent' in col:
                df_copy[col] = df_copy[col].fillna(0.0)
            elif 'count' in col:
                df_copy[col] = df_copy[col].fillna(0).astype(int)
        
        return df_copy
    
    def _df_to_params_list(self, df: pd.DataFrame, columns: List[str]) -> List[tuple]:
        """
        Convert a DataFrame to a list of parameter tuples for database insertion.
        
        Args:
            df (pd.DataFrame): DataFrame to convert
            columns (List[str]): Columns to include in the parameter tuples
        
        Returns:
            List[tuple]: List of parameter tuples
        """
        # Filter the DataFrame to include only specified columns
        filtered_df = df[columns]
        
        # Convert to list of tuples
        params_list = [tuple(row) for row in filtered_df.values]
        
        return params_list
    
    def load_people(self) -> int:
        """
        Load people data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('people.csv')
            df = self._prepare_df_for_db(df, 'people')
            
            columns = ['user_id', 'first_name', 'last_name', 'email', 'city', 'country', 'devices', 'phone']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO people ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (user_id) DO UPDATE
                SET 
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    email = EXCLUDED.email,
                    city = EXCLUDED.city,
                    country = EXCLUDED.country,
                    devices = EXCLUDED.devices,
                    phone = EXCLUDED.phone
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into people table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading people data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_promotions(self) -> int:
        """
        Load promotions data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('promotions.csv')
            df = self._prepare_df_for_db(df, 'promotions')
            
            columns = ['promotion_id', 'user_id', 'promotion', 'responded']
            
            # Handle column rename if needed (promotion_date -> date)
            if 'promotion_date' in df.columns:
                df['date'] = df['promotion_date']
                columns.append('date')
            elif 'date' in df.columns:
                columns.append('date')
                
            # Add amount column if it exists
            if 'amount' in df.columns:
                columns.append('amount')
            
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO promotions ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (promotion_id) DO UPDATE
                SET 
                    user_id = EXCLUDED.user_id,
                    promotion = EXCLUDED.promotion,
                    responded = EXCLUDED.responded
            """
            
            if 'date' in columns:
                query += ", date = EXCLUDED.date"
                
            if 'amount' in columns:
                query += ", amount = EXCLUDED.amount"
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into promotions table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading promotions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_transfers(self) -> int:
        """
        Load transfers data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('transfers.csv')
            df = self._prepare_df_for_db(df, 'transfers')
            
            columns = ['transfer_id', 'sender_id', 'recipient_id', 'amount', 'timestamp']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO transfers ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (transfer_id) DO UPDATE
                SET 
                    sender_id = EXCLUDED.sender_id,
                    recipient_id = EXCLUDED.recipient_id,
                    amount = EXCLUDED.amount,
                    timestamp = EXCLUDED.timestamp
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into transfers table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading transfers data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_transactions(self) -> int:
        """
        Load transactions data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('transactions.csv')
            df = self._prepare_df_for_db(df, 'transactions')
            
            columns = ['transaction_id', 'user_id', 'item', 'store', 'price', 'quantity', 'price_per_item']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO transactions ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (transaction_id) DO UPDATE
                SET 
                    user_id = EXCLUDED.user_id,
                    item = EXCLUDED.item,
                    store = EXCLUDED.store,
                    price = EXCLUDED.price,
                    quantity = EXCLUDED.quantity,
                    price_per_item = EXCLUDED.price_per_item
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into transactions table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading transactions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_user_transactions(self) -> int:
        """
        Load user transactions summary data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('user_transactions.csv')
            df = self._prepare_df_for_db(df, 'user_transactions')
            
            columns = ['user_id', 'total_spent', 'transaction_count', 'favorite_store', 'favorite_item']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO user_transactions ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (user_id) DO UPDATE
                SET 
                    total_spent = EXCLUDED.total_spent,
                    transaction_count = EXCLUDED.transaction_count,
                    favorite_store = EXCLUDED.favorite_store,
                    favorite_item = EXCLUDED.favorite_item
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into user_transactions table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading user transactions data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_user_transfers(self) -> int:
        """
        Load user transfers summary data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('user_transfers.csv')
            df = self._prepare_df_for_db(df, 'user_transfers')
            
            columns = ['user_id', 'total_sent', 'total_received', 'net_transferred', 
                      'sent_count', 'received_count', 'transfer_count']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO user_transfers ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (user_id) DO UPDATE
                SET 
                    total_sent = EXCLUDED.total_sent,
                    total_received = EXCLUDED.total_received,
                    net_transferred = EXCLUDED.net_transferred,
                    sent_count = EXCLUDED.sent_count,
                    received_count = EXCLUDED.received_count,
                    transfer_count = EXCLUDED.transfer_count
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into user_transfers table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading user transfers data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_item_summary(self) -> int:
        """
        Load item summary data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('item_summary.csv')
            df = self._prepare_df_for_db(df, 'item_summary')
            
            # Add a sequential ID column if not present
            if 'item_id' not in df.columns:
                df['item_id'] = range(1, len(df) + 1)
            
            columns = ['item_id', 'item', 'total_revenue', 'items_sold', 
                      'transaction_count', 'average_price']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO item_summary ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (item) DO UPDATE
                SET 
                    total_revenue = EXCLUDED.total_revenue,
                    items_sold = EXCLUDED.items_sold,
                    transaction_count = EXCLUDED.transaction_count,
                    average_price = EXCLUDED.average_price
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into item_summary table")
            return rows_affected
            
        except Exception as e:
            error_msg = f"Error loading item summary data: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def load_store_summary(self) -> int:
        """
        Load store summary data into the database.
        
        Returns:
            int: Number of rows inserted
        
        Raises:
            DatabaseError: If database insertion fails
        """
        try:
            df = self.load_csv_to_df('store_summary.csv')
            df = self._prepare_df_for_db(df, 'store_summary')
            
            # Add a sequential ID column if not present
            if 'store_id' not in df.columns:
                df['store_id'] = range(1, len(df) + 1)
            
            columns = ['store_id', 'store', 'total_revenue', 'items_sold', 
                      'total_transactions', 'average_transaction_value',
                      'most_sold_item', 'most_profitable_item']
            columns = [col for col in columns if col in df.columns]
            
            placeholders = ', '.join(['%s'] * len(columns))
            column_str = ', '.join(columns)
            
            query = f"""
                INSERT INTO store_summary ({column_str})
                VALUES ({placeholders})
                ON CONFLICT (store) DO UPDATE
                SET 
                    total_revenue = EXCLUDED.total_revenue,
                    items_sold = EXCLUDED.items_sold,
                    total_transactions = EXCLUDED.total_transactions,
                    average_transaction_value = EXCLUDED.average_transaction_value,
                    most_sold_item = EXCLUDED.most_sold_item,
                    most_profitable_item = EXCLUDED.most_profitable_item
            """
            
            params_list = self._df_to_params_list(df, columns)
            rows_affected = Database.execute_many(query, params_list)
            
            logger.info(f"Inserted {rows_affected} rows into store_summary table")
            return rows_affected
            
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