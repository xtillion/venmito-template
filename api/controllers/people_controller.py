from flask import Blueprint, jsonify
from etl_pipeline.transform.transform_people import People

people_controller = Blueprint('people_controller', __name__)
people = People('data/people.json', 'data/people.yml')

@people_controller.route('/people', methods=['GET'])
def get_all_people():
    return jsonify(people.data.to_dict(orient='records'))