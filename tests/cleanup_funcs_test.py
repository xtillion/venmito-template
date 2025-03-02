import sys
import os
import pandas as pd

# Ensure the helpers module is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.cleanup_funcs import (
    split_location,
    split_location_str,
    full_name,
    split_name,
    device_list,
    find_person,
    fill_blank_email_or_num,
)
from helpers.data_viz_funcs import (check_if_international, check_if_bought)

def test_functions():
    # Test for split_location
    location = {'City': 'Montreal', 'Country': 'Canada'}
    assert split_location(location) == ["Montreal", "Canada"], "split_location failed"

    # Test for split_location_str
    location_str = "Montreal, Canada"
    assert split_location_str(location_str) == ["Montreal", "Canada"], "split_location_str failed"

    # Test for full_name
    assert full_name("John", "Doe") == "John Doe", "full_name failed"

    # Test for split_name
    assert split_name("John Doe") == ["John", "Doe"], "split_name failed"

    # Test for device_list
    devices = ['Android', 'Iphone', 'Desktop', 'Android', 'Iphone']
    assert device_list(devices) == [2, 1, 2], "device_list failed"

    # Mock DataFrame for `find_person` and `fill_blank_email_or_num`
    data = {
        'id': [1, 2], 
        'client_email': ['john.doe@example.com', 'jane.doe@example.com'],
        'telephone': ['123-456-7890', '234-567-8901'],
        'first_name': ['John', 'Jane'],
        'last_name': ['Doe', 'Doe'],
        'email': ['john.doe@example.com', 'jane.doe@example.com'],
        'phone': ['123-456-7890', '234-567-8901']
    }
    all_people = pd.DataFrame(data)

    # Test for find_person
    assert find_person('client_email', 'john.doe@example.com', all_people, 'first_name') == "John", "find_person failed for email"
    assert find_person('telephone', '234-567-8901', all_people, 'email') == "jane.doe@example.com", "find_person failed for phone"
    
    row_1 = {'id': 1, 'client_email': pd.NA, 'telephone': '123-456-7890'}
    assert fill_blank_email_or_num(row_1, all_people) == ["John", "Doe", "john.doe@example.com", "123-456-7890"], "fill_blank_email_or_num failed for missing email"

    row_2 = {'id': 2, 'client_email': 'jane.doe@example.com', 'telephone': pd.NA}
    assert fill_blank_email_or_num(row_2, all_people) == ["Jane", "Doe", "jane.doe@example.com", "234-567-8901"], "fill_blank_email_or_num failed for missing phone"

    print("All tests passed successfully!")


# Run all tests
if __name__ == "__main__":
    test_functions()
    print('Cleanup Functions Test Passed!')
