from flask import jsonify, request
from sqlalchemy import text

def register_clients_endpoints(app, engine):
    @app.route('/clients/promotions', methods=['GET'])
    def get_clients_promotions():
        try:
            with engine.connect() as connection:
                query = text("""
                    SELECT p.email, pr.promotion
                    FROM person p
                    JOIN promotion pr ON p.email = pr.client_email
                """)
                result = connection.execute(query)
                promotions = [{'email': row[0], 'promotion': row[1]} for row in result]
                return jsonify(promotions)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

