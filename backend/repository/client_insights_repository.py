from sqlalchemy.sql import func

from backend.database import Session
from backend.model.people import People
from backend.model.transactions import Transactions
from backend.model.transfer import Transfers
from backend.utils.apply_filters import apply_client_filters


class ClientInsightsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_most_recurring_clients(self, filters=None):
        query = self.db_session.query(
                People.first_name,
                People.last_name,
                People.email,
                People.telephone,
                func.count(Transactions.telephone).label('total_purchases_done'),
                )

        if filters is not None:
            query = apply_client_filters(query, filters)
        
        query = query.join(Transactions, Transactions.telephone == People.telephone)

        query = query.group_by(People.first_name, People.last_name, People.email, People.telephone)
        query = query.order_by(func.count(Transactions.telephone).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'first_name': value.first_name,
            'last_name': value.last_name,
            'email': value.email,
            'telephone': value.telephone,
            'total_purchases_done': value.total_purchases_done
        } for value in results]

    def get_clients_with_most_purchases(self, filters=None):
        query = self.db_session.query(
                People.first_name,
                People.last_name,
                People.email,
                People.telephone,
                func.sum(Transactions.quantity).label('total_items_purchased'),
                )

        if filters is not None:
            query = apply_client_filters(query, filters)
        
        query = query.join(Transactions, Transactions.telephone == People.telephone)

        query = query.group_by(People.first_name, People.last_name, People.email, People.telephone)
        query = query.order_by(func.sum(Transactions.quantity).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'first_name': value.first_name,
            'last_name': value.last_name,
            'email': value.email,
            'telephone': value.telephone,
            'total_items_purchased': value.total_items_purchased
        } for value in results]

    def get_clients_with_most_transferred_funds(self, filters):
        query = self.db_session.query(
            People.first_name,
            People.last_name,
            People.email,
            People.telephone,
            func.sum(Transfers.amount).label('total_funds_transferred'),
        )

        if filters is not None:
            query = apply_client_filters(query, filters)

        query = query.join(Transfers, Transfers.sender_id == People.id)

        query = query.group_by(People.first_name, People.last_name, People.email, People.telephone)
        query = query.order_by(func.sum(Transfers.amount).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'first_name': value.first_name,
            'last_name': value.last_name,
            'email': value.email,
            'telephone': value.telephone,
            'total_funds_transferred': value.total_funds_transferred
        } for value in results]

    def get_clients_with_most_received_funds(self, filters):
        query = self.db_session.query(
            People.first_name,
            People.last_name,
            People.email,
            People.telephone,
            func.sum(Transfers.amount).label('total_funds_received'),
        )

        if filters is not None:
            query = apply_client_filters(query, filters)

        query = query.join(Transfers, Transfers.recipient_id == People.id)

        query = query.group_by(People.first_name, People.last_name, People.email, People.telephone)
        query = query.order_by(func.sum(Transfers.amount).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'first_name': value.first_name,
            'last_name': value.last_name,
            'email': value.email,
            'telephone': value.telephone,
            'total_funds_received': value.total_funds_received
        } for value in results]

    def get_cities_with_most_clients(self, filters):
        query = self.db_session.query(
            People.city,
            func.count(People.email).label('total_clients_in_city'),
        )

        if filters is not None:
            query = apply_client_filters(query, filters)

        query = query.group_by(People.city)
        query = query.order_by(func.count(People.email).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'city': value.city,
            'total_clients_in_city': value.total_clients_in_city,
        } for value in results]

    def get_countries_with_most_users(self, filters):
        query = self.db_session.query(
            People.country,
            func.count(People.email).label('total_users_in_country'),
        )

        if filters is not None:
            query = apply_client_filters(query, filters)

        query = query.group_by(People.country)
        query = query.order_by(func.count(People.email).desc())

        if filters is not None and 'limit' in filters:
            query = query.limit(filters['limit'])

        results = query.all()
        return [{
            'country': value.country,
            'total_users_in_country': value.total_users_in_country,
        } for value in results]