from fastapi import FastAPI

from src.api.people import router as people_router
from src.api.promotions import router as promotions_router
from src.api.transactions import router as transactions_router
from src.api.transfers import router as transfers_router

# Create FastAPI instance
app = FastAPI()



# Include all route modules
app.include_router(people_router, prefix="/people", tags=["People"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
app.include_router(transfers_router, prefix="/transfers", tags=["Transfers"])
app.include_router(promotions_router, prefix="/promotions", tags=["Promotions"])

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Venmito API!"}
