from sqlalchemy import create_engine
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_url="sqlite:///data.db"):
        self.engine = create_engine(db_url)

    def save_to_db(self, df, table_name):
        try:
            # Convert Timestamp to string format before saving
            if 'date' in df.columns:
                df['date'] = df['date'].astype(str)

            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f" Saved data to table '{table_name}'")
        except Exception as e:
            print(f"Error saving data: {e}")


    def load_from_db(self, table_name):
        try:
            df = pd.read_sql_table(table_name, self.engine)
            return df
        except Exception as e:
            print(f"Error loading data from table '{table_name}': {e}")
            return None
