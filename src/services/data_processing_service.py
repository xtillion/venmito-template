# src/services/data_processing_service.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union, List

import pandas as pd

from src.data.processor import process_dataframe


class DataProcessingService(ABC):
    """Abstract base class for all data processing services."""
    
    @abstractmethod
    def process(self, data: pd.DataFrame, **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Process data according to service-specific logic."""
        pass


class PeopleProcessingService(DataProcessingService):
    """Service for processing people data."""
    
    def __init__(self, validator=None, merger=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.merger = merger
    
    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Process people data through the standard pipeline."""
        # Validate data if validator is provided
        if self.validator:
            validation_errors = self.validator.validate(data)
            if validation_errors:
                # Handle validation errors according to your requirements
                # For now, just log them
                print(f"Validation errors: {validation_errors}")
        
        # Process the data
        return process_dataframe(data, 'people')
    
    def merge_people_data(self, json_data: pd.DataFrame, yml_data: pd.DataFrame) -> pd.DataFrame:
        """Merge people data from multiple sources."""
        if self.merger:
            merged_data = self.merger.merge(json_data, yml_data)
            return merged_data.get('people', pd.DataFrame())
        return pd.DataFrame()


class TransactionProcessingService(DataProcessingService):
    """Service for processing transaction data."""
    
    def __init__(self, validator=None, people_service=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.people_service = people_service
    
    def process(self, data: pd.DataFrame, **kwargs) -> Dict[str, pd.DataFrame]:
        """Process transaction data and return both transactions and items."""
        # Validate if validator is provided
        if self.validator:
            validation_errors = self.validator.validate(data)
            if validation_errors:
                print(f"Validation errors: {validation_errors}")
        
        # Process the data
        result = process_dataframe(data, 'transactions')
        
        # If people_service is provided, try to link transactions to people
        if self.people_service and 'people_data' in kwargs:
            people_data = kwargs['people_data']
            # Logic to link transactions to people
            # This would typically call a method on the people_service
        
        return result


class TransferProcessingService(DataProcessingService):
    """Service for processing transfer data."""
    
    def __init__(self, validator=None, transaction_service=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.transaction_service = transaction_service
    
    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Process transfer data."""
        # Validate if validator is provided
        if self.validator:
            validation_errors = self.validator.validate(data)
            if validation_errors:
                print(f"Validation errors: {validation_errors}")
        
        # Process the data
        result = process_dataframe(data, 'transfers')
        
        # If transaction_service is provided, try to link transfers to transactions
        if self.transaction_service and 'transaction_data' in kwargs:
            transaction_data = kwargs['transaction_data']
            # Logic to link transfers to transactions
        
        return result