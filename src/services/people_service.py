from typing import Dict, Any, Optional, Union

import pandas as pd

from src.services.data_processing_service import DataProcessingService
from src.data.processor import process_dataframe
from src.data.merger import PeopleMerger


class PeopleProcessingService(DataProcessingService):
    """Service for processing people data."""
    
    def __init__(self, validator=None, merger=None):
        """Initialize the service with optional dependencies."""
        self.validator = validator
        self.merger = merger
    
    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Process people data through the standard pipeline."""
        # Create validator on demand with the actual DataFrame
        validator = self._validate('people', data)
        validation_errors = validator.validate()
        if validation_errors:
            print(f"Validation errors: {validation_errors}")
        
        # Process the data
        return process_dataframe(data, 'people')
    
    def merge_people_data(self, json_data: pd.DataFrame, yml_data: pd.DataFrame) -> pd.DataFrame:
        """Merge people data from multiple sources."""
        # If a merger is provided, use it
        if self.merger:
            merged_result = self.merger.merge()
            return merged_result.get('people', pd.DataFrame())
        
        # Otherwise, create and use a PeopleMerger
        merger = PeopleMerger(json_data, yml_data)
        result = merger.merge()
        return result.get('people', pd.DataFrame())