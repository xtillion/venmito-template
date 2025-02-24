import pandas as pd
from etl_pipeline.transform.transform_promotions import Promotion
from etl_pipeline.transform.transform_people import People

class PeoplePromotionsAggregator:
    def __init__(self):
        self.people_df = People('data/people.json', 'data/people.yml').data
        self.promotions_df = Promotion('data/promotions.csv').data

    def get_people_with_promotions(self):
        """Merge people with promotions using email and telephone."""
        email_merge = pd.merge(
            self.people_df,
            self.promotions_df,
            how='inner',
            left_on='email',
            right_on='client_email',
            suffixes=('_people', '_promo')
        )
        phone_merge = pd.merge(
            self.people_df,
            self.promotions_df,
            how='inner',
            left_on='telephone',
            right_on='telephone',
            suffixes=('_people', '_promo')
        )
        merged = pd.concat([email_merge, phone_merge])
        merged = merged.groupby(['person_id', 'promotion_id'], as_index=False).first()
        merged['telephone'] = merged['telephone_people'].combine_first(merged['telephone'])
        merged.drop(columns=['client_email', 'telephone_people', 'telephone_promo'], inplace=True, errors='ignore')
        return merged.sort_values(by=['person_id', 'promotion_id'])

    def get_promotions_by_person(self, person_id):
        promotions = self.get_people_with_promotions()
        if promotions is None or promotions.empty:
            return None
        # Ensure matching types for person_id comparison
        person_id = int(person_id) if promotions["person_id"].dtype == "int64" else str(person_id)
        return promotions[promotions["person_id"] == person_id]
    
    def get_people_with_specified_promotion_role(self, promotion):
        people_with_promotions_df = self.get_people_with_promotions()

        # Filter based on promotion type
        filtered_df = people_with_promotions_df[people_with_promotions_df['promotion'] == promotion]
        
        # Define the sorting order: "Yes" should come before "No"
        response_order = {'Yes': 0, 'No': 1}
        
        # Sort by the 'responded' column using the custom mapping
        filtered_df = filtered_df.sort_values(by='responded', key=lambda col: col.map(response_order))
        
        return filtered_df  

    def get_people_with_accepted_promotions(self):
        people_with_promotions_df = self.get_people_with_promotions()

        # Filter based on 'Yes' response
        filtered_df = people_with_promotions_df[people_with_promotions_df['responded'] == 'Yes']

        return filtered_df                  

    def get_people_with_denied_promotions(self):
        people_with_promotions_df = self.get_people_with_promotions()

        # Filter based on 'No' response
        filtered_df = people_with_promotions_df[people_with_promotions_df['responded'] == 'No']

        return filtered_df        