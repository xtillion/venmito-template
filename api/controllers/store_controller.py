from flask import Blueprint, jsonify
from etl_pipeline.aggregators.people_transactions_aggregator import PeopleTransactionsAggregator

store_controller = Blueprint('store_controller', __name__)
people_transactions_aggregator = PeopleTransactionsAggregator()

@store_controller.route('stores/<name>/people', methods=['GET'])
def get_people_by_store(name):
    data = people_transactions_aggregator.get_people_by_store(name)
    return jsonify(data)