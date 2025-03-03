from sqlalchemy import text

class Transaction:
    def __init__(self, id, phone, store):
        self.id = id
        self.phone = phone
        self.store = store


    def __repr__(self):
        return (f"Transaction(id={self.id}, phone={self.phone}, store={self.store}, items={self.items})")

    @staticmethod
    def insert_transaction(engine, transaction):
        try:
            with engine.connect() as connection:
                query = text("""
                    INSERT INTO transaction (id, phone, store)
                    VALUES (:id, :phone, :store)
                    ON CONFLICT (id) DO NOTHING
                """)
                result = connection.execute(query, {
                    'id': transaction.id,
                    'phone': transaction.phone,
                    'store': transaction.store
                })

                if result.rowcount > 0:
                    connection.commit()
                    print(f"Successfully inserted transaction {transaction.id}")
                else:
                    connection.rollback()
                    print(f"Transaction {transaction.id} already exists, skipping insertion.")
        except Exception as e:
            print(f"Error inserting transaction {transaction.id}: {e}") 