from etl_pipeline.extract.extract_csv import extract_csv

class Transfer:
    def __init__(self, filepath):
        self.data = extract_csv(filepath)

    def get_transfer_details(self):
        return self.data
