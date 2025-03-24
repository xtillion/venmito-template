from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.client_insights_service import ClientInsightsService
from backend.repository.client_insights_repository import ClientInsightsRepository

client_insights_blueprint = Blueprint('client_insights', __name__, url_prefix='/api/client_insights')

repository = ClientInsightsRepository(db_session)
service = ClientInsightsService(repository)

@client_insights_blueprint.route('/most_recurring_clients', methods=['GET'])
def most_recurring_clients():
    filters = request.args.to_dict()

    clients = service.get_most_recurring_clients(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No clients found for given filters'}), 200

@client_insights_blueprint.route('/clients_with_most_purchases', methods=['GET'])
def clients_with_most_purchases():
    filters = request.args.to_dict()

    clients = service.get_clients_with_most_purchases(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No clients found for given filters'}), 200

@client_insights_blueprint.route('/clients_with_most_transferred_funds', methods=['GET'])
def clients_with_most_transferred_funds():
    filters = request.args.to_dict()

    clients = service.get_clients_with_most_transferred_funds(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No clients found for given filters'}), 200

@client_insights_blueprint.route('/clients_with_most_received_funds', methods=['GET'])
def clients_with_most_received_funds():
    filters = request.args.to_dict()

    clients = service.get_clients_with_most_received_funds(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No clients found for given filters'}), 200

@client_insights_blueprint.route('/cities_with_most_clients', methods=['GET'])
def cities_with_most_clients():
    filters = request.args.to_dict()

    clients = service.get_cities_with_most_clients(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No cities found for given filters'}), 200

@client_insights_blueprint.route('/countries_with_most_users', methods=['GET'])
def countries_with_most_users():
    filters = request.args.to_dict()

    clients = service.get_countries_with_most_users(filters)
    if clients:
        return jsonify(clients), 200
    return jsonify({'message': 'No cities found for given filters'}), 200