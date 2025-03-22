"""
Controller for People/Users API endpoints.

This module provides functions for handling user-related API requests.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from flask import jsonify, request, abort

from src.api.queries import people_queries

# Configure logging
logger = logging.getLogger(__name__)

def get_users():
    """
    Get all users with pagination and optional filtering.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Max 100
        search = request.args.get('search')
        city = request.args.get('city')
        country = request.args.get('country')
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get users data
        if city or country:
            users = people_queries.get_users_by_location(
                city=city, 
                country=country, 
                limit=per_page, 
                offset=offset
            )
            total = len(users)  # Simplification - could need a separate count query
        else:
            users = people_queries.get_all_users(
                limit=per_page, 
                offset=offset, 
                search=search
            )
            total = people_queries.get_users_count(search=search)
        
        # Calculate pagination info
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        response = {
            'data': users,
            'pagination': {
                'total': total,
                'per_page': per_page,
                'current_page': page,
                'total_pages': total_pages
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def get_user(user_id: int):
    """
    Get a user by ID.
    
    Args:
        user_id (int): User ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        user = people_queries.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user), 200
    
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def create_user():
    """
    Create a new user.
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Get request data
        user_data = request.get_json()
        
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in user_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create user
        user = people_queries.create_user(user_data)
        
        return jsonify(user), 201
    
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def update_user(user_id: int):
    """
    Update an existing user.
    
    Args:
        user_id (int): User ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Check if user exists
        existing_user = people_queries.get_user_by_id(user_id)
        if not existing_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get request data
        user_data = request.get_json()
        
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update user
        updated_user = people_queries.update_user(user_id, user_data)
        
        return jsonify(updated_user), 200
    
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def delete_user(user_id: int):
    """
    Delete a user.
    
    Args:
        user_id (int): User ID
    
    Returns:
        tuple: (JSON response, status code)
    """
    try:
        # Check if user exists
        existing_user = people_queries.get_user_by_id(user_id)
        if not existing_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete user
        success = people_queries.delete_user(user_id)
        
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
    
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500