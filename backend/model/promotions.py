from sqlalchemy import Column, Integer, String, Date, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Promotions(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)
    promotion = Column(String, nullable=False)
    responded = Column(String, nullable=False)
    promotion_date = Column(Date, nullable=False)
    email = Column(String, ForeignKey('people.email'), nullable=False)
    telephone = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'promotion': self.promotion,
            'responded': self.responded,
            'promotion_date': self.promotion_date,
            'email': self.email,
            'telephone': self.telephone,
        }