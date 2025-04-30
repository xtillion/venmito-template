"""
API routes for Venmito project.

This module defines the API routes for the Venmito application.
"""

import logging
from flask import Blueprint, jsonify

from src.api.controllers import (
    people_controller,
    transfers_controller,
    transactions_controller,
    analytics_controller
)

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprints for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')
people_bp = Blueprint('people', __name__, url_prefix='/people')
transfers_bp = Blueprint('transfers', __name__, url_prefix='/transfers')
transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


# Register routes for people
@people_bp.route('/', methods=['GET'])
def get_users():
    return people_controller.get_users()

@people_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return people_controller.get_user(user_id)

@people_bp.route('/', methods=['POST'])
def create_user():
    return people_controller.create_user()

@people_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return people_controller.update_user(user_id)

@people_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return people_controller.delete_user(user_id)


# Register routes for transfers
@transfers_bp.route('/', methods=['GET'])
def get_transfers():
    return transfers_controller.get_transfers()

@transfers_bp.route('/<int:transfer_id>', methods=['GET'])
def get_transfer(transfer_id):
    return transfers_controller.get_transfer(transfer_id)

@transfers_bp.route('/', methods=['POST'])
def create_transfer():
    return transfers_controller.create_transfer()

@transfers_bp.route('/user/<int:user_id>/summary', methods=['GET'])
def get_user_transfers_summary(user_id):
    return transfers_controller.get_user_transfers_summary(user_id)

@transfers_bp.route('/user/<int:user_id>/contacts', methods=['GET'])
def get_user_frequent_contacts(user_id):
    return transfers_controller.get_user_frequent_contacts(user_id)


# Register routes for transactions
@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    return transactions_controller.get_transactions()

@transactions_bp.route('/<string:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    return transactions_controller.get_transaction(transaction_id)

@transactions_bp.route('/<string:transaction_id>/items', methods=['GET'])
def get_transaction_items(transaction_id):
    return transactions_controller.get_transaction_items(transaction_id)

@transactions_bp.route('/user/<int:user_id>/summary', methods=['GET'])
def get_user_transactions_summary(user_id):
    return transactions_controller.get_user_transactions_summary(user_id)

@transactions_bp.route('/items/summary', methods=['GET'])
def get_item_summary():
    return transactions_controller.get_item_summary()

@transactions_bp.route('/stores/summary', methods=['GET'])
def get_store_summary():
    return transactions_controller.get_store_summary()


# Register routes for analytics
@analytics_bp.route('/transactions/daily', methods=['GET'])
def get_daily_transactions_summary():
    return analytics_controller.get_daily_transactions_summary()

@analytics_bp.route('/transfers/daily', methods=['GET'])
def get_daily_transfers_summary():
    return analytics_controller.get_daily_transfers_summary()

@analytics_bp.route('/users/top-spending', methods=['GET'])
def get_top_users_by_spending():
    return analytics_controller.get_top_users_by_spending()

@analytics_bp.route('/users/top-transfers', methods=['GET'])
def get_top_users_by_transfers():
    return analytics_controller.get_top_users_by_transfers()

@analytics_bp.route('/items/monthly-popular', methods=['GET'])
def get_popular_items_by_month():
    return analytics_controller.get_popular_items_by_month()

@analytics_bp.route('/users/spending-distribution', methods=['GET'])
def get_user_spending_distribution():
    return analytics_controller.get_user_spending_distribution()

@analytics_bp.route('/geographic/spending', methods=['GET'])
def get_geographic_spending_summary():
    return analytics_controller.get_geographic_spending_summary()

@analytics_bp.route('/transfers/amount-distribution', methods=['GET'])
def get_transfer_amount_distribution():
    return analytics_controller.get_transfer_amount_distribution()

@analytics_bp.route('/dashboard', methods=['GET'])
def get_analytics_dashboard():
    return analytics_controller.get_analytics_dashboard()

@analytics_bp.route('/top-transactions', methods=['GET'])
def top_transactions():
    return analytics_controller.get_top_transactions()

@analytics_bp.route('/dashboard-totals', methods=['GET'])
def dashboard_totals():
    return analytics_controller.get_dashboard_totals()

@analytics_bp.route('/top-items', methods=['GET'])
def top_items():
    return analytics_controller.get_top_items()

# API root endpoint
@api_bp.route('/', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Venmito API',
        'version': '1.0.0',
        'endpoints': {
            'people': '/api/people',
            'transfers': '/api/transfers',
            'transactions': '/api/transactions',
            'analytics': '/api/analytics'
        }
    })


# Register all blueprints with the api blueprint
api_bp.register_blueprint(people_bp)
api_bp.register_blueprint(transfers_bp)
api_bp.register_blueprint(transactions_bp)
api_bp.register_blueprint(analytics_bp)


def init_app(app):
    """
    Initialize the API routes with the Flask app.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(api_bp)
    logger.info("API routes registered")
    #debug info
    endpoints = [str(rule) for rule in app.url_map.iter_rules() 
                if str(rule).startswith('/api')]
    logger.info(f"Available API endpoints: {endpoints}")
