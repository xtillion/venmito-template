from backend.utils.logger import configure_logging
from ..repository.transactions_repository import TransactionsRepository


class TransactionsService:
    def __init__(self, repository: TransactionsRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_transactions_by_filter(self, filters):
        self.logger.info(f'Retrieving transactions with filters: {filters.keys()}')
        return self.repository.get_transactions_by_filters(filters)

    def get_transactions_by_id(self, transact_id: int):
        return self.repository.get_transactions_by_id(transact_id)