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

    @app.route('/clients/search', methods=['GET'])
    def search_clients():
        try:
            query_params = request.args
            conditions = []
            parameters = {}

            for key in ['id', 'first_name', 'last_name', 'telephone', 'email', 'android', 'desktop', 'iphone', 'city', 'country']:
                if key in query_params:
                    conditions.append(f"{key} = :{key}")
                    parameters[key] = query_params[key]

            if not conditions:
                return jsonify({'error': 'At least one search parameter is required'}), 400

            with engine.connect() as connection:
                query = f"SELECT * FROM person WHERE {' AND '.join(conditions)}"
                result = connection.execute(text(query), parameters)
                clients = [dict(row) for row in result]
                return jsonify(clients)
        except Exception as e:
            return jsonify({'error': str(e)}), 500 
        
    @app.route('/clients/count', methods=['GET'])
    def count_clients():
        return count_records('person', ['id', 'first_name', 'last_name', 'telephone', 'email', 'android', 'desktop', 'iphone', 'city', 'country'])

    def count_records(table_name, valid_keys):
        try:
            query_params = request.args
            query = f"SELECT COUNT(*) FROM {table_name} WHERE "
            conditions = []
            parameters = {}

            for key, value in query_params.items():
                if key in valid_keys:
                    conditions.append(f"{key} = :{key}")
                    parameters[key] = value

            if conditions:
                query += " AND ".join(conditions)
            else:
                query = f"SELECT COUNT(*) FROM {table_name}"

            with engine.connect() as connection:
                result = connection.execute(text(query), parameters)
                count = result.scalar()
                return jsonify({'count': count})
        except Exception as e:
            return jsonify({'error': str(e)}), 500