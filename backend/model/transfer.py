from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transfers(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'amount': self.amount,
            'date': self.date,
        }