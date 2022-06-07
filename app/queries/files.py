from sqlalchemy.future import select
from sqlalchemy import insert, update, delete

from app.models.models import Files


def insert_files_q():
    q = insert(Files)
    return q


def select_files_q():
    q = select(Files)
    return q


def update_files_q():
    q = update(Files)
    return q


def delete_file_q():
    q = delete(Files)
    return q
