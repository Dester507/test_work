from typing import Optional

from fastapi.responses import FileResponse
from fastapi import (
    APIRouter,
    Depends,
    Security,
    UploadFile,
    File
)

from app.api.dependencies.common import get_service
from app.api.dependencies.security import get_current_user
from app.schemas.users import UserSchema
from app.services.files import FilesService
from app.services.folders import FoldersService
from app.config import settings
from app.schemas.files import (
    FileSettingsSchema,
    FileDeleteSchema,
    FileMoveSchema,
    FileBrowseSchema
)
from app.lib.files import (
    save_file,
    rename_file,
    delete_storage_file,
    get_path_to_file,
    move_file_to_another_folder
)


router = APIRouter()


# Upload single file
@router.post(
    "/file/upload/{folder_id}",
    name="files:upload",
    description="Upload file endpoint. Upload single file to user folder."
)
def upload_file(
        folder_id: int,
        file: UploadFile = File(...),
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check folder
    folder = folder_service.get_folder_by_id(folder_id, user.id)
    if not folder:
        return {"message": f"Failed to upload file, folder with this id <{folder_id}> doesn't exist.'"}
    # Get correct filename
    correct_filename = ".".join(file.filename.split(".")[:-1])
    # Check file
    check_file = file_service.check_file(correct_filename, folder_id, user.id)
    if check_file:
        return {"message": f"Failure to upload file, file with this name <{correct_filename}> already exists."}
    # Save file in folder and database
    result = save_file(user.id, folder.name, file.filename, file.file)
    if isinstance(result, dict):
        return result
    else:
        file_service.create_file(
            correct_filename,
            file.filename,
            result,
            file.content_type,
            folder_id,
            user.id
        )
    return {"message": f"Successfully uploaded file."}


# Change file name and share mode
@router.patch(
    "/file",
    name="files:settings",
    description="Settings for file. Funcs: rename, share"
)
def settings_file(
        data: FileSettingsSchema,
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check file
    file = file_service.get_file_by_id(data.file_id, user.id)
    if not file:
        return {"message": "File doesn't exist'"}
    # Check mode
    if data.rename is None and data.share is None:
        return {"message": "No one mode selected"}
    else:
        result = []
        # Share
        if data.share is not None:
            file_service.update_file_share(data.file_id, data.share)
            if data.share:
                result.append(
                    {"share": "On", "link": f"http://{settings.PROJECT_IP}:{settings.PROJECT_PORT}/file/{data.file_id}"}
                )
            else:
                result.append(
                    {"share": "Off"}
                )
        # Rename
        if data.rename is not None:
            # Check if new name is correct
            check_file = file_service.check_file(data.rename, file.folder_id, user.id)
            if check_file:
                result.append(
                    {"rename": f"Fail! File with this name <{data.rename}> already exists"}
                )
            else:
                # Get folder
                folder = folder_service.get_folder_by_id(file.folder_id, user.id)
                # Change file name
                new_full_name = f"{data.rename}.{file.full_name.split('.')[-1:][0]}"
                rename_file(file.full_name, new_full_name, folder.name, user.id)
                # Change name in db
                file_service.update_file_name(file.id, data.rename, new_full_name)
                result.append(
                    {"rename": f"Successfully renamed file"}
                )
        return {"result": result}


# Delete file
@router.delete(
    "/file",
    name="files:delete",
    description="Delete file endpoint. Single and multiple mode"
)
def delete_file(
        data: FileDeleteSchema,
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check mode
    if isinstance(data.file_id, list):
        good_ids = set()
        bad_ids = set()
        # Filter ids
        for elem in data.file_id:
            # Check file
            file = file_service.get_file_by_id(elem, user.id)
            if file:
                good_ids.add(elem)
            else:
                bad_ids.add(elem)
        # Delete files
        for elem in good_ids:
            file = file_service.get_file_by_id(elem, user.id)
            folder = folder_service.get_folder_by_id(file.folder_id, user.id)
            # Delete storage file
            delete_storage_file(user.id, folder.name, file.full_name)
            # Delete from database
            file_service.delete_file(file.id)
        return {"deleted": "; ".join(map(str, good_ids)), "failed": "; ".join(map(str, bad_ids))}
    else:
        # Check file
        file = file_service.get_file_by_id(data.file_id, user.id)
        if not file:
            return {"message": f"Fail, file with this id <{data.file_id}> doesn't exist'"}
        folder = folder_service.get_folder_by_id(file.folder_id, user.id)
        # Delete storage file
        delete_storage_file(user.id, folder.name, file.full_name)
        # Delete from database
        file_service.delete_file(file.id)
        return {"message": f"Success, file with this id <{file.id}> deleted"}


# Download shared file
@router.get(
    "/file/{file_id}",
    name="files:download-shared",
    description="Can download file, where shared is True"
)
def download_shared(
        file_id: int,
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService))
):
    # Check file
    file = file_service.get_shared_file(file_id)
    if not file:
        return {"message": "File not found."}
    folder = folder_service.get_folder_from_file(file.folder_id)
    full_path = get_path_to_file(folder.name, file.full_name, file.user_id)
    return FileResponse(full_path, media_type=file.type, filename=file.full_name)


# Download single file
@router.get(
    "/file/download/{file_id}"
)
def download_single_file(
        file_id: int,
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check file
    file = file_service.get_file_by_id(file_id, user.id)
    if not file:
        return {"message": "File not found."}
    folder = folder_service.get_folder_by_id(file.folder_id, user.id)
    full_path = get_path_to_file(folder.name, file.full_name, user.id)
    return FileResponse(full_path, media_type=file.type, filename=file.full_name)


# Move file to another folder
@router.post(
    "/file/move",
    name="files:move",
    description="Move file to another folder"
)
def move_file(
        data: FileMoveSchema,
        file_service: FilesService = Depends(get_service(FilesService)),
        folder_service: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check file
    file = file_service.get_file_by_id(data.file_id, user.id)
    if not file:
        return {"message": "File not found!"}
    # Check folder
    folder = folder_service.get_folder_by_id(data.folder_id, user.id)
    if not folder:
        return {"message": "Folder not found!"}
    elif file.folder_id == folder.id:
        return {"message": "Same folder!"}
    # Check for same name in new folder
    check_file = file_service.check_file(file.name, folder.id, user.id)
    if check_file:
        return {"message": "File with same name already exists in this folder!"}
    # Move file
    old_folder = folder_service.get_folder_by_id(file.folder_id, user.id)
    move_file_to_another_folder(old_folder.name, folder.name, file.full_name, user.id)
    file_service.update_folder_data(file.id, folder.id)
    return {"message": "Successfully move file to another folder!"}


# Browse files
@router.post(
    "/file",
    name="files:browse",
    description="Browse files with filters. "
                "Can pass name_pattern and filters or only name_pattern or only filters or nothing"
)
def browse_files(
        data: Optional[FileBrowseSchema] = None,
        file_service: FilesService = Depends(get_service(FilesService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check if file name pattern exist
    pattern = None
    if data and data.name_pattern:
        pattern = f"%{data.name_pattern}%"
    # Get files by file name pattern
    files = file_service.browse_files(user.id, pattern)
    if len(files) == 0:
        return {"files": []}
    # Perform list with files
    all_files = []
    for elem in files:
        all_files.append(
            {
                "id": elem.id,
                "name": elem.name,
                "type": elem.type,
                "size": elem.size,
                "created_date": elem.created_at,
                "updated_date": elem.updated_at,
                "folder_id": elem.folder.id,
                "folder_name": elem.folder.name
            }
        )
    if not data:
        return {"files": all_files}
    # Filters
    if data.filters:
        all_files.sort(
            key=lambda x: (
                x["name"] if data.filters.name else None,
                x["size"] if data.filters.size == "start" else -x["size"] if data.filters.size == "end" else None,
                x["type"] if data.filters.type else None,
                x["created_date"] if data.filters.create_date else None,
                x["updated_date"] if data.filters.modified_date and not data.filters.create_date else None
            )
        )
    return {"files": all_files}
