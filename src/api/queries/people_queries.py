"""
Database queries for people/users data.

This module provides functions for accessing and manipulating user data.
"""

import logging
from typing import Dict, Any, Optional, List

from src.db.config import execute_query

# Configure logging
logger = logging.getLogger(__name__)

def get_all_users(limit: int = 100, offset: int = 0, search: Optional[str] = None):
    """
    Get all users with optional pagination and search.
    
    Args:
        limit (int): Maximum number of users to return
        offset (int): Number of users to skip
        search (str, optional): Search term for user name or email
    
    Returns:
        list: List of user records
    """
    query = """
    SELECT user_id, first_name, last_name, email, city, country, devices, phone
    FROM people
    """
    
    params = {}
    
    if search:
        query += """
        WHERE first_name ILIKE %(search)s 
        OR last_name ILIKE %(search)s 
        OR email ILIKE %(search)s
        """
        params['search'] = f'%{search}%'
    
    query += """
    ORDER BY user_id
    LIMIT %(limit)s OFFSET %(offset)s
    """
    
    params.update({
        'limit': limit,
        'offset': offset
    })
    
    return execute_query(query, params)


def get_user_by_id(user_id: int):
    """
    Get a user by ID.
    
    Args:
        user_id (int): User ID
    
    Returns:
        dict: User record or None if not found
    """
    query = """
    SELECT user_id, first_name, last_name, email, city, country, devices, phone
    FROM people
    WHERE user_id = %(user_id)s
    """
    
    params = {'user_id': user_id}
    
    return execute_query(query, params, fetchall=False)


def get_users_count(search: Optional[str] = None):
    """
    Get the total number of users, optionally filtered by search.
    
    Args:
        search (str, optional): Search term for user name or email
    
    Returns:
        int: Total number of users
    """
    query = """
    SELECT COUNT(*) as count
    FROM people
    """
    
    params = {}
    
    if search:
        query += """
        WHERE first_name ILIKE %(search)s 
        OR last_name ILIKE %(search)s 
        OR email ILIKE %(search)s
        """
        params['search'] = f'%{search}%'
    
    result = execute_query(query, params, fetchall=False)
    return result['count'] if result else 0


def get_users_by_location(city: Optional[str] = None, country: Optional[str] = None,
                         limit: int = 100, offset: int = 0):
    """
    Get users filtered by location.
    
    Args:
        city (str, optional): City to filter by
        country (str, optional): Country to filter by
        limit (int): Maximum number of users to return
        offset (int): Number of users to skip
    
    Returns:
        list: List of user records
    """
    query = """
    SELECT user_id, first_name, last_name, email, city, country, devices, phone
    FROM people
    WHERE 1=1
    """
    
    params = {}
    
    if city:
        query += " AND city ILIKE %(city)s"
        params['city'] = f'%{city}%'
    
    if country:
        query += " AND country ILIKE %(country)s"
        params['country'] = f'%{country}%'
    
    query += """
    ORDER BY user_id
    LIMIT %(limit)s OFFSET %(offset)s
    """
    
    params.update({
        'limit': limit,
        'offset': offset
    })
    
    return execute_query(query, params)


def create_user(user_data: Dict[str, Any]):
    """
    Create a new user.
    
    Args:
        user_data (dict): User data to insert
    
    Returns:
        dict: Newly created user record
    """
    query = """
    INSERT INTO people (
        first_name, last_name, email, city, country, devices, phone
    ) VALUES (
        %(first_name)s, %(last_name)s, %(email)s, %(city)s, 
        %(country)s, %(devices)s, %(phone)s
    ) RETURNING user_id, first_name, last_name, email, city, country, devices, phone
    """
    
    return execute_query(query, user_data, fetchall=False)


def update_user(user_id: int, user_data: Dict[str, Any]):
    """
    Update an existing user.
    
    Args:
        user_id (int): User ID to update
        user_data (dict): User data to update
    
    Returns:
        dict: Updated user record
    """
    # Build dynamic update query based on provided fields
    fields = []
    params = {'user_id': user_id}
    
    for key, value in user_data.items():
        if key != 'user_id':  # Skip user_id
            fields.append(f"{key} = %({key})s")
            params[key] = value
    
    if not fields:
        logger.warning(f"No fields to update for user_id {user_id}")
        return get_user_by_id(user_id)
    
    query = f"""
    UPDATE people
    SET {", ".join(fields)}
    WHERE user_id = %(user_id)s
    RETURNING user_id, first_name, last_name, email, city, country, devices, phone
    """
    
    return execute_query(query, params, fetchall=False)


def delete_user(user_id: int):
    """
    Delete a user.
    
    Args:
        user_id (int): User ID to delete
    
    Returns:
        bool: True if user was deleted, False otherwise
    """
    query = """
    DELETE FROM people
    WHERE user_id = %(user_id)s
    RETURNING user_id
    """
    
    params = {'user_id': user_id}
    
    result = execute_query(query, params, fetchall=False)
    return result is not None