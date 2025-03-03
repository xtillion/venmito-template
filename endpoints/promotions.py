from flask import jsonify, request
from sqlalchemy import text

def register_promotions_endpoints(app, engine):
    

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

    
    # Add other promotions-related endpoints here 