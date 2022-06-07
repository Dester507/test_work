from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings


SQLALCHEMY_ENGINE_OPTIONS = {
    "echo": False,
    "future": True,
    "connect_args": {
        "connect_timeout": 5
    }
}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS)

session = sessionmaker(engine, expire_on_commit=False)
