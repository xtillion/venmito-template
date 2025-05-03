from typing import Dict, Any, Optional, Union, List
import pandas as pd

from src.services.data_processing_service import DataProcessingService
from src.data.processor import process_dataframe
from src.data.merger import TransferMerger

class TransferProcessingService(DataProcessingService):
    """Service for processing transfer data."""
    
    def __init__(self, validator=None, merger=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.merger = merger
    
    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Process transfer data through the standard pipeline."""
        # Create validator on demand with the actual DataFrame
        validator = self._validate('transfer', data)
        validation_errors = validator.validate()
        if validation_errors:
            print(f"Validation errors: {validation_errors}")
        
        # Process the data
        return process_dataframe(data, 'transfer')
    
    def merge_transfer_data(self, json_data: pd.DataFrame, yml_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Merge transfer data from multiple sources."""
        # Create and use a TransferMerger
        merger = TransferMerger(json_data, yml_data)
        # Return the full dictionary result
        return merger.merge()