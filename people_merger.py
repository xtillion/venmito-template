import sqlite3
import pandas as pd

def merge_people_dbs(json_db, yml_db, output_db="merged_people.db", output_csv="merged_people.csv"):
    """Merge people data from JSON and YAML databases into a single standardized table."""
    
    # Connect to JSON database and load data
    conn_json = sqlite3.connect(json_db)
    people_json_df = pd.read_sql_query("SELECT * FROM people_json", conn_json)
    conn_json.close()
    
    # Connect to YAML database and load data
    conn_yml = sqlite3.connect(yml_db)
    people_yml_df = pd.read_sql_query("SELECT * FROM people_yml", conn_yml)
    conn_yml.close()
    
    # Standardize column names before merging
    people_json_df.rename(columns={"name": "name", "phone_number": "phone_number", "email": "email", "id": "id"}, inplace=True)
    people_yml_df.rename(columns={"name": "name", "phone_number": "phone_number", "email": "email", "id": "id"}, inplace=True)
    
    # Merge datasets (removing duplicates based on ID, prioritizing JSON data if conflicts exist)
    merged_df = pd.concat([people_json_df, people_yml_df]).drop_duplicates(subset="id", keep="first")
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    merged_df.to_sql('people', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    merged_df.to_csv(output_csv, index=False)
    print(f"Merged people data stored in '{output_db}' and exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    merge_people_dbs("people_json_to_db.db", "people_yml_to_db.db")
