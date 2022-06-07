from fastapi import (
    APIRouter,
    Depends,
    Security
)

from app.services.folders import FoldersService
from app.api.dependencies.common import get_service
from app.api.dependencies.security import get_current_user
from app.schemas.users import UserSchema
from app.lib.folders import (
    create_dir,
    rename_dir,
    delete_dir
)
from app.schemas.folder import (
    FoldersListSchema,
    FolderCreateSchema,
    FolderRenameSchema,
    FolderDeleteSchema
)

router = APIRouter()


@router.get(
    "/folder",
    response_model=FoldersListSchema,
    name="folders:list"
)
def get_folders(
        folder: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    folders = folder.get_folders_by_user_id(user.id)
    data = []
    for elem in folders:
        data.append({"folder_id": elem.id, "folder_name": elem.name})
    return {"folders": data}


@router.post(
    "/folder",
    name="folders:create",
    description="Create folder endpoint. Has two mods (single and multiple)"
)
def create_folder(
        folder_data: FolderCreateSchema,
        folder: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check mode (single or multiple)
    if isinstance(folder_data.name, list):
        bad_folders = set()
        good_folders = set()
        # Filter names
        for elem in folder_data.name:
            check_folder = folder.get_folder_by_name(elem, user.id)
            if check_folder:
                bad_folders.add(elem)
            else:
                good_folders.add(elem)
        # Create folders
        for elem in good_folders:
            create_dir(elem, user.id)
            folder.create_folder(elem, user.id)
        return {
            "created": "; ".join(good_folders),
            "failed": "; ".join(bad_folders)
        }
    else:
        check_folder = folder.get_folder_by_name(folder_data.name, user.id)
        # Check name
        if check_folder:
            return {"message": "Failure creating. Folder with this name already exists."}
        # Create folder
        create_dir(folder_data.name, user.id)
        folder.create_folder(folder_data.name, user.id)
        return {"message": "Successfully created."}


@router.patch(
    "/folder",
    name="folders:rename"
)
def rename_folder(
        data: FolderRenameSchema,
        folder: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    # Check if folder exists
    check_old_folder = folder.get_folder_by_name(data.old_name, user.id)
    if not check_old_folder:
        return {"message": "Fail! Folder with this name doesn't exist'"}
    check_new_folder = folder.get_folder_by_name(data.new_name, user.id)
    if check_new_folder:
        return {"message": f"Fail! Folder with this name <{data.new_name}> already exists"}
    folder.rename_folder(data.old_name, data.new_name, user.id)
    rename_dir(data.old_name, data.new_name, user.id)
    return {"message": "Successfully renamed!"}


@router.delete(
    "/folder",
    name="folders:delete",
    description="Delete folder endpoint. Has two mods (single and multiple)"
)
def delete_folder(
        data: FolderDeleteSchema,
        folder: FoldersService = Depends(get_service(FoldersService)),
        user: UserSchema = Security(get_current_user, scopes=["*"])
):
    if isinstance(data.name, list):
        good_folders = set()
        bad_folders = set()
        # Filter folders
        for elem in data.name:
            check_folder = folder.get_folder_by_name(elem, user.id)
            if check_folder:
                good_folders.add(elem)
            else:
                bad_folders.add(elem)
        # Delete folders
        for elem in good_folders:
            folder.delete_folder(elem, user.id)
            delete_dir(elem, user.id)
        return {
            "deleted": "; ".join(good_folders),
            "failed": "; ".join(bad_folders)
        }
    else:
        check_folder = folder.get_folder_by_name(data.name, user.id)
        if not check_folder:
            return {"message": "Fail! Folder with this name doesn't exist'"}
        folder.delete_folder(data.name, user.id)
        delete_dir(data.name, user.id)
        return {"message": "Successfully deleted the folder"}
