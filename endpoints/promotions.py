from flask import jsonify, request
from sqlalchemy import text

def register_promotions_endpoints(app, engine):
    @app.route('/promotions/search', methods=['GET'])
    def search_promotions():
        try:
            query_params = request.args
            conditions = []
            parameters = {}

            for key in ['id', 'client_email', 'telephone', 'promotion', 'responded']:
                if key in query_params:
                    conditions.append(f"{key} = :{key}")
                    parameters[key] = query_params[key]

            if not conditions:
                return jsonify({'error': 'At least one search parameter is required'}), 400

            with engine.connect() as connection:
                query = f"SELECT * FROM promotion WHERE {' AND '.join(conditions)}"
                result = connection.execute(text(query), parameters)
                promotions = [dict(row) for row in result]
                return jsonify(promotions)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/promotions/search/person', methods=['GET'])
    def search_promotions_by_person():
        try:
            query_params = request.args
            conditions = []
            parameters = {}

            for key in ['id', 'first_name', 'last_name', 'telephone', 'email', 'android', 'desktop', 'iphone', 'city', 'country']:
                if key in query_params:
                    conditions.append(f"p.{key} = :{key}")
                    parameters[key] = query_params[key]

            if not conditions:
                return jsonify({'error': 'At least one person attribute is required'}), 400

            with engine.connect() as connection:
                base_query = """
                    SELECT p.*, pr.promotion, pr.responded
                    FROM person p
                    JOIN promotion pr ON p.email = pr.client_email OR p.telephone = pr.telephone
                """

                if conditions:
                    base_query += " WHERE " + " AND ".join(conditions)

                result = connection.execute(text(base_query), parameters).mappings().all()

                responded_promotions = [dict(row) for row in result if row['responded']]
                not_responded_promotions = [dict(row) for row in result if not row['responded']]

                response = {
                    'total_promotions': len(result),
                    'responded_promotions': responded_promotions,
                    'not_responded_promotions': not_responded_promotions
                }

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/promotions/responded/max_min', methods=['GET'])
    def promotions_responded_max_min():
        try:
            with engine.connect() as connection:
                max_responded_query = text("""
                    SELECT pr.promotion, COUNT(pr.id) as response_count
                    FROM promotion pr
                    WHERE pr.responded = TRUE
                    GROUP BY pr.promotion
                    ORDER BY response_count DESC
                    LIMIT 1
                """)
                max_responded_result = connection.execute(max_responded_query).fetchone()

                min_responded_query = text("""
                    SELECT pr.promotion, COUNT(pr.id) as response_count
                    FROM promotion pr
                    WHERE pr.responded = TRUE
                    GROUP BY pr.promotion
                    ORDER BY response_count ASC
                    LIMIT 1
                """)
                min_responded_result = connection.execute(min_responded_query).fetchone()

                response = {
                    'max_responded': {
                        'promotion': max_responded_result[0] if max_responded_result else None,
                        'response_count': max_responded_result[1] if max_responded_result else None
                    },
                    'min_responded': {
                        'promotion': min_responded_result[0] if min_responded_result else None,
                        'response_count': min_responded_result[1] if min_responded_result else None
                    }
                }

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/promotions/responded/city/max_min', methods=['GET'])
    def promotions_responded_city_max_min():
        try:
            with engine.connect() as connection:
                max_responded_city_query = text("""
                    SELECT p.city, COUNT(pr.id) as response_count
                    FROM promotion pr
                    JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                    WHERE pr.responded = TRUE
                    GROUP BY p.city
                    ORDER BY response_count DESC
                    LIMIT 1
                """)
                max_responded_city_result = connection.execute(max_responded_city_query).fetchone()

                min_responded_city_query = text("""
                    SELECT p.city, COUNT(pr.id) as response_count
                    FROM promotion pr
                    JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                    WHERE pr.responded = TRUE
                    GROUP BY p.city
                    ORDER BY response_count ASC
                    LIMIT 1
                """)
                min_responded_city_result = connection.execute(min_responded_city_query).fetchone()

                response = {
                    'max_responded_city': {
                        'city': max_responded_city_result[0] if max_responded_city_result else None,
                        'response_count': max_responded_city_result[1] if max_responded_city_result else None
                    },
                    'min_responded_city': {
                        'city': min_responded_city_result[0] if min_responded_city_result else None,
                        'response_count': min_responded_city_result[1] if min_responded_city_result else None
                    }
                }

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/promotions/responded/device/max_min', methods=['GET'])
    def promotions_responded_device_max_min():
        try:
            with engine.connect() as connection:
                max_responded_device_query = text("""
                    SELECT device_type, COUNT(id) as response_count
                    FROM (
                        SELECT 'android' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.android = TRUE
                        UNION ALL
                        SELECT 'desktop' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.desktop = TRUE
                        UNION ALL
                        SELECT 'iphone' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.iphone = TRUE
                    ) as device_responses
                    GROUP BY device_type
                    ORDER BY response_count DESC
                    LIMIT 1
                """)
                max_responded_device_result = connection.execute(max_responded_device_query).fetchone()

                min_responded_device_query = text("""
                    SELECT device_type, COUNT(id) as response_count
                    FROM (
                        SELECT 'android' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.android = TRUE
                        UNION ALL
                        SELECT 'desktop' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.desktop = TRUE
                        UNION ALL
                        SELECT 'iphone' as device_type, pr.id
                        FROM promotion pr
                        JOIN person p ON p.email = pr.client_email OR p.telephone = pr.telephone
                        WHERE pr.responded = TRUE AND p.iphone = TRUE
                    ) as device_responses
                    GROUP BY device_type
                    ORDER BY response_count ASC
                    LIMIT 1
                """)
                min_responded_device_result = connection.execute(min_responded_device_query).fetchone()

                response = {
                    'max_responded_device': {
                        'device': max_responded_device_result[0] if max_responded_device_result else None,
                        'response_count': max_responded_device_result[1] if max_responded_device_result else None
                    },
                    'min_responded_device': {
                        'device': min_responded_device_result[0] if min_responded_device_result else None,
                        'response_count': min_responded_device_result[1] if min_responded_device_result else None
                    }
                }

                return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/promotions/count', methods=['GET'])
    def count_promotions():
        try:
            query_params = request.args
            query = "SELECT COUNT(*) FROM promotion WHERE "
            conditions = []
            parameters = {}

            for key, value in query_params.items():
                if key in ['id', 'client_email', 'telephone', 'promotion', 'responded']:
                    conditions.append(f"{key} = :{key}")
                    parameters[key] = value

            if conditions:
                query += " AND ".join(conditions)
            else:
                query = "SELECT COUNT(*) FROM promotion"

            with engine.connect() as connection:
                result = connection.execute(text(query), parameters)
                count = result.scalar()
                return jsonify({'count': count})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Add other promotions-related endpoints here 