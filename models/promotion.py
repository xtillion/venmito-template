from sqlalchemy import text

class Promotion:
    def __init__(self, id, client_email, telephone, promotion, responded):
        self.id = id
        self.client_email = client_email if client_email else None
        self.telephone = telephone if telephone else None
        self.promotion = promotion
        self.responded = bool(responded)

    def __repr__(self):
        return (f"Promotion(id={self.id}, client_email={self.client_email}, telephone={self.telephone}, "
                f"promotion={self.promotion}, responded={self.responded})")

    @staticmethod
    def insert_promotion(engine, promotion):
        try:
            with engine.connect() as connection:
                query = text("""
                    INSERT INTO promotion (id, client_email, telephone, promotion, responded)
                    VALUES (:id, :client_email, :telephone, :promotion, :responded)
                    ON CONFLICT (id) DO NOTHING
                """)
                result = connection.execute(query, {
                    'id': promotion.id,
                    'client_email': promotion.client_email,
                    'telephone': promotion.telephone,
                    'promotion': promotion.promotion,
                    'responded': promotion.responded
                })

                if result.rowcount > 0:
                    connection.commit()
                    print(f"Successfully inserted promotion {promotion.id}")
                else:
                    connection.rollback()
                    print(f"Promotion {promotion.id} already exists, skipping insertion.")
        except Exception as e:
            print(f"Error inserting promotion {promotion.id}: {e}") 