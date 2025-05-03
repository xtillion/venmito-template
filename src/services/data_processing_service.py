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
        
    def _validate(self, data: pd.DataFrame, data_type: str) -> List[str]:
        """Validate data using the appropriate validator."""
        from src.data.validator import get_validator
        validator = get_validator(data_type, data)
        return validator.validate()
