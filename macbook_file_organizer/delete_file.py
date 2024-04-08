import os
import time
from typing import List

import send2trash

import Settings

DIR_TO_WATCH = Settings.DIR_TO_WATCH


def remove_items_older_than(days: int) -> None:
    """
    Removes files and folders present in the "DOWNLOAD_FOLDER_PATH" older than provided days.

    Args:
        days (int): Files and folders older than these many days will be removed.
    """
    file_paths_to_remove = [path
                            for path in get_all_file_paths_in_category_folder(DIR_TO_WATCH)
                            if _is_older_than(path, days)]

    for path in file_paths_to_remove:
        send2trash.send2trash(path)

    remove_empty_dirs()


def remove_empty_dirs() -> None:
    """
    Removes any empty directories present in the "DOWNLOAD_FOLDER_PATH" which are older than the provided days.
    """
    for dir_path, dir_names, file_names in os.walk(DIR_TO_WATCH, topdown=False):
        if is_empty_dir(dir_path):
            send2trash.send2trash(dir_path)


def is_empty_dir(folder_path: str) -> bool:
    """
    Checks if a given directory is empty or not.

    Args:
        folder_path (str): Path of the directory to be checked.

    Returns:
        bool: True if the directory is empty, False otherwise.
    """
    visible_files = [path
                     for path in os.listdir(folder_path)
                     if not os.path.basename(path).startswith('.')]

    return len(visible_files) == 0


def get_all_file_paths_in_category_folder(path: str) -> List[str]:
    """
    Returns all file paths in the given directory.

    Args:
        path (str): The directory in which to search for files.

    Returns:
        list: A list containing paths of all files in the given directory.
    """
    paths = []

    category_folder_paths = [os.path.join(path, dir)
                             for dir in os.listdir(path)
                             if _is_category_folder(os.path.join(path, dir))]

    for path in category_folder_paths:
        for root, subdirs, files in os.walk(path):
            subdirs_copy = subdirs[:]
            for subdir in subdirs_copy:
                if subdir.endswith('.app'):
                    paths.append(os.path.join(root, subdir))
                    subdirs.remove(subdir)

            for file in files:
                if not file.startswith('.'):
                    paths.append(os.path.join(root, file))

    return paths


def _is_older_than(path: str, days: int) -> bool:
    """
    Checks if a file or directory at a given path is older than certain days.

    Args:
        path ```python
        path (str): Path of the file or directory.
        days (int): Number of days to check against.

    Returns:
        bool: True if the file or directory is older than 'days', False otherwise.
    """
    current_timestamp = time.time()
    if current_timestamp - _get_epoch_ctime(path) >= _duration2seconds(days):
        return True
    else:
        return False


def _get_epoch_ctime(file_path: str) -> float:
    """
    Returns the creation time of a file or directory at a given path in seconds since the epoch.

    Args:
        file_path (str): Path of the file or directory.

    Returns:
        int: Creation time of the file or directory in seconds from the epoch.
    """
    return os.stat(file_path).st_birthtime


def _duration2seconds(days: int) -> int:
    """
    Converts days to seconds.

    Args:
        days (int): Number of days to be converted.

    Returns:
        int: The input number of days converted to seconds.
    """
    return days * 86400


def _is_category_folder(dir_path: str) -> bool:
    """
    Checks if a given directory is a category folder. A category folder is one that starts and ends with '*'.

    Args:
        dir_path (str): Path of the directory to be checked.

    Returns:
        bool: True if the directory is a category folder, False otherwise.
    """
    folder_name = os.path.basename(dir_path)

    if (((folder_name.startswith('*') and folder_name.endswith('*')) or
         (folder_name in ['Documents', 'Images', 'Audio', 'Video', 'Archives', 'E-books',
                          'Software and Others', 'Folder', 'Unknown'])) and os.path.isdir(dir_path)):
        return True
    else:
        return False


if __name__ == '__main__':
    remove_items_older_than(Settings.REMOVE_FILES_OLDER_THAN_DAYS)
