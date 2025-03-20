"""
Tests for the data merging module.

This module contains tests for the data merging functionality, including tests for
merging different data sources and handling merge errors.
"""

import os
import tempfile
import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from unittest.mock import patch, MagicMock, mock_open

from src.data.merger import (
    DataMerger, PeopleMerger, UserReferencesMerger, UserTransactionsMerger,
    UserTransfersMerger, ItemSummaryMerger, StoreSummaryMerger, MainDataMerger,
    MergeError
)


# Fixtures for test data
@pytest.fixture
def people_json_df():
    """Sample people data from JSON source."""
    return pd.DataFrame({
        'user_id': [1, 2, 3],
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
        'city': ['New York', 'Los Angeles', 'Chicago'],
        'country': ['USA', 'USA', 'USA'],
        'devices': ['iPhone', 'Android', 'Desktop'],
        'phone': ['+1234567890', '+19876543210', '+5551234567']
    })

@pytest.fixture
def people_yml_df():
    """Sample people data from YAML source."""
    return pd.DataFrame({
        'user_id': [4, 5, 2],  # Note: user_id 2 overlaps with JSON data
        'first_name': ['Alice', 'Dave', 'Jane'],
        'last_name': ['Williams', 'Brown', 'Smith'],
        'email': ['alice@example.com', 'dave@example.com', 'jane@example.com'],
        'city': ['Boston', 'Philadelphia', 'Los Angeles'],
        'country': ['USA', 'USA', 'USA'],
        'devices': ['iPhone, Android', 'Desktop', 'Android'],
        'phone': ['+13334445555', '+16667778888', '+19876543210']
    })

@pytest.fixture
def promotions_df():
    """Sample promotions data."""
    return pd.DataFrame({
        'promotion_id': [1, 2, 3, 4],
        'client_email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'unknown@example.com'],
        'promotion': ['New Year Offer', 'Birthday Bonus', 'Referral Reward', 'Holiday Special'],
        'amount': [10.50, 25.00, 15.75, 20.00],
        'responded': ['Yes', 'No', 'Yes', 'No'],
        'date': pd.to_datetime(['2023-01-01', '2023-02-15', '2023-03-20', '2023-04-10'])
    })

@pytest.fixture
def transfers_df():
    """Sample transfers data."""
    return pd.DataFrame({
        'transfer_id': [1, 2, 3, 4],
        'sender_id': [1, 2, 3, 4],
        'recipient_id': [2, 3, 1, 5],
        'amount': [100.00, 50.25, 75.50, 200.00],
        'timestamp': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-25', '2023-04-05'])
    })

@pytest.fixture
def transactions_df():
    """Sample transactions data."""
    return pd.DataFrame({
        'transaction_id': ['T001', 'T002', 'T003', 'T004'],
        'phone': ['+1234567890', '+19876543210', '+5551234567', '+13334445555'],
        'item': ['Laptop Computer', 'Smartphone', 'Wireless Headphones', 'Tablet'],
        'store': ['Electronics Store', 'Phone Shop', 'Audio Outlet', 'Electronics Store'],
        'price': [1200.00, 800.00, 150.00, 600.00],
        'quantity': [1, 1, 2, 1],
        'price_per_item': [1200.00, 800.00, 75.00, 600.00]
    })

@pytest.fixture
def expected_merged_people():
    """Expected result of merging people data."""
    return pd.DataFrame({
        'user_id': [1, 2, 3, 4, 5],
        'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Dave'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com', 'dave@example.com'],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Boston', 'Philadelphia'],
        'country': ['USA', 'USA', 'USA', 'USA', 'USA'],
        'devices': ['iPhone', 'Android', 'Desktop', 'iPhone, Android', 'Desktop'],
        'phone': ['+1234567890', '+19876543210', '+5551234567', '+13334445555', '+16667778888']
    })

@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


# Tests for DataMerger base class
class TestDataMerger:
    def test_init(self):
        """Test initializing the DataMerger base class."""
        merger = TestableDataMerger()
        assert isinstance(merger, DataMerger)
        assert merger.merge_errors == []
    
    def test_add_error(self):
        """Test adding errors to the merger."""
        merger = TestableDataMerger()
        merger._add_error("Test error")
        assert len(merger.merge_errors) == 1
        assert merger.merge_errors[0] == "Test error"
    
    def test_get_errors(self):
        """Test getting errors from the merger."""
        merger = TestableDataMerger()
        merger._add_error("Error 1")
        merger._add_error("Error 2")
        errors = merger.get_errors()
        assert len(errors) == 2
        assert errors == ["Error 1", "Error 2"]
    
    def test_save_dataframe(self, temp_output_dir):
        """Test saving a DataFrame to CSV."""
        merger = TestableDataMerger()
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        
        # Save the DataFrame
        merger._save_dataframe(df, "test", temp_output_dir)
        
        # Check the file was created
        output_path = os.path.join(temp_output_dir, "test.csv")
        assert os.path.exists(output_path)
        
        # Check the file contains the correct data
        saved_df = pd.read_csv(output_path)
        pd.testing.assert_frame_equal(df, saved_df)
    
    def test_merge_not_implemented(self):
        """Test that merge() raises NotImplementedError."""
        merger = TestableDataMerger()
        with pytest.raises(NotImplementedError):
            merger.merge()


# Tests for PeopleMerger
class TestPeopleMerger:
    def test_init(self, people_json_df, people_yml_df):
        """Test initializing the PeopleMerger."""
        merger = PeopleMerger(people_json_df, people_yml_df)
        assert isinstance(merger, PeopleMerger)
        pd.testing.assert_frame_equal(merger.people_json_df, people_json_df)
        pd.testing.assert_frame_equal(merger.people_yml_df, people_yml_df)
    
    def test_merge(self, people_json_df, people_yml_df, expected_merged_people):
        """Test merging people data from JSON and YAML sources."""
        merger = PeopleMerger(people_json_df, people_yml_df)
        result = merger.merge()
        
        # Check the merged DataFrame
        assert 'people' in result
        merged_people = result['people']
        
        # Sort by user_id for consistent comparison
        merged_people = merged_people.sort_values('user_id').reset_index(drop=True)
        expected = expected_merged_people.sort_values('user_id').reset_index(drop=True)
        
        # Compare DataFrames
        pd.testing.assert_frame_equal(merged_people, expected)
    
    def test_merge_with_empty_data(self, people_json_df):
        """Test merging when one source is empty."""
        empty_df = pd.DataFrame(columns=people_json_df.columns)
        merger = PeopleMerger(people_json_df, empty_df)
        result = merger.merge()
        
        # Check the result - should contain only the JSON data
        assert 'people' in result
        merged_people = result['people']
        assert len(merged_people) == len(people_json_df)
    
    def test_merge_with_error(self, people_json_df, people_yml_df):
        """Test error handling during merge."""
        # Create a merger with a mocked implementation that raises an exception
        merger = PeopleMerger(people_json_df, people_yml_df)
        
        # Mock pd.merge to raise an exception
        with patch('pandas.merge', side_effect=Exception("Test exception")):
            result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Unexpected error" in merger.merge_errors[0]
        
        # Result should still contain people key with empty DataFrame
        assert 'people' in result
        assert result['people'].empty


# Tests for UserReferencesMerger
class TestUserReferencesMerger:
    def test_init(self, people_json_df, promotions_df, transactions_df):
        """Test initializing the UserReferencesMerger."""
        merger = UserReferencesMerger(people_json_df, promotions_df, transactions_df)
        assert isinstance(merger, UserReferencesMerger)
        pd.testing.assert_frame_equal(merger.people_df, people_json_df)
        pd.testing.assert_frame_equal(merger.promotions_df, promotions_df)
        pd.testing.assert_frame_equal(merger.transactions_df, transactions_df)
    
    def test_add_user_references_to_promotions(self, people_json_df, promotions_df):
        """Test adding user references to promotions."""
        merger = UserReferencesMerger(people_json_df, promotions_df)
        result = merger._add_user_references_to_promotions()
        
        # Check user_id column was added
        assert 'user_id' in result.columns
        
        # Check references were correctly added
        assert result.loc[0, 'user_id'] == 1  # john@example.com -> user_id 1
        assert result.loc[1, 'user_id'] == 2  # jane@example.com -> user_id 2
        assert result.loc[2, 'user_id'] == 3  # bob@example.com -> user_id 3
        
        # The last promotion should have no user_id (unknown@example.com)
        assert pd.isna(result.loc[3, 'user_id'])
        
        # Check client_email column was dropped
        assert 'client_email' not in result.columns
    
    def test_add_user_references_to_transactions(self, people_json_df, transactions_df):
        """Test adding user references to transactions."""
        merger = UserReferencesMerger(people_json_df, None, transactions_df)
        result = merger._add_user_references_to_transactions()
        
        # Check user_id column was added
        assert 'user_id' in result.columns
        
        # Check references were correctly added
        assert result.loc[0, 'user_id'] == 1  # +1234567890 -> user_id 1
        assert result.loc[1, 'user_id'] == 2  # +19876543210 -> user_id 2
        assert result.loc[2, 'user_id'] == 3  # +5551234567 -> user_id 3
        
        # Check phone column was dropped
        assert 'phone' not in result.columns
    
    def test_merge(self, people_json_df, promotions_df, transactions_df):
        """Test merging user references."""
        merger = UserReferencesMerger(people_json_df, promotions_df, transactions_df)
        result = merger.merge()
        
        # Check result contains both DataFrames
        assert 'promotions' in result
        assert 'transactions' in result
        
        # Check both have user_id column
        assert 'user_id' in result['promotions'].columns
        assert 'user_id' in result['transactions'].columns
    
    def test_merge_with_error(self, people_json_df, promotions_df):
        """Test error handling during merge."""
        merger = UserReferencesMerger(people_json_df, promotions_df)
        
        # Mock _add_user_references_to_promotions to raise an exception
        with patch.object(merger, '_add_user_references_to_promotions', 
                         side_effect=Exception("Test exception")):
            result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Unexpected error" in merger.merge_errors[0]
        
        # Result should still contain promotions key with original DataFrame
        assert 'promotions' in result
        pd.testing.assert_frame_equal(result['promotions'], promotions_df)


# Tests for UserTransactionsMerger
class TestUserTransactionsMerger:
    def test_init(self, transactions_df, people_json_df):
        """Test initializing the UserTransactionsMerger."""
        merger = UserTransactionsMerger(transactions_df, people_json_df)
        assert isinstance(merger, UserTransactionsMerger)
        pd.testing.assert_frame_equal(merger.transactions_df, transactions_df)
        pd.testing.assert_frame_equal(merger.people_df, people_json_df)
    
    def test_get_favorite_store(self, transactions_df):
        """Test getting favorite store."""
        merger = UserTransactionsMerger(transactions_df, pd.DataFrame())
        
        # Test with user who has multiple transactions in different stores
        stores = pd.Series(['Electronics Store', 'Phone Shop', 'Electronics Store'])
        assert merger._get_favorite_store(stores) == 'Electronics Store'
        
        # Test with empty series
        assert merger._get_favorite_store(pd.Series([])) is None
    
    def test_get_favorite_item(self, transactions_df):
        """Test getting favorite item."""
        merger = UserTransactionsMerger(transactions_df, pd.DataFrame())
        
        # Test with user who has multiple items
        items = pd.Series(['Laptop', 'Smartphone', 'Laptop'])
        assert merger._get_favorite_item(items) == 'Laptop'
        
        # Test with empty series
        assert merger._get_favorite_item(pd.Series([])) is None
    
    def test_merge(self, transactions_df, people_json_df):
        """Test creating user-level transaction summaries."""
        # Add user_id column to transactions
        transactions_with_uid = transactions_df.copy()
        transactions_with_uid['user_id'] = [1, 2, 3, 4]
        
        merger = UserTransactionsMerger(transactions_with_uid, people_json_df)
        result = merger.merge()
        
        # Check result contains user_transactions DataFrame
        assert 'user_transactions' in result
        user_transactions = result['user_transactions']
        
        # Check structure
        assert 'user_id' in user_transactions.columns
        assert 'total_spent' in user_transactions.columns
        assert 'transaction_count' in user_transactions.columns
        assert 'favorite_store' in user_transactions.columns
        assert 'favorite_item' in user_transactions.columns
        
        # Check values for a specific user
        user1 = user_transactions[user_transactions['user_id'] == 1]
        assert len(user1) == 1
        assert user1.iloc[0]['total_spent'] == 1200.00
        assert user1.iloc[0]['transaction_count'] == 1
        assert user1.iloc[0]['favorite_store'] == 'Electronics Store'
        assert user1.iloc[0]['favorite_item'] == 'Laptop Computer'
    
    def test_merge_with_missing_columns(self, people_json_df):
        """Test handling of missing required columns."""
        # Create transactions DataFrame missing required columns
        transactions_df = pd.DataFrame({
            'user_id': [1, 2, 3],
            'amount': [100, 200, 300]  # Missing required columns
        })
        
        merger = UserTransactionsMerger(transactions_df, people_json_df)
        result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Missing required columns" in merger.merge_errors[0]
        
        # Result should contain empty DataFrame
        assert 'user_transactions' in result
        assert result['user_transactions'].empty


# Tests for UserTransfersMerger
class TestUserTransfersMerger:
    def test_init(self, transfers_df, people_json_df):
        """Test initializing the UserTransfersMerger."""
        merger = UserTransfersMerger(transfers_df, people_json_df)
        assert isinstance(merger, UserTransfersMerger)
        pd.testing.assert_frame_equal(merger.transfers_df, transfers_df)
        pd.testing.assert_frame_equal(merger.people_df, people_json_df)
    
    def test_merge(self, transfers_df, people_json_df):
        """Test creating user-level transfer summaries."""
        merger = UserTransfersMerger(transfers_df, people_json_df)
        result = merger.merge()
        
        # Check result contains user_transfers DataFrame
        assert 'user_transfers' in result
        user_transfers = result['user_transfers']
        
        # Check structure
        assert 'user_id' in user_transfers.columns
        assert 'total_sent' in user_transfers.columns
        assert 'total_received' in user_transfers.columns
        assert 'net_transferred' in user_transfers.columns
        assert 'sent_count' in user_transfers.columns
        assert 'received_count' in user_transfers.columns
        assert 'transfer_count' in user_transfers.columns
        
        # Check values for a specific user
        user1 = user_transfers[user_transfers['user_id'] == 1]
        assert len(user1) == 1
        assert user1.iloc[0]['total_sent'] == 100.00
        assert user1.iloc[0]['total_received'] == 75.50
        assert user1.iloc[0]['net_transferred'] == -24.50  # received - sent
        assert user1.iloc[0]['sent_count'] == 1
        assert user1.iloc[0]['received_count'] == 1
        assert user1.iloc[0]['transfer_count'] == 2
    
    def test_merge_with_missing_columns(self, people_json_df):
        """Test handling of missing required columns."""
        # Create transfers DataFrame missing required columns
        transfers_df = pd.DataFrame({
            'transfer_id': [1, 2, 3],
            'sender_id': [1, 2, 3]
            # Missing recipient_id and amount
        })
        
        merger = UserTransfersMerger(transfers_df, people_json_df)
        result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Missing required columns" in merger.merge_errors[0]
        
        # Result should contain empty DataFrame
        assert 'user_transfers' in result
        assert result['user_transfers'].empty


# Tests for ItemSummaryMerger
class TestItemSummaryMerger:
    def test_init(self, transactions_df):
        """Test initializing the ItemSummaryMerger."""
        merger = ItemSummaryMerger(transactions_df)
        assert isinstance(merger, ItemSummaryMerger)
        pd.testing.assert_frame_equal(merger.transactions_df, transactions_df)
    
    def test_merge(self, transactions_df):
        """Test creating item-level summaries."""
        merger = ItemSummaryMerger(transactions_df)
        result = merger.merge()
        
        # Check result contains item_summary DataFrame
        assert 'item_summary' in result
        item_summary = result['item_summary']
        
        # Check structure
        assert 'item' in item_summary.columns
        assert 'total_revenue' in item_summary.columns
        assert 'items_sold' in item_summary.columns
        assert 'transaction_count' in item_summary.columns
        assert 'average_price' in item_summary.columns
        
        # Check values for a specific item
        laptop = item_summary[item_summary['item'] == 'Laptop Computer']
        assert len(laptop) == 1
        assert laptop.iloc[0]['total_revenue'] == 1200.00
        assert laptop.iloc[0]['items_sold'] == 1
        assert laptop.iloc[0]['transaction_count'] == 1
        assert laptop.iloc[0]['average_price'] == 1200.00
    
    def test_merge_with_missing_columns(self):
        """Test handling of missing required columns."""
        # Create transactions DataFrame missing required columns
        transactions_df = pd.DataFrame({
            'transaction_id': [1, 2, 3],
            'user_id': [1, 2, 3]
            # Missing item, price, quantity
        })
        
        merger = ItemSummaryMerger(transactions_df)
        result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Missing required columns" in merger.merge_errors[0]
        
        # Result should contain empty DataFrame
        assert 'item_summary' in result
        assert result['item_summary'].empty


# Tests for StoreSummaryMerger
class TestStoreSummaryMerger:
    def test_init(self, transactions_df):
        """Test initializing the StoreSummaryMerger."""
        merger = StoreSummaryMerger(transactions_df)
        assert isinstance(merger, StoreSummaryMerger)
        pd.testing.assert_frame_equal(merger.transactions_df, transactions_df)
    
    def test_get_most_sold_item(self, transactions_df):
        """Test getting most sold item for a store."""
        merger = StoreSummaryMerger(transactions_df)
        
        # Test for Electronics Store (should be either Laptop or Tablet, one quantity each)
        assert merger._get_most_sold_item('Electronics Store') in ['Laptop Computer', 'Tablet']
        
        # Test for non-existent store
        assert merger._get_most_sold_item('Non-existent Store') is None
    
    def test_get_most_profitable_item(self, transactions_df):
        """Test getting most profitable item for a store."""
        merger = StoreSummaryMerger(transactions_df)
        
        # Test for Electronics Store (Laptop has higher price than Tablet)
        assert merger._get_most_profitable_item('Electronics Store') == 'Laptop Computer'
        
        # Test for non-existent store
        assert merger._get_most_profitable_item('Non-existent Store') is None
    
    def test_merge(self, transactions_df):
        """Test creating store-level summaries."""
        merger = StoreSummaryMerger(transactions_df)
        result = merger.merge()
        
        # Check result contains store_summary DataFrame
        assert 'store_summary' in result
        store_summary = result['store_summary']
        
        # Check structure
        assert 'store' in store_summary.columns
        assert 'total_revenue' in store_summary.columns
        assert 'items_sold' in store_summary.columns
        assert 'total_transactions' in store_summary.columns
        assert 'average_transaction_value' in store_summary.columns
        assert 'most_sold_item' in store_summary.columns
        assert 'most_profitable_item' in store_summary.columns
        
        # Check values for a specific store
        electronics = store_summary[store_summary['store'] == 'Electronics Store']
        assert len(electronics) == 1
        assert electronics.iloc[0]['total_revenue'] == 1800.00  # 1200 (laptop) + 600 (tablet)
        assert electronics.iloc[0]['items_sold'] == 2  # 1 laptop + 1 tablet
        assert electronics.iloc[0]['total_transactions'] == 2
        assert electronics.iloc[0]['average_transaction_value'] == 900.00  # 1800 / 2
        assert electronics.iloc[0]['most_profitable_item'] == 'Laptop Computer'
    
    def test_merge_with_missing_columns(self):
        """Test handling of missing required columns."""
        # Create transactions DataFrame missing required columns
        transactions_df = pd.DataFrame({
            'transaction_id': [1, 2, 3],
            'user_id': [1, 2, 3]
            # Missing store, item, price, quantity
        })
        
        merger = StoreSummaryMerger(transactions_df)
        result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Missing required columns" in merger.merge_errors[0]
        
        # Result should contain empty DataFrame
        assert 'store_summary' in result
        assert result['store_summary'].empty


# Tests for MainDataMerger
class TestMainDataMerger:
    def test_init(self, people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir):
        """Test initializing the MainDataMerger."""
        merger = MainDataMerger(
            people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir
        )
        assert isinstance(merger, MainDataMerger)
        pd.testing.assert_frame_equal(merger.people_json_df, people_json_df)
        pd.testing.assert_frame_equal(merger.people_yml_df, people_yml_df)
        pd.testing.assert_frame_equal(merger.promotions_df, promotions_df)
        pd.testing.assert_frame_equal(merger.transfers_df, transfers_df)
        pd.testing.assert_frame_equal(merger.transactions_df, transactions_df)
        assert merger.output_dir == temp_output_dir
    
    def test_merge(self, people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir):
        """Test the full merging pipeline."""
        merger = MainDataMerger(
            people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir
        )
        result = merger.merge()
        
        # Check result contains all expected DataFrames
        expected_keys = [
            'people', 'promotions', 'transactions', 
            'user_transactions', 'item_summary', 'store_summary', 
            'user_transfers'
        ]
        for key in expected_keys:
            assert key in result
            assert not result[key].empty
        
        # Check files were saved
        for key in expected_keys:
            assert os.path.exists(os.path.join(temp_output_dir, f"{key}.csv"))
    
    def test_merge_with_missing_people(self, promotions_df, transfers_df, transactions_df, temp_output_dir):
        """Test handling of missing people data."""
        # Create empty people DataFrames
        empty_df = pd.DataFrame()
        
        merger = MainDataMerger(
            empty_df, empty_df, promotions_df, transfers_df, transactions_df, temp_output_dir
        )
        result = merger.merge()
        
        # Check that error was recorded
        assert len(merger.merge_errors) == 1
        assert "Failed to merge people data" in merger.merge_errors[0]
        
        # Result should be empty
        assert 'people' in result
        assert result['people'].empty
    
    @patch('src.data.merger.PeopleMerger')
    def test_error_propagation(self, mock_people_merger, people_json_df, people_yml_df, 
                              promotions_df, transfers_df, transactions_df, temp_output_dir):
        """Test that errors from component mergers are propagated."""
        # Mock PeopleMerger to add an error
        mock_merger_instance = MagicMock()
        mock_merger_instance.merge.return_value = {'people': people_json_df}
        mock_merger_instance.get_errors.return_value = ["Test error from PeopleMerger"]
        mock_people_merger.return_value = mock_merger_instance
        
        # Create the MainDataMerger and verify it uses the mock
        with patch.object(MainDataMerger, '_add_error') as mock_add_error:
            merger = MainDataMerger(
                people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir
            )
            result = merger.merge()
        
            # Check that the error was added
            mock_add_error.assert_any_call("Test error from PeopleMerger")

# Integration tests
class TestMergerIntegration:
    def test_complete_pipeline(self, people_json_df, people_yml_df, promotions_df, 
                              transfers_df, transactions_df, temp_output_dir):
        """Test the complete data merging pipeline."""
        # Process the full pipeline
        merger = MainDataMerger(
            people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir
        )
        result = merger.merge()
        
        # Verify the relationships between merged data
        
        # 1. Check promotions correctly reference people
        if 'promotions' in result and 'people' in result:
            promo_user_ids = set(result['promotions']['user_id'].dropna())
            people_user_ids = set(result['people']['user_id'])
            assert promo_user_ids.issubset(people_user_ids)
        
        # 2. Check transactions correctly reference people
        if 'transactions' in result and 'people' in result:
            trans_user_ids = set(result['transactions']['user_id'].dropna())
            people_user_ids = set(result['people']['user_id'])
            assert trans_user_ids.issubset(people_user_ids)
        
        # 3. Check user_transactions includes all people
        if 'user_transactions' in result and 'people' in result:
            user_transaction_ids = set(result['user_transactions']['user_id'])
            people_user_ids = set(result['people']['user_id'])
            assert user_transaction_ids.issuperset(people_user_ids)
        
        # 4. Check user_transfers includes all people
        if 'user_transfers' in result and 'people' in result:
            user_transfer_ids = set(result['user_transfers']['user_id'])
            people_user_ids = set(result['people']['user_id'])
            assert user_transfer_ids.issuperset(people_user_ids)
        
        # 5. Check store_summary and item_summary are consistent with transactions
        if 'store_summary' in result and 'transactions' in result:
            store_names = set(result['transactions']['store'].unique())
            summary_store_names = set(result['store_summary']['store'])
            assert store_names == summary_store_names
        
        if 'item_summary' in result and 'transactions' in result:
            item_names = set(result['transactions']['item'].unique())
            summary_item_names = set(result['item_summary']['item'])
            assert item_names == summary_item_names
    
    def test_data_consistency(self, people_json_df, people_yml_df, promotions_df, 
                             transfers_df, transactions_df, temp_output_dir):
        """Test consistency of merged data."""
        # Process the full pipeline
        merger = MainDataMerger(
            people_json_df, people_yml_df, promotions_df, transfers_df, transactions_df, temp_output_dir
        )
        result = merger.merge()
        
        # Verify that totals and aggregations are consistent
        
        # 1. Check transfer totals for each user match user_transfers summary
        if 'transfers' in result and 'user_transfers' in result:
            for user_id in result['user_transfers']['user_id']:
                # Get sent amount from transfers
                sent_filter = result['transfers']['sender_id'] == user_id
                sent_total = result['transfers'][sent_filter]['amount'].sum()
                
                # Get received amount from transfers
                received_filter = result['transfers']['recipient_id'] == user_id
                received_total = result['transfers'][received_filter]['amount'].sum()
                
                # Get values from user_transfers
                user_row = result['user_transfers'][result['user_transfers']['user_id'] == user_id]
                
                # Compare values (allowing for small floating point differences)
                assert abs(user_row['total_sent'].values[0] - sent_total) < 0.01
                assert abs(user_row['total_received'].values[0] - received_total) < 0.01
                assert abs(user_row['net_transferred'].values[0] - (received_total - sent_total)) < 0.01
        
        # 2. Check transaction totals for each user match user_transactions summary
        if 'transactions' in result and 'user_transactions' in result:
            for user_id in result['user_transactions']['user_id']:
                # Get transaction amount from transactions
                trans_filter = result['transactions']['user_id'] == user_id
                trans_total = result['transactions'][trans_filter]['price'].sum()
                
                # Get value from user_transactions
                user_row = result['user_transactions'][result['user_transactions']['user_id'] == user_id]
                
                # Compare values (allowing for small floating point differences)
                if not pd.isna(user_row['total_spent'].values[0]):
                    assert abs(user_row['total_spent'].values[0] - trans_total) < 0.01

# Helper class for testing the abstract base class
class TestableDataMerger(DataMerger):
    def merge(self):
        return {"test": pd.DataFrame()}
    
# Performance tests
@pytest.mark.parametrize("size", [100, 1000])
def test_merger_performance(size, temp_output_dir):
    """Test merger performance with different sized datasets."""
    # Create larger datasets
    people_json_data = {
        'user_id': list(range(1, size+1)),
        'first_name': [f'User{i}' for i in range(1, size+1)],
        'email': [f'user{i}@example.com' for i in range(1, size+1)],
        'phone': [f'+1{i:010d}' for i in range(1, size+1)]
    }
    people_json_df = pd.DataFrame(people_json_data)
    
    people_yml_data = {
        'user_id': list(range(size+1, size*2+1)),
        'first_name': [f'User{i}' for i in range(size+1, size*2+1)],
        'email': [f'user{i}@example.com' for i in range(size+1, size*2+1)],
        'phone': [f'+1{i:010d}' for i in range(size+1, size*2+1)]
    }
    people_yml_df = pd.DataFrame(people_yml_data)
    
    transfers_data = {
        'transfer_id': list(range(1, size+1)),
        'sender_id': [i for i in range(1, size+1)],
        'recipient_id': [(i % size) + 1 for i in range(1, size+1)],  # Circular references
        'amount': [100.0 for _ in range(1, size+1)]
    }
    transfers_df = pd.DataFrame(transfers_data)
    
    # Measure the time it takes to merge the dataframes
    import time
    start_time = time.time()
    
    # Just test the PeopleMerger for performance
    merger = PeopleMerger(people_json_df, people_yml_df)
    result = merger.merge()
    
    end_time = time.time()
    
    assert 'people' in result
    assert len(result['people']) == size*2
    
    # Log the performance (this will show in the test output)
    print(f"\nMerged {size*2} people records in {end_time - start_time:.6f} seconds")