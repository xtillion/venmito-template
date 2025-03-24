from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.transactions_service import TransactionsService
from backend.repository.transactions_repository import TransactionsRepository

transactions_blueprint = Blueprint('transactions', __name__, url_prefix='/api/transactions')


repository = TransactionsRepository(db_session)
service = TransactionsService(repository)

@transactions_blueprint.route("/", methods=['GET'])
def get_transactions_by_filter():
    filters = request.args.to_dict()
    transactions = service.get_transactions_by_filter(filters)
    if transactions:
        return jsonify([t.to_dict() for t in transactions]), 200
    return jsonify({"message": "No transactions found"}), 200

@transactions_blueprint.route('/<int:transact_id>', methods=['GET'])
def get_transactions_by_id(transact_id):
    transactions = service.get_transactions_by_id(transact_id)
    if transactions:
        return jsonify(transactions.to_dict()), 200
    return jsonify({'error': 'Transactions with that id not found'}), 404
