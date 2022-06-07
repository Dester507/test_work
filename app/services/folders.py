from . import BaseService
from app.models.models import Folders
from app.queries.folders import (
    select_folders_q,
    insert_folders_q,
    update_folders_q,
    delete_folders_q
)


class FoldersService(BaseService):

    def get_folder_by_id(
            self,
            folder_id: int,
            user_id: int,
    ):
        stmt = select_folders_q(
        ).where(
            Folders.id == folder_id,
            Folders.user_id == user_id
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def get_folders_by_user_id(
            self,
            user_id: int
    ):
        stmt = select_folders_q(
        ).where(
            Folders.user_id == user_id
        )
        result = self.db_session.execute(stmt)
        return result.scalars()

    def get_folder_by_name(
            self,
            name: str,
            user_id: int
    ):
        stmt = select_folders_q(
        ).where(
            Folders.name == name,
            Folders.user_id == user_id
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def create_folder(
            self,
            name: str,
            user_id: int
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = insert_folders_q(
            ).values(
                name=name,
                user_id=user_id
            )
            self.db_session.execute(stmt)

    def rename_folder(
            self,
            old_name: str,
            new_name: str,
            user_id: int
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = update_folders_q(
            ).where(
                Folders.name == old_name,
                Folders.user_id == user_id
            ).values(
                name=new_name
            )
            self.db_session.execute(stmt)

    def delete_folder(
            self,
            name: str,
            user_id: int
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = delete_folders_q(
            ).where(
                Folders.name == name,
                Folders.user_id == user_id
            )
            self.db_session.execute(stmt)

    def get_folder_from_file(
            self,
            folder_id: int
    ):
        stmt = select_folders_q(
        ).where(
            Folders.id == folder_id
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()
