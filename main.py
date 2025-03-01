import numpy as np
import pandas as pd
from helpers.data_parser import data_parser
import helpers.cleanup_funcs as cleanup

ppl_json = data_parser("data/people.json")
# Cleaning Up People Json

# ppl_json.isna().sum() = results show that there are no missing values
ppl_json[['city', 'country']] = ppl_json['location'].apply(lambda x: pd.Series(cleanup.split_location(x)))
ppl_json.drop(['location'], axis=1, inplace=True) ##not dropping first and last name to see if families shop at same place
ppl_json['name'] = ppl_json.apply(lambda x: cleanup.full_name(x['first_name'], x['last_name']), axis=1)
ppl_json['id'] =  ppl_json.apply(lambda x: int(str(x['id']).lstrip("0")), axis=1)
ppl_json.rename(columns={'telephone': 'phone'}, inplace=True)


# print(ppl_json['id'].isin(ppl_yml['id'])) #reveals discrepancies in the ids

ppl_yml = data_parser("data/people.yml")
# Making yml uniform with json





# promo_csv = data_parser("data/promotions.csv")
# transaction_csv = data_parser("data/transactions.xml")
# transfer_csv = data_parser("data/transfers.csv")
