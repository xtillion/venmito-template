import pandas as pd
from etl_pipeline.transform.transform_transactions import Transaction

class TransactionsAggregator:
    def __init__(self):
        self.df = Transaction('data/transactions.xml').data

    def get_all_transactions(self):
        return self.df

    def get_best_selling_item(self):
        """Find the best-selling item based on total quantity sold."""
        items_list = []
        for transaction in self.df["items"].dropna():
            for item in transaction:
                items_list.append(item)
        items_df = pd.DataFrame(items_list)
        if items_df.empty:
            return None
        grouped = items_df.groupby("item")["quantity"].sum()
        best_item = grouped.idxmax()
        return {"item": best_item, "quantity": int(grouped.max())}

    def get_store_with_most_items_sold(self):
        """Find the store that sold the highest total quantity of items."""
        if not {"store", "items"}.issubset(self.df.columns):
            return None
        store_sales = {}
        for _, row in self.df.dropna(subset=["store", "items"]).iterrows():
            store = row["store"]
            if not isinstance(row["items"], list):
                continue
            total = sum(item.get("quantity", 0) for item in row["items"])
            store_sales[store] = store_sales.get(store, 0) + total
        if not store_sales:
            return None
        best_store = max(store_sales, key=store_sales.get)
        return {"store": best_store, "total_items_sold": int(store_sales[best_store])}

    def get_most_profitable_store(self):
        """Find the store with the highest total revenue."""
        if not {"store", "items"}.issubset(self.df.columns):
            return None
        store_revenue = {}
        for _, row in self.df.dropna(subset=["store", "items"]).iterrows():
            store = row["store"]
            if not isinstance(row["items"], list):
                continue
            revenue = sum(item.get("price", 0) for item in row["items"])
            store_revenue[store] = store_revenue.get(store, 0) + revenue
        if not store_revenue:
            return None
        best_store = max(store_revenue, key=store_revenue.get)
        return {"store": best_store, "revenue": float(store_revenue[best_store])}

    def get_profitability_of_items(self):
        """Calculate total revenue per item."""
        if "items" not in self.df.columns:
            return None
        item_revenue = {}
        for items in self.df["items"].dropna():
            if not isinstance(items, list):
                continue
            for item in items:
                name = item.get("item")
                revenue = item.get("price", 0)
                if name:
                    item_revenue[name] = item_revenue.get(name, 0) + revenue
        if not item_revenue:
            return None
        return {name: float(revenue) for name, revenue in item_revenue.items()}

    def get_items_sold_by_store(self):
        """List all items sold per store with quantity and revenue."""
        if not {"store", "items"}.issubset(self.df.columns):
            return None
        store_sales = {}
        for _, row in self.df.dropna(subset=["store", "items"]).iterrows():
            store = row["store"]
            if not isinstance(row["items"], list):
                continue
            store_sales.setdefault(store, {})
            for item in row["items"]:
                name = item.get("item")
                quantity = item.get("quantity", 0)
                revenue = item.get("price", 0)
                if name:
                    if name not in store_sales[store]:
                        store_sales[store][name] = {"quantity": 0, "revenue": 0.0}
                    store_sales[store][name]["quantity"] += quantity
                    store_sales[store][name]["revenue"] += revenue
        result = []
        for store, items in store_sales.items():
            result.append({
                "store": store,
                "items_sold": [
                    {"item_name": name, "quantity": data["quantity"], "revenue": float(data["revenue"])}
                    for name, data in items.items()
                ]
            })
        return result
    
    def get_transactions_by_item_name(self, item_name):
        """Retrieve transactions that contain a specific item name."""
        
        if "items" not in self.df.columns:
            return None  # Ensure the column exists

        filtered_transactions = []

        # Iterate through each transaction
        for _, row in self.df.iterrows():
            if not isinstance(row["items"], list):
                continue  # Skip invalid entries
            
            # Filter items that match the given item_name
            matching_items = [item for item in row["items"] if item.get("item") == item_name]

            if matching_items:
                filtered_transactions.append({
                    "transaction_id": row["transaction_id"],
                    "store": row["store"],
                    "phone": row["phone"],
                    "items": matching_items
                })

        return filtered_transactions if filtered_transactions else None
