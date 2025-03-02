import numpy as np
import pandas as pd
from helpers.data_parser import data_parser
import helpers.cleanup_funcs as cleanup
import xml.etree.ElementTree as ET

### Pre Cleanup  Discoveries ###

# print(ppl_json['id'].isin(ppl_yml['id'])) #reveals discrepancies in the ids
# ppl_json.isna().sum() = results show that there are no missing values

#Defining Functions for later processing
def cleanup_items_xml(data_path):
    tree = ET.parse(data_path)
    root = tree.getroot()
    items = []
    for child in root:
        for next in child:
            if next.tag == 'items':
                transaction_items = []
                for item in next:
                    item_info = {}
                    for i in item:
                        if i.tag == 'item':
                            item_info['name'] = i.text
                        elif i.tag == 'price':
                            item_info['total'] = i.text
                        elif i.tag == 'price_per_item':
                            item_info['price_per_item'] = i.text
                        elif i.tag == 'quantity':
                            item_info['quantity'] = i.text
                    transaction_items.append(item_info)
                items.append(transaction_items)
    transaction['items'] = pd.Series(items)

def cleanup_json():
    ppl_json[['city', 'country']] = ppl_json['location'].apply(lambda x: pd.Series(cleanup.split_location(x)))
    ppl_json[['Android', 'Desktop','Iphone']] = ppl_json['devices'].apply(lambda x: pd.Series(cleanup.device_list(x)))
    ## NOTE: no unknown devices found
    ppl_json['name'] = ppl_json.apply(lambda x: cleanup.full_name(x['first_name'], x['last_name']), axis=1)
    ppl_json.drop(['devices','location'], axis=1, inplace=True) ##not dropping first and last name to see if families shop at same place
    ppl_json['id'] =  ppl_json.apply(lambda x: int(str(x['id']).lstrip("0")), axis=1)
    ppl_json.rename(columns={'telephone': 'phone'}, inplace=True)

def cleanup_yml():
    ppl_yml[['first_name', 'last_name']] = ppl_yml['name'].apply(lambda x: pd.Series(cleanup.split_name(x)))
    ppl_yml[['city', 'country']] = ppl_yml['city'].apply(lambda x: pd.Series(cleanup.split_location_str(x)))

def check_missing_values(**dfs):
    total_missing = []
    for name, df in dfs.items():
        missing_counts = df.isna().sum().sum()
        if missing_counts > 0:
            total_missing.append[name]
            print(f'Warning: {name} contains {missing_counts} missing values!')
    if len(total_missing) == 0:
        print('No missing values! All good :) ')

## Reading In Files and formatting ##

ppl_json = data_parser("data/people/people.json") #people.json
cleanup_json()

ppl_yml = data_parser("data/people/people.yml") #people.yml
cleanup_yml()

promo_csv = data_parser("data/promotions.csv") #promotions.csv

transaction = data_parser("data/transactions.xml") #transactions.xml
cleanup_items_xml('data/transactions.xml')
transaction.to_csv("data/transactions.csv", index=False)

transfer = data_parser("data/transfers.csv") #transfers.csv

#concatting to make full dataset with all people
full_ppl = pd.concat([ppl_json, ppl_yml], ignore_index=True).drop_duplicates()
full_ppl.to_csv("data/people.csv", index=False)

### Cleaning up Promo CSV ###
promo_csv[['first_name','last_name','client_email','telephone']] = promo_csv.apply(lambda x: pd.Series(cleanup.fill_blank_email_or_num(x,full_ppl)),axis = 1)
promo_csv.rename(columns={'telephone': 'phone'}, inplace=True)


### Cleaning up transfers.csv ###
transfer[['year','month','day']] = transfer['date'].apply(lambda x: pd.Series(x.split('-')))
transfer['date'] = pd.to_datetime(transfer['date'])

check_missing_values(full_ppl=full_ppl, transaction=transaction, promo_csv=promo_csv, transfer=transfer)

# print("wow",cleanup.find_person('phone','216-516-1958',full_ppl,'name'))

def data_to_use():
    return full_ppl, promo_csv, transaction, transfer