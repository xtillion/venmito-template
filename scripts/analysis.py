import os
import sys

# Ensure Python can find the 'scripts' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from scripts.database import query_db

# Function to get clients who participated in promotions
def get_clients_with_promotions():
    query = """
    SELECT Client_ID, First_Name, Last_Name, Phone, email, promotion, responded
    FROM clients
    WHERE promotion IS NOT NULL AND promotion != 'No Promotion';
    """
    return query_db(query)

# Function to get the top stores by revenue
def get_top_stores():
    query = """
    SELECT Store, COUNT(Transaction_ID) AS Num_Transactions, SUM(Amount_USD) AS Total_Revenue
    FROM clients
    WHERE Store IS NOT NULL AND Store != 'No Store'
    GROUP BY Store
    ORDER BY Total_Revenue DESC
    LIMIT 5;
    """
    return query_db(query)

# Calculates the average transaction value from all transactions
def get_avg_transaction_value():
    query = """
    SELECT 
        IFNULL(AVG(Amount_USD), 0) AS Avg_Transaction_Value
    FROM clients
    WHERE Amount_USD > 0;
    """
    return query_db(query)

# Function to get clients with the highest transfer amounts
def get_top_transfers():
    query = """
    SELECT Client_ID, First_Name, Last_Name, Phone, SUM(Transfer_Amount) AS Total_Transferred
    FROM clients
    WHERE Transfer_Amount > 0
    GROUP BY Client_ID, First_Name, Last_Name, Phone
    ORDER BY Total_Transferred DESC
    LIMIT 5;
    """
    return query_db(query)

# Function to get store sales for the past 12 months
def get_store_sales_past_year():
    query = """
    WITH months AS (
    SELECT strftime('%Y-%m', date('now', 'start of month', '-11 months')) AS Month
    UNION ALL
    SELECT strftime('%Y-%m', date(Month || '-01', '+1 month'))
    FROM months
    WHERE Month < strftime('%Y-%m', date('now', 'start of month'))
    )
    SELECT m.Month, 
        IFNULL(SUM(c.Amount_USD), 0) AS Total_Sales
    FROM months m
    LEFT JOIN clients c ON strftime('%Y-%m', c.Transfer_Date) = m.Month
    GROUP BY m.Month
    ORDER BY m.Month ASC;
    """
    return query_db(query)

# Function to get the promotion analysis
def get_promotion_analysis():
    query = """
    SELECT 
        promotion,
        COUNT(*) AS Count,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM clients), 2) AS Percentage
    FROM clients
    GROUP BY promotion;
    """
    return query_db(query)

# Retrieves revenue trends for the last 12 months
def get_revenue_trend():
    query = """
    SELECT strftime('%Y-%m', Transfer_Date) AS Month, SUM(Amount_USD) AS Total_Revenue
    FROM clients
    WHERE Transfer_Date >= date('now', '-12 months')
    GROUP BY Month
    ORDER BY Month ASC;
    """
    return query_db(query)

# Retrieves transaction distribution by store
def get_transaction_distribution():
    query = """
    SELECT Store, COUNT(Transaction_ID) AS Num_Transactions, SUM(Amount_USD) AS Total_Revenue
    FROM clients
    WHERE Store IS NOT NULL AND Store != 'No Store'
    GROUP BY Store
    ORDER BY Total_Revenue DESC;
    """
    return query_db(query)

# Retrieves the top 10 customers by total spent
def get_top_customers():
    query = """
    SELECT 
        c.Client_ID, 
        c.First_Name || ' ' || c.Last_Name AS Customer,
        COUNT(t.Transaction_ID) AS Transactions,
        SUM(t.Amount_USD) AS Total_Spent,
        IFNULL(pr.promotion, 'No Promotion') AS Promotion
    FROM clients c
    LEFT JOIN clients t ON c.Client_ID = t.Client_ID
    LEFT JOIN clients pr ON c.Phone = pr.Phone
    WHERE t.Amount_USD > 0
    GROUP BY c.Client_ID, Customer, pr.promotion
    ORDER BY Total_Spent DESC
    LIMIT 10;
    """
    return query_db(query)

# Retrieves recent transaction data
def get_transactions_data():
    query = """
    SELECT First_Name, Last_Name, Store, Amount_USD, Transfer_Date, 'Credit Card' AS Payment_Method
    FROM clients
    WHERE Amount_USD > 0
    ORDER BY Transfer_Date DESC
    LIMIT 50;
    """
    return query_db(query)

# Retrieves earnings data by store
def get_earnings_data():
    query = """
    SELECT Store, 
        COUNT(Transaction_ID) AS Num_Transactions, 
        SUM(Amount_USD) AS Total_Revenue
    FROM clients
    WHERE Store IS NOT NULL AND Store != 'No Store'
    GROUP BY Store
    ORDER BY Total_Revenue DESC;
    """
    return query_db(query)

# Retrieves revenue trends from April 2023 to April 2024
def get_earnings_trends():
    query = """
    SELECT strftime('%Y-%m', Transfer_Date) AS Month, 
           SUM(Amount_USD) AS Total_Revenue
    FROM clients
    WHERE Store IS NOT NULL 
      AND Store != 'No Store' 
      AND Transfer_Date BETWEEN '2023-04-01' AND '2024-04-30'
    GROUP BY Month
    ORDER BY Month ASC;
    """
    return query_db(query)

# Retrieves customer data with total transactions and spending
def get_customer_data():
    query = """
    SELECT First_Name || ' ' || Last_Name AS Customer, 
           COUNT(Transaction_ID) AS Transactions, 
           SUM(Amount_USD) AS Total_Spent
    FROM clients
    WHERE Amount_USD > 0
    GROUP BY Customer
    ORDER BY Total_Spent DESC
    LIMIT 10;
    """
    return query_db(query)

"""
# Test the functions if the script is run directly
if __name__ == "__main__":
    print("\n🔹 Clients with Promotions:")
    print(get_clients_with_promotions().head())

    print("\n🔹 Top 5 Stores by Revenue:")
    print(get_top_stores().head())

    print("\n🔹 Top 5 Clients by Transfer Amount:")
    print(get_top_transfers().head())

    print("\n🔹 Store Sales for the Last 12 Months:")
    print(get_store_sales_past_year().head())"""