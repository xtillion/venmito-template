from flask import jsonify, request
from sqlalchemy import text

def register_items_endpoints(app, engine):

    @app.route('/items/summary', methods=['GET'])
    def item_summary():
        try:
            with engine.connect() as connection:
                # Query to get the summary of all items
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
