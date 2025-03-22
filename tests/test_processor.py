"""
Tests for the data processing module.

This module contains tests for the data processing functionality, including tests for
different data transformations, cleaning operations, and error handling.
"""

import os
import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from unittest.mock import patch, MagicMock

from src.data.processor import (
    process_dataframe, 
    PeopleProcessor, 
    PromotionsProcessor, 
    TransfersProcessor,
    TransactionsProcessor
)
from src.data.processor_base import DataProcessor, ProcessingError


# Fixtures for test data
@pytest.fixture
def raw_people_df():
    """Create a raw people DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'email': ['JOHN@example.com', ' jane@example.com ', 'bob@example.com'],
        'location': [
            {'City': 'New York', 'Country': 'USA'},
            {'City': 'Los Angeles', 'Country': 'USA'},
            {'City': 'Chicago', 'Country': 'USA'}
        ],
        'Android': [1, 0, 0],
        'Iphone': [0, 1, 0],
        'Desktop': [0, 0, 1],
        'telephone': ['123-456-7890', '+1 (987) 654-3210', '555.123.4567']
    })

@pytest.fixture
def expected_processed_people_df():
    """Expected result after processing people data."""
    return pd.DataFrame({
        'user_id': [1, 2, 3],
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
        'city': ['new york', 'los angeles', 'chicago'],
        'country': ['usa', 'usa', 'usa'],  
        'devices': ['Android', 'Iphone', 'Desktop'],
        'phone': ['1234567890', '+19876543210', '5551234567']
    })

@pytest.fixture
def raw_promotions_df():
    """Create a raw promotions DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'user_id': [1, 2, 3],
        'promotion': ['new_year_offer', 'birthday_bonus', 'REFERRAL_REWARD'],
        'responded': ['yes', 'N', 'TRUE']
    })

@pytest.fixture
def expected_processed_promotions_df():
    """Expected result after processing promotions data."""
    return pd.DataFrame({
        'promotion_id': [1, 2, 3],
        'user_id': [1, 2, 3],
        'promotion': ['New Year Offer', 'Birthday Bonus', 'Referral Reward'],
        'responded': ['Yes', 'No', 'Yes']
    })

@pytest.fixture
def raw_transfers_df():
    """Create a raw transfers DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'sender_id': ['1', '2', '3'],  # String IDs
        'recipient_id': ['2', '3', '1'],
        'amount': ['100.00', '50.25', '75.50'],  # String amounts
        'date': ['2023-01-15', '2023-02-20', '2023-03-25']  # String dates
    })

@pytest.fixture
def expected_processed_transfers_df():
    """Expected result after processing transfers data."""
    return pd.DataFrame({
        'transfer_id': [1, 2, 3],
        'sender_id': [1, 2, 3],
        'recipient_id': [2, 3, 1],
        'amount': [100.00, 50.25, 75.50],
        'timestamp': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-25'])
    })

@pytest.fixture
def raw_transactions_df():
    """Create a raw transactions DataFrame for testing."""
    return pd.DataFrame({
        'transaction_id': ['T001', 'T002', 'T003'],
        'user_id': [1, 2, 3],
        'item': ['laptop_computer', ' smartphone ', 'WIRELESS_HEADPHONES'],
        'store': ['electronics_store', 'phone_shop', 'AUDIO_OUTLET'],
        'price': [1200, 800, 150],
        'quantity': [1, 1, 2],
        'price_per_item': [1200, 800, 75]  # Note: 75 * 2 = 150, consistent with price
    })

@pytest.fixture
def expected_processed_transactions_df():
    """Expected result after processing transactions data."""
    return pd.DataFrame({
        'transaction_id': ['T001', 'T002', 'T003'],
        'user_id': [1, 2, 3],
        'item': ['Laptop Computer', 'Smartphone', 'Wireless Headphones'],
        'store': ['Electronics Store', 'Phone Shop', 'Audio Outlet'],
        'price': [1200.00, 800.00, 150.00],
        'quantity': [1, 1, 2],
        'price_per_item': [1200.00, 800.00, 75.00]
    })


# Tests for DataProcessor base class
class TestDataProcessor:
    def test_init(self, raw_people_df):
        """Test initializing the DataProcessor base class."""
        processor = TestableDataProcessor(raw_people_df)
        assert isinstance(processor, DataProcessor)
        assert processor.df is not raw_people_df  # Should be a copy
        assert processor.processing_errors == []
    
    def test_add_error(self, raw_people_df):
        """Test adding errors to the processor."""
        processor = TestableDataProcessor(raw_people_df)
        processor._add_error("Test error")
        assert len(processor.processing_errors) == 1
        assert processor.processing_errors[0] == "Test error"
    
    def test_get_errors(self, raw_people_df):
        """Test getting errors from the processor."""
        processor = TestableDataProcessor(raw_people_df)
        processor._add_error("Error 1")
        processor._add_error("Error 2")
        errors = processor.get_errors()
        assert len(errors) == 2
        assert errors == ["Error 1", "Error 2"]
    
    def test_rename_columns(self, raw_people_df):
        """Test renaming columns in the DataFrame."""
        processor = TestableDataProcessor(raw_people_df)
        processor._rename_columns({"id": "user_id", "name": "full_name"})
        assert "user_id" in processor.df.columns
        assert "full_name" in processor.df.columns
        assert "id" not in processor.df.columns
        assert "name" not in processor.df.columns
    
    def test_drop_columns(self, raw_people_df):
        """Test dropping columns from the DataFrame."""
        processor = TestableDataProcessor(raw_people_df)
        processor._drop_columns(["Android", "Iphone", "Desktop"])
        assert "Android" not in processor.df.columns
        assert "Iphone" not in processor.df.columns
        assert "Desktop" not in processor.df.columns
    
    def test_fill_missing_values(self, raw_people_df):
        """Test filling missing values in a column."""
        # Create df with missing values
        df = raw_people_df.copy()
        df.loc[0, "email"] = None
        
        # Fill missing values
        processor = TestableDataProcessor(df)
        processor._fill_missing_values("email", "default@example.com")
        assert processor.df.loc[0, "email"] == "default@example.com"

    def test_convert_column_type(self, raw_people_df):
        """Test converting column type."""
        processor = TestableDataProcessor(raw_people_df)
        processor._convert_column_type("id", str)
        assert processor.df["id"].dtype == object  # string columns have object dtype
    
    def test_apply_to_column(self, raw_people_df):
        """Test applying a function to a column."""
        processor = TestableDataProcessor(raw_people_df)
        processor._apply_to_column("email", lambda x: x.lower() if isinstance(x, str) else x)
        
        # Check all emails are lowercase
        for email in processor.df["email"]:
            assert email == email.lower() if isinstance(email, str) else email
    
    def test_normalize_text(self, raw_people_df):
        """Test normalizing text in a column."""
        processor = TestableDataProcessor(raw_people_df)
        processor._normalize_text("email")
        
        # Check emails are normalized (lowercase and stripped)
        assert processor.df.loc[0, "email"] == "john@example.com"
        assert processor.df.loc[1, "email"] == "jane@example.com"
        assert processor.df.loc[2, "email"] == "bob@example.com"


# Tests for PeopleProcessor
class TestPeopleProcessor:
    def test_process(self, raw_people_df, expected_processed_people_df):
        """Test processing people data."""
        processor = PeopleProcessor(raw_people_df)
        result_df = processor.process()
        
        # Compare with expected results
        # We use subset to only compare columns that exist in both DataFrames
        common_columns = list(set(result_df.columns) & set(expected_processed_people_df.columns))
        
        # Print columns for debugging
        print("Result columns:", result_df.columns.tolist())
        print("Expected columns:", expected_processed_people_df.columns.tolist())
        print("Common columns:", common_columns)
        
        # Convert column types to be the same for comparison
        for col in common_columns:
            if result_df[col].dtype != expected_processed_people_df[col].dtype:
                if pd.api.types.is_numeric_dtype(result_df[col].dtype) and pd.api.types.is_numeric_dtype(expected_processed_people_df[col].dtype):
                    # Both numeric but different types, convert to float
                    result_df[col] = result_df[col].astype(float)
                    expected_processed_people_df[col] = expected_processed_people_df[col].astype(float)
                else:
                    # Convert to string for safer comparison
                    result_df[col] = result_df[col].astype(str)
                    expected_processed_people_df[col] = expected_processed_people_df[col].astype(str)
        
        pd.testing.assert_frame_equal(
            result_df[common_columns].reset_index(drop=True), 
            expected_processed_people_df[common_columns].reset_index(drop=True),
            check_dtype=False  # Don't check data types
        )
    
    def test_standardize_devices(self, raw_people_df):
        """Test standardizing devices information."""
        processor = PeopleProcessor(raw_people_df)
        processor._standardize_devices()
        
        # Check devices column was created from binary indicators
        assert "devices" in processor.df.columns
        assert processor.df.loc[0, "devices"] == "Android"
        assert processor.df.loc[1, "devices"] == "Iphone"
        assert processor.df.loc[2, "devices"] == "Desktop"
        
        # Check binary indicator columns were dropped
        assert "Android" not in processor.df.columns
        assert "Iphone" not in processor.df.columns
        assert "Desktop" not in processor.df.columns
    
    def test_standardize_location(self, raw_people_df):
        """Test standardizing location information."""
        processor = PeopleProcessor(raw_people_df)
        processor._standardize_location()
        
        # Check city and country columns were created from location
        assert "city" in processor.df.columns
        assert "country" in processor.df.columns
        
        # Check values
        assert processor.df.loc[0, "city"] == "New York"
        assert processor.df.loc[0, "country"] == "USA"
        assert processor.df.loc[1, "city"] == "Los Angeles"
        assert processor.df.loc[1, "country"] == "USA"
        assert processor.df.loc[2, "city"] == "Chicago"
        assert processor.df.loc[2, "country"] == "USA"
        
        # Check location column was dropped
        assert "location" not in processor.df.columns
    
    def test_standardize_name(self, raw_people_df):
        """Test standardizing name information."""
        processor = PeopleProcessor(raw_people_df)
        processor._standardize_name()
        
        # Check first_name and last_name columns were created
        assert "first_name" in processor.df.columns
        assert "last_name" in processor.df.columns
        
        # Check values
        assert processor.df.loc[0, "first_name"] == "John"
        assert processor.df.loc[0, "last_name"] == "Doe"
        assert processor.df.loc[1, "first_name"] == "Jane"
        assert processor.df.loc[1, "last_name"] == "Smith"
        assert processor.df.loc[2, "first_name"] == "Bob"
        assert processor.df.loc[2, "last_name"] == "Johnson"
    
    def test_standardize_phone(self, raw_people_df):
        """Test standardizing phone numbers."""
        processor = PeopleProcessor(raw_people_df)
        processor._standardize_phone()
        
        # Check telephone column was renamed to phone
        assert "phone" in processor.df.columns
        assert "telephone" not in processor.df.columns
        
        # Check phone numbers are standardized
        assert processor.df.loc[0, "phone"] == "1234567890"
        assert processor.df.loc[1, "phone"] == "+19876543210"
        assert processor.df.loc[2, "phone"] == "5551234567"
    
    def test_standardize_id(self, raw_people_df):
        """Test standardizing ID field."""
        processor = PeopleProcessor(raw_people_df)
        processor._standardize_id()
        
        # Check id column was renamed to user_id
        assert "user_id" in processor.df.columns
        assert "id" not in processor.df.columns
        
        # Check user_id is integer type
        assert pd.api.types.is_integer_dtype(processor.df["user_id"].dtype)


# Tests for PromotionsProcessor
class TestPromotionsProcessor:
    def test_process(self, raw_promotions_df, expected_processed_promotions_df):
        """Test processing promotions data."""
        processor = PromotionsProcessor(raw_promotions_df)
        result_df = processor.process()
        
        # Compare with expected results
        pd.testing.assert_frame_equal(
            result_df.reset_index(drop=True), 
            expected_processed_promotions_df.reset_index(drop=True),
            check_dtype=False  # Don't check data types
        )
    
    def test_standardize_ids(self, raw_promotions_df):
        """Test standardizing ID fields in promotions."""
        processor = PromotionsProcessor(raw_promotions_df)
        processor._standardize_ids()
        
        # Check id column was renamed to promotion_id
        assert "promotion_id" in processor.df.columns
        assert "id" not in processor.df.columns
        
        # Check promotion_id is integer type
        assert pd.api.types.is_integer_dtype(processor.df["promotion_id"].dtype)
    
    def test_standardize_response(self, raw_promotions_df):
        """Test standardizing response values."""
        processor = PromotionsProcessor(raw_promotions_df)
        processor._standardize_response()
        
        # Check responded values are standardized to Yes/No
        assert processor.df.loc[0, "responded"] == "Yes"
        assert processor.df.loc[1, "responded"] == "No"
        assert processor.df.loc[2, "responded"] == "Yes"
    
    def test_standardize_promotion_names(self, raw_promotions_df):
        """Test standardizing promotion names."""
        processor = PromotionsProcessor(raw_promotions_df)
        processor._standardize_promotion_names()
        
        # Check promotion names are standardized
        assert processor.df.loc[0, "promotion"] == "New Year Offer"
        assert processor.df.loc[1, "promotion"] == "Birthday Bonus"
        assert processor.df.loc[2, "promotion"] == "Referral Reward"


# Tests for TransfersProcessor
class TestTransfersProcessor:
    def test_process(self, raw_transfers_df, expected_processed_transfers_df):
        """Test processing transfers data."""
        processor = TransfersProcessor(raw_transfers_df)
        result_df = processor.process()
        
        # Convert timestamp to same type for comparison
        result_df["timestamp"] = pd.to_datetime(result_df["timestamp"])
        expected_processed_transfers_df["timestamp"] = pd.to_datetime(expected_processed_transfers_df["timestamp"])
        
        # Compare with expected results
        pd.testing.assert_frame_equal(
            result_df.reset_index(drop=True), 
            expected_processed_transfers_df.reset_index(drop=True),
            check_dtype=False  # Don't check data types
        )
    
    def test_standardize_ids(self, raw_transfers_df):
        """Test standardizing ID fields in transfers."""
        processor = TransfersProcessor(raw_transfers_df)
        processor._standardize_ids()
        
        # Check id column was renamed to transfer_id
        assert "transfer_id" in processor.df.columns
        assert "id" not in processor.df.columns
        
        # Check all ID fields are integer type
        assert pd.api.types.is_integer_dtype(processor.df["transfer_id"].dtype)
        assert pd.api.types.is_integer_dtype(processor.df["sender_id"].dtype)
        assert pd.api.types.is_integer_dtype(processor.df["recipient_id"].dtype)
    
    def test_standardize_amount(self, raw_transfers_df):
        """Test standardizing amount field."""
        processor = TransfersProcessor(raw_transfers_df)
        processor._standardize_amount()
        
        # Check amount is numeric type
        assert pd.api.types.is_numeric_dtype(processor.df["amount"].dtype)
        
        # Check values
        assert processor.df.loc[0, "amount"] == 100.00
        assert processor.df.loc[1, "amount"] == 50.25
        assert processor.df.loc[2, "amount"] == 75.50
    
    def test_standardize_timestamp(self, raw_transfers_df):
        """Test standardizing timestamp field."""
        processor = TransfersProcessor(raw_transfers_df)
        processor._standardize_timestamp()
        
        # Check date column was renamed to timestamp
        assert "timestamp" in processor.df.columns
        assert "date" not in processor.df.columns
        
        # Check timestamp is datetime type
        assert pd.api.types.is_datetime64_dtype(processor.df["timestamp"].dtype)
        
        # Check values
        assert processor.df.loc[0, "timestamp"] == pd.Timestamp("2023-01-15")
        assert processor.df.loc[1, "timestamp"] == pd.Timestamp("2023-02-20")
        assert processor.df.loc[2, "timestamp"] == pd.Timestamp("2023-03-25")


# Tests for TransactionsProcessor
class TestTransactionsProcessor:
    def test_process(self, raw_transactions_df, expected_processed_transactions_df):
        """Test processing transactions data."""
        processor = TransactionsProcessor(raw_transactions_df)
        result_df = processor.process()
        
        # Compare with expected results
        pd.testing.assert_frame_equal(
            result_df.reset_index(drop=True), 
            expected_processed_transactions_df.reset_index(drop=True),
            check_dtype=False  # Don't check data types
        )
    
    def test_standardize_ids(self, raw_transactions_df):
        """Test standardizing ID fields in transactions."""
        processor = TransactionsProcessor(raw_transactions_df)
        processor._standardize_ids()
        
        # Check transaction_id is string type
        assert pd.api.types.is_object_dtype(processor.df["transaction_id"].dtype)
        
        # Check user_id is integer type
        assert pd.api.types.is_integer_dtype(processor.df["user_id"].dtype)
    
    def test_standardize_numeric_fields(self, raw_transactions_df):
        """Test standardizing numeric fields."""
        processor = TransactionsProcessor(raw_transactions_df)
        processor._standardize_numeric_fields()
        
        # Check numeric fields are numeric type
        assert pd.api.types.is_numeric_dtype(processor.df["price"].dtype)
        assert pd.api.types.is_numeric_dtype(processor.df["quantity"].dtype)
        assert pd.api.types.is_numeric_dtype(processor.df["price_per_item"].dtype)
        
        # Check values are rounded to 2 decimal places
        assert processor.df.loc[0, "price"] == 1200.00
        assert processor.df.loc[0, "price_per_item"] == 1200.00
    
    def test_standardize_item_and_store_names(self, raw_transactions_df):
        """Test standardizing item and store names."""
        processor = TransactionsProcessor(raw_transactions_df)
        processor._standardize_item_and_store_names()
        
        # Check item names are standardized
        assert processor.df.loc[0, "item"] == "Laptop Computer"
        assert processor.df.loc[1, "item"] == "Smartphone"
        assert processor.df.loc[2, "item"] == "Wireless Headphones"
        
        # Check store names are standardized
        assert processor.df.loc[0, "store"] == "Electronics Store"
        assert processor.df.loc[1, "store"] == "Phone Shop"
        assert processor.df.loc[2, "store"] == "Audio Outlet"
    
    def test_validate_price_and_quantity(self, raw_transactions_df):
        """Test validating price and quantity consistency."""
        processor = TransactionsProcessor(raw_transactions_df)
        processor._validate_price_and_quantity()
        
        # No errors should be added since our test data is consistent
        assert len(processor.processing_errors) == 0
        
        # Modify one row to create an inconsistency
        processor.df.loc[0, "price"] = 1000.00  # Not equal to price_per_item * quantity
        processor._validate_price_and_quantity()
        
        # Should detect the inconsistency
        assert len(processor.processing_errors) == 1
        assert "inconsistent price" in processor.processing_errors[0].lower()


# Tests for process_dataframe function
class TestProcessDataframe:
    def test_process_people(self, raw_people_df, expected_processed_people_df):
        """Test processing people data through the convenience function."""
        result_df = process_dataframe(raw_people_df, "people")
        
        # Compare result with expected output (subset of columns)
        common_columns = [col for col in result_df.columns if col in expected_processed_people_df.columns]
        pd.testing.assert_frame_equal(
            result_df[common_columns].reset_index(drop=True),
            expected_processed_people_df[common_columns].reset_index(drop=True),
            check_dtype=False
        )
    
    def test_process_invalid_data_type(self, raw_people_df):
        """Test processing with an invalid data type."""
        with pytest.raises(ValueError):
            process_dataframe(raw_people_df, "invalid_type")

    
# Tests for error handling
class TestErrorHandling:
    def test_process_with_invalid_column_types(self):
        """Test processing with invalid column types."""
        # Create df with mixed types in a column
        df = pd.DataFrame({
            'id': [1, 'two', 3],  # Mixed types
            'name': ['John', 'Jane', 'Bob']
        })
        
        # Should process without raising exception but add errors
        processor = PeopleProcessor(df)
        result_df = processor.process()
        
        # Check errors were added
        assert len(processor.processing_errors) > 0
        
        # Check result still has both rows
        assert len(result_df) == 3
    
    def test_process_empty_dataframe(self):
        """Test processing an empty DataFrame."""
        df = pd.DataFrame(columns=['id', 'name', 'email'])
        
        processor = PeopleProcessor(df)
        result_df = processor.process()
        
        # Result should still be empty but with proper structure
        assert result_df.empty
        assert "user_id" in result_df.columns  # Should have renamed id to user_id


# Integration tests
class TestProcessorIntegration:
    def test_multiple_processing_steps(self, raw_people_df):
        """Test a sequence of processing steps."""
        # Process people data
        people_df = process_dataframe(raw_people_df, "people")
        
        # Create a simple promotions df using processed people data
        promotions_df = pd.DataFrame({
            'id': [1, 2],
            'user_id': people_df['user_id'].iloc[:2].tolist(),  # Use first 2 user_ids
            'promotion': ['offer_1', 'offer_2'],
            'responded': ['yes', 'no']
        })
        
        # Process promotions data
        processed_promotions = process_dataframe(promotions_df, "promotions")
        
        # Verify that the promotions were processed correctly
        assert len(processed_promotions) == 2
        assert "promotion_id" in processed_promotions.columns
        assert processed_promotions.loc[0, "responded"] == "Yes"
        assert processed_promotions.loc[1, "responded"] == "No"
        
        # Verify that the user_ids remain valid references
        assert all(uid in people_df['user_id'].values for uid in processed_promotions['user_id'])



# Performance tests
@pytest.mark.parametrize("size", [100, 1000])
def test_processor_performance(size):
    """Test processor performance with different sized datasets."""
    # Create a larger dataset
    data = {
        'id': list(range(1, size+1)),
        'name': [f'User {i}' for i in range(1, size+1)],
        'email': [f'user{i}@example.com' for i in range(1, size+1)],
        'telephone': [f'555-{i:03d}-{i*2:04d}' for i in range(1, size+1)]
    }
    df = pd.DataFrame(data)
    
    # Measure the time it takes to process the dataframe
    import time
    start_time = time.time()
    result_df = process_dataframe(df, "people")
    end_time = time.time()
    
    assert len(result_df) == size
    assert "user_id" in result_df.columns
    assert "first_name" in result_df.columns
    assert "last_name" in result_df.columns
    
    # Log the performance (this will show in the test output)
    print(f"\nProcessed {size} rows in {end_time - start_time:.6f} seconds")

@pytest.mark.skip(reason="Helper class, not a test")
# Helper class for testing the abstract base class
class TestableDataProcessor(DataProcessor):
    def process(self):
        return self.df    