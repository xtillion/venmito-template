"""
Data processing module for Venmito project.

This module provides classes for cleaning and transforming data
from various sources into a standardized format.
"""

import logging
import re
from typing import List, Dict, Any, Optional, Union, Callable, Tuple

import pandas as pd
import numpy as np

from src.data.processor_base import DataProcessor, get_processor, logger

# Configure logger
logger = logging.getLogger(__name__)


class PeopleProcessor(DataProcessor):
    """Processor for people data."""
    
    def _standardize_devices(self) -> None:
        """Standardize device information into a consistent format."""
        # Handle different formats of device information
        if 'devices' in self.df.columns:
            def standardize_device_list(devices):
                if pd.isna(devices):
                    return ''
                elif isinstance(devices, list):
                    return ', '.join(sorted(devices))
                elif isinstance(devices, str):
                    # Already a string, ensure consistent format
                    device_list = [d.strip() for d in devices.split(',')]
                    return ', '.join(sorted(device_list))
                else:
                    return str(devices)
            
            self._apply_to_column('devices', standardize_device_list, 
                                "Error standardizing device information in column")
            logger.info("Standardized device information")
        
        # Handle binary indicator columns
        device_columns = ['Android', 'Iphone', 'Desktop']
        if all(col in self.df.columns for col in device_columns):
            try:
                # Create a new devices column from binary indicators
                def get_devices_from_indicators(row):
                    devices = []
                    if row.get('Android') == 1:
                        devices.append('Android')
                    if row.get('Iphone') == 1:
                        devices.append('Iphone')
                    if row.get('Desktop') == 1:
                        devices.append('Desktop')
                    return ', '.join(devices) if devices else ''
                
                self.df['devices'] = self.df.apply(get_devices_from_indicators, axis=1)
                self._drop_columns(device_columns)
                logger.info("Created devices column from binary indicators")
            except Exception as e:
                self._add_error(f"Failed to standardize device indicators: {str(e)}")
    
    def _standardize_location(self) -> None:
        """Standardize location information (city, country)."""
        # Handle nested location data (e.g., from JSON)
        if 'location' in self.df.columns:
            try:
                # Check if location column contains dictionaries
                if isinstance(self.df['location'].iloc[0], dict):
                    location_df = pd.json_normalize(self.df['location'])
                    
                    # Make column names consistent
                    location_df.rename(columns={
                        'City': 'city', 
                        'Country': 'country'
                    }, inplace=True)
                    
                    # Add normalized columns to main dataframe
                    for col in ['city', 'country']:
                        if col in location_df.columns:
                            self.df[col] = location_df[col]
                    
                    self._drop_columns(['location'])
                    logger.info("Extracted location information from nested dictionaries")
            except Exception as e:
                self._add_error(f"Failed to standardize location dictionary: {str(e)}")
        
        # Handle combined city/country format (e.g., "New York, USA")
        if 'city' in self.df.columns and 'country' not in self.df.columns:
            try:
                # Try to split on comma
                if self.df['city'].str.contains(',').any():
                    city_country = self.df['city'].str.split(',', expand=True)
                    if len(city_country.columns) > 1:
                        self.df['city'] = city_country[0].str.strip()
                        self.df['country'] = city_country[1].str.strip()
                        logger.info("Split city/country combined field")
            except Exception as e:
                self._add_error(f"Failed to split city/country field: {str(e)}")
    
    def _standardize_name(self) -> None:
        """Standardize name information (split into first_name and last_name if needed)."""
        # Handle combined name (e.g., "John Doe")
        if 'name' in self.df.columns and not all(col in self.df.columns for col in ['first_name', 'last_name']):
            try:
                # Split name into first and last name
                names = self.df['name'].str.split(n=1, expand=True)
                
                if len(names.columns) > 0:
                    self.df['first_name'] = names[0]
                    
                if len(names.columns) > 1:
                    self.df['last_name'] = names[1]
                    
                logger.info("Split name into first_name and last_name")
            except Exception as e:
                self._add_error(f"Failed to split name field: {str(e)}")
    
    def _standardize_phone(self) -> None:
        """Standardize phone numbers to a consistent format."""
        phone_columns = ['phone', 'telephone']
        target_column = 'phone'
        
        # Find which phone column exists
        existing_column = next((col for col in phone_columns if col in self.df.columns), None)
        
        if existing_column:
            # If the column is not already called 'phone', rename it
            if existing_column != target_column:
                self._rename_columns({existing_column: target_column})
            
            # Standardize phone format
            def clean_phone(phone):
                if pd.isna(phone):
                    return None
                
                # Convert to string and remove non-numeric characters except + for country code
                phone_str = str(phone)
                # Keep + at the beginning if it exists
                if phone_str.startswith('+'):
                    return '+' + re.sub(r'[^0-9]', '', phone_str[1:])
                else:
                    
                    return re.sub(r'[^0-9]', '', phone_str)
            
            self._apply_to_column(target_column, clean_phone, 
                                "Error standardizing phone number in column")
            logger.info("Standardized phone numbers")
    
    def _standardize_id(self) -> None:
        """Standardize ID field to ensure it's named consistently and has the right type."""
        # Ensure ID column is named 'user_id'
        if 'id' in self.df.columns and 'user_id' not in self.df.columns:
            self._rename_columns({'id': 'user_id'})
        
        # Ensure ID is an integer
        if 'user_id' in self.df.columns:
            try:
                self.df['user_id'] = self.df['user_id'].astype(int)
                logger.info("Converted user_id to integer type")
            except Exception as e:
                self._add_error(f"Failed to convert user_id to integer: {str(e)}")
    
    def process(self) -> pd.DataFrame:
        """
        Process people data to standardize format.
        
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        try:
            logger.info("Processing people data...")
            
            # Standardize various fields
            self._standardize_id()
            self._standardize_devices()
            self._standardize_location()
            self._standardize_name()
            self._standardize_phone()
            
            # Normalize text fields
            for column in ['email', 'city', 'country']:
                if column in self.df.columns:
                    self._normalize_text(column)
            
            # Fill missing values for non-critical fields
            self._fill_missing_values('devices', '')
            
            logger.info(f"Completed processing people data. Result shape: {self.df.shape}")
            return self.df
            
        except Exception as e:
            error_msg = f"Unexpected error in people data processing: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return self.df


class PromotionsProcessor(DataProcessor):
    """Processor for promotions data."""
    
    def _standardize_ids(self) -> None:
        """Standardize ID fields to ensure they're named consistently and have the right type."""
        # Ensure promotion ID column is named 'promotion_id'
        if 'id' in self.df.columns and 'promotion_id' not in self.df.columns:
            self._rename_columns({'id': 'promotion_id'})
        
        # Ensure promotion_id is an integer
        if 'promotion_id' in self.df.columns:
            try:
                self.df['promotion_id'] = self.df['promotion_id'].astype(int)
                logger.info("Converted promotion_id to integer type")
            except Exception as e:
                self._add_error(f"Failed to convert promotion_id to integer: {str(e)}")
    
    def _standardize_user_references(self) -> None:
        """Standardize user references to use user_id consistently."""
        # Check if we have user_id already
        if 'user_id' in self.df.columns and not self.df['user_id'].isna().all():
            # Already have user_id, ensure it's an integer
            try:
                self.df['user_id'] = self.df['user_id'].fillna(-1).astype(int)
                self.df.loc[self.df['user_id'] == -1, 'user_id'] = None
                logger.info("Standardized user_id references")
            except Exception as e:
                self._add_error(f"Failed to standardize user_id: {str(e)}")
        
        # No further processing needed here - user ID mapping is typically handled in the merger
    
    def _standardize_response(self) -> None:
        """Standardize response values to Yes/No format."""
        if 'responded' in self.df.columns:
            def standardize_response(value):
                if pd.isna(value):
                    return None
                
                value_str = str(value).strip().lower()
                
                if value_str in ['yes', 'y', 'true', '1']:
                    return 'Yes'
                elif value_str in ['no', 'n', 'false', '0']:
                    return 'No'
                else:
                    return value  # Keep original if it doesn't match
            
            self._apply_to_column('responded', standardize_response, 
                                "Error standardizing response values in column")
            logger.info("Standardized response values")
    
    def _standardize_promotion_names(self) -> None:
        """Standardize promotion names to be consistently formatted."""
        if 'promotion' in self.df.columns:
            # Normalize promotion names
            self._normalize_text('promotion')
            
            # Additional specific normalization for promotion names
            def clean_promotion_name(name):
                if pd.isna(name):
                    return None
                
                # Replace underscores with spaces
                name = str(name).replace('_', ' ')
                
                # Capitalize first letter of each word
                name = ' '.join(word.capitalize() for word in name.split())
                
                return name
            
            self._apply_to_column('promotion', clean_promotion_name,
                                "Error standardizing promotion names in column")
            logger.info("Standardized promotion names")
    
    def process(self) -> pd.DataFrame:
        """
        Process promotions data to standardize format.
        
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        try:
            logger.info("Processing promotions data...")
            
            # Standardize various fields
            self._standardize_ids()
            self._standardize_user_references()
            self._standardize_response()
            self._standardize_promotion_names()
            
            # Drop unnecessary columns that might be present
            unnecessary_columns = []
            self._drop_columns(unnecessary_columns)
            
            logger.info(f"Completed processing promotions data. Result shape: {self.df.shape}")
            return self.df
            
        except Exception as e:
            error_msg = f"Unexpected error in promotions data processing: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return self.df


class TransfersProcessor(DataProcessor):
    """Processor for transfers data."""
    
    def _standardize_ids(self) -> None:
        """Standardize ID fields to ensure they're named consistently and have the right type."""
        # Add transfer_id if it doesn't exist
        if 'transfer_id' not in self.df.columns:
            if 'id' in self.df.columns:
                self._rename_columns({'id': 'transfer_id'})
            else:
                # Create a new transfer_id column
                self.df['transfer_id'] = range(1, len(self.df) + 1)
                logger.info("Created transfer_id column")
        
        # Ensure IDs are integers
        for id_column in ['transfer_id', 'sender_id', 'recipient_id']:
            if id_column in self.df.columns:
                try:
                    self.df[id_column] = self.df[id_column].astype(int)
                    logger.info(f"Converted {id_column} to integer type")
                except Exception as e:
                    self._add_error(f"Failed to convert {id_column} to integer: {str(e)}")
    
    def _standardize_amount(self) -> None:
        """Standardize amount field to ensure it's a numeric value."""
        if 'amount' in self.df.columns:
            try:
                # Convert to numeric, coercing errors to NaN
                self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
                
                # Log warning about any values that couldn't be converted
                nan_count = self.df['amount'].isna().sum()
                if nan_count > 0:
                    self._add_error(f"Found {nan_count} non-numeric values in amount column")
                
                # Round to 2 decimal places for currency
                self.df['amount'] = self.df['amount'].round(2)
                
                logger.info("Standardized amount column")
            except Exception as e:
                self._add_error(f"Failed to standardize amount column: {str(e)}")
    
    def _standardize_timestamp(self) -> None:
        """Standardize timestamp field to ensure it's a datetime."""
        timestamp_columns = ['timestamp', 'date', 'transfer_date']
        
        # Find which timestamp column exists
        existing_column = next((col for col in timestamp_columns if col in self.df.columns), None)
        
        if existing_column:
            try:
                # Convert to datetime
                self.df[existing_column] = pd.to_datetime(self.df[existing_column], errors='coerce')
                
                # Rename to 'timestamp' if needed
                if existing_column != 'timestamp':
                    self._rename_columns({existing_column: 'timestamp'})
                
                logger.info("Standardized timestamp column")
            except Exception as e:
                self._add_error(f"Failed to standardize timestamp column: {str(e)}")
    
    def process(self) -> pd.DataFrame:
        """
        Process transfers data to standardize format.
        
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        try:
            logger.info("Processing transfers data...")
            
            # Standardize various fields
            self._standardize_ids()
            self._standardize_amount()
            self._standardize_timestamp()
            
            # Verify sender and recipient are different
            if all(col in self.df.columns for col in ['sender_id', 'recipient_id']):
                same_ids = self.df['sender_id'] == self.df['recipient_id']
                if same_ids.any():
                    count = same_ids.sum()
                    self._add_error(f"Found {count} transfers where sender_id equals recipient_id")
            
            logger.info(f"Completed processing transfers data. Result shape: {self.df.shape}")
            return self.df
            
        except Exception as e:
            error_msg = f"Unexpected error in transfers data processing: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return self.df


class TransactionsProcessor(DataProcessor):
    """Processor for transactions data."""
    
    def _standardize_ids(self) -> None:
        """Standardize ID fields to ensure they're named consistently and have the right type."""
        # Ensure transaction ID column is named 'transaction_id'
        if 'id' in self.df.columns and 'transaction_id' not in self.df.columns:
            self._rename_columns({'id': 'transaction_id'})
        
        # Ensure transaction_id is string (since it might contain alphanumeric values)
        if 'transaction_id' in self.df.columns:
            try:
                self.df['transaction_id'] = self.df['transaction_id'].astype(str)
                logger.info("Converted transaction_id to string type")
            except Exception as e:
                self._add_error(f"Failed to convert transaction_id to string: {str(e)}")
        
        # Ensure user_id is integer if present
        if 'user_id' in self.df.columns:
            try:
                # Handle potentially null values
                mask = self.df['user_id'].notna()
                if mask.any():
                    self.df.loc[mask, 'user_id'] = self.df.loc[mask, 'user_id'].astype(int)
                    logger.info("Converted user_id to integer type")
            except Exception as e:
                self._add_error(f"Failed to convert user_id to integer: {str(e)}")
    
    def _standardize_numeric_fields(self) -> None:
        """Standardize numeric fields (price, quantity, price_per_item)."""
        numeric_fields = ['price', 'quantity', 'price_per_item']
        
        for field in numeric_fields:
            if field in self.df.columns:
                try:
                    # Convert to numeric, coercing errors to NaN
                    self.df[field] = pd.to_numeric(self.df[field], errors='coerce')
                    
                    # Log warning about any values that couldn't be converted
                    nan_count = self.df[field].isna().sum()
                    if nan_count > 0:
                        self._add_error(f"Found {nan_count} non-numeric values in {field} column")
                    
                    # Set some sensible defaults for missing values
                    if field == 'quantity' and self.df[field].isna().any():
                        self.df[field].fillna(1, inplace=True)
                        logger.info(f"Filled missing values in {field} with 1")
                    
                    # Round price fields to 2 decimal places
                    if field in ['price', 'price_per_item']:
                        self.df[field] = self.df[field].round(2)
                    
                    logger.info(f"Standardized {field} column")
                except Exception as e:
                    self._add_error(f"Failed to standardize {field} column: {str(e)}")
    
    def _standardize_item_and_store_names(self) -> None:
        """Standardize item and store names to be consistently formatted."""
        for field in ['item', 'store']:
            if field in self.df.columns:
                # Basic normalization (lowercase, strip whitespace)
                self._normalize_text(field)
                
                # Additional specific normalization
                def clean_name(name):
                    if pd.isna(name):
                        return None
                    
                    # Replace underscores with spaces
                    name = str(name).replace('_', ' ')
                    
                    # Capitalize first letter of each word
                    name = ' '.join(word.capitalize() for word in name.split())
                    
                    return name
                
                self._apply_to_column(field, clean_name,
                                    f"Error standardizing {field} names")
                logger.info(f"Standardized {field} names")
    
    def _validate_price_and_quantity(self) -> None:
        """Validate price and quantity fields for consistency."""
        if all(col in self.df.columns for col in ['price', 'quantity', 'price_per_item']):
            try:
                # Check if price = price_per_item * quantity
                expected_price = (self.df['price_per_item'] * self.df['quantity']).round(2)
                actual_price = self.df['price'].round(2)
                
                # Calculate discrepancy
                discrepancy = (actual_price - expected_price).abs()
                inconsistent = discrepancy > 0.01  # Allow small rounding differences
                
                if inconsistent.any():
                    count = inconsistent.sum()
                    self._add_error(f"Found {count} transactions with inconsistent price, price_per_item, and quantity")
                    
                    # Fix the inconsistency by recalculating price_per_item
                    mask = (inconsistent & (self.df['quantity'] > 0))
                    if mask.any():
                        self.df.loc[mask, 'price_per_item'] = (
                            self.df.loc[mask, 'price'] / self.df.loc[mask, 'quantity']
                        ).round(2)
                        logger.info("Recalculated price_per_item for inconsistent transactions")
            except Exception as e:
                self._add_error(f"Failed to validate price consistency: {str(e)}")
    
    def _standardize_date(self) -> None:
        """Standardize date field to ensure it's converted to a proper timestamp."""
        if 'date' in self.df.columns:
            try:
                # Convert to datetime and create transaction_date column
                self.df['transaction_date'] = pd.to_datetime(self.df['date'], errors='coerce')
                
                # Check for any dates that couldn't be parsed
                invalid_dates = self.df['transaction_date'].isna() & self.df['date'].notna()
                if invalid_dates.any():
                    invalid_count = invalid_dates.sum()
                    self._add_error(f"Found {invalid_count} invalid date values")
                
                logger.info("Converted date to transaction_date")
            except Exception as e:
                self._add_error(f"Failed to standardize date: {str(e)}")
        else:
            # If no date column exists, add a default date (this is optional)
            self.df['transaction_date'] = pd.Timestamp.now()
            logger.info("No date column found, added current timestamp as transaction_date")

    def _process_transaction_items(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process transaction items into separate DataFrames.
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (transaction_df, transaction_items_df)
        """
        # Create a copy of the original DataFrame for transactions
        transaction_df = self.df.copy()
        
        # Create an empty DataFrame for transaction items
        items_columns = ['transaction_id', 'item', 'quantity', 'price_per_item', 'subtotal']
        transaction_items_df = pd.DataFrame(columns=items_columns)
        
        # Temporary list to hold item rows
        items_rows = []
        
        # Process each transaction row
        for idx, row in transaction_df.iterrows():
            transaction_id = row['transaction_id']
            
            # Check if item is a comma-separated list
            if isinstance(row['item'], str) and ',' in row['item']:
                items = [item.strip() for item in row['item'].split(',')]
                
                # If we have quantities for each item
                if isinstance(row['quantity'], str) and ',' in row['quantity']:
                    quantities = [int(q.strip()) for q in row['quantity'].split(',')]
                else:
                    # Default to equal distribution if single quantity
                    quantities = [row['quantity'] // len(items)] * len(items)
                    # Add remainder to first item
                    quantities[0] += row['quantity'] % len(items)
                
                # Calculate price per item based on total price
                if len(items) > 1:
                    # Distribute price evenly if multiple items
                    price_per_item = [row['price'] / row['quantity']] * len(items)
                else:
                    # Use existing price_per_item if available
                    price_per_item = [row['price_per_item'] if 'price_per_item' in row else row['price'] / row['quantity']]
                
                # Create item rows
                for i, (item, qty, price) in enumerate(zip(items, quantities, price_per_item)):
                    subtotal = qty * price
                    items_rows.append({
                        'transaction_id': transaction_id,
                        'item': item,
                        'quantity': qty,
                        'price_per_item': price,
                        'subtotal': subtotal
                    })
            else:
                # Single item transaction
                subtotal = row['quantity'] * (row['price_per_item'] if 'price_per_item' in row else row['price'] / row['quantity'])
                items_rows.append({
                    'transaction_id': transaction_id,
                    'item': row['item'],
                    'quantity': row['quantity'],
                    'price_per_item': row['price_per_item'] if 'price_per_item' in row else row['price'] / row['quantity'],
                    'subtotal': subtotal
                })
        
        # Create the transaction items DataFrame
        if items_rows:
            transaction_items_df = pd.DataFrame(items_rows)
        
        # Remove item-specific columns from transaction_df
        if 'item' in transaction_df.columns:
            transaction_df.drop(columns=['item', 'quantity', 'price_per_item'], inplace=True, errors='ignore')
        
        return transaction_df, transaction_items_df

    def process(self) -> Dict[str, pd.DataFrame]:
        """
        Process transactions data and return both transactions and transaction_items DataFrames.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with processed DataFrames
        """
        try:
            logger.info("Processing transactions data...")
            
            # Standardize various fields
            self._standardize_ids()
            self._standardize_numeric_fields()
            self._standardize_item_and_store_names()
            self._standardize_date()
            self._validate_price_and_quantity()
            
            # Process transaction items
            transactions_df, transaction_items_df = self._process_transaction_items()
            
            logger.info(f"Completed processing transactions data. Result shapes: " +
                    f"transactions {transactions_df.shape}, items {transaction_items_df.shape}")
            
            return {
                'transactions': transactions_df,
                'transaction_items': transaction_items_df
            }
            
        except Exception as e:
            error_msg = f"Unexpected error in transactions data processing: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'transactions': self.df, 'transaction_items': pd.DataFrame()}

# Dictionary mapping data types to processor classes
PROCESSOR_MAP = {
    'people': PeopleProcessor,
    'promotions': PromotionsProcessor,
    'transfers': TransfersProcessor,
    'transactions': TransactionsProcessor
}


# Convenience function for direct processing
def process_dataframe(df: pd.DataFrame, data_type: str) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Process a DataFrame for a specific data type.
    
    Args:
        df (pd.DataFrame): DataFrame to process
        data_type (str): Type of data to process ('people', 'promotions', 'transfers', 'transactions')
    
    Returns:
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]: Processed DataFrame(s)
                                                     Returns a dictionary for 'transactions' type
    
    Raises:
        ValueError: If the data type is not supported
    """
    processor = get_processor(data_type, df, PROCESSOR_MAP)
    result = processor.process()
    
    # TransactionsProcessor now returns a dictionary
    if data_type.lower() == 'transactions' and isinstance(result, dict):
        return result
    
    # For other processors that return a single DataFrame
    return result