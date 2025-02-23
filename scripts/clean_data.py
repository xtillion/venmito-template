import os
import sys
import pandas as pd

# Ensure script can access other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.load_data import load_all_data

def clean_data():
    """Loads, cleans, and merges all datasets into a single DataFrame."""
    
    # Load data from files
    df_people_json, df_people_yaml, df_transfers, df_promotions, df_transactions = load_all_data()

    # Standardize Column Names
    df_people_json.rename(columns={'id': 'Client_ID', 'first_name': 'First_Name', 'last_name': 'Last_Name', 'telephone': 'Phone'}, inplace=True)
    df_people_yaml.rename(columns={'id': 'Client_ID', 'name': 'Full_Name', 'phone': 'Phone'}, inplace=True)
    df_transfers.rename(columns={'sender_id': 'Client_ID', 'recipient_id': 'Receiver_ID', 'amount': 'Transfer_Amount', 'date': 'Transfer_Date'}, inplace=True)
    df_promotions.rename(columns={'id': 'Promotion_ID', 'telephone': 'Phone'}, inplace=True)
    
    # Handle Missing Values
    df_people_json.fillna("Unknown", inplace=True)
    df_people_yaml.fillna("Unknown", inplace=True)

    # Split Full Name into First and Last Name
    if "Full_Name" in df_people_yaml.columns:
        name_split = df_people_yaml["Full_Name"].str.split(" ", n=1, expand=True)
        df_people_yaml["First_Name"] = name_split[0]
        df_people_yaml["Last_Name"] = name_split[1].fillna("Unknown")
        
    df_people_yaml.drop(columns=['name'], inplace=True, errors='ignore')  # Drop original name column


    df_transfers.fillna({"Transfer_Amount": 0, "Transfer_Date": "Unknown"}, inplace=True)
    df_promotions.fillna({"promotion": "No Promotion", "responded": "No"}, inplace=True)
    df_transactions.fillna({"Amount_USD": 0, "Store": "No Store", "Phone": "Unknown"}, inplace=True)

    # Convert Numeric Columns
    df_transfers["Transfer_Amount"] = pd.to_numeric(df_transfers["Transfer_Amount"], errors='coerce').fillna(0)
    df_transactions["Amount_USD"] = pd.to_numeric(df_transactions["Amount_USD"], errors='coerce').fillna(0)
    df_people_json["Client_ID"] = pd.to_numeric(df_people_json["Client_ID"], errors='coerce')
    df_people_yaml["Client_ID"] = pd.to_numeric(df_people_yaml["Client_ID"], errors='coerce')
    
    # Convert Date Columns
    df_transfers["Transfer_Date"] = pd.to_datetime(df_transfers["Transfer_Date"], errors='coerce')
    df_transfers.dropna(subset=["Transfer_Date"], inplace=True)  # Remove invalid dates
    df_transfers["Transfer_Date"] = df_transfers["Transfer_Date"].dt.strftime("%Y-%m-%d")

    # Remove Duplicates
    df_people_json.drop_duplicates(subset='Client_ID', keep='first', inplace=True)
    df_people_yaml.drop_duplicates(subset='Client_ID', keep='first', inplace=True)
    df_transfers.drop_duplicates(subset=['Client_ID', 'Receiver_ID'], keep='first', inplace=True)
    df_promotions.drop_duplicates(subset='Phone', keep='first', inplace=True)
    df_transactions.drop_duplicates(subset='Transaction_ID', keep='first', inplace=True)
    
    # Merge People Data
    df_people = pd.concat([df_people_json, df_people_yaml], ignore_index=True).drop_duplicates(subset='Client_ID', keep='first')
   
    # Conver Phone Numbers to Strings
    df_people["Phone"] = df_people["Phone"].fillna("Unknown").astype(str).str.strip()
    df_transactions["Phone"] = df_transactions["Phone"].fillna("Unknown").astype(str).str.strip()

    
    # Merge with Transfers, Promotions, Transactions
    df_merged = df_people.merge(df_transfers, on='Client_ID', how='left')
    df_merged = df_merged.merge(df_promotions, on='Phone', how='left')
    df_merged = df_merged.merge(df_transactions, on='Phone', how='left')


    # Drop Unnecessary Columns
    df_merged.drop_duplicates(subset=['Client_ID', 'Transaction_ID'], keep='first', inplace=True)

    # Ensure clients apeear only once if the no have transactions
    df_merged = df_merged.sort_values(by='Amount_USD', ascending=False)
    
    # Ensure Final Cleaning
    df_merged["promotion"].fillna("No Promotion", inplace=True)
    df_merged.fillna({"Store": "No Store", "Amount_USD": 0, "Transfer_Amount": 0}, inplace=True)
    df_merged.dropna(subset=["Client_ID"], inplace=True)  # Ensure all clients have an ID
    
    # Save Cleaned Data
    df_merged.to_csv("data/cleaned_client_data.csv", index=False)
    
    print("\n✅ Cleaned Data Saved Successfully!")
    print(df_merged.head(30))  # Preview first rows
    
    return df_merged  # Return cleaned data

# Function to retrieve cleaned data
def get_cleaned_data():
    """Returns the cleaned dataset as a DataFrame."""
    return pd.read_csv("data/cleaned_client_data.csv")

# Run script directly to clean and save data
if __name__ == "__main__":
    df_cleaned = clean_data()
