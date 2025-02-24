from etl_pipeline.extract.extract_csv import extract_csv

class Promotion:
    def __init__(self, filepath):
        self.data = extract_csv(filepath)
        self.data.rename(columns={'id': 'promotion_id'}, inplace=True)

    def get_promotion_details(self):
        return self.data