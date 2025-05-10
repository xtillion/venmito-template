# Function to calculate the age range based on dob
from datetime import date

def get_age_range(dob: date):
    age = (date.today() - dob).days // 365
    if age <= 25:
        return '18-25'
    elif age <= 35:
        return '26-35'
    elif age <= 45:
        return '36-45'
    elif age <= 55:
        return '46-55'
    elif age <= 65:
        return '56-65'
    else:
        return '66+'