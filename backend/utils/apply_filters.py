from datetime import datetime

from sqlalchemy import func, inspect

from backend.model.people import People
from backend.model.promotions import Promotions
from backend.model.transactions import Transactions
from backend.model.transfer import Transfers


def apply_item_filters(query, filters):
    for key, value in filters.items():
        column = getattr(Transactions, key)
        if column:
            query = query.filter(column.__eq__(value))

    # Only join People table once and use it for all relevant filters
    join_people = False
    if 'city' in filters or 'country' in filters:
        query = query.join(People, People.telephone == Transactions.telephone)
        join_people = True

    # Apply filters for the People table (filters related to city, country, age)
    if join_people:
        if 'city' in filters:
            query = query.filter(People.city == filters['city'])
        if 'country' in filters:
            query = query.filter(People.country == filters['country'])

    # Apply filters for Promotions table (filters related to promotion type)
    if 'promotion' in filters:
        query = query.join(Promotions, Promotions.promotion == Transactions.item_name)
        query = query.filter(Promotions.promotion == filters['promotion'])

    if 'month' in filters:
        query = query.filter(func.extract('month', Transactions.date) == filters['month'])
    if 'year' in filters:
        query = query.filter(func.extract('year', Transactions.date) == filters['year'])

    return query

def apply_client_filters(query, filters):
    columns = [column.name for column in inspect(People).c if column.name != 'id']
    
    for field in columns:
        if field in filters:
            query = query.filter(getattr(People, field) == filters[field])


    join_promotions = False
    if 'promotion' in filters:
        query = query.join(Promotions, Promotions.email == People.email)
        join_promotions = True

    if join_promotions:
        if 'promotion' in filters:
            query = query.filter(Promotions.promotion == filters['promotion'])

    join_transactions = False
    if 'item_name' in filters or 'store' in filters:
        query = query.join(Transactions, Transactions.telephone == People.telephone)
        join_transactions = True

    if join_transactions:
        if 'item_name' in filters:
            query = query.filter(Transactions.item_name == filters['item_name'])
        if 'store' in filters:
            query = query.filter(Transactions.store == filters['store'])

    # join_transfer = False
    # if 'sender_id' or 'recipient_id' in filters:
    #     query = query.join(Transfers, Transfers.sender_id == People.id)
    #     query = query.join(Transfers, Transfers.recipient_id == People.id)
    #     join_transfer = True
    #
    # # if join_transfer:
    # #     if ''


    if 'month' in filters:
        query = query.filter(func.extract('month', People.dob) == filters['month'])
    if 'year' in filters:
        query = query.filter(func.extract('year', People.dob) == filters['year'])

    return query
