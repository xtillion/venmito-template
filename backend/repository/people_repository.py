from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

from ..model.people import People


class PeopleRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_people_by_filters(self, filters):
        query = self.db_session.query(People)

        for key, value in filters.items():
            column = getattr(People, key)
            if column:
                query = query.filter(column.__eq__(value))

        return query.all()

    def get_people_by_id(self, people_id: int):
        return self.db_session.query(People).get(people_id)