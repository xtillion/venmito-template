from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, nullable=False)
    telephone = Column(String, ForeignKey('people.telephone'))
    store = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    total_price = Column(Numeric, nullable=False)
    price_per_item = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'telephone': self.telephone,
            'store': self.store,
            'item_name': self.item_name,
            'total_price': self.total_price,
            'price_per_item': self.price_per_item,
            'quantity': self.quantity,
            'date': self.date,
        }