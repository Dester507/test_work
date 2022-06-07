from sqlalchemy.future import select
from sqlalchemy import insert, update, delete

from app.models.models import Folders


def select_folders_q():
    q = select(Folders)
    return q


def insert_folders_q():
    q = insert(Folders)
    return q


def update_folders_q():
    q = update(Folders)
    return q


def delete_folders_q():
    q = delete(Folders)
    return q
