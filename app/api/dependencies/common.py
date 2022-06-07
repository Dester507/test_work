from typing import (
    Type,
    Callable
)

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.services import BaseService
from app.models import engine


sync_session = sessionmaker(engine, expire_on_commit=False)


def get_db_session():
    with sync_session() as session:
        yield session


def get_service(service_type: Type[BaseService]) -> Callable[[Session], BaseService]:
    def _get_service(db_session: Session = Depends(get_db_session)) -> BaseService:
        return service_type(db_session)
    return _get_service
