from typing import Optional

from . import BaseService
from app.models.models import Users
from app.queries.users import (
    select_user_q,
    insert_user_q
)


class UsersService(BaseService):

    def get_by_username(
            self,
            username: str
    ) -> Optional[Users]:
        stmt = select_user_q(
        ).where(
            Users.username == username
        )
        result = self.db_session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    def create_user(
            self,
            username: str,
            password: str,
            full_name: str,
            age: Optional[int] = None
    ):
        # Close started session and start new
        self.db_session.close()
        with self.db_session.begin():
            stmt = insert_user_q(
            ).values(
                username=username,
                password=password,
                full_name=full_name,
                age=age
            )
            self.db_session.execute(stmt)
