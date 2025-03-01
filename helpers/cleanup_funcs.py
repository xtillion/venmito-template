## spliting city country 

#Example of location: {'City': 'Montreal', 'Country': 'Canada'}

def split_location(location:str):
    return [location['City'], location['Country']]

def split_location_str(location:str):
    return location.split(", ")

def full_name(first_name:str, last_name:str):
    return first_name + " " + last_name

def split_name(name:str):
    return name.split(" ")

# ['Android', 'Iphone']
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