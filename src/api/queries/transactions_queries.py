"""
Database queries for transactions data.

This module provides functions for accessing and manipulating transactions data.
"""

import logging
from typing import Dict, Any, Optional, List

from src.db.config import execute_query

# Configure logging
logger = logging.getLogger(__name__)

def get_all_transactions(limit: int = 100, offset: int = 0,
                       user_id: Optional[int] = None,
                       item: Optional[str] = None,
                       store: Optional[str] = None,
                       min_price: Optional[float] = None,
                       max_price: Optional[float] = None,
                       include_first_item: bool = True):
    """
    Get all transactions with optional filtering.
    
    Args:
        limit (int): Maximum number of transactions to return
        offset (int): Number of transactions to skip
        user_id (int, optional): Filter by user ID
        item (str, optional): Filter by item name
        store (str, optional): Filter by store name
        min_price (float, optional): Filter by minimum price
        max_price (float, optional): Filter by maximum price
        include_first_item (bool): Whether to include the first item for each transaction
    
    Returns:
        list: List of transaction records
    """
    base_query = """
    SELECT 
        t.transaction_id, 
        t.user_id, 
        t.store,
        t.price,
        t.transaction_date,
        COUNT(ti.item_id) as item_count
    """
    
    if include_first_item:
        # Add a subquery to get the first item for each transaction
        base_query += """
        , (
            SELECT item FROM transaction_items 
            WHERE transaction_id = t.transaction_id 
            ORDER BY item_id LIMIT 1
        ) as first_item
        """
    
    base_query += """
    FROM transactions t
    LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    """
    
    # Item filter requires joining with transaction_items
    if item:
        base_query += """
        JOIN transaction_items filter_items ON t.transaction_id = filter_items.transaction_id 
            AND filter_items.item ILIKE %(item)s
        """
    
    base_query += " WHERE 1=1 "
    
    params = {}
    
    if user_id:
        base_query += " AND t.user_id = %(user_id)s"
        params['user_id'] = user_id
    
    if item:
        params['item'] = f'%{item}%'
    
    if store:
        base_query += " AND t.store ILIKE %(store)s"
        params['store'] = f'%{store}%'
    
    if min_price is not None:
        base_query += " AND t.price >= %(min_price)s"
        params['min_price'] = min_price
    
    if max_price is not None:
        base_query += " AND t.price <= %(max_price)s"
        params['max_price'] = max_price
    
    base_query += """
    GROUP BY t.transaction_id, t.user_id, t.store, t.price, t.transaction_date
    ORDER BY t.transaction_date DESC
    LIMIT %(limit)s OFFSET %(offset)s
    """
    
    params.update({
        'limit': limit,
        'offset': offset
    })
    
    return execute_query(base_query, params)

def get_transaction_items_by_id(transaction_id: str):
    """
    Get items for a specific transaction.
    
    Args:
        transaction_id (str): Transaction ID
    
    Returns:
        list: List of transaction item records
    """
    query = """
    SELECT 
        item_id,
        transaction_id,
        item,
        quantity,
        price_per_item,
        subtotal
    FROM transaction_items
    WHERE transaction_id = %(transaction_id)s
    ORDER BY item_id
    """
    
    params = {'transaction_id': transaction_id}
    
    return execute_query(query, params)
def get_transaction_by_id(transaction_id: str):
    """
    Get a transaction by ID.
    
    Args:
        transaction_id (str): Transaction ID
    
    Returns:
        dict: Transaction record or None if not found
    """
    query = """
    SELECT 
        t.transaction_id, 
        t.user_id, 
        t.store,
        t.price,
        t.transaction_date,
        COUNT(ti.item_id) as item_count
    FROM transactions t
    LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    WHERE t.transaction_id = %(transaction_id)s
    GROUP BY t.transaction_id, t.user_id, t.store, t.price, t.transaction_date
    """
    
    params = {'transaction_id': transaction_id}
    
    return execute_query(query, params, fetchall=False)


def get_transactions_count(user_id: Optional[int] = None,
                         item: Optional[str] = None,
                         store: Optional[str] = None,
                         min_price: Optional[float] = None,
                         max_price: Optional[float] = None):
    """
    Get the total number of transactions, optionally filtered.
    
    Args:
        user_id (int, optional): Filter by user ID
        item (str, optional): Filter by item name
        store (str, optional): Filter by store name
        min_price (float, optional): Filter by minimum price
        max_price (float, optional): Filter by maximum price
    
    Returns:
        int: Total number of transactions
    """
    query = """
    SELECT COUNT(*) as count
    FROM transactions t
    WHERE 1=1
    """
    
    params = {}
    
    if user_id:
        query += " AND t.user_id = %(user_id)s"
        params['user_id'] = user_id
    
    if item:
        query += " AND t.item ILIKE %(item)s"
        params['item'] = f'%{item}%'
    
    if store:
        query += " AND t.store ILIKE %(store)s"
        params['store'] = f'%{store}%'
    
    if min_price is not None:
        query += " AND t.price >= %(min_price)s"
        params['min_price'] = min_price
    
    if max_price is not None:
        query += " AND t.price <= %(max_price)s"
        params['max_price'] = max_price
    
    result = execute_query(query, params, fetchall=False)
    return result['count'] if result else 0


def get_user_transactions_summary(user_id: int):
    """
    Get a summary of a user's transactions.
    
    Args:
        user_id (int): User ID
    
    Returns:
        dict: Summary of user's transactions
    """
    query = """
    SELECT
        user_id,
        SUM(price) AS total_spent,
        COUNT(*) AS transaction_count,
        (
            SELECT store
            FROM transactions
            WHERE user_id = %(user_id)s
            GROUP BY store
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS favorite_store,
        (
            SELECT item
            FROM transactions
            WHERE user_id = %(user_id)s
            GROUP BY item
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS favorite_item
    FROM transactions
    WHERE user_id = %(user_id)s
    GROUP BY user_id
    """
    
    params = {'user_id': user_id}
    
    return execute_query(query, params, fetchall=False)


def get_item_summary(limit: int = 20):
    """
    Get a summary of items sold.
    
    Args:
        limit (int): Maximum number of items to return
    
    Returns:
        list: Summary of items
    """
    query = """
    SELECT
        item,
        SUM(subtotal) AS total_revenue,
        SUM(quantity) AS items_sold,
        COUNT(DISTINCT transaction_id) AS transaction_count,
        ROUND(AVG(price_per_item), 2) AS average_price
    FROM transaction_items
    GROUP BY item
    ORDER BY total_revenue DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)


def get_store_summary(limit: int = 20):
    """
    Get a summary of stores.
    
    Args:
        limit (int): Maximum number of stores to return
    
    Returns:
        list: Summary of stores
    """
    query = """
    SELECT
        t.store,
        SUM(t.price) AS total_revenue,
        COUNT(DISTINCT t.transaction_id) AS total_transactions,
        ROUND(SUM(t.price) / COUNT(DISTINCT t.transaction_id), 2) AS average_transaction_value,
        (
            SELECT ti.item
            FROM transaction_items ti
            JOIN transactions t2 ON ti.transaction_id = t2.transaction_id
            WHERE t2.store = t.store
            GROUP BY ti.item
            ORDER BY SUM(ti.quantity) DESC
            LIMIT 1
        ) AS most_sold_item,
        (
            SELECT ti.item
            FROM transaction_items ti
            JOIN transactions t2 ON ti.transaction_id = t2.transaction_id
            WHERE t2.store = t.store
            GROUP BY ti.item
            ORDER BY SUM(ti.subtotal) DESC
            LIMIT 1
        ) AS most_profitable_item
    FROM transactions t
    GROUP BY t.store
    ORDER BY total_revenue DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)

def get_top_transactions_by_amount(limit: int = 5):
    """
    Get top transactions by amount.
    
    Args:
        limit (int): Maximum number of transactions to return
    
    Returns:
        list: List of top transaction records sorted by price
    """
    query = """
    SELECT 
        transaction_id, 
        user_id, 
        store,
        price,
        transaction_date
    FROM transactions
    ORDER BY price DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)