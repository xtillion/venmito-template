import pandas as pd
from etl_pipeline.transform.transform_transfers import Transfer
from etl_pipeline.transform.transform_people import People

class PeopleTransfersAggregator:
    def __init__(self):
        self.people_df = People('data/people.json', 'data/people.yml').data
        self.transfers_df = Transfer('data/transfers.csv').data

    def get_people_with_transfers(self):
        """Merge to return people who have received transfers."""
        merged = pd.merge(
            self.people_df,
            self.transfers_df,
            how='inner',
            left_on='person_id',
            right_on='recipient_id'
        )
        merged = pd.merge(
            merged,
            self.people_df,
            left_on='sender_id',
            right_on='person_id',
            suffixes=('_recipient', '_sender')
        )
        merged['sender_name'] = merged['first_name_sender'] + " " + merged['last_name_sender']
        merged['recipient_name'] = merged['first_name_recipient'] + " " + merged['last_name_recipient']
        merged.rename(columns={
            'date': 'transfer_date',
            'email_sender': 'sender_email',
            'email_recipient': 'recipient_email',
            'telephone_sender': 'sender_telephone',
            'telephone_recipient': 'recipient_telephone',
            'city_recipient': 'recipient_city', 
            'country_recipient': 'recipient_country', 
            'city_sender': 'sender_city', 
            'country_sender': 'sender_country'
        }, inplace=True)
        merged.drop(columns=['person_id_sender', 'person_id_recipient', 'first_name_sender', 
                               'last_name_sender', 'first_name_recipient', 'last_name_recipient', 
                               'devices_sender', 'devices_recipient'], inplace=True)
        return merged