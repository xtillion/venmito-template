import os
import sqlite3

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# Construct the correct paths
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")


# Pydantic Model for Request Validation
class Person(BaseModel):
    first_name: str = Field(..., title="First Name")
    last_name: str = Field(..., title="Last Name")
    email: str = Field(None, title="Email")
    phone: str = Field(None, title="Phone Number")
    city: str = Field(..., title="City")
    country: str = Field(..., title="Country")
    android: int = Field(..., title="Uses Android (1/0)")
    iphone: int = Field(..., title="Uses iPhone (1/0)")
    desktop: int = Field(..., title="Uses Desktop (1/0)")

    @staticmethod
    def validate_email_or_phone(person):
        if not person.email and not person.phone:
            raise HTTPException(status_code=400, detail="Either email or phone must be provided.")
        return person

# Database Query Helper Function
def query_db(query: str, params: tuple = ()):  
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/")
def get_people(email: str = Query(None), phone: str = Query(None), city: str = Query(None), country: str = Query(None), limit: int = Query(10, ge=1)):
    """Fetch people data, optionally filtered by email, phone, city, or country, with an optional limit on the number of records returned."""
    query = "SELECT * FROM people WHERE 1=1"
    params = []
    if email:
        query += " AND email = ?"
        params.append(email)
    if phone:
        query += " AND telephone = ?"
        params.append(phone)
    if city:
        query += " AND city = ?"
        params.append(city)
    if country:
        query += " AND country = ?"
        params.append(country)
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    return query_db(query, tuple(params))

@router.get("/device_counts")
def get_device_counts():
    """Returns the total count of each device type in descending order."""
    query = '''
        SELECT 'Android' AS device, SUM(android) AS total FROM people
        UNION ALL
        SELECT 'iPhone', SUM(iphone) FROM people
        UNION ALL
        SELECT 'Desktop', SUM(desktop) FROM people
        ORDER BY total DESC;
    '''
    return query_db(query)

@router.get("/{id}")
def get_person_by_id(id: int):
    """Fetch a single person by their ID."""
    result = query_db("SELECT * FROM people WHERE id = ?", (id,))
    if not result:
        raise HTTPException(status_code=404, detail="Person not found")
    return result[0]

@router.post("/")
def create_person(person: Person):
    """Create a new person in the database."""
    Person.validate_email_or_phone(person)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO people (first_name, last_name, email, telephone, city, country, android, iphone, desktop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (person.first_name, person.last_name, person.email, person.phone, person.city, person.country, person.android, person.iphone, person.desktop))
    conn.commit()
    new_person_id = cursor.lastrowid
    conn.close()
    
    return {"id": new_person_id, "message": "Person created successfully."}

# Export router for inclusion in Router.py
__all__ = ["router"]

