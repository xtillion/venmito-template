import json
import yaml
import sqlite3
import pandas as pd

def load_people_json(json_file):
    """Load people.json and structure it as a DataFrame."""
    with open(json_file, 'r', encoding='utf-8') as f:
        people_json = json.load(f)
    
    data = []
    for person in people_json:
        data.append({
            'id': person['id'],
            'first_name': person['first_name'],
            'last_name': person['last_name'],
            'full_name': f"{person['first_name']} {person['last_name']}",
            'email': person['email'],
            'phone': person['telephone'],
            'city': person['location']['City'],
            'country': person['location']['Country'],
            'android': 1 if 'Android' in person['devices'] else 0,
            'desktop': 1 if 'Desktop' in person['devices'] else 0,
            'iphone': 1 if 'iPhone' in person['devices'] else 0,
            'source': 'json'
        })
    
    return pd.DataFrame(data)

def load_people_yml(yml_file):
    """Load people.yml and structure it as a DataFrame."""
    with open(yml_file, 'r', encoding='utf-8') as f:
        people_yml = yaml.safe_load(f)
    
    data = []
    for person in people_yml:
        city_country = person['city'].split(', ')
        city, country = city_country if len(city_country) == 2 else (person['city'], '')
        data.append({
            'id': str(person['id']).zfill(4),  # Ensuring ID format matches JSON
            'full_name': person['name'],
            'email': person['email'],
            'phone': person['phone'],
            'city': city,
            'country': country,
            'android': person['Android'],
            'desktop': person['Desktop'],
            'iphone': person['Iphone'],
            'source': 'yml'
        })
    
    return pd.DataFrame(data)

def merge_people(json_file, yml_file):
    """Merge people.json and people.yml into a single dataset."""
    df_json = load_people_json(json_file)
    df_yml = load_people_yml(yml_file)
    
    # Merge on ID, Email, and Phone to prevent duplication
    merged_df = pd.merge(df_json, df_yml, on=['id', 'email', 'phone'], how='outer', suffixes=('_json', '_yml'))
    
    # Resolve conflicts by prioritizing JSON data
    merged_df['full_name'] = merged_df['full_name_json'].combine_first(merged_df['full_name_yml'])
    merged_df['city'] = merged_df['city_json'].combine_first(merged_df['city_yml'])
    merged_df['country'] = merged_df['country_json'].combine_first(merged_df['country_yml'])
    merged_df['android'] = merged_df[['android_json', 'android_yml']].max(axis=1)
    merged_df['desktop'] = merged_df[['desktop_json', 'desktop_yml']].max(axis=1)
    merged_df['iphone'] = merged_df[['iphone_json', 'iphone_yml']].max(axis=1)
    
    # Keep a column indicating where the record was originally found
    merged_df['source'] = merged_df.apply(lambda row: 'both' if pd.notna(row['source_json']) and pd.notna(row['source_yml']) else ('json' if pd.notna(row['source_json']) else 'yml'), axis=1)
    
    # Select relevant columns
    final_df = merged_df[['id', 'full_name', 'email', 'phone', 'city', 'country', 'android', 'desktop', 'iphone', 'source']]
    
    return final_df

def create_database(db_name, json_file, yml_file):
    """Create an SQLite database and store the unified people table."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create the people table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY,
            full_name TEXT,
            email TEXT UNIQUE,
            phone TEXT UNIQUE,
            city TEXT,
            country TEXT,
            android INTEGER,
            desktop INTEGER,
            iphone INTEGER,
            source TEXT
        )
    ''')
    
    # Merge data
    final_df = merge_people(json_file, yml_file)
    
    # Insert data into the database
    final_df.to_sql('people', conn, if_exists='replace', index=False)
    print(f"Database '{db_name}' created and people table populated.")
    
    conn.commit()
    conn.close()
    
# Example usage:
if __name__ == "__main__":
    create_database('venmito.db', 'data/people.json', 'data/people.yml')
