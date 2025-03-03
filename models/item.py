from sqlalchemy import text

class Item:
    def __init__(self, transaction_id, item_name, price, price_per_item, quantity):
        self.transaction_id = transaction_id
        self.item_name = item_name
        self.price = price
        self.price_per_item = price_per_item
        self.quantity = quantity

    def __repr__(self):
        return (f"Item(transaction_id={self.transaction_id}, item_name={self.item_name}, "
                f"price={self.price}, price_per_item={self.price_per_item}, quantity={self.quantity})")

    @staticmethod
    def insert_item(engine, item):
        try:
            with engine.connect() as connection:
                query = text("""
                    INSERT INTO item (transaction_id, item_name, price, price_per_item, quantity)
                    VALUES (:transaction_id, :item_name, :price, :price_per_item, :quantity)
                """)
                result = connection.execute(query, {
                    'transaction_id': item.transaction_id,
                    'item_name': item.item_name,
                    'price': item.price,
                    'price_per_item': item.price_per_item,
                    'quantity': item.quantity
                })

                if result.rowcount > 0:
                    connection.commit()
                    print(f"Successfully inserted item {item.item_name} for transaction {item.transaction_id}")
                else:
                    connection.rollback()
                    print(f"Failed to insert item {item.item_name} for transaction {item.transaction_id}")
        except Exception as e:
            print(f"Error inserting item {item.item_name}: {e}") 