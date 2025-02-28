import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from database import engine  # Engine configured in database.py

st.title("📊 Venmito Data Dashboard")

@st.cache_data
def load_data(query):
    """
    Executes a SQL query using the SQLAlchemy engine and returns the result as a DataFrame.
    
    Uses the raw DBAPI connection to avoid errors related to missing the cursor attribute.
    
    Parameters:
        query (str): The SQL query to execute.
    
    Returns:
        pd.DataFrame: The query result.
    """
    try:
        with engine.connect() as conn:
            # Obtain the underlying raw DBAPI connection
            raw_conn = conn.connection
            return pd.read_sql(query, raw_conn)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs

# ------------------------------
# Insights for Non-Technical Users
# ------------------------------
st.header("Insights")

# Insight 1: Which Clients Have What Type of Promotion?
if st.button("Client Promotions Breakdown"):
    query = """
        SELECT client_email, promotion, COUNT(*) AS count
        FROM promotions
        WHERE client_email IS NOT NULL  
        GROUP BY client_email, promotion
        ORDER BY client_email;
    """
    df = load_data(query)
    if not df.empty:
        st.write("Client Promotions Breakdown:", df)

        # Drop None/Null values before pivoting
        df = df.dropna(subset=["client_email"])

        # Pivot on "client_email" instead of "client_id"
        pivot_df = df.pivot(index="client_email", columns="promotion", values="count").fillna(0)

        st.bar_chart(pivot_df)
    else:
        st.warning("No promotions data available.")

# Insight 2: Suggestions for 'No' Responses in Promotions
if st.button("Promotions - 'No' Responses Analysis"):
    query = """
            SELECT 
            promotion,
            SUM(CASE WHEN LOWER(TRIM(responded)) LIKE 'no%' THEN 1 ELSE 0 END) AS no_count,
            COUNT(*) AS total_count
            FROM promotions
            GROUP BY promotion
            ORDER BY no_count DESC;
            """
    df = load_data(query)
    if not df.empty:
        st.write("Promotions 'No' Responses Analysis:", df)
        # Set index to promotion text for plotting
        df = df.set_index("promotion")
        st.bar_chart(df)
        st.info("Consider offering incentives or alternative promotions to improve acceptance.")
    else:
        st.warning("No 'No' response data available.")

# Insight 3: What Item is the Best Seller?
if st.button("Top 5 Best-Selling Items"):
    query = """
        SELECT item_name, SUM(quantity) AS total_quantity
        FROM transaction_items
        WHERE item_name IS NOT NULL
        GROUP BY item_name
        ORDER BY total_quantity DESC
        LIMIT 5;
    """
    df = load_data(query)
    if not df.empty:
        df = df.sort_values(by="total_quantity", ascending=False)  # Ensure sorting
        st.write("### Top 5 Best-Selling Items:", df)

        # Plot the data with sorted order
        st.bar_chart(df.set_index("item_name"))
    else:
        st.warning("No transaction data available.")

# Insight 4: What Store Has Had the Most Profit?
if st.button("Store Profit Analysis"):
    query = """
        SELECT 
        t.store, 
        SUM(COALESCE(ti.price_per_item, 0) * COALESCE(ti.quantity, 1)) AS revenue
        FROM transactions t
        JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
        GROUP BY t.store
        ORDER BY revenue DESC
        LIMIT 5;
        """
    df = load_data(query)
    if not df.empty:
        st.write("Top 5 Stores by Revenue:", df)
        df = df.set_index("store")
        st.bar_chart(df)
    else:
        st.warning("No data available.")

# Insight 5: Transfer Data Analysis
if st.button("Transfer Data Analysis"):
    query = """
        SELECT sender_id, COUNT(*) AS num_transfers, SUM(amount) AS total_amount
        FROM transfers
        GROUP BY sender_id
        ORDER BY total_amount DESC
        LIMIT 5;
    """
    df = load_data(query)
    
    if not df.empty:
        st.write("### Top 5 Senders by Total Transfer Amount:", df)

        # Separate plots: one for transfer amounts, one for number of transfers
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Total Transfer Amount")
            st.bar_chart(df.set_index("sender_id")["total_amount"])

        with col2:
            st.write("#### Number of Transfers")
            st.bar_chart(df.set_index("sender_id")["num_transfers"])

    else:
        st.warning("No data available.")

st.markdown("---")

# ------------------------------
# Technical SQL Query Interface
# ------------------------------
st.header("Technical SQL Query Interface")
user_query = st.text_area("Enter your SQL query:", """SELECT t.store, SUM(ti.price_per_item * ti.quantity) AS total_revenue
                                                        FROM transactions t
                                                        JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
                                                        GROUP BY t.store
                                                        ORDER BY total_revenue DESC;
                                                        """
                                                        )
if st.button("Run Query"):
    df_query = load_data(user_query)
    if not df_query.empty:
        st.write("Query Results:", df_query)
        # Save query result in session_state for plotting later
        st.session_state.df_query = df_query
    else:
        st.warning("No results returned.")

st.markdown("---")

# ------------------------------
# Data Visualization Section
# ------------------------------
st.header("Data Visualization")
if st.checkbox("Plot Query Results"):
    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Area Chart"])
    if "df_query" in st.session_state:
        df_to_plot = st.session_state.df_query
    else:
        st.warning("Please run a query first.")
        df_to_plot = pd.DataFrame()
    
    if not df_to_plot.empty:
        numeric_cols = df_to_plot.select_dtypes(include=["number"])
        if not numeric_cols.empty:
            if chart_type == "Line Chart":
                st.line_chart(numeric_cols)
            elif chart_type == "Bar Chart":
                st.bar_chart(numeric_cols)
            elif chart_type == "Area Chart":
                st.area_chart(numeric_cols)
        else:
            st.warning("No numeric columns available for plotting.")