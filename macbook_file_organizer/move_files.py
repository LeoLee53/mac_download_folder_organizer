import datetime
import os
import shutil
import time

from Settings import DIR_TO_WATCH

DOWNLOAD_FOLDER_PATH = DIR_TO_WATCH


def move_file(file_path: str) -> None:
    """
    Moves a file to the appropriate destination path.

    Args:
        file_path (str): The path of the file to be moved.

    Returns:
        None
    """
    dst_path = _get_destination_path(file_path)

    _is_downloaded(file_path)

    os.makedirs(dst_path, exist_ok=True)

    try:
        shutil.move(file_path, dst_path)
    except OSError as e:
        basename = os.path.basename(file_path).split('.')[0]
        new_path = file_path.replace(basename, f'{basename}(1)')
        os.rename(file_path, new_path)
        shutil.move(new_path, dst_path)


def _is_downloaded(file_path):
    """
    Checks if a file has finished downloading by comparing its size at different time intervals.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file has finished downloading, False otherwise.
    """
    while True:
        old_file_size = os.stat(file_path).st_size
        time.sleep(1)
        new_file_size = os.stat(file_path).st_size

        if old_file_size == new_file_size:
            break


def _get_destination_path(file_path):
    """
    Get the destination path for a given file.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The destination path for the file.
    """
    c_year = _get_dir_cyear(file_path)
    destination_category_folder = _get_file_category_folder(file_path)

    return DOWNLOAD_FOLDER_PATH + '/*' + c_year + '*/' + destination_category_folder


def _get_file_category_folder(file_path):
    """
    Determines the category folder for a given file based on its extension.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The category folder name for the file. Possible values are:
            - "Documents"
            - "Images"
            - "Audio"
            - "Video"
            - "Archives"
            - "E-books"
            - "Software and Others"
            - "Folder" (for directories)
            - "Unknown" (if the file extension doesn't match any category)
    """
    category_map = {
        "Documents": {"pdf", "docx", "doc", "odt", "rtf", "tex", "log",
                      "msg", "wpd", "wps", "pptx", "ppt", "ods", "xlr",
                      "xls", "xlsx", "key", "pps", "ai", "ps", "svg",
                      "indd", "pct", "eps", "txt", "md", "html", "htm",
                      "xhtml", "xml", "csv", 'goodnotes'},

        "Images": {"jpg", "jpeg", "png", "heic", "gif", "bmp", "tif", "tiff",
                   "psd", "ai", "indd", "pct", "pdf", "eps", "svg", "ico"},

        "Audio": {"mp3", "m4a", "wav", "aac", "wma", "flac", "alac", "ogg",
                  "mid", "midi", "mpa", "cda", "aif"},

        "Video": {"mp4", "m4v", "mov", "wmv", "avi", "avchd", "flv", "swf",
                  "h264", "mkv", "3g2", "3gp", "h264", "rm", "vob", "webm"},

        "Archives": {"zip", "rar", "7z", "tar", "gz", "arj", "deb", "pkg", "rpm",
                     "tar.gz", "z", "bin"},

        "E-books": {"mobi", "epub", "azw", "azw3", "kf8", "fb2"},

        "Software and Others": {"app", "exe", "dmg", "bat", "cgi", "pl", "com",
                                "jar", "py", "wsf", "fnt", "fon", "otf", "ttf",
                                "rom", "sav", "bak", "cfg", "ini", "prf",
                                "torrent", "asp", "aspx", "cer", "cfm", "cgi",
                                "pl", "css", "htm", "html", "js", "jsp",
                                "part", "php", "py", "rss", "xhtml", "dat",
                                "db", "dbf", "mdb", "sql", "tar", "xml"},

        "Folder": {"folder"}
    }

    extension = _get_dir_extension(file_path)

    for category_folder, extensions in category_map.items():
        if extension in extensions:
            return category_folder

    return "Unknown"


def _get_dir_cyear(file_path):
    """
    Get the creation year of a file.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The creation year of the file.

    """
    return datetime.datetime.fromtimestamp(os.stat(file_path).st_birthtime).strftime('%Y')[:4]


def _get_dir_extension(file_path):
    """
    Get the extension of a file or return 'folder' if it's a directory.

    Args:
        file_path (str): The path of the file or directory.

    Returns:
        str: The extension of the file or 'folder' if it's a directory.
    """
    extension = os.path.splitext(file_path)[1]
    if extension == '':
        return 'folder'
    else:
        return os.path.splitext(file_path)[1][1:].lower()


def _get_dir_paths():
    """
    Get the directory paths of files in the download folder, excluding files with certain years in their names.

    Returns:
        A list of directory paths.
    """
    excluded_years = ['*2021*', '*2022*', '*2023*', '*2024*']

    return [os.path.join(DOWNLOAD_FOLDER_PATH, file_name)
            for file_name in os.listdir(DOWNLOAD_FOLDER_PATH)
            if not file_name.startswith('.') and
            not any(year in file_name for year in excluded_years)]
