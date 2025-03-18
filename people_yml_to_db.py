import sqlite3
import pandas as pd
import yaml

def create_people_yml_table(people_yml_file, output_db="people_yml_to_db.db", output_csv="people_yml_to_db.csv"):
    """Create a database from people.yml, converting it into a structured format."""
    
    # Load people data from YAML
    with open(people_yml_file, "r", encoding="utf-8") as file:
        people_data = yaml.safe_load(file)
    
    # Convert to DataFrame
    people_df = pd.DataFrame(people_data)
    
    # Ensure ID is a string with leading zeros
    people_df['id'] = people_df['id'].astype(str).str.zfill(4)
    
    # Standardize column names
    people_df.rename(columns={
        "name": "name",
        "city": "city_country",
        "phone": "phone_number",
        "email": "email"
    }, inplace=True)
    
    # Split city and country into separate columns
    people_df[['city', 'country']] = people_df['city_country'].str.split(', ', expand=True)
    people_df.drop(columns=['city_country'], inplace=True)
    
    # Convert binary device indicators (1/0) into Yes/No values
    people_df['android'] = people_df['Android'].apply(lambda x: 'Yes' if x == 1 else 'No')
    people_df['iphone'] = people_df['Iphone'].apply(lambda x: 'Yes' if x == 1 else 'No')
    people_df['desktop'] = people_df['Desktop'].apply(lambda x: 'Yes' if x == 1 else 'No')
    
    # Drop original binary columns
    people_df.drop(columns=['Android', 'Iphone', 'Desktop'], inplace=True)
    
    # Save to new database
    conn = sqlite3.connect(output_db)
    people_df.to_sql('people_yml', conn, if_exists='replace', index=False)
    conn.close()
    
    # Export to CSV for easy viewing
    people_df.to_csv(output_csv, index=False)
    print(f"People YAML data stored in '{output_db}' and exported to '{output_csv}'.")

# Example usage
if __name__ == "__main__":
    create_people_yml_table("data/people.yml")
