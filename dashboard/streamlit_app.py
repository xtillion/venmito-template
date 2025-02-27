import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# ---------------------------
# Page Configuration & Secrets
# ---------------------------
st.set_page_config(page_title="Venmito Data Dashboard", layout="wide", initial_sidebar_state="expanded")
# Use secrets.toml in the .streamlit folder to configure the database connection
DATABASE_URL = st.secrets.get("DATABASE_URL", "postgresql://admin:admin_pass@db:5432/venmito_db")
engine = create_engine(DATABASE_URL)

# ---------------------------
# Caching function to load SQL data
# ---------------------------
@st.cache_data(show_spinner=False)
def load_data(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# ---------------------------
# Load Data from PostgreSQL (all data files are loaded once here)
# ---------------------------
df_clients = load_data("SELECT * FROM clients")
df_transactions = load_data("SELECT * FROM transactions")
df_transaction_items = load_data("SELECT * FROM transaction_items")
df_transfers = load_data("SELECT * FROM transfers")
df_promotions = load_data("SELECT * FROM promotions")

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.header("Navigation")
section = st.sidebar.selectbox(
    "Select Analysis Section", 
    [
        "Promotions Analysis",
        "Store Insights",
        "Client Demographics & Device Usage Analysis",
        "Transfer Analysis",
        "Summary Statistics"
    ]
)

# ---------------------------
# Section: Promotions Analysis (Grouping all promotions-related charts)
# ---------------------------
if section == "Promotions Analysis":
    st.header("Promotions Analysis")
    
    # Use tabs to organize the different promotions analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "Clients Promotions", 
        "Analyzing 'No' Responses", 
        "Contact Method Rejections", 
        "Promotion Effectiveness"
    ])
    
    with tab1:
        st.subheader("1. Which Clients Have What Type of Promotion?")
        # Create a unified identifier: prioritize client_email over telephone
        df_promotions["client_id"] = df_promotions["client_email"].combine_first(df_promotions["telephone"])
        # Group by client_id and promotion type
        df_promos_summary = (
            df_promotions.groupby(["client_id", "promotion"])
            .size()
            .reset_index(name="count")
        )
        # Identify top 10 clients (by total promotions received)
        top_clients = (
            df_promos_summary.groupby("client_id")["count"]
            .sum()
            .reset_index()
            .sort_values("count", ascending=False)
            .head(10)
        )
        # Filter for only these top clients
        df_promos_summary_top = df_promos_summary[df_promos_summary["client_id"].isin(top_clients["client_id"])]
        # Stacked bar chart
        fig_promos = px.bar(
            df_promos_summary_top,
            x="client_id",
            y="count",
            color="promotion",
            barmode="stack",
            title="Promotions Received per Client (Top 10)",
            labels={"client_id": "Client Identifier", "count": "Number of Promotions", "promotion": "Promotion Type"},
            template="plotly_white"
        )
        fig_promos.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_promos, use_container_width=True)
    
    with tab2:
        st.subheader("2. Analyzing 'No' Responses in Promotions")
        # (For this tab we work directly with the promotions data loaded from SQL)
        # Convert 'responded' column to boolean (if not already converted)
        df_promotions["responded"] = df_promotions["responded"].map({"Yes": True, "No": False})
        # Count "No" responses per promotion type
        no_responses = df_promotions[df_promotions["responded"] == False].groupby("promotion").size().reset_index(name="no_count")
        # Count total responses per promotion type
        total_responses = df_promotions.groupby("promotion").size().reset_index(name="total_count")
        # Merge and calculate "No" percentage
        promotion_analysis = pd.merge(total_responses, no_responses, on="promotion", how="left").fillna(0)
        promotion_analysis["no_percentage"] = (promotion_analysis["no_count"] / promotion_analysis["total_count"]) * 100
        # Sort from least to most 'No' responses
        promotion_analysis = promotion_analysis.sort_values("no_percentage", ascending=True)
        # Create bar chart
        fig_no = go.Figure()
        fig_no.add_trace(go.Bar(
            x=promotion_analysis["promotion"],
            y=promotion_analysis["no_percentage"],
            name="Percentage of 'No' Responses",
            marker=dict(color="dodgerblue"),
            text=promotion_analysis["no_percentage"].apply(lambda x: f"{x:.2f}%"),
            textposition="auto"
        ))
        fig_no.update_layout(
            title="Percentage of 'No' Responses per Promotion",
            xaxis_title="Promotion Type",
            yaxis_title="Percentage of 'No' Responses",
            xaxis=dict(categoryorder="array", categoryarray=promotion_analysis["promotion"]),
            template="plotly_white",
            xaxis_tickangle=45
        )
        st.plotly_chart(fig_no, use_container_width=True)
    
    with tab3:
        st.subheader("3. Promotion Rejections by Contact Method")
        # Categorize contact method using the promotions data
        df_promotions["contact_method"] = df_promotions.apply(
            lambda row: "Both" if pd.notna(row["client_email"]) and pd.notna(row["telephone"])
            else "Email" if pd.notna(row["client_email"])
            else "Phone" if pd.notna(row["telephone"])
            else "Unknown",
            axis=1
        )
        # Count "No" responses per contact method
        contact_no_responses = df_promotions[df_promotions["responded"] == False].groupby("contact_method").size().reset_index(name="no_count")
        # Count total responses per contact method
        total_responses_contact = df_promotions.groupby("contact_method").size().reset_index(name="total_count")
        # Merge and calculate rejection percentage
        contact_method_rejection_rate = pd.merge(contact_no_responses, total_responses_contact, on="contact_method", how="right")
        contact_method_rejection_rate["no_percentage"] = (contact_method_rejection_rate["no_count"].fillna(0) / contact_method_rejection_rate["total_count"]) * 100
        # Define custom colors
        color_map = {"Both": "blue", "Email": "green", "Phone": "orange", "Unknown": "red"}
        # Create bar chart
        fig_contact = px.bar(
            contact_method_rejection_rate.sort_values("no_percentage", ascending=False),
            x="contact_method",
            y="no_percentage",
            title="Rejection Rates by Contact Method",
            labels={"no_percentage": "Percentage of No Responses", "contact_method": "Contact Method"},
            text_auto=".2f",
            color="contact_method",
            color_discrete_map=color_map,
            template="plotly_white"
        )
        fig_contact.update_layout(xaxis_tickangle=0)
        st.plotly_chart(fig_contact, use_container_width=True)
    
    with tab4:
        st.subheader("4. Promotion Effectiveness Analysis")
        # Calculate the response rate for each promotion type
        promo_summary = (
            df_promotions.groupby("promotion")
            .agg(
                total_promos=("id", "count"),
                responded_count=("responded", lambda x: x.sum())
            )
            .reset_index()
        )
        promo_summary["response_rate"] = (promo_summary["responded_count"] / promo_summary["total_promos"]) * 100
        # Create bar chart
        fig_effectiveness = px.bar(
            promo_summary,
            x="promotion",
            y="response_rate",
            title="Promotion Response Rate (%)",
            labels={"promotion": "Promotion", "response_rate": "Response Rate (%)"},
            template="plotly_white"
        )
        fig_effectiveness.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_effectiveness, use_container_width=True)

# ---------------------------
# Section: Store Insights (Using Transaction and Transaction Items Data)
# ---------------------------
elif section == "Store Insights":
    st.header("Store Insights: Best-Selling Items & Most Profitable Stores")
    
    # Best-Selling Items Analysis
    st.subheader("Best-Selling Items")
    df_transaction_items["quantity"] = pd.to_numeric(df_transaction_items["quantity"], errors="coerce")
    best_items = df_transaction_items.groupby("item_name").agg(total_quantity=("quantity", "sum")).reset_index()
    best_items = best_items.sort_values("total_quantity", ascending=True).head(10)
    color_map_items = px.colors.qualitative.Prism
    fig_best_items = px.histogram(
        best_items,
        x="total_quantity",
        y="item_name",
        orientation="h",
        title="Top 10 Best-Selling Items",
        labels={"total_quantity": "Total Quantity Sold", "item_name": "Item Name"},
        text_auto=".2f",
        template="plotly_white",
        color="item_name",
        color_discrete_sequence=color_map_items
    )
    fig_best_items.update_layout(xaxis_title="Total Quantity Sold", yaxis_title="Item Name")
    st.plotly_chart(fig_best_items, use_container_width=True)
    
    # Most Profitable Store Analysis
    st.subheader("Most Profitable Stores")
    df_transaction_items["price_per_item"] = pd.to_numeric(df_transaction_items["price_per_item"], errors="coerce")
    df_transaction_items["quantity"] = pd.to_numeric(df_transaction_items["quantity"], errors="coerce")
    df_transaction_items["total_revenue"] = df_transaction_items["price_per_item"] * df_transaction_items["quantity"]
    df_merged = pd.merge(df_transaction_items, df_transactions[["id", "store"]], left_on="transaction_id", right_on="id", how="left")
    store_revenue = df_merged.groupby("store").agg(total_revenue=("total_revenue", "sum")).reset_index()
    store_revenue = store_revenue.sort_values("total_revenue", ascending=True)
    color_map_stores = px.colors.qualitative.Safe
    fig_store_profit = px.bar(
        store_revenue,
        x="total_revenue",
        y="store",
        orientation="h",
        title="Most Profitable Stores",
        labels={"total_revenue": "Total Revenue ($)", "store": "Store Name"},
        text_auto=".2f",
        template="plotly_white",
        color="store",
        color_discrete_sequence=color_map_stores
    )
    fig_store_profit.update_layout(xaxis_title="Total Revenue ($)", yaxis_title="Store Name")
    st.plotly_chart(fig_store_profit, use_container_width=True)

# ---------------------------
# Section: Client Demographics & Device Usage Analysis (Using Clients Data)
# ---------------------------
elif section == "Client Demographics & Device Usage Analysis":
    st.header("Client Demographics & Device Usage Analysis")
    # Distribution by Country and City (Sunburst Chart)
    location_counts = df_clients.groupby(["country", "city"]).size().reset_index(name="num_clients")
    fig_sunburst = px.sunburst(
        location_counts, 
        path=["country", "city"], 
        values="num_clients",
        title="Client Distribution by Country and City",
        template="plotly_white"
    )
    fig_sunburst.update_layout(showlegend=True, legend_title="City")
    st.plotly_chart(fig_sunburst, use_container_width=True)
    
    # Device Usage Breakdown (Pie Chart)
    device_cols = ["Android", "Iphone", "Desktop"]
    device_usage = df_clients[device_cols].sum().reset_index()
    device_usage.columns = ["Device", "Count"]
    device_usage["Percentage"] = (device_usage["Count"] / device_usage["Count"].sum()) * 100
    fig_pie = px.pie(
        device_usage, 
        names="Device", 
        values="Percentage",
        title="Percentage of Clients Using Each Device",
        template="plotly_white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------
# Section: Transfer Analysis (Using Transfers Data)
# ---------------------------
elif section == "Transfer Analysis":
    st.header("Transfer Data Analysis")
    transfers_sent = df_transfers.groupby("sender_id").agg(total_sent=("amount", "sum")).reset_index()
    transfers_received = df_transfers.groupby("recipient_id").agg(total_received=("amount", "sum")).reset_index()
    transfers_summary = pd.merge(transfers_sent, transfers_received, left_on="sender_id", right_on="recipient_id", how="outer")
    transfers_summary["client_id"] = transfers_summary["sender_id"].combine_first(transfers_summary["recipient_id"])
    transfers_summary.fillna(0, inplace=True)
    fig_transfers = px.bar(
        transfers_summary,
        x="client_id",
        y=["total_sent", "total_received"],
        title="Transfers Sent vs. Received per Client",
        labels={"client_id": "Client ID", "value": "Amount"},
        template="plotly_white"
    )
    st.plotly_chart(fig_transfers, use_container_width=True)

# ---------------------------
# Section: Summary Statistics
# ---------------------------
elif section == "Summary Statistics":
    st.header("Summary Statistics")
    st.subheader("Clients Overview")
    st.dataframe(df_clients.head())
    st.subheader("Transactions Overview")
    st.dataframe(df_transactions.head())
    st.subheader("Transfers Overview")
    st.dataframe(df_transfers.head())
    st.subheader("Promotions Overview")
    st.dataframe(df_promotions.head())

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("© 2025 Venmito Data Engineering Project by José A. Megret Bonilla")