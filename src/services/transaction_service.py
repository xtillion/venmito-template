from typing import List, Dict, Any
import pandas as pd

from src.data.processor import process_dataframe
from src.data.merger import ItemSummaryMerger
from src.services.data_processing_service import DataProcessingService

class TransactionProcessingService(DataProcessingService):
    """Service for processing transaction data."""
    
    def __init__(self, validator=None, merger=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.merger = merger
    
    def process(self, data: pd.DataFrame, **kwargs) -> Dict[str, pd.DataFrame]:
        """Process transaction data through the standard pipeline."""
        # Create validator on demand with the actual DataFrame
        validator = self._validate('transaction', data)
        validation_errors = validator.validate()
        if validation_errors:
            print(f"Validation errors: {validation_errors}")
        
        # Process the data
        return process_dataframe(data, 'transaction')
    
    def merge_transaction_data(self, json_data: pd.DataFrame, yml_data: pd.DataFrame) -> pd.DataFrame:
        """Merge transaction data from multiple sources."""
        # If a merger is provided, use it
        if self.merger:
            merged_result = self.merger.merge()
            return merged_result.get('transaction', pd.DataFrame())
        
        # Otherwise, create and use a TransactionMerger
        merger = ItemSummaryMerger(json_data, yml_data)
        result = merger.merge()
        return result.get('transaction', pd.DataFrame())