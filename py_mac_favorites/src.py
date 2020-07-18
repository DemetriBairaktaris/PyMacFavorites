import os
from py_mac_favorites import favorites_file


def set_favorite(user: str, folder_path: str, refresh: bool = True) -> None:
    favorites_file.update_favorites(user, [folder_path], [])
    if refresh:
        favorites_file.refresh()


def get_favorites(user: str) -> list:
    return favorites_file.get_favorites(user)


def is_favorite(user: str, folder_path: str) -> bool:
    if not folder_path:
        raise Exception("folder_path argument is invalid: " + str(folder_path))

    folder_path = os.path.normpath(folder_path)
    favorites = [os.path.normpath(x) for x in get_favorites(user)]
    return folder_path in favorites


def delete_favorite(user: str, folder_path: str, refresh: bool = True) -> None:
    favorites_file.update_favorites(user, [], [folder_path])
    if refresh:
        favorites_file.refresh()
