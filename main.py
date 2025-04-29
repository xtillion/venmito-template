"""
Main script to run the Venmito data processing pipeline with support for the new schema.
"""

import os
import pandas as pd
from src.data.loader import load_file
from src.data.validator import validate_dataframe
from src.data.processor import process_dataframe
from src.data.merger import MainDataMerger

def main():
    print("Running Venmito data processing pipeline...")
    
    # Create output directory if it doesn't exist
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created/exists at: {os.path.abspath(output_dir)}")
    
    # Step 1: Load data
    print("Loading data...")
    people_json = load_file("data/raw/people.json")
    people_yml = load_file("data/raw/people.yml")
    promotions = load_file("data/raw/promotions.csv")
    transfers = load_file("data/raw/transfers.csv")
    
    # Load transactions from XML file (our XMLLoader class will handle the format)
    try:
        transactions = load_file("data/raw/transactions.xml")
        print(f"Loaded transactions XML data: {len(transactions)} rows")
    except Exception as e:
        print(f"Warning: Could not load transactions data: {e}")
        transactions = pd.DataFrame()
    
    # Step 2: Validate data
    print("Validating data...")
    json_errors = validate_dataframe(people_json, "people")
    yml_errors = validate_dataframe(people_yml, "people")
    promotions_errors = validate_dataframe(promotions, "promotions")
    transfers_errors = validate_dataframe(transfers, "transfers")
    
    # Only validate transactions if data exists
    transactions_errors = []
    if not transactions.empty:
        transactions_errors = validate_dataframe(transactions, "transactions")
    
    # Log validation errors
    for data_type, errors in [
        ("people_json", json_errors),
        ("people_yml", yml_errors),
        ("promotions", promotions_errors),
        ("transfers", transfers_errors),
        ("transactions", transactions_errors)
    ]:
        if errors:
            print(f"Validation errors for {data_type}:")
            for error in errors:
                print(f"  - {error}")
    
    # Step 3: Process data
    print("Processing data...")
    processed_people_json = process_dataframe(people_json, "people")
    processed_people_yml = process_dataframe(people_yml, "people")
    processed_promotions = process_dataframe(promotions, "promotions")
    processed_transfers = process_dataframe(transfers, "transfers")
    
    # Process transactions if data exists
    processed_transactions = {}
    processed_transaction_items = None
    
    if not transactions.empty:
        # The process_dataframe function now returns a dictionary for transactions
        processed_result = process_dataframe(transactions, "transactions")
        
        # Check if we got a dictionary (new format) or DataFrame (old format)
        if isinstance(processed_result, dict):
            processed_transactions = processed_result.get('transactions', pd.DataFrame())
            processed_transaction_items = processed_result.get('transaction_items', pd.DataFrame())
            print(f"Processed transactions data: {len(processed_transactions)} rows")
            print(f"Processed transaction items data: {len(processed_transaction_items)} rows")
        else:
            # Handle the case where process_dataframe still returns a DataFrame
            processed_transactions = processed_result
            print(f"Processed transactions data (old format): {len(processed_transactions)} rows")
    else:
        processed_transactions = pd.DataFrame()
    
    # Step 4: Merge data
    print("Merging data...")
    
    # Print data types for debugging
    print(f"People JSON type: {type(processed_people_json)}")
    print(f"People YAML type: {type(processed_people_yml)}")
    print(f"Promotions type: {type(processed_promotions)}")
    print(f"Transfers type: {type(processed_transfers)}")
    print(f"Transactions type: {type(processed_transactions)}")
    
    merger = MainDataMerger(
        processed_people_json,
        processed_people_yml,
        processed_promotions,
        processed_transfers,
        processed_transactions,
        output_dir=output_dir
    )
    
    try:
        merged_data = merger.merge()
        
        # Ensure all data was properly saved
        for data_name, df in {
            "transfers": processed_transfers,
            "transactions": processed_transactions,
        }.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                file_path = os.path.join(output_dir, f"{data_name}.csv")
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    print(f"Warning: {data_name}.csv was not properly saved, saving it manually")
                    df.to_csv(file_path, index=False)
        
        # Save transaction_items separately if available
        if processed_transaction_items is not None and not processed_transaction_items.empty:
            file_path = os.path.join(output_dir, "transaction_items.csv")
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                print(f"Saving transaction_items.csv manually")
                processed_transaction_items.to_csv(file_path, index=False)
                
            # Also add to merged_data for reporting
            merged_data['transaction_items'] = processed_transaction_items
        
        # Step 5: Report results
        print("\nProcessing complete!")
        print("Summary of merged data:")
        for name, df in merged_data.items():
            if isinstance(df, pd.DataFrame):
                print(f"  - {name}: {df.shape[0]} rows, {df.shape[1]} columns")
            else:
                print(f"  - {name}: {type(df)} (not a DataFrame)")
        
        # List files in output directory
        print(f"\nFiles in output directory ({output_dir}):")
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            print(f"  - {file}: {os.path.getsize(file_path)} bytes")
            
    except Exception as e:
        import traceback
        print(f"Error during merge: {e}")
        traceback.print_exc()
    
    print(f"\nResults saved to {output_dir}")


if __name__ == "__main__":
    main()