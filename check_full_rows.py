import pandas as pd

def check_full_rows(input_csv="venmito_master.csv", output_csv="full_rows.csv"):
    """Check for rows that have no empty entries and save them to a new CSV file."""
    
    # Load data
    df = pd.read_csv(input_csv)
    
    # Find rows with no missing values
    full_rows_df = df.dropna()
    
    # Save to CSV
    full_rows_df.to_csv(output_csv, index=False)
    
    print(f"Rows with no empty entries saved to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    check_full_rows()
