from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.transfers_service import TransfersService
from backend.repository.transfers_repository import TransfersRepository

transfers_blueprint = Blueprint('transfers', __name__, url_prefix='/api/transfers')


repository = TransfersRepository(db_session)
service = TransfersService(repository)

@transfers_blueprint.route("/", methods=['GET'])
def get_transfers_by_filter():
    filters = request.args.to_dict()
    transfers = service.get_transfers_by_filter(filters)
    if transfers:
        return jsonify([t.to_dict() for t in transfers]), 200
    return jsonify({"message": "No transfers found"}), 200

@transfers_blueprint.route('/<int:transfer_id>', methods=['GET'])
def get_transfers_by_id(transfer_id):
    transfers = service.get_transfers_by_id(transfer_id)
    if transfers:
        return jsonify(transfers.to_dict()), 200
    return jsonify({'error': 'Transfers with that id not found'}), 404
