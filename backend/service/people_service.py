from backend.utils.logger import configure_logging
from ..repository.people_repository import PeopleRepository


class PeopleService:
    def __init__(self, repository: PeopleRepository):
        self.repository = repository
        self.logger = configure_logging()

    def get_people_by_filter(self, filters):
        self.logger.info(f'Retrieving people that match {filters.keys()}')
        return self.repository.get_people_by_filters(filters)

    def get_people_by_id(self, people_id: int):
        return self.repository.get_people_by_id(people_id)