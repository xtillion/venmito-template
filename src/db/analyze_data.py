"""
Utility script to analyze data before loading into the database.

This script helps identify potential issues with data before loading it into PostgreSQL.
"""

import os
import sys
import pandas as pd
import numpy as np

def analyze_integer_columns(df, filename):
    """Analyze integer columns to check if they're in range for PostgreSQL types."""
    print(f"\nAnalyzing {filename}:")
    
    int_max = 2_147_483_647  # PostgreSQL INTEGER max value
    bigint_max = 9_223_372_036_854_775_807  # PostgreSQL BIGINT max value
    
    for col in df.columns:
        # Check if the column has numeric values
        if pd.api.types.is_numeric_dtype(df[col]):
            # Skip float columns
            if df[col].dtype == float:
                continue
                
            try:
                # Get min and max values
                min_val = df[col].min()
                max_val = df[col].max()
                
                # Check for NaN
                if pd.isna(min_val) or pd.isna(max_val):
                    print(f"  - Column '{col}' contains NaN values")
                    continue
                
                print(f"  - Column '{col}': Range [{min_val}, {max_val}]")
                
                # Check if out of INTEGER range
                if max_val > int_max or min_val < -int_max-1:
                    if max_val > bigint_max or min_val < -bigint_max-1:
                        print(f"    WARNING: Values out of BIGINT range!")
                    else:
                        print(f"    NOTE: Values out of INTEGER range but within BIGINT range")
            except Exception as e:
                print(f"  - Error analyzing column '{col}': {str(e)}")

def main():
    data_dir = "data/processed"
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    for file in files:
        try:
            df = pd.read_csv(os.path.join(data_dir, file))
            analyze_integer_columns(df, file)
            
            # Print the first few rows for inspection
            print(f"\nFirst 3 rows of {file}:")
            print(df.head(3))
            
            # Print data types
            print(f"\nData types in {file}:")
            for col, dtype in df.dtypes.items():
                print(f"  - {col}: {dtype}")
                
        except Exception as e:
            print(f"Error analyzing {file}: {str(e)}")

if __name__ == "__main__":
    main()