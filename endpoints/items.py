from flask import jsonify, request
from sqlalchemy import text

def register_items_endpoints(app, engine):
    @app.route('/items/search', methods=['GET'])
    def search_items():
        return search_records('item', ['id', 'transaction_id', 'item_name', 'price', 'price_per_item', 'quantity'])

    @app.route('/items/count', methods=['GET'])
    def count_items():
        return count_records('item', ['id', 'transaction_id', 'item_name', 'price', 'price_per_item', 'quantity'])

    @app.route('/items/aggregation', methods=['GET'])
    def aggregate_items():
        return aggregate_records('item', 'price')

    @app.route('/items/best_worst_seller', methods=['GET'])
    def best_worst_seller():
        try:
            with engine.connect() as connection:
                best_seller_query = text("""
                    SELECT item_name, SUM(quantity) as total_quantity, SUM(price_per_item * quantity) as total_price
                    FROM item
                    GROUP BY item_name
                    ORDER BY total_quantity DESC
                    LIMIT 1
                """)
                best_seller_result = connection.execute(best_seller_query).fetchone()

                worst_seller_query = text("""
                    SELECT item_name, SUM(quantity) as total_quantity, SUM(price_per_item * quantity) as total_price
                    FROM item
                    GROUP BY item_name
                    ORDER BY total_quantity ASC
                    LIMIT 1
                """)
                worst_seller_result = connection.execute(worst_seller_query).fetchone()

                best_seller_profit = best_seller_result[2]
                worst_seller_profit = worst_seller_result[2]

                response = {
                    'best_seller': {
                        'item_name': best_seller_result[0],
                        'total_quantity': best_seller_result[1],
                        'total_price': best_seller_result[2],
                        'profit': best_seller_profit
                    },
                    'worst_seller': {
                        'item_name': worst_seller_result[0],
                        'total_quantity': worst_seller_result[1],
                        'total_price': worst_seller_result[2],
                        'profit': worst_seller_profit
                    }
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/items/summary', methods=['GET'])
    def item_summary():
        try:
            item_name = request.args.get('item_name')
            with engine.connect() as connection:
                if item_name:
                    query = text("""
                        SELECT item_name, SUM(quantity) as total_quantity, SUM(price_per_item * quantity) as total_price
                        FROM item
                        WHERE item_name = :item_name
                        GROUP BY item_name
                    """)
                    result = connection.execute(query, {'item_name': item_name}).fetchone()
                    if result:
                        response = {
                            'item_name': result[0],
                            'total_quantity': result[1],
                            'total_price': result[2]
                        }
                    else:
                        response = {'error': 'Item not found'}
                else:
                    query = text("""
                        SELECT item_name, SUM(quantity) as total_quantity, SUM(price_per_item * quantity) as total_price
                        FROM item
                        GROUP BY item_name
                        ORDER BY total_quantity ASC
                    """)
                    result = connection.execute(query)
                    response = [{'item_name': row[0], 'total_quantity': row[1], 'total_price': row[2]} for row in result]

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