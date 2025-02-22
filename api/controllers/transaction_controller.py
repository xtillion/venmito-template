from flask import Blueprint, jsonify
from etl_pipeline.transform.transform_transactions import Transaction

transaction_controller = Blueprint('transaction_controller', __name__)
transactions = Transaction('data/transactions.xml')

@transaction_controller.route('/transactions', methods=['GET'])
def get_all_transactions():
    return jsonify(transactions.data.to_dict(orient='records'))
