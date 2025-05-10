import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Replace hardcoded values with .env variables
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///fallback.db")  # Fallback to SQLite if not defined
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False")