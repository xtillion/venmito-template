from pathlib import Path
from dateutil import parser

import pandas as pd

from backend.utils.logger import configure_logging

logger = configure_logging()

def transform_json_data(df_json: pd.DataFrame):
    logger.info('Transforming json data')
    # Flattening devices list into their own columns
    df_json[['android', 'iphone', 'desktop']] = pd.json_normalize(df_json['devices'].map(lambda x: dict.fromkeys(x, 1))).astype(bool).fillna(0)
    df_json.drop(columns=['devices'], inplace=True)

    # Flattening location object into their own columns
    df_json_location = pd.DataFrame.from_records(df_json['location'])
    df_json = df_json.drop(columns=['location']).join(df_json_location)
    df_json.rename(columns={'City': 'city', 'Country': 'country'}, inplace=True)

    # Convert the dob column to ISO 8601 standard to ease data manipulation
    df_json['dob'] = df_json['dob'].map(lambda x: parser.parse(x).strftime('%Y-%m-%d'))

    return df_json


def transform_yml_data(df_yml: pd.DataFrame):
    logger.info('Transforming yml data')
    df_yml[['Android', 'Desktop', 'Iphone']] = df_yml[['Android', 'Desktop', 'Iphone']].astype(bool)
    df_yml.rename(columns={'Android': 'android', 'Iphone': 'iphone', 'Desktop': 'desktop'}, inplace=True)

    # Separating city into two columns
    df_yml[['city', 'country']] = df_yml['city'].str.split(', ', n=1, expand=True)

    # Separating name into two columns
    df_yml[['first_name', 'last_name']] = df_yml['name'].str.split(' ', n=1, expand=True)
    df_yml.drop(columns=['name'], inplace=True)

    df_yml.rename(columns={'phone': 'telephone'}, inplace=True)

    # Convert the dob column to ISO 8601 standard to ease data manipulation
    df_yml['dob'] = df_yml['dob'].map(lambda x: parser.parse(x).strftime('%Y-%m-%d'))

    return df_yml


def transform_csv_data(df_csv: pd.DataFrame):
    logger.info('Transforming csv data')
    df_csv.rename(columns={'client_email': 'email'}, inplace=True)
    return df_csv


def merge_people_data(df1: pd.DataFrame, df2: pd.DataFrame):
    logger.info('Merging people data')
    merged_df_people = pd.merge(df1, df2, on='id', how='outer')
    merged_df_people['first_name'] = merged_df_people['first_name_x'].combine_first(merged_df_people['first_name_y'])
    merged_df_people['last_name'] = merged_df_people['last_name_x'].combine_first(merged_df_people['last_name_y'])
    merged_df_people['telephone'] = merged_df_people['telephone_x'].combine_first(merged_df_people['telephone_y'])
    merged_df_people['email'] = merged_df_people['email_x'].combine_first(merged_df_people['email_y'])
    merged_df_people['dob'] = merged_df_people['dob_x'].combine_first(merged_df_people['dob_y'])
    merged_df_people['city'] = merged_df_people['city_x'].combine_first(merged_df_people['city_y'])
    merged_df_people['country'] = merged_df_people['country_x'].combine_first(merged_df_people['country_y'])
    merged_df_people['android'] = merged_df_people['android_x'].combine_first(merged_df_people['android_y'])
    merged_df_people['iphone'] = merged_df_people['iphone_x'].combine_first(merged_df_people['iphone_y'])
    merged_df_people['desktop'] = merged_df_people['desktop_x'].combine_first(merged_df_people['desktop_y'])
    merged_df_people.drop(columns=['first_name_x', 'last_name_x', 'telephone_x', 'email_x',
                                   'dob_x', 'city_x', 'country_x', 'android_x', 'iphone_x',
                                   'desktop_x', 'first_name_y', 'last_name_y', 'telephone_y',
                                   'email_y', 'dob_y', 'city_y', 'country_y', 'android_y',
                                   'iphone_y', 'desktop_y'], inplace=True)

    return merged_df_people


def complete_promotions_data(df_promotions: pd.DataFrame, df_people: pd.DataFrame):
    logger.info('Completing promotions data')
    complete_df_promotions = df_promotions.merge(df_people[['email', 'telephone']], on='telephone', how='left')
    complete_df_promotions['email'] = complete_df_promotions['email_x'].combine_first(complete_df_promotions['email_y'])
    complete_df_promotions = complete_df_promotions.merge(df_people[['email', 'telephone']], on='email', how='left')
    complete_df_promotions['telephone'] = complete_df_promotions['telephone_x'].combine_first(complete_df_promotions['telephone_y'])
    complete_df_promotions.drop(columns=['email_x', 'email_y', 'telephone_x', 'telephone_y'], inplace=True)
    return complete_df_promotions

def save_data_as_csv(df: pd.DataFrame, filename: str):
    output_dir = Path.cwd().parent / 'output_data'
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / f'{filename}.csv', index=False)