from sqlalchemy.sql import func

from backend.database import Session
from backend.model.people import People
from backend.model.promotions import Promotions
from backend.model.transactions import Transactions
from backend.utils.apply_filters import apply_item_filters


class ItemInsightsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_top_selling_items(self, filters=None):
        query = self.db_session.query(
                Transactions.item_name,
                func.sum(Transactions.quantity).label('total_quantity_sold'),
                )

        if filters is not None:
            query = apply_item_filters(query, filters)

        query = query.group_by(Transactions.item_name)
        query = query.order_by(func.sum(Transactions.quantity).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'item_name': value.item_name,
            'total_quantity_sold': value.total_quantity_sold
        } for value in results]

    def get_most_profitable_item(self, filters=None):
        query = self.db_session.query(
                Transactions.item_name, func.sum(Transactions.total_price).label('total_profit')
            )

        if filters is not None:
            query = apply_item_filters(query, filters)

        query = query.group_by(Transactions.item_name)
        query = query.order_by(func.sum(Transactions.total_price).desc())

        results = query.all()

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        return [{
            'item_name': value.item_name,
            'total_profit': value.total_profit
        } for value in results]

    def get_stores_with_most_sales(self, filters=None):
        query = self.db_session.query(
                Transactions.store, func.sum(Transactions.quantity).label('total_items_sold')
            )

        if filters is not None:
            query = apply_item_filters(query, filters)

        query = query.group_by(Transactions.store)
        query = query.order_by(func.sum(Transactions.quantity).desc())

        results = query.all()

        return [{
            'store': value.store,
            'total_items_sold': value.total_items_sold
        } for value in results]

    def get_stores_with_most_revenue(self, filters=None):
        query = self.db_session.query(
                Transactions.store, func.sum(Transactions.total_price).label('total_store_revenue')
            )

        if filters is not None:
            query = apply_item_filters(query, filters)

        query = query.group_by(Transactions.store)
        query = query.order_by(func.sum(Transactions.total_price).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()

        return [{
            'store': value.store,
            'total_store_revenue': value.total_store_revenue
        } for value in results]

    def get_most_promoted_items(self, filters):
        query = self.db_session.query(
            Promotions.promotion,
            func.count(Promotions.promotion).label('times_on_promotion')
        )

        if filters is not None:
            apply_item_filters(query, filters)

        query = query.group_by(Promotions.promotion)
        query = query.order_by(func.count(Promotions.promotion).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()

        return [{
            'promotion': value.promotion,
            'times_on_promotion': value.times_on_promotion
        } for value in results]


    def get_top_selling_item_by_ages(self):
        query = self.db_session.query(
            People.dob,
            Transactions.item_name,
            func.sum(Transactions.quantity).label("total_quantity_sold")
        ).join(People, People.telephone == Transactions.telephone)  # Ensure correct join condition
        query = query.group_by(People.dob, Transactions.item_name)
        query = query.order_by(func.sum(Transactions.quantity).desc())

        return query.all()