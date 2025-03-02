from flask import jsonify, request
from sqlalchemy import text

def register_transactions_endpoints(app, engine):
    @app.route('/transactions/search', methods=['GET'])
    def search_transactions():
        return search_records('transaction', ['id', 'phone', 'store'])

    @app.route('/transactions/count', methods=['GET'])
    def count_transactions():
        return count_records('transaction', ['id', 'phone', 'store'])

    # Add any additional transactions-related endpoints here

def search_records(table_name, valid_keys):
    try:
        query_params = request.args
        query = f"SELECT * FROM {table_name} WHERE "
        conditions = []
        parameters = {}

        for key, value in query_params.items():
            if key in valid_keys:
                conditions.append(f"{key} = :{key}")
                parameters[key] = value

        if conditions:
            query += " AND ".join(conditions)
        else:
            return jsonify({'error': 'No valid query parameters provided'}), 400

        with engine.connect() as connection:
            result = connection.execute(text(query), parameters)
            records = [dict(row) for row in result.mappings()]
            return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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