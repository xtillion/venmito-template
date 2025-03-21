#!/usr/bin/env python
# isolation_test.py - Test script to isolate promotions loading issue

import os
import logging
import pandas as pd
from dotenv import load_dotenv

from src.db.db import Database, init_db_from_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def isolate_promotion_issue():
    """Methodically test promotions loading to isolate the issue."""
    try:
        # Initialize database connection
        init_db_from_env()
        
        # Load the file
        file_path = os.path.join('data/processed', 'promotions.csv')
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows from {file_path}")
        
        # Print data types
        logger.info(f"Data types: {df.dtypes}")
        
        # Check for null values
        null_counts = df.isnull().sum()
        logger.info(f"Null value counts: {null_counts}")
        
        # Print a few sample rows
        logger.info("Sample rows:")
        for idx, row in df.head(3).iterrows():
            logger.info(f"Row {idx}: {row.to_dict()}")
        
        # Prepare data - handle nulls and convert types
        df_copy = df.copy()
        
        # Convert promotion_id to Python int
        df_copy['promotion_id'] = df_copy['promotion_id'].astype(int)
        
        # For user_id, we'll leave NaN values as is for now
        # We'll handle them individually during insertion
        
        # Make sure strings are actual strings
        for col in ['promotion', 'responded', 'promotion_date']:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype(str)
        
        # Try inserting one row at a time
        logger.info("Starting row-by-row insert test...")
        
        # Define columns and query
        columns = ['promotion_id', 'promotion', 'responded']
        if 'promotion_date' in df_copy.columns:
            columns.append('date')  # We'll map promotion_date to date
        if 'user_id' in df_copy.columns:
            columns.append('user_id')  # Add user_id if present
        
        placeholders = ', '.join(['%s'] * len(columns))
        column_str = ', '.join(columns)
        
        query = f"""
            INSERT INTO promotions ({column_str})
            VALUES ({placeholders})
            ON CONFLICT (promotion_id) DO NOTHING
        """
        
        inserted = 0
        errors = 0
        error_details = []
        
        # Try to insert 5 rows to find the issue
        for idx, row in df_copy.head(5).iterrows():
            try:
                # Create parameters tuple with explicit type conversion
                params = []
                for col in columns:
                    if col == 'date' and 'promotion_date' in df_copy.columns:
                        # Map promotion_date to date
                        val = row['promotion_date']
                    else:
                        val = row[col] if col in row else None
                    
                    if col == 'promotion_id':
                        # Make sure promotion_id is an integer
                        params.append(int(val))
                    elif col == 'user_id':
                        # Handle user_id conversion - can be null
                        if pd.isna(val):
                            params.append(None)
                        else:
                            params.append(int(val))
                    else:
                        # Everything else is treated as is
                        params.append(val)
                
                # Log the parameters
                logger.info(f"Row {idx} parameters: {params}")
                
                # Execute the query
                Database.execute_query(query, tuple(params), commit=True)
                inserted += 1
                logger.info(f"Successfully inserted row {idx}")
            except Exception as e:
                errors += 1
                error_info = f"Error on row {idx}: {str(e)}"
                error_details.append(error_info)
                logger.error(error_info)
                logger.error(f"Row data: {row.to_dict()}")
        
        logger.info(f"Insert test completed. Inserted: {inserted}, Errors: {errors}")
        if errors > 0:
            logger.info("Error details:")
            for detail in error_details:
                logger.info(detail)
        
    except Exception as e:
        logger.error(f"Error during isolation test: {str(e)}")
    finally:
        Database.close()

if __name__ == "__main__":
    load_dotenv('.env')
    isolate_promotion_issue()