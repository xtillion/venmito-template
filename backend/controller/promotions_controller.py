from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.promotions_service import PromotionsService
from backend.repository.promotions_repository import PromotionsRepository

promotions_blueprint = Blueprint('promotions', __name__, url_prefix='/api/promotions')


repository = PromotionsRepository(db_session)
service = PromotionsService(repository)

@promotions_blueprint.route("/", methods=['GET'])
def get_promotions_by_filter():
    filters = request.args.to_dict()  # Get query parameters as a dictionary
    promotions = service.get_promotions_by_filter(filters)
    if promotions:
        return jsonify([p.to_dict() for p in promotions]), 200
    return jsonify({"message": "No promotions found"}), 200

@promotions_blueprint.route('/<int:promotion_id>', methods=['GET'])
def get_promotions_by_id(promotion_id):
    promotions = service.get_promotions_by_id(promotion_id)
    if promotions:
        return jsonify(promotions.to_dict()), 200
    return jsonify({'error': 'Promotions with that id not found'}), 404
