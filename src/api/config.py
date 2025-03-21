"""
Configuration settings for Venmito application.

This module defines configuration classes for different environments.
"""

import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Config:
    """Base configuration."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    
    # Database settings
    DB_NAME = os.environ.get('DB_NAME', 'venmito')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    
    # API settings
    API_TITLE = 'Venmito API'
    API_VERSION = '1.0.0'
    
    # Pagination settings
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Logging settings
    LOG_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
    # Use a different database for testing
    DB_NAME = 'venmito_test'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # In production, secret key must be set as environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable not set")
    
    # Stricter secure settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    LOG_LEVEL = logging.WARNING


# Configuration dictionary for easy access
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Get the current configuration based on the environment.
    
    Returns:
        Config object for the current environment
    """
    env = os.environ.get('FLASK_ENV', 'default')
    return config_by_name[env]