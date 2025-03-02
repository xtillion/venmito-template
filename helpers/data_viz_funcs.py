import numpy as np
import pandas as pd

def check_if_international(row):
    if row['sender_country'] != row['reciepient_country']:
        return True
    return False
