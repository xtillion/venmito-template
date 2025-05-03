# src/commands/process_data_command.py
from typing import Dict, Any, Optional, Union

import pandas as pd

from src.commands.command import Command
from src.services.service_factory import ServiceFactory


class ProcessDataCommand(Command):
    """Command to process a DataFrame through a specific data processing service."""
    
    def __init__(self, data: pd.DataFrame, data_type: str, **kwargs):
        """
        Initialize the command.
        
        Args:
            data: The DataFrame to process
            data_type: The type of data to process ('people', 'transactions', 'transfers')
            **kwargs: Additional arguments to pass to the service
        """
        self.data = data
        self.data_type = data_type
        self.kwargs = kwargs
    
    def execute(self) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Execute the command by processing the data.
        
        Returns:
            The processed DataFrame or dictionary of DataFrames
        """
        # Get the appropriate service for the data type
        service = ServiceFactory.get_service(self.data_type)
        
        # Process the data
        return service.process(self.data, **self.kwargs)


class MergeDataCommand(Command):
    """Command to merge data from multiple sources."""
    
    def __init__(self, json_data: pd.DataFrame, yml_data: pd.DataFrame):
        """
        Initialize the command.
        
        Args:
            json_data: The DataFrame from JSON source
            yml_data: The DataFrame from YAML source
        """
        self.json_data = json_data
        self.yml_data = yml_data
    
    def execute(self) -> pd.DataFrame:
        """
        Execute the command by merging the data.
        
        Returns:
            The merged DataFrame
        """
        # Get the people service
        service = ServiceFactory.get_service('people')
        
        # Merge the data
        return service.merge_people_data(self.json_data, self.yml_data)