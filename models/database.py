from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    android = Column(Boolean, nullable=True)
    desktop = Column(Boolean, nullable=True)
    iphone = Column(Boolean, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)

    def __repr__(self):
        return (f"Person(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, "
                f"telephone={self.telephone}, email={self.email}, android={self.android}, "
                f"desktop={self.desktop}, iphone={self.iphone}, city={self.city}, country={self.country})")

class Promotion(Base):
    __tablename__ = 'promotion'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    client_email = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    promotion = Column(String, nullable=False)
    responded = Column(Boolean, nullable=False)

    def __repr__(self):
        return (f"Promotion(id={self.id}, client_email={self.client_email}, telephone={self.telephone}, "
                f"promotion={self.promotion}, responded={self.responded})")

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    store = Column(String, nullable=False)
    items = relationship("Item", back_populates="transaction")

    def __repr__(self):
        return (f"Transaction(id={self.id}, phone={self.phone}, store={self.store})")

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    item_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    price_per_item = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction = relationship("Transaction", back_populates="items")

    def __repr__(self):
        return (f"Item(id={self.id}, transaction_id={self.transaction_id}, item_name={self.item_name}, "
                f"price={self.price}, price_per_item={self.price_per_item}, quantity={self.quantity})")

class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, nullable=True)
    recipient_id = Column(Integer, nullable=True)
    amount = Column(Float, nullable=True)
    date = Column(Date, nullable=True)

    def __repr__(self):
        return (f"Transfer(id={self.id}, sender_id={self.sender_id}, recipient_id={self.recipient_id}, "
                f"amount={self.amount}, date={self.date})")

def get_engine(user, password, host, port, db):
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

def create_tables(engine):
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    try:
        Base.metadata.create_all(engine)
        for table in Base.metadata.tables.keys():
            if table in existing_tables:
                print(f"Table '{table}' already exists.")
            else:
                print(f"Table '{table}' created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session() 