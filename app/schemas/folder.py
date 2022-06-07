from typing import List, Union

from pydantic import BaseModel


class FoldersListSchema(BaseModel):
    folders: List[dict]


class FolderCreateSchema(BaseModel):
    name: Union[List[str], str]


class FolderRenameSchema(BaseModel):
    old_name: str
    new_name: str


class FolderDeleteSchema(BaseModel):
    name: Union[List[str], str]
