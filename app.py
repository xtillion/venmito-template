"""
Venmito Flask application entry point.

This module initializes the Flask application and registers API routes.
"""

import os
import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from src.api.routes import init_app as init_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_object=None):
    """
    Create and configure the Flask application.
    
    Args:
        config_object: Configuration object or module
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DEBUG=os.environ.get('FLASK_DEBUG', True),
        # Add any other configuration settings here
    )
    
    if config_object:
        app.config.from_object(config_object)
    
    # Enable CORS
    CORS(app)
    
    # Register API routes
    init_routes(app)
    
    # Register web view routes
    register_web_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    logger.info("Flask application initialized")
    return app


def register_web_routes(app):
    """
    Register web view routes for the Flask application.
    
    Args:
        app: Flask application instance
    """
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/users')
    def users():
        return render_template('users.html')
    
    @app.route('/transfers')
    def transfers():
        return render_template('transfers.html')
    
    @app.route('/transactions')
    def transactions():
        return render_template('transactions.html')
    
    @app.route('/analytics')
    def analytics():
        return render_template('analytics.html')
    
    logger.info("Web routes registered")


def register_error_handlers(app):
    """
    Register error handlers for the Flask application.
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An internal server error occurred'
        }), 500
    
    logger.info("Error handlers registered")


if __name__ == '__main__':
    # Create and run the application
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port)