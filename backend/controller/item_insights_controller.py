from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.item_insights_service import ItemInsightsService
from backend.repository.item_insights_repository import ItemInsightsRepository

item_insights_blueprint = Blueprint('item_insights', __name__, url_prefix='/api/item_insights')

repository = ItemInsightsRepository(db_session)
service = ItemInsightsService(repository)

@item_insights_blueprint.route('/top_selling_items', methods=['GET'])
def top_selling_items():
    filters = request.args.to_dict()

    items = service.get_top_selling_items(filters)
    if items:
        return jsonify(items), 200
    return jsonify({'message': 'No items found for given filters'}), 200

@item_insights_blueprint.route('/most_profitable_items', methods=['GET'])
def most_profitable_items():
    filters = request.args.to_dict()

    items = service.get_most_profitable_item(filters)
    if items:
        return jsonify(items), 200
    return jsonify({'message': 'No items found for given filters'}), 200

@item_insights_blueprint.route('/stores_with_most_sales', methods=['GET'])
def stores_with_most_sales():
    filters = request.args.to_dict()

    stores = service.get_stores_with_most_sales(filters)
    if stores:
        return jsonify(stores), 200
    return jsonify({'message': 'No stores found for given filters'}), 200

@item_insights_blueprint.route('/stores_with_most_revenue', methods=['GET'])
def stores_with_most_revenue():
    filters = request.args.to_dict()

    stores = service.get_stores_with_most_revenue(filters)
    if stores:
        return jsonify(stores), 200
    return jsonify({'message': 'No stores found for given filters'}), 200

@item_insights_blueprint.route('/most_promoted_items', methods=['GET'])
def most_promoted_items():
    filters = request.args.to_dict()

    items = service.get_most_promoted_items(filters)
    if items:
        return jsonify(items), 200
    return jsonify({'message': 'No items found for given filters'}), 200

@item_insights_blueprint.route('/top_selling_item_by_ages', methods=['GET'])
def top_selling_item_by_ages():

    result = service.get_top_selling_item_by_ages()

    return jsonify(result), 200