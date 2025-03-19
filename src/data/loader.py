"""
Data loading module for Venmito project.

This module contains classes for loading data from different file formats 
(JSON, YAML, CSV, XML) into pandas DataFrames.
"""

import os
import logging
from typing import Dict, Any, Optional, Union

import pandas as pd
import yaml
import xml.etree.ElementTree as ET


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseLoader:
    """Base class for all data loaders."""
    
    def __init__(self, file_path: str):
        """
        Initialize the loader with a file path.
        
        Args:
            file_path (str): Path to the data file
        
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.file_path = file_path
        logger.info(f"Initialized loader for {file_path}")
    
    def load(self) -> pd.DataFrame:
        """
        Load data from file.
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded data
        
        Raises:
            NotImplementedError: If the subclass does not implement this method
        """
        raise NotImplementedError("Subclasses must implement load method")


class JSONLoader(BaseLoader):
    """Loader for JSON data files."""
    
    def load(self) -> pd.DataFrame:
        """
        Load JSON data into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded JSON data
        
        Raises:
            ValueError: If the JSON file is not properly formatted
        """
        try:
            logger.info(f"Loading JSON data from {self.file_path}")
            df = pd.read_json(self.file_path)
            logger.info(f"Successfully loaded JSON data with shape {df.shape}")
            return df
        except ValueError as e:
            logger.error(f"Error loading JSON data: {str(e)}")
            raise ValueError(f"Error loading JSON data: {str(e)}")


class YAMLLoader(BaseLoader):
    """Loader for YAML data files."""
    
    def load(self) -> pd.DataFrame:
        """
        Load YAML data into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded YAML data
        
        Raises:
            ValueError: If the YAML file is not properly formatted
        """
        try:
            logger.info(f"Loading YAML data from {self.file_path}")
            with open(self.file_path, 'r') as file:
                yaml_data = yaml.safe_load(file)
            
            if not yaml_data:
                logger.warning(f"Empty YAML data in {self.file_path}")
                return pd.DataFrame()
            
            df = pd.DataFrame(yaml_data)
            logger.info(f"Successfully loaded YAML data with shape {df.shape}")
            return df
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML data: {str(e)}")
            raise ValueError(f"Error parsing YAML data: {str(e)}")


class CSVLoader(BaseLoader):
    """Loader for CSV data files."""
    
    def load(self, **kwargs) -> pd.DataFrame:
        """
        Load CSV data into a pandas DataFrame.
        
        Args:
            **kwargs: Additional arguments to pass to pd.read_csv
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded CSV data
        
        Raises:
            ValueError: If the CSV file is not properly formatted
        """
        try:
            logger.info(f"Loading CSV data from {self.file_path}")
            df = pd.read_csv(self.file_path, **kwargs)
            logger.info(f"Successfully loaded CSV data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV data: {str(e)}")
            raise ValueError(f"Error loading CSV data: {str(e)}")


class XMLLoader(BaseLoader):
    """Loader for XML data files."""
    
    def load(self) -> pd.DataFrame:
        """
        Load XML data into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded XML data
        
        Raises:
            ValueError: If the XML file is not properly formatted
        """
        try:
            logger.info(f"Loading XML data from {self.file_path}")
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            data = []
            
            # This is a generic implementation, which needs to be adapted
            # to the specific XML structure of your data
            for child in root:
                item = {}
                for subchild in child:
                    item[subchild.tag] = subchild.text
                data.append(item)
            
            df = pd.DataFrame(data)
            logger.info(f"Successfully loaded XML data with shape {df.shape}")
            return df
        except ET.ParseError as e:
            logger.error(f"Error parsing XML data: {str(e)}")
            raise ValueError(f"Error parsing XML data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in XML parsing: {str(e)}")
            raise ValueError(f"Unexpected error in XML parsing: {str(e)}")


class DataLoader:
    """Factory class for loading data from different file formats."""
    
    def __init__(self):
        """Initialize the DataLoader factory."""
        self.loaders = {
            'json': JSONLoader,
            'yml': YAMLLoader,
            'yaml': YAMLLoader,
            'csv': CSVLoader,
            'xml': XMLLoader
        }
        logger.info("Initialized DataLoader factory")
    
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from a file based on its extension.
        
        Args:
            file_path (str): Path to the data file
            **kwargs: Additional arguments to pass to the specific loader
        
        Returns:
            pd.DataFrame: DataFrame containing the loaded data
        
        Raises:
            ValueError: If the file extension is not supported or loading fails
        """
        try:
            file_extension = file_path.split('.')[-1].lower()
            
            if file_extension not in self.loaders:
                logger.error(f"Unsupported file extension: {file_extension}")
                raise ValueError(f"Unsupported file extension: {file_extension}")
            
            loader = self.loaders[file_extension](file_path)
            return loader.load(**kwargs)
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise
    
    def register_loader(self, extension: str, loader_class: type) -> None:
        """
        Register a new loader for a specific file extension.
        
        Args:
            extension (str): File extension (without the dot)
            loader_class (type): Loader class to use for this extension
        """
        if not issubclass(loader_class, BaseLoader):
            logger.error("Loader class must be a subclass of BaseLoader")
            raise TypeError("Loader class must be a subclass of BaseLoader")
        
        self.loaders[extension.lower()] = loader_class
        logger.info(f"Registered loader for extension .{extension}")


# Convenience function for direct use
def load_file(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load data from a file based on its extension.
    
    Args:
        file_path (str): Path to the data file
        **kwargs: Additional arguments to pass to the specific loader
    
    Returns:
        pd.DataFrame: DataFrame containing the loaded data
    """
    loader = DataLoader()
    return loader.load_data(file_path, **kwargs)