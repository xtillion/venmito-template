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
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory created/exists at: {os.path.abspath(output_dir)}")
        
        # Test write access
        test_file = os.path.join(output_dir, "test_write.txt")
        with open(test_file, 'w') as f:
            f.write("Test write access")
        print(f"Successfully wrote test file to: {test_file}")
        
        # Clean up the test file
        os.remove(test_file)
        print("Test file removed")
    except Exception as e:
        print(f"Error with output directory: {e}")
    
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
    
    # Debug: Check datatypes before merge
    print(f"People JSON type: {type(processed_people_json)}")
    print(f"People YAML type: {type(processed_people_yml)}")
    print(f"Promotions type: {type(processed_promotions)}")
    print(f"Transfers type: {type(processed_transfers)}")
    
    try:
        merged_data = merger.merge()
        
        # Step 5: Report results
        print("\nProcessing complete!")
        print("Summary of merged data:")
        for name, df in merged_data.items():
            print(f"  - {name}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Debug: Check output directory
        print(f"\nFiles in output directory ({output_dir}):")
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                print(f"  - {file}")
        else:
            print(f"  Directory {output_dir} does not exist")
            
    except Exception as e:
        import traceback
        print(f"Error during merge: {e}")
        traceback.print_exc()
    
    print(f"\nResults saved to {output_dir}")
    
    # After you get the merged_data dictionary
    if 'people' in merged_data:
        try:
            print("\nTesting direct save of people data...")
            people_df = merged_data['people']
            save_path = os.path.join(output_dir, "people_direct.csv")
            people_df.to_csv(save_path, index=False)
            print(f"Successfully saved people DataFrame to: {save_path}")
            
            # Verify the file exists
            if os.path.exists(save_path):
                print(f"People file exists: {save_path}")
            else:
                print(f"People file does not exist: {save_path}")
        except Exception as e:
            print(f"Error saving people DataFrame: {e}")

    # Test direct save
    try:
        print("\nTesting direct save...")
        test_df = pd.DataFrame({'test': [1, 2, 3]})
        save_path = os.path.join(output_dir, "test_save.csv")
        test_df.to_csv(save_path, index=False)
        print(f"Successfully saved test DataFrame to: {save_path}")
        
        # Verify the file exists
        if os.path.exists(save_path):
            print(f"File exists: {save_path}")
        else:
            print(f"File does not exist: {save_path}")
    except Exception as e:
        print(f"Error saving test DataFrame: {e}")


if __name__ == "__main__":
    main()