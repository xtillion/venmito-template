from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend.db_config import Config
from backend.controller.item_insights_controller import item_insights_blueprint
from backend.controller.client_insights_controller import client_insights_blueprint
from backend.controller.people_controller import people_blueprint
from backend.controller.promotions_controller import promotions_blueprint
from backend.controller.transactions_controller import transactions_blueprint
from backend.controller.transfer_controller import transfers_blueprint

# Initialize SQLAlchemy without binding it to a Flask app yet
database = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r'/api/*': {
            'origins': 'http://localhost:3000',
            'methods': ['GET'],
            'allow_headers': ['Content-Type'],
        }
    })
    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    database.init_app(app)

    app.register_blueprint(people_blueprint, url_prefix='/api/people')
    app.register_blueprint(promotions_blueprint, url_prefix='/api/promotions')
    app.register_blueprint(transactions_blueprint, url_prefix='/api/transactions')
    app.register_blueprint(transfers_blueprint, url_prefix='/api/transfers')
    app.register_blueprint(item_insights_blueprint, url_prefix='/api/item_insights')
    app.register_blueprint(client_insights_blueprint, url_prefix='/api/client_insights')

    return app