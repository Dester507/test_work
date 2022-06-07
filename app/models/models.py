from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Column,
    Identity,
    ForeignKey
)
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    BigInteger,
    Boolean,
    UnicodeText,
    Text
)

from app.models import engine


Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, Identity(always=True), primary_key=True)
    username = Column(String(63), nullable=False, unique=True)
    password = Column(UnicodeText, nullable=False)
    full_name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=True)
    scopes = Column(ARRAY(UnicodeText), default=["*"])
    created_at = Column(DateTime, server_default=func.now())


class Folders(Base):
    __tablename__ = "Folders"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(String(63), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    user = relationship("Users", backref=backref("folders", lazy=True))


class Files(Base):
    __tablename__ = "Files"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(Text, nullable=False)
    full_name = Column(Text, nullable=False)
    size = Column(BigInteger, nullable=False)
    type = Column(Text, nullable=False)
    share = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    folder_id = Column(Integer, ForeignKey(Folders.id, ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    folder = relationship("Folders", backref=backref("files", lazy=True))


Base.metadata.create_all(engine)
