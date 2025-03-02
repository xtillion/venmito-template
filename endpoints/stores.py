from flask import jsonify, request
from sqlalchemy import text

def register_stores_endpoints(app, engine):
    @app.route('/stores/profit', methods=['GET'])
    def store_profit():
        try:
            with engine.connect() as connection:
                most_profit_query = text("""
                    SELECT t.store, SUM(i.price_per_item * i.quantity) as total_profit
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                    GROUP BY t.store
                    ORDER BY total_profit DESC
                    LIMIT 1
                """)
                most_profit_result = connection.execute(most_profit_query).fetchone()

                least_profit_query = text("""
                    SELECT t.store, SUM(i.price_per_item * i.quantity) as total_profit
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                    GROUP BY t.store
                    ORDER BY total_profit ASC
                    LIMIT 1
                """)
                least_profit_result = connection.execute(least_profit_query).fetchone()

                response = {
                    'most_profit': {
                        'store': most_profit_result[0],
                        'total_profit': most_profit_result[1]
                    },
                    'least_profit': {
                        'store': least_profit_result[0],
                        'total_profit': least_profit_result[1]
                    }
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/stores/profit/list', methods=['GET'])
    def store_profit_list():
        try:
            with engine.connect() as connection:
                query = text("""
                    SELECT t.store, SUM(i.price_per_item * i.quantity) as total_profit
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                    GROUP BY t.store
                    ORDER BY total_profit DESC
                """)
                result = connection.execute(query)
                response = [{'store': row[0], 'total_profit': row[1]} for row in result]
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/stores/quantity', methods=['GET'])
    def store_quantity():
        try:
            store_name = request.args.get('store')
            with engine.connect() as connection:
                if store_name:
                    query = text("""
                        SELECT t.store, SUM(i.quantity) as total_quantity
                        FROM transaction t
                        JOIN item i ON t.id = i.transaction_id
                        WHERE t.store = :store_name
                        GROUP BY t.store
                    """)
                    result = connection.execute(query, {'store_name': store_name}).fetchone()
                    if result:
                        response = {
                            'store': result[0],
                            'total_quantity': result[1]
                        }
                    else:
                        response = {'error': 'Store not found'}
                else:
                    query = text("""
                        SELECT t.store, SUM(i.quantity) as total_quantity
                        FROM transaction t
                        JOIN item i ON t.id = i.transaction_id
                        GROUP BY t.store
                        ORDER BY total_quantity DESC
                    """)
                    result = connection.execute(query)
                    response = [{'store': row[0], 'total_quantity': row[1]} for row in result]

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/stores/quantity/max_min', methods=['GET'])
    def store_quantity_max_min():
        try:
            with engine.connect() as connection:
                max_quantity_query = text("""
                    SELECT t.store, SUM(i.quantity) as total_quantity
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                    GROUP BY t.store
                    ORDER BY total_quantity DESC
                    LIMIT 1
                """)
                max_quantity_result = connection.execute(max_quantity_query).fetchone()

                min_quantity_query = text("""
                    SELECT t.store, SUM(i.quantity) as total_quantity
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                    GROUP BY t.store
                    ORDER BY total_quantity ASC
                    LIMIT 1
                """)
                min_quantity_result = connection.execute(min_quantity_query).fetchone()

                response = {
                    'max_quantity': {
                        'store': max_quantity_result[0],
                        'total_quantity': max_quantity_result[1]
                    },
                    'min_quantity': {
                        'store': min_quantity_result[0],
                        'total_quantity': min_quantity_result[1]
                    }
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/stores/search', methods=['GET'])
    def search_stores():
        try:
            store_name = request.args.get('store')
            with engine.connect() as connection:
                query = text("""
                    SELECT t.store, SUM(i.price_per_item * i.quantity) as total_profit, SUM(i.quantity) as total_quantity
                    FROM transaction t
                    JOIN item i ON t.id = i.transaction_id
                """)

                if store_name:
                    query = text(query.text + " WHERE t.store = :store_name GROUP BY t.store")
                    result = connection.execute(query, {'store_name': store_name}).fetchone()
                    if result:
                        response = {
                            'store': result[0],
                            'total_profit': result[1],
                            'total_quantity': result[2]
                        }
                    else:
                        response = {'error': 'Store not found'}
                else:
                    query = text(query.text + " GROUP BY t.store ORDER BY total_profit DESC")
                    result = connection.execute(query)
                    response = [{'store': row[0], 'total_profit': row[1], 'total_quantity': row[2]} for row in result]

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500 