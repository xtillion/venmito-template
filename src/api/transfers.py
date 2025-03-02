import os
import sqlite3

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Get base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(BASE_DIR, "src/database/venmito.db")

# Helper function to query the database
def query_db(query: str, params: tuple = ()):  
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/")
def get_transfers(limit: int = Query(10, ge=1)):
    """Fetch all transfers with an optional limit."""
    query = "SELECT * FROM transfers ORDER BY date DESC LIMIT ?"
    return query_db(query, (limit,))


@router.get("/{id}")
def get_transfer_by_id(id: int):
    """Fetch a specific transfer by its ID."""
    result = query_db("SELECT * FROM transfers WHERE sender_id = ? OR recipient_id = ?", (id, id))
    if not result:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return result


@router.post("/")
def create_transfer(sender_id: int, recipient_id: int, amount: float, date: str):
    """Create a new transfer record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transfers (sender_id, recipient_id, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (sender_id, recipient_id, amount, date))
    conn.commit()
    new_transfer_id = cursor.lastrowid
    conn.close()
    return {"transfer_id": new_transfer_id, "message": "Transfer recorded successfully."}

# Export router
__all__ = ["router"]
