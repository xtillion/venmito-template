"""
Data merging module for Venmito project.

This module provides classes for merging data from various sources
into coherent datasets for analytics.
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union, Tuple

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MergeError(Exception):
    """Exception raised for data merging errors."""
    pass


class DataMerger(ABC):
    """Abstract base class for data mergers."""
    
    def __init__(self):
        """Initialize the merger."""
        self.merge_errors = []
        logger.info("Initialized data merger")
    
    @abstractmethod
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Merge data from different sources.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of merged DataFrames
        """
        pass
    
    def get_errors(self) -> List[str]:
        """
        Get all merging errors.
        
        Returns:
            List[str]: List of merging error messages
        """
        return self.merge_errors
    
    def _add_error(self, message: str) -> None:
        """
        Add an error message to the list of merging errors.
        
        Args:
            message (str): Error message
        """
        self.merge_errors.append(message)
        logger.warning(f"Merging error: {message}")
    
    def _save_dataframe(self, df: pd.DataFrame, name: str, output_dir: str) -> None:
        """
        Save a DataFrame to CSV.
        
        Args:
            df (pd.DataFrame): DataFrame to save
            name (str): Name to use for the file
            output_dir (str): Directory to save to
        """
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Save the DataFrame
            output_path = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(output_path, index=False)
            logger.info(f"Saved {name} to {output_path}")
        except Exception as e:
            self._add_error(f"Failed to save {name}: {str(e)}")


class PeopleMerger(DataMerger):
    """Merger for people data from different sources."""
    
    def __init__(self, people_json_df: pd.DataFrame, people_yml_df: pd.DataFrame):
        """
        Initialize the merger with people data from JSON and YAML sources.
        
        Args:
            people_json_df (pd.DataFrame): People data from JSON
            people_yml_df (pd.DataFrame): People data from YAML
        """
        super().__init__()
        self.people_json_df = people_json_df
        self.people_yml_df = people_yml_df
    
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Merge people data from JSON and YAML sources.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with the merged people DataFrame
        """
        try:
            logger.info("Merging people data...")
            
            # Check for overlapping users
            json_ids = set(self.people_json_df['user_id'].astype(str)) if 'user_id' in self.people_json_df.columns else set()
            yml_ids = set(self.people_yml_df['user_id'].astype(str)) if 'user_id' in self.people_yml_df.columns else set()
            
            overlap = json_ids.intersection(yml_ids)
            if overlap:
                logger.info(f"Found {len(overlap)} overlapping users in JSON and YAML data")
            
            # Make a copy of the dataframes to avoid modifying the originals
            json_df = self.people_json_df.copy()
            yml_df = self.people_yml_df.copy()
            
            # Standardize the devices column to ensure it's a string
            if 'devices' in json_df.columns:
                json_df['devices'] = json_df['devices'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else str(x) if pd.notna(x) else ''
                )
            
            if 'devices' in yml_df.columns:
                yml_df['devices'] = yml_df['devices'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else str(x) if pd.notna(x) else ''
                )
            
            # Identify common columns for the merge
            json_columns = set(json_df.columns)
            yml_columns = set(yml_df.columns)
            common_columns = list(json_columns.intersection(yml_columns))
            
            # Ensure user_id is included in common columns if it exists in both dataframes
            if 'user_id' in json_columns and 'user_id' in yml_columns:
                if 'user_id' not in common_columns:
                    common_columns.append('user_id')
            
            # For columns that are in one dataframe but not the other, add them with NaN values
            for col in json_columns - set(common_columns):
                if col not in yml_df.columns:
                    yml_df[col] = np.nan
            
            for col in yml_columns - set(common_columns):
                if col not in json_df.columns:
                    json_df[col] = np.nan
            
            # Concatenate the dataframes instead of merging
            # This avoids issues with unhashable types and complex merge logic
            merged_df = pd.concat([json_df, yml_df], ignore_index=True)
            
            # Remove duplicate user_ids, keeping the first occurrence (from JSON)
            if 'user_id' in merged_df.columns:
                merged_df = merged_df.drop_duplicates(subset=['user_id'], keep='first')
            
            logger.info(f"Merged people data with shape {merged_df.shape}")
            
            return {'people': merged_df}
            
        except Exception as e:
            error_msg = f"Unexpected error in people data merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'people': pd.DataFrame()}


class UserReferencesMerger(DataMerger):
    """Merger for adding user_id references to promotions and transactions."""
    
    def __init__(self, people_df: pd.DataFrame, promotions_df: pd.DataFrame, 
                transactions_df: Optional[pd.DataFrame] = None):
        """
        Initialize the merger with people, promotions, and transactions data.
        
        Args:
            people_df (pd.DataFrame): People data
            promotions_df (pd.DataFrame): Promotions data
            transactions_df (pd.DataFrame, optional): Transactions data
        """
        super().__init__()
        self.people_df = people_df
        self.promotions_df = promotions_df
        self.transactions_df = transactions_df
    
    def _add_user_references_to_promotions(self) -> pd.DataFrame:
        """
        Add user_id references to promotions based on email or phone.
        
        Returns:
            pd.DataFrame: Promotions DataFrame with user_id references
        """
        promotions_df = self.promotions_df.copy()
        
        # Check if user_id already exists and is populated
        if 'user_id' in promotions_df.columns and not promotions_df['user_id'].isna().all():
            logger.info("Promotions already have user_id references")
            return promotions_df
        
        # Initialize user_id column if it doesn't exist
        if 'user_id' not in promotions_df.columns:
            promotions_df['user_id'] = None
        
        # Check for email reference
        if 'client_email' in promotions_df.columns and 'email' in self.people_df.columns:
            email_map = self.people_df.set_index('email')['user_id'].to_dict()
            
            for index, row in promotions_df.iterrows():
                if pd.notna(row['client_email']) and row['client_email'] in email_map:
                    promotions_df.at[index, 'user_id'] = email_map[row['client_email']]
            
            # Drop client_email column since we now have user_id
            promotions_df.drop(columns=['client_email'], inplace=True, errors='ignore')
            logger.info("Added user references to promotions based on email")
        
        # Check for phone reference
        if 'telephone' in promotions_df.columns and 'phone' in self.people_df.columns:
            phone_map = self.people_df.set_index('phone')['user_id'].to_dict()
            
            # For rows that still have no user_id, try to find by phone
            mask = promotions_df['user_id'].isna()
            for index, row in promotions_df[mask].iterrows():
                if pd.notna(row['telephone']) and row['telephone'] in phone_map:
                    promotions_df.at[index, 'user_id'] = phone_map[row['telephone']]
            
            # Drop telephone column since we now have user_id
            promotions_df.drop(columns=['telephone'], inplace=True, errors='ignore')
            logger.info("Added user references to promotions based on phone")
        
        # Log warning for promotions without user_id
        missing_user_id = promotions_df['user_id'].isna().sum()
        if missing_user_id > 0:
            self._add_error(f"Could not find user_id for {missing_user_id} promotions")
        
        return promotions_df
    
    def _add_user_references_to_transactions(self) -> pd.DataFrame:
        """
        Add user_id references to transactions based on phone.
        
        Returns:
            pd.DataFrame: Transactions DataFrame with user_id references
        """
        if self.transactions_df is None:
            logger.info("No transactions data provided for user reference merging")
            return pd.DataFrame()
        
        transactions_df = self.transactions_df.copy()
        
        # Check if user_id already exists and is populated
        if 'user_id' in transactions_df.columns and not transactions_df['user_id'].isna().all():
            logger.info("Transactions already have user_id references")
            return transactions_df
        
        # Initialize user_id column if it doesn't exist
        if 'user_id' not in transactions_df.columns:
            transactions_df['user_id'] = None
        
        # Check for phone reference
        if 'phone' in transactions_df.columns and 'phone' in self.people_df.columns:
            phone_map = self.people_df.set_index('phone')['user_id'].to_dict()
            
            for index, row in transactions_df.iterrows():
                if pd.notna(row['phone']) and row['phone'] in phone_map:
                    transactions_df.at[index, 'user_id'] = phone_map[row['phone']]
            
            # Drop phone column since we now have user_id
            transactions_df.drop(columns=['phone'], inplace=True, errors='ignore')
            logger.info("Added user references to transactions based on phone")
        
        # Log warning for transactions without user_id
        missing_user_id = transactions_df['user_id'].isna().sum()
        if missing_user_id > 0:
            self._add_error(f"Could not find user_id for {missing_user_id} transactions")
        
        return transactions_df
    
    def identify_store_accounts(self) -> pd.DataFrame:
        """
        Identify potential store accounts based on transfer patterns.
        
        Returns:
            pd.DataFrame: Updated people DataFrame with is_store_account flag
        """
        logger.info("Identifying store accounts...")
        
        # Create a copy of the people DataFrame
        updated_people_df = self.people_df.copy()
        
        # Add is_store_account column with default False
        if 'is_store_account' not in updated_people_df.columns:
            updated_people_df['is_store_account'] = False
        
        # Only continue if we have transfers data
        if self.transfers_df is None or self.transfers_df.empty:
            logger.warning("No transfers data available to identify store accounts")
            return updated_people_df
            
        # Only continue if we have transactions data
        if self.transactions_df is None or self.transactions_df.empty:
            logger.warning("No transactions data available to identify store accounts")
            return updated_people_df
        
        # Count how many times each user appears as a recipient in transfers
        recipient_counts = self.transfers_df['recipient_id'].value_counts()
        
        # Find transaction amounts
        transaction_amounts = set(self.transactions_df['price'].round(2))
        
        store_account_ids = set()
        
        # For each frequent recipient, check if their transfer amounts match transaction amounts
        for user_id, count in recipient_counts.items():
            if count >= 10:  # Threshold for potential store account
                # Get transfers received by this user
                user_transfers = self.transfers_df[self.transfers_df['recipient_id'] == user_id]
                
                # Round transfer amounts for comparison
                transfer_amounts = set(user_transfers['amount'].round(2))
                
                # Check overlap between transfer amounts and transaction amounts
                common_amounts = transaction_amounts.intersection(transfer_amounts)
                
                # Calculate ratio of matching amounts
                match_ratio = len(common_amounts) / len(transfer_amounts) if len(transfer_amounts) > 0 else 0
                
                # If high match ratio, mark as store account
                if match_ratio > 0.5 and len(common_amounts) >= 5:
                    store_account_ids.add(user_id)
                    logger.info(f"Identified user_id {user_id} as potential store account " +
                               f"(match ratio: {match_ratio:.2f}, matching amounts: {len(common_amounts)})")
        
        # Mark identified accounts in the DataFrame
        updated_people_df.loc[updated_people_df['user_id'].isin(store_account_ids), 'is_store_account'] = True
        
        logger.info(f"Identified {len(store_account_ids)} potential store accounts")
        return updated_people_df
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Merge user references into promotions and transactions.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with updated DataFrames
        """
        try:
            logger.info("Adding user references to related data...")
            
            result = {}
            
            # Add user references to promotions
            promotions_df = self._add_user_references_to_promotions()
            result['promotions'] = promotions_df
            
            # Add user references to transactions if available
            if self.transactions_df is not None:
                transactions_df = self._add_user_references_to_transactions()
                result['transactions'] = transactions_df
            
            logger.info("Completed adding user references")
            return result
            
        except Exception as e:
            error_msg = f"Unexpected error in user reference merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'promotions': self.promotions_df, 'transactions': self.transactions_df}


class UserTransactionsMerger(DataMerger):
    """Merger for creating user-level transaction summaries."""
    
    def __init__(self, transactions_df: pd.DataFrame, people_df: pd.DataFrame):
        """
        Initialize the merger with transactions and people data.
        
        Args:
            transactions_df (pd.DataFrame): Transactions data
            people_df (pd.DataFrame): People data
        """
        super().__init__()
        self.transactions_df = transactions_df
        self.people_df = people_df
    
    def _get_favorite_store(self, stores: pd.Series) -> str:
        """
        Get the most frequent store for a user.
        
        Args:
            stores (pd.Series): Series of stores
        
        Returns:
            str: Most frequent store or None if no data
        """
        if stores.empty:
            return None
        
        mode = stores.mode()
        return mode.iloc[0] if not mode.empty else None
    
    def _get_favorite_item(self, items: pd.Series) -> str:
        """
        Get the most frequently purchased item for a user.
        
        Args:
            items (pd.Series): Series of items
        
        Returns:
            str: Most frequent item or None if no data
        """
        if items.empty:
            return None
        
        mode = items.mode()
        return mode.iloc[0] if not mode.empty else None
    
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Create user-level transaction summaries.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with user_transactions DataFrame
        """
        try:
            logger.info("Creating user-level transaction summaries...")
            
            # Ensure required columns exist
            required_columns = ['user_id', 'transaction_id', 'price', 'item', 'store']
            if not all(col in self.transactions_df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in self.transactions_df.columns]
                self._add_error(f"Missing required columns for user transactions summary: {missing}")
                return {'user_transactions': pd.DataFrame()}
            
            # Group transactions by user_id
            aggregated_df = self.transactions_df.groupby('user_id').agg(
                total_spent=('price', 'sum'),
                transaction_count=('transaction_id', 'nunique'),
                favorite_store=('store', self._get_favorite_store),
                favorite_item=('item', self._get_favorite_item)
            )
            
            # Reset index to make user_id a column
            aggregated_df = aggregated_df.reset_index()
            
            # Merge with people data to ensure all users are included
            result_df = pd.merge(self.people_df[['user_id']], aggregated_df, on='user_id', how='left')
            
            # Fill missing values for users with no transactions
            result_df['total_spent'] = result_df['total_spent'].fillna(0)
            result_df['transaction_count'] = result_df['transaction_count'].fillna(0).astype(int)
            
            logger.info(f"Created user transaction summaries with shape {result_df.shape}")
            
            return {'user_transactions': result_df}
            
        except Exception as e:
            error_msg = f"Unexpected error in user transactions merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'user_transactions': pd.DataFrame()}


class UserTransfersMerger(DataMerger):
    """Merger for creating user-level transfer summaries."""
    
    def __init__(self, transfers_df: pd.DataFrame, people_df: pd.DataFrame):
        """
        Initialize the merger with transfers and people data.
        
        Args:
            transfers_df (pd.DataFrame): Transfers data
            people_df (pd.DataFrame): People data
        """
        super().__init__()
        self.transfers_df = transfers_df
        self.people_df = people_df
    
    def link_transfers_to_transactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Link transfers to their corresponding transactions.
        
        Args:
            transactions_df (pd.DataFrame): Transactions data
        
        Returns:
            pd.DataFrame: Updated transfers DataFrame with related_transaction_id
        """
        logger.info("Linking transfers to transactions...")
        
        # Create a copy of the transfers DataFrame
        updated_transfers_df = self.transfers_df.copy()
        
        # Add related_transaction_id column with default None
        if 'related_transaction_id' not in updated_transfers_df.columns:
            updated_transfers_df['related_transaction_id'] = None
        
        # Only continue if we have transactions data
        if transactions_df is None or transactions_df.empty:
            logger.warning("No transactions data available to link transfers")
            return updated_transfers_df
        
        # Create mappings for faster lookups
        # For each store and amount, find matching transaction_ids
        transaction_lookup = {}
        for _, tx in transactions_df.iterrows():
            key = (tx['user_id'], round(tx['price'], 2))
            if key not in transaction_lookup:
                transaction_lookup[key] = []
            transaction_lookup[key].append(tx['transaction_id'])
        
        # Try to match transfers to transactions
        matched_count = 0
        
        for idx, transfer in updated_transfers_df.iterrows():
            sender_id = transfer['sender_id']
            amount = round(transfer['amount'], 2)
            
            # Look for matching transaction
            key = (sender_id, amount)
            if key in transaction_lookup and transaction_lookup[key]:
                # Use the first matching transaction and remove it from the list
                transaction_id = transaction_lookup[key].pop(0)
                updated_transfers_df.at[idx, 'related_transaction_id'] = transaction_id
                matched_count += 1
        
        logger.info(f"Linked {matched_count} transfers to transactions")
        return updated_transfers_df
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Create user-level transfer summaries.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with user_transfers DataFrame
        """
        try:
            logger.info("Creating user-level transfer summaries...")
            
            # Ensure required columns exist
            required_columns = ['transfer_id', 'sender_id', 'recipient_id', 'amount']
            if not all(col in self.transfers_df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in self.transfers_df.columns]
                self._add_error(f"Missing required columns for user transfers summary: {missing}")
                return {'user_transfers': pd.DataFrame()}
            
            # Calculate sent amounts
            sent_total = self.transfers_df.groupby('sender_id')['amount'].sum()
            sent_count = self.transfers_df.groupby('sender_id')['transfer_id'].nunique()
            
            # Calculate received amounts
            received_total = self.transfers_df.groupby('recipient_id')['amount'].sum()
            received_count = self.transfers_df.groupby('recipient_id')['transfer_id'].nunique()
            
            # Calculate net transferred
            net_transferred = pd.Series(dtype='float64')
            all_user_ids = set(self.transfers_df['sender_id']).union(set(self.transfers_df['recipient_id']))
            for user_id in all_user_ids:
                sent = sent_total.get(user_id, 0)
                received = received_total.get(user_id, 0)
                net_transferred[user_id] = received - sent
            
            # Create the result DataFrame
            result_df = pd.DataFrame({
                'user_id': list(all_user_ids)
            })
            
            # Add calculated columns
            result_df['total_sent'] = result_df['user_id'].map(sent_total).fillna(0)
            result_df['total_received'] = result_df['user_id'].map(received_total).fillna(0)
            result_df['net_transferred'] = result_df['user_id'].map(net_transferred).fillna(0)
            result_df['sent_count'] = result_df['user_id'].map(sent_count).fillna(0).astype(int)
            result_df['received_count'] = result_df['user_id'].map(received_count).fillna(0).astype(int)
            result_df['transfer_count'] = result_df['sent_count'] + result_df['received_count']
            
            # Merge with people data to ensure all users are included
            result_df = pd.merge(self.people_df[['user_id']], result_df, on='user_id', how='left')
            
            # Fill missing values for users with no transfers
            for col in ['total_sent', 'total_received', 'net_transferred']:
                result_df[col] = result_df[col].fillna(0)
            
            for col in ['sent_count', 'received_count', 'transfer_count']:
                result_df[col] = result_df[col].fillna(0).astype(int)
            
            logger.info(f"Created user transfer summaries with shape {result_df.shape}")
            
            return {'user_transfers': result_df}
            
        except Exception as e:
            error_msg = f"Unexpected error in user transfers merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'user_transfers': pd.DataFrame()}
    
class ItemSummaryMerger(DataMerger):
    """Merger for creating item-level summaries."""
    
    def __init__(self, transactions_df: pd.DataFrame):
        """
        Initialize the merger with transactions data.
        
        Args:
            transactions_df (pd.DataFrame): Transactions data
        """
        super().__init__()
        self.transactions_df = transactions_df
    
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Create item-level summaries.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with item_summary DataFrame
        """
        try:
            logger.info("Creating item-level summaries...")
            
            # Ensure required columns exist
            required_columns = ['item', 'price', 'quantity', 'transaction_id']
            if not all(col in self.transactions_df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in self.transactions_df.columns]
                self._add_error(f"Missing required columns for item summary: {missing}")
                return {'item_summary': pd.DataFrame()}
            
            # Group transactions by item
            aggregated_df = self.transactions_df.groupby('item').agg(
                total_revenue=('price', 'sum'),
                items_sold=('quantity', 'sum'),
                transaction_count=('transaction_id', 'nunique')
            )
            
            # Calculate average price per item
            aggregated_df['average_price'] = (aggregated_df['total_revenue'] / aggregated_df['items_sold']).round(2)
            
            # Reset index to make item a column
            aggregated_df = aggregated_df.reset_index()
            
            logger.info(f"Created item summaries with shape {aggregated_df.shape}")
            
            return {'item_summary': aggregated_df}
            
        except Exception as e:
            error_msg = f"Unexpected error in item summary merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'item_summary': pd.DataFrame()}


class StoreSummaryMerger(DataMerger):
    """Merger for creating store-level summaries."""
    
    def __init__(self, transactions_df: pd.DataFrame):
        """
        Initialize the merger with transactions data.
        
        Args:
            transactions_df (pd.DataFrame): Transactions data
        """
        super().__init__()
        self.transactions_df = transactions_df
    
    def _get_most_sold_item(self, store: str) -> str:
        """
        Get the most sold item for a store based on quantity.
        
        Args:
            store (str): Store name
        
        Returns:
            str: Most sold item or None if no data
        """
        store_data = self.transactions_df[self.transactions_df['store'] == store]
        if store_data.empty:
            return None
        
        item_qty = store_data.groupby('item')['quantity'].sum()
        return item_qty.idxmax() if not item_qty.empty else None
    
    def _get_most_profitable_item(self, store: str) -> str:
        """
        Get the most profitable item for a store based on total revenue.
        
        Args:
            store (str): Store name
        
        Returns:
            str: Most profitable item or None if no data
        """
        store_data = self.transactions_df[self.transactions_df['store'] == store]
        if store_data.empty:
            return None
        
        item_revenue = store_data.groupby('item')['price'].sum()
        return item_revenue.idxmax() if not item_revenue.empty else None
    
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Create store-level summaries.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with store_summary DataFrame
        """
        try:
            logger.info("Creating store-level summaries...")
            
            # Ensure required columns exist
            required_columns = ['store', 'item', 'price', 'quantity', 'transaction_id']
            if not all(col in self.transactions_df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in self.transactions_df.columns]
                self._add_error(f"Missing required columns for store summary: {missing}")
                return {'store_summary': pd.DataFrame()}
            
            # Group transactions by store
            aggregated_df = self.transactions_df.groupby('store').agg(
                total_revenue=('price', 'sum'),
                items_sold=('quantity', 'sum'),
                total_transactions=('transaction_id', 'nunique')
            )
            
            # Calculate average transaction value
            aggregated_df['average_transaction_value'] = (
                aggregated_df['total_revenue'] / aggregated_df['total_transactions']
            ).round(2)
            
            # Add most sold and most profitable items
            stores = aggregated_df.index.tolist()
            
            most_sold_items = []
            most_profitable_items = []
            
            for store in stores:
                most_sold_items.append(self._get_most_sold_item(store))
                most_profitable_items.append(self._get_most_profitable_item(store))
            
            aggregated_df['most_sold_item'] = most_sold_items
            aggregated_df['most_profitable_item'] = most_profitable_items
            
            # Reset index to make store a column
            aggregated_df = aggregated_df.reset_index()
            
            logger.info(f"Created store summaries with shape {aggregated_df.shape}")
            
            return {'store_summary': aggregated_df}
            
        except Exception as e:
            error_msg = f"Unexpected error in store summary merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
            return {'store_summary': pd.DataFrame()}


class MainDataMerger(DataMerger):
    """Main merger class to orchestrate the entire merging process."""
    
    def __init__(self, 
                people_json_df: pd.DataFrame, 
                people_yml_df: pd.DataFrame,
                promotions_df: pd.DataFrame,
                transfers_df: pd.DataFrame,
                transactions_df: Optional[pd.DataFrame] = None,
                output_dir: str = 'data/processed'):
        """
        Initialize the main merger with all data sources.
        
        Args:
            people_json_df (pd.DataFrame): People data from JSON
            people_yml_df (pd.DataFrame): People data from YAML
            promotions_df (pd.DataFrame): Promotions data
            transfers_df (pd.DataFrame): Transfers data
            transactions_df (pd.DataFrame, optional): Transactions data
            output_dir (str): Directory to save processed data
        """
        super().__init__()
        self.people_json_df = people_json_df
        self.people_yml_df = people_yml_df
        self.promotions_df = promotions_df
        self.transfers_df = transfers_df
        self.transactions_df = transactions_df
        self.output_dir = output_dir
    
    def merge(self) -> Dict[str, pd.DataFrame]:
        """
        Execute the full merging pipeline.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with all merged DataFrames
        """
        all_results = {}
        
        try:
            logger.info("Starting main data merging process...")
            
            # Step 1: Merge people data from JSON and YAML
            try:
                people_merger = PeopleMerger(self.people_json_df, self.people_yml_df)
                people_results = people_merger.merge()
                all_results.update(people_results)
                
                # Check if we have people data
                if 'people' not in all_results or all_results['people'].empty:
                    self._add_error("Failed to merge people data, cannot continue")
                    return all_results
                    
                people_df = all_results['people']
                logger.info(f"Successfully merged people data with shape {people_df.shape}")
                
                # Save the people data immediately
                self._save_dataframe(people_df, "people", self.output_dir)
            except Exception as e:
                error_msg = f"Error in people merging: {str(e)}"
                logger.error(error_msg)
                self._add_error(error_msg)
                return all_results
            
            # Step 2: Add user references to promotions and transactions
            try:
                user_refs_merger = UserReferencesMerger(
                    people_df, 
                    self.promotions_df,
                    self.transactions_df
                )
                user_refs_results = user_refs_merger.merge()
                all_results.update(user_refs_results)
                
                # Get the updated DataFrames
                promotions_df = user_refs_results.get('promotions', self.promotions_df)
                transactions_df = user_refs_results.get('transactions', self.transactions_df)
                
                # Identify store accounts (NEW)
                updated_people_df = user_refs_merger.identify_store_accounts()
                all_results['people'] = updated_people_df
                
                # Save the updated people data
                self._save_dataframe(updated_people_df, "people", self.output_dir)
                
                # Save the promotions data immediately
                if 'promotions' in all_results:
                    self._save_dataframe(all_results['promotions'], "promotions", self.output_dir)
                    logger.info(f"Saved promotions data with shape {all_results['promotions'].shape}")
                    
                # Save the transactions data immediately if it exists
                if 'transactions' in all_results:
                    self._save_dataframe(all_results['transactions'], "transactions", self.output_dir)
                    logger.info(f"Saved transactions data with shape {all_results['transactions'].shape}")
            except Exception as e:
                error_msg = f"Error in user references merging: {str(e)}"
                logger.error(error_msg)
                self._add_error(error_msg)
                # Continue with other steps
            
            # Step 3: Create user transaction summaries
            if transactions_df is not None and not transactions_df.empty:
                try:
                    user_transactions_merger = UserTransactionsMerger(transactions_df, people_df)
                    user_transactions_results = user_transactions_merger.merge()
                    all_results.update(user_transactions_results)
                    
                    # Save the user transactions data immediately
                    if 'user_transactions' in all_results:
                        self._save_dataframe(all_results['user_transactions'], "user_transactions", self.output_dir)
                        logger.info(f"Saved user transactions data with shape {all_results['user_transactions'].shape}")
                except Exception as e:
                    error_msg = f"Error in user transactions merging: {str(e)}"
                    logger.error(error_msg)
                    self._add_error(error_msg)
            
                # Step 4: Create item and store summaries
                try:
                    item_summary_merger = ItemSummaryMerger(transactions_df)
                    item_summary_results = item_summary_merger.merge()
                    all_results.update(item_summary_results)
                    
                    # Save the item summary data immediately
                    if 'item_summary' in all_results:
                        self._save_dataframe(all_results['item_summary'], "item_summary", self.output_dir)
                        logger.info(f"Saved item summary data with shape {all_results['item_summary'].shape}")
                except Exception as e:
                    error_msg = f"Error in item summary merging: {str(e)}"
                    logger.error(error_msg)
                    self._add_error(error_msg)
                    
                try:
                    store_summary_merger = StoreSummaryMerger(transactions_df)
                    store_summary_results = store_summary_merger.merge()
                    all_results.update(store_summary_results)
                    
                    # Save the store summary data immediately
                    if 'store_summary' in all_results:
                        self._save_dataframe(all_results['store_summary'], "store_summary", self.output_dir)
                        logger.info(f"Saved store summary data with shape {all_results['store_summary'].shape}")
                except Exception as e:
                    error_msg = f"Error in store summary merging: {str(e)}"
                    logger.error(error_msg)
                    self._add_error(error_msg)
            
            # Step 5: Create user transfer summaries and link transfers to transactions
            try:
                user_transfers_merger = UserTransfersMerger(self.transfers_df, people_df)
                
                # Link transfers to transactions (NEW)
                if transactions_df is not None and not transactions_df.empty:
                    updated_transfers_df = user_transfers_merger.link_transfers_to_transactions(transactions_df)
                    self.transfers_df = updated_transfers_df  # Update transfers data
                    all_results['transfers'] = updated_transfers_df
                    
                    # Save the updated transfers data
                    self._save_dataframe(updated_transfers_df, "transfers", self.output_dir)
                
                # Continue with regular transfer summaries
                user_transfers_results = user_transfers_merger.merge()
                all_results.update(user_transfers_results)
                
                # Save the user transfers data immediately
                if 'user_transfers' in all_results:
                    self._save_dataframe(all_results['user_transfers'], "user_transfers", self.output_dir)
                    logger.info(f"Saved user transfers data with shape {all_results['user_transfers'].shape}")
            except Exception as e:
                error_msg = f"Error in user transfers merging: {str(e)}"
                logger.error(error_msg)
                self._add_error(error_msg)
            
            logger.info("Completed main data merging process")
            
        except Exception as e:
            error_msg = f"Unexpected error in main data merging: {str(e)}"
            logger.error(error_msg)
            self._add_error(error_msg)
        
        return all_results