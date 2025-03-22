"""
Controller for Analytics API endpoints.

This module provides functions for handling analytics-related API requests.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from flask import jsonify, request, abort

from src.api.queries import analytics_queries
from src.api.queries import transactions_queries

# Configure logging
logger = logging.getLogger(__name__)

def get_daily_transactions_summary():
    """
    Get a summary of daily transactions.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get days parameter
        days = min(int(request.args.get('days', 30)), 365)  # Default 30, max 365
        
        # Get daily transactions summary
        summary = analytics_queries.get_daily_transactions_summary(days)
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting daily transactions summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_daily_transfers_summary():
    """
    Get a summary of daily transfers.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get days parameter
        days = min(int(request.args.get('days', 30)), 365)  # Default 30, max 365
        
        # Get daily transfers summary
        summary = analytics_queries.get_daily_transfers_summary(days)
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting daily transfers summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_top_users_by_spending():
    """
    Get top users by spending.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get limit parameter
        limit = min(int(request.args.get('limit', 10)), 50)  # Default 10, max 50
        
        # Get top users by spending
        users = analytics_queries.get_top_users_by_spending(limit)
        
        return jsonify(users), 200
    
    except Exception as e:
        logger.error(f"Error getting top users by spending: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_top_users_by_transfers():
    """
    Get top users by transfer volume.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get limit parameter
        limit = min(int(request.args.get('limit', 10)), 50)  # Default 10, max 50
        
        # Get top users by transfers
        users = analytics_queries.get_top_users_by_transfers(limit)
        
        return jsonify(users), 200
    
    except Exception as e:
        logger.error(f"Error getting top users by transfers: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_popular_items_by_month():
    """
    Get popular items by month.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get months parameter
        months = min(int(request.args.get('months', 12)), 36)  # Default 12, max 36
        
        # Get popular items by month
        items = analytics_queries.get_popular_items_by_month(months)
        
        return jsonify(items), 200
    
    except Exception as e:
        logger.error(f"Error getting popular items by month: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_user_spending_distribution():
    """
    Get the distribution of user spending.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get user spending distribution
        distribution = analytics_queries.get_user_spending_distribution()
        
        return jsonify(distribution), 200
    
    except Exception as e:
        logger.error(f"Error getting user spending distribution: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_geographic_spending_summary():
    """
    Get a summary of spending by geographic location.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get geographic spending summary
        summary = analytics_queries.get_geographic_spending_summary()
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting geographic spending summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_transfer_amount_distribution():
    """
    Get the distribution of transfer amounts.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get transfer amount distribution
        distribution = analytics_queries.get_transfer_amount_distribution()
        
        return jsonify(distribution), 200
    
    except Exception as e:
        logger.error(f"Error getting transfer amount distribution: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_analytics_dashboard():
    """
    Get a comprehensive analytics dashboard with key metrics.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get various analytics data
        top_users_by_spending = analytics_queries.get_top_users_by_spending(5)
        top_users_by_transfers = analytics_queries.get_top_users_by_transfers(5)
        spending_distribution = analytics_queries.get_user_spending_distribution()
        transfer_distribution = analytics_queries.get_transfer_amount_distribution()
        daily_transactions = analytics_queries.get_daily_transactions_summary(30)
        daily_transfers = analytics_queries.get_daily_transfers_summary(30)
        
        # Compile dashboard data
        dashboard = {
            'top_users_by_spending': top_users_by_spending,
            'top_users_by_transfers': top_users_by_transfers,
            'spending_distribution': spending_distribution,
            'transfer_distribution': transfer_distribution,
            'daily_transactions': daily_transactions,
            'daily_transfers': daily_transfers
        }
        
        return jsonify(dashboard), 200
    
    except Exception as e:
        logger.error(f"Error getting analytics dashboard: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
def get_dashboard_totals():
    """
    API endpoint for comprehensive dashboard metrics
    
    Returns:
        JSON response with dashboard metrics
    """
    try:
        totals = analytics_queries.get_dashboard_totals()
        return jsonify(totals), 200
    except Exception as e:
        logger.error(f"Error getting dashboard totals: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def get_top_items():

    """
    API endpoint for top items
    
    Query parameters:
    - limit: Number of top items to return (default 5)
    - order_by: Metric to order by ('revenue', 'sales', 'transactions', default 'revenue')
    
    Returns:
        JSON response with top items
    """
    try:
        # Get query parameters with defaults
        limit = min(int(request.args.get('limit', 5)), 20)  # Limit to 20 max
        order_by = request.args.get('order_by', 'revenue')
        
        # Validate order_by parameter
        valid_order_by = ['revenue', 'sales', 'transactions']
        if order_by not in valid_order_by:
            order_by = 'revenue'
        
        # Get top items
        top_items = analytics_queries.get_top_items(limit, order_by)
        
        return jsonify(top_items), 200
    except Exception as e:
        logger.error(f"Error getting top items: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
def get_top_transactions():
    """
    Get top transactions by amount.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get limit parameter
        limit = min(int(request.args.get('limit', 5)), 100)  # Default 5, max 100
        
        # Get top transactions
        transactions = transactions_queries.get_top_transactions_by_amount(limit)
        
        return jsonify(transactions), 200
    
    except Exception as e:
        logger.error(f"Error getting top transactions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500