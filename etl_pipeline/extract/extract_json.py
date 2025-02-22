import json

# Function to load JSON files
def extract_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)