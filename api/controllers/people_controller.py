from flask import Blueprint, jsonify
from etl_pipeline.aggregators.people_promotions_aggregator import PeoplePromotionsAggregator
from etl_pipeline.aggregators.people_transactions_aggregator import PeopleTransactionsAggregator
from etl_pipeline.aggregators.people_transfers_aggregator import PeopleTransfersAggregator
from etl_pipeline.analyzers.promotion_suggestion_analyzer import PromotionSuggestionAnalyzer

people_controller = Blueprint('people_controller', __name__)
people_promotion_aggregator = PeoplePromotionsAggregator()
people_transactions_aggregator = PeopleTransactionsAggregator()
people_transfers_aggregator = PeopleTransfersAggregator()
promotion_suggestion_analyzer = PromotionSuggestionAnalyzer()

@people_controller.route('/people/<id>/promotions', methods=['GET'])
def get_promotions_by_people(id):
    data = people_promotion_aggregator.get_promotions_by_person(id)
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/promotions', methods=['GET'])
def get_people_with_promotions():
    data = people_promotion_aggregator.get_people_with_promotions()
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/transactions', methods=['GET'])
def get_people_with_transactions():
    data = people_transactions_aggregator.get_people_with_transactions()
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/transfers', methods=['GET'])
def get_people_with_transfers():
    data = people_transfers_aggregator.get_people_with_transfers()
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/promotions/<promotion>', methods=['GET'])
def get_people_with_specified_promotion(promotion):
    data = people_promotion_aggregator.get_people_with_specified_promotion_role(promotion)
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/promotions/accepted-promotions', methods=['GET'])
def get_people_with_accepted_promotion():
    data = people_promotion_aggregator.get_people_with_accepted_promotions()
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/promotions/denied-promotions', methods=['GET'])
def get_people_with_denied_promotion():
    data = people_promotion_aggregator.get_people_with_denied_promotions()
    return jsonify(data.to_dict(orient='records'))

@people_controller.route('/people/promotions/improvement-suggestions', methods=['GET'])
def get_improvement_suggestions_for_declined_promotions():
    suggestions = promotion_suggestion_analyzer.suggest_improvements()
    return jsonify(suggestions)

@people_controller.route('/people/promotions/<promotion>/improvement-suggestions', methods=['GET'])
def get_improvement_suggestions_for_declined_promotions_by_name(promotion):
    suggestions = promotion_suggestion_analyzer.suggest_improvements(promotion)
    return jsonify(suggestions)