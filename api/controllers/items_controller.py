from flask import Blueprint, jsonify
from etl_pipeline.aggregators.transactions_aggregator import TransactionsAggregator
from etl_pipeline.aggregators.people_transactions_aggregator import PeopleTransactionsAggregator


items_controller = Blueprint('items_controller', __name__)
transactions_aggregator = TransactionsAggregator()
people_transaction_aggregator = PeopleTransactionsAggregator()

@items_controller.route('items/<name>/transactions', methods=['GET'])
def get_transactions_by_item_name(name):
    data = transactions_aggregator.get_transactions_by_item_name(name)
    return jsonify(data)

@items_controller.route('items/<name>/people/transactions', methods=['GET'])
def get_buyers_by_item_name(name):
    data = people_transaction_aggregator.get_people_with_transaction_by_item_name(name)
    return jsonify(data)