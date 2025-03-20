"""
Main script to run the Venmito data processing pipeline.
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
    
    # Step 1: Load data
    print("Loading data...")
    people_json = load_file("data/raw/people.json")
    people_yml = load_file("data/raw/people.yml")
    promotions = load_file("data/raw/promotions.csv")
    transfers = load_file("data/raw/transfers.csv")
    
    # Step 2: Validate data
    print("Validating data...")
    json_errors = validate_dataframe(people_json, "people")
    yml_errors = validate_dataframe(people_yml, "people")
    promotions_errors = validate_dataframe(promotions, "promotions")
    transfers_errors = validate_dataframe(transfers, "transfers")
    
    # Log validation errors
    for data_type, errors in [
        ("people_json", json_errors),
        ("people_yml", yml_errors),
        ("promotions", promotions_errors),
        ("transfers", transfers_errors)
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
    
    # Step 4: Merge data
    print("Merging data...")
    merger = MainDataMerger(
        processed_people_json,
        processed_people_yml,
        processed_promotions,
        processed_transfers,
        output_dir=output_dir
    )
    merged_data = merger.merge()
    
    # Check for merge errors
    merge_errors = merger.get_errors()
    if merge_errors:
        print("Merge errors:")
        for error in merge_errors:
            print(f"  - {error}")
    
    # Step 5: Report results
    print("\nProcessing complete!")
    print("Summary of merged data:")
    for name, df in merged_data.items():
        print(f"  - {name}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    print(f"\nResults saved to {output_dir}")
    
    return merged_data

if __name__ == "__main__":
    main()