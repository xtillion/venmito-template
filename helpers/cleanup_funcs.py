import pandas as pd
import numpy as np
## spliting city country 

#Example of location: {'City': 'Montreal', 'Country': 'Canada'} to ["Montreal", "Canada"]
def split_location(location:str):
    return [location['City'], location['Country']]

#Example of location: "Montreal, Canada" to ["Montreal", "Canada"]
def split_location_str(location:str):
    return location.split(", ")

#Example of first_name: "John" and last_name: "Doe" into "John Doe"
def full_name(first_name:str, last_name:str):
    return first_name + " " + last_name

#Example of name: "John Doe" into John and Doe
def split_name(name:str):
    return name.split(" ")

# should return a list of the devices used by the user 
def device_list(devices: list):
    android = 0
    iphone = 0
    desktop = 0
    for device in devices:
        if device == 'Android':
            android += 1
        elif device == 'Iphone':
            iphone += 1
        elif device == 'Desktop':
            desktop += 1
        else:
            print("Unknown Device")
    return [android, desktop, iphone]

## should detect if missing phone or email and fill the other values
def find_person(item_col,item_value,all_people,specific_item):
    person = all_people.loc[all_people[item_col] == item_value].dropna()
    if specific_item != None:
        return person.iloc[0][specific_item]
    return all_people.loc[all_people[item_col] == item_value].dropna()
 
def fill_blank_email_or_num(row, all_people):
    email, phone = row['client_email'], row['telephone']
    if pd.isna(email) and pd.isna(phone):
        print(f"Both email and phone are missing for row {row['id']}")
        return None  
    key, value = ('phone', phone) if pd.isna(email) else ('email', email)
    person_info = find_person(key, value, all_people,None)
    if person_info.empty:
        return None  
    first_name, last_name, email, phone = person_info.iloc[0][['first_name', 'last_name', 'email', 'phone']]
    return [first_name, last_name, email, phone]
