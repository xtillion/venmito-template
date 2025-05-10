from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..model.transactions import Transactions


class TransactionsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_transactions_by_filters(self, filters):
        query = self.db_session.query(Transactions)

        for key, value in filters.items():
            column = getattr(Transactions, key)
            if column:
                query = query.filter(column.__eq__(value))

        return query.all()

    def get_transactions_by_id(self, transact_id: int):
        return self.db_session.query(Transactions).filter(Transactions.id.__eq__(transact_id)).first()