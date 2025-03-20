# src/db/analyze_promotions.py
import pandas as pd
import os

def analyze_promotions():
    """Analyze promotions data to identify issues."""
    file_path = os.path.join('data/processed', 'promotions.csv')
    
    if not os.path.exists(file_path):
        print(f"Promotions file not found: {file_path}")
        return
    
    try:
        # Load with explicit dtype to prevent automatic type inference
        df = pd.read_csv(file_path)
        
        print(f"Loaded {len(df)} rows from {file_path}")
        print(f"\nFirst 5 rows:")
        print(df.head(5).to_string())
        
        print(f"\nPromotion ID data type: {df['promotion_id'].dtype}")
        print(f"Promotion ID min: {df['promotion_id'].min()}")
        print(f"Promotion ID max: {df['promotion_id'].max()}")
        
        # Check if there are any promotion_ids that would exceed the INT range
        int_max = 2_147_483_647
        large_ids = df[df['promotion_id'] > int_max]
        
        if not large_ids.empty:
            print(f"\nFound {len(large_ids)} promotion_ids exceeding INT range:")
            print(large_ids.head().to_string())
        else:
            print("\nNo promotion_ids exceed INT range.")
            
        # Look for other potential issues
        print(f"\nUser ID data type: {df['user_id'].dtype}")
        print(f"Missing user_ids: {df['user_id'].isna().sum()}")
        
        # Check for duplicate promotion_ids
        duplicates = df[df.duplicated(subset=['promotion_id'], keep=False)]
        if not duplicates.empty:
            print(f"\nFound {len(duplicates)} duplicate promotion_ids:")
            print(duplicates.to_string())
        else:
            print("\nNo duplicate promotion_ids found.")
            
        # Check for non-numeric promotion_ids
        try:
            pd.to_numeric(df['promotion_id'])
            print("\nAll promotion_ids are numeric.")
        except ValueError:
            print("\nSome promotion_ids are not numeric!")
            print(df[pd.to_numeric(df['promotion_id'], errors='coerce').isna()].head())
        
    except Exception as e:
        print(f"Error analyzing promotions data: {str(e)}")

if __name__ == "__main__":
    analyze_promotions()