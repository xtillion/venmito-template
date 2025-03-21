"""
Database queries for transfers data.

This module provides functions for accessing and manipulating transfers data.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.db.config import execute_query

# Configure logging
logger = logging.getLogger(__name__)

def get_all_transfers(limit: int = 100, offset: int = 0, 
                    user_id: Optional[int] = None,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None):
    """
    Get all transfers with optional filtering.
    
    Args:
        limit (int): Maximum number of transfers to return
        offset (int): Number of transfers to skip
        user_id (int, optional): Filter by user ID (sender or recipient)
        start_date (datetime, optional): Filter by start date
        end_date (datetime, optional): Filter by end date
    
    Returns:
        list: List of transfer records
    """
    query = """
    SELECT 
        t.transfer_id, 
        t.sender_id, 
        t.recipient_id, 
        t.amount, 
        t.timestamp,
        s.first_name as sender_first_name,
        s.last_name as sender_last_name,
        r.first_name as recipient_first_name,
        r.last_name as recipient_last_name
    FROM transfers t
    JOIN people s ON t.sender_id = s.user_id
    JOIN people r ON t.recipient_id = r.user_id
    WHERE 1=1
    """
    
    params = {}
    
    if user_id:
        query += " AND (t.sender_id = %(user_id)s OR t.recipient_id = %(user_id)s)"
        params['user_id'] = user_id
    
    if start_date:
        query += " AND t.timestamp >= %(start_date)s"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND t.timestamp <= %(end_date)s"
        params['end_date'] = end_date
    
    query += """
    ORDER BY t.timestamp DESC
    LIMIT %(limit)s OFFSET %(offset)s
    """
    
    params.update({
        'limit': limit,
        'offset': offset
    })
    
    return execute_query(query, params)


def get_transfer_by_id(transfer_id: int):
    """
    Get a transfer by ID.
    
    Args:
        transfer_id (int): Transfer ID
    
    Returns:
        dict: Transfer record or None if not found
    """
    query = """
    SELECT 
        t.transfer_id, 
        t.sender_id, 
        t.recipient_id, 
        t.amount, 
        t.timestamp,
        s.first_name as sender_first_name,
        s.last_name as sender_last_name,
        r.first_name as recipient_first_name,
        r.last_name as recipient_last_name
    FROM transfers t
    JOIN people s ON t.sender_id = s.user_id
    JOIN people r ON t.recipient_id = r.user_id
    WHERE t.transfer_id = %(transfer_id)s
    """
    
    params = {'transfer_id': transfer_id}
    
    return execute_query(query, params, fetchall=False)


def get_transfers_count(user_id: Optional[int] = None,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None):
    """
    Get the total number of transfers, optionally filtered.
    
    Args:
        user_id (int, optional): Filter by user ID (sender or recipient)
        start_date (datetime, optional): Filter by start date
        end_date (datetime, optional): Filter by end date
    
    Returns:
        int: Total number of transfers
    """
    query = """
    SELECT COUNT(*) as count
    FROM transfers t
    WHERE 1=1
    """
    
    params = {}
    
    if user_id:
        query += " AND (t.sender_id = %(user_id)s OR t.recipient_id = %(user_id)s)"
        params['user_id'] = user_id
    
    if start_date:
        query += " AND t.timestamp >= %(start_date)s"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND t.timestamp <= %(end_date)s"
        params['end_date'] = end_date
    
    result = execute_query(query, params, fetchall=False)
    return result['count'] if result else 0


def create_transfer(transfer_data: Dict[str, Any]):
    """
    Create a new transfer.
    
    Args:
        transfer_data (dict): Transfer data to insert
    
    Returns:
        dict: Newly created transfer record
    """
    query = """
    INSERT INTO transfers (
        sender_id, recipient_id, amount, timestamp
    ) VALUES (
        %(sender_id)s, %(recipient_id)s, %(amount)s, 
        %(timestamp)s
    ) RETURNING transfer_id, sender_id, recipient_id, amount, timestamp
    """
    
    # Set timestamp if not provided
    if 'timestamp' not in transfer_data:
        transfer_data['timestamp'] = datetime.now()
    
    return execute_query(query, transfer_data, fetchall=False)


def get_user_transfers_summary(user_id: int):
    """
    Get a summary of a user's transfers.
    
    Args:
        user_id (int): User ID
    
    Returns:
        dict: Summary of user's transfers
    """
    query = """
    SELECT
        %(user_id)s AS user_id,
        (SELECT COALESCE(SUM(amount), 0) FROM transfers WHERE sender_id = %(user_id)s) AS total_sent,
        (SELECT COALESCE(SUM(amount), 0) FROM transfers WHERE recipient_id = %(user_id)s) AS total_received,
        (SELECT COALESCE(SUM(amount), 0) FROM transfers WHERE recipient_id = %(user_id)s) - 
        (SELECT COALESCE(SUM(amount), 0) FROM transfers WHERE sender_id = %(user_id)s) AS net_transferred,
        (SELECT COUNT(*) FROM transfers WHERE sender_id = %(user_id)s) AS sent_count,
        (SELECT COUNT(*) FROM transfers WHERE recipient_id = %(user_id)s) AS received_count,
        (SELECT COUNT(*) FROM transfers WHERE sender_id = %(user_id)s OR recipient_id = %(user_id)s) AS transfer_count
    """
    
    params = {'user_id': user_id}
    
    return execute_query(query, params, fetchall=False)


def get_user_most_frequent_contacts(user_id: int, limit: int = 5):
    """
    Get a user's most frequent transfer contacts.
    
    Args:
        user_id (int): User ID
        limit (int): Maximum number of contacts to return
    
    Returns:
        list: List of most frequent contacts
    """
    query = """
    SELECT 
        counterparty_id,
        first_name,
        last_name,
        transfer_count,
        total_amount
    FROM (
        -- Sent transfers
        SELECT 
            recipient_id AS counterparty_id,
            COUNT(*) AS transfer_count,
            SUM(amount) AS total_amount
        FROM transfers
        WHERE sender_id = %(user_id)s
        GROUP BY recipient_id
        
        UNION ALL
        
        -- Received transfers
        SELECT 
            sender_id AS counterparty_id,
            COUNT(*) AS transfer_count,
            SUM(amount) AS total_amount
        FROM transfers
        WHERE recipient_id = %(user_id)s
        GROUP BY sender_id
    ) AS combined
    JOIN people ON people.user_id = combined.counterparty_id
    GROUP BY counterparty_id, first_name, last_name, transfer_count, total_amount
    ORDER BY transfer_count DESC, total_amount DESC
    LIMIT %(limit)s
    """
    
    params = {
        'user_id': user_id,
        'limit': limit
    }
    
    return execute_query(query, params)