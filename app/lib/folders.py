import os
import shutil


def create_main_dir(user_id: int):
    folder_name = f"app/folders/{user_id}"
    full_path = os.path.join(os.getcwd(), folder_name)
    os.mkdir(full_path)


def create_dir(name: str, user_id: int):
    folder_name = f"app/folders/{user_id}/{name}"
    full_path = os.path.join(os.getcwd(), folder_name)
    os.mkdir(full_path)


def rename_dir(old_name: str, new_name: str, user_id: int):
    old_folder_name = f"app/folders/{user_id}/{old_name}"
    new_folder_name = f"app/folders/{user_id}/{new_name}"
    old_full_path = os.path.join(os.getcwd(), old_folder_name)
    new_full_path = os.path.join(os.getcwd(), new_folder_name)
    os.rename(old_full_path, new_full_path)


def delete_dir(name: str, user_id: int):
    folder_name = f"app/folders/{user_id}/{name}"
    full_path = os.path.join(os.getcwd(), folder_name)
    shutil.rmtree(full_path, ignore_errors=True)
