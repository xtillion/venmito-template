from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    android = Column(Boolean, default=False, nullable=False)
    iphone = Column(Boolean, default=False, nullable=False)
    desktop = Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'telephone': self.telephone,
            'email': self.email,
            'dob': self.dob,
            'city': self.city,
            'country': self.country,
            'android': self.android,
            'iphone': self.iphone,
            'desktop': self.desktop
        }