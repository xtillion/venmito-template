"""
Data validation module for Venmito project.

This module provides classes for validating data structure and content
of DataFrames loaded from various sources.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union, Callable

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Exception raised for data validation errors."""
    pass


class DataValidator(ABC):
    """Abstract base class for data validators."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the validator with a DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
        """
        self.df = df
        self.validation_errors = []
        logger.info(f"Initialized validator for DataFrame with shape {df.shape}")
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the DataFrame.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        pass
    
    def get_errors(self) -> List[str]:
        """
        Get all validation errors.
        
        Returns:
            List[str]: List of validation error messages
        """
        return self.validation_errors
    
    def _add_error(self, message: str) -> None:
        """
        Add an error message to the list of validation errors.
        
        Args:
            message (str): Error message
        """
        self.validation_errors.append(message)
        logger.warning(f"Validation error: {message}")
    
    def _validate_required_columns(self, required_columns: List[str]) -> bool:
        """
        Validate that all required columns are present in the DataFrame.
        
        Args:
            required_columns (List[str]): List of required column names
        
        Returns:
            bool: True if all required columns are present, False otherwise
        """
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            self._add_error(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        
        return True
    
    def _validate_no_duplicates(self, columns: List[str]) -> bool:
        """
        Validate that there are no duplicate values in the specified columns.
        
        Args:
            columns (List[str]): Columns to check for duplicates
        
        Returns:
            bool: True if no duplicates found, False otherwise
        """
        if not all(col in self.df.columns for col in columns):
            self._add_error(f"Cannot check for duplicates, some columns do not exist: {columns}")
            return False
        
        duplicates = self.df.duplicated(subset=columns, keep='first')
        
        if duplicates.any():
            duplicate_indices = self.df[duplicates].index.tolist()
            self._add_error(f"Found {len(duplicate_indices)} duplicate entries based on columns {columns}")
            return False
        
        return True
    
    def _validate_no_missing_values(self, columns: List[str]) -> bool:
        """
        Validate that there are no missing values in the specified columns.
        
        Args:
            columns (List[str]): Columns to check for missing values
        
        Returns:
            bool: True if no missing values found, False otherwise
        """
        if not all(col in self.df.columns for col in columns):
            self._add_error(f"Cannot check for missing values, some columns do not exist: {columns}")
            return False
        
        missing_counts = self.df[columns].isna().sum()
        missing_columns = missing_counts[missing_counts > 0].index.tolist()
        
        if missing_columns:
            for col in missing_columns:
                count = missing_counts[col]
                self._add_error(f"Column '{col}' has {count} missing values")
            return False
        
        return True
    
    def _validate_column_values(self, column: str, validator: Callable[[Any], bool], 
                              error_message: str) -> bool:
        """
        Validate that all values in a column pass a custom validation function.
        
        Args:
            column (str): Column to validate
            validator (Callable[[Any], bool]): Function to validate each value
            error_message (str): Error message template
        
        Returns:
            bool: True if all values pass validation, False otherwise
        """
        if column not in self.df.columns:
            self._add_error(f"Cannot validate values, column does not exist: {column}")
            return False
        
        # Skip NaN values to avoid validation errors
        invalid_indices = self.df[~self.df[column].isna()][~self.df[column].apply(validator)].index.tolist()
        
        if invalid_indices:
            self._add_error(error_message.format(len(invalid_indices), column))
            return False
        
        return True
    
    def _validate_numeric_column(self, column: str, min_val: Optional[float] = None, 
                               max_val: Optional[float] = None) -> bool:
        """
        Validate that a column contains only numeric values within an optional range.
        
        Args:
            column (str): Column to validate
            min_val (float, optional): Minimum allowed value
            max_val (float, optional): Maximum allowed value
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        if column not in self.df.columns:
            self._add_error(f"Cannot validate numeric values, column does not exist: {column}")
            return False
        
        # Check that values are numeric
        non_numeric = self.df[~self.df[column].isna() & ~pd.to_numeric(self.df[column], errors='coerce').notna()]
        
        if not non_numeric.empty:
            self._add_error(f"Column '{column}' has {len(non_numeric)} non-numeric values")
            return False
        
        # Convert to numeric for range validation
        numeric_col = pd.to_numeric(self.df[column], errors='coerce')
        
        # Check minimum value if specified
        if min_val is not None:
            below_min = numeric_col < min_val
            if below_min.any():
                count = below_min.sum()
                self._add_error(f"Column '{column}' has {count} values below minimum {min_val}")
                return False
        
        # Check maximum value if specified
        if max_val is not None:
            above_max = numeric_col > max_val
            if above_max.any():
                count = above_max.sum()
                self._add_error(f"Column '{column}' has {count} values above maximum {max_val}")
                return False
        
        return True
    
    def _validate_string_pattern(self, column: str, pattern: str) -> bool:
        """
        Validate that all string values in a column match a regex pattern.
        
        Args:
            column (str): Column to validate
            pattern (str): Regular expression pattern
        
        Returns:
            bool: True if all values match the pattern, False otherwise
        """
        if column not in self.df.columns:
            self._add_error(f"Cannot validate pattern, column does not exist: {column}")
            return False
        
        # Create a compiled regex for better performance
        regex = re.compile(pattern)
        
        # Only check non-NA string values
        mask = ~self.df[column].isna() & self.df[column].apply(lambda x: isinstance(x, str))
        invalid = ~self.df.loc[mask, column].apply(lambda x: bool(regex.match(x)))
        
        if invalid.any():
            count = invalid.sum()
            self._add_error(f"Column '{column}' has {count} values not matching pattern '{pattern}'")
            return False
        
        return True


class PeopleValidator(DataValidator):
    """Validator for people data."""
    
    def validate(self) -> bool:
        """
        Validate people data.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        is_valid = True
        
        # Check required columns
        required_columns = ['id', 'email', 'phone']
        if not self._validate_required_columns(required_columns):
            is_valid = False
        
        # Check for unique identifiers
        if 'id' in self.df.columns and not self._validate_no_duplicates(['id']):
            is_valid = False
        
        if 'email' in self.df.columns and not self._validate_no_duplicates(['email']):
            is_valid = False
        
        if 'phone' in self.df.columns and not self._validate_no_duplicates(['phone']):
            is_valid = False
        
        # Check for missing values in key fields
        non_empty_columns = ['id', 'email']
        if not self._validate_no_missing_values(non_empty_columns):
            is_valid = False
        
        # Validate email format
        if 'email' in self.df.columns:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not self._validate_string_pattern('email', email_pattern):
                is_valid = False
        
        # Validate phone format (basic check, may need to be adapted)
        if 'phone' in self.df.columns:
            phone_pattern = r'^\+?[0-9\s\-\(\)]{7,20}$'
            if not self._validate_string_pattern('phone', phone_pattern):
                is_valid = False
        
        # Location data validation (if present)
        location_columns = ['city', 'country']
        if all(col in self.df.columns for col in location_columns):
            if not self._validate_no_missing_values(location_columns):
                is_valid = False
        
        return is_valid


class PromotionsValidator(DataValidator):
    """Validator for promotions data."""
    
    def validate(self) -> bool:
        """
        Validate promotions data.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        is_valid = True
        
        # Check required columns
        required_columns = ['promotion_id', 'promotion', 'responded']
        if not self._validate_required_columns(required_columns):
            is_valid = False
        
        # Check for unique identifiers
        if 'promotion_id' in self.df.columns and not self._validate_no_duplicates(['promotion_id']):
            is_valid = False
        
        # Check for missing values in key fields
        non_empty_columns = ['promotion_id', 'promotion']
        if not self._validate_no_missing_values(non_empty_columns):
            is_valid = False
        
        # Validate response values
        if 'responded' in self.df.columns:
            valid_responses = ['Yes', 'No']
            
            def is_valid_response(val):
                return val in valid_responses
            
            error_msg = "Column 'responded' has {} invalid values (expected 'Yes' or 'No')"
            if not self._validate_column_values('responded', is_valid_response, error_msg):
                is_valid = False
        
        # Validate user_id if present (should match existing users)
        if 'user_id' in self.df.columns:
            if not self._validate_no_missing_values(['user_id']):
                is_valid = False
        
        return is_valid


class TransfersValidator(DataValidator):
    """Validator for transfers data."""
    
    def validate(self) -> bool:
        """
        Validate transfers data.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        is_valid = True
        
        # Check required columns
        required_columns = ['sender_id', 'recipient_id', 'amount']
        if not self._validate_required_columns(required_columns):
            is_valid = False
        
        # Check for missing values in key fields
        if not self._validate_no_missing_values(required_columns):
            is_valid = False
        
        # Validate amount is numeric and positive
        if 'amount' in self.df.columns:
            if not self._validate_numeric_column('amount', min_val=0):
                is_valid = False
        
        # Sender and recipient should be different
        if all(col in self.df.columns for col in ['sender_id', 'recipient_id']):
            same_sender_recipient = (self.df['sender_id'] == self.df['recipient_id']).sum()
            
            if same_sender_recipient > 0:
                self._add_error(f"Found {same_sender_recipient} transfers where sender_id equals recipient_id")
                is_valid = False
        
        return is_valid


class TransactionsValidator(DataValidator):
    """Validator for transactions data."""
    
    def validate(self) -> bool:
        """
        Validate transactions data.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        is_valid = True
        
        # Check required columns
        required_columns = ['transaction_id', 'item', 'price', 'quantity', 'store']
        if not self._validate_required_columns(required_columns):
            is_valid = False
        
        # Check for unique identifiers
        if 'transaction_id' in self.df.columns and not self._validate_no_duplicates(['transaction_id']):
            is_valid = False
        
        # Check for missing values in key fields
        non_empty_columns = ['transaction_id', 'item', 'price', 'store']
        if not self._validate_no_missing_values(non_empty_columns):
            is_valid = False
        
        # Validate numeric fields
        if 'price' in self.df.columns:
            if not self._validate_numeric_column('price', min_val=0):
                is_valid = False
        
        if 'quantity' in self.df.columns:
            if not self._validate_numeric_column('quantity', min_val=1):
                is_valid = False
        
        if 'price_per_item' in self.df.columns:
            if not self._validate_numeric_column('price_per_item', min_val=0):
                is_valid = False
        
        return is_valid


# Factory function to get the appropriate validator
def get_validator(data_type: str, df: pd.DataFrame) -> DataValidator:
    """
    Factory function to get the appropriate validator for a data type.
    
    Args:
        data_type (str): Type of data to validate ('people', 'promotions', 'transfers', 'transactions')
        df (pd.DataFrame): DataFrame to validate
    
    Returns:
        DataValidator: Validator for the specified data type
    
    Raises:
        ValueError: If the data type is not supported
    """
    validators = {
        'people': PeopleValidator,
        'promotions': PromotionsValidator,
        'transfers': TransfersValidator,
        'transactions': TransactionsValidator
    }
    
    if data_type.lower() not in validators:
        logger.error(f"Unsupported data type: {data_type}")
        raise ValueError(f"Unsupported data type: {data_type}")
    
    return validators[data_type.lower()](df)


# Convenience function for direct validation
def validate_dataframe(df: pd.DataFrame, data_type: str) -> List[str]:
    """
    Validate a DataFrame for a specific data type.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        data_type (str): Type of data to validate ('people', 'promotions', 'transfers', 'transactions')
    
    Returns:
        List[str]: List of validation error messages, empty if validation passed
    
    Raises:
        ValueError: If the data type is not supported
    """
    validator = get_validator(data_type, df)
    validator.validate()
    return validator.get_errors()