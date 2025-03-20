"""
Tests for the data loading module.

This module contains tests for the data loading functionality, including tests for 
different file formats, error handling, and the loader factory.
"""

import os
import json
import pytest
import pandas as pd
import yaml
import tempfile
from unittest.mock import patch, mock_open, MagicMock

from src.data.loader import (
    BaseLoader, JSONLoader, YAMLLoader, CSVLoader, XMLLoader, 
    DataLoader, load_file
)


# Fixtures for test data
@pytest.fixture
def sample_json_data():
    return {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ]
    }

@pytest.fixture
def sample_yaml_data():
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]

@pytest.fixture
def sample_csv_data():
    return "id,name,email\n1,John Doe,john@example.com\n2,Jane Smith,jane@example.com"

@pytest.fixture
def sample_xml_data():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <users>
        <user>
            <id>1</id>
            <name>John Doe</name>
            <email>john@example.com</email>
        </user>
        <user>
            <id>2</id>
            <name>Jane Smith</name>
            <email>jane@example.com</email>
        </user>
    </users>"""

@pytest.fixture
def temp_json_file(sample_json_data):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
        json.dump(sample_json_data, f)
        temp_file_path = f.name
    yield temp_file_path
    os.unlink(temp_file_path)

@pytest.fixture
def temp_yaml_file(sample_yaml_data):
    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False, mode='w') as f:
        yaml.dump(sample_yaml_data, f)
        temp_file_path = f.name
    yield temp_file_path
    os.unlink(temp_file_path)

@pytest.fixture
def temp_csv_file(sample_csv_data):
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(sample_csv_data.encode('utf-8'))
        temp_file_path = f.name
    yield temp_file_path
    os.unlink(temp_file_path)

@pytest.fixture
def temp_xml_file(sample_xml_data):
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        f.write(sample_xml_data.encode('utf-8'))
        temp_file_path = f.name
    yield temp_file_path
    os.unlink(temp_file_path)


# Tests for BaseLoader
class TestBaseLoader:
    def test_init_valid_file(self, temp_json_file):
        """Test initializing BaseLoader with a valid file."""
        loader = BaseLoader(temp_json_file)
        assert loader.file_path == temp_json_file

    def test_init_invalid_file(self):
        """Test initializing BaseLoader with a non-existent file."""
        with pytest.raises(FileNotFoundError):
            BaseLoader("non_existent_file.json")

    def test_load_not_implemented(self, temp_json_file):
        """Test that load() raises NotImplementedError."""
        loader = BaseLoader(temp_json_file)
        with pytest.raises(NotImplementedError):
            loader.load()


# Tests for JSONLoader
class TestJSONLoader:
    def test_load_valid_json(self, temp_json_file, sample_json_data):
        """Test loading a valid JSON file."""
        loader = JSONLoader(temp_json_file)
        df = loader.load()
        
        # For this particular structure, pandas will create a DataFrame with
        # users column that contains list of dictionaries
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Converting the result back to dict for easier comparison
        if 'users' in df.columns:
            # Handle nested data
            result_data = {"users": df['users'].tolist()}
            assert result_data == sample_json_data
        else:
            # Handle flat data
            assert df.to_dict(orient='records') == sample_json_data.get("users", sample_json_data)

    def test_load_invalid_json(self):
        """Test loading an invalid JSON file."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            f.write(b"invalid_json_data")
            temp_file_path = f.name
        
        try:
            loader = JSONLoader(temp_file_path)
            with pytest.raises(ValueError):
                loader.load()
        finally:
            os.unlink(temp_file_path)


# Tests for YAMLLoader
class TestYAMLLoader:
    def test_load_valid_yaml(self, temp_yaml_file, sample_yaml_data):
        """Test loading a valid YAML file."""
        loader = YAMLLoader(temp_yaml_file)
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_yaml_data)
        
        # Compare data
        result_data = df.to_dict(orient='records')
        assert result_data == sample_yaml_data

    def test_load_invalid_yaml(self):
        """Test loading an invalid YAML file."""
        with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as f:
            f.write(b"invalid: yaml: data: : :")
            temp_file_path = f.name
        
        try:
            loader = YAMLLoader(temp_file_path)
            with pytest.raises(ValueError):
                loader.load()
        finally:
            os.unlink(temp_file_path)
    
    def test_load_empty_yaml(self):
        """Test loading an empty YAML file."""
        with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as f:
            f.write(b"")
            temp_file_path = f.name
        
        try:
            loader = YAMLLoader(temp_file_path)
            df = loader.load()
            assert isinstance(df, pd.DataFrame)
            assert df.empty
        finally:
            os.unlink(temp_file_path)


# Tests for CSVLoader
class TestCSVLoader:
    def test_load_valid_csv(self, temp_csv_file, sample_csv_data):
        """Test loading a valid CSV file."""
        loader = CSVLoader(temp_csv_file)
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2  # Two rows in our sample data
        assert list(df.columns) == ["id", "name", "email"]
        
        # Check values
        assert df.iloc[0]["name"] == "John Doe"
        assert df.iloc[1]["email"] == "jane@example.com"

    def test_load_csv_with_kwargs(self, temp_csv_file):
        """Test loading a CSV file with additional kwargs."""
        loader = CSVLoader(temp_csv_file)
        df = loader.load(dtype={"id": int})
        
        assert isinstance(df, pd.DataFrame)
        assert df["id"].dtype == int

    def test_load_invalid_csv(self):
        """Test loading a malformed CSV file."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='w') as f:
            # CSV with mismatched columns
            f.write("id,name,email\n1,John Doe\n2,Jane Smith,jane@example.com,extra")
            temp_file_path = f.name
        
        try:
            loader = CSVLoader(temp_file_path)
            # This should raise a ValueError
            with pytest.raises(ValueError, match="Error loading CSV data"):
                loader.load()
        finally:
            os.unlink(temp_file_path)


# Tests for XMLLoader
class TestXMLLoader:
    def test_load_valid_xml(self, temp_xml_file):
        """Test loading a valid XML file."""
        loader = XMLLoader(temp_xml_file)
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        # Since XML parsing logic is generic and would need to be adapted for specific XML,
        # we just check that it loaded something
        assert not df.empty

    def test_load_invalid_xml(self):
        """Test loading an invalid XML file."""
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            f.write(b"<invalid>xml<file>")
            temp_file_path = f.name
        
        try:
            loader = XMLLoader(temp_file_path)
            with pytest.raises(ValueError):
                loader.load()
        finally:
            os.unlink(temp_file_path)


# Tests for DataLoader factory class
class TestDataLoader:
    def test_init(self):
        """Test initializing DataLoader."""
        loader = DataLoader()
        assert isinstance(loader, DataLoader)
        assert 'json' in loader.loaders
        assert 'csv' in loader.loaders
        assert 'yml' in loader.loaders
        assert 'yaml' in loader.loaders
        assert 'xml' in loader.loaders

    def test_load_data_json(self, temp_json_file):
        """Test loading a JSON file through the factory."""
        loader = DataLoader()
        df = loader.load_data(temp_json_file)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_data_yaml(self, temp_yaml_file):
        """Test loading a YAML file through the factory."""
        loader = DataLoader()
        df = loader.load_data(temp_yaml_file)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_data_csv(self, temp_csv_file):
        """Test loading a CSV file through the factory."""
        loader = DataLoader()
        df = loader.load_data(temp_csv_file)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_data_xml(self, temp_xml_file):
        """Test loading an XML file through the factory."""
        loader = DataLoader()
        df = loader.load_data(temp_xml_file)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_data_unsupported_extension(self):
        """Test loading a file with an unsupported extension."""
        with tempfile.NamedTemporaryFile(suffix=".unsupported", delete=False) as f:
            f.write(b"some data")
            temp_file_path = f.name
        
        try:
            loader = DataLoader()
            with pytest.raises(ValueError):
                loader.load_data(temp_file_path)
        finally:
            os.unlink(temp_file_path)
    
    def test_register_loader(self):
        """Test registering a custom loader."""
        class CustomLoader(BaseLoader):
            def load(self):
                return pd.DataFrame({"test": [1, 2, 3]})
        
        loader = DataLoader()
        loader.register_loader("custom", CustomLoader)
        
        # Create a custom file
        with tempfile.NamedTemporaryFile(suffix=".custom", delete=False) as f:
            f.write(b"custom data")
            temp_file_path = f.name
        
        try:
            df = loader.load_data(temp_file_path)
            assert isinstance(df, pd.DataFrame)
            assert list(df.columns) == ["test"]
            assert len(df) == 3
        finally:
            os.unlink(temp_file_path)
    
    def test_register_invalid_loader(self):
        """Test registering an invalid loader class."""
        loader = DataLoader()
        
        class InvalidLoader:  # Not a subclass of BaseLoader
            def load(self):
                return pd.DataFrame()
        
        with pytest.raises(TypeError):
            loader.register_loader("invalid", InvalidLoader)


# Tests for convenience function
def test_load_file(temp_csv_file):
    """Test the convenience function load_file."""
    df = load_file(temp_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Integration-style tests
class TestIntegration:
    def test_load_with_custom_kwargs(self, temp_csv_file):
        """Test loading a CSV with custom kwargs through the factory."""
        df = load_file(temp_csv_file, dtype={"id": int}, skiprows=0)
        assert isinstance(df, pd.DataFrame)
        assert df["id"].dtype == int

    def test_error_propagation(self):
        """Test that errors are properly propagated."""
        with pytest.raises(FileNotFoundError):
            load_file("nonexistent_file.csv")

    @patch('pandas.read_csv')
    def test_exception_handling(self, mock_read_csv, temp_csv_file):
        """Test exception handling in the CSV loader."""
        # Make read_csv raise an exception
        mock_read_csv.side_effect = Exception("Test exception")
        
        with pytest.raises(ValueError):
            load_file(temp_csv_file)


# Performance tests
@pytest.mark.parametrize("size", [100, 1000])
def test_csv_performance(size):
    """Test performance with different sized datasets."""
    # Create a larger dataset
    data = "id,name,email\n"
    for i in range(size):
        data += f"{i},User {i},user{i}@example.com\n"
    
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(data.encode('utf-8'))
        temp_file_path = f.name
    
    try:
        # Measure the time it takes to load the file
        import time
        start_time = time.time()
        df = load_file(temp_file_path)
        end_time = time.time()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == size
        
        # Log the performance (this will show in the test output)
        print(f"\nLoaded {size} rows in {end_time - start_time:.6f} seconds")
    finally:
        os.unlink(temp_file_path)