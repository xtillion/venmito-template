import sqlite3
import pandas as pd
import json

def create_people_json_table(people_json_file, output_db="people_json_to_db.db", output_csv="people_json_to_db.csv"):
    """Create a database from people.json, converting it into a structured format."""
    
    # Load people data from JSON
    with open(people_json_file, "r", encoding="utf-8") as file:
        people_data = json.load(file)
    
    # Convert to DataFrame
    people_df = pd.json_normalize(people_data)
    
    # Ensure ID is a string with leading zeros
    people_df['id'] = people_df['id'].astype(str).str.zfill(4)
    
    # Standardize column names
    people_df.rename(columns={
        "first_name": "name",
        "location.City": "city",
        "location.Country": "country",
        "telephone": "phone_number",
        "email": "email"
    }, inplace=True)
    
    # Combine first and last names into one column
    people_df["name"] = people_df["name"] + " " + people_df["last_name"]
    
    # Process devices column
    if 'devices' in people_df.columns:
        # Count number of devices
        people_df['device_count'] = people_df['devices'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
        # Convert all device names to lowercase for case-insensitive matching
        people_df['android'] = people_df['devices'].apply(lambda x: 'Yes' if isinstance(x, list) and any(device.lower() == 'android' for device in x) else 'No')
        people_df['iphone'] = people_df['devices'].apply(lambda x: 'Yes' if isinstance(x, list) and any(device.lower() == 'iphone' for device in x) else 'No')
        people_df['desktop'] = people_df['devices'].apply(lambda x: 'Yes' if isinstance(x, list) and any(device.lower() == 'desktop' for device in x) else 'No')
        
        # Drop original devices column
        people_df.drop(columns=['devices'], inplace=True)
    
    # Drop redundant columns
    people_df.drop(columns=["last_name"], inplace=True)
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    people_df.to_sql('people_json', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    people_df.to_csv(output_csv, index=False)
    print(f"People JSON data stored in '{output_db}' and exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    create_people_json_table("data/people.json")