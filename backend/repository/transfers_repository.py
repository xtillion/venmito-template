from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..model.transfer import Transfers


class TransfersRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_transfers_by_filters(self, filters):
        query = self.db_session.query(Transfers)

        for key, value in filters.items():
            column = getattr(Transfers, key)
            if column:
                query = query.filter(column.__eq__(value))

        return query.all()

    def get_transfers_by_id(self, transfers_id: int):
        return self.db_session.query(Transfers).filter(Transfers.id.__eq__(transfers_id)).first()