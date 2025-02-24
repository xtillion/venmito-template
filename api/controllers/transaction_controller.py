from flask import Blueprint, jsonify
from etl_pipeline.aggregators.transactions_aggregator import TransactionsAggregator

transaction_controller = Blueprint('transaction_controller', __name__)
transactions = TransactionsAggregator()

@transaction_controller.route('/transactions', methods=['GET'])
def get_all_transactions():
    data = transactions.get_all_transactions()
    return jsonify(data.to_dict(orient='records'))

@transaction_controller.route('/transactions/best-selling-item', methods=['GET'])
def get_best_selling_item():
    data = transactions.get_best_selling_item()
    return jsonify(data)

@transaction_controller.route('/transactions/best-selling-store', methods=['GET'])
def get_store_with_most_items_sold():
    data = transactions.get_store_with_most_items_sold()
    return jsonify(data)

@transaction_controller.route('/transactions/most-profitable-store', methods=['GET'])
def get_most_profitable_store():
    data = transactions.get_most_profitable_store()
    return jsonify(data)

@transaction_controller.route('/transactions/profitability-of-items', methods=['GET'])
def get_profitability_of_items():
    data = transactions.get_profitability_of_items()
    return jsonify(data)

@transaction_controller.route('/transactions/items-sold-by-store', methods=['GET'])
def get_items_sold_by_store():
    data = transactions.get_items_sold_by_store()
    return jsonify(data)