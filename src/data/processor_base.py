"""
Base data processing module for Venmito project.

This module provides the abstract base class and utilities for data processing.
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


class ProcessingError(Exception):
    """Exception raised for data processing errors."""
    pass


class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the processor with a DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame to process
        """
        self.df = df.copy()  # Create a copy to avoid modifying the original
        self.processing_errors = []
        logger.info(f"Initialized processor for DataFrame with shape {df.shape}")
    
    @abstractmethod
    def process(self) -> pd.DataFrame:
        """
        Process the DataFrame.
        
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        pass
    
    def get_errors(self) -> List[str]:
        """
        Get all processing errors.
        
        Returns:
            List[str]: List of processing error messages
        """
        return self.processing_errors
    
    def _add_error(self, message: str) -> None:
        """
        Add an error message to the list of processing errors.
        
        Args:
            message (str): Error message
        """
        self.processing_errors.append(message)
        logger.warning(f"Processing error: {message}")
    
    def _rename_columns(self, column_mapping: Dict[str, str]) -> None:
        """
        Rename columns in the DataFrame.
        
        Args:
            column_mapping (Dict[str, str]): Mapping from old column names to new column names
        """
        # Only rename columns that exist
        existing_columns = {col: new_col for col, new_col in column_mapping.items() 
                           if col in self.df.columns}
        
        if existing_columns:
            self.df.rename(columns=existing_columns, inplace=True)
            logger.info(f"Renamed columns: {existing_columns}")
    
    def _drop_columns(self, columns: List[str]) -> None:
        """
        Drop columns from the DataFrame.
        
        Args:
            columns (List[str]): Columns to drop
        """
        # Only drop columns that exist
        columns_to_drop = [col for col in columns if col in self.df.columns]
        
        if columns_to_drop:
            self.df.drop(columns=columns_to_drop, inplace=True)
            logger.info(f"Dropped columns: {columns_to_drop}")
    
    def _fill_missing_values(self, column: str, value: Any) -> None:
        """
        Fill missing values in a column.
        
        Args:
            column (str): Column to fill
            value (Any): Value to fill with
        """
        if column in self.df.columns:
            missing_count = self.df[column].isna().sum()
            
            if missing_count > 0:
                self.df[column].fillna(value, inplace=True)
                logger.info(f"Filled {missing_count} missing values in column '{column}' with {value}")
    
    def _convert_column_type(self, column: str, dtype: Any) -> None:
        """
        Convert a column to a specific data type.
        
        Args:
            column (str): Column to convert
            dtype (Any): Data type to convert to
        """
        if column in self.df.columns:
            try:
                self.df[column] = self.df[column].astype(dtype)
                logger.info(f"Converted column '{column}' to {dtype}")
            except Exception as e:
                self._add_error(f"Failed to convert column '{column}' to {dtype}: {str(e)}")
    
    def _apply_to_column(self, column: str, func: Callable, 
                        error_msg: str = "Error applying function to column") -> None:
        """
        Apply a function to a column.
        
        Args:
            column (str): Column to apply function to
            func (Callable): Function to apply
            error_msg (str): Error message template
        """
        if column in self.df.columns:
            try:
                self.df[column] = self.df[column].apply(func)
                logger.info(f"Applied function to column '{column}'")
            except Exception as e:
                self._add_error(f"{error_msg} '{column}': {str(e)}")
    
    def _normalize_text(self, column: str) -> None:
        """
        Normalize text in a column (lowercase, strip whitespace).
        
        Args:
            column (str): Column to normalize
        """
        if column in self.df.columns:
            try:
                # Only apply to string values
                mask = self.df[column].apply(lambda x: isinstance(x, str))
                self.df.loc[mask, column] = self.df.loc[mask, column].str.lower().str.strip()
                logger.info(f"Normalized text in column '{column}'")
            except Exception as e:
                self._add_error(f"Failed to normalize text in column '{column}': {str(e)}")


# Convenience function to get the appropriate processor
def get_processor(data_type: str, df: pd.DataFrame, processor_map: Dict[str, type]) -> DataProcessor:
    """
    Get the appropriate processor for a data type.
    
    Args:
        data_type (str): Type of data to process
        df (pd.DataFrame): DataFrame to process
        processor_map (Dict[str, type]): Mapping from data types to processor classes
    
    Returns:
        DataProcessor: Processor for the specified data type
    
    Raises:
        ValueError: If the data type is not supported
    """
    if data_type.lower() not in processor_map:
        logger.error(f"Unsupported data type: {data_type}")
        raise ValueError(f"Unsupported data type: {data_type}")
    
    return processor_map[data_type.lower()](df)