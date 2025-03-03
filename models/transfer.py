from sqlalchemy import text

class Transfer:
    def __init__(self, sender_id, recipient_id, amount, date):
        self.sender_id = sender_id if sender_id else None
        self.recipient_id = recipient_id if recipient_id else None
        self.amount = float(amount) if amount else None
        self.date = date if date else None

    def __repr__(self):
        return (f"Transfer(sender_id={self.sender_id}, recipient_id={self.recipient_id}, "
                f"amount={self.amount}, date={self.date})")

    @staticmethod
    def insert_transfer(engine, transfer):
        try:
            with engine.connect() as connection:
                query = text("""
                    INSERT INTO transfer (sender_id, recipient_id, amount, date)
                    VALUES (:sender_id, :recipient_id, :amount, :date)
                """)
                result = connection.execute(query, {
                    'sender_id': transfer.sender_id,
                    'recipient_id': transfer.recipient_id,
                    'amount': transfer.amount,
                    'date': transfer.date
                })

                if result.rowcount > 0:
                    connection.commit()
                    print(f"Successfully inserted transfer from {transfer.sender_id} to {transfer.recipient_id}")
                else:
                    connection.rollback()
                    print(f"Failed to insert transfer from {transfer.sender_id} to {transfer.recipient_id}")
        except Exception as e:
            print(f"Error inserting transfer from {transfer.sender_id} to {transfer.recipient_id}: {e}") 