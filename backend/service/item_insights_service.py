from backend.repository.item_insights_repository import ItemInsightsRepository
from backend.utils.logger import configure_logging
from backend.utils.useful_functions import get_age_range


class ItemInsightsService:
    def __init__(self, repository: ItemInsightsRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_top_selling_items(self, filters=None):
        return self.repository.get_top_selling_items(filters)

    def get_most_profitable_item(self, filters=None):
        return self.repository.get_most_profitable_item(filters)

    def get_stores_with_most_sales(self, filters=None):
        return self.repository.get_stores_with_most_sales(filters)

    def get_stores_with_most_revenue(self, filters=None):
        return self.repository.get_stores_with_most_revenue(filters)

    def get_most_promoted_items(self, filters=None):
        return self.repository.get_most_promoted_items(filters)

    def get_top_selling_item_by_ages(self):
        # Fetch raw data from the repository
        result = self.repository.get_top_selling_item_by_ages()

        # List to store the final structured output
        most_sold_items = []

        # Dictionary to track the most sold item per age range
        age_range_data = {}

        for row in result:
            dob = row.dob
            age_range = get_age_range(dob)  # Get age range from DOB

            # Compare and find the most sold item for this age range
            if age_range not in age_range_data or row.total_quantity_sold > age_range_data[age_range]["total_quantity_sold"]:
                age_range_data[age_range] = {
                    "age_range": age_range,
                    "item_name": row.item_name,
                    "total_quantity_sold": row.total_quantity_sold,
                }

        # Convert the dictionary into a list format
        top_selling_items_by_age = sorted(age_range_data.values(), key=lambda x: x["age_range"])

        return top_selling_items_by_age

