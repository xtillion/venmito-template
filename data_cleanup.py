import numpy as np
import pandas as pd
from helpers.data_parser import data_parser
import helpers.cleanup_funcs as cleanup
import xml.etree.ElementTree as ET

### Pre Cleanup  Discoveries ###

# print(ppl_json['id'].isin(ppl_yml['id'])) #reveals discrepancies in the ids
# ppl_json.isna().sum() = results show that there are no missing values


### Cleaning Up People Json and People Yml ###
ppl_json = data_parser("data/people/people.json")
def cleanup_json():
    ppl_json[['city', 'country']] = ppl_json['location'].apply(lambda x: pd.Series(cleanup.split_location(x)))
    ppl_json[['Android', 'Desktop','Iphone']] = ppl_json['devices'].apply(lambda x: pd.Series(cleanup.device_list(x)))
    ## NOTE: no unknown devices found
    ppl_json['name'] = ppl_json.apply(lambda x: cleanup.full_name(x['first_name'], x['last_name']), axis=1)
    ppl_json.drop(['devices','location'], axis=1, inplace=True) ##not dropping first and last name to see if families shop at same place
    ppl_json['id'] =  ppl_json.apply(lambda x: int(str(x['id']).lstrip("0")), axis=1)
    ppl_json.rename(columns={'telephone': 'phone'}, inplace=True)
cleanup_json()
    
ppl_yml = data_parser("data/people/people.yml")
def cleanup_yml():
    ppl_yml[['first_name', 'last_name']] = ppl_yml['name'].apply(lambda x: pd.Series(cleanup.split_name(x)))
    ppl_yml[['city', 'country']] = ppl_yml['city'].apply(lambda x: pd.Series(cleanup.split_location_str(x)))
cleanup_yml()


### Checking Datatypes  ###

# print(ppl_json.dtypes)
# print('-------------------')
# print(ppl_yml.dtypes)
#Tested and they're good to go


### Performing Concat for people information (psuedo merge, performing outer inner join wasn't needed) ###
full_ppl = pd.concat([ppl_json, ppl_yml], ignore_index=True).drop_duplicates()
full_ppl.to_csv("data/people.csv", index=False)


### Cleaning up Promo CSV ###
promo_csv = data_parser("data/promotions.csv")
promo_csv[['first_name','last_name','client_email','telephone']] = promo_csv.apply(lambda x: pd.Series(cleanup.fill_blank_email_or_num(x,full_ppl)),axis = 1)
# print(promo_csv.isna().sum()) #reveals that there are no missing values
print('promo_csv head',promo_csv.head())

### Cleaning up transaction.xml ###
transaction = data_parser("data/transactions.xml") # we need to fix items
tree = ET.parse('data/transactions.xml')
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
                        item_info['price'] = i.text
                    elif i.tag == 'price_per_item':
                        item_info['price_per_item'] = i.text
                    elif i.tag == 'quantity':
                        item_info['quantity'] = i.text
                transaction_items.append(item_info)
            items.append(transaction_items)
transaction['items'] = pd.Series(items)
#transaction now ready to be used for analysis


### Cleaning up transfers.csv ###
transfer = data_parser("data/transfers.csv")
# print(transfer.isna().sum()) #reveals that there are no missing values


def data_to_use():
    return full_ppl, promo_csv, transaction, transfer