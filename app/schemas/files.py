from typing import Optional, List, Union, Literal

from pydantic import BaseModel


class FileSettingsSchema(BaseModel):
    file_id: int
    share: Optional[bool] = None
    rename: Optional[str] = None


class FileDeleteSchema(BaseModel):
    file_id: Union[List[int], int]


class FileMoveSchema(BaseModel):
    file_id: int
    folder_id: int


class FileFiltersSchema(BaseModel):
    name: bool = False
    size: Optional[Literal['start', 'end']] = None
    type: bool = False
    create_date: bool = False
    modified_date: bool = False


class FileBrowseSchema(BaseModel):
    name_pattern: Optional[str] = None
    filters: Optional[FileFiltersSchema] = None
