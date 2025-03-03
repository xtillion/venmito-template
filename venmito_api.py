from flask import Flask, jsonify, request
from sqlalchemy import text
from models.database import get_engine
import argparse
from endpoints.clients import register_clients_endpoints
from endpoints.promotions import register_promotions_endpoints
from endpoints.transfers import register_transfers_endpoints
from endpoints.items import register_items_endpoints
from endpoints.stores import register_stores_endpoints

app = Flask(__name__)

def create_app():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Flask API for Venmito")
    parser.add_argument('--user', type=str, required=True, help='Database username')
    parser.add_argument('--password', type=str, required=True, help='Database password')
    parser.add_argument('--host', type=str, default='localhost', help='Database host')
    parser.add_argument('--port', type=str, default='5432', help='Database port')
    parser.add_argument('--db', type=str, required=True, help='Database name')
    args = parser.parse_args()

    # Initialize database connection
    engine = get_engine(args.user, args.password, args.host, args.port, args.db)

    # Register endpoints
    register_clients_endpoints(app, engine)
    register_promotions_endpoints(app, engine)
    register_transfers_endpoints(app, engine)
    register_items_endpoints(app, engine)
    register_stores_endpoints(app, engine)
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)