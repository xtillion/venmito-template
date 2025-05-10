import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from backend.db_config import Config

# Configure logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Create engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Scoped session for thread-safe database sessions
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_session = Session()

# Declarative base
Base = declarative_base()

# Function to initialize the database
def create_database():
    Base.metadata.create_all(bind=engine)

# Test database connectivity
if __name__ == "__main__":
    try:
        print("Testing database connection...")
        conn = engine.connect()
        print("Connected successfully!")
        create_database()
        print("Database tables created successfully!")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")