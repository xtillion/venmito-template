from flask import jsonify, request
from sqlalchemy import text

def register_transfers_endpoints(app, engine):
   
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
                        'person': max_transferred_result[0] ,
                        'total_transferred': max_transferred_result[1] 
                    },
                    'min_transferred': {
                        'person': min_transferred_result[0],
                        'total_transferred': min_transferred_result[1]
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

    

    @app.route('/transfers/device/total', methods=['GET'])
    def total_transferred_by_device():
        try:
            with engine.connect() as connection:
                # Query for total transferred by android devices
                android_query = text("""
                    SELECT SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.android = TRUE
                """)
                android_result = connection.execute(android_query).scalar()

                # Query for total transferred by desktop devices
                desktop_query = text("""
                    SELECT SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.desktop = TRUE
                """)
                desktop_result = connection.execute(desktop_query).scalar()

                # Query for total transferred by iphone devices
                iphone_query = text("""
                    SELECT SUM(t.amount) as total_transferred
                    FROM transfer t
                    JOIN person p ON t.sender_id = p.id
                    WHERE p.iphone = TRUE
                """)
                iphone_result = connection.execute(iphone_query).scalar()

                response = {
                    'android': android_result,
                    'desktop': desktop_result,
                    'iphone': iphone_result
                }
                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    