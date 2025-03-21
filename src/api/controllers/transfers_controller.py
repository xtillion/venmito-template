"""
Controller for Transfers API endpoints.

This module provides functions for handling transfer-related API requests.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from flask import jsonify, request, abort

from src.api.queries import transfers_queries
from src.api.queries import people_queries

# Configure logging
logger = logging.getLogger(__name__)

def get_transfers():
    """
    Get all transfers with pagination and optional filtering.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Max 100
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Parse dates if provided
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        # Convert user_id to int if provided
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = int(user_id)
            except ValueError:
                return jsonify({'error': 'Invalid user_id format. Must be an integer'}), 400
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get transfers data
        transfers = transfers_queries.get_all_transfers(
            limit=per_page,
            offset=offset,
            user_id=parsed_user_id,
            start_date=parsed_start_date,
            end_date=parsed_end_date
        )
        
        # Get total count
        total = transfers_queries.get_transfers_count(
            user_id=parsed_user_id,
            start_date=parsed_start_date,
            end_date=parsed_end_date
        )
        
        # Calculate pagination info
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        response = {
            'data': transfers,
            'pagination': {
                'total': total,
                'per_page': per_page,
                'current_page': page,
                'total_pages': total_pages
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error getting transfers: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_transfer(transfer_id: int):
    """
    Get a transfer by ID.
    
    Args:
        transfer_id (int): Transfer ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        transfer = transfers_queries.get_transfer_by_id(transfer_id)
        
        if not transfer:
            return jsonify({'error': 'Transfer not found'}), 404
        
        return jsonify(transfer), 200
    
    except Exception as e:
        logger.error(f"Error getting transfer {transfer_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def create_transfer():
    """
    Create a new transfer.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get request data
        transfer_data = request.get_json()
        
        if not transfer_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['sender_id', 'recipient_id', 'amount']
        for field in required_fields:
            if field not in transfer_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate sender and recipient exist
        sender = people_queries.get_user_by_id(transfer_data['sender_id'])
        if not sender:
            return jsonify({'error': 'Sender not found'}), 404
        
        recipient = people_queries.get_user_by_id(transfer_data['recipient_id'])
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        
        # Validate sender and recipient are different
        if transfer_data['sender_id'] == transfer_data['recipient_id']:
            return jsonify({'error': 'Sender and recipient must be different'}), 400
        
        # Validate amount is positive
        try:
            amount = float(transfer_data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be positive'}), 400
            
            # Update amount in transfer_data (in case it was a string)
            transfer_data['amount'] = amount
        except ValueError:
            return jsonify({'error': 'Invalid amount format'}), 400
        
        # Create transfer
        transfer = transfers_queries.create_transfer(transfer_data)
        
        return jsonify(transfer), 201
    
    except Exception as e:
        logger.error(f"Error creating transfer: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_user_transfers_summary(user_id: int):
    """
    Get a summary of a user's transfers.
    
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
        
        # Get transfer summary
        summary = transfers_queries.get_user_transfers_summary(user_id)
        
        return jsonify(summary), 200
    
    except Exception as e:
        logger.error(f"Error getting transfer summary for user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_user_frequent_contacts(user_id: int):
    """
    Get a user's most frequent transfer contacts.
    
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
        
        # Get limit parameter
        limit = min(int(request.args.get('limit', 5)), 20)  # Default 5, max 20
        
        # Get frequent contacts
        contacts = transfers_queries.get_user_most_frequent_contacts(user_id, limit)
        
        return jsonify(contacts), 200
    
    except Exception as e:
        logger.error(f"Error getting frequent contacts for user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500