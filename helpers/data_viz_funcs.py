import numpy as np
import pandas as pd

def check_if_international(row):
    if row['sender_country'] != row['reciepient_country']:
        return True
    return False

def check_if_bought(row):
    item_names = []
    for item in row['items']:
        item_names.append(item['name'])
    if row['promotion'] in item_names:
        return 'Yes'
    return 'No'