import yaml

# Function to load YAML files
def extract_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)