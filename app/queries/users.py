from sqlalchemy.future import select
from sqlalchemy import insert

from app.models.models import Users


def select_user_q():
    q = select(Users)
    return q


def insert_user_q():
    q = insert(Users)
    return q
