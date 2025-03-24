from backend.utils.logger import configure_logging
from ..repository.transfers_repository import TransfersRepository


class TransfersService:
    def __init__(self, repository: TransfersRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_transfers_by_filter(self, filters):
        self.logger.info(f'Retrieving transfers with filters: {filters.keys()}')
        return self.repository.get_transfers_by_filters(filters)

    def get_transfers_by_id(self, transfer_id: int):
        return self.repository.get_transfers_by_id(transfer_id)