import os
import sqlite3

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# Construct the correct paths
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")

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
def get_promotions(client_email: str = Query(None), promotion_type: str = Query(None), responded: str = Query(None), limit: int = Query(10, ge=1)):
    """Fetch promotions data, optionally filtered by client email, promotion type, or response status, with an optional limit."""
    query = "SELECT * FROM promotions WHERE 1=1"
    params = []
    if client_email:
        query += " AND client_email = ?"
        params.append(client_email)
    if promotion_type:
        query += " AND promotion = ?"
        params.append(promotion_type)
    if responded:
        query += " AND responded = ?"
        params.append(responded)
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    return query_db(query, tuple(params))

@router.get("/{id}")
def get_promotion_by_id(id: int):
    """Fetch a single promotion by its ID."""
    result = query_db("SELECT * FROM promotions WHERE id = ?", (id,))
    if not result:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return result[0]

@router.get("/most_popular")
def get_most_popular_promotions():
    """Fetch all promotions in ascending order and highlight the top 5 most popular."""
    query = """
        SELECT promotion, COUNT(*) as count
        FROM promotions
        GROUP BY promotion
        ORDER BY count ASC;
    """
    results = query_db(query)
    if not results:
        raise HTTPException(status_code=404, detail="No promotion data found")
    
    # Mark top 5 promotions
    for i in range(min(5, len(results))):
        results[i]["top"] = True
    
    return results

@router.post("/")
def create_promotion(client_email: str, promotion: str, responded: str):
    """Create a new promotion entry in the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO promotions (client_email, promotion, responded)
        VALUES (?, ?, ?)
    ''', (client_email, promotion, responded))
    conn.commit()
    new_promotion_id = cursor.lastrowid
    conn.close()
    
    return {"id": new_promotion_id, "message": "Promotion created successfully."}

# Export router for inclusion in Router.py
__all__ = ["router"]
