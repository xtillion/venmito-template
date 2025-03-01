import numpy as np
import pandas as pd
from helpers.data_parser import data_parser
import helpers.cleanup_funcs as cleanup

#Pre Cleanup  Discoveries

# print(ppl_json['id'].isin(ppl_yml['id'])) #reveals discrepancies in the ids
# ppl_json.isna().sum() = results show that there are no missing values

ppl_json = data_parser("data/people.json")
# Cleaning Up People Json

def cleanup_json():
    ppl_json[['city', 'country']] = ppl_json['location'].apply(lambda x: pd.Series(cleanup.split_location(x)))
    ppl_json[['Android', 'Desktop','Iphone']] = ppl_json['devices'].apply(lambda x: pd.Series(cleanup.device_list(x)))
    ## NOTE: no unknown devices found
    ppl_json['name'] = ppl_json.apply(lambda x: cleanup.full_name(x['first_name'], x['last_name']), axis=1)
    ppl_json.drop(['devices','location'], axis=1, inplace=True) ##not dropping first and last name to see if families shop at same place
    ppl_json['id'] =  ppl_json.apply(lambda x: int(str(x['id']).lstrip("0")), axis=1)
    ppl_json.rename(columns={'telephone': 'phone'}, inplace=True)

cleanup_json()
    
ppl_yml = data_parser("data/people.yml")

def cleanup_yml():
    ppl_yml[['first_name', 'last_name']] = ppl_yml['name'].apply(lambda x: pd.Series(cleanup.split_name(x)))
    ppl_yml[['city', 'country']] = ppl_yml['city'].apply(lambda x: pd.Series(cleanup.split_location_str(x)))

cleanup_yml()

print(pd.merge(ppl_json, ppl_yml, on='id', how='cross'))

##### check datatypes before merging as well as removing duplicates  ####


# promo_csv = data_parser("data/promotions.csv")
# transaction_csv = data_parser("data/transactions.xml")
# transfer_csv = data_parser("data/transfers.csv")
