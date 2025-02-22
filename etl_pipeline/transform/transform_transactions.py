import pandas as pd
from etl_pipeline.extract.extract_xml import extract_xml

class Transaction:
    def __init__(self, filepath):
        """Initializes the Transaction class and loads transaction data."""
        self.data = self.load_transactions(filepath)

    def load_transactions(self, filepath):
        """Extracts transactions from XML, converts to a Pandas DataFrame, and ensures JSON serializability."""
        root = extract_xml(filepath)
        transactions_list = []

        for transaction in root.findall('transaction'):
            transaction_data = {}

            transaction_data["transaction_id"] = transaction.get("id", None)  # Ensures ID is captured

            # Extract main transaction details
            for child in transaction:
                if child.tag == "items":
                    # Extract all items as a list
                    items_list = []
                    for item in child.findall("item"):
                        item_data = {sub.tag: sub.text.strip() if sub.text else None for sub in item}

                        # Convert numeric values in items safely
                        numeric_fields = ["price", "price_per_item", "quantity"]
                        for field in numeric_fields:
                            if field in item_data:
                                item_data[field] = pd.to_numeric(item_data[field], errors="coerce")

                                # Ensure values are JSON serializable (convert NumPy types to Python types)
                                if pd.isna(item_data[field]):
                                    item_data[field] = 0
                                else:
                                    item_data[field] = int(item_data[field]) if item_data[field] % 1 == 0 else float(item_data[field])

                        items_list.append(item_data)

                    transaction_data["items"] = items_list
                else:
                    transaction_data[child.tag] = child.text.strip() if child.text else None

            transactions_list.append(transaction_data)

        # Convert to DataFrame
        transactions_df = pd.DataFrame(transactions_list)

        if transactions_df.empty:
            return transactions_df  # Return an empty DataFrame if no data is found

        # Ensure correct data types for top-level transaction fields
        numeric_columns = ['transaction_id', 'amount']
        for col in numeric_columns:
            if col in transactions_df.columns:
                transactions_df[col] = pd.to_numeric(transactions_df[col], errors='coerce').fillna(0)

                # Convert to JSON-friendly types
                transactions_df[col] = transactions_df[col].apply(lambda x: int(x) if x % 1 == 0 else float(x))

        return transactions_df
