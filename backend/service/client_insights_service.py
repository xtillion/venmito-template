from backend.repository.client_insights_repository import ClientInsightsRepository
from backend.utils.logger import configure_logging


class ClientInsightsService:
    def __init__(self, repository: ClientInsightsRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_most_recurring_clients(self, filters=None):
        return self.repository.get_most_recurring_clients(filters)

    def get_clients_with_most_purchases(self, filters=None):
        return self.repository.get_clients_with_most_purchases(filters)

    def get_clients_with_most_transferred_funds(self, filters=None):
        return self.repository.get_clients_with_most_transferred_funds(filters)

    def get_clients_with_most_received_funds(self, filters=None):
        return self.repository.get_clients_with_most_received_funds(filters)

    def get_cities_with_most_clients(self, filters=None):
        return self.repository.get_cities_with_most_clients(filters)

    def get_countries_with_most_users(self, filters=None):
        return self.repository.get_countries_with_most_users(filters)