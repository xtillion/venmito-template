import sys
import os
import pandas as pd

# Ensure the helpers module is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.data_viz_funcs import (check_if_international, check_if_bought)


def test_check_if_international():
    row1 = {'sender_country': 'USA', 'reciepient_country': 'Canada'}
    row2 = {'sender_country': 'France', 'reciepient_country': 'France'}

    assert check_if_international(row1) == True, "check_if_international failed: Expected True"
    assert check_if_international(row2) == False, "check_if_international failed: Expected False"

def test_check_if_bought():
    row1 = {
        'items': [{'name': 'Laptop'}, {'name': 'Phone'}],
        'promotion': 'Phone'
    }
    row2 = {
        'items': [{'name': 'Tablet'}, {'name': 'Monitor'}],
        'promotion': 'Headphones'
    }

    assert check_if_bought(row1) == 'Yes', "check_if_bought failed: Expected 'Yes'"
    assert check_if_bought(row2) == 'No', "check_if_bought failed: Expected 'No'"


# Run all tests
if __name__ == "__main__":
    test_check_if_international()
    test_check_if_bought()
    print('Data Viz Functions Tests Passed!')