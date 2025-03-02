import os
import sqlite3
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()
# Get the base directory (two levels up from the script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# Construct the correct paths
db_file = os.path.join(BASE_DIR, "src/database", "venmito.db")


# ---------------------
# Pydantic Models
# ---------------------
class TransactionItem(BaseModel):
    """
    Represents an item within a transaction.
    """
    item_name: str
    quantity: int
    price_per_item: float
    total_price: float


class Transaction(BaseModel):
    """
    Represents a single transaction.
    If you include items on POST, it will insert both
    the transaction row and its transaction_items rows.
    """
    phone: str
    store: str
    total_price: float
    items: Optional[List[TransactionItem]] = None


# ---------------------
# Database Helper
# ---------------------
def query_db(query: str, params: tuple = ()):
    """Helper function to query SQLite and return list of dicts."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------
# Routes
# ---------------------
@router.get("/")
def get_transactions(
    phone: str = Query(None),
    store: str = Query(None),
    limit: int = Query(10, ge=1)
):
    """
    Fetch transactions, optionally filtered by phone, store, 
    and limited by 'limit' (default = 10).
    Each transaction includes a nested 'items' list.
    """
    # 1. Base query to join transactions + items
    query = """
        SELECT 
            t.transaction_id, 
            t.phone, 
            t.store, 
            t.total_price AS transaction_total,
            i.item_name, 
            i.quantity, 
            i.price_per_item, 
            i.total_price AS item_total
        FROM transactions t
        LEFT JOIN transaction_items i 
            ON t.transaction_id = i.transaction_id
        WHERE 1=1
    """
    params = []

    # 2. Apply filters
    if phone:
        query += " AND t.phone = ?"
        params.append(phone)
    if store:
        query += " AND t.store = ?"
        params.append(store)

    query += " ORDER BY t.transaction_id DESC"

    # 3. Apply limit
    if limit:
        query += " LIMIT ?"
        params.append(limit)

    # 4. Execute query and group items
    rows = query_db(query, tuple(params))

    # Build a dictionary to group items by transaction_id
    transactions_dict = {}
    for row in rows:
        tid = row["transaction_id"]
        if tid not in transactions_dict:
            transactions_dict[tid] = {
                "transaction_id": tid,
                "phone": row["phone"],
                "store": row["store"],
                "total_price": row["transaction_total"],
                "items": []
            }
        if row["item_name"]:
            item_info = {
                "item_name": row["item_name"],
                "quantity": row["quantity"],
                "price_per_item": row["price_per_item"],
                "total_price": row["item_total"]
            }
            transactions_dict[tid]["items"].append(item_info)

    return list(transactions_dict.values())

@router.get("/items_summary")
def get_items_summary():
    """
    Returns each distinct item, total quantity sold, and total revenue,
    in descending order by total revenue.
    Example output:
    [
      {
        "item_name": "Popsi",
        "total_quantity": 55,
        "total_revenue": 220.0
      },
      ...
    ]
    """
    query = """
        SELECT 
            item_name,
            SUM(quantity) AS total_quantity,
            SUM(total_price) AS total_revenue
        FROM transaction_items
        GROUP BY item_name
        ORDER BY total_revenue DESC
    """
    results = query_db(query)
    return results


@router.get("/{transaction_id}")
def get_transaction_by_id(transaction_id: int):
    """
    Fetch a single transaction (with items) by its ID.
    """
    query = """
        SELECT 
            t.transaction_id, 
            t.phone, 
            t.store, 
            t.total_price AS transaction_total,
            i.item_name, 
            i.quantity, 
            i.price_per_item, 
            i.total_price AS item_total
        FROM transactions t
        LEFT JOIN transaction_items i 
            ON t.transaction_id = i.transaction_id
        WHERE t.transaction_id = ?
        ORDER BY t.transaction_id
    """
    rows = query_db(query, (transaction_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Build the transaction object
    transaction_data = {
        "transaction_id": transaction_id,
        "phone": rows[0]["phone"],
        "store": rows[0]["store"],
        "total_price": rows[0]["transaction_total"],
        "items": []
    }
    for row in rows:
        if row["item_name"]:
            item_info = {
                "item_name": row["item_name"],
                "quantity": row["quantity"],
                "price_per_item": row["price_per_item"],
                "total_price": row["item_total"]
            }
            transaction_data["items"].append(item_info)

    return transaction_data



@router.post("/")
def create_transaction(transaction: Transaction):
    """
    Create a new transaction record, plus optional items.

    Example Request Body:
    {
      "phone": "555-1234",
      "store": "Trader Tales",
      "total_price": 25.0,
      "items": [
         {"item_name": "Popsi", "quantity": 1, "price_per_item": 4.0, "total_price": 4.0},
         ...
      ]
    }
    """
    # 1. Insert into transactions table
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (phone, store, total_price)
        VALUES (?, ?, ?)
    ''', (transaction.phone, transaction.store, transaction.total_price))
    new_transaction_id = cursor.lastrowid

    # 2. Insert each item into transaction_items table (if any)
    if transaction.items:
        for item in transaction.items:
            cursor.execute('''
                INSERT INTO transaction_items (transaction_id, item_name, quantity, price_per_item, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (new_transaction_id, item.item_name, item.quantity, item.price_per_item, item.total_price))

    conn.commit()
    conn.close()

    return {"transaction_id": new_transaction_id, "message": "Transaction created successfully."}


__all__ = ["router"]
