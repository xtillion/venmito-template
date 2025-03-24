from flask import Blueprint, jsonify, request

from backend.database import db_session
from backend.service.people_service import PeopleService
from backend.repository.people_repository import PeopleRepository

people_blueprint = Blueprint('people', __name__, url_prefix='/api/people')


repository = PeopleRepository(db_session)
service = PeopleService(repository)

@people_blueprint.route('/', methods=['GET'])
def get_people_by_filter():
    filters = request.args.to_dict()  # Get query parameters as a dictionary
    people = service.get_people_by_filter(filters)
    if people:
        return jsonify([p.to_dict() for p in people]), 200
    return jsonify({'message': 'No people found for given filters'}), 200

@people_blueprint.route('/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = service.get_people_by_id(people_id)
    if people:
        return jsonify(people.to_dict()), 200
    return jsonify({'error': 'No people found with that id'}), 404