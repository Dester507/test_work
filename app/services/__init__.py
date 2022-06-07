from sqlalchemy.orm import Session


class BaseService:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    @property
    def db_session(self) -> Session:
        return self._db_session
