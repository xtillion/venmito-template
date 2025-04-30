"""
Controller for Transactions API endpoints.

This module provides functions for handling transaction-related API requests.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from flask import jsonify, request, abort

from src.api.queries import transactions_queries
from src.api.queries import people_queries

# Configure logging
logger = logging.getLogger(__name__)

def get_transactions():
    """
    Get all transactions with pagination and optional filtering.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Max 100
        user_id = request.args.get('user_id')
        item = request.args.get('item')
        store = request.args.get('store')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        # Parse numeric parameters
        parsed_user_id = None
        parsed_min_price = None
        parsed_max_price = None
        
        if user_id:
            try:
                parsed_user_id = int(user_id)
            except ValueError:
                return jsonify({'error': 'Invalid user_id format. Must be an integer'}), 400
        
        if min_price:
            try:
                parsed_min_price = float(min_price)
            except ValueError:
                return jsonify({'error': 'Invalid min_price format. Must be a number'}), 400
        
        if max_price:
            try:
                parsed_max_price = float(max_price)
            except ValueError:
                return jsonify({'error': 'Invalid max_price format. Must be a number'}), 400
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get transactions data
        transactions = transactions_queries.get_all_transactions(
            limit=per_page,
            offset=offset,
            user_id=parsed_user_id,
            item=item,
            store=store,
            min_price=parsed_min_price,
            max_price=parsed_max_price
        )
        
        # Get total count
        total = transactions_queries.get_transactions_count(
            user_id=parsed_user_id,
            item=item,
            store=store,
            min_price=parsed_min_price,
            max_price=parsed_max_price
        )
        
        # Calculate pagination info
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        response = {
            'data': transactions,
            'pagination': {
                'total': total,
                'per_page': per_page,
                'current_page': page,
                'total_pages': total_pages
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error getting transactions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_transaction(transaction_id: str):
    """
    Get a transaction by ID.
    
    Args:
        transaction_id (str): Transaction ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        transaction = transactions_queries.get_transaction_by_id(transaction_id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify(transaction), 200
    
    except Exception as e:
        logger.error(f"Error getting transaction {transaction_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def get_transaction_items(transaction_id: str):
    """
    Get items for a specific transaction.
    
    Args:
        transaction_id (str): Transaction ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        items = transactions_queries.get_transaction_items_by_id(transaction_id)
        
        if not items:
            return jsonify([]), 200  # Return empty array, not 404
        
        return jsonify(items), 200
    
    except Exception as e:
        logger.error(f"Error getting items for transaction {transaction_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


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
    
def get_user_transactions_summary(user_id: int):
    """
    Get a summary of a user's transactions.
    
    Args:
        user_id (int): User ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Check if user exists
        user = people_queries.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get transaction summary
        summary = transactions_queries.get_user_transactions_summary(user_id)
        
        # If user has no transactions, return empty summary
        if not summary:
            summary = {
                'user_id': user_id,
                'total_spent': 0,
                'transaction_count': 0,
                'favorite_store': None,
                'favorite_item': None
            }
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting transaction summary for user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_item_summary():
    """
    Get a summary of items sold.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get limit parameter
        limit = min(int(request.args.get('limit', 20)), 100)  # Default 20, max 100
        
        # Get item summary
        summary = transactions_queries.get_item_summary(limit)
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting item summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_store_summary():
    """
    Get a summary of stores.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get limit parameter
        limit = min(int(request.args.get('limit', 20)), 100)  # Default 20, max 100
        
        # Get store summary
        summary = transactions_queries.get_store_summary(limit)
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting store summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500