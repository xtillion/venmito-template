from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..model.promotions import Promotions


class PromotionsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_promotions(self):
        return self.db_session.query(Promotions).all()

    def get_promotions_by_filters(self, filters):
        query = self.db_session.query(Promotions)

        for key, value in filters.items():
            column = getattr(Promotions, key, None)
            if column:
                query = query.filter(column.__eq__(value))

        return query.all()

    def get_promotions_by_id(self, promotions_id: int):
        return self.db_session.query(Promotions).filter(Promotions.id.__eq__(promotions_id)).first()