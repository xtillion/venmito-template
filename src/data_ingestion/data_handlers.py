from database import engine
import pandas as pd
from sqlalchemy.sql import text

def store_people_and_devices(df):
    """
    Processes a DataFrame containing people data and their associated devices,
    handling differences between JSON and YAML formats, and stores the data into
    the 'people' and 'devices' tables in the database.
    """
    # Handle different formats (JSON vs YAML)
    if "location" in df.columns:
        # JSON format: Extract city and country from location
        df["city"] = df["location"].apply(lambda loc: loc.get("City"))
        df["country"] = df["location"].apply(lambda loc: loc.get("Country"))
        df = df.drop(columns=["location"])  # Remove original location field

    elif "city" in df.columns and "country" not in df.columns:
        # YAML format: split 'city' into 'city' and 'country'
        df[["city", "country"]] = df["city"].str.split(", ", expand=True)

    # Handle name differences (JSON vs YAML)
    if "name" in df.columns:  # YAML uses "name"
        df["first_name"] = df["name"].apply(lambda x: x.split(" ", 1)[0])
        df["last_name"] = df["name"].apply(lambda x: x.split(" ", 1)[1])
        df = df.drop(columns=["name"])  # Remove original name field

    # Standardize "telephone" field (YAML uses "phone")
    if "phone" in df.columns and "telephone" not in df.columns:
        df["telephone"] = df["phone"]
        df = df.drop(columns=["phone"])  # Drop original phone field

    # Process device ownership correctly (if applicable)
    device_columns = ["Android", "Desktop", "Iphone"]
    if any(col in df.columns for col in device_columns):
        df["devices"] = df.apply(lambda row: [col for col in device_columns if row.get(col, 0) == 1], axis=1)
        df = df.drop(columns=[col for col in device_columns if col in df.columns])  # Drop only existing device columns
    else:
        df["devices"] = [[]] * len(df)  # Default to an empty list if no device columns exist

    # Remove duplicate IDs
    people_data = df.drop_duplicates(subset=["id"])

    with engine.begin() as conn:
        # Use UPSERT (ON CONFLICT DO UPDATE) instead of dropping the table
        for _, row in people_data.iterrows():
            conn.execute(
                text("""
                    INSERT INTO people (id, first_name, last_name, telephone, email, city, country) 
                    VALUES (:id, :first_name, :last_name, :telephone, :email, :city, :country)
                    ON CONFLICT (id) DO UPDATE SET 
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        telephone = EXCLUDED.telephone,
                        email = EXCLUDED.email,
                        city = EXCLUDED.city,
                        country = EXCLUDED.country
                """),
                {
                    "id": row["id"],
                    "first_name": row.get("first_name", ""),  # Handle missing fields
                    "last_name": row.get("last_name", ""),
                    "telephone": row.get("telephone", ""),  # Ensure 'telephone' always exists
                    "email": row["email"],
                    "city": row["city"],
                    "country": row["country"]
                }
            )

        # Insert devices separately, avoiding duplicates
        for _, row in df.iterrows():
            person_id = row["id"]
            devices = row["devices"]

            for device in devices:
                conn.execute(
                    text("""
                        INSERT INTO devices (person_id, device_type) 
                        VALUES (:person_id, :device) 
                        ON CONFLICT DO NOTHING
                    """),
                    {"person_id": person_id, "device": device}
                )

def store_transfers(df):
    """
    Handles and stores transfers, ensuring correct column names.
    """
    expected_columns = {"sender_id", "recipient_id", "amount", "date"}
    
    # Handle column name mismatches (e.g., 'receiver_id' vs. 'recipient_id')
    if "receiver_id" in df.columns and "recipient_id" not in df.columns:
        df.rename(columns={"receiver_id": "recipient_id"}, inplace=True)

    # Ensure required columns exist
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in transfers dataset: {missing_columns}")

    # Convert date to correct format
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df.to_sql("transfers", engine, if_exists="append", index=False, method="multi")

def store_transactions(df_transactions, df_items):
    """
    Stores transaction data in the database.
    Ensures transactions are inserted before transaction items to maintain referential integrity.
    """

    # Remove duplicates before insertion
    df_transactions.drop_duplicates(subset=["transaction_id"], inplace=True)

    with engine.begin() as conn:
        # Step 1: Insert Transactions First
        df_transactions.to_sql("transactions", conn, if_exists="append", index=False, method="multi")

        # Step 2: Ensure only valid transaction IDs exist before inserting transaction items
        valid_transaction_ids = set(df_transactions["transaction_id"])

        # Filter transaction items to only include those that reference valid transactions
        df_items = df_items[df_items["transaction_id"].isin(valid_transaction_ids)]

        if not df_items.empty:
            df_items.to_sql("transaction_items", conn, if_exists="append", index=False, method="multi")

def store_promotions(df):
    """
    Process and store promotions data without any renaming or mapping.
    
    Assumes the CSV file columns are exactly:
      id, client_email, telephone, promotion, responded

    It retains only these columns, drops duplicates, and inserts the data as-is.
    """
    # Keep only the expected columns
    expected = {"id", "client_email", "telephone", "promotion", "responded"}
    df = df[[col for col in df.columns if col in expected]]
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Insert the data into the promotions table
    df.to_sql("promotions", engine, if_exists="append", index=False, method="multi")
