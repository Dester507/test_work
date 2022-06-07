import os


def save_file(
        user_id: int,
        folder_name: str,
        file_name: str,
        file
):
    file_path = f"app/folders/{user_id}/{folder_name}/{file_name}"
    full_path = os.path.join(os.getcwd(), file_path)
    try:
        contents = file.read()
        with open(full_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        length = len(contents)
        file.close()
        return length


def rename_file(old_name: str, new_name: str, folder_name: str, user_id: int):
    old_full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{folder_name}/{old_name}")
    new_full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{folder_name}/{new_name}")
    os.rename(old_full_path, new_full_path)


def delete_storage_file(user_id: int, folder_name: str, file_name: str):
    full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{folder_name}/{file_name}")
    os.remove(full_path)


def get_path_to_file(folder_name: str, file_name: str, user_id: int):
    full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{folder_name}/{file_name}")
    return full_path


def move_file_to_another_folder(old_folder: str, new_folder: str, file_name: str, user_id: int):
    old_full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{old_folder}/{file_name}")
    new_full_path = os.path.join(os.getcwd(), f"app/folders/{user_id}/{new_folder}/{file_name}")
    os.replace(old_full_path, new_full_path)
