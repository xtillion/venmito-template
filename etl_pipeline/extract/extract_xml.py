import xml.etree.ElementTree as ET

# Function to load XML files
def extract_xml(filepath):
    tree = ET.parse(filepath)
    return tree.getroot()