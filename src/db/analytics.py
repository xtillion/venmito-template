"""
Analytics module for Venmito project.

This module provides SQL-based analytical functions for the Venmito data.
"""

import logging
import pandas as pd
from typing import Dict, Any, Optional, List, Union, Tuple

from src.db.db import Database, DatabaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Analytics:
    """Class for performing analytics on Venmito data."""
    
    @staticmethod
    def execute_query_to_df(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a pandas DataFrame.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
        
        Returns:
            pd.DataFrame: Query results as a DataFrame
        
        Raises:
            DatabaseError: If query execution fails
        """
        try:
            results = Database.execute_query(query, params)
            
            # Get column names from the cursor description
            with Database.get_cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
            
            # Create a DataFrame from the results
            df = pd.DataFrame(results, columns=columns)
            logger.info(f"Query returned {len(df)} rows")
            return df
        
        except Exception as e:
            error_msg = f"Error executing analytics query: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    @classmethod
    def get_top_users_by_spending(cls, limit: int = 10) -> pd.DataFrame:
        """
        Get the top users by spending.
        
        Args:
            limit (int): Maximum number of users to return
        
        Returns:
            pd.DataFrame: DataFrame with top users
        """
        query = """
            SELECT 
                p.user_id, 
                p.first_name, 
                p.last_name, 
                p.email,
                ut.total_spent,
                ut.transaction_count,
                ut.favorite_store,
                ut.favorite_item
            FROM 
                people p
            JOIN 
                user_transactions ut ON p.user_id = ut.user_id
            ORDER BY 
                ut.total_spent DESC
            LIMIT %s
        """
        
        return cls.execute_query_to_df(query, (limit,))
    
    @classmethod
    def get_top_users_by_transfers(cls, limit: int = 10) -> pd.DataFrame:
        """
        Get the top users by transfer activity (sent + received).
        
        Args:
            limit (int): Maximum number of users to return
        
        Returns:
            pd.DataFrame: DataFrame with top users
        """
        query = """
            SELECT 
                p.user_id, 
                p.first_name, 
                p.last_name, 
                p.email,
                ut.total_sent,
                ut.total_received,
                ut.net_transferred,
                ut.transfer_count
            FROM 
                people p
            JOIN 
                user_transfers ut ON p.user_id = ut.user_id
            ORDER BY 
                ut.transfer_count DESC
            LIMIT %s
        """
        
        return cls.execute_query_to_df(query, (limit,))
    
    @classmethod
    def get_top_stores_by_revenue(cls, limit: int = 10) -> pd.DataFrame:
        """
        Get the top stores by revenue.
        
        Args:
            limit (int): Maximum number of stores to return
        
        Returns:
            pd.DataFrame: DataFrame with top stores
        """
        query = """
            SELECT 
                store,
                total_revenue,
                items_sold,
                total_transactions,
                average_transaction_value,
                most_sold_item,
                most_profitable_item
            FROM 
                store_summary
            ORDER BY 
                total_revenue DESC
            LIMIT %s
        """
        
        return cls.execute_query_to_df(query, (limit,))
    
    @classmethod
    def get_top_items_by_revenue(cls, limit: int = 10) -> pd.DataFrame:
        """
        Get the top items by revenue.
        
        Args:
            limit (int): Maximum number of items to return
        
        Returns:
            pd.DataFrame: DataFrame with top items
        """
        query = """
            SELECT 
                item,
                total_revenue,
                items_sold,
                transaction_count,
                average_price
            FROM 
                item_summary
            ORDER BY 
                total_revenue DESC
            LIMIT %s
        """
        
        return cls.execute_query_to_df(query, (limit,))
    
    @classmethod
    def get_user_profile(cls, user_id: int) -> Dict[str, Any]:
        """
        Get a complete profile for a specific user.
        
        Args:
            user_id (int): User ID
        
        Returns:
            Dict[str, Any]: Dictionary with user profile data
        """
        user_query = """
            SELECT 
                p.user_id, 
                p.first_name, 
                p.last_name, 
                p.email,
                p.city,
                p.country,
                p.devices,
                p.phone
            FROM 
                people p
            WHERE 
                p.user_id = %s
        """
        
        transactions_query = """
            SELECT 
                ut.total_spent,
                ut.transaction_count,
                ut.favorite_store,
                ut.favorite_item
            FROM 
                user_transactions ut
            WHERE 
                ut.user_id = %s
        """
        
        transfers_query = """
            SELECT 
                ut.total_sent,
                ut.total_received,
                ut.net_transferred,
                ut.sent_count,
                ut.received_count,
                ut.transfer_count
            FROM 
                user_transfers ut
            WHERE 
                ut.user_id = %s
        """
        
        recent_transactions_query = """
            SELECT 
                transaction_id,
                item,
                store,
                price,
                quantity,
                price_per_item
            FROM 
                transactions
            WHERE 
                user_id = %s
            ORDER BY 
                transaction_id DESC
            LIMIT 5
        """
        
        recent_transfers_sent_query = """
            SELECT 
                t.transfer_id,
                t.recipient_id,
                p.first_name || ' ' || p.last_name AS recipient_name,
                t.amount,
                t.timestamp
            FROM 
                transfers t
            JOIN
                people p ON t.recipient_id = p.user_id
            WHERE 
                t.sender_id = %s
            ORDER BY 
                t.timestamp DESC
            LIMIT 5
        """
        
        recent_transfers_received_query = """
            SELECT 
                t.transfer_id,
                t.sender_id,
                p.first_name || ' ' || p.last_name AS sender_name,
                t.amount,
                t.timestamp
            FROM 
                transfers t
            JOIN
                people p ON t.sender_id = p.user_id
            WHERE 
                t.recipient_id = %s
            ORDER BY 
                t.timestamp DESC
            LIMIT 5
        """
        
        try:
            # Get basic user info
            user_df = cls.execute_query_to_df(user_query, (user_id,))
            if user_df.empty:
                raise ValueError(f"User with ID {user_id} not found")
            
            user_data = user_df.iloc[0].to_dict()
            
            # Get transaction summary
            transactions_df = cls.execute_query_to_df(transactions_query, (user_id,))
            if not transactions_df.empty:
                user_data.update(transactions_df.iloc[0].to_dict())
            
            # Get transfer summary
            transfers_df = cls.execute_query_to_df(transfers_query, (user_id,))
            if not transfers_df.empty:
                user_data.update(transfers_df.iloc[0].to_dict())
            
            # Get recent transactions
            recent_transactions = cls.execute_query_to_df(recent_transactions_query, (user_id,))
            user_data['recent_transactions'] = recent_transactions.to_dict(orient='records')
            
            # Get recent transfers sent
            recent_transfers_sent = cls.execute_query_to_df(recent_transfers_sent_query, (user_id,))
            user_data['recent_transfers_sent'] = recent_transfers_sent.to_dict(orient='records')
            
            # Get recent transfers received
            recent_transfers_received = cls.execute_query_to_df(recent_transfers_received_query, (user_id,))
            user_data['recent_transfers_received'] = recent_transfers_received.to_dict(orient='records')
            
            return user_data
            
        except Exception as e:
            error_msg = f"Error retrieving user profile for ID {user_id}: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    @classmethod
    def get_monthly_transaction_summary(cls, year: int = None) -> pd.DataFrame:
        """
        Get a monthly summary of transactions.
        
        Args:
            year (int, optional): Year to filter by
        
        Returns:
            pd.DataFrame: DataFrame with monthly transaction summary
        """
        if year:
            query = """
                SELECT 
                    DATE_TRUNC('month', t.timestamp) AS month,
                    COUNT(*) AS transaction_count,
                    SUM(t.price) AS total_revenue,
                    AVG(t.price) AS average_transaction_value,
                    COUNT(DISTINCT t.user_id) AS unique_users
                FROM 
                    transactions t
                WHERE
                    EXTRACT(YEAR FROM t.timestamp) = %s
                GROUP BY 
                    DATE_TRUNC('month', t.timestamp)
                ORDER BY 
                    month
            """
            return cls.execute_query_to_df(query, (year,))
        else:
            query = """
                SELECT 
                    DATE_TRUNC('month', t.timestamp) AS month,
                    COUNT(*) AS transaction_count,
                    SUM(t.price) AS total_revenue,
                    AVG(t.price) AS average_transaction_value,
                    COUNT(DISTINCT t.user_id) AS unique_users
                FROM 
                    transactions t
                GROUP BY 
                    DATE_TRUNC('month', t.timestamp)
                ORDER BY 
                    month
            """
            return cls.execute_query_to_df(query)
    
    @classmethod
    def get_promotion_effectiveness(cls) -> pd.DataFrame:
        """
        Analyze the effectiveness of different promotions.
        
        Returns:
            pd.DataFrame: DataFrame with promotion effectiveness metrics
        """
        query = """
            SELECT 
                p.promotion,
                COUNT(*) AS total_sent,
                SUM(CASE WHEN p.responded = 'Yes' THEN 1 ELSE 0 END) AS responded_yes,
                ROUND(
                    (SUM(CASE WHEN p.responded = 'Yes' THEN 1 ELSE 0 END)::FLOAT / COUNT(*)) * 100,
                    2
                ) AS response_rate,
                AVG(p.amount) AS average_amount
            FROM 
                promotions p
            GROUP BY 
                p.promotion
            ORDER BY 
                response_rate DESC
        """
        
        return cls.execute_query_to_df(query)
    
    @classmethod
    def get_user_cohort_analysis(cls, date_column: str = 'timestamp') -> pd.DataFrame:
        """
        Perform cohort analysis for users based on their first transaction date.
        
        Args:
            date_column (str): Column to use for date filtering ('timestamp')
        
        Returns:
            pd.DataFrame: DataFrame with cohort analysis
        """
        query = f"""
            WITH first_transactions AS (
                SELECT
                    user_id,
                    DATE_TRUNC('month', MIN({date_column})) AS cohort_month
                FROM
                    transactions
                GROUP BY
                    user_id
            ),
            monthly_activity AS (
                SELECT
                    ft.user_id,
                    ft.cohort_month,
                    DATE_TRUNC('month', t.{date_column}) AS activity_month,
                    (EXTRACT(YEAR FROM DATE_TRUNC('month', t.{date_column})) - 
                     EXTRACT(YEAR FROM ft.cohort_month)) * 12 +
                    (EXTRACT(MONTH FROM DATE_TRUNC('month', t.{date_column})) - 
                     EXTRACT(MONTH FROM ft.cohort_month)) AS month_number
                FROM
                    transactions t
                JOIN
                    first_transactions ft ON t.user_id = ft.user_id
            ),
            cohort_size AS (
                SELECT
                    cohort_month,
                    COUNT(DISTINCT user_id) AS users
                FROM
                    first_transactions
                GROUP BY
                    cohort_month
            ),
            retention AS (
                SELECT
                    cohort_month,
                    month_number,
                    COUNT(DISTINCT user_id) AS active_users
                FROM
                    monthly_activity
                GROUP BY
                    cohort_month,
                    month_number
            )
            SELECT
                c.cohort_month,
                c.users AS cohort_size,
                r.month_number,
                r.active_users,
                ROUND(
                    (r.active_users::FLOAT / c.users) * 100,
                    2
                ) AS retention_rate
            FROM
                cohort_size chttps://claude.ai/chat/142ee15c-9e77-4e6d-892d-ecdd11a4ea38
            JOIN
                retention r ON c.cohort_month = r.cohort_month
            ORDER BY
                c.cohort_month,
                r.month_number
        """
        
        return cls.execute_query_to_df(query)
    
    @classmethod
    def get_customer_lifetime_value(cls, segment_by_country: bool = False) -> pd.DataFrame:
        """
        Calculate customer lifetime value (CLV).
        
        Args:
            segment_by_country (bool): Whether to segment CLV by country
        
        Returns:
            pd.DataFrame: DataFrame with CLV calculations
        """
        if segment_by_country:
            query = """
                SELECT
                    p.country,
                    COUNT(DISTINCT p.user_id) AS user_count,
                    ROUND(AVG(ut.total_spent), 2) AS average_spent_per_user,
                    ROUND(AVG(ut.transaction_count), 2) AS average_transactions_per_user,
                    ROUND(SUM(ut.total_spent) / COUNT(DISTINCT p.user_id), 2) AS customer_lifetime_value
                FROM
                    people p
                JOIN
                    user_transactions ut ON p.user_id = ut.user_id
                GROUP BY
                    p.country
                ORDER BY
                    customer_lifetime_value DESC
            """
        else:
            query = """
                SELECT
                    COUNT(DISTINCT p.user_id) AS user_count,
                    ROUND(AVG(ut.total_spent), 2) AS average_spent_per_user,
                    ROUND(AVG(ut.transaction_count), 2) AS average_transactions_per_user,
                    ROUND(SUM(ut.total_spent) / COUNT(DISTINCT p.user_id), 2) AS customer_lifetime_value
                FROM
                    people p
                JOIN
                    user_transactions ut ON p.user_id = ut.user_id
            """
        
        return cls.execute_query_to_df(query)
    
    @classmethod
    def custom_query(cls, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Execute a custom SQL query.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
        
        Returns:
            pd.DataFrame: Query results as a DataFrame
        """
        return cls.execute_query_to_df(query, params)