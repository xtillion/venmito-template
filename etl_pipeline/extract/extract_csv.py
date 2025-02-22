import pandas as pd

# Function to load CSV files
def extract_csv(filepath):
    return pd.read_csv(filepath)