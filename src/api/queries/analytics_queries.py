"""
Database queries for analytics data.

This module provides functions for accessing analytics data.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from src.db.config import execute_query

# Configure logging
logger = logging.getLogger(__name__)

def get_daily_transactions_summary(days: int = 365):
    """
    Get a summary of daily transactions across all historical data.
    
    Args:
        days (int): Number of days to include (default to full history)
    
    Returns:
        list: Daily transaction summaries
    """
    query = """
    WITH date_series AS (
        SELECT generate_series(
            (SELECT MIN(DATE(transaction_date)) FROM transactions),
            (SELECT MAX(DATE(transaction_date)) FROM transactions),
            '1 day'::interval
        )::date AS day
    )
    SELECT
        ds.day::date AS date,
        COALESCE(COUNT(t.transaction_id), 0) AS transaction_count,
        COALESCE(SUM(t.price), 0) AS total_amount,
        COALESCE(AVG(t.price), 0) AS average_transaction_value,
        COALESCE(COUNT(DISTINCT t.user_id), 0) AS unique_users
    FROM date_series ds
    LEFT JOIN transactions t ON DATE(t.transaction_date) = ds.day
    GROUP BY ds.day
    ORDER BY ds.day
    """
    
    return execute_query(query)

def get_daily_transfers_summary(days: int = 30):
    """
    Get a summary of daily transfers.
    
    Args:
        days (int): Number of days to include
    
    Returns:
        list: Daily transfer summaries
    """
    query = """
    WITH date_series AS (
        SELECT generate_series(
            current_date - %(days)s::interval,
            current_date,
            '1 day'::interval
        )::date AS day
    )
    SELECT
        ds.day::date AS date,
        COALESCE(COUNT(t.transfer_id), 0) AS transfer_count,
        COALESCE(SUM(t.amount), 0) AS total_amount,
        COALESCE(AVG(t.amount), 0) AS average_transfer_amount,
        COALESCE(COUNT(DISTINCT t.sender_id), 0) AS unique_senders,
        COALESCE(COUNT(DISTINCT t.recipient_id), 0) AS unique_recipients
    FROM date_series ds
    LEFT JOIN transfers t ON DATE(t.timestamp) = ds.day
    GROUP BY ds.day
    ORDER BY ds.day
    """
    
    params = {'days': f'{days} days'}
    
    return execute_query(query, params)


def get_top_users_by_spending(limit: int = 10):
    """
    Get top users by total spending.
    
    Args:
        limit (int): Maximum number of users to return
    
    Returns:
        list: Top users by spending
    """
    query = """
    SELECT
        p.user_id,
        p.first_name,
        p.last_name,
        p.email,
        COALESCE(SUM(t.price), 0) AS total_spent,
        COUNT(t.transaction_id) AS transaction_count,
        COALESCE(AVG(t.price), 0) AS average_transaction_value
    FROM people p
    LEFT JOIN transactions t ON p.user_id = t.user_id
    GROUP BY p.user_id, p.first_name, p.last_name, p.email
    ORDER BY total_spent DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)


def get_top_users_by_transfers(limit: int = 10):
    """
    Get top users by transfer volume.
    
    Args:
        limit (int): Maximum number of users to return
    
    Returns:
        list: Top users by transfer volume
    """
    query = """
    SELECT
        p.user_id,
        p.first_name,
        p.last_name,
        p.email,
        COALESCE(sent.total_sent, 0) AS total_sent,
        COALESCE(received.total_received, 0) AS total_received,
        COALESCE(sent.total_sent, 0) + COALESCE(received.total_received, 0) AS total_volume,
        COALESCE(sent.sent_count, 0) AS sent_count,
        COALESCE(received.received_count, 0) AS received_count,
        COALESCE(sent.sent_count, 0) + COALESCE(received.received_count, 0) AS total_transfers
    FROM people p
    LEFT JOIN (
        SELECT
            sender_id,
            SUM(amount) AS total_sent,
            COUNT(*) AS sent_count
        FROM transfers
        GROUP BY sender_id
    ) sent ON p.user_id = sent.sender_id
    LEFT JOIN (
        SELECT
            recipient_id,
            SUM(amount) AS total_received,
            COUNT(*) AS received_count
        FROM transfers
        GROUP BY recipient_id
    ) received ON p.user_id = received.recipient_id
    ORDER BY total_volume DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    
    return execute_query(query, params)


def get_popular_items_by_month(months: int = 12):
    """
    Get popular items by month.
    
    Args:
        months (int): Number of past months to include
    
    Returns:
        list: Popular items by month
    """
    query = """
    WITH month_series AS (
        SELECT generate_series(
            date_trunc('month', current_date - %(months)s::interval),
            date_trunc('month', current_date),
            '1 month'::interval
        )::date AS month
    )
    SELECT
        to_char(ms.month, 'YYYY-MM') AS month,
        COALESCE(item_summary.item, 'No Data') AS top_item,
        COALESCE(item_summary.items_sold, 0) AS items_sold,
        COALESCE(item_summary.total_revenue, 0) AS total_revenue
    FROM month_series ms
    LEFT JOIN LATERAL (
        SELECT
            item,
            SUM(quantity) AS items_sold,
            SUM(price) AS total_revenue
        FROM transactions
        WHERE DATE_TRUNC('month', timestamp) = ms.month
        GROUP BY item
        ORDER BY items_sold DESC
        LIMIT 1
    ) item_summary ON true
    ORDER BY ms.month
    """
    
    params = {'months': f'{months} months'}
    
    return execute_query(query, params)


def get_user_spending_distribution():
    """
    Get the distribution of user spending.
    
    Returns:
        list: Spending distribution data
    """
    query = """
    SELECT
        spending_range,
        COUNT(*) AS user_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM people), 2) AS percentage
    FROM (
        SELECT
            p.user_id,
            CASE
                WHEN COALESCE(SUM(t.price), 0) = 0 THEN '$0 (No purchases)'
                WHEN SUM(t.price) < 100 THEN '$0.01 - $99.99'
                WHEN SUM(t.price) < 500 THEN '$100 - $499.99'
                WHEN SUM(t.price) < 1000 THEN '$500 - $999.99'
                WHEN SUM(t.price) < 5000 THEN '$1,000 - $4,999.99'
                ELSE '$5,000+'
            END AS spending_range
        FROM people p
        LEFT JOIN transactions t ON p.user_id = t.user_id
        GROUP BY p.user_id
    ) AS spending_groups
    GROUP BY spending_range
    ORDER BY CASE
        WHEN spending_range = '$0 (No purchases)' THEN 0
        WHEN spending_range = '$0.01 - $99.99' THEN 1
        WHEN spending_range = '$100 - $499.99' THEN 2
        WHEN spending_range = '$500 - $999.99' THEN 3
        WHEN spending_range = '$1,000 - $4,999.99' THEN 4
        WHEN spending_range = '$5,000+' THEN 5
        ELSE 6
    END
    """
    
    return execute_query(query)


def get_geographic_spending_summary():
    """
    Get a summary of spending by geographic location.
    
    Returns:
        list: Geographic spending summary
    """
    query = """
    SELECT
        p.country,
        p.city,
        COUNT(DISTINCT p.user_id) AS user_count,
        COUNT(t.transaction_id) AS transaction_count,
        COALESCE(SUM(t.price), 0) AS total_spent,
        COALESCE(AVG(t.price), 0) AS average_transaction_value
    FROM people p
    LEFT JOIN transactions t ON p.user_id = t.user_id
    GROUP BY p.country, p.city
    ORDER BY total_spent DESC
    """
    
    return execute_query(query)


def get_transfer_amount_distribution():
    """
    Get the distribution of transfer amounts.
    
    Returns:
        list: Transfer amount distribution
    """
    query = """
    SELECT
        amount_range,
        COUNT(*) AS transfer_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transfers), 2) AS percentage,
        SUM(amount) AS total_amount
    FROM (
        SELECT
            transfer_id,
            amount,
            CASE
                WHEN amount < 10 THEN '$0.01 - $9.99'
                WHEN amount < 50 THEN '$10 - $49.99'
                WHEN amount < 100 THEN '$50 - $99.99'
                WHEN amount < 500 THEN '$100 - $499.99'
                WHEN amount < 1000 THEN '$500 - $999.99'
                ELSE '$1,000+'
            END AS amount_range
        FROM transfers
    ) AS amount_groups
    GROUP BY amount_range
    ORDER BY CASE
        WHEN amount_range = '$0.01 - $9.99' THEN 1
        WHEN amount_range = '$10 - $49.99' THEN 2
        WHEN amount_range = '$50 - $99.99' THEN 3
        WHEN amount_range = '$100 - $499.99' THEN 4
        WHEN amount_range = '$500 - $999.99' THEN 5
        WHEN amount_range = '$1,000+' THEN 6
        ELSE 7
    END
    """
    
    return execute_query(query)

def get_dashboard_totals():
    """
    Get comprehensive dashboard metrics
    
    Returns:
        dict: Expanded dashboard metrics
    """
    query = """
    WITH revenue_metrics AS  (
        SELECT 
            ROUND(SUM(total_revenue), 2) AS total_revenue,
            SUM(transaction_count) AS total_transactions,
            ROUND(AVG(average_price), 2) AS average_transaction_value,
            COUNT(DISTINCT item) AS unique_items_sold
        FROM item_summary
    ), 
    top_item AS (
        SELECT item, total_revenue, items_sold
        FROM item_summary
        ORDER BY total_revenue DESC
        LIMIT 1
    )
    SELECT 
        rm.total_revenue,
        rm.total_transactions,
        rm.average_transaction_value,
        rm.unique_items_sold,
        ti.item AS top_selling_item,
        ti.total_revenue AS top_item_revenue,
        ti.items_sold AS top_item_sales
    FROM revenue_metrics rm, top_item ti;
    """
    
    return execute_query(query)[0]

def get_top_items(limit: int = 5, order_by: str = 'revenue'):
    """
    Get top items by different metrics
    
    Args:
        limit (int): Number of top items to return
        order_by (str): Metric to order by ('revenue', 'sales', 'transactions')
    
    Returns:
        list: Top items
    """
    order_column = {
        'revenue': 'total_revenue',
        'sales': 'items_sold',
        'transactions': 'transaction_count'
    }.get(order_by, 'total_revenue')
    
    query = f"""
    SELECT 
        item,
        SUM(price) AS total_revenue,
        SUM(quantity) AS items_sold,
        COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY item
    ORDER BY {order_column} DESC
    LIMIT %(limit)s
    """
    
    params = {'limit': limit}
    return execute_query(query, params)
