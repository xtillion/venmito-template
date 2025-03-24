from backend.utils.logger import configure_logging
from ..repository.promotions_repository import PromotionsRepository


class PromotionsService:
    def __init__(self, repository: PromotionsRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_promotions_by_filter(self, filters):
        self.logger.info(f'Retrieving promotions with filters: {filters.keys()}')
        return self.repository.get_promotions_by_filters(filters)

    def get_promotions_by_id(self, promotion_id: int):
        return self.repository.get_promotions_by_id(promotion_id)