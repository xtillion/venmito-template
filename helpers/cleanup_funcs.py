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
def fill_blank_email_or_num(row,all_people):
    email = row['client_email']
    telephone = row['telephone']
    #if email missing but phone is present
    if pd.isna(email) and not pd.isna(telephone):
        email_found = all_people.loc[all_people['phone'] == telephone, 'email'].dropna().tolist()[0]
        return [email_found, telephone]
    elif pd.isna(telephone) and not pd.isna(email):
        phone_found = all_people.loc[all_people['email'] == email, 'phone'].dropna().tolist()[0]
        return [email, phone_found]
    elif pd.isna(email) and pd.isna(telephone):
        print(f'Both email and phone are missing for this row {row['id']}')
    # both present, dont do anything
    return [email, telephone]