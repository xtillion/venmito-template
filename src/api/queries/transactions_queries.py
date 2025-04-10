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
                       max_price: Optional[float] = None):
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
    
    Returns:
        list: List of transaction records
    """
    query = """
    SELECT 
        t.transaction_id, 
        t.user_id, 
        t.item, 
        t.store,
        t.price,
        t.quantity,
        t.price_per_item,
        t.transaction_date
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
    
    query += """
    ORDER BY t.transaction_id
    LIMIT %(limit)s OFFSET %(offset)s
    """
    
    params.update({
        'limit': limit,
        'offset': offset
    })
    
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
        t.item, 
        t.store,
        t.price,
        t.quantity,
        t.price_per_item,
        p.first_name,
        p.last_name
    FROM transactions t
    JOIN people p ON t.user_id = p.user_id
    WHERE t.transaction_id = %(transaction_id)s
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
        SUM(price) AS total_revenue,
        SUM(quantity) AS items_sold,
        COUNT(*) AS transaction_count,
        ROUND(AVG(price_per_item), 2) AS average_price
    FROM transactions
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
        store,
        SUM(price) AS total_revenue,
        SUM(quantity) AS items_sold,
        COUNT(*) AS total_transactions,
        ROUND(SUM(price) / COUNT(*), 2) AS average_transaction_value,
        (
            SELECT item
            FROM transactions t2
            WHERE t2.store = t1.store
            GROUP BY item
            ORDER BY SUM(quantity) DESC
            LIMIT 1
        ) AS most_sold_item,
        (
            SELECT item
            FROM transactions t2
            WHERE t2.store = t1.store
            GROUP BY item
            ORDER BY SUM(price) DESC
            LIMIT 1
        ) AS most_profitable_item
    FROM transactions t1
    GROUP BY store
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
        item, 
        store,
        price,
        quantity,
        price_per_item,
        transaction_date
    FROM transactions
    ORDER BY price DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)