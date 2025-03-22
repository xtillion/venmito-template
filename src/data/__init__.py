"""
Data handling package for Venmito project.

This package provides modules for loading, validating, processing, and merging
data from various sources.
"""

# Import main functions from each module for easier access
from src.data.loader import load_file
from src.data.validator import validate_dataframe
from src.data.processor import process_dataframe
from src.data.merger import MainDataMerger

# Version
__version__ = '0.1.0'