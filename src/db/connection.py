import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Get a database connection."""
    # Get connection details from environment variables for security
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=os.environ.get('DB_PORT', '5432')
    )
    return conn