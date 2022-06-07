from typing import Optional

from . import BaseService
from app.models.models import Files
from app.queries.files import (
    insert_files_q,
    select_files_q,
    update_files_q,
    delete_file_q
)


class FilesService(BaseService):

    def create_file(
            self,
            name: str,
            full_name: str,
            size: int,
            _type: str,
            folder_id: int,
            user_id: int
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = insert_files_q(
            ).values(
                name=name,
                full_name=full_name,
                size=size,
                type=_type,
                folder_id=folder_id,
                user_id=user_id
            )
            self.db_session.execute(stmt)

    def check_file(
            self,
            name: str,
            folder_id: int,
            user_id: int
    ):
        stmt = select_files_q(
        ).where(
            Files.name == name,
            Files.folder_id == folder_id,
            Files.user_id == user_id
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def get_file_by_id(
            self,
            file_id: int,
            user_id: int
    ):
        stmt = select_files_q(
        ).where(
            Files.id == file_id,
            Files.user_id == user_id
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def update_file_share(
            self,
            file_id: int,
            share: bool
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = update_files_q(
            ).where(
                Files.id == file_id
            ).values(
                share=share
            )
            self.db_session.execute(stmt)

    def update_file_name(
            self,
            file_id: int,
            file_name: str,
            full_name: str
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = update_files_q(
            ).where(
                Files.id == file_id
            ).values(
                name=file_name,
                full_name=full_name
            )
            self.db_session.execute(stmt)

    def delete_file(
            self,
            file_id
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = delete_file_q(
            ).where(
                Files.id == file_id
            )
            self.db_session.execute(stmt)

    def get_shared_file(
            self,
            file_id: int
    ):
        stmt = select_files_q(
        ).where(
            Files.id == file_id,
            Files.share == True
        )
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def update_folder_data(
            self,
            file_id: int,
            folder_id: int
    ):
        self.db_session.close()
        with self.db_session.begin():
            stmt = update_files_q(
            ).where(
                Files.id == file_id
            ).values(
                folder_id=folder_id
            )
            self.db_session.execute(stmt)

    def browse_files(
            self,
            user_id: int,
            name_pattern: Optional[str] = None
    ):
        stmt = select_files_q(
        ).where(
            Files.user_id == user_id
        )
        if name_pattern:
            stmt.filter(
                Files.name.ilike(name_pattern)
            )
        result = self.db_session.execute(stmt)
        return result.scalars().all()
