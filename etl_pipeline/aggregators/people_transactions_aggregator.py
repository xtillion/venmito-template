import pandas as pd
from etl_pipeline.transform.transform_people import People
from etl_pipeline.transform.transform_transactions import Transaction

class PeopleTransactionsAggregator:
    def __init__(self):
        self.people_df = People('data/people.json', 'data/people.yml').data
        self.transactions_df = Transaction('data/transactions.xml').data

    def get_people_with_transactions(self):
        """Returns only people who have made transactions, merging transaction and people data."""

        transactions_df = self.transactions_df

        # Ensure necessary columns exist
        if not {"telephone", "person_id"}.issubset(self.people_df.columns) or not {"phone", "transaction_id", "items", "store"}.issubset(transactions_df.columns):
            return None  # Missing required columns

        # Standardize column name for merging
        transactions_df = transactions_df.rename(columns={"phone": "telephone"})

        # Expand transaction items into structured format
        transaction_records = []
        for _, row in transactions_df.iterrows():
            if isinstance(row["items"], list):  # Ensure "items" is a list
                transaction_records.append({
                    "telephone": row["telephone"],
                    "transaction": {
                        "transaction_id": row["transaction_id"],
                        "store": row["store"],
                        "items": [
                            {
                                "item_name": item["item"],
                                "quantity": item["quantity"],
                                "price_per_item": item["price_per_item"],
                                "total_price": item["price"]
                            }
                            for item in row["items"]
                        ]
                    }
                })

        transactions_expanded_df = pd.DataFrame(transaction_records)

        # Merge transactions with people (inner join = only keep people with transactions)
        merged_df = pd.merge(self.people_df, transactions_expanded_df, on="telephone", how="inner")

        # Group transactions per person
        merged_grouped = (
            merged_df.groupby(["person_id", "first_name", "last_name", "email", "telephone", "city", "country"], dropna=False)
            .agg(
                transactions=("transaction", lambda x: list(x.dropna()))  # Keep full transaction details
            )
            .reset_index()
        )

        # Convert to structured JSON-compatible output
        return merged_grouped

    def get_people_by_store(self, store_name):
        """Retrieves people who made transactions at a specific store, including their specific transaction details."""
        
        # Get people with transactions
        people_transactions = self.get_people_with_transactions()

        if people_transactions is None or people_transactions.empty:
            return None  # No transaction data available

        # Check if necessary columns exist
        if "telephone" not in people_transactions.columns:
            raise KeyError("Column 'telephone' not found in people_transactions. Ensure merge was done correctly.")

        # Filter people who have transactions at the given store
        filtered_people = []

        for _, person in people_transactions.iterrows():
            # Get only the transactions related to the specified store for this person
            store_transactions = [
                {
                    "transaction_id": t.get("transaction_id"),
                    "store": t.get("store"),
                    "items": t.get("items")  # Keep the items inside the transaction
                }
                for t in person["transactions"]
                if t.get("store") == store_name
            ]

            if store_transactions:  # Only include the person if they have transactions at this store
                filtered_people.append({
                    "person_id": person.get("person_id"),
                    "first_name": person.get("first_name"),
                    "last_name": person.get("last_name"),
                    "email": person.get("email"),
                    "telephone": person.get("telephone"),
                    "city": person.get("city"),
                    "country": person.get("country"),
                    "transactions": store_transactions  # Attach only relevant transactions
                })

        return {"store": store_name, "customers": filtered_people} if filtered_people else None
    
    def get_people_with_transaction_by_item_name(self, item_name):
        """Retrieves people who made transactions that included a specific item, along with transaction details."""
        
        # Get people with transactions
        people_transactions = self.get_people_with_transactions()

        if people_transactions is None or people_transactions.empty:
            return None  # No transaction data available

        # Check if necessary columns exist
        if "transactions" not in people_transactions.columns:
            raise KeyError("Column 'transactions' not found in people_transactions. Ensure merge was done correctly.")

        # Filter people who have transactions containing the specified item
        filtered_people = []

        for _, person in people_transactions.iterrows():
            # Get only the transactions that contain the specified item for this person
            relevant_transactions = []

            for transaction in person["transactions"]:
                matching_items = []

                for item in transaction.get("items", []):
                    if item.get("item_name") == item_name:
                        matching_items.append({
                            "item_name": item.get("item_name"),
                            "quantity": item.get("quantity"),
                            "price_per_item": item.get("price_per_item"),
                            "total_price": item.get("total_price")
                        })

                if matching_items:  # Only add transactions that include the item
                    relevant_transactions.append({
                        "transaction_id": transaction.get("transaction_id"),
                        "store": transaction.get("store"),
                        "items": matching_items
                    })

            if relevant_transactions:  # Only include the person if they have transactions containing the item
                filtered_people.append({
                    "person_id": person.get("person_id"),
                    "first_name": person.get("first_name"),
                    "last_name": person.get("last_name"),
                    "email": person.get("email"),
                    "telephone": person.get("telephone"),
                    "city": person.get("city"),
                    "country": person.get("country"),
                    "transactions": relevant_transactions  # Attach only relevant transactions
                })

        return {"item": item_name, "customers": filtered_people} if filtered_people else None

    
