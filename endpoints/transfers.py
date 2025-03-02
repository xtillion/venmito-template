from flask import jsonify, request
from sqlalchemy import text

def register_transfers_endpoints(app, engine):
    @app.route('/transfers/search', methods=['GET'])
    def search_transfers():
        return search_records('transfer', ['id', 'sender_id', 'recipient_id', 'amount', 'date'])

    @app.route('/transfers/count', methods=['GET'])
    def count_transfers():
        return count_records('transfer', ['id', 'sender_id', 'recipient_id', 'amount', 'date'])

    @app.route('/transfers/aggregation', methods=['GET'])
    def aggregate_transfers():
        return aggregate_records('transfer', 'amount')

    @app.route('/transfers/total', methods=['GET'])
    def total_transfers():
        try:
            with engine.connect() as connection:
                query = text("SELECT SUM(amount) as total FROM transfer")
                result = connection.execute(query).scalar()
                return jsonify({'total_transfers': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/max_min', methods=['GET'])
    def person_max_min_transferred():
        try:
            with engine.connect() as connection:
                max_transferred_query = text("""
                    SELECT p.*, SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    GROUP BY p.id
                    ORDER BY total_transferred DESC
                    LIMIT 1
                """)
                max_transferred_result = connection.execute(max_transferred_query).fetchone()

                min_transferred_query = text("""
                    SELECT p.*, SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    GROUP BY p.id
                    ORDER BY total_transferred ASC
                    LIMIT 1
                """)
                min_transferred_result = connection.execute(min_transferred_query).fetchone()

                response = {
                    'max_transferred': {
                        'person': dict(max_transferred_result) if max_transferred_result else None,
                        'total_transferred': max_transferred_result['total_transferred'] if max_transferred_result else None
                    },
                    'min_transferred': {
                        'person': dict(min_transferred_result) if min_transferred_result else None,
                        'total_transferred': min_transferred_result['total_transferred'] if min_transferred_result else None
                    }
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/list', methods=['GET'])
    def list_person_transferred():
        try:
            with engine.connect() as connection:
                query = text("""
                    SELECT p.*, SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    GROUP BY p.id
                    ORDER BY total_transferred DESC
                """)
                result = connection.execute(query).mappings()
                response = [{'person': dict(row), 'total_transferred': row['total_transferred']} for row in result]

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/amount/search', methods=['GET'])
    def search_person_transfers():
        try:
            query_params = request.args
            conditions = []
            parameters = {}

            for key in ['id', 'first_name', 'last_name', 'telephone', 'email', 'city', 'country']:
                if key in query_params:
                    conditions.append(f"p.{key} = :{key}")
                    parameters[key] = query_params[key]

            with engine.connect() as connection:
                query = """
                    SELECT p.*, 
                           COALESCE(SUM(t_send.amount), 0) as total_transferred,
                           COALESCE(SUM(t_receive.amount), 0) as total_received
                    FROM person p
                    LEFT JOIN transfer t_send ON t_send.sender_id = p.id
                    LEFT JOIN transfer t_receive ON t_receive.recipient_id = p.id
                """

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                query += " GROUP BY p.id ORDER BY total_transferred DESC"

                result = connection.execute(text(query), parameters).mappings()
                response = [{
                    'person': dict(row),
                    'total_transferred': row['total_transferred'],
                    'total_received': row['total_received']
                } for row in result]

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/timeline', methods=['GET'])
    def person_transaction_timeline():
        try:
            query_params = request.args
            conditions = []
            parameters = {}

            for key in ['id', 'first_name', 'last_name', 'telephone', 'email', 'city', 'country']:
                if key in query_params:
                    conditions.append(f"p.{key} = :{key}")
                    parameters[key] = query_params[key]

            if not conditions:
                return jsonify({'error': 'At least one person attribute is required'}), 400

            with engine.connect() as connection:
                base_query = """
                    SELECT t.id, t.amount, t.date, 'sent' as type
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                """

                sent_query = base_query + " WHERE " + " AND ".join(conditions)
                sent_transactions = connection.execute(text(sent_query), parameters).mappings().all()

                base_query = """
                    SELECT t.id, t.amount, t.date, 'received' as type
                    FROM transfer t
                    JOIN person p ON t.recipient_id = p.id
                """

                received_query = base_query + " WHERE " + " AND ".join(conditions)
                received_transactions = connection.execute(text(received_query), parameters).mappings().all()

                timeline = sorted(sent_transactions + received_transactions, key=lambda x: x['date'])

                return jsonify(timeline)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/device/total', methods=['GET'])
    def total_transferred_by_device():
        try:
            device_type = request.args.get('device')
            if device_type not in ['android', 'desktop', 'iphone']:
                return jsonify({'error': 'Invalid device type. Use android, desktop, or iphone.'}), 400

            with engine.connect() as connection:
                query = text(f"""
                    SELECT SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.{device_type} = TRUE
                """)
                result = connection.execute(query).scalar()

                response = {
                    'device': device_type,
                    'total_transferred': result
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/transfers/device/max_min', methods=['GET'])
    def max_min_transferred_by_device():
        try:
            device_type = request.args.get('device')
            if device_type not in ['android', 'desktop', 'iphone']:
                return jsonify({'error': 'Invalid device type. Use android, desktop, or iphone.'}), 400

            with engine.connect() as connection:
                max_transferred_query = text(f"""
                    SELECT p.*, SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.{device_type} = TRUE
                    GROUP BY p.id
                    ORDER BY total_transferred DESC
                    LIMIT 1
                """)
                max_transferred_result = connection.execute(max_transferred_query).mappings().fetchone()

                min_transferred_query = text(f"""
                    SELECT p.*, SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.{device_type} = TRUE
                    GROUP BY p.id
                    ORDER BY total_transferred ASC
                    LIMIT 1
                """)
                min_transferred_result = connection.execute(min_transferred_query).mappings().fetchone()

                response = {
                    'device': device_type,
                    'max_transferred': {
                        'person': dict(max_transferred_result) if max_transferred_result else None,
                        'total_transferred': max_transferred_result['total_transferred'] if max_transferred_result else None
                    },
                    'min_transferred': {
                        'person': dict(min_transferred_result) if min_transferred_result else None,
                        'total_transferred': min_transferred_result['total_transferred'] if min_transferred_result else None
                    }
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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

def aggregate_records(table_name, column_name):
    try:
        agg_type = request.args.get('type')
        if agg_type not in ['min', 'max', 'sum', 'avg']:
            return jsonify({'error': 'Invalid aggregation type. Use min, max, sum, or avg.'}), 400

        query = f"SELECT {agg_type.upper()}({column_name}) FROM {table_name}"

        with engine.connect() as connection:
            result = connection.execute(text(query))
            value = result.scalar()
            return jsonify({f'{agg_type}': value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 